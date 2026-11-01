**Edge cases:**
- Empty graph: input `None`, return `None` (the checker passes `None` when `adj == []`).
- Single node with no neighbours.
- A node adjacent to a node that points back (every edge, since the graph is undirected): handled by the map.
- Neighbour order must be kept (the checker compares lists exactly).
- The copy must not contain any original object; appending `v` instead of `copy_of[v]` is the classic leak.

**Follow-ups:**
- Directed graph, or graph not connected from the given node? Same code copies only what is reachable; for a whole graph, loop over all nodes.
- Deep graph (10^5 nodes)? The iterative BFS version already works; a recursive DFS needs an explicit stack.
- Cloning a linked list with random pointers? Same idea: map old -> new, then wire.

**Common mistakes:**
- No dict, or checking "visited" by `val` on the original but then creating a second clone anyway.
- Appending the original neighbour into the copy's list.
- Creating the clone only when a node is popped, so a neighbour's clone does not exist yet when you want to append it.
- Forgetting the `None` case.
