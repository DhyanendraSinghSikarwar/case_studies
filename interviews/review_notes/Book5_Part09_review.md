# Book 5 Part 9 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45 (DSA in Python: graphs, BFS/DFS, topological sort, Dijkstra, union-find). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-11, Q12-22, Q23-33, Q34-45; merged by heading: 45 of 45 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A rendered all 158 examples from the same data the checker runs and cross-checked each of the 45 reference solutions against an independent brute force or validator on 400 seeded inputs; where several outputs are valid (course schedule II, alien dictionary) the prompts state exactly what the validator accepts. Eight questions require an iterative DFS (Q4, Q5, Q6, Q10, Q13's `find`, Q22, Q31, Q44).

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45; star order and counts 15 / 19 / 11 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 45 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 45 of 45 exit 0 |
| Cross-part references (Part 4 Q4 and Q30, Part 7 Q9 and Q35, Part 8 Q29, Q31, Q38) | resolve against the headings of Parts 1-8 (re-checked by the lead) |
| In-part references written as bare "Qn" in answers (e.g. Q25 to Q28 and Q42, Q28 to Q34, Q29 to Q37, Q31 to Q24, Q33 to Q31) | agents checked them; not independently re-verified by the lead beyond the numbering being continuous |

## Corrections made during review (frozen prompts)
- Q22 (undirected cycle with repeated edges) claimed that tracking only the parent node would miss a repeated edge. The Q12-22 agent showed this is not true in general: with list adjacency (each edge stored at both ends), parent-node skipping caught every repeated edge and self loop in an exhaustive test (n <= 3, <= 3 edges), including mark-on-pop and mark-on-push stack variants. The bug appears only when repeated edges collapse into one entry, as with `set` or `dict` adjacency (192 wrong lists; smallest `[[0,1],[0,1]]`). The prompt now says when parent-only tracking misses a repeat and that the edge index is correct for any storage.
- Q15 (word ladder) did not say what to return when `begin` equals `end` and `end` is in `word_list`. The prompt now says 1 (the three methods agreed on this convention).
The lead applied both wordings to the part file, the answer agent's headings, the Wave A prompt sources (`draft.py` and `qs.py`) and the question_index rows.

## Findings kept in the text (observed)
- Dijkstra: finalise-on-first-pop is wrong on 2,897 of the 64,927 three-node graphs (weights -3..3, no reachable negative cycle) and never with non-negative weights (Q42); lazy Dijkstra pushes are at most E+1 and stale pops equal pushes minus reached nodes (61,320 cases, Q25); the stale-check variant matches Bellman-Ford but is exponential on a gadget family (4 expansions on 3 nodes, 22 on 7, 12,286 on 25, outside the n <= 8 bound); a visited-set Dijkstra is wrong on 13 of 20,000 skewed cases and on one hand-built case returning -1 where the answer is 6 (Q34).
- Bellman-Ford: in-place relaxation is wrong on 29 of 2,000 cases (Q34); n-2 rounds are not enough on a reverse-ordered path and an unguarded integer-sentinel version is wrong on 110 of 1,000 graphs (Q28); Floyd-Warshall with k as the inner loop differs on 22 of 300 small graphs (Q35).
- 0-1 grids: ordinary mark-on-enqueue BFS is wrong on 12,914 of 17,557 grids up to 4x4 (Q27) and on 803 of 2,000 in an earlier check; mark-on-push DFS order differs from the recursive preorder (8,876 of 10,810 small graphs; Q38), with peak stack 44,850 vs 299 on K300 (mark-on-pop vs mark-on-push) measured, not proven.
- Sliding puzzle: 720 boards, 360 reachable (even inversions among the five tiles), hardest board needs 21 moves (Q32); open the lock needs the sum of min(digit, 10 - digit) over wheels when there are no dead ends (Q30); minimum height trees have 1 or 2 roots on all 18,248 labelled trees with 2 to 7 nodes (Q45); a topological order is unique exactly when Kahn has one ready node at every step (4,165 loop-free sets, Q9); three points at pairwise distance 2 give 3 different minimum trees of weight 4 (Q37); naive union without union by size builds a 10^5-deep chain (Q13).
- Recursion limit demonstrated with real RecursionError: Q2, Q4, Q5, Q6, Q10, Q13, Q19, Q22, Q31, Q41, Q43, Q44; the iterative versions handle 2*10^5-node paths, 300x300 grids and 10^5-node graphs.

## Boundaries and notes
Q36 (Eulerian path, existence test only), Q21 (bipartite, basic colouring) and Q29 (Kruskal, with Prim mentioned) stop at Part 14, which is named by part number only (also Q37 and Q39). Q39 refers to "the number-of-islands-II question later in this part" without a number. Hierholzer, cut property, Boruvka, SCCs and flow are handed to Part 14.

## Evidence limits
No company-reported problems verified; number of islands and word ladder appear in Flipkart candidate-reported snippets (self-reported, unverified); nothing company-specific for course schedule, Dijkstra or union-find; every WebFetch failed (3 searches, snippets only). See research_notes/Book5_Part09_sources.md.
