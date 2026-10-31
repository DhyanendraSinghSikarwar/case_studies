**Pattern:** Single-source shortest path with non-negative weights: Dijkstra with a binary heap. The answer is the largest shortest distance (the signal reaches the last node then), or -1 if any node has distance infinity.

**Say this first (1 line):** "Dijkstra with heapq and lazy deletion: push on every improvement, skip stale pops, answer is max distance or -1; it needs weights >= 0."

**Brute force:** Bellman-Ford. Relax every edge, repeat n times. O(V * E) = 10^5 * 2*10^5 = 2*10^10. Too slow, but it is a fine checker and it also copes with negative weights.

**Optimal:**
- `dist[k] = 0`, heap holds `(distance, node)`.
- Pop the smallest. If `d > dist[u]` the entry is stale (a better one was pushed later), skip it.
- Otherwise relax each edge `u -> v`: if `d + w < dist[v]`, update and push `(d + w, v)`.
- `heapq` has no decrease-key, so we push a duplicate and ignore the old one when it surfaces (same trick as Part 8 Q31).
- Invariant: when a node is popped non-stale, its distance is final. Any other path must leave the settled set through an edge to a node whose heap key is >= d, and weights are >= 0, so it cannot be shorter.
- Why non-negative: with a negative edge, a node popped earlier could still be improved later through that edge. The invariant breaks. Use Bellman-Ford then.
- Ties: the heap entries are `(int, int)` so ties compare on the node and never raise TypeError (Part 8 Q29 covers tied unorderable payloads).

**Complexity:**
- Each push comes from a successful relaxation, so pushes <= E + 1 (the +1 is the source). Each pop costs O(log heap size) and log(E + 1) <= 2 log V, so O(log V).
- Time O((V + E) log V). Space O(V + E) for adjacency lists plus up to E + 1 heap entries.
- Zero weights are fine. Repeated edges and self loops are harmless: a self loop never improves anything.

**Dry run:** `n=3, times=[[1,2,5],[1,3,2],[3,2,1]], k=1`.
- Heap `[(0,1)]`. Pop (0,1): relax 1->2 gives dist[2]=5, push (5,2); relax 1->3 gives dist[3]=2, push (2,3).
- Pop (2,3): relax 3->2: 2+1=3 < 5, dist[2]=3, push (3,2).
- Pop (3,2): fine, no out edges. Pop (5,2): 5 > 3, stale, skip.
- dist = [0, 3, 2], max = 3.
