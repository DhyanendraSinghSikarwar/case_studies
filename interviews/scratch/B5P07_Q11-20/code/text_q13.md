**Pattern:** Post-order combine on a binary tree (no ordering to exploit, so the answer has to be found by looking at both sides).

**Say this first (1 line):** "Recurse on both children. A call returns its node if it matches p or q, otherwise whatever the children found. The first node where both sides report a hit is the LCA."

**Brute force:**
- Find the root-to-p path and the root-to-q path (store the nodes), then walk both from the root and keep the last node they share.
- O(n) time and O(n) space for the paths. Perfectly fine, but two passes and extra memory. I use it as the oracle.

**Optimal:**
- `go(n)`: if `n` is None or matches p or q, return `n`. Otherwise `l = go(left)`, `r = go(right)`.
- If both `l` and `r` are non-None, p and q are on different sides, so `n` is the LCA. Else return whichever is non-None (or None).
- Why returning early at a match is correct when both values exist: when `go` reaches p, either q is below p (so p is the LCA, and nothing below p needs checking), or q is somewhere else and will be reported by another branch, so a higher node sees two hits. Either way the right node wins.
- If a value may be missing: that argument breaks. With q absent, the early return hands back p's node as if it were an LCA. Fix: visit both children before testing the node and count matches. Return the answer only if the count is 2 (or do a second pass to confirm both exist). The code has `lca_safe`.

**Complexity:** Time O(n), each node once. Space O(h) recursion: O(log n) balanced, O(n) on a chain. The parent-map version is O(n) time and space but iterative.

**Dry run:** `[3,5,1,6,2,0,8,null,null,7,4]`, p=6, q=4. At 3: go(5) and go(1). At 5: go(6) matches, returns 6. go(2): go(7) none, go(4) matches, returns 4, so 2 returns 4. At 5: both sides hit, return 5. At 1: nothing found, None. At 3: left is 5, right is None, return 5. Answer 5.

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- p is an ancestor of q: the early return gives p (the examples `p=5, q=4` and `[1, 2]`).
- p and q at the deepest level on a chain of 20000 nodes: recursion raises `RecursionError`; the parent-map version is iterative and fine.
- Missing value: the run shows the early-return version "answers" in every one of the 4081 cases where q is absent, while the counting version returns None each time.
- Values are distinct per the prompt. With duplicate values you would match by node reference, not by value.

**Follow-ups:**
- It is a BST? Use the ordering and go left or right, O(h) with no full traversal. That is Q6 in this part: the LCA is the first node whose value lies between p and q.
- Many LCA queries on one tree? Preprocess with Euler tour plus sparse table or binary lifting; each query becomes O(1) or O(log n).
- Do it without recursion? Build a parent map (as in the code), mark p's ancestors in a set, then climb from q.

**Common mistakes:**
- Comparing `n.val == p` without handling None first.
- Trusting the early-return version when a value can be absent.
- Returning a value instead of a node from the helper, then being unable to tell "found nothing" from "found value 0".
- Treating "a node is its own descendant" wrongly: the LCA of 5 and 4 where 5 is above 4 is 5, not 3.
