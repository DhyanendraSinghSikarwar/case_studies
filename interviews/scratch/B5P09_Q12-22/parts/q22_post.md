**Edge cases:**
- Self loop `[u, u]`: True (found at the first look at `u`'s list).
- Two copies of `[u, v]` (either order, `[1, 0]` is the same pair as `[0, 1]`): True.
- Disconnected graph: the outer loop restarts from every unseen node; a cycle in a later component counts.
- No edges, single node: False.
- A path of 200,000 nodes: False; plus an extra edge anywhere: True (checked above).

**Follow-ups:**
- Directed graph? Different problem: you need three states (unseen, on the stack, done), or Kahn's algorithm (see Part 9 cycle-in-directed-graph question).
- Which edge closes the cycle? Union-find returns it directly (see the redundant connection question in this part).
- Count the independent cycles? E - V + C (edges, nodes, components), the cyclomatic number.

**Common mistakes:**
- Skipping the parent node instead of the arrival edge, then storing neighbours in a set or dict.
- Recursion on large inputs.
- Treating a self loop as harmless.
- Running only from node 0.
- Using the "directed" three-colour logic on an undirected graph, which reports the tree edge back to the parent as a cycle.
