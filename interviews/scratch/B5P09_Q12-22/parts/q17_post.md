**Edge cases:**
- n = 1: one province.
- Identity matrix: n provinces. All ones: 1 province.
- The diagonal is always 1; do not treat `m[i][i]` as a union (it would be a no-op anyway).
- Indirect connection: 0-1 and 1-2 joined, 0-2 not directly: still one province (the chain case).

**Follow-ups:**
- Input as an edge list instead? Union-find or list-based BFS in O(V + E); no need to ever build a matrix.
- Return the sizes of the provinces? Keep a counter per traversal, or use union by size.
- Cities added over time? Union-find answers it online (see Number of Islands II in this part).

**Common mistakes:**
- Treating the matrix like an edge list and running O(n^3).
- Recursive DFS with n = 200 is fine, but the habit fails at 10^5; write the stack version.
- Counting the number of 1s or the number of rows with a 1.
- Forgetting `seen` marking on the neighbour loop and revisiting nodes.
