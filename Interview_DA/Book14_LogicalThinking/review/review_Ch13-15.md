# Review Ch13-15 (Book 14), reviewer scratch id Ch13-15

Scratch code: /tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C14_Ch13-15 (c13.py, c14.py, c15.py).

## Counts
| Chapter | Practice (index) | Re-solved by code | Wrong answers | Items changed |
|---|---|---|---|---|
| 13 Direction and distance | 30 / 30 | 30 simulated or checked by code (turn/walk simulator, bearings, arithmetic) | 0 | 3 (overlap rewrites) |
| 14 Blood relations | 40 / 40 | Q15, Q35, Q37 by code (Q35 exhaustive search n=1..6); the other chain items by hand-built tree reasoning (no code for relation words) | 0 | 4 |
| 15 Ranking and ordering | 30 / 30 | 30 / 30 (all permutation, scoring, tie and tournament puzzles brute-forced; rank arithmetic recomputed) | 0 | 1 |
Solved examples, scenario numbers and self-checks in all three chapters recomputed: all correct. Template check: all sections present, 5 examples, 2 scenarios, 3 self-checks, 5-line recaps, no answers in chapter files, no em/en dashes, fences balanced, Book 13 Part 6 and Part 3 cross-references exist and cover the topics.

## Fixes
| Ch | Item | Problem | Fix |
|---|---|---|---|
| 13 | Q5 | Near copy of Book 6 Part 7 Q16 (N, right, right, back) | New route: 18 S, left 5, left 6; answer 13 km south-east, walked 29; key rewritten |
| 13 | Q1 | 9-12-15 east/north identical to Book 13 Part 6 Q5/Q23 numbers | Now 24 E, 10 N, 26 km north-east; key updated |
| 13 | Q18 | Same start (south-west) and turn pattern as Book 13 Part 6 Q29 | Start north-west; answer now south-east (key recomputed) |
| 14 | Concept table | Column "Tells you the gender?" answered "No" next to gendered words (confusing) | Column reworded |
| 14 | Rules list | Marriage between a man and a woman was never stated, but Q34, Q38, Q39 rely on it | Rule added to chapter and to key conventions |
| 14 | Ex 3 | Awkward answer wording ("often called a maternal uncle's wife") | Reworded |
| 14 | Scenario 1 | Claimed "wife's" implies a male speaker (not valid) | Sentence replaced |
| 14 | Q13 | "Three" brother-in-law types: third (wife's sister's husband) is not in the chapter's table and is only a casual usage | Question now asks for two (wife's side and sister's side); key notes the casual usage |
| 14 | Q16 key | "cousin-in-law" is not a standard term | Qualified in key |
| 14 | Q21 | Same symbol structure as Book 13 Part 6 worked example (A + B x C / D: mother, sister, father) | New code (husband, brother, daughter), two-part question; key rewritten |
| 15 | Q16 | Same structure as Book 13 Part 3 Q20 (bottom rank, step up, step up) | Restructured (Jai 22nd from bottom, Ira 7 above, Kavi 9 below Ira); answer 26th from top; key rewritten |

## Overlaps
- Fixed above (Ch13 Q1, Q5, Q18; Ch14 Q21; Ch15 Q16).
- Left, different numbers/context but same genre: Ch14 Q35 (minimum-size group, adds aunt and niece) vs Book 13 Part 6 Q3; Ch14 Q37 (sons/daughters counting, different clues, answer 5 and 4) vs Book 13 Part 6 Q16; Ch14 Q7/Q18/Q36 use the "only ... collapses to a known person" device also used in Book 6 Part 7 Q4 and Book 13 Part 6 Q14; Ch14 Q32 (daughter, brother, father) vs Book 13 Part 6 Q20 (sister, mother, father); Ch13 Q20 (two walkers, how far apart) vs Book 13 Part 6 Q23; Ch15 Q7, Q9, Q17 (competition vs dense ranking) vs Book 13 Part 3 Q21. Teaching-level similarity; wording and data are new.
- Duplicates inside Book 14: none found in these chapters (names such as Uday, Vera, Ravi recur across Ch15 questions only as labels).

## Unresolved / notes
- Ch14 relation-word answers (Q1-Q34) were not run through a kinship program; they were checked by hand with explicit tree reasoning and the convention rules, plus code for the counting and search items. Q38/Q39 uniqueness argued by hand (generation counts), not by a fresh search; the key's claim of an earlier exhaustive search is the writer's.
- Ch14 Q27 calls the top person "great-grandfather" relative to the youngest generation; left as is.
- Ch13 Q25 (clock laid flat) is a mixed topic; kept (correct: hands south and south-east, 45 degrees).

## Unverified claims
None added. Chapters contain no external names, studies or statistics; scenarios are labelled illustrative. Spreadsheet pointers contain no formulas.
