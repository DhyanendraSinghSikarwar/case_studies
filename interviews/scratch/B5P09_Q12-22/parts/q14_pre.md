**Pattern:** Union-find as an online cycle detector. Add edges one by one; the first edge whose two ends are already in the same set closes a cycle.

**Say this first (1 line):** "Scan the edges with union-find and return the first edge whose endpoints already share a root; that is the last edge of the cycle in input order."

**Brute force:** For each edge from the back, remove it and test whether the other n - 1 edges still connect all nodes (DFS). The first one that keeps the graph connected is the answer. O(n) edges times O(n) DFS = O(n^2), about 10^6 for n = 1000. Fine here, and it is the checker.

**Optimal:**
- `parent[i] = i` for nodes 1..n.
- For each `[u, v]` in order: find both roots. Equal: return `[u, v]`. Different: link them.
- Why this is exactly the wanted edge: the graph is a tree plus one edge, so it has exactly one cycle. Before the scan reaches the last cycle edge, the cycle's edges seen so far form a path (no cycle yet), so no earlier edge finds its ends already joined. When the last cycle edge arrives, the rest of the cycle is already there, so its ends are joined. Edges not on the cycle can never have both ends joined by earlier edges, because the only second route between two nodes goes around the cycle.
- Every cycle edge can be removed (removing any edge of a cycle leaves a spanning tree), and the one that appears last in the list is the one the scan returns.

**Complexity:** O(n * alpha(n)) time, O(n) space. A single pass.

**Dry run:** `edges=[[1,4],[3,4],[1,3],[1,2],[4,5]]`.
- [1,4]: roots 1,4 differ, link. [3,4]: 3 and root of 4 differ, link (now {1,3,4}).
- [1,3]: both already in {1,3,4}, same root, return `[1, 3]`.
- Cycle is 1-4-3-1 with edges [1,4],[3,4],[1,3]; the last of them in the list is [1,3]. Correct.
