**Pattern:** Cost model of graph storage. BFS is the same algorithm either way; what changes is how much it costs to ask "who are the neighbours of u".

**Say this first (1 line):** "BFS touches each reached node once and scans its neighbours: with lists that is the out-degree, so O(V + E); with a matrix it is a whole row of n cells, so O(V^2)."

**Brute force:** Not a different algorithm here. The "brute" is the matrix version: build an n x n matrix and scan a full row per dequeued node. It is also my checker, because it counts cells by actually scanning.

**Optimal:** Adjacency lists, with BFS marking nodes when they are enqueued.
- `reached`: nodes dequeued (each at most once, since marked on enqueue).
- `entries_list`: for each dequeued node add `len(adj[u])`. In an undirected graph an edge `[u, v]` is stored in both lists, so it is examined from each end.
- `cells_matrix`: `n * reached`, because the row of a node is scanned in full whether it has 1 neighbour or 50.

**Complexity:**
- BFS or DFS with lists: each node dequeued once, each list entry examined once. Entries sum to E (directed) or 2E (undirected). Time O(V + E), space O(V + E) for the lists plus O(V) for the queue and seen set.
- With a matrix: O(V) rows times O(V) cells = O(V^2) time, O(V^2) space. Better only when the graph is dense (E near V^2); then V^2 and V + E are the same order.
- Dijkstra with a binary heap: at most E + 1 pushes, each push and pop O(log heap size). In a simple graph E <= V^2, so log E <= 2 log V, and the heap work is O(E log V). Add the V + E scanning: O((V + E) log V).
- Check the claim on small graphs: the run tries every directed graph on up to 4 nodes and every undirected one, and `E <= n^2` and `entries <= E or 2E` hold in all of them.

**Dry run:** `n=5, edges=[[0,1],[1,2],[2,0],[3,4]]`, undirected, src 0.
- Lists: 0:[1,2], 1:[0,2], 2:[1,0], 3:[4], 4:[3].
- Dequeue 0 (2 entries), then 1 (2), then 2 (2). Nodes 3 and 4 are never reached.
- reached = 3, entries = 2 + 2 + 2 = 6, cells = 3 rows * 5 = 15. Answer `[3, 6, 15]`.
