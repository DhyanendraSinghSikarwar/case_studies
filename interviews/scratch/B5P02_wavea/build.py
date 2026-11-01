import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B5P02_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
N=45
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==N, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==N and all(q[1] in order for q in QS)
assert len({q[2] for q in QS})==N
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
for s,d,q,a in QS:
    assert 'Example' in q and '->' in q, q[:40]
    assert 'Asked' not in q and a.strip()
# resolve every 'Part N Qn' reference against the built part files, by checked heading keyword
p1=open('Book5_DSA/Book5_DSA_Part01.md',encoding='utf-8').read()
KW={(1,3):'Valid anagram',(1,5):'Move zeroes',(1,6):'Remove duplicates from a sorted array',(1,13):'Subarray sum equals k',(1,22):'Merge sorted array in place'}
refs=set()
for s,d,q,a in QS:
    for m in re.finditer(r'Part (\d+) Q(\d+)',q): refs.add((int(m.group(1)),int(m.group(2))))
print('refs',sorted(refs))
for (p,qn) in refs:
    assert p==1 and (p,qn) in KW, (p,qn)
    m=re.search(rf'^### Q{qn} \S+ \S+ (.*)$',p1,re.M)
    assert m and m.group(1).startswith(KW[(p,qn)]), (qn, m and m.group(1)[:50])
hdr=f"""# Book 5 — Part 2: Two pointers and sliding window

**Topic:** Python DSA for product-company interviews: opposite-ends two pointers (sorted two-sum, container with most water, 3Sum, 3Sum closest, 4Sum, trapping rain water, palindrome variants), same-direction and partition pointers on arrays (remove duplicates keeping at most two, parity partition, Dutch national flag), merging and walking sorted lists, fixed-size windows (maximum average, anagram and permutation windows, cards from the ends), variable windows (longest substring without repeats, minimum window substring, at most k distinct, minimum size subarray sum, character replacement, fruit baskets, flips), counting subarrays with 'at most k minus at most k-1', Counter-state windows, why windows break with negatives and when to switch to prefix sums, the monotonic-deque window maximum, fast and slow pointers on arrays, and invariants and off-by-one patterns

**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns two pointers (opposite ends, same direction, partition, fast and slow on arrays) and sliding windows (fixed, variable, counting, Counter state). Part 1 already owns hashing, prefix sums with a hashmap, and the in-place keep-one remove-duplicates, move-zeroes and merge-into-array tasks (cross-referenced here only as 'Part 1 Q3, Q5, Q6, Q13, Q22', each checked against its heading); Part 3 owns string algorithms proper (KMP, Z, rolling hash, palindromic substrings), so string questions here are windows and pointers only; Part 4 owns stacks, queues and the monotonic stack and queue family (the two window-maximum questions here use the deque idea only); Part 5 owns binary search (including the O(log) two-sorted-arrays selection); Part 6 linked-list two pointers; Part 8 heaps, intervals and greedy (boats-style pairing appears here only as the sort plus two-pointer step); Part 13 owns deep prefix sums. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force reference code (scratch/B5P02_wavea/check_examples.py, python3 -I) before freezing. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part02_sources.md). Searches for TCS NQT, Infosys, Wipro and for Amazon, Google and other company frequency returned only generic pattern guides, so 'Asked at' tags name source types (public pattern lists, pattern guides, Indian placement-style prep sheets, company-tagged prep pages), not verified company reports; company tags on community pages are unverified. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only (sortedcontainers only where a question says so).

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==N and txt.count('**Asked at:**')==N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt
assert txt.count('\n### Q')==N
os.makedirs('Book5_DSA',exist_ok=True)
open('Book5_DSA/Book5_DSA_Part02.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B5P02-Q{i} | 2 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B5P02_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
idx=open('question_index.md',encoding='utf-8').read()
if 'B5P02-Q1 ' not in idx:
    if not idx.endswith('\n'): idx+='\n'
    open('question_index.md','w',encoding='utf-8',newline='\n').write(idx+rows_i)
print('built',n,c)
