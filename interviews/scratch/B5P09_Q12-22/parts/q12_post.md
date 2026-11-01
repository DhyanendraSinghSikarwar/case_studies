**Edge cases:**
- n = 1 and no edges: answer 0.
- Source cannot reach some node: -1 (check `max(dist) == INF`).
- Self loops, repeated edges with different weights (the cheapest wins), zero-weight edges.
- Nodes are 1-indexed, so allocate n + 1 and ignore index 0 when taking the max.
- Do not forget that the answer is the max over all nodes, not the distance to one target.

**Follow-ups:**
- Negative edges? Dijkstra with finalise-on-pop gives wrong answers (the run above shows 1 instead of -1). Use Bellman-Ford O(V E), and a negative cycle reachable from k makes distances undefined.
- Dense graph, V^2 ~ E? An O(V^2) array Dijkstra without a heap can win.
- Weights only 0 or 1? 0-1 BFS with a deque gives O(V + E).

**Common mistakes:**
- Marking a node done when it is pushed instead of when it is popped.
- Forgetting the stale check, which re-expands nodes and can blow the time bound.
- Returning the sum of distances or the distance to the last node instead of the max.
- Using n instead of n + 1 for a 1-indexed array.
- Using float `inf` comparisons carelessly: `max(dist[1:])` is fine, but `dist[0]` must be excluded.
