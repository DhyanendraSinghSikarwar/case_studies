# Book 5 Part 4 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (DSA in Python: stack, queue, monotonic stack). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A ran every prompt example (`scratch/B5P04_wavea/check_examples.py`) before freezing; each answer agent ran them again.

## Frozen-question correction made during review
Q17 (minimum removals to make parentheses valid) claimed "the set of dropped indices is unique, so the answer is unique". That is false: `'(a(b(c)d)'` and `'lee(t(c)o)de)'` each have 3 valid minimal answers, and an exhaustive run over strings on `a`, `(`, `)` up to length 8 found 2,615 of 9,841 with more than one valid minimal answer. Only the minimum number of deletions is unique. The lead corrected the prompt sentence identically in the part file, the answer agent's heading, the Wave A source (`qs.py`) and the question_index rows; the four prompt examples were unaffected (they are the stack algorithm's output and each is checked to be a valid minimal answer).

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 13 / 16 / 11 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 40 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 40 of 40 exit 0 |
| Cross-references (Part 2 Q14, Q16, Q43; Part 3 Q13) | verified by Wave A's build.py |

Each block holds the brute force or reference, the optimal solution, a seeded cross-check (500 to 4,000 cases) or an exhaustive check (all 335,923 strings up to length 7; all 8,191 strings up to length 12; all 4,096 3x4 matrices; 132,496 string pairs), and edge-case asserts.

## Findings kept in the text (observed on Python 3.13.17)
- `7 // -2` is -4, so RPN division needs a sign-aware truncation; `int(a/b)` breaks on a 10^17+1 case (Q6). `(-1) % 3` is 2 (Q36).
- `sys.getrecursionlimit()` is 1000: a recursive parser raises RecursionError at nesting depth 5000 (Q8, Q25) and a recursive-descent reference fails at 150,000-deep nesting (Q11) while the explicit-stack versions return; `sum(generator)` recursion uses two frames per level.
- `list.pop(0)` vs `deque.popleft`: 3.058 s vs 0.027 s at n=200,000 (Q4) and 0.731 s vs 0.006 s draining 100,000 items (Q30); labelled sandbox-only and variable. `deque(maxlen=2)` silently drops the old end; `queue.Full`/`queue.Empty` are raised; a forced check-then-act race on a deque gave one thread `IndexError`; `queue.Queue.shutdown()` exists on 3.13 (Q31).
- `posixpath.normpath('//a')` returns `'//a'`, not the canonical form the path question wants (Q9). Several answers include real bug demos (Q23 equal values, Q24, Q27, Q29 `[2,2,2]` gives 20 instead of 12, Q30 mark-on-dequeue).

## Not verified by running code
The `queue.Queue` internals (locking, blocking `get`, `maxsize`, `task_done`/`join`) are editor knowledge per the sources note; the Q8 worst case O(L·d) is reasoned, not measured; the Catalan counts for n=7 rely on the formula (brute force covers n up to 6, Q33).

## Evidence limits
No company-reported problems found beyond a few candidate-reported Amazon items for queue-via-stacks and stack-via-queues; every WebFetch failed, so sources are snippets (3 searches); the `queue` module docs were not found. See research_notes/Book5_Part04_sources.md.
