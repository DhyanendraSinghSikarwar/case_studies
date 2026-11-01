**Pattern:** Disjoint-set union (union-find). It answers "are these two in the same group" and "merge two groups" in near-constant amortised time, with no graph traversal.

**Say this first (1 line):** "Parent array, iterative find with path compression, union by size; the set count drops by one on each real merge, and I track the largest size from the root's size."

**Brute force:** Keep a label per node. `connected` compares two labels, O(1). `union` relabels every node of one group, O(n). Total O(n * ops) = 10^5 * 2*10^5 = 2*10^10. Too slow, but it is the checker.

**Optimal:**
- `parent[i] = i`, `size[i] = 1`.
- `find(x)`: walk up to the root, then walk again and point every node on the path at the root (path compression). Written as two loops, not recursion.
- `union(a, b)`: find both roots. Same root: return False. Else hang the smaller tree under the larger, add sizes, `sets -= 1`, return True.
- `connected` is just `find(a) == find(b)` and changes nothing structurally that matters (compression only shortens paths).
- Largest set at the end: `max(size[find(i)])`, or track it on each merge.
- Why iterative: without union by size, `union(i, i+1)` repeated can make a 10^5 chain; a recursive `find` on it hits CPython's limit of 1000 (the run below shows the RecursionError).

**Complexity:**
- With both tricks, m operations on n elements cost O(m * alpha(n)) amortised, where alpha is the inverse Ackermann function (at most 4 for any n you can store). Treat it as constant.
- By size alone (no compression): a node at depth h sits in a set of size >= 2^h, so depth <= log2 n and every find is O(log n) worst case. The run checks this.
- Compression alone: a single find can still be O(n) once, but it flattens the path, and the amortised cost over m ops is O(log n) per op.
- Space O(n).

**Dry run:** `n=5` and the first example.
- union(0,1): roots 0,1 differ, sizes 1,1, tie so root 0 stays, parent[1]=0, size[0]=2, sets=4, True.
- union(1,2): find(1)=0, find(2)=2, size[0]=2 >= 1, parent[2]=0, size[0]=3, sets=3, True.
- connected(0,2): both root 0, True. union(0,2): same root, False. connected(3,4): roots 3 and 4, False.
- Result `[[True, True, True, False, False], 3, 3]`.
