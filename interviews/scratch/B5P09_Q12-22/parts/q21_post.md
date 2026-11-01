**Edge cases:**
- Disconnected graph: the outer loop must restart. One odd cycle in a later component makes the answer False even when the first component is fine.
- Isolated nodes (empty lists): True.
- Single node: True.
- Even cycle: True; odd cycle of length 99,999: False (checked at full size in the run).
- No self loops by the prompt (a self loop would make it False immediately).

**Follow-ups:**
- Return the two sets? Collect nodes by colour.
- Possible bipartition (dislike pairs)? The same problem with edges as "dislikes".
- Find the odd cycle itself? Store parents; on a conflict walk both nodes up to their common ancestor.
- Matching and flow on bipartite graphs are in Part 14.

**Common mistakes:**
- Colouring only from node 0 (misses other components).
- Comparing with the parent only; any visited neighbour with the same colour is a conflict, not just the parent.
- Marking colour on dequeue instead of enqueue, which lets a node be given two colours.
- Recursive DFS on a 10^5 path: RecursionError.
