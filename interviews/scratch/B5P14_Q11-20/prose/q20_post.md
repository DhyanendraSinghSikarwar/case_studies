**Edge cases:**
- No edges: every node is its own component.
- Single node; a self loop only (`[[0, 0]]`).
- Repeated edges (tested).
- A DAG: n components (tested).
- One big cycle with unsorted labels (tested); the output is sorted inside and across components.
- Path of 10^5 nodes and the same path closed into a cycle (tested, the explicit stack never hits the recursion limit).
- Disconnected graph: both loops start from every unvisited node.

**Follow-ups:**
- *Why reversed graph?* In the reversed graph the component of the last finisher cannot leak into other components, so one DFS stays inside it. A forward DFS from it would escape into everything it can reach.
- *Tarjan's version (Q41):* one DFS with `low` values and a component stack; same O(n + m), no reversed graph.
- *Use of SCCs:* condense to a DAG and run topological DP (2-SAT, minimum number of nodes to reach everything is the number of source components).

**Common mistakes:**
- Using recursion and crashing on a deep path (CPython's limit is 1000).
- Running pass 2 on the original graph instead of the reversed graph.
- Processing pass 2 in finish order instead of decreasing finish order.
- Appending to `order` at discovery instead of at finish.
- Forgetting to sort members and components for the required output.
