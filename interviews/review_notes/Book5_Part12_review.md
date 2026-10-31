# Book 5 Part 12 review (Wave C)

Date: 2026-10-29. Reviewer: lead session (independent of the four answer agents). Scope: 35 questions, Q1-Q35 (DSA in Python: backtracking, tries, bit manipulation, DS-flavoured items). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-9, Q10-18, Q19-27, Q28-35; merged by heading: 35 of 35 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A compared all 142 examples with independent oracles and required every enumeration prompt to state its output order and duplicate treatment; each answer agent re-ran the examples and tested every stated claim on small inputs. No frozen prompt needed correcting this part.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q35; star order and counts 11 / 15 / 9 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 35 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 35 of 35 exit 0 |
| Cross-references (Part 1 Q8, Q15, Q34, Q35, Q36, Q42, Q47; Part 3 Q2, Q36; Part 6 Q30; Part 7 Q41; Part 9 Q13; Part 10 Q10; Part 11 Q19; within-part Q references) | verified by Wave A's build.py |

## Overlap decisions
Part 1 already owns the randomised set (Q35, Q47) and the Bloom filter (Q42), so Part 12 has no question on them; Part 1 Q8 owns the single missing number, so Q15 here is the repeated-and-missing XOR task; LRU is only referenced to Part 6 Q30; Q34 is a minimal skip list and Q33 trie memory versus a dict of sets and 26-slot arrays, both concept level. Q32 is the only question requiring an iterative solution.

## Findings kept in the text (observed on Python 3.13.17)
- Backtracking cost, measured as calls: n-queens n = 9 takes 8,394 calls against 986,410 (columns only) and 435,848,050 (unpruned), counts 1, 0, 0, 2, 10, 4, 40, 92, 352 for n = 1..9 (Q10); subsets, permutations (unpruned n = 6: 55,987 calls against 1,957; Q6), Catalan prefixes (n = 8: 6,917 against 131,071; Q7); combination sum `[3,4,5]` target 12 takes 17 calls with break, 28 without, 70 with no start index (Q8); word search 6x6 all-'A' against `'A'*11+'B'` makes 1,069,612 calls under the 36*3^11 bound and forgetting the undo is wrong on 95 of 2,000 boards (Q9); permutations of `[1,1,1,2,2,3]`: 1,957 calls with no rule, 517 with `used[i-1]`, 189 with the tight rule (Q19); k-combinations n = 20, k = 19: 210 calls against 1,048,575 (Q20); the skip rule cuts calls from 14,920 to 48 and `j > 0` instead of `j > start` loses `[1,1,2]` for target 4 (Q21); sudoku 17-given puzzle: 17,918 calls with the heuristic while reading order did not finish within a 3,000,000-call cap (Q25); the `used[i-1]` variant is correct but slower, and `i > 0` instead of `i > start` is wrong on 178 of 300 inputs for subsets with duplicates (Q18).
- Bit manipulation on Python 3.13: unmasked carry loop never ends for -1 and 1; a `while n:` loop never ends on a negative n because `-1 >> 1` is -1; single-number-II without the sign fix returns 4,294,967,288 for -8; `~m` is negative so candidates use `~(...) & 0x3FE`; 32-bit masking is the question's rule, not the language (Q17, Q25, Q26, Q28, Q29); the masked adder matches a 32-bit ripple-carry adder on 20,000 random pairs and takes at most 32 rounds (-3+3 takes 32); `x & -x` is the lowest set bit for every nonzero x in [-2,000, 2,000] (Q16); `& 0x55555555` is correct only within the stated range, `bit_length` parity is range-free (Q12); the XOR swap on the same slot zeroes it (Q15); submask enumeration visits each submask once in decreasing order and pair count is 3^n - 2^n (Q30).
- Tries: trie visits 13 against 104 calls for one search per word on the first example and deleting exhausted branches gave 516 versus 36,796 visits (Q11, different units stated); trie nodes <= pairs, equality exactly when first letters all differ (Q33); in the sandbox the plain set was smaller than the trie by `sys.getsizeof` (sandbox figures); lowering a count in a trie needs a rebuild from children (Q24); adding `val` instead of the delta gives 10 where 7 is right (Q27).
- Q31: "B never makes more calls than A" holds exhaustively (5,376 cases) with a short proof; skip list: results identical across 6 seeds and forced levels, about 11 average steps per lookup with random levels against about 1,000 with all level 1 on 2,000 sorted keys (illustration only; Q34); Q35: the call counts with and without the leading-zero rule, and `'05'` with target 5 does have the answer `0+5`.
- Recursion: a 1x1500 row with a 1,500-letter word raises RecursionError and 300 works; a 49x40 serpentine corridor with 1,024 path cells also fails recursively; with the limit set to 5,000 the 1,500 case works here (observation about this machine only). A 43x43 winding corridor (967 cells) still ran recursively, so the prompt names the 1x1500 row as the failing case.

## Not run / hedged
`int.bit_count` needing Python 3.10 or later is editor knowledge, not checked (Q2, Q12 mentions). Memory figures (Q3: about 1.56 MB dicts against 2.04 MB lists for 1,000 random 8-letter words; Q33) and timings (Q26) are sandbox-only. Counts are measured calls or visits, not big-O proofs. Q7's "random cross-check" only repeats small n because its oracle is exhaustive for n <= 6 (the answer says so); Q9's call counts include rejected attempts, so the comparison is conservative; the Q28-35 agent only skimmed its assembled answers.md (label-count check), which the lead's full structure check and re-run covered.

## Evidence limits
No company-reported problems found; every WebFetch failed (3 searches, snippets only); Part 13 and Part 14 are named without question numbers because they were not built when this part was frozen. See research_notes/Book5_Part12_sources.md.
