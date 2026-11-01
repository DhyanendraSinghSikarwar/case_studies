**Pattern:** Cycle detection in an undirected multigraph with an iterative DFS. A cycle exists when a traversal reaches an already-seen node by an edge other than the one it arrived by.

**Say this first (1 line):** "Iterative DFS where each stack entry carries the index of the edge I came by; I skip only that exact edge, and any other edge to a seen node is a cycle. Self loops and repeated pairs are cycles automatically."

**Brute force:** For each edge, remove it and check with a DFS whether its two ends are still connected; a self loop counts at once. O(E * (V + E)), about 6 * 10^10 at the limits. It is my checker.

**Optimal:**
- Adjacency lists of `(neighbour, edge_index)`, each edge stored at both ends (a self loop lands twice in the same list).
- For each unseen start: mark it, push `(start, -1)`.
- Pop `(u, arrived_by)`. For each `(v, i)` in `adj[u]`: if `i == arrived_by` skip (that is the edge we just walked). Else if `v` is seen, return True. Else mark `v`, push `(v, i)`.
- Why this is correct: in a forest, a DFS only ever meets a seen node through the tree edge it arrived by. Any other edge to a seen node closes a cycle, including a parallel edge (a different index, same endpoints) and a self loop (a different index leading to the node itself).
- Why the edge index and not the parent node: skipping "the parent node" skips every edge to the parent, so a second copy of that edge is skipped too. The run shows what happens in practice. With list adjacency, the parent's own loop still meets the second copy later and finds the node seen, so the cycle is reported anyway. The bug is real when repeated edges are collapsed: with a `set` or `dict` of neighbours (very common) the second copy is gone and `[[0, 1], [0, 1]]` is wrongly called acyclic. Tracking the edge index makes the answer right for any storage that keeps each edge.
- A union-find alternative also works: an edge whose ends already share a root closes a cycle, and a repeated edge or self loop does so trivially.

**Complexity:** O(V + E) time with the DFS (each node pushed once, each adjacency entry read once), O(V + E) space. The explicit stack replaces recursion: a path of 10^5 nodes is deeper than CPython's limit of 1000 and would raise RecursionError (the run shows it at 5000).

**Dry run:** `n=2, edges=[[0,1],[1,0]]`.
- adj[0] = [(1,0),(1,1)], adj[1] = [(0,0),(0,1)]. Start 0, stack [(0,-1)].
- Pop (0,-1): (1,0): 1 unseen, mark it, push (1,0). (1,1): 1 is seen and 1 != -1: return True.
- With a set-based "parent node" version adj[0] = {1}: only one entry, no cycle found: wrong.
