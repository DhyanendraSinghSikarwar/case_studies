**Edge cases:**
- No gates: nothing is queued, the grid comes back unchanged.
- 1 x 1 grid: return as is.
- Rooms walled off from every gate stay at 2147483647 (not -1).
- Gate next to gate: both stay 0, no overwrite.
- Do not overwrite walls or gates; the check `== INF` takes care of it.

**Follow-ups:**
- Rotting oranges is the same pattern with levels counted per minute (a sibling question in this part).
- Different step costs per cell? Then it is Dijkstra from all sources (push all sources with distance 0).
- Return which gate is nearest? Store the gate id along with the distance in the queue.

**Common mistakes:**
- BFS from every room (times out).
- Starting from one gate at a time and keeping the minimum (that is also O(gates * mn)).
- Using `0` as the unvisited marker, so gates look unvisited.
- Mutating the input when a new grid is required.
- Checking `g[a][b] != -1` only, which lets BFS overwrite already-set smaller distances.
