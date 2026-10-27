# Book 5 Part 6 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the four answer agents). Scope: 35 questions, Q1-Q35 (DSA in Python: linked lists). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-9, Q10-18, Q19-27, Q28-35; merged by heading: 35 of 35 merged, 0 skipped, 0 pending. All four were stopped once by a spend limit and resumed with SendMessage; their saved per-question files let them continue (the Q1-9 agent had already finished). Wave A ran every prompt example against node-based reference code and brute force (`scratch/B5P06_wavea/check_examples.py`) and corrected the Floyd meeting-time wording before freezing; each answer agent re-ran the examples.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q35; star order and counts 13 / 13 / 9 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 35 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 35 of 35 exit 0 |
| Cross-references (Part 1 Q28; Part 2 Q44) | verified by Wave A's build.py |

Every code block builds its own lists, guards against cycles when printing or comparing, and verifies "in place" claims by node identity; each has a brute force, a seeded or exhaustive cross-check (e.g. all 240 and 900 (mu, lambda) pairs; all 330 sorted multisets; all 0/1/2 lists up to length 8) and edge asserts.

## Corrections made during review
- The Floyd meeting-time bound was stated as `t < mu + lambda` in the part header and in Q6's complexity line (and in the Wave A sources note). The Q28-35 agent found that false at mu = 0, where t = lambda. Corrected to `t <= mu + lambda` (equality only at mu = 0; t is the smallest positive multiple of lambda that is at least mu) in the part file, the Wave A header source (`build.py`) and the sources note. Q33's answer already states the correct bound and the exact move count 3t + lambda + 2mu (at most 5mu + 4lambda, reached at mu = 0).

## Prompt notes handled in the answers (frozen prompts otherwise unchanged)
- Q1: the prompt allows 5,000 nodes but a recursive reverse raises RecursionError at 5,000 under the default limit of 1,000; the answer shows the limit raised to 20,000 working. Q8: `int()` of a 5,000-digit string raises ValueError under the default limit. Q26: the smallest failing recursion length printed 999 here (varies with caller depth). Q31: the recursive flatten fails on a 1,200-deep child chain while the iterative version works.
- Q10: "both pointers travel m + n steps" is loose; with no intersection the switch trick takes m + n + 1 moves (the last lands on None); the answer gives exact counts.
- Q28: the O(n)-when-sorted claim holds only with the compare-with-last shortcut; without it sorted input is the worst case (19,900 comparisons at n = 200) and reversed the best (199); even with the shortcut a list with the maximum first and the rest ascending costs about n^2/2 (20,099).
- Q34: the cut node is always the original tail (index n-1) whenever a cycle exists (checked on 325 exhaustive cases), stated in the answer.
- Q18: the node-VALUES variant is tagged "candidate-reported Flipkart" in the prompt but rests only on a search snippet (a LeetCode discuss post, no page opened); the answer adds no company claim.

## Demonstrated bugs (real runs)
A value swap fails the identity check and a wrong assignment order creates a cycle (Q19); testing `odd` instead of `even` raises AttributeError for lengths 2, 4, 6, 8 (Q20); omitting `l.next = None` creates a cycle (Q21); reversing without restoring leaves the input head as the tail (Q23); a set of values wrongly flags `[1,1,1]` as a palindrome-cycle case (Q4); a harness that catches a reverse building new nodes and one creating a cycle (Q32).

## Not run / sandbox-only
Q17's `__slots__` memory figures (about 89 vs 129 bytes per node) are sandbox-only and labelled; Q17's node class skips the shared helper preamble so `from_array` returns just the head.

## Evidence limits
Candidate-reported items found: an Amazon flatten-multilevel-list entry (March 2021), an add-two-numbers entry (December 2021), Flipkart reverse-list entries (2020, 2021) and a Reverse Linked List II variant (June 2024), all via snippets; nothing company-specific for reverse in k-groups, merge k, copy with random pointer or LRU (the LRU question rests on editor knowledge). Every WebFetch failed (5 searches, snippets only). See research_notes/Book5_Part06_sources.md.
