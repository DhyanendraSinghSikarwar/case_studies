# Review Ch01-03 (Book 14, Chapters 1 to 3)

## Counts
| Ch | Practice re-solved / total | Self-checks | Examples + scenarios | Items wrong or changed |
|---|---|---|---|---|
| 1 | 15 / 15 (index 15) | 3/3 | 5 + 2 | 0 wrong; 1 cross-ref added |
| 2 | 30 / 30 (index 30) | 3/3 | 5 + 2 | 0 wrong; Q29 replaced, 2 key notes |
| 3 | 20 / 20 (index 20) | 3/3 | 5 + 2 | 0 wrong; 1 cross-ref fixed |

Method: Ch1 and Ch2 items are text classification (no code applies), so each was re-derived by hand and checked against the key; all arithmetic and table facts in Ch2 (12+9, 8+7, 55,000+48,000=103,000, row counts, word count) were recomputed. Every Ch3 truth table, row count, equivalence and De Morgan claim (Examples 1 to 5, Scenario 1 and 2, Q1 to Q20, self-checks) was recomputed in Python with itertools; all matched (Q11=3, Q12=5, Q13 differ on rows 5 and 7 with 3 vs 5 true, Q17=7 of 16, Q18 equivalent with 5 true, Q20=4 rings and 3 single-sensor rows, Example 5=5 of 8).

## Fixes
| Ch | Item | Problem | Fix |
|---|---|---|---|
| 2 | Q29 + key | Sentence reused verbatim from the concept table ("first candidate Anita interviewed ... middle name"), so the reader had seen it explained | Replaced with a new unknown-fact sentence (helpdesk caller, refund pending); key updated |
| 2 | Key Q17, Q24 | "either...or" was read as inclusive before Chapter 3 introduces the OR convention | Key now says the answer is true under both readings and points to Chapter 3 |
| 3 | Closing pointer | "Book 13 Part 2" is conditionals and syllogisms; Boolean logic drills are in Part 9 | Pointed to Book 13 Part 9 |
| 1 | Closing pointer | Premise/conclusion drills live in Book 13 Part 8 and were not referenced | Added Part 8 reference (Part 2 kept for next steps) |

## Checks passed
- Template: self-check, concept, why-it-matters box, exactly 5 examples, 2 scenarios labelled illustrative, numbered Q1..Qn tagged easy/medium/hard, no answers in chapter files, mistake log (5 each), 5-line recap, spreadsheet pointer. Keys cover every practice question and self-check.
- No em or en dashes in any of the 6 files; no code fences (none needed, so balanced); tables followed by blank lines.
- Honesty: no real people, companies or studies; invented numbers labelled illustrative. Ch2 Excel formula `=B2>50000` is trivial and not labelled "from memory, not run here" (not run); minor.

## Overlap
Grepped Book 13 Parts 1 to 12 and Book 6 Part 7 for: truth table, exclusive or, De Morgan, tautology, premise, deduction/induction, sensors, gym, free delivery, library fine, phone allowance. No copied or reworded items. Related but different: Book 6 Part 7 Q48 (deduction vs induction, a definition question) and Book 13 Part 9 Q17 (XOR of 3 inputs), Q23 (tautologies); Ch1 and Ch3 items use different scenarios and structure.
Within Book 14: Ch3 Q3 and Q7 are both plain "p OR q" tables (Q7 adds the inclusive-OR explanation); Ch1 Example 5B and Q10 are both "because" explanations. Left as deliberate reinforcement.

## Unresolved / notes
- Ch2 is about 1,770 words (below the 2,000 guide); not padded.
- Ch1 Q3 treats "must be at the airport by 6 am" as deduction from check-in closing 2 hours before departure; accepted as the stated rule, a pedantic reader could add an unstated premise (must arrive before check-in closes).
- Ch3 Q7 (easy) is nearly a repeat of Example 3.
- Claims left unverified: none beyond the above; no external sources cited.
