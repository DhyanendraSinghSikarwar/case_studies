import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B5P01_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==50, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==50 and all(q[1] in order for q in QS)
assert len({q[2] for q in QS})==50
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
for s,d,q,a in QS:
    assert 'Example' in q or 'example' in q or '->' in q, q[:40]
    assert not re.search(r'Part \d+ Q\d+',q)
hdr=f"""# Book 5 — Part 1: Arrays and hashing

**Topic:** Python DSA for product-company interviews: two-sum family and complement lookup, frequency counting, anagram grouping, duplicates and set membership, prefix and suffix products, subarray sums with a hashmap, longest consecutive sequence, top-k frequent, majority element and Boyer-Moore, in-place array rewrites (remove duplicates, move zeroes, rotate, next permutation), index-as-marker and matrix encoding tricks, hash-key design (tuples, sorted strings, counts), Python dict and set internals, collisions and ordering, Counter and defaultdict idioms, sorting versus hashing trade-offs, and concept-level notes on randomised hashing (Bloom filter)

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns arrays, hash maps and hash sets, frequency counting, in-place array rewrites and the prefix-sum-plus-hashmap pattern in its basic form. Part 2 owns two pointers and sliding window; Part 3 strings (anagram and isomorphism questions here are about hashing, not string algorithms); Part 4 stacks, queues and monotonic stacks; Part 5 binary search; Part 6 linked lists; Part 7 trees; Part 8 heaps, intervals and greedy (no interval questions here; heaps appear only as the top-k alternative to bucket counting); Part 9 graphs; Parts 10 and 11 dynamic programming; Part 12 backtracking, tries and bit manipulation (the XOR question here is a prefix-hashmap question); Part 13 owns deep prefix sums, matrices and grids, math and randomised algorithms (this part uses prefix sums only with a hashmap and the Bloom filter only as a concept); Part 14 owns full design problems (LRU, LFU, rate limiter), so the randomised-set questions here are limited to the list-plus-dict trick. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part01_sources.md). No page was found that reports problems asked by a named company, so 'Asked at' tags name source types (public pattern lists, Indian placement and online-assessment prep sheets, commercial prep lists, Python internals explainers), not verified company reports, and company tags inside community sheets contradict each other. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only (sortedcontainers 2.4.0, hypothesis and pytest are installed in the sandbox but used only where a question says so).

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==50 and txt.count('**Asked at:**')==50
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt
assert txt.count('\n### Q')==50
os.makedirs('Book5_DSA',exist_ok=True)
open('Book5_DSA/Book5_DSA_Part01.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B5P01-Q{i} | 1 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B5P01_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
idx=open('question_index.md',encoding='utf-8').read()
if 'B5P01-Q1 ' not in idx:
    if not idx.endswith('\n'): idx+='\n'
    open('question_index.md','w',encoding='utf-8',newline='\n').write(idx+rows_i)
print(n,c)
