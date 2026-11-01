# Book 5 Part 14 review (Wave C)

Date: 2026-10-29. Reviewer: lead session (independent of the five answer agents). Scope: 50 questions, Q1-Q50 (DSA in Python, Extra II: design problems, advanced graphs, segment/Fenwick trees, timed mock Sets A-D). No salary figures.

## Process
Five agents answered Q1-10, Q11-20, Q21-30, Q31-40, Q41-50; merged by heading: 50 of 50 merged, 0 skipped, 0 pending. No spend-limit stops.

## Checks (`scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q50; star order and counts 13 / 24 / 13 | pass |
| All 11 template labels in order; fences balanced; one python block per answer | pass for all 50 |
| Every python block re-run standalone with `python3 -I` | 50 of 50 exit 0 |
| Design answers: seeded random operation-sequence oracle, tie/eviction rules, per-operation complexity | present |
| Mock-set questions: scoring bullet and pacing sentence inside Follow-ups | present |

## Corrections to frozen prompts (found by answer agents)
Applied identically to the part file, agent heading, `qs.py`, `draft.py`, `question_index.md`, `index_rows.txt`:
- Q1: memory is bounded by 300 distinct seconds only if `hit` also expires old buckets (tested with 5000 hit-only seconds, 300 entries left).
- Q4: "plain dict is not enough" was loose: pop and re-insert emulates move-to-end; the cost is `next(iter(d))` scanning dead slots after many front deletions. Prompt now says "a poor fit".
- Q5: an unlink is two pointer assignments, a push-front is four.

## Findings kept in the text (Python 3.13.17)
- Q9: `copy.deepcopy` of a depth-5000 list raises RecursionError, so a harness that deep-copies `init` fails there; the iterator itself handles depth 5000.
- Q21/Q22/Q23/Q25 variants and Q36 `[-1, -1] -> 1` verified against brute force or exact oracles; iterative DFS/Tarjan/Kosaraju/union-find run at n = 10^5 without recursion; Q43 measured recursion depth 300 at L = R = 300.
- Q49 `remove(x)` outside 0..max_value returns False (prompt silent; stated in the answer).

## Not run / hedged
Thread safety is a stated concept only. Sandbox timings (Q4) are shown only as booleans. Editor knowledge is labelled as such. Every WebFetch failed (snippets only); see research_notes/Book5_Part14_sources.md.
