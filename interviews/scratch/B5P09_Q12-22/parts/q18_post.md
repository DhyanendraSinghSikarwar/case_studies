**Edge cases:**
- 1 x 1 grid with 0: answer 1 (the start is the target). With 1: -1.
- Start or end blocked: -1, check before the loop.
- Target reachable only diagonally between two blocked cells (corner moves): allowed here, since cells share a corner.
- Fully blocked middle: BFS empties the queue, return -1.

**Follow-ups:**
- 4 directions only? Same code with 4 offsets.
- Return the path itself? Keep a parent array and walk it back from the target.
- Several blockers you may remove (k obstacles)? BFS over (cell, removals used), state space n^2 * k.

**Common mistakes:**
- Counting steps instead of cells (the answer counts both ends, so start at 1).
- Marking on dequeue, which inflates the queue and, with a plain set of dequeued cells, adds duplicates.
- Forgetting the blocked-start check, then returning 1 for a 1 x 1 blocked grid.
- Using `list.pop(0)` instead of `deque.popleft()` (O(n) per pop; see Part 4 Q4).
- Only 4 offsets, missing diagonal moves.
