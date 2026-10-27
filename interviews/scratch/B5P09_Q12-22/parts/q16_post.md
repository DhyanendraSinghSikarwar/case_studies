**Edge cases:**
- No edges: only the source is reached, entries 0, cells n.
- Unreachable parts of the graph cost nothing in the list version (never dequeued).
- Directed versus undirected: the same edge list gives different entry counts (E versus 2E for the part that is reached).
- The count is for BFS that marks on enqueue; marking on dequeue would examine entries of duplicates too.

**Follow-ups:**
- When is a matrix the right choice? Dense graphs, and when you need O(1) "is there an edge u-v" (Floyd-Warshall also wants it).
- Edge list as the storage? Neighbour lookup is O(E) per node, so BFS becomes O(V * E); build lists first (Kruskal is the case where an edge list is natural).
- Memory for V = 10^5? A matrix would be 10^10 cells, impossible; lists are the only option.

**Common mistakes:**
- Saying undirected BFS is O(E) with no 2: the work is 2E entries, same order but worth saying.
- Claiming BFS is O(V + E) for a matrix input: it is O(V^2).
- Writing Dijkstra as O(E log E) without noting it equals O(E log V).
- Counting all n nodes instead of only reached nodes in the matrix cost.
