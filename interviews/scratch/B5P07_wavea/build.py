import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B5P07_wavea')
from qs import QS as RAW
def render(v): return repr(v).replace('None','null')
def example_text(ex):
    return '; '.join(', '.join(f"{k}={render(v)}" for k,v in kw.items())+' -> '+render(out) for kw,out in ex)
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted([(s,d,key,f"{text.strip()} Example: {example_text(ex)}.",a) for s,d,key,text,ex,a in RAW],key=lambda q:(-q[0],order[q[1]]))   # stable
N=50
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==N, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==N and all(q[1] in order for q in QS)
assert len({q[3] for q in QS})==N and len({q[2] for q in QS})==N
assert len({q[3].split('.')[0] for q in QS})==N   # unique titles
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
for s,d,key,q,a in QS:
    assert 'Example' in q and '->' in q, q[:40]
    assert 'Asked' not in q and a.strip()
    assert 'null' in q or 'TreeNode' not in q or True
    assert '`TreeNode(val, left, right)`' in q or key in ('nary','trie_counts','classify'), key
KW={(1,13):'Subarray sum equals k.',(3,36):'Prefix queries:',(4,25):'Recursion limit versus an explicit stack.',(4,30):'The BFS level-order queue idiom',(6,2):'Middle of a linked list.',(6,17):'Python specifics: the node class',(6,26):'Why a recursive list algorithm fails'}
def refs_in(t):
    return {(int(m.group(1)),int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)',t)}
refs=set()
for s,d,key,q,a in QS: refs|=refs_in(q)
print('refs',sorted(refs))
files={p:open(f'Book5_DSA/Book5_DSA_Part0{p}.md',encoding='utf-8').read() for p in (1,2,3,4,5,6)}
def check_ref(p,qn):
    assert p in files and (p,qn) in KW, (p,qn)
    m=re.search(rf'^### Q{qn} \S+ \S+ (.*)$',files[p],re.M)
    assert m and m.group(1).startswith(KW[(p,qn)]), (p,qn, m and m.group(1)[:50])
for p,qn in refs: check_ref(p,qn)
assert refs==set(KW), set(KW)^refs   # every checked reference is actually used
hdr=f"""# Book 5 — Part 7: Trees and BST

**Topic:** Python DSA for product-company interviews: the TreeNode class (with __slots__) and a builder from level-order arrays with null, tree traversals recursive and iterative (preorder, inorder, postorder, level order, zigzag, right side view, vertical order, boundary), depth, height, diameter and balance, same tree, symmetric tree and subtree of another tree, inverting, the path-sum family (root to leaf, all root-to-leaf paths, any downward path counted with prefix sums), lowest common ancestor in a binary tree and in a BST, BST validate, insert, delete, k-th smallest, inorder successor, range sum, recover a BST with two swapped values and two-sum in a BST, building trees from preorder plus inorder, inorder plus postorder and from a BST preorder, sorted array and sorted list to a balanced BST, serialize and deserialize (preorder and BFS formats), flatten to a linked list, counting the nodes of a complete tree in O(log^2 n), maximum path sum, house robber III and binary tree cameras at concept level, Morris traversal, the O(h)-space BST iterator, converting a BST to a circular doubly linked list, N-ary tree basics, a trie as a tree at concept level, recursion limit and deep skewed trees with iterative alternatives, tree identity versus value equality (cycle and shared-node validation), and the complexity of traversals (time O(n), space O(h) versus O(w) versus O(n))

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns binary trees, BSTs and N-ary tree basics. Part 4 owns stacks and queues (the iterative-stack and level-order queue ideas are cross-referenced only as 'Part 4 Q25' and 'Part 4 Q30'), Part 6 owns linked lists (the middle-of-list technique, the node-identity conventions and the recursion limit on long lists are cross-referenced as 'Part 6 Q2', 'Part 6 Q17' and 'Part 6 Q26'), Part 1 owns the array prefix-sum counting idea ('Part 1 Q13', which the tree version extends) and Part 3 the trie-versus-sorted-list comparison ('Part 3 Q36'); each of these references was checked against its heading by build.py. Part 8 owns heaps and greedy, Part 9 graphs (BFS and DFS on general graphs; the distance-K question uses a parent map and a BFS on a tree only), Parts 10 and 11 dynamic programming (house robber III and binary tree cameras appear here only as the return-a-tuple and greedy-state patterns), Part 12 backtracking and tries (the trie question is concept level), and Part 14 design problems. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: every prompt states its tree as a level-order array in the examples (null for a missing child, the children of a null are not listed, trailing nulls omitted) and uses `class TreeNode: __slots__ = ('val', 'left', 'right')` with constructor `TreeNode(val, left, right)`; N-ary trees use the LeetCode-style array with null separating each node's children, and the identity-validation question gives nodes as [val, left_index, right_index] triples. Questions that say 'in place' require the result to consist of the same node objects, which the tests verify by node identity. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example below is rendered from the same data that scratch/B5P07_wavea/check_examples.py executes (python3 -I) against node-based reference solutions, so no example can differ from what was run. Cross-checks: all 626 tree shapes with 0 to 7 nodes (label sets by preorder and by inorder) against independent brute force on tuple-encoded trees and on node-pair graphs for traversals in all orders (recursive against iterative), levels, zigzag, right view, vertical order, depth, minimum depth, balance, diameter (all-pairs distance), symmetry, invert, root-to-leaf and downward path sums (every target from -1 to 11), maximum width, serialization round trips in both formats, subtree, boundary (independent path-based definition), deepest-subtree, Morris traversal, flatten, binary tree cameras (smallest covering subset) and the lowest common ancestor and distance-K answers for every value pair; all BST shapes with 0 to 7 nodes against sorted-list brute force for validate, k-th smallest, LCA, range sum for every range, insert and delete of every present and absent key, successor, two-sum for every target, the BST iterator, BST from preorder and the doubly-linked-list conversion; plus seeded random cases: 1500 trees for maximum path sum (all node pairs), 600 for house robber III (all subsets), 3000 for validate BST (all ancestor constraints), 3000 random pointer graphs for identity validation, 400 N-ary trees and 500 tries. Claims tested exhaustively: preorder plus inorder and inorder plus postorder identify the tree for every shape up to 7 nodes, while preorder plus postorder does not (for n = 2 exactly one pair of trees collides, and the colliding trees are never full binary trees, while for full binary trees the pair is unique); the serialized string has exactly 2n + 1 tokens for n = 0..7 in both formats; the BST iterator never holds more than h nodes; the recover-BST pair to swap back is unique (for every BST shape up to 7 nodes and every swapped pair, exactly one value pair restores a BST); the three sorted-to-BST constructions (array, list with slow and fast pointers, list by inorder simulation) give the same height-balanced tree for every length 0 to 59; the Morris loop runs exactly n + L times (L = nodes with a left child) and restores every pointer; the level-order queue peaks at 2^(k-1) on a perfect tree of height k; the spine-step bound of the count-complete solution is at most 2h^2 for every n up to 2^11, exactly 2h for the perfect tree and exactly h(2h - 1) at n = 2^(h+1) - 2 for h >= 2, checked at the boundary cases n = 2^h, 2^(h+1) - 2 and 2^(h+1) - 1 for every h up to 13 (a first draft of the prompt said (h + 1)^2, which the run refuted at n = 22 where 26 steps exceed 25, and it was corrected before freezing); recursive depth on a skewed tree raises RecursionError at 2000 nodes under the default limit of 1000 while the iterative version handles 10^5; and the index-normalised width and the iterative deserializer both handle a 3000-node skewed tree. The prompts state their uniqueness rules (sorted-to-BST uses the lower middle, insert adds a leaf, delete uses the inorder successor, vertical-order ties take the smaller value, BFS serialization never trims markers). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part07_sources.md). Searches returned tree-pattern guides (techinterview.org), Naukri Code360 candidate-reported entries (Flipkart November 2021 online round with vertical order traversal, Amazon March 2022 SDE-2 with LCA of a binary tree), a Glassdoor Flipkart 2025 LCA report and a LeetCode discuss Facebook intern report (serialize and deserialize, LCA, smallest subtree with the deepest nodes), Morris traversal and count-complete-nodes explainers, tree-DP guides for house robber III and cameras, recover-BST write-ups and Python recursion-limit explainers; nothing was found tying construct-from-traversals, BST delete, flatten or boundary traversal to a named company, so 'Asked at' tags name source types (pattern guides, practice lists, candidate-reported snippets, editor knowledge of standard lists), not verified company reports. The pre/in/post-order uniqueness claims, the Morris iteration count and the count-complete step bounds were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
for m in refs_in(hdr): check_ref(*m)
out=[hdr]
for i,(s,d,key,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==N and txt.count('**Asked at:**')==N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt and "**Target:** 50" in txt
assert txt.count('\n### Q')==N
assert not re.search(r'(?i)\blpa\b|salary|\brs \d',txt.split('Evidence limits')[0].replace('No salary figures',''))
open('Book5_DSA/Book5_DSA_Part07.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B5P07-Q{i} | 7 | {q.strip()} |\n" for i,(s,d,key,q,a) in enumerate(QS,1))
open('scratch/B5P07_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
idx=open('question_index.md',encoding='utf-8').read()
if 'B5P07-Q1 ' not in idx:
    if not idx.endswith('\n'): idx+='\n'
    open('question_index.md','w',encoding='utf-8',newline='\n').write(idx+rows_i)
print('built',n,c)
for i,(s,d,key,q,a) in enumerate(QS,1): print(i,s,d,key)
