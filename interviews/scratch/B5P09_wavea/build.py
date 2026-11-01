import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B5P09_wavea')
from qs import QS as RAW
def render(v): return repr(v).replace('None', 'null')
def example_text(ex):
    return '; '.join(', '.join(f"{k}={render(v)}" for k, v in kw.items()) + ' -> ' + render(out) for kw, out in ex)
order = {'🟢': 0, '🟡': 1, '🔴': 2}
QS = sorted([(s, d, key, f"{text.strip()} Example: {example_text(ex)}.", a) for s, d, key, text, ex, a in RAW], key=lambda q: (-q[0], order[q[1]]))   # stable
N = 45
n = len(QS)
c = [sum(1 for q in QS if q[0] == s) for s in (3, 2, 1)]
print(n, c)
assert n == N, n
assert [q[0] for q in QS] == sorted([q[0] for q in QS], reverse=True)
assert sum(c) == N and all(q[1] in order for q in QS)
assert len({q[3] for q in QS}) == N and len({q[2] for q in QS}) == N
assert len({q[3].split('.')[0] for q in QS}) == N   # unique titles
for s in (3, 2, 1):
    d = [order[q[1]] for q in QS if q[0] == s]
    assert d == sorted(d), (s, d)
for s, d, key, q, a in QS:
    assert 'Example' in q and '->' in q, q[:40]
    assert 'Asked' not in q and a.strip()
KW = {(4, 4): 'Python list versus collections.deque as a stack and a queue.', (4, 30): 'The BFS level-order queue idiom, at concept level.',
      (7, 9): 'Level-order traversal.', (7, 35): 'Deep skewed trees and the recursion limit.',
      (8, 29): 'heapq with tuples and tie-breaking.', (8, 31): 'Priority queue with removal by lazy deletion.',
      (8, 38): 'A priority queue with changing priorities and no decrease-key.'}
def refs_in(t):
    return {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)', t)}
refs = set()
for s, d, key, q, a in QS: refs |= refs_in(q)
print('refs', sorted(refs))
files = {p: open(f'Book5_DSA/Book5_DSA_Part0{p}.md', encoding='utf-8').read() for p in (1, 2, 3, 4, 5, 6, 7, 8)}
def check_ref(p, qn):
    assert p in files and (p, qn) in KW, (p, qn)
    m = re.search(rf'^### Q{qn} \S+ \S+ (.*)$', files[p], re.M)
    assert m and m.group(1).startswith(KW[(p, qn)]), (p, qn, m and m.group(1)[:50])
for r in refs: check_ref(*r)
hdr = f"""# Book 5 — Part 9: Graphs (BFS/DFS, Topological Sort, Dijkstra, Union-Find)

**Topic:** Python DSA for product-company interviews: graph representations (adjacency list, adjacency matrix, edge list; directed, undirected and weighted; building them from an edge list and the cost of each), BFS and DFS written iteratively (and why recursive DFS is limited by CPython's recursion limit of 1000), connected components, number of islands and grids as implicit graphs, flood fill, clone graph, shortest paths in unweighted graphs (BFS, grid variants, 8-directional moves), multi-source BFS (rotting oranges, walls and gates, shortest bridge), word ladder, state-space BFS on implicit graphs (open the lock, sliding puzzle), course schedule with Kahn's algorithm and DFS three-colour topological sort, parallel courses, eventual safe nodes, alien dictionary (topological order from constraints), cycle detection in directed and undirected graphs, bipartite check, Dijkstra with heapq and lazy deletion (no decrease-key; counting pushes and stale pops; why a negative edge breaks it), minimum-effort paths, 0-1 BFS, Bellman-Ford with negative cycles, cheapest flights within k stops, Floyd-Warshall, shortest paths in a DAG, union-find (path compression, union by size, redundant connection, accounts merge, number of provinces, stones removed, number of islands II), minimum spanning tree at basic level (Kruskal and a dense Prim), minimum height trees by leaf peeling, Eulerian path and circuit as a concept (existence test only), and graph complexity (O(V + E) with lists, O(V^2) with a matrix, O((V + E) log V) for Dijkstra with a binary heap)

**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns the graph algorithms listed above. Part 4 owns stacks and queues (the BFS queue idioms are cross-referenced as 'Part 4 Q4', the deque-versus-list cost, and 'Part 4 Q30', the level-order queue idiom), Part 7 owns trees (tree level-order and DFS are reused by reference as 'Part 7 Q9' and the deep-skewed-tree recursion limit as 'Part 7 Q35'; trees here appear only as a special graph in minimum height trees), Part 8 owns heaps (heapq lazy deletion, tie-breaking and priority updates without decrease-key are cross-referenced as 'Part 8 Q31', 'Part 8 Q29' and 'Part 8 Q38'; this part uses heapq only inside Dijkstra and Prim), Parts 10 and 11 own dynamic programming (shortest-path-style DP variants are handed off by part number only; Bellman-Ford and Floyd-Warshall here are the graph algorithms), and Part 14 owns advanced graphs and design problems (strongly connected components, bridges and articulation points, deeper minimum spanning tree theory such as the cut property, Boruvka and second-best trees, bipartite matching and flow, and design problems; this part gives only the basic colouring check, Kruskal and a dense Prim, and mentions them at concept level); each Part N Qn reference was checked against its heading by build.py. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: nodes are numbered 0..n-1 unless a prompt says 1..n; a graph is given as an edge list (`n` plus a list of [u, v] or [u, v, w]), an adjacency list (`graph[u]` lists neighbours) or an adjacency matrix, and each prompt states which, whether it is directed, whether repeated edges and self loops can occur, and whether weights can be negative; grids are lists of lists or lists of strings with 4-directional moves unless a prompt says 8-directional. Recursion: every prompt whose natural solution is a DFS and whose size reaches the thousands (up to 10^5 nodes or a 300 x 300 grid) says an iterative solution is required, because a recursive DFS exceeds CPython's default limit of 1000 (the claim is demonstrated: a recursive DFS on a 5000-node path raises RecursionError, while the iterative versions finish 2*10^5-node paths, a 300 x 300 all-land grid and 10^5-node random graphs); no prompt relies on raising the limit, and no claim is made about the C stack. Questions whose output is not unique say what the checker accepts: course schedule II (any order that respects every prerequisite; [] exactly when a cycle exists) and alien dictionary (any string that lists every letter once and under which the words are sorted; '' exactly when no ordering of the letters works) are validated by property and the examples show one accepted answer; topological order by DFS, the BFS and DFS visiting orders, the Dijkstra push counts and the iterative DFS variants are defined step by step so their outputs are unique; minimum spanning tree questions accept only the total weight (the trees may differ, the weight does not); redundant connection asks for the last cycle edge in input order; minimum height trees returns every optimal root; the Floyd-Warshall city question fixes the tie rule (largest index). Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P09_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force or validator on 400 seeded random small inputs per question (18000 in all), for example edge-list-to-matrix reconstruction, label propagation for components and islands, a recursive DFS and level-by-level BFS for the traversal orders, transitive closure for cycle detection, course feasibility and safe nodes, Bellman-Ford and Floyd-Warshall for Dijkstra, DAG shortest paths and network delay, a binary search on a threshold for minimum effort, removal of each edge in turn for redundant connection and undirected cycles, all subsets of n - 1 edges for Kruskal, Kruskal against Prim for the point MST, all removal orders for stones, all edge sequences for Eulerian trails, all permutations of the alphabet for the alien dictionary, all two-island pairs for the shortest bridge (minimum Manhattan distance minus one), a per-room BFS for walls and gates, all two-colourings for bipartite checks, and a full-grid flood fill after every addition for islands II. Claims tested by running code: for every one of the 720 sliding-puzzle boards the BFS agrees with a table built backwards from the goal, exactly 360 boards are solvable and the hardest needs 21 moves; the finalise-on-first-pop Dijkstra is wrong on 2897 of the three-node graphs with weights in -3..3 (without a negative cycle) and is never wrong when all weights are non-negative, while the stale-check variant matches Bellman-Ford on 1500 random negative-edge graphs; in lazy-deletion Dijkstra pushes never exceed E + 1 and stale pops always equal pushes minus reached nodes (1500 random graphs); minimum height trees have one or two roots for all 18248 labelled trees with 2 to 7 nodes; in the cheapest-flights question an in-place update and a Dijkstra with a visited set are each wrong on some random inputs (seeded counts 22 and 35 of 3000); an ordinary BFS with marking on first enqueue is wrong on the 0-1 grid problem (803 of 2000 seeded grids); the mark-on-push iterative DFS order differs from the recursive preorder on 367 of 800 random graphs while visiting the same nodes; mark-on-dequeue BFS on the binary matrix gives the same answers; a naive link of union(i, i + 1) without union by size builds a 10^5-deep parent chain, which is why `find` must be iterative; BFS entries examined are at most E (directed) or 2E (undirected) and matrix cells are n times the reached nodes. Both branches of every boolean or sentinel answer occurred in the random tests. All solutions run at the stated sizes (10^5-node graphs, a 300 x 300 grid, 5000 words for word ladder, 1000 points for Prim) in a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part09_sources.md). Searches returned graph pattern guides (techinterview.org, DesignGurus, Techie Delight), candidate-reported Flipkart rounds that mention number of islands and word ladder (Naukri Code360 and GeeksforGeeks, self-reported), and Dijkstra lazy-deletion write-ups (PracHub, Codeforces tutorials, a python-dev thread); nothing was found tying course schedule, Dijkstra, union-find or the other items to a named company, so 'Asked at' tags name source types, not verified company reports. Items such as accounts merge, alien dictionary, parallel courses, shortest bridge, minimum height trees, stones removed and sliding puzzle come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
for m in refs_in(hdr): check_ref(*m)
out = [hdr]
for i, (s, d, key, q, a) in enumerate(QS, 1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt = ''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->') == N and txt.count('**Asked at:**') == N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt and "**Target:** 45" in txt
assert txt.count('\n### Q') == N
assert not re.search(r'(?i)\blpa\b|salary|\brs \d', txt.split('Evidence limits')[0])
assert '\n' not in ''.join(q for _, _, _, q, _ in QS)
open('Book5_DSA/Book5_DSA_Part09.md', 'w', encoding='utf-8', newline='\n').write(txt)
rows_i = ''.join(f"| B5P09-Q{i} | 9 | {q.strip()} |\n" for i, (s, d, key, q, a) in enumerate(QS, 1))
open('scratch/B5P09_wavea/index_rows.txt', 'w', encoding='utf-8', newline='\n').write(rows_i)
idx = open('question_index.md', encoding='utf-8').read()
if 'B5P09-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8', newline='\n').write(idx + rows_i)
print('built', n, c)
for i, (s, d, key, q, a) in enumerate(QS, 1): print(i, s, d, key)
