# Review: Chapters 34, 35, 37 (Book 14)

Judged against the adapted layouts (Ch35: 2 worked examples, 10 cases x 5 sub-questions, no self-check; Ch37: template chapter, 15 classification exercises, 3 self-check questions, 5 examples, 2 scenarios).

## Counts
| Chapter | Re-solved by code / total | Items wrong | Items changed |
|---|---|---|---|
| Ch34 | 15/15 practice, 5/5 examples, 2/2 scenarios, 3/3 self-check | 0 | 0 (labels only, see fixes) |
| Ch35 | 50/50 sub-questions (10 cases), 2/2 worked examples | 0 | 0 |
| Ch37 | 15/15 exercises, 5/5 examples, Scenario 1 tally, 3/3 self-check | 0 numeric errors | 1 (Q5 ambiguity) |

Code covered: Venn regions and inclusion-exclusion (Ch34 Q8, Ch35 Case 2), all 24 height orders (Ch34 Q13), all 720 task orders (Ch35 Case 3: 6 valid), the checkout algorithm run on every cart plus 20,000 random positive-price reorders (no order dependence), the 16-row truth table (Case 9: 5 eligible), Simpson rates, fraud table, packer arithmetic, review averages, Ch37 arithmetic (36, 336, 1,184.76, 9/108, median 15).

## Fixes
| Chapter | Item | Problem | Fix |
|---|---|---|---|
| Ch34 | Catalogue of bugs / key Q10 | Key used "wrong direction" for Q10, a bug type missing from the catalogue | Added a "Wrong direction" row to the catalogue; key wording aligned |
| Ch34 key | Q8 | Bug label "double counting setup / forgetting a group" was muddled (nothing is counted twice; a group was left out of the sum) | Relabelled "arithmetic slip (the both group was left out of the sum)" |
| Ch37 | Q5 (and key) | Learner's list "12 and 21" hides a silent assumption (digits differ), so the decision order (rule 6 before rule 8) would give "wrong assumption", contradicting the key's "skipped case" | Wrong solution changed to "11, 12 and 21, so 3 codes" (only 22 missing, no assumption); key rewritten with the same type, root cause and a corrected "why not" line |
| Ch37 | Taxonomy table | "Chapters 21 to 26" for fallacies; fallacies, causation, biases and claims are Chapters 23 to 26 | Changed to 23 to 26 |
| Ch37 | Recap line 3 | "tried too fast" differed from the type name "Tried to be too fast" | Made consistent |

## Checks passed
- Concept correctness: converse/contrapositive and vacuous truth (Ch35 C1), Simpson's paradox, base rate, percentage points versus relative change, selection bias, inclusive counting all stated correctly.
- Template: Ch34 has 3 self-check, 5 examples, 2 scenarios, 15 Qs (5 easy, 5 medium, 5 hard, tagged, no answers in chapter), 5 mistakes, 5-line recap, key complete. Ch35 has 2 worked examples, 10 cases with 5 sub-questions each, 5 mistakes, 5-line recap, key complete. Ch37 has template, 5 filled rows, spreadsheet formulas labelled "from memory, not run here", key complete.
- Honesty: all numbers labelled illustrative or invented; no real people, firms or statistics; the weekly/monthly schedule is labelled "our suggestion, not research".
- Style: no em or en dashes; Ch37 code fences balanced (2); no table lacks a following blank line.

## Overlaps
- Greps of Book13 Parts 1-12 and Book06 Part 07 for the topics and distinctive numbers (98,000; 250,000; fraud 95%/5%; free shipping; fence posts; Pune sample) found no copied or lightly reworded items. Book13 Part 08 covers truncated axes, Simpson's paradox and average of averages as interview questions with different scenarios and numbers.
- Within Book 14: expected topic repeats only (Ch34 Ex 4 and Q6 and Ch37 Q6 all use average of averages with different numbers; Ch34 Ex 3/Q7 converse error and Ch35 C1/C10 reuse the idea by design as mixed cases).

## Unresolved / notes
- Ch37 and Appendix E point to Chapter 36 (timed practice sets), but `Ch36.md` does not exist yet in the folder (not in my scope); the cross-reference is correct once it is written.
- Word counts: Ch34 2,314, Ch35 3,195, Ch37 3,818 (inside the 2,000 to 4,500 range).
- Ch37 Q6 label (wrong assumption versus average of averages in Ch34's catalogue) is a defensible choice under the decision order; left as is.
- Nothing in these chapters rests on unverified outside facts; the Excel formulas in Ch37 were not run (labelled as such).
