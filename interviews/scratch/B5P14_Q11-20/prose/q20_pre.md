**Pattern:** Strongly connected components with Kosaraju: two DFS passes, both written with an explicit stack because recursion would break on a 10^5-node path (Part 9 Q6 shows the explicit-stack DFS).

**Say this first (1 line):** "Pass 1: DFS on the graph recording finish order. Pass 2: DFS on the reversed graph in decreasing finish order; each tree of pass 2 is one component."

**Brute force:**
- Compute reachability from every node (Floyd-Warshall or a BFS per node), then group u and v when each reaches the other. O(n^3) or O(n (n + m)); far too slow at 10^5 nodes. It is the oracle in the code.

**Optimal:**
- Build `g` and the reversed graph `rg`.
- Pass 1: for each unvisited start, run an iterative DFS with a stack of `(node, next neighbour index)`. When a node has no neighbours left, append it to `order` (it finishes).
- Pass 2: go through `order` backwards. For each node not yet assigned, run a DFS (a plain stack is fine, only reachability matters) over `rg` through unassigned nodes. Everything reached forms one component.
- Finally sort each component, then sort components by their smallest member.
- Why it works: take the component whose node finished LAST in pass 1. It is a source of the condensation, so nothing outside reaches it; in the reversed graph it has no way out to other components. So the reversed DFS from that node collects exactly this component. Remove it, and the next-latest remaining finisher is a source of what is left, and so on.
- The condensation is the graph obtained by shrinking every SCC to one node. It is always a DAG (a cycle between components would merge them), which is what makes the finish-order argument work.
- Self loops and repeated edges change nothing: a self loop leaves a node in its own component; duplicates are ignored by the visited marks.

**Complexity:**
- Time O(n + m): each node and edge is processed a constant number of times in each pass, plus the final sort O(n log n).
- Space O(n + m) for the two adjacency lists, the stacks and the order.
- The stack lives in a Python list on the heap, so depth is not limited by the recursion limit (1000 by default).

**Dry run:** `n = 5`, edges 0->1, 1->2, 2->0, 1->3, 3->4.
- Pass 1 from 0: go to 1, go to 2; 2's only neighbour 0 is seen, so 2 finishes. Back at 1: next neighbour 3, then 4; 4 finishes, 3 finishes, 1 finishes, 0 finishes. `order = [2, 4, 3, 1, 0]`.
- Reversed edges: 1->0, 2->1, 0->2, 3->1, 4->3.
- Pass 2 in reverse order: start 0. `rg[0] = [2]`, `rg[2] = [1]`, `rg[1] = [0]` (seen). Component {0, 2, 1}. Next unassigned in order: 3. `rg[3] = [1]` is assigned, so {3}. Then 4: `rg[4] = [3]` assigned, so {4}.
- Sorted result `[[0, 1, 2], [3], [4]]`.
