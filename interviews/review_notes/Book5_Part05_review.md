# Book 5 Part 5 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (DSA in Python: binary search, including binary search on the answer). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A ran every prompt example (`scratch/B5P05_wavea/check_examples.py`) and tested its uniqueness and tie claims exhaustively before freezing (the Part 4 lesson); each answer agent re-ran the examples.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 13 / 16 / 11 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 40 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 40 of 40 exit 0 |
| Cross-references (Part 1 Q28; Part 2 Q38, Q40; Part 3 Q36, Q40) | verified by Wave A's build.py |

Each block holds the brute force or reference, the optimal solution, a seeded cross-check or an exhaustive check, and edge-case asserts.

## Prompt notes (all handled in the answers; frozen prompts unchanged)
- The mountain-array question with the 100-call budget is Q23 in the part file (Wave A's report said Q22). The budget is enforced by a counting wrapper in code. The prompt's "about 3 * ceil(log2 n) calls" is loose: the peak-finding step costs 2 `get` calls per round, so the worst case is about 4 * ceil(log2 n) = 56 for n = 10^4; the measured maximum over all peak positions was 54, within the budget, and the answer says so.
- Q36 gives no value bound, so the answer states an assumption (values within +-10^4, 31 halvings) and uses a fixed 50 iterations. Q40: a sane epsilon (1e-6) terminates in 24 loops; only a too-small epsilon hangs, so a fixed iteration count buys guaranteed termination, not accuracy.
- Q30 guards a target equal to the 2147483647 sentinel, which would falsely match a past-the-end index (returns -1).

## Exhaustive and large checks that held (observed)
all 231,231 (arr, k, x) triples for k-closest with three tie-break formulations agreeing (Q24); every num 1..200,000 for integer square root against `math.isqrt` used only as a checking tool (Q14); every n up to 600 and every first-bad position within ceil(log2 n) calls, 29 calls at n = f = 10^9 (Q15); all 19,008 rotated lists with duplicates (Q17) and all 3,168 rotated lists for the minimum, where the distinct-values code is wrong on 147 (Q18); "at most k pieces" equals "exactly k pieces" on 6,372 inputs (Q13); exactly one value has count 1 in all 21,792 valid inputs (Q25); partitions checked exhaustively (Q8, Q20). Worst cases: all-ones rotated search takes n/2 loop steps (Q17), all-equal minimum takes n-1 (Q18). `[3,1]` target 1 breaks the `nums[lo] < nums[mid]` variant (Q5); an upper-biased mid never terminates on `[1,2,3,4,9]` with c=2 (Q20).

## Not run
Timings; complexity is reasoned in the text. Q3: 46340^2 = 2,147,395,600 <= 2^31-1 < 46341^2 so the cap holds.

## Evidence limits
No company-reported problems found beyond Flipkart entries on one aggregator (Allocate Books in 2021, rotated-array search); every WebFetch failed, so sources are snippets (4 searches). See research_notes/Book5_Part05_sources.md.
