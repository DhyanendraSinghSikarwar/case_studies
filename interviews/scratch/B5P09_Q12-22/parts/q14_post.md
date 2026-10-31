**Edge cases:**
- Smallest case: a triangle. The third edge is returned.
- Edge order matters: the same graph in a different order returns a different edge. Endpoint order inside the answer must be as given (`[1, 3]`, not `[3, 1]`).
- The extra edge may connect nodes far apart (long cycle) or neighbours (cycle of length 3).
- The cycle edge is not always the last edge of the input; extra tree edges can come after it (example 2).

**Follow-ups:**
- Directed version (a rooted tree plus one extra edge)? Harder: a node may get two parents, or a cycle appears; handle the two-parents case by trying to drop each candidate edge.
- Which edges are *on* the cycle? Remove leaves repeatedly (degree 1 peeling); what is left is the cycle.
- Return all edges that could be removed? Walk the cycle: the edges on the path between the closing edge's endpoints plus the closing edge.

**Common mistakes:**
- Returning the first removable edge in input order instead of the last. The prompt wants the last.
- Using the DFS "parent node" trick for the cycle test and still returning edges in the wrong order.
- Forgetting 1-indexing and allocating `n` instead of `n + 1` slots.
- Reversing the endpoints in the answer.
