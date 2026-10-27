**Pattern:** Tree recursion with inherited constraints (top-down), or the BST property "inorder is sorted". Same fact, two views.

**Say this first (1 line):** "A node is valid only if it fits the open interval (low, high) set by ALL its ancestors, so I pass the bounds down, using None for 'no bound'. Or I run an inorder walk and check it is strictly increasing."

**Brute force:**
- For every node, scan its whole left subtree (all values must be smaller) and right subtree (all larger).
- Correct, but each node scans its subtree: O(n^2) on a chain. I use it below as the oracle.

**Optimal:**
- Bounds: `ok(node, low, high)`. A None node is fine. Otherwise `low < node.val < high` must hold. Go left with `(low, node.val)` and right with `(node.val, high)`.
- Invariant: every value in the subtree must lie strictly between `low` and `high`. Going left, the parent becomes the new upper bound but the lower bound from further up is kept, so a deep node is checked against every ancestor.
- Inorder: iterative stack walk, keep the previous value, fail if `cur <= prev`. The `<=` is what makes duplicates invalid.
- Why parent-only fails: `[5, 4, 6, null, null, 3, 7]`. Node 6 is a valid right child of 5, and 3 is a valid left child of 6, but 3 sits in the right subtree of 5, so it must be greater than 5.
- Why sentinels like `-2**31` fail: the tree `[-2147483648]` is valid but `val <= low` rejects it. Use None (or `float("-inf")`, which compares with ints fine).

**Complexity:** Time O(n), each node once. Space O(h) for the recursion or the stack: O(log n) balanced, O(n) on a chain.

**Dry run:** `[5, 1, 4, null, null, 3, 6]`. Root 5 with bounds (None, None): ok. Left child 1 with (None, 5): ok. Right child 4 with (5, None): `4 <= 5` so False. Answer False, found at the first right-subtree node, before ever looking at 3 and 6.

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Empty tree: True. Single node: True, even `-2**31`.
- Duplicates anywhere: False (strict on both sides), including `[2, 2, 2]` and a duplicate far below.
- Extremes `-2**31` and `2**31 - 1`: use None bounds, not sentinels.
- A chain of 5000 nodes: recursive bounds hits `RecursionError` at the default limit of 1000; use the iterative inorder (or an explicit stack of `(node, low, high)`).

**Follow-ups:**
- Allow duplicates on the left only? Say the rule out loud first, then make the bound inclusive on that side only: the left-going `high` rejects `val > high` instead of `val >= high`, and the right side stays strict.
- Which is better? Same big-O. Inorder is shorter to write iteratively and stops early; bounds also generalises to "each node must lie in a range".
- Why is checking only inorder sortedness enough? A tree is a BST exactly when its inorder sequence is strictly increasing, and the code tests that directly.

**Common mistakes:**
- Comparing each node only with its parent.
- Using `<` where `<=` is needed (accepting duplicates).
- Sentinels `-2**31` and `2**31 - 1`.
- Starting an inorder `prev` at 0 or a sentinel instead of None.
