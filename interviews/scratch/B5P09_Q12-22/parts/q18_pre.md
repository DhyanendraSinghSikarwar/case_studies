**Pattern:** BFS on a grid as an implicit graph. Every move costs 1, so BFS order is shortest-path order. The only change from the 4-direction version is 8 neighbour offsets.

**Say this first (1 line):** "BFS from the top-left with 8 directions, mark a cell when I enqueue it, and the depth of the bottom-right cell is the answer, counted in cells."

**Brute force:** Distance relaxation: set `dist[start] = 1`, then keep sweeping every open cell and its 8 neighbours until nothing improves. Each sweep is O(n^2), and up to O(n^2) sweeps, so O(n^4) = 10^8 for n = 100. It is my checker, not the solution.

**Optimal:**
- If either endpoint is 1, return -1 at once.
- Queue of `(row, col, length)`, start `(0, 0, 1)` (cells counted, so the start is 1).
- Pop a cell, if it is the target return its length. Otherwise for each of 8 offsets in bounds, open, and not seen: mark seen, push with length + 1.
- Why BFS is right: all edges have the same cost, so cells leave the queue in non-decreasing length. The first time the target is dequeued is its shortest length.
- Why mark on enqueue: a cell is reached first by the shortest route, so later routes to it are useless. If you mark on dequeue, the same cell can sit in the queue several times (up to once per neighbour, so up to 8). The answer stays correct, but the queue is bigger and you do repeated work. The run shows peak queue 199 against 788 on an open 100 x 100 grid.

**Complexity:** O(n^2) time (each cell enqueued once, 8 neighbour checks each), O(n^2) space for the seen array and the queue (the queue holds at most one frontier, which is O(n) in practice).

**Dry run:** `[[0,0,0],[1,1,0],[1,1,0]]`.
- Start (0,0) length 1. Neighbours open: (0,1) length 2. (1,0), (1,1) are blocked.
- Pop (0,1): neighbours (0,2) open, length 3. (1,2) is diagonal-adjacent too: open, length 3.
- Pop (0,2) length 3: its neighbours (1,2) already seen. Pop (1,2) length 3: neighbour (2,2) open, length 4.
- Pop (2,2): target, return 4.
