**Pattern:** Connected components on a graph given as an adjacency matrix. A province is one component.

**Say this first (1 line):** "Count components: start a traversal from every unseen city and add one each time; or union-find and subtract one per real merge. Either way it is O(n^2) because the matrix has n^2 cells."

**Brute force:** Transitive closure with Warshall (three nested loops over n), then count cities that are the smallest member of their group. O(n^3) = 8 * 10^6 for n = 200. Fine here, and it is my checker.

**Optimal:** Two standard solutions.
- Traversal: `seen` array. For each city not seen, `count += 1` and run DFS or BFS over `row[v] == 1` neighbours. I use an explicit stack so there is no recursion-limit worry. Mark when pushing.
- Union-find: start with `count = n`. For each pair `i < j` with `is_connected[i][j] == 1`, union them; every successful merge does `count -= 1`. Only the upper triangle is needed because the matrix is symmetric.
- Invariant (traversal): each traversal visits exactly one whole component, so the number of traversal starts is the number of components.

**Complexity:**
- Both read the matrix, which alone is O(n^2). Traversal: each node dequeued once, a row scan of n cells each, so O(n^2). Union-find: n^2/2 cell checks plus at most n - 1 merges at O(alpha(n)). O(n^2) total.
- Space O(n) extra (seen or parent array), not counting the input.
- With n = 200 this is 40,000 cells; trivial.

**Dry run:** `[[1,1,0],[1,1,0],[0,0,1]]`.
- Traversal: start at 0 (count 1), see 1 connected, mark it; row 1 gives 0 (seen). Start at 2 (count 2). Answer 2.
- Union-find: count = 3. Pair (0,1) is 1, roots differ, merge, count = 2. Pairs (0,2), (1,2) are 0. Answer 2.
