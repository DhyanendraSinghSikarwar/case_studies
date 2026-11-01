**Pattern:** Same-tree check run at every node (O(n * m)), or serialize both trees and use a substring search.

**Say this first (1 line):** "For every node in root I ask 'is the tree below you identical to sub?' with the same-tree check. That is O(n * m). The alternative is serialization with null markers and delimiters, then a substring test."

**Brute force / baseline:**
- Visit each node of `root`; call `is_same(node, sub)`, which compares values and both children, treating None carefully (`a is b` when either is None).
- "Identical" means down to the leaves: a node with extra descendants does not count (the second example).
- Cost: each `is_same` call from one start node touches at most 2m + 1 calls (every call with a non-None sub node is a distinct node of sub, and every call with a None sub node is a child of one of them). So at most `n * (2m + 1)` calls in total: O(n * m). The run checks this bound for every pair of small trees.

**Optimal / alternative:**
- Serialize both trees as preorder with a null marker for every missing child and a delimiter before every token, for example `,3,4,1,#,#,2,#,#,5,#,#`. Then `ser(sub) in ser(root)`.
- Why this is right: the marker string is self-delimiting (it parses to exactly one tree, as in Q18), and every token starts with a comma, so a match must start at a token boundary. It then parses as a whole subtree beginning at that node.
- Why both parts are needed: without delimiters, `12` contains `2` (root `[12]` against sub `[2]`; the run shows the wrong answer). Without markers, `[1, null, 2]` and `[1, 2]` both give `,1,2`, so a root with a right child "contains" the sub with a left child (the run shows it). With markers but no delimiters `12##` still contains `2##`.
- The substring test with Python's `in` is fast in practice. The worst-case guarantee needs KMP or a hash-based search over the token list, giving O(n + m).

**Complexity:** Same-tree approach: time O(n * m) worst case (for example a chain of ones against a chain of ones ending in a 2: the run measures 120198 calls for n = 400, m = 200, bound 160400), space O(h) recursion. Serialization: O(n + m) to build the strings and the substring test's cost, space O(n + m).

**Dry run:** `root=[3, 4, 5, 1, 2]`, `sub=[4, 1, 2]`. At node 3: values differ, no. At node 4: values equal, then 1 vs 1 (both children None on each side: equal), 2 vs 2: True. Second example: the node 4 matches but its child 2 has a child 0 while `sub` has None there, so `a is b` fails: False.

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- `sub` equal to the whole root: True. Root a single node: only a single-node sub with the same value matches.
- Repeated values (`[1, 1]` against `[1]`): the second node matches.
- Extra descendants below the match (second example): False.
- `12` versus `2`: delimiters needed.
- Deep chains: recursive `is_same` is limited by the recursion limit; the chain test uses a right chain of 400 nodes, which is safe, and a real 2000-node chain needs the iterative approach (the iterative serializer above has no recursion).

**Follow-ups:**
- Faster than O(n * m)? Serialization plus KMP, or hash every subtree (Merkle-style hash with canonical ids) and compare the hash of `sub` with every node's hash: O(n + m) expected.
- Why not compare only heights or sizes first? It is a good prune: skip `is_same` when the sizes differ.
- Count how many nodes root has with sub as their subtree? Same hashing, count matches.

**Common mistakes:**
- Calling `is_same` only at the root.
- Treating "contains the same values below" as a match (extra descendants must not match).
- Serializing without markers or without delimiters.
- Writing `a == b` on node objects (compares identity, not structure).
