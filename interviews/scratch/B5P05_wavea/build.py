import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B5P05_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
N=40
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==N, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==N and all(q[1] in order for q in QS)
assert len({q[2] for q in QS})==N
assert len({q[2].split('.')[0] for q in QS})==N   # unique titles
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
for s,d,q,a in QS:
    assert 'Example' in q and '->' in q, q[:40]
    assert 'Asked' not in q and a.strip()
# resolve every 'Part N Qn' reference against the built part files, by checked heading keyword
KW={(1,28):'Find the duplicate number.',(2,38):'Longest mountain in an array.',(2,40):'K-th smallest in the union of two sorted lists',(3,36):'Prefix queries: sorted list versus trie',(3,40):'Longest repeated substring'}
def refs_in(t):
    out=set()
    for m in re.finditer(r'Part (\d+) Q(\d+)',t): out.add((int(m.group(1)),int(m.group(2))))
    return out
refs=set()
for s,d,q,a in QS: refs|=refs_in(q)
print('refs',sorted(refs))
files={p:open(f'Book5_DSA/Book5_DSA_Part0{p}.md',encoding='utf-8').read() for p in (1,2,3,4)}
def check_ref(p,qn):
    assert p in (1,2,3,4) and (p,qn) in KW, (p,qn)
    m=re.search(rf'^### Q{qn} \S+ \S+ (.*)$',files[p],re.M)
    assert m and m.group(1).startswith(KW[(p,qn)]), (p,qn, m and m.group(1)[:50])
for p,qn in refs: check_ref(p,qn)
hdr=f"""# Book 5 — Part 5: Binary search (including binary search on the answer)

**Topic:** Python DSA for product-company interviews: classic binary search and its loop invariants (closed versus half-open templates, lo<hi versus lo<=hi, mid rounding), lower and upper bound semantics and the bisect module (bisect_left, bisect_right, insort, the key= parameter on Python 3.10+), first and last position, search insert position, rotated sorted arrays (distinct values and with duplicates) and the minimum of a rotated array, peak element, mountain array search under a call budget, search in a 2D matrix (flattened and row-and-column sorted variants), integer square root, perfect square and integer k-th root, binary search on the answer (Koko eating bananas, capacity to ship packages, split array largest sum, allocate books, minimum days for bouquets, aggressive cows style max-min distance, cutting logs, k-th missing positive), median of two sorted arrays and the k-th element of two sorted arrays, k-th smallest in a sorted matrix, the median of a row-sorted matrix, k-th in a multiplication table and k-th smallest pair distance (search on value with counting), k closest elements, single element in a sorted array of pairs, exponential search in an array of unknown length, floating-point binary search and termination (fixed iterations versus epsilon: maximum average subarray, gas stations), and monotonic predicate design with counterexamples

**Target:** 40  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns binary search on indices, on values and on the answer, plus the bisect module. The greedy feasibility checks used as predicates (ship loading, cow placement, bouquet counting, split pieces) are only predicates here; the theory of why those greedy rules are optimal belongs to Part 8 (heaps, intervals, greedy). Part 1 owns hashing and the value-range plus Floyd solutions of find the duplicate number (cross-referenced only as 'Part 1 Q28', checked against its heading; the pair-distance question here is a different counting problem). Part 2 owns the two-pointer and window versions: longest mountain by one pass and the O(k) merge walk for the k-th element of two sorted lists (cross-referenced as 'Part 2 Q38, Q40', each checked against its heading; the questions here are the call-budget mountain search and the O(log) k-th element). Part 3 owns prefix queries with a sorted list and bisect and the rolling-hash plus binary-search longest repeated substring (cross-referenced as 'Part 3 Q36, Q40', each checked against its heading; the questions here contrast with them rather than repeat them). Part 7 owns binary search trees, Part 13 owns math and number theory and randomized algorithms (integer roots and square roots here are the binary-search forms only). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force or independent reference code (scratch/B5P05_wavea/check_examples.py, python3 -I) before freezing. Claims were tested exhaustively where they could be: exactly-k versus at-most-k splitting (400 random small cases), the is-bad call budget ceil(log2 n) for every n < 300 and every boundary, the two bisect templates on every monotone predicate with n < 12, the k-closest tie rule (3000 random small cases, tie-break by value versus by index gives the same list), k-th missing positive (1000 random), multiplication-table counting (all m, n <= 5 and every k), maximum average and gas-station predicates against brute force, the mountain search call count (worst observed 55 of the 100-call budget, including n = 10^4), the non-termination of an epsilon loop at eps = 1e-15 for x = 10**6, and that int(125 ** (1/3)) is 4 in CPython. The peak-element prompt states that its answer is NOT unique and the checker accepts any peak (both peaks of the second example were enumerated); the single-element prompt states that the lone value is unique by the statement. The prompts were written once, and all examples passed on the first full run of the checker. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org and neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part05_sources.md). Searches returned binary-search pattern guides and question roundups, a median-of-two-arrays explainer and candidate-reported Flipkart items on Naukri Code360 (an Allocate Books entry from 2021 and a rotated-array search entry; one aggregator, reports spanning 2015-2022); no Amazon India, Google or Microsoft report naming these problems was found (a jointaro page carried a Microsoft company filter but its content was not verified), so 'Asked at' tags name source types (pattern guides, practice lists, candidate-reported snippets, Python docs mirrors, editor knowledge of standard lists), not verified company reports. The bisect key= behaviour (key added in 3.10, not applied to the search value in bisect_left/bisect_right, applied to it in insort) rests on docs snippets plus a sandbox run on Python 3.13. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
for m in refs_in(hdr): check_ref(*m)
for p,qn in {(1,28),(2,38),(2,40),(3,36),(3,40)}: assert f'Q{qn}' in hdr
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==N and txt.count('**Asked at:**')==N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt
assert txt.count('\n### Q')==N
assert not re.search(r'(?i)lpa|salary|rs \d',txt.split('Evidence limits')[0].replace('No salary figures','')) 
os.makedirs('Book5_DSA',exist_ok=True)
open('Book5_DSA/Book5_DSA_Part05.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B5P05-Q{i} | 5 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B5P05_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
idx=open('question_index.md',encoding='utf-8').read()
if 'B5P05-Q1 ' not in idx:
    if not idx.endswith('\n'): idx+='\n'
    open('question_index.md','w',encoding='utf-8',newline='\n').write(idx+rows_i)
print('built',n,c)
