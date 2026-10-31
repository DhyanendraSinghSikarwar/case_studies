import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B5P14_wavea')
from qs import QS as RAW
def render(v): return repr(v).replace('None', 'null')
def example_text(ex):
    return '; '.join(', '.join(f"{k}={render(v)}" for k, v in kw.items()) + ' -> ' + render(out) for kw, out in ex)
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S3 = sorted([(s, d, key, text, ex, a) for s, d, key, text, ex, a in RAW], key=lambda q: (-q[0], order[q[1]]))   # stable
KEYNO = {q[2]: i for i, q in enumerate(S3, 1)}
PLACE = set()
def subst(key, text):
    def f(m):
        PLACE.add((key, KEYNO[m.group(1)])); return f"Q{KEYNO[m.group(1)]}"
    return re.sub(r'Q\{Q:(\w+)\}', f, text)
QS = [(s, d, key, f"{re.sub(r' +', ' ', subst(key, text).strip())} Example: {example_text(ex)}.", a) for s, d, key, text, ex, a in S3]
N = 50
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
    assert 'seeded random cross-check' in q, key
    assert '{Q:' not in q
# within-part references 'Qn' (not preceded by 'Part N ', not a set tag 'Qn of m') must come from verified placeholders
BARE = r'(?<!Part \d )(?<!Part \d\d )\bQ(\d+)\b(?! of \d)'
for s, d, key, q, a in QS:
    for m in re.finditer(BARE, q):
        assert (key, int(m.group(1))) in PLACE, (key, m.group(0))
for key, qn in PLACE:
    assert re.search(rf'\bQ{qn}\b', next(q[3] for q in QS if q[2] == key)), (key, qn)
    assert 1 <= qn <= N
# ---- mock sets
SETS = {  # name: (theme, minutes, size)
 'A': ('Backend design round: streams, trips, scores, expiring caches and delayed jobs', 45, 5),
 'B': ('Graph round: union-find, Kruskal with pre-built edges, directed tree repair and strongly connected components', 45, 5),
 'C': ('Range-query round: positions with bisect, Fenwick order statistics, reverse pairs and a lazy segment tree', 45, 4),
 'D': ('Online-assessment mix: heaps with lazy deletion, bisect, frequency stacks and an event sweep', 45, 4)}
TAG = re.compile(r'^\[Set ([A-Z]), Q(\d+) of (\d+), (\d+) min, (\d+) pts\] ')
setq = {k: [] for k in SETS}; nset = 0
for i, (s, d, key, q, a) in enumerate(QS, 1):
    m = TAG.match(q)
    if m:
        k, qi, mm, mins, pts = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
        assert k in SETS and mm == SETS[k][2], (k, mm); setq[k].append((qi, mins, pts, i, key)); nset += 1
    else:
        assert '[Set' not in q, key
for k, (theme, tot, size) in SETS.items():
    lst = sorted(setq[k]); assert [x[0] for x in lst] == list(range(1, size + 1)), (k, lst)
    assert sum(x[2] for x in lst) == 100, (k, sum(x[2] for x in lst))
    assert sum(x[1] for x in lst) == tot, (k, sum(x[1] for x in lst))
    pts = [x[2] for x in lst]; assert pts == sorted(pts)           # points never decrease inside a set
assert nset == sum(v[2] for v in SETS.values()) == 18
nstand = N - nset
KW = {(1, 10): 'Top K frequent elements.', (1, 39): 'Counter and defaultdict idioms and traps.', (2, 3): 'Maximum average of a fixed-size window.',
      (2, 45): 'Longest subarray with max minus min at most limit.', (4, 2): 'Min stack.', (4, 22): 'Design a circular queue (ring buffer).', (4, 38): 'Max stack.',
      (5, 4): 'First and last position of an element.', (5, 11): 'Lower and upper bound semantics and the bisect module.',
      (6, 29): 'Doubly linked list operations with sentinels.', (6, 30): 'LRU cache: the linked-list idea (concept only).', (7, 30): 'BST iterator with O(h) space.',
      (8, 1): 'Python heapq basics and the max-heap trick.', (8, 4): 'Kth largest element in an array.', (8, 5): 'Merge intervals.', (8, 7): 'Meeting rooms II (minimum number of rooms).',
      (8, 17): 'Median of a data stream.', (8, 29): 'heapq with tuples and tie-breaking.', (8, 31): 'Priority queue with removal by lazy deletion.', (8, 38): 'A priority queue with changing priorities',
      (9, 3): 'Connected components of an undirected graph.', (9, 6): 'Iterative DFS on a very deep graph.', (9, 9): 'Course schedule II: produce an order.', (9, 13): 'Union-find with path compression and union by size.',
      (9, 14): 'Redundant connection (union-find).', (9, 21): 'Is the graph bipartite?', (9, 24): 'Parallel courses: minimum number of semesters.', (9, 29): 'Minimum spanning tree weight with Kruskal.',
      (9, 33): 'Alien dictionary', (9, 34): 'Cheapest flights with at most k stops.', (9, 36): 'Eulerian path and circuit: existence only.', (9, 37): 'Prim', (9, 43): 'Number of islands II (online union-find).',
      (13, 1): 'Range sum queries on an immutable array.', (13, 4): 'Range addition with a difference array.', (13, 17): 'Count inversions with merge sort.',
      (13, 40): 'Matrix region sums with point updates (basic level).', (13, 47): 'Count of range sums with merge sort.', (1, 35): 'Randomised set with O(1) operations.'}
def refs_in(t):
    return {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)', t)}
refs = set()
for s, d, key, q, a in QS: refs |= refs_in(q)
print('refs in prompts', len(refs), sorted(refs))
files = {p: open(f'Book5_DSA/Book5_DSA_Part{p:02d}.md', encoding='utf-8').read() for p in range(1, 14)}
def check_ref(p, qn):
    assert 1 <= p <= 13 and (p, qn) in KW, (p, qn)
    m = re.search(rf'^### Q{qn} \S+ \S+ (.*)$', files[p], re.M)
    assert m and m.group(1).startswith(KW[(p, qn)]), (p, qn, m and m.group(1)[:50])
for r in refs: check_ref(*r)
def set_refs(k):
    r = set(); w = set()
    for qi, mins, pts, i, key in setq[k]:
        text = QS[i - 1][3]; r |= refs_in(text)
        w |= {int(m.group(1)) for m in re.finditer(BARE, text)}
    return sorted(r), sorted(w)
rows = ''
for k, (theme, tot, size) in SETS.items():
    r, w = set_refs(k)
    rows += f"| {k} | {theme} | {size} | {tot} min | 100 | {', '.join(f'Part {p} Q{q}' for p, q in r)}{'; this part: ' + ', '.join(f'Q{x}' for x in w) if w else ''} |\n"
setlist = '; '.join(f"Set {k}: " + ', '.join(f"Q{i}" for qi, mins, pts, i, key in sorted(setq[k])) for k in SETS)
K = KEYNO
hdr = f"""# Book 5 — Part 14: Extra II (Design Problems, Advanced Graphs, Segment and Fenwick Trees, Mixed Mock Sets)

**Topic:** Python DSA for product-company interviews, the 'Extra II' part and the LAST part of Book 5: design problems with exact API and tie rules (LRU cache with OrderedDict and with a hand-built doubly linked list, LFU cache in O(1), rate limiters (fixed window, sliding window log, token bucket) and the logger and hit counter, all with an injected clock; iterator design (nested list, peeking, zigzag), time-based key-value store with bisect, snapshot array, news feed with heaps, the all-O(1) data structure), advanced graphs (strongly connected components with Kosaraju and with Tarjan, bridges and articulation points, Hierholzer's Eulerian path for the itinerary problem, lexicographically smallest topological order, parallel courses with durations, shortest path with a coupon, maximum bipartite matching), segment trees and Fenwick (BIT) trees (point update and range query, range minimum, lazy propagation for range add and range sum, sparse table, coordinate compression, inversions and smaller-after-self with a BIT, a 2D BIT), and four timed company-style mock sets that integrate Parts 1 to 14.

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Split:** {nstand} standalone questions and {nset} mock-set questions ({'; '.join(f'Set {k} has {v[2]}' for k, v in SETS.items())}). The set questions are real problems of their own (not repeats of the standalone ones) and are listed by star rating like every other question, so a set is scattered through the file; to run a set as a mock, collect its tag. Where the sets sit in this file: {setlist}.

How the sets work: there are 4 sets (A and B with 5 questions, C and D with 4), each 45 minutes and 100 points. Each set question is tagged `[Set A, Q1 of 5, 5 min, 10 pts]`. Inside a set the questions run from warm-up to hardest and the points never decrease: sets of 5 use 10, 15, 20, 25 and 30 points, sets of 4 use 15, 25, 30 and 30 points; the minutes add up to 45. Suggested scoring per question: 30 percent for stating the rules, tie-breaks and boundaries out loud before coding (inclusive or exclusive windows, tie rules, what an empty input returns), 30 percent for a correct solution that passes the example and a random operation-sequence or brute-force check, 20 percent for the stated complexity and the reason it holds, 10 percent for the edge cases the prompt seeds, 10 percent for a crisp spoken summary in under 60 seconds. Bands per set: 85 to 100 strong, 70 to 84 solid with gaps, 50 to 69 review the linked parts, below 50 redo the linked earlier parts first. Time budgets and bands are practice targets set by this book, not any company's published rules.

| Set | What it covers | Questions | Time | Points | Earlier questions it builds on |
|---|---|---|---|---|---|
{rows}
Scope note: this part owns design problems with an API, advanced graph algorithms, segment and Fenwick trees and the mixed mock sets. It does not repeat: the min stack ('Part 4 Q2') and max stack ('Part 4 Q38'), the randomised set ('Part 1 Q35'), the BST iterator ('Part 7 Q30'), the linked-list pieces of an LRU cache ('Part 6 Q29' and 'Part 6 Q30'; Q{K['lru_dll']} here builds the full class), minimum spanning trees ('Part 9 Q29' Kruskal and 'Part 9 Q37' Prim; Set B reuses Kruskal with pre-built edges), basic bipartite colouring ('Part 9 Q21'; Q{K['bipartite_matching']} is the matching variant), the Eulerian existence test ('Part 9 Q36'; Q{K['itinerary']} constructs the trail), unit-time parallel courses ('Part 9 Q24'; Q{K['parallel_time']} adds durations), cheapest flights with at most k stops ('Part 9 Q34'; Q{K['sp_coupon']} is a different constraint), the merge-sort inversion count and range-sum counting ('Part 13 Q17' and 'Part 13 Q47'; Q{K['inversions_bit']}, Q{K['count_smaller']} and Q{K['reverse_pairs']} use a Fenwick tree) and the row-prefix 2D point-update version ('Part 13 Q40'; Q{K['bit_2d']} is the Fenwick answer it promises). Every 'Part N Qn' reference in this file was checked by script against the headings of Book5_DSA_Part01 to Part13.

API-shaped questions: every design prompt names the class, the methods and their signatures and states the exact call format used in its examples: the checker builds the object with `init` (the constructor arguments) and runs `ops`, a list of [method, [args]] calls, collecting one return value per call (None when a method returns nothing); an example is written `init=..., ops=... -> list of return values`. Time-dependent designs (Q{K['sliding_log']}, Q{K['token_bucket']}, Q{K['fixed_window']}, Q{K['hit_counter']}, Q{K['logger']} and the set questions with a clock) take an INJECTED clock: the first constructor argument is a zero-argument callable returning integer seconds, the checker sets it before each call, ops are [time, method, [args]] with non-decreasing times, and every prompt states the window boundary exactly (half-open windows, expiry at the exact second, the second a message may print again). Tie and eviction rules are explicit (LRU and LFU eviction, the all-O(1) tie rule, the Twitter feed recency rule, the frequency-stack tie rule, the voting tie rule). Thread safety appears only as a stated concept (what a lock would have to cover), never as code. Every design answer must include an operation-sequence oracle: random operation sequences replayed against a simple reference implementation, with the two outputs compared.

Recursion and size notes: every graph question that walks deep paths (Q{K['scc_kosaraju']}, Q{K['bridges']}, Q{K['scc_tarjan']}, Q{K['articulation']}, Q{K['min_sources']} as the SCC step) requires an iterative implementation because a path of 10^5 nodes exceeds CPython's default recursion limit of 1000; the checker confirmed that a recursive flatten or DFS fails at depth 1500 and that the iterative references handle 10^5 nodes. Segment-tree recursion depth is about log2(n) (under 20) and the matching recursion depth is at most L <= 300, so recursion is fine there; the prompts say so. Examples in every prompt are rendered from the same data the checker runs.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for en.wikipedia.org), so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part14_sources.md). Searches returned design-problem lists (a LeetCode Discuss post, talentd.in, walkccc, designgurus), rate-limiter and LRU guides (techinterview.org, InterviewBit, a Redis rate-limiter post), segment-tree, Fenwick and sparse-table guides (techinterview.org, mintlify, cp-algorithms, designgurus) and advanced-graph guides (techinterview.org, algocademy, Naukri Code360). The searches did not cover the zigzag iterator, the skyline problem or a worked LFU solution, so those come from editor knowledge of standard lists. Nothing was found tying any single item to a named company, so 'Asked at' lines name source types only; the mock sets are editor designs in the style of timed rounds. No salary figures appear anywhere in this part.

---
"""
for m in refs_in(hdr): check_ref(*m)
for m in re.finditer(r"Q\{K\['(\w+)'\]\}", hdr): raise SystemExit('unrendered')
out = [hdr]
for i, (s, d, key, q, a) in enumerate(QS, 1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt = ''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->') == N and txt.count('**Asked at:**') == N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt and "**Target:** 50" in txt
assert txt.count('\n### Q') == N
assert not re.search(r'(?i)\blpa\b|salary|\brs \d', txt.split('Evidence limits')[0])
assert '\n' not in ''.join(q for _, _, _, q, _ in QS)
for m in re.finditer(BARE, hdr):
    assert 1 <= int(m.group(1)) <= N
for k in SETS: assert f"| {k} |" in hdr
open('Book5_DSA/Book5_DSA_Part14.md', 'w', encoding='utf-8', newline='\n').write(txt)
rows_i = ''.join(f"| B5P14-Q{i} | 14 | {q.strip()} |\n" for i, (s, d, key, q, a) in enumerate(QS, 1))
open('scratch/B5P14_wavea/index_rows.txt', 'w', encoding='utf-8', newline='\n').write(rows_i)
idx = open('question_index.md', encoding='utf-8').read()
idx = ''.join(l for l in idx.splitlines(True) if not l.startswith('| B5P14-Q'))
if not idx.endswith('\n'): idx += '\n'
open('question_index.md', 'w', encoding='utf-8', newline='\n').write(idx + rows_i)
print('built', n, c, 'standalone', nstand, 'set', nset)
for i, (s, d, key, q, a) in enumerate(QS, 1): print(i, s, d, key)
