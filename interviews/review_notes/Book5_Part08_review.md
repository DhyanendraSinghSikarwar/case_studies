# Book 5 Part 8 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45 (DSA in Python: heaps, intervals, greedy). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-11, Q12-22, Q23-33, Q34-45; merged by heading: 45 of 45 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A ran all 179 examples against reference solutions and brute force (or validators where several outputs are valid, with the accepted rule stated in the prompt) and tested every bound and uniqueness claim exhaustively on small inputs; every solution is iterative, so nothing depends on the recursion limit.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45; star order and counts 17 / 18 / 10 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 45 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 45 of 45 exit 0 |
| Cross-references (Part 1 Q10, Part 2 Q16 and Q37, Part 4 Q38, Part 5 Q8, Q26 and Q33, Part 6 Q12) | verified by Wave A's build.py |

## Corrections made during review (frozen prompts)
- Q36: "a two-way Lomuto scheme would need n rounds" was imprecise. The agent's two-way simulation at n = 3000 with all-equal values took 1, 1500 and 3000 rounds for k = 1, n/2 and n when equals go to the small side, and 3000, 1501 and 1 with equals on the big side. The prompt now says "a two-way scheme that sends every equal value to the same side needs up to n rounds, depending on k and on which side takes the equals". The allowed n = 10^5 is also a quadratic case with the first-element pivot on an ascending list with k = 1 (about 5*10^9 element visits); the answer says so.
- Q41 (sliding window median): "O(n log k) amortised" is not guaranteed, because stale entries buried below the heap tops can let the heaps grow to O(n) entries. The prompt now states O(n log n) worst case, O(n log k) in the usual case or with periodic compaction, and O(n) space for stale entries.
The lead applied both wordings to the part file, the answer agent's headings, the Wave A prompt sources (`draft.py` and `qs.py`; edit `draft.py` and regenerate, not `qs.py`) and the question_index rows.

## Prompt notes handled in the answers (frozen prompts otherwise unchanged)
- Q45: for an empty `s`, `''` is the valid answer, so `''` does not always mean "impossible" (the exhaustive check returns `''` exactly when no arrangement exists over every multiset up to length 7 over `abc` and 5 over `abcd`: 1,380 cases, 704 infeasible).
- Q21: "sorting by x_start fails" holds only for the naive version that does not shrink the group end; start-sorted with a min-end shrink also works; the naive version is wrong on 332 of 3,875 small multisets. Q32: neither wrong rule fails on 1 or 2 activities and both fail on 3; shortest-first has exactly one failing 3-set, {[0,3],[2,4],[3,6]}, and its counter-example needs tied lengths. Q30: a `(-len, w)` tuple cannot give descending alphabetical order; a negated-code-point tuple with a sentinel does, and without the sentinel it fails on prefixes like "ab"/"abc". Q10: `heapq.merge` returns an iterator (a generator in CPython). Q40: Fibonacci frequencies push code depth to n - 1 (31 at n = 32), so a recursive depth walk is avoided.

## Exhaustive and large checks that held (observed)
Task scheduler formula against a heap simulation and BFS on 476 combinations (Q11); jump game on 19,530 and 13,635 lists (Q12, Q13); gas station on 69,904 circuits with 30,940 having several valid starts, so the greedy returns the smallest valid start (Q14); reorganise feasibility `max_count <= (len+1)//2` exact on 3,279 strings (Q15); finest partition unique on 9,840 + 21,844 strings (Q22); queue reconstruction unique on 31,174 height sequences (Q23); bottom-up build-heap swaps at most n - popcount(n) over every permutation up to n = 8, and CPython's `heapify` layout differs from the textbook layout on 445 of 2,000 seeded lists while both are valid heaps (Q28); the coin-system bound c[-1]+c[-2] on all 2,048 systems with largest coin up to 12 (Q33); `nlargest` equals `sorted(reverse=True)[:k]` on 2,369 tie-heavy cases (Q37); Huffman lengths valid under the Kraft sum and optimal for n up to 7 (Q40); forgetting the room number as tie-break fails at n = 2 (Q42); cheapest-capital-first is wrong with a counter-example (Q44). Heap tie-breaking is demonstrated wherever a heap is used (TypeError on tied unorderable payloads; silent wrong order with `(priority, id)` in Q29; counter fix).

## Not run
No timings anywhere. Q40 and Q45 claims were checked on small inputs, not exhaustively across all inputs; max-size runs are included (Q40 at n = 10^5, Q43 at k = 3,500 with N = 10^5).

## Evidence limits
No company-reported problems verified; sources are heap, interval and greedy pattern guides, the heapq docs recipe, three Naukri Code360 candidate reports and the Kozen-Zaks coin papers, all as snippets (docs.python.org failed with ENOTFOUND; 6 searches). See research_notes/Book5_Part08_sources.md.
