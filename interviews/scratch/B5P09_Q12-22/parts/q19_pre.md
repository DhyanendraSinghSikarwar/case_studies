**Pattern:** Graph traversal (BFS or DFS) with a hash map from original node to its copy. The map is both the "visited" set and the way to wire copied neighbours.

**Say this first (1 line):** "Traverse the graph once; keep a dict original -> clone; create a clone the first time I see a node, and always append the clone of each neighbour."

**Brute force:** `copy.deepcopy(node)`. It handles cycles by its own memo dict, so it is correct, but it is a library call that hides the idea, and its recursion depth equals the longest DFS path. I use it only to know the expected shape. Copying recursively with no memo is the broken idea: any cycle (even two nodes pointing at each other) recurses forever (the run shows the RecursionError).

**Optimal:**
- `None` in, `None` out.
- `copy_of = {node: Node(node.val)}`, queue (BFS) or stack (DFS) holding original nodes.
- For each popped node `u` and each neighbour `v`: if `v` has no clone yet, create it and queue `v`. Then `copy_of[u].neighbors.append(copy_of[v])`.
- Why the dict is needed: the graph has cycles and each undirected edge appears from both ends. Without a map you cannot tell "already copied" from "new", and a node would be copied once per path, or forever.
- Neighbour order is preserved because each node's neighbours are appended in the original order.
- BFS vs DFS: both are O(V + E). BFS uses a queue and no recursion. DFS recursion depth can be V; here V <= 100 so it is safe, but for 10^5 nodes use an explicit stack. For this question the choice is style.

**Complexity:** O(V + E) time (each node cloned once, each adjacency entry visited once), O(V) extra space for the map and queue, plus the O(V + E) output.

**Dry run:** `adj=[[2],[1,3],[2]]` (a path 1-2-3).
- copy_of = {1: 1'}; queue [1]. Pop 1: neighbour 2 is new, create 2', queue it; 1'.neighbors = [2'].
- Pop 2: neighbour 1 is in the map, 2'.neighbors = [1']; neighbour 3 is new, create 3'; 2'.neighbors = [1', 3'].
- Pop 3: neighbour 2 in the map, 3'.neighbors = [2']. Return 1'. The copy has the same adjacency, all new objects.
