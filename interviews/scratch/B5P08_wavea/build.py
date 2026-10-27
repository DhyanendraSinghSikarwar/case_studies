import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B5P08_wavea')
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
KW = {(1, 10): 'Top K frequent elements.', (2, 16): 'Sliding window maximum.', (2, 37): 'Boats to save people.', (4, 38): 'Max stack.',
      (5, 8): 'Capacity to ship packages within D days.', (5, 26): 'Kth smallest element in a sorted matrix.', (5, 33): 'Designing and proving a monotone predicate.',
      (6, 12): 'Merge k sorted linked lists.'}
def refs_in(t):
    return {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)', t)}
refs = set()
for s, d, key, q, a in QS: refs |= refs_in(q)
print('refs', sorted(refs))
files = {p: open(f'Book5_DSA/Book5_DSA_Part0{p}.md', encoding='utf-8').read() for p in (1, 2, 3, 4, 5, 6, 7)}
def check_ref(p, qn):
    assert p in files and (p, qn) in KW, (p, qn)
    m = re.search(rf'^### Q{qn} \S+ \S+ (.*)$', files[p], re.M)
    assert m and m.group(1).startswith(KW[(p, qn)]), (p, qn, m and m.group(1)[:50])
for p, qn in refs: check_ref(p, qn)
assert refs == set(KW), set(KW) ^ refs   # every checked reference is actually used
hdr = f"""# Book 5 — Part 8: Heaps, Intervals and Greedy

**Topic:** Python DSA for product-company interviews: heapq as a binary min-heap on a list and the max-heap negation trick, heap internals (parent and child indices, sift up and sift down, the O(n) build-heap argument), kth largest and smallest (sort versus a size-k heap versus quickselect), kth largest in a stream, top-k frequent words with tie-breaking, k closest points, merging k sorted arrays with a heap, task scheduler, reorganize string and its k-distance variant, last stone weight, minimum cost to connect sticks, median of a data stream (two heaps) and sliding-window median with lazy deletion, meeting rooms I, II and III, merge and insert intervals, non-overlapping intervals, minimum arrows to burst balloons, employee free time, interval list intersections, maximum events attended, smallest range covering k lists, furthest building and IPO as heap-greedy problems, k pairs with smallest sums, the greedy classics (jump game I and II, gas station, assign cookies, partition labels, candy, queue reconstruction by height, activity selection), exchange-argument proofs and the counter-examples for wrong greedy rules, when greedy fails (the coin counter-example and the hand-off to dynamic programming), the greedy feasibility check inside a binary search on the answer, Huffman coding at concept level, heapq with tuples and tie-breaking (entry counters, FIFO among equals), custom orderings and wrapper classes (a string cannot be negated), lazy deletion, and priority updates without decrease-key

**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns heaps, interval problems and greedy algorithms. Part 1 owns hashing and the counting-based top-k (cross-referenced as 'Part 1 Q10'), Part 2 owns sliding windows and two pointers (the sliding-window maximum and the boats two-pointer greedy are cross-referenced as 'Part 2 Q16' and 'Part 2 Q37'; boats is not repeated here), Part 4 owns stacks, queues and monotonic structures (the max stack, which uses the same lazy-deletion idea, as 'Part 4 Q38'), Part 5 owns binary search (the binary-search-on-answer wrapper and the monotone-predicate discussion are cross-referenced as 'Part 5 Q8' and 'Part 5 Q33', and the sorted-matrix kth smallest as 'Part 5 Q26'; this part writes only the greedy check inside them), Part 6 owns linked lists ('Part 6 Q12' merges k linked lists and uses the heap only as a merge tool, while here the heap is the subject and the data are arrays); each of these references was checked against its heading by build.py. Part 7 owns trees, Part 9 graphs (Dijkstra and minimum spanning trees; the indexed heap and lazy invalidation used for Dijkstra are only previewed here by the priority-update question), Parts 10 and 11 dynamic programming (the coin and the candy-style counter-examples hand off to them by part number only), Part 13 sorting internals and Part 14 design problems (rate limiters, schedulers as systems). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: intervals are lists [start, end]; unless a prompt says otherwise they are half-open, so a meeting that ends at 5 does not clash with one starting at 5, and the merge, insert, intersection, balloon and employee-free-time questions say explicitly that they use closed intervals; a heap here is Python's heapq (a min-heap on a list), so every max-heap is written with negated values or a wrapper class; every solution is iterative, so no prompt depends on CPython's recursion limit of 1000, and the stated sizes (up to 10^5) were chosen for iterative heap and sorting solutions. Questions whose output is not unique say what the checker accepts: k closest points, reorganize string, k pairs with smallest sums, Huffman code lengths and the k-distance rearrangement are validated by property (same multiset, adjacency or distance rule, optimal sums or cost), and the examples show one accepted answer; the others state their tie rules (top-k words by count then alphabet, gas station smallest start, smallest range by width then start, meeting rooms III smallest room, FIFO among equal priorities, stable ties in nlargest). Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example below is rendered from the same data that scratch/B5P08_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force on thousands of random small inputs (sorted-list simulation, all subsets, all permutations, breadth-first search over schedules, exhaustive assignment, all contiguous splits, all subsets of a coordinate range) for kth largest and the stream, merge intervals (checked on a doubled-coordinate point set), insert, meeting rooms I and II (heap against sweep against point counting), non-overlapping intervals, intersections, maximum events (bipartite matching), balloons (hitting sets), employee free time (unit slots), top-k words, merge k arrays, median stream, last stone, cookies, sticks (all merge orders), furthest building (all brick and ladder choices), IPO (all project orders), smallest range, sliding median (including 3000 tie-heavy values and window sizes 1 to 3000), greedy days (all splits), meeting rooms III, candy (every rating array with values 0 to 2 up to length 4, plus random length 6), partition labels (all cut sets) and jump games (reachability dynamic programme). Claims tested exhaustively: the textbook bottom-up build-heap never exceeds n - popcount(n) swaps and reaches it, checked over every permutation of up to 8 distinct values, and the node heights of an n-node complete tree sum to n - popcount(n) for every n up to 2000, while CPython's own heapify layout differs from the textbook sift-down layout on about 14 percent of random lists (so the heap-internals prompt defines the textbook procedure exactly); the one-by-one build equals heappush layouts; the task-scheduler formula equals a heap simulation equals a breadth-first search over schedules for every sorted multiset of up to 7 tasks over three letters and cooldowns 0 to 3; reorganize string is possible exactly when the maximum letter count is at most (len + 1) // 2 for all 3^L strings up to length 7 over three letters (582 infeasible ones), and the k-distance rearrangement returns the empty string exactly when no permutation works (all those strings, k from 0 to 5); the gas-station answer equals the smallest valid start, and unique starts are not guaranteed (about a third of random small inputs have several valid starts, so the prompt asks for the smallest index); queue reconstruction recovers the original queue and the pairs of any queue are distinct and determine it uniquely for every queue of up to 6 people with heights 1 to 3; in activity selection earliest-finish matches brute force while shortest-first and earliest-start-first both first fail at exactly 3 activities and never with 1 or 2 (times 0 to 6); the largest-coin-first counter-example search needs only amounts below coins[-1] + coins[-2], checked for all 2047 coin systems with largest coin up to 12 (1854 non-canonical) against amounts up to 200, plus 300 random systems with a larger top coin; the day count of the greedy feasibility check is non-increasing in capacity; Huffman cost is the same for random tie-breaking, equals an exhaustive search over all full binary trees and equals the sticks answer; heapq.nlargest and nsmallest equal the stable sorted slices for every list of up to 6 scores with heavy ties; quickselect with first-element pivot and three-way partitions finishes in 1 round on all-equal input and needs len rounds on an ascending list with k = 1; lazy deletion never holds more heap entries than pushes and never pops more than pushes; pushing (priority, dict) tuples raises TypeError on ties while (priority, id) silently orders ties alphabetically instead of by arrival; a string cannot be negated. All solutions run at the stated limits (kth largest, sliding median and a 100-way merge over 10^5 values) without recursion. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part08_sources.md). Searches returned heap-pattern guides (igotanoffer, a LeetCode discuss post on four heap patterns, techinterview.org, DesignGurus), techinterview.org interval and greedy pattern pages, snippets of the heapq documentation recipe on entry counters and removed-task markers, Naukri Code360 candidate-reported entries (a Flipkart August 2022 write-up and an Amazon August 2021 online round with merge intervals, a Flipkart May 2021 online test with merge k sorted arrays) and canonical coin-system papers (Kozen and Zaks); nothing was found tying kth-largest, meeting rooms, task scheduler, median of a stream, candy, jump game or the other items to a named company beyond those entries, so 'Asked at' tags name source types (pattern guides, candidate-reported snippets, editor knowledge of standard lists), not verified company reports. The snippets did not cover partition labels, queue reconstruction, furthest building, IPO, smallest range or meeting rooms III, which come from editor knowledge. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

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
assert not re.search(r'(?i)\blpa\b|salary|\brs \d', txt.split('Evidence limits')[0].replace('No salary figures', ''))
open('Book5_DSA/Book5_DSA_Part08.md', 'w', encoding='utf-8', newline='\n').write(txt)
rows_i = ''.join(f"| B5P08-Q{i} | 8 | {q.strip()} |\n" for i, (s, d, key, q, a) in enumerate(QS, 1))
open('scratch/B5P08_wavea/index_rows.txt', 'w', encoding='utf-8', newline='\n').write(rows_i)
idx = open('question_index.md', encoding='utf-8').read()
if 'B5P08-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8', newline='\n').write(idx + rows_i)
print('built', n, c)
for i, (s, d, key, q, a) in enumerate(QS, 1): print(i, s, d, key)
