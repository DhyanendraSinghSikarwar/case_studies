# Review Ch10-12 (Book 14, Wave C)

Scope: Ch10 Tables and matrices, Ch11 Flowcharts and decision trees, Ch12 Syllogisms (chapter files and answer keys). Scratch: C14_Ch10-12.

## Counts (re-solved independently by code, before comparing with the keys)
| Chapter | Practice re-solved / total | Wrong answers | Items changed |
|---|---|---|---|
| Ch10 | 15 / 15 (11 grid puzzles brute-forced over all arrangements; Q4, Q8, Q12 and both scenario tables solved by exhaustive search) | 0 | 1 wording fix |
| Ch11 | 10 / 10 (each chart coded as a graph and run against a direct if/else rule on 5 to 180 inputs per chart, all traced paths reproduced) | 0 | 1 key note rewritten |
| Ch12 | 40 / 40 (Venn-region enumeration of every picture; numeric items Q12, Q23, Q34 by arithmetic) | 0 | 3 small fixes |

Also re-solved: all self-check questions (3 per chapter), all 15 solved examples, all 6 scenarios, the Ch12 shortcut table (10 rows, all correct), the Ch12 either-or and "extra statement" items (Q18, Q27, Q36) and the clash items (Q28, Q35, Q40). Ch10 grid puzzles: every one has exactly one solution and no clue is redundant (checked by dropping each clue), as the key claims. Q12 has 10 solutions without its extra clue and exactly 1 with it.
Template: 5 examples, 2 scenarios, 3 self-checks, mistake log of 5, recap of 5 in each chapter; practice counts 15 / 10 / 40 match the index; no answers in chapter files. Word counts: Ch10 3554, Ch11 4069, Ch12 4343.

## Fixes
| Chapter | Item | Problem | Fix |
|---|---|---|---|
| Ch10 | Scenario 1 | "better first fix" read as an effectiveness claim | Reworded as "our suggestion" |
| Ch11 key | Notes on verification | Input counts quoted (Q1 6, Q3 8, Q4 72, Q5 24) did not match what a rerun covers | Replaced with the counts I actually ran |
| Ch12 | Excel COUNTIFS snippet | Unlabelled, bare code fence | Fenced as text, labelled "from memory, not run here"; SQL snippet was run on a test table and gives 1 then 0 as stated |
| Ch12 key Q11 | Explanation of option (d) | Muddled: (d) is actually true under the chapter's convention, but weaker than (a) | Rewrote to say it is true but weaker, so not "exactly the same" |
| Ch12 key Q34 | Check line | Said smallest number of temps is 0, which contradicts the "every group has a member" convention | Removed the claim |

## Overlaps
- Grepped Book13 Parts 2, 3, 4, 5, 9 and Book06 Part07 for the Ch10 to Ch12 names, groups and scenarios: no copied or lightly reworded items found. Meera appears in a Book13 conditional-logic item only as a name.
- Within Book 14: no duplicate of Ch12 statements or the Ch10 puzzle casts found in other chapters (Ch10 itself reuses the same name pool across puzzles, with different clues and structure).

## Cross-references checked
Book 1 Part 2 (IF) and Part 4 (pivots), Book 2 Part 2 (GROUP BY) and Part 7 (CASE WHEN), Book 13 Part 2 (deduction), Part 5 (grids), Part 9 (flowchart tracing), Book 6 Part 7: all exist and cover the topic.

## Style
No em or en dashes; code fences balanced; blank line after every table (one apparent hit is inside a code block); no invented real names or statistics; numbers labelled illustrative.

## Unresolved / unverified
- None wrong. The key header claims in Ch10 and Ch12 ("brute force", "by computer") turned out true on rerun.
- Ch12 key picture counts (8, 32, 160, ...) match my enumeration for every item I compared; Q31 (2944 pictures) is not quoted in the key.
- Beginner-clarity judgment is mine only; chapters were left at current length (the Ch12 key is long, about 8,400 words, because every item lists pictures in full).
