# Review: Book 13 Part 2 (Deductive Logic and Conditional Reasoning)

Reviewer: Wave C. File: Book13_LogicalReasoning/Book13_Part02.md. Scratch scripts: scratchpad/C13_Part02 (syl.py, more.py, rest.py).

## Counts
- Answers checked: 73 (Q1-Q73).
- Independently re-solved by code or hand enumeration before reading the written answer: 73. Code: all 20 syllogism or possibility items (Q1, 2, 11-15, 24, 36-42, 58-61, 71) by enumerating every region-occupancy model with every group non-empty; Q16, Q25, Q26 model counts; Q29 worked example (5 groups, small-model search); Q43 (256 premise/figure/conclusion combinations); Q62, Q63 (all trios and their follow-ups); Q55, Q68, Q73 (set bounds by region enumeration). Conditional, table, fallacy and negation items (Q3-10, 17-23, 27-28, 30-35, 44-57, 64-67, 69-70, 72) re-derived by truth table or hand case-check (Q21, Q22, Q18 re-run on the tables and chains).
- Wrong conclusions or answers: 0. Non-unique answers: 0 (Q62 gives 2 selections, Q63 gives 5, both unique).
- Every "script-verified" model count in the answers was reproduced: Q15 36, Q36 24/8/20, Q37 312/224/120, Q38 10/2/8, Q39 40/32/32/40, Q40 32/16, Q41 30/26/24/20, Q42 24/16/0, Q58 736, Q59 96, Q60 8, Q61 96/64, Q71 312/224/192/120, Q16 160, Q25 8 and 4.
- Edits made: 11.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q26 | Check said "all 8 Venn models of two groups"; two groups have 4 regions, so 16 models. | Changed to 16 and explained 4 regions. |
| Q29 | "Say this" gave 15-18 s per conclusion; the Answer routine (20 s + 5 x 14 s = 90 s) uses 14 s. | Say-this now says about 14 seconds. |
| Q43 | The count line was labelled "Worked mini-example (numbers)" and the 256 was unexplained. | Relabelled Check; explained 4x4x4 x 4 conclusion types = 256 and 24 valid forms (re-run: 24, none with two negatives or two "some"). |
| Q6 | Claimed statement-conclusion questions "never" ask "possible"; Q42 and Q71 do. | Reworded to "most ask which follow; a few ask certain/possible/false". |
| Q7 | Reason for rejecting (d) was vague ("contradicts the original idea"). | Gave the concrete case (passed and renewed satisfies the original but breaks (d)). |
| Q53 | "standard 3-star topic in the sources" is an internal rating, not a company claim. | Replaced by "standard syllogism variant on prep sites (unverified)". |
| Q21, Q22, Q26, Q27, Q28, Q65 | No blank line after a table. | Blank lines added. |
| Q65, Q66, Q67 | No Check line. | Added short Check lines (Q67 states examples are invented). |

## Checked and left as is
- Conventions (some = at least one, every named group non-empty) are stated and applied consistently. Q25 and Q60 follow-up correctly show what changes if empty groups are allowed.
- Either-or items Q13 and Q38 correct: (c) in both (contradictory pairs, 0 models where neither holds). Q14, Q15, Q17 either-or remarks correct and appropriately qualified.
- Q55 text has an unused parenthesis ("most" means more than half); the question line may not be changed, the answer (exactly 2, both bounds equal) is right, and its follow-up (2 to 8 if some use neither) was re-run.
- No em or en dashes in answer text (only the part-title line). Code fences: none, balanced.
- "Asked at" lines claim only what research/Book13_Part02_sources.md supports (TCS NQT, Infosys, Wipro, Mu Sigma, all prep-site claims, labelled unverified); the source file itself notes Cognizant evidence conflicts and Part 2 does not cite Cognizant. Timings in Q29 are labelled "our suggestion".

## Overlap with Book 6 Part 7 (report only, no near copies found)
Same templates but different wording, names and statements: Q12 vs B6 Q25 and Q61 (all/no chains); Q40 vs B6 Q8 and Q55 (some + all); Q37 vs B6 Q24 (some + all + no); Q23 and Q53 vs B6 Q45 ("only"); Q58-Q61 vs B6 Q70 (long chains). None is a near copy; the Part 2 versions add the possible/follows and counter-model reasoning that Book 6 lacks. Q56 and Q44 (affirming the consequent / denying the antecedent) overlap Q32, Q47, Q49, Q70 inside this part (same fallacy, different scenarios); consider trimming one if the part must shrink.

## Unresolved / unverified
- Ordering: stars are not strictly descending in the order of files (the 3-star block ends Q23, then 2-star Q24 onward, 1-star from Q64), which is consistent; no change needed.
- Fallacy names (Q31-35, Q64, Q67, Q69) are checked against textbook definitions only, not by code.
- Prep-site claims on exam formats (Q29: 2 syllogisms in a 20-question, 25-minute TCS NQT section) are reported, unverified, and not checkable here.
