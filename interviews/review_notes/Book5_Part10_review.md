# Book 5 Part 10 review (Wave C)

Date: 2026-10-29. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (DSA in Python: dynamic programming I, 1D DP and knapsack). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. All four were stopped once by a spend limit and resumed with SendMessage; their saved per-question files let them continue. Wave A rendered all 177 examples from the same data the checker runs and cross-checked each reference solution against a brute-force or plain-recursion oracle on 400 seeded inputs per question (15,612 checks); recursion-limit claims were tested at the quoted sizes (the 3-step stair recursion passes at n = 500 and fails at 1000, 1500 and 2000, so prompts use only n <= 500 or n >= 2000).

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 13 / 17 / 10 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 40 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 40 of 40 exit 0 |
| Cross-references (Part 4 Q35, Part 5 Q11, Part 7 Q35 and Q45, Part 8 Q12, Q13, Q18, Q33) | verified by Wave A's build.py (also within-part references) |

## Correction made during review (frozen prompt)
Q31 (the `[[0]*n]*m` aliasing trap) said that a DP table filled row by row on the aliased table "is silently wrong". The Q31-40 agent showed that is not always true: unique paths with right/down moves on `[[0]*n]*m` gives the right answer (6 for 3x3), because the single shared row acts like a rolling array; it breaks once a cell reads another row such as `dp[r-1][c-1]` (a diagonal-move grid gives 17 instead of 13). The prompt now says the aliased table gives wrong answers whenever a cell reads a value from a row it did not just write, and that a table reading only the cell above and the cell to the left can look right by accident. The lead applied the same wording to the part file, the agent's heading, the Wave A prompt sources (`draft.py`, `qs.py`) and the question_index rows.

## Prompt notes handled in the answers (frozen prompts otherwise unchanged)
- Q15's line about not taking the modulus of the inputs in a comparison is vague; the answer reads it as "never order or compare reduced values" and says so. Q13's memo trap: a memoised version that fills the cache in ascending index order never goes deep, so the answer's memo version asks for the last index first.
- Q21: the memoised ordered count fails at the default limit even at target 500 (largest working target here was 498) because `sum(generator)` costs two frames per level; sandbox-specific. Q28: the top-down memo overflows or not depending on inner-loop order (`j` ascending succeeds on the increasing list 0..1999, descending raises RecursionError). Q7 fails on an increasing list of 1500; Q8 and Q9 depth is at most n so memoisation works at the stated sizes and fails only outside them; Q10: amount-5000 recursion fails while the by-index recursion works at amount 300.
- Q33: with the default limit n 0..500 are 'ok' and 1000, 1500, 2000, 5000, 10^5 raise RecursionError (largest working n 997); raising `sys.setrecursionlimit(10**6)` with `@cache` on Python 3.13.17 still raised at n = 5000 although n = 3000 passed and a plain dict-memo recursion went deeper, recorded as an observation, not a rule; the remark that other builds can segfault is general knowledge, not tested. Q32: `cache_info()` must be read before `cache_clear()`; misses equal `currsize`.
- Q22: updating only on a strictly greater sum is also right on all 19,530 lists, so the "equal sum, smaller l" check is not needed (proof in the text); Q34: the patience method with predecessor pointers returns a valid LIS but its index list differs from the lexicographic tie-rule answer on 368 of 600 random lists (first example gives `[2,3,7,18]` where the rule gives `[2,5,7,101]`); Q23: a parent pointer built with coins in input order differs from the tie rule on 38 of 2,000, ascending coins never differs.

## Findings kept in the text (observed)
ways(n) is Fibonacci(n+1) for n = 0..299 (Q1); greedy coin change wrong on 231 of 1,905 small sets and amounts (Q6); `tails` is not a subsequence of the input in 441 of 2,000 lists (Q7); the 50-ones decoding example gives 20,365,011,074 (Q9); swapped loop order differs from the combination count on 219 of 600 cases (Q10); no valid circular selection holds both house 0 and house n-1 (Q12); the answer is at most 4 and equals 4 exactly when n = 4^a(8b+7) for every n up to 10^4 (Q16); naive_calls = 2*fib(n+1) - 1 and memo_calls = 2n - 1 (Q14); restarting when the running sum is <= 0 is wrong on 4,503 of 19,530 lists (Q22); the naive Kadane formula is wrong on 363 of 19,607 lists, all all-negative (Q26); `k >= n // 2` equals unlimited transactions on all 21,845 lists and is tight at `[0,1,0,1]` (Q29); `bisect_left` for the non-decreasing variant is wrong on 284 of 600 lists (Q35); the ascending height tie-break is wrong on `[[4,5],[4,6],[6,7],[2,3],[1,1]]` (gives 5, correct 4) and on 282 of 600 random cases (Q40); at n = k = 30 the dice count has 43 digits so the modulus matters (Q36).

## Not run
No timings. Q39 (ones and zeroes) is the concept edge toward Part 11 and is kept to what the prompt states.

## Evidence limits
No company-reported problems verified; 8 questions carry the Flipkart candidate-report tag (self-reported, unverified); every WebFetch failed (4 searches, snippets only). See research_notes/Book5_Part10_sources.md.
