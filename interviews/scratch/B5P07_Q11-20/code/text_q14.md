**Pattern:** Level-order traversal (BFS), or depth-first with a depth counter and "first to reach a depth wins".

**Say this first (1 line):** "The right view is the last node of every level. BFS gives it directly. DFS also works if I go right first and record the first node I meet at each new depth."

**Brute force:**
- Collect every level into a list of lists, then take the last element of each. O(n) time, O(n) extra space for the stored levels. It works, it just stores more than needed.
- My independent check gives every node a heap-style index (root 1, children `2i` and `2i+1`) and keeps the largest index per depth.

**Optimal:**
- BFS: at the start of each round the queue holds exactly one level. Its last element, `q[-1]`, is the visible node. Then pop the `len(q)` nodes of that level and push their children.
- DFS: `go(node, depth)`. If `depth == len(out)`, this is the first node at that depth, and because we visit right before left it is the rightmost one, so append it. Then recurse right, then left.
- Why not just the right spine: the view shows a left-side node whenever the right side is shorter. In `[1, 2, 3, 4]`, node 4 is the only node at depth 2 (3 has no children), so it is visible even though it hangs on the left. The spine gives `[1, 3]`, the view is `[1, 3, 4]`.

**Complexity:** Time O(n) both ways. Space: BFS O(w) (the widest level, up to n/2). DFS O(h) (n on a chain, log n balanced). Pick DFS on a wide shallow tree, BFS on a tall thin one.

**Dry run:** `[1, 2, 3, null, 5, null, 4]`. Level 0 queue `[1]`: last is 1. Level 1 queue `[2, 3]`: last is 3. Level 2 queue `[5, 4]` (children of 2 then 3): last is 4. Answer `[1, 3, 4]`. DFS: depth 0 sees 1, goes right to 3 (depth 1, new, record), goes right to 4 (depth 2, new, record), back up, then 3's left is None, then 2 at depth 1 (already recorded), then 5 at depth 2 (already recorded).

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Empty tree: `[]`.
- Left-only chain: every node is visible, so the answer is the whole chain (10^4 nodes: recursive DFS hits `RecursionError` under the default limit; BFS and the explicit-stack DFS are fine).
- Repeated values: no problem, we record nodes by level, not by value.
- A left subtree deeper than the right: its extra levels show through (`[1, 2, 3, 4]`).

**Follow-ups:**
- Left side view? Same code with left first (BFS: `q[0]`).
- Both views, or the full vertical view? That is the vertical order question (Q28).
- Why does DFS need the depth check? Without it you would append every node.

**Common mistakes:**
- Following only `.right` pointers.
- Reading `q[-1]` after popping the level instead of before.
- Forgetting that DFS must go right first.
- Looping `while q` for the level instead of `range(len(q))`, which mixes levels together.
