import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B5P04_wavea')
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
KW={(2,14):'Trapping rain water.',(2,16):'Sliding window maximum.',(2,43):'Shortest subarray with sum at least k',(3,13):'Basic calculator without parentheses'}
refs=set()
for s,d,q,a in QS:
    for m in re.finditer(r'Part (\d+) Q(\d+)',q): refs.add((int(m.group(1)),int(m.group(2))))
print('refs',sorted(refs))
files={p:open(f'Book5_DSA/Book5_DSA_Part0{p}.md',encoding='utf-8').read() for p in (1,2,3)}
for (p,qn) in refs:
    assert p in (1,2,3) and (p,qn) in KW, (p,qn)
    m=re.search(rf'^### Q{qn} \S+ \S+ (.*)$',files[p],re.M)
    assert m and m.group(1).startswith(KW[(p,qn)]), (p,qn, m and m.group(1)[:50])
hdr=f"""# Book 5 — Part 4: Stack, queue, monotonic stack

**Topic:** Python DSA for product-company interviews: bracket matching and validation (valid parentheses, minimum removals, longest valid parentheses), stacks with extra O(1) powers (min stack, max stack with popMax), stack-based parsing and evaluation (reverse Polish notation, calculators with parentheses and with all four operators, decode string, simplify path, exclusive time of functions, backspace compare, adjacent-duplicate removal), queue and stack implemented from each other (queue via two stacks, stack via queues), ring buffers (circular queue, circular deque), monotonic stack (next greater and next smaller, circular next greater, daily temperatures, stock span, previous and next smaller indices, largest rectangle in a histogram, maximal rectangle in a binary matrix, trapping rain water by layers, sum of subarray minimums, visible people, the 132 pattern), monotonic-greedy string problems (remove k digits, remove duplicate letters), car fleet and asteroid-style stack simulation, monotonic deque as a reusable class and as DP speed-up (jump game with window maximum), validate stack sequences, BFS-level queue idiom and undo/redo plus browser history at concept level only, and Python specifics (list as stack, deque versus list.pop(0), queue.Queue versus deque thread-safety, recursion limit versus explicit stack and the recursion-to-stack recipe)

**Target:** 40  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns stacks, queues, deques and the monotonic stack and queue patterns, plus the Python specifics around them. Part 2 already owns the plain sliding-window-maximum prompt, trapping rain water by prefix/suffix maxima and two pointers, shortest subarray with sum at least k (deque over prefix sums) and the two-deque max-minus-min window (cross-referenced here only as 'Part 2 Q14, Q16, Q43', each checked against its heading; none of those prompts is repeated, and the questions here are the stack version of rain water, a reusable monotonic-queue class with the duplicate rule, and a different deque DP, the jump game with window maximum). Part 3 owns the single-pass calculator without stack design (cross-referenced as 'Part 3 Q13', checked against its heading; the calculator questions here are the stack-of-contexts versions with parentheses). Part 1 owns hashing; Part 5 binary search; Part 7 trees (iterative traversals belong there, so the explicit-stack question here uses nested lists); Part 8 heaps, intervals and greedy; Part 9 graphs (the BFS-level question here is the queue idiom on a tiny hand-built dict, concept level only); Part 14 owns design problems (undo/redo and browser history here are concept level with two stacks). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force or independent reference code (scratch/B5P04_wavea/check_examples.py, python3 -I) before freezing, including a check that CPython's default recursion limit of 1000 raises RecursionError on a 5000-deep chain and that floor division gives -4 for 7 // -2; all examples passed on the first full run after one flawed car-fleet reference simulation (my own checker bug, not a prompt example) was rewritten. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part04_sources.md). Searches returned monotonic-stack pattern guides, a stacks-and-queues roundup and a few candidate-reported Amazon items for the queue/stack conversion questions; the searches for TCS and Infosys returned only a generic fresher list and no stack or queue problem attributed to either, and no query surfaced Google or Microsoft reports, so 'Asked at' tags name source types (pattern guides and practice lists, prep roundups, candidate-reported snippets, Python docs mirrors, editor knowledge of standard lists), not verified company reports; company tags on community pages are unverified. The queue-module documentation was not found, so queue.Queue claims rest on editor knowledge plus the sandbox run. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==N and txt.count('**Asked at:**')==N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt
assert txt.count('\n### Q')==N
# header refs resolve too
for m in re.finditer(r"Part (\d+) Q(\d+)",hdr): assert (int(m.group(1)),int(m.group(2))) in KW
os.makedirs('Book5_DSA',exist_ok=True)
open('Book5_DSA/Book5_DSA_Part04.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B5P04-Q{i} | 4 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B5P04_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
idx=open('question_index.md',encoding='utf-8').read()
if 'B5P04-Q1 ' not in idx:
    if not idx.endswith('\n'): idx+='\n'
    open('question_index.md','w',encoding='utf-8',newline='\n').write(idx+rows_i)
print('built',n,c)
