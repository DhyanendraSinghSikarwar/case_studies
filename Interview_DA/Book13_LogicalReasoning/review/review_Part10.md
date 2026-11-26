# Review, Book 13 Part 10 (quantitative-logic puzzles), Wave C

## Counts
- Answers checked: 54. Questions independently re-solved by code from the question text before reading the written answer: 52 (Q8 and Q9 are method questions; their numeric example was re-checked by hand).
- Final answers wrong: 0. Non-unique or ambiguous: 1 (Q36, reading). Answers changed: 0. Text fixes: 8 (table below).
- Scratch scripts: /tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/C13_Part10/ (a.py, b.py, c.py, d.py, q49.py).

## Independent results (all match the stated answers)
Q1 4; Q2 5; Q3 5; Q4 day 18; Q5 48; Q6 10; Q7 4; Q10 4; Q11 10 GB; Q12 36 (only solution); Q13 80 (union 135); Q14 40; Q15 10; Q16 200; Q17 18; Q18 8; Q19 11 (follow-ups 12 and 21 re-run); Q20 31; Q21 37; Q22 2^30 larger; Q23 25 (Rule of 72 gives 24); Q24 22; Q25 1892 (only x = 44); Q26 7; Q27 90; Q28 180; Q29 36; Q30 47; Q31 22; Q32 44; Q33 10 squares; Q34 1296; Q35 3 cuts, only split (1,2,4,8); Q37 4 weights, unique set (1,3,9,27) even with repeats allowed; Q38 bag 5; Q39 1001; Q41 equal (fractions 100/11, 150/53, 1000/1001 re-run); Q42 7 moves by BFS, exactly 1 shortest path; Q43 60; Q44 266; Q45 34; Q46 73 (64 gives 1, 1000 gives 977); Q47 6 (1-D stacked-cut BFS: lengths 2,3,4,5 need 1,2,2,3); Q48 bottles 1,4,5; Q50 10 and Q51 9; Q52 29 (17 and 16 for the follow-ups); Q53 APPLE = 10038, unique over all 6-letter assignments; Q54 (3,3,8), only sum 14 repeats, product-36 follow-up gives (2,2,9).
- Q49 (wording trap): a state search over (unknown-type, maybe-heavy, maybe-light) balls gives a maximum of 13 balls for 3 weighings when only the odd ball must be named, and 12 when its heavy/light type must also be stated. Also confirmed: 4 for 2 weighings (5 fails), 40 for 4 weighings (41 fails), 14 with one spare genuine ball (15 fails), and 14 balls fail. The written 13-ball plan was simulated for all 26 cases and always names the right ball. Answer 13 is correct and the classic 12 is correctly explained.
- Q50/Q51 lower bounds: exhaustive minimax over partial orders gives 1,3,4,6,7 (max and min) and 1,3,4,6,7 (second largest) for n = 2 to 6, matching the formulas; n = 8 (10 and 9) rests on the known general results, as the answers already say.

## Fixes made
| Q | Problem | Fix |
|---|---|---|
| Q36 | "Closed chain" is ambiguous. The written solution (open link 3, pieces 2, 1, 4) only works for a straight chain with loose ends. For a closed ring one opened link cannot pay all 7 days (minimum is 2). | Answer now states the reading (straight chain) and the ring result (2 links, checked by script); step 1 and the Check line updated. |
| Q36 | 15-link follow-up listed pieces "2, 3, 8, 1, 1" without saying which is which. | Now "open links 3 and 7: pieces 2, 1, 3, 1, 8" and labelled straight chain (verified). |
| Q23 | Simple-interest trap said "8 x 100/9, about 78", which does not equal 78. | Now 700 / 9 = about 78 (the extra must be 700%). |
| Q41 | "brings back 10/11 of milk" read as a fraction of all the milk. | Now "10/11 of a unit of milk (the mixture is 1/11 milk)". |
| Q47 | Claimed diagonal cuts "do not help" without proof. | Reworded as an assumption: flat cuts parallel to the faces. |
| Q52 | Check line claimed "8 different ways" to reach 29; not verified. | Replaced by "no schedule beats 29 (optimal schedules not counted)". |
| Q53 | Follow-up said the thousands digit is "0 or 1" for a sum under 11,000. | Now: the sum is at most 10,998, so P must be 0. |
| Q22 | "The crossover is at 13!" was vague. | Now "13! is larger, even though 12! is still smaller than 2^30". |

## Flags (report only)
- Near-variants of Book 6 Part 7 items, none a copy (numbers or sizes differ): Q40 (B6 Q74 45-minute ropes; this asks 90, and its follow-up repeats the 45-minute solution), Q52 (B6 Q77 four-person bridge 1,2,5,10; this has five people and its follow-up reuses the four-person case), Q49 (B6 Q80 the 12-ball puzzle; this asks the largest count, answer 13), Q1 (B6 Q63 8 balls, one heavier), Q42 (B6 Q62 5/3 jugs), Q7/Q12 (B6 Q67 age ratio items). Consider whether the overlap in Q40 and Q52 follow-ups is wanted.
- Q54 with product 36 is the classic version; the main question uses product 72 as stated.
- Q19 follow-up 2 (sum 21 from 1 to 30) is hand-reasoned in the text; my graph count agrees (21).
- Numbering: 54 questions against Target 50 is stated in the header; ordering and stars were not changed.

## Left unverified
- All "Asked at" lines say "commonly asked (no company-specific report found)" and prep-site claims are labelled unverified; I did not check them against sources.
- Q47 lower bound (cuts in different directions cannot share) is a hand argument, as the answer says.
- Q50/Q51 for n = 8 lower bounds are cited as known results, not searched here.
- No em or en dashes remain outside the title line; code fences balanced.
