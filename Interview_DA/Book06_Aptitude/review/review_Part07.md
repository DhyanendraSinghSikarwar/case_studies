# Review: Book06_Part07 (Logical reasoning), Wave C

**Counts:** answers checked 80; re-solved by code or enumeration 66 (all numeric, seating, ordering, calendar, clock, set-counting, syllogism, inequality, truth/liar, jug, bridge, egg, 12-ball items; concept and strategy items Q6, Q9 (checked), Q11, Q14, Q34, Q38 formula (checked), Q44, Q46 to Q48, Q56, Q71 read by hand); answers with a wrong answer or follow-up fixed: 3 (Q20, Q43 trap, Q72 follow-up); other text fixes: 9 more. All 80 final answers matched the written answers.

Scripts: scratchpad C06_Part07 (a.py, b.py, c.py). Syllogisms enumerated as all sets of present member types; puzzles by full permutation search.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| 20 | Follow-up "26 minus value of C" answered X (24); 26 - 3 = 23 = W | Corrected to W, noted X is the 27-rule mirror |
| 23 | Check said exactly one of 720 arrangements; code finds 6 (rotations of one ring) | Reworded: unique ring up to rotation |
| 33 | Same: said 1 of 5,040 (and 5,040 is the wrong count for 8 seats); code finds 8 rotations of 40,320 | Reworded |
| 39 | 100 years = 5 odd days only holds for the textbook century; 1901-2000 gives 6 | Added the assumption |
| 43 | Trap said Lata is third from bottom; the middle person is third from both ends | Trap rewritten |
| 62 | Follow-up for 1 litre said "emptying both"; vague gcd explanation | Exact 1-litre route (6 moves, BFS-confirmed); gcd wording fixed |
| 70 | "545 worlds, IV fails in 225" not reproducible | Replaced with enumerated counts: 36,864 worlds, I to III always true, IV false in 6,144 |
| 72 | Follow-up "We are both knights" said A is a knave; three combinations fit | Corrected |
| 73 | LED follow-up gave a nonsense workaround; assumptions unstated | Rewritten, assumption added |
| 79 | Check overclaimed ("elimination checked", minimality hand-waved) | Reworded honestly: standard result, not script-proven |
| 62,63,72 to 77,79,80 | "Asked at" said puzzle rounds at Mu Sigma, Fractal and Flipkart; interview_processes.md lists puzzles for Mu Sigma, Flipkart, Tiger, PhonePe, Novartis, not Fractal | Fractal removed, Tiger and PhonePe added, caveat kept |

## Verified with no change
Unique solutions confirmed by brute force: Q10, Q19, Q30, Q31, Q43, Q60 (and the Dev-variant follow-up gives 2 solutions), Q69 (B on Saturday). Syllogism verdicts confirmed by model enumeration: Q7, Q8, Q24 (incl. follow-up), Q25, Q55 (exactly one of I, II always true), Q61, Q70. Also Q54, Q52, Q64 (2037, 2052, 2038), Q66, Q67, Q68, Q75 (both variants), Q76 (2 arrangements), Q77 (17 and 18), Q78 (14; 3 eggs 9), Q80 (full 3-weighing plan simulated for all 24 cases, no failure), clock angles, Q49, Q53, Q65.

## Unresolved / left unverified
- Q79: minimality of 7 races not proved by code (standard result).
- All "prep-site" topic claims (Infosys, Accenture, TCS NQT, Wipro, Cognizant) remain unverified per the sources file; Q1 mentions TCS NQT blood relations, which the sources file supports only for seating.
- The sources file itself (Book06_Part07_sources.md) repeats the Fractal puzzle claim; not edited (out of scope).
- Q28 assumes full (not half) siblings; Q29 states its own assumption.

## Report-only
- Ordering: stars descend 3, 2, 1 as designed; Q71 (1 star) sits among puzzles, fine.
- Overlap: Q7/Q8/Q9/Q46 and Q38/Q51 (clock angle) and Q41-Q42/Q52/Q64 (calendar) repeat ideas inside the part; Q49/Q53/Q65 set counting may overlap with data parts elsewhere. Not edited.
- Style: only em dash is in the part-title line; no code fences; no pasted scripts.
