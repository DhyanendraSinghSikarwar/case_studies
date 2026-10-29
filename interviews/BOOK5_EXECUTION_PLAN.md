# BOOK5_EXECUTION_PLAN.md — How Book 5 (DSA in Python, 14 parts) will be built

Follows plan.md §4 (answer template, Book 5 extras), §5 (Book 5 table), §11 (workflow) and style_guide.md. Books 1-4 are complete (728 + 558 + 501 + 500 Qs). Band: Rs 30-80 LPA roles at product companies; no salary figures. Output files: `Book5_DSA/Book5_DSA_PartNN.md`.

## Pipeline (same as Books 2-4)
1. **Wave A (one research agent per part):** research real DSA interview problems for the pattern (public problem lists, pattern guides, company-tagged lists; record opened vs snippet-only pages; paraphrase problems, never copy statements verbatim), freeze the list in `Book5_DSA/Book5_DSA_PartNN.md` with ANSWER_PENDING, append `B5PNN-Qn` rows to question_index.md, write `research_notes/Book5_PartNN_sources.md`. Script `scratch/B5PNN_wavea/build.py` (copy `scratch/B4P12_wavea/build.py` and `qs.py`; asserts: count, stars sorted 3,2,1, difficulty easy to hard inside a star, unique prompts, header counts, ANSWER_PENDING and Asked-at counts).
2. **Wave B (4 answer agents per part, about 10-12 Qs each, own folder `scratch/B5PNN_Qxx-yy/answers.md`; each agent writes progress to disk early so a spend-limit stop loses nothing):** lead merges by heading with `scratch/B5PNN_merge/merge.py` (copy `scratch/B4P12_merge/merge.py`, change paths).
3. **Wave C (lead):** structure check, re-run every code block (these ARE runnable standalone, so the lead re-runs them all), spot-check, `review_notes/Book5_PartNN_review.md`, update plan.md tracker and this checklist, fetch then plain push (never force).

## Book 5 answer template
Per question, in order: `### Qn stars emoji text` / `**Asked at:**` / **Pattern:** (name the pattern and why it applies) / **Say this first (1 line):** / **Brute force:** (idea, complexity) / **Optimal:** (idea, why it works, invariant) / **Complexity:** (time and space, with the reasoning) / **Dry run:** (hand trace on a small input) / **Code:** (ONE python block: the brute force, the optimal solution, a randomised cross-check of optimal against brute force on seeded small inputs, edge-case asserts; prints results) / **Output (my run):** (pasted real output) / **Edge cases:** / **Follow-ups:** (1-3 with short answers) / **Common mistakes:**. Spoken-interview tone, short sentences.

## Execution rules
- Python 3.13, standard library (collections, heapq, bisect, itertools, functools) plus sortedcontainers only where the question says so. Every block runs with `python3 -I` and is self-contained.
- Complexity claims are reasoned from the code; empirical timings (if any) are sandbox-only and labelled; never present timings as proof of big-O.
- Seed all randomness; cross-check optimal vs brute force over at least a few hundred seeded random small cases; include the adversarial edge cases (empty, single, duplicates, negatives, all equal, max size).
- Paraphrase problem statements; name well-known problems by common names only. No company claims beyond "commonly reported in public lists" and no salary figures.
- Python specifics to state where relevant: recursion limit, integer overflow absent, `heapq` is a min-heap, `list.pop(0)` is O(n), `bisect` semantics, mutable default args, `dict` ordering, `sorted` stability, `lru_cache` on mutable args.
- Scope: Book 3 owns SQL; Book 4 owns systems; Book 1 owns ML maths. Parts are pattern-pure: tag cross-pattern problems to the part whose pattern is the key insight; cross-reference earlier Book 5 parts by checked heading only.

## Part checklist (targets from plan.md)
| Part | Pattern | Target | Wave A | Wave B | Wave C |
|---|---|---|---|---|---|
| 1 | Arrays and hashing | 50 | ✅ (50 Qs) | ✅ | ✅ |
| 2 | Two pointers and sliding window | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 3 | Strings | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 4 | Stack, queue, monotonic stack | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 5 | Binary search (incl. on answer) | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 6 | Linked lists | 35 | ✅ (35 Qs) | ✅ | ✅ |
| 7 | Trees and BST | 50 | ✅ (50 Qs) | ✅ | ✅ |
| 8 | Heaps, intervals, greedy | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 9 | Graphs (BFS/DFS, topo sort, Dijkstra, union-find) | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 10 | Dynamic programming I (1D, knapsack) | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 11 | Dynamic programming II (2D, strings, intervals) | 35 | ✅ (35 Qs) | ✅ | ✅ |
| 12 | Backtracking, tries, bit manipulation, DS-flavoured DSA | 35 | ⬜ | ⬜ | ⬜ |
| 13 | Extra I: prefix sums, matrices/2D grids, math and number theory, randomized algorithms, sorting internals | 50 | ⬜ | ⬜ | ⬜ |
| 14 | Extra II: design problems, advanced graphs, segment/Fenwick trees, mixed company mock sets | 50 | ⬜ | ⬜ | ⬜ |

## Process notes
Split Wave B into agents of about 10-12 questions; tell agents to stop and report (not retry) at a spend limit; commit and push WIP often (a stop hook demands it); after each part's merge run the lead re-run of all code blocks; Part 14 includes timed mock sets with scoring like Book 3 Part 12 and Book 4 Part 12 (cross-reference by checked headings).

## Next step
Part 12 Wave A (backtracking, tries, bit manipulation, DS-flavoured DSA; target 35: subsets/permutations/combinations with and without duplicates, combination sum, n-queens, sudoku solver, word search (grid backtracking), palindrome partitioning, generate parentheses, letter combinations of a phone number, restore IP addresses, pruning and the cost of backtracking (count nodes visited), iterative backtracking and recursion depth, tries (insert/search/startsWith, autocomplete with counts, word search II with a trie, longest common prefix via trie, replace words, map sum, memory vs dict-of-sets), bit manipulation (single number I/II/III, count set bits and Brian Kernighan, power of two, reverse bits, bitmask subsets, XOR tricks, missing number, hamming distance, Python's arbitrary-precision ints and negative numbers with & ~ >> (no fixed width: mask to 32 bits explicitly), int.bit_count, bit_length), DS-flavoured items such as union-find in-place structures reference Part 9, LRU as concept (Part 14 owns design), randomised set/insert-delete-getRandom O(1) (check Part 1/13 owners), skip lists/bloom filters concept only, segment/Fenwick trees belong to Part 14). Cross-reference earlier parts only by build.py-verified headings (Part 3 palindrome/tries concept items, Part 7 Q41 trie concept, Part 11 DP enumeration vs count versions). Part 11 lessons: no frozen prompt needed correction when Wave A tested every WHY sentence against the exact claim and recursion boundaries with oracle-backed examples; keep recursion-depth statements as observed and clear of boundaries; state reconstruction/output order rules for backtracking outputs (the order of returned lists must be specified or compared as sets).
