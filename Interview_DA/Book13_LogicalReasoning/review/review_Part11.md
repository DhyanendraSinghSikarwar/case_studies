# Review: Book 13 Part 11 (timed mixed mock sets)

Script: scratchpad/C13_Part11/s.py (itertools, sqlite3, datetime, fractions).

## Counts
- Answers checked: 40. Independently re-solved by code from the question text: 40 (Q7, Q19, Q30, Q40 strategy parts judged by hand; their arithmetic by code).
- Final answers wrong: 0. Answers non-unique: 0 (Q12, Q13, Q14, Q20, Q22, Q23, Q35 each have exactly one solution by enumeration).
- Answers changed: 0. Supporting text/follow-ups fixed: 8 items below, plus labels.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Scope | Set 3 and Set 4 minutes did not match heading times (sums 16.75 and 13.5 min); strategies unlabelled | now "about 17" and "about 14"; added "our suggestion" label |
| Q4 | Direction ambiguous; wrong reason against (d) nephew; follow-up 2 sentence did not match the question; "daughter" assumed for Tara | answer states its reading (what Naveen is to Tara; opposite reading gives "cousin's child", not an option); (d) and (a) reasons corrected; follow-up rewritten; Tara's gender left open |
| Q8 | "guess any option" though no options exist | reworded |
| Q11 | Follow-up said 4 of 8 combos allowed after a signature; code gives 3 | corrected to 3 |
| Q25 | Follow-up: right turn from west gave east; correct is north: (-9, 20), sqrt(481) = 21.9 km, north-west | corrected |
| Q36 | Mistake line said 5 vs 5 needs 4 weighings; code shows 3 | replaced with the real error (two-outcome thinking, log base 2 gives about 4) |
| Q1, Q5 | "Asked at" named TCS (not in the sources file) | now only Mu Sigma topic lists, "reported, unverified" |
| Q7, Q28 | No "Check" line | added (judgement rule; invented numbers) |
| Q29, Q35 | "Asked at" lacked "unverified" | added |
| 38 answers | "If you are short of time" not labelled | "(our suggestion)" added (Q12, Q13 already labelled) |

## Verified by code (claims confirmed)
Q1 312 models, I false in 88; Q2 140 cases, III true in 105, M>Q 70; Q21 576 models; Q31 40 models, exactly one of I and II true in each; Q22 unique, and 2 solutions without the Dina-not-Pune clue; Q23 unique (ABEDC), 2 without "C after D"; Q24 sorted after Step 3, Step 4 no change; Q20 only 4,3,2,1,0; Q17 and Q37 sqlite outputs; Q8 dates; Q13 variant (C opposite E); Q14 variants; all arithmetic items.

## Template and style
- All 40 carry "Target time" and "If you are short of time". No em or en dashes in answers (one in the part title). Code fences balanced.
- Q29 to Q40 order the header lines differently from Q1 to Q28 (Target time after Answer); left as is.

## Overlap
Not checked in detail against Book 6 Part 7 (its file was not opened); the sources file and dedupe log say no duplicates. Standard types (syllogism, inequality chain, blood relation, direction) may resemble Book 6 items in type only.

## Unresolved / unverified
- Excel blank-cell behaviour (Q27) and other-database NULL behaviour (Q17, Q37): "from memory, unverified", unchanged.
- Mu Sigma topic claims and all time strategies: prep-site level, unverified.
- Q5 and Q34: no second defensible rule found by simple checks.
