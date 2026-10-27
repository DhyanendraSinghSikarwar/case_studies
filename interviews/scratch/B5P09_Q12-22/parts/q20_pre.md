**Pattern:** Multi-source BFS. Put every source in the queue at distance 0 and run one BFS; each cell gets the distance to its nearest source.

**Say this first (1 line):** "Reverse the question: instead of searching from each room for a gate, start from all gates together; the first time BFS reaches a room is its nearest-gate distance."

**Brute force:** For every empty room run its own BFS until it hits a gate. One BFS is O(mn), there are up to mn rooms, so O((mn)^2) = 10^8 for 100 x 100. On a 30 x 30 grid with one gate in the corner the run below counts 596,584 queue pops against 900 for the right method.

**Optimal:**
- Copy the grid (the prompt wants a new grid). Queue = all cells equal to 0.
- Pop `(x, y)`. For each of 4 neighbours in bounds that still holds 2147483647: set it to `g[x][y] + 1` and enqueue.
- The sentinel value does two jobs: "unvisited" and "still unreachable". Walls (-1) and gates (0) are never overwritten.
- Why it works: this is the same as adding a virtual super-source joined to every gate by a zero-cost edge. BFS pops cells in order of distance from that super-source, so the first writer of a cell is its nearest gate.
- Rooms never reached keep 2147483647, exactly the required output.

**Complexity:**
- Multi-source BFS: each cell enqueued at most once, 4 neighbour checks each, so O(mn) time and O(mn) space (queue plus copied grid).
- One BFS per room: O(mn) rooms times O(mn) each, O((mn)^2) time.

**Dry run:** the 1 x 3 grid `[0, -1, INF]`.
- Queue [(0,0)]. Pop it: neighbour (0,1) is a wall (-1, not INF), skip. Queue empty.
- (0,2) was never written, stays INF. Result `[0, -1, INF]`, as expected.
- On the 4 x 4 example the gates at (0,2) and (3,0) both start in the queue; the cell (1,2) is reached from (0,2) at distance 1 and keeps that value even though (3,0) would give a longer one.
