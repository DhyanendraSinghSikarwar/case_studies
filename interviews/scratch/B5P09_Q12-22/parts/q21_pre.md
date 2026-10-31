**Pattern:** Two-colouring a graph with BFS (or DFS). A graph is bipartite exactly when it has no odd cycle, and the colouring check finds one if it exists.

**Say this first (1 line):** "Colour a start node 0, give every neighbour the other colour, and if an edge ever joins two nodes of the same colour it is not bipartite; restart from every unseen node because the graph may be disconnected."

**Brute force:** Try all 2^n assignments of side 0 or 1 and test every edge. O(2^n * E). Only usable for n <= 20; it is my checker.

**Optimal:**
- `color = [-1] * n`. For each `s` with `color[s] == -1`: colour it 0, BFS.
- For `u` popped and each neighbour `v`: if `v` is uncoloured, give it `1 - color[u]` and enqueue; else if `color[v] == color[u]`, return False.
- If every component finishes cleanly, return True.
- Link to odd cycles: in BFS every edge joins nodes whose depths differ by 0 or 1. A same-colour edge means equal depths, and the two paths back to their common ancestor plus that edge form an odd cycle. Conversely an odd cycle can never be coloured with 2 colours (colours must alternate around it). So "no conflict found" is equivalent to "no odd cycle".
- The run checks this equivalence on all 1099 graphs with up to 5 nodes, against both the 2^n brute force and a separate BFS-layer odd-cycle test.
- A node with no edges is its own component and always fine.

**Complexity:** O(V + E) time (each node queued once, each adjacency entry read once), O(V) space for colours and the queue. All iterative: V is 10^5, so a recursive DFS would exceed CPython's recursion limit of 1000.

**Dry run:** `[[1,2],[0,2],[0,1]]` (a triangle).
- Colour 0 -> 0. Neighbours 1 and 2 get colour 1; queue [1, 2].
- Pop 1: neighbour 0 has colour 0 != 1, fine; neighbour 2 has colour 1 == colour of 1: conflict, return False.
- A 4-cycle `[[1,3],[0,2],[1,3],[0,2]]` colours 0,1,0,1 with no conflict: True.
