**Pattern:** Divide and conquer on traversal order. Preorder tells you the root, inorder tells you the sizes of the left and right parts.

**Say this first (1 line):** "The first preorder value is the root. Find it in inorder: everything left of it is the left subtree, everything right is the right subtree. I use a dict for that position and a moving preorder pointer, so it is O(n)."

**Brute force:** Take `pre[0]` as the root, `ino.index(root)` to find the split, and recurse on slices `pre[1:i+1], ino[:i]` and `pre[i+1:], ino[i+1:]`. `index` is O(n) and slicing copies, so each level costs O(n) and a chain costs O(n^2). The run counts the copied elements: 9900, 39800, 159600 for n = 100, 200, 400, which is about n^2.

**Optimal:**
- Build `pos = {value: inorder index}` once. Keep a pointer `p` into `pre`.
- `go(lo, hi)` builds the subtree whose inorder range is `ino[lo:hi]`. If empty, return None. Otherwise the root is `pre[p]` (then `p += 1`), `i = pos[root.val]`, left is `go(lo, i)`, right is `go(i + 1, hi)`.
- Left must be built first. Preorder is root, left part, right part, so the pointer reaches the right subtree's root only after the whole left part is consumed.
- Distinct values are required so that `pos` is well defined.
- Why the pair is unique: the root is forced (first of preorder), its inorder position fixes how many nodes are on each side, and the same argument applies inside each side. By induction there is exactly one tree. I also checked it by running: for every shape up to 7 nodes (625 non-empty shapes) all (preorder, inorder) pairs are different.
- Why preorder alone is not enough: for `[1, 2]` the tree can be 2 as the left child or 2 as the right child. The run shows that all 429 shapes with 7 nodes have the same preorder when labelled in preorder, so the sequence says nothing about the shape.

**Complexity:** Time O(n): one dict build, then O(1) per node. Space O(n) for the dict plus O(h) recursion. Slicing plus `index`: O(n^2) time.

**Dry run:** `pre=[3,9,20,15,7]`, `ino=[9,3,15,20,7]`. Root 3 at inorder index 1: left range `[0,1)`, right range `[2,5)`. Left: root 9, ranges empty both sides. Right: next preorder is 20 at index 3: left range `[2,3)` gives 15, right range `[4,5)` gives 7. Tree `[3, 9, 20, null, null, 15, 7]`.

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- One node. A chain going right (`pre == ino`) and a chain going left (`ino` reversed).
- Depth: a skewed tree of 3000 nodes is within the stated limit, but the recursive build needs depth 3000 and raises `RecursionError` at the default limit of 1000. Either raise the limit (`sys.setrecursionlimit`, and be aware the C stack can still overflow for big values) or use the iterative stack version in the code, which handles it.
- Duplicate values would break `pos`; the prompt rules them out.
- Inputs that are not a valid pair (different sets of values) raise `KeyError` or `IndexError`. Say you would validate first if the input is untrusted.

**Follow-ups:**
- Inorder plus postorder? Same idea, the root is the last postorder value and you build the right subtree first (Q29).
- Preorder plus postorder? Not unique in general (e.g. a single child can be left or right); unique only for full binary trees.
- Why not preorder plus level order? Possible but more complex; the inorder split is what gives the sizes.

**Common mistakes:**
- Building the right subtree before the left with a shared preorder pointer.
- Slicing lists and using `index` (O(n^2)).
- Off-by-one in the slice bounds when slicing (the left part of preorder is `pre[1:i+1]` only when `i` counts from the start of the current range).
- Mutating `pre` with `pop(0)` (O(n) each).
