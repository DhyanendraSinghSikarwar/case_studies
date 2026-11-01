import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B5P13_wavea')
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
# within-part references 'Qn' (not preceded by 'Part N ') must come from verified placeholders and point at the intended question
for s, d, key, q, a in QS:
    for m in re.finditer(r'(?<!Part \d )(?<!Part \d\d )\bQ(\d+)\b', q):
        assert (key, int(m.group(1))) in PLACE, (key, m.group(0))
for key, qn in PLACE:
    assert re.search(rf'\bQ{qn}\b', next(q[3] for q in QS if q[2] == key)), (key, qn)
    assert 1 <= qn <= N
KW = {(1, 11): 'Product of array except self.', (1, 13): 'Subarray sum equals k.', (1, 31): 'Set matrix zeroes.', (1, 35): 'Randomised set with O(1) operations.',
      (1, 47): 'Insert, delete and getRandom with duplicates.', (1, 50): 'Number of submatrices that sum to target.', (1, 14): 'Rotate array in place.',
      (5, 10): 'Search a 2D matrix with sorted rows (flattening variant).', (5, 22): 'Search a 2D matrix with sorted rows and sorted columns.',
      (8, 28): 'Heap internals: sift up, sift down and the build-heap bound.', (8, 36): 'Quickselect with three-way partitioning: exact rounds.',
      (6, 25): 'Sort a list with merge sort in O(1) extra space.'}
def refs_in(t):
    return {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)', t)}
refs = set()
for s, d, key, q, a in QS: refs |= refs_in(q)
print('refs in prompts', sorted(refs))
files = {p: open(f'Book5_DSA/Book5_DSA_Part{p:02d}.md', encoding='utf-8').read() for p in range(1, 13)}
def check_ref(p, qn):
    assert 1 <= p <= 12 and (p, qn) in KW, (p, qn)
    m = re.search(rf'^### Q{qn} \S+ \S+ (.*)$', files[p], re.M)
    assert m and m.group(1).startswith(KW[(p, qn)]), (p, qn, m and m.group(1)[:50])
for r in refs: check_ref(*r)
hdr = f"""# Book 5 — Part 13: Extra I (Prefix Sums, Matrices and 2D Grids, Math and Number Theory, Randomized Algorithms, Sorting Internals)

**Topic:** Python DSA for product-company interviews, the 'Extra I' part: prefix sums and difference arrays (immutable range sums, range addition, car pooling, running sums and the pivot index, counting range sums with merge sort), 2D prefix sums (region sums, matrix block sums, point updates at a basic level, adding to many rectangles with a 2D difference array), matrix manipulation (in-place rotation, spiral and diagonal traversal, set matrix zeroes in O(1) space, Game of Life in place, rotating every layer), math and number theory (Euclid's gcd and lcm, trailing zeroes of n factorial, the prime sieve, factorisation, fast power, modular inverse with pow(a, -1, m) and n choose r modulo a prime, Pascal's triangle, happy number, Excel column numbers, fractions to recurring decimals), fixed-width versus Python integers and floating-point pitfalls (reversing a 32-bit integer, round-half-even, float versus Fraction and Decimal, big-integer Fibonacci and the int-to-string digit limit), randomized algorithms checked exactly by enumerating every random-choice sequence (Fisher-Yates and the classic biased shuffle, reservoir sampling with one slot and k slots, weighted random pick with prefix sums and bisect, rejection sampling, random index of a target value), and sorting internals from scratch (merge sort with exact comparison counts, counting inversions, iterative Lomuto quicksort, Hoare partition, three-way partition on duplicates, heap sort, counting and radix sort, maximum gap in linear time, stability and Python's sort behaviour with key=, reverse=, cmp_to_key and mixed types, adaptive behaviour on nearly sorted input, Timsort's minrun and natural runs, the comparison-sort lower bound).

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns the prefix-sum and difference-array techniques, matrix manipulation, math and number theory, randomized algorithms and sorting from scratch. Part 1 owns hashing and the hashmap prefix-sum count 'Part 1 Q13' (subarray sum equals k), 'Part 1 Q11' (product of array except self), the set matrix zeroes statement at concept level 'Part 1 Q31' (Q{KEYNO['set_matrix_zeroes']} here writes it fully in O(1) space and tests the marker trap), 'Part 1 Q50' (submatrices that sum to a target) and the randomised set 'Part 1 Q35' and its duplicate version 'Part 1 Q47' (not repeated; the reservoir questions here are about one-pass streams). Part 5 owns binary search ('Part 5 Q10' and 'Part 5 Q22' search sorted matrices; not repeated). Part 8 owns heaps and greedy ('Part 8 Q28' heap sift up and down, 'Part 8 Q36' quickselect rounds; heap sort here is the sorting-internals version and kth largest is not repeated). Part 6 owns linked-list merge sort ('Part 6 Q25'). Part 9 owns graph traversal on grids (BFS, DFS, flood fill), Part 12 owns bit manipulation, and Part 14 owns design problems and the Fenwick and segment trees (named here only as the answer for mutable range queries: Q{KEYNO['range_add']}, Q{KEYNO['range_sum_2d_mutable']} and Q{KEYNO['count_range_sum']}).

Fixed-width integers: Python integers have no overflow, so only Q{KEYNO['reverse_int32']} simulates a 32-bit signed integer (it returns both the checked result and what a wrapping machine would hold); Q{KEYNO['gcd_lcm']}, Q{KEYNO['pow_fast']} and Q{KEYNO['pascal_triangle']} ask where a fixed-width language would overflow while the Python answers stay exact. Randomised questions never use a live random generator in the checker: each fixes the random choices as an input list (or enumerates ALL choice sequences for tiny sizes) and states exactly what is accepted (the output order, the draw convention and the exact counts). Every recursive question keeps its depth far below CPython's default recursion limit of 1000, and the two quicksort questions (Q{KEYNO['quicksort_iter']}, Q{KEYNO['three_way']}) require an explicit stack because sorted or all-equal input nests about n frames. Version notes for pow(a, -1, m), math.lcm and the int-to-str digit limit are editor knowledge (behaviour itself was verified by running Python 3.13); the Timsort description in Q{KEYNO['timsort_minrun']} is editor-level and labelled so.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part13_sources.md). Searches returned prefix-sum and difference-array guides (techinterview.org, a LeetCode Discuss study guide, talentd.in topic lists), matrix question lists (Educative, Techie Delight, talentd.in, labuladong), number-theory and math pattern guides (techinterview.org), sampling guides (Wikipedia reservoir sampling, techinterview.org, a Codemia rand7 page), sorting guides (techinterview.org, Techie Delight, GeeksforGeeks) and Python Sorting HOWTO snippets; nothing was found tying any single item to a named company, so 'Asked at' lines name source types only. No salary figures appear anywhere in this part.

---
"""
for m in refs_in(hdr): check_ref(*m)
for m in re.finditer(r"Q\{KEYNO\['(\w+)'\]\}", hdr): raise SystemExit('unrendered')
out = [hdr]
for i, (s, d, key, q, a) in enumerate(QS, 1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt = ''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->') == N and txt.count('**Asked at:**') == N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt and "**Target:** 50" in txt
assert txt.count('\n### Q') == N
assert not re.search(r'(?i)\blpa\b|salary|\brs \d', txt.split('Evidence limits')[0])
assert '\n' not in ''.join(q for _, _, _, q, _ in QS)
for m in re.finditer(r'(?<!Part \d )(?<!Part \d\d )\bQ(\d+)\b', hdr):
    assert 1 <= int(m.group(1)) <= N
open('Book5_DSA/Book5_DSA_Part13.md', 'w', encoding='utf-8', newline='\n').write(txt)
rows_i = ''.join(f"| B5P13-Q{i} | 13 | {q.strip()} |\n" for i, (s, d, key, q, a) in enumerate(QS, 1))
open('scratch/B5P13_wavea/index_rows.txt', 'w', encoding='utf-8', newline='\n').write(rows_i)
idx = open('question_index.md', encoding='utf-8').read()
if 'B5P13-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8', newline='\n').write(idx + rows_i)
print('built', n, c)
for i, (s, d, key, q, a) in enumerate(QS, 1): print(i, s, d, key)
