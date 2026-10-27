**Pattern:** Inorder traversal of a BST visits values in sorted order, so the k-th smallest is the k-th node visited. Stop early.

**Say this first (1 line):** "Inorder of a BST is sorted, so I walk inorder with an explicit stack and return on the k-th pop. That is O(h + k) time and O(h) space."

**Brute force:** Do a full inorder walk into a list and return `list[k - 1]`. O(n) time and O(n) space. Even simpler and worse: dump all values and sort, O(n log n).

**Optimal:**
- Push the left spine, pop a node (that is the next smallest), count it, then move to its right child and push that child's left spine.
- Return the moment the count reaches k. Nothing after the k-th node is ever touched.
- The stack only ever holds the ancestors of the current node, so at most h nodes. Pushes are at most `k + h - 1`: every popped node was pushed, and fewer than h are left on the stack.
- Follow-up (frequent queries on a changing tree): store `size` (nodes in the subtree) in each node. At node n with `left = size(n.left)`: if `k == left + 1` the answer is n; if `k <= left` go left; else `k -= left + 1` and go right. That is O(h) per query. Every insert or delete must add or subtract 1 on every ancestor on the path (O(h) extra work), and rotations in a balanced tree must recompute the sizes of the two nodes they move.

**Complexity:** Time O(h + k): at most h pushes to reach the first node, then k pops. Space O(h). With sizes: O(h) per query, O(h) per update, O(n) extra space for the size field. In a balanced tree h is O(log n); on a chain it is n.

**Dry run:** `[5, 3, 6, 2, 4, null, null, 1]`, k=3. Push 5, 3, 2, 1 (stack `[5,3,2,1]`). Pop 1, k=2 left. 1 has no right. Pop 2, k=1. 2 has no right child. Pop 3, k=0, return 3. We never touched 4 or 6.

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- k = 1: the leftmost node. k = n: the rightmost, the walk visits the whole tree.
- One node.
- Chain of 10^4 nodes: the iterative walk is fine (a recursive walk would raise `RecursionError`).
- Duplicates are excluded by the prompt. With duplicates you would count occurrences and need a clear rule.
- k out of range: the code raises `ValueError` instead of returning garbage.

**Follow-ups:**
- Many queries, tree changes often: size field as above, O(h) per query and update.
- Tree never changes, many queries? Store the sorted inorder array once, then each query is O(1).
- k-th largest? Mirror the walk (right first), or ask for the `(n - k + 1)`-th smallest if you know n.

**Common mistakes:**
- A recursive walk that collects everything and then indexes (O(n) when O(h + k) is possible).
- Off-by-one: decrementing k before or after the check.
- Not restoring `cur = cur.right` after a pop, so the walk loops or skips a subtree.
- Forgetting to update the size of every ancestor on insert and delete.
