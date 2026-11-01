# Book 5 Part 11 review (Wave C)

Date: 2026-10-29. Reviewer: lead session (independent of the four answer agents). Scope: 35 questions, Q1-Q35 (DSA in Python: dynamic programming II, 2D grids, strings and intervals). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-9, Q10-18, Q19-27, Q28-35; merged by heading: 35 of 35 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A rendered all 158 examples from the same data the checker runs and ran 9,610 seeded cross-checks against independent oracles (brute force, plain recursion, `re.fullmatch`, a BFS over printer states, an instrumented `lru_cache` recursion, enumeration of paths, permutations and parenthesisations); every reconstruction tie rule was checked exhaustively on small inputs against an oracle using the same rule. Each answer agent re-ran the examples and oracles.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q35; star order and counts 9 / 15 / 11 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 35 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 35 of 35 exit 0 |
| Cross-references (Part 3 Q8, Q9, Q34, Q35, Q38; Part 9 Q40; Part 10 Q29, Q31; within-part Q6, Q7, Q8, Q17) | verified by Wave A's build.py |

## Prompt notes (no frozen prompt needed correcting this part)
Every example and stated claim held. Wave A fixed three things before freezing: Q26 (longest repeating subsequence) was restated as `p[k] != q[k]` for every k because the disjoint-index-set reading disagreed with the standard reading on "aaa"; Q24's prompt now relies on a winding corridor with zero-valued walls because a boustrophedon snake did not trigger RecursionError (a 61x61 corridor fails at the default limit, 21x21 works); Q7 was raised to len <= 2000 so its memoised recursion fails clearly. Q17 is a counting table `[matches, ways]` so it does not duplicate Part 3 Q38. Q31's prompt allows n <= 15 (the brief said 12 for bitmask questions) and runs in well under a second. Q28's modulus never bites at these limits (cost never exceeds 1,791); the answer says so and shows the damage with an artificial modulus. Q24: the corridor path length reported is the corridor cell count plus 1 because a wall cell of value 0 sits beside the start.

## Findings kept in the text (observed on Python 3.13, default recursion limit 1000)
- Recursion: memoised LCS-style recursions on disjoint strings fail from n = 520 (400 and 480 pass; Q6, Q8, Q10, Q16, Q18 raise at 1000); Q7 passes at 300 and 500 and raises at 2000; Q9 passes at 100, 300, 400 and raises at 1000; Q14 memoised 200x200 runs and 600x600 raises; Q15 300x300 runs and a disjoint 600+600 pair raises; Q19 passes at 300 and raises at 2000; Q21 passes at s=300/t=150 and raises at s=1000/t=500; Q22 passes at n=300 and fails at 1100 (outside stated sizes); Q26 passes at 200 and raises at 1000; Q29: 400x400 (depth 799) works and 600x600 (depth 1199) raises, and only depth causes it, not cache size or the 359-digit answer; every call at cell (i, j) sits at depth i + j + 1. Boundaries were not hunted.
- Wrong variants shown by running them: a descending inner loop in the one-row grid DP is wrong exactly when m >= 2 and n >= 3 (42 of 64 grids up to 8 x 8; Q1); skipping instead of zeroing a blocked cell is wrong on 210 of 682 grids (Q2); greedy fails on `[[1,3,1],[2,9,1]]` (13 vs optimal 6; Q3); the in-place triangle needs j descending, ascending fails on 34,638 of 59,805 triangles (Q4); dropping the up-left term is wrong on 98 of 512 3x3 matrices (Q5); the LCS back-pointer walk is not the smallest LCS on 49 of 500 pairs (Q10); an ascending inner loop in the one-row palindrome DP is wrong on 248 of 300 strings (Q12); a prefix-table parent walk differs from the suffix tie rule on 264 of 500 grids and greedy cheaper-neighbour is wrong on 184 of 500 4x4 grids (Q14); ascending inner loop for distinct subsequences gives 10 instead of 6 on `aaaa`/`aa` (93 of 300 fail; Q21); a first-burst split disagrees with the optimum on 236 of 300 lists (Q22); `<=` instead of `<` returns `((A0A1)A2)` on `[2,2,2,2]` and several optimal trees exist in 70 of 300 chains (Q23); the negative-index wrap-around bug is wrong on 118 of 600 matrices and a greedy walk on 100 (Q25).
- Claims verified: the forward "best sum so far" idea fails on `[[-3,-3,2],[-2,0,3]]` (health 7 vs optimum 6; 15 of 500 grids; Q20); `ways(a^n, k stars) == C(n+k-1, k-1)` (Q17); with lowercase letters a longer common subsequence can weigh less, so the weighted LCS is needed (Q18); a 2000x2000 table is about 32.1 MB as list of lists, 4.1 MB as bytearray rows, 2.1 MB as a triangle (Q19); `ways` mod 10^9+7 equals the exact value mod 10^9+7 (Q21, Q27); the 100x100 path count is a 59-digit integer matching `math.comb` (Q1).
- Q33's "first letter across a wider range" lemma is an exchange argument checked against the BFS, not proven. Q30's first-cut view is the time-reverse of last-burst; a last-cut view would not work.

## Not run
Timings are sandbox-only and appear only as pass/fail against a generous bound.

## Evidence limits
No company-reported problems verified; the only India-relevant angle is self-reported Flipkart snippets on four 2D-table palindrome and path questions; every WebFetch failed (3 searches, snippets only). See research_notes/Book5_Part11_sources.md.
