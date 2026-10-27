import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B5P06_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
N=35
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
KW={(1,28):'Find the duplicate number.',(2,44):'Circular array loop.'}
def refs_in(t):
    return {(int(m.group(1)),int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)',t)}
refs=set()
for s,d,q,a in QS: refs|=refs_in(q)
print('refs',sorted(refs))
files={p:open(f'Book5_DSA/Book5_DSA_Part0{p}.md',encoding='utf-8').read() for p in (1,2,3,4,5)}
def check_ref(p,qn):
    assert p in files and (p,qn) in KW, (p,qn)
    m=re.search(rf'^### Q{qn} \S+ \S+ (.*)$',files[p],re.M)
    assert m and m.group(1).startswith(KW[(p,qn)]), (p,qn, m and m.group(1)[:50])
for p,qn in refs: check_ref(p,qn)
hdr=f"""# Book 5 — Part 6: Linked lists

**Topic:** Python DSA for product-company interviews: the node class (ListNode with __slots__) and the test harness, identity versus equality, building lists from arrays and printing safely on cycles, the dummy (sentinel) node technique, reversing a list (iterative and recursive), reversing between positions and in k-groups, Floyd cycle detection with the cycle start and its proof, cycle and tail length, removing a cycle, the middle node, palindrome list in O(1) space, merging two sorted lists and k sorted lists (a heap only as the merge tool), removing the n-th node from the end, removing duplicates (sorted, all-duplicated, unsorted), partition, rotate, reorder, odd-even, swap in pairs, adding two numbers (reverse and forward digit order), intersection of two lists, deleting a node given only that node, copying a list with random pointers (hash map and O(1) extra space), flattening a multilevel doubly linked list, sorting a list (top-down and O(1)-space bottom-up merge sort, insertion sort), doubly linked list operations with sentinels, the LRU cache idea at concept level, and why recursion on long lists fails in Python

**Target:** 35  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns pointer manipulation on singly and doubly linked lists. Fast and slow pointers on ARRAYS belong to Part 2 (the circular array loop is cross-referenced only as 'Part 2 Q44', checked against its heading), and the value-range plus Floyd solution of find the duplicate number is Part 1 ('Part 1 Q28', checked against its heading; here Floyd is on node pointers). Part 4 owns stacks and queues, Part 5 binary search, Part 7 trees, Part 8 heaps, intervals and greedy (the merge-k question uses `heapq` only as a merge tool and heap theory is left to Part 8), Part 9 graphs (cycle detection in graphs), and Part 14 owns design problems (the LRU cache here is concept level only: why a doubly linked list plus a dict gives O(1), not the class design). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: every prompt states its list as a Python array in the examples and uses `class ListNode: __slots__ = ('val', 'next')` with constructor `ListNode(val, next)`; cyclic examples are written as an array plus `pos` (the index the tail points back to, -1 for none); random-pointer nodes are written [val, random_index]; the multilevel list is written as a nested array in which a list item is the child list of the node before it. Questions that say 'in place' require the result to consist of the same node objects, which the tests verify by node identity, together with an acyclicity check and a step cap so a broken solution fails instead of hanging. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example was run against node-based reference solutions and independent brute-force code on Python lists (scratch/B5P06_wavea/check_examples.py, python3 -I) before freezing, together with randomised cross-checks (500 random lists for most operations, 300 for the sorts' stability, doubly linked list and LRU checks) and exhaustive checks of claims: Floyd's slow and fast pointers meet after exactly t steps, where t is the smallest positive multiple of the cycle length lambda that is at least the tail length mu, for every mu in 0..15 and lambda in 1..15 (240 pairs), the restart step returns the cycle start for all of them, and t < mu + lambda, which bounds the moves in the cycle-length question; merge-k tie order (lower list index first) in both the heap and the divide-and-conquer versions; stability of both merge sorts and insertion sort by node identity; the recursive reverse raising RecursionError at 2000 nodes under the default limit of 1000 while the iterative one handles 10^5; that a ListNode has no __dict__ and rejects new attributes; that equal-valued nodes compare unequal; and that a value-set cycle check would be wrong (a list [1,1,1] has repeated values but no cycle). The prompts state their uniqueness assumptions: the middle of an even list is the second middle, sorts and partitions are stable, merge ties favour the first list, intersection means shared node objects, and remove-n-th, rotate, reorder and the like have exactly one result list. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part06_sources.md). Searches returned linked-list pattern guides and question roundups, candidate-reported Naukri Code360 entries (Amazon on-campus March 2021 flatten of a multilevel list and December 2021 with adding two numbers; Flipkart 2020 and 2021 reverse linked list, one with an O(n) time O(1) space follow-up; one LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant), Floyd explanations (partial proof sketches only) and Python recursion-limit explainers; nothing was found for reverse in k-groups, merge k sorted lists or LRU cache at a named company, so 'Asked at' tags name source types (pattern guides, practice lists, candidate-reported snippets, editor knowledge of standard lists), not verified company reports. The Floyd proof and the __slots__ behaviour were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
for m in refs_in(hdr): check_ref(*m)
for p,qn in {(1,28),(2,44)}: assert f'Q{qn}' in hdr
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==N and txt.count('**Asked at:**')==N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt
assert txt.count('\n### Q')==N
assert not re.search(r'(?i)lpa|salary|rs \d',txt.split('Evidence limits')[0].replace('No salary figures','')) 
open('Book5_DSA/Book5_DSA_Part06.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B5P06-Q{i} | 6 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B5P06_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
idx=open('question_index.md',encoding='utf-8').read()
if 'B5P06-Q1 ' not in idx:
    if not idx.endswith('\n'): idx+='\n'
    open('question_index.md','w',encoding='utf-8',newline='\n').write(idx+rows_i)
print('built',n,c)
for i,(s,d,q,a) in enumerate(QS,1): print(i,s,d,q.split('.')[0][:60])
