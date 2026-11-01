**Pattern:** Shortest path to a leaf in a tree: BFS stops at the first leaf; recursion needs a special case for nodes with one child.

**Say this first (1 line):** "A leaf has no children, so a node with one child is not a leaf. If one side is empty I must use the other side, not take `1 + min` of an empty 0. Or I do BFS and return the depth of the first leaf I meet."

**Brute force:** Collect the depth of every leaf and take the minimum: O(n) time, O(h) to O(w) space. This is correct but always touches every node. I use it as the oracle.

**Optimal:**
- Recursive: `None` gives 0. If `left` is None return `1 + depth(right)`. If `right` is None return `1 + depth(left)`. Otherwise `1 + min(depth(left), depth(right))`.
- Why `1 + min(l, r)` alone is wrong: for a node with one child, the empty side returns 0, so the formula says the node is a leaf at depth 1. For `[1, 2]` it answers 1, but the root is not a leaf; the only leaf is 2, at depth 2. The run shows the wrong answers (1 for `[1, 2]`, 1 for the chain with expected 5) and that it fails on 496 of 626 small shapes.
- BFS: process the tree level by level; the first node with no children is the shallowest leaf, so return the current depth immediately. No case analysis on one-child nodes is needed.
- Which does less work: on a perfect tree of height 10 (1023 nodes) the recursion visits all 1023 nodes while BFS stops after popping 512 (the 511 internal nodes plus the first leaf), about half. On a long chain both visit every node (500 and 500). On a tree with a shallow leaf beside a long chain BFS pops 2 nodes and the plain recursion still visits 500.
- Space: BFS holds up to a whole level (about n/2 on the perfect tree) but only 1 node at a time on a chain; recursion holds up to the height (n on a chain).

**Complexity:** Time O(n) worst case for both (recursion always O(n); BFS O(n) worst, often far less because it stops at the first leaf, at most all nodes on levels above the shallowest leaf). Space: recursion O(h); BFS O(w), the widest level.

**Dry run:** `[3, 9, 20, null, null, 15, 7]`. BFS: depth 1, queue `[3]`: 3 has children. Depth 2, queue `[9, 20]`: pop 9, no children, it is a leaf, return 2. Never looks at 15 or 7. Recursive: node 3 has two children, so `1 + min(depth(9), depth(20))` is `1 + min(1, 2) = 2`.

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Empty tree: 0. Single node: 1 (it is a leaf).
- A root with one child (`[1, 2]`): 2, not 1.
- A chain: the depth is n, the case where the one-child rule matters most.
- n up to 10^5: a 100000-node chain makes the recursive version raise `RecursionError` at the default limit of 1000 (the run shows it); BFS handles it. A plain recursion limit of 1000 already fails at about 1000 nodes, so for the stated bound use BFS or an explicit stack.

**Follow-ups:**
- Count edges instead of nodes? Subtract 1 for a non-empty tree.
- Maximum depth? Plain `1 + max(l, r)` works, since an empty side never wins a max (Q2).
- Can recursion stop early too? Yes: DFS with a global `best` that prunes any branch already deeper than `best`, but the worst case is still O(n).

**Common mistakes:**
- `1 + min(left, right)` without the one-child case.
- Treating a node with one child as a leaf.
- Returning the BFS depth after the whole level instead of at the first leaf (still correct, but loses the early exit).
- Off-by-one: starting the depth at 0 and counting edges.
