# Review: Book 14, Chapters 19, 20, 21 (scratch id Ch19-21)

All code in scratchpad `C14_Ch19-21` (t19.py, t20.py). Solved blind by brute force, then compared with chapter and key.

## Counts
| Chapter | Practice re-solved by code / total | Examples + scenarios + self-checks re-solved | Wrong answers | Items changed |
|---|---|---|---|---|
| 19 Truth-teller and liar | 20 / 20 (all puzzles over every labelling x facts; Q19 over 6 kind assignments; Q12 by reasoning) | 5 / 5 examples, 2 / 2 scenarios, 3 / 3 self-checks | 0 | 0 puzzles; 1 key header |
| 20 Clocks and calendars | 25 / 25 (exact fractions, datetime, calendar) | 5 / 5, 2 / 2, 3 / 3 | 0 | 2 (overlap) |
| 21 Statement-assumption | 40 / 40 (numeric and logical items by code; Q27, Q29 to Q30, Q35 to Q40 by set enumeration and arithmetic; judgement items Q1 to Q4, Q8 to Q18, Q22 to Q24, Q28, Q31 to Q34 re-judged by hand with the chapter's own tests) | 5 / 5, 2 / 2, 3 / 3 | 0 | 1 (overlap) |

Known issue: Ch19 Example 3 final wording was re-run in final form (thief in {Rina, Sam, Tara}, exactly one liar): unique answer Tara, table rows (2, 2, 1 liars) all correct.

## Fixes
| Chapter | Item | Problem | Fix |
|---|---|---|---|
| 19 key | header | Said Q19 was checked over "4 x 4 x 4 = 64" assignments; with three kinds it is 3 x 3 x 3 = 27 (6 with one of each) | Corrected the sentence; added Q13 to the days checked |
| 20 | Q5 + key | Same template as Book 6 Part 7 Q42 (Wednesday, 100 days from today) | Changed to "Tuesday, what day was it 150 days ago?"; key now Saturday (checked by datetime) |
| 20 | Q6 + key | Lightly reworded Book 6 Part 7 Q40 (1900, 2000, 2024, 2100 leap years) | New years 1800, 2024, 2400, 2500; answer 2024 and 2400 |
| 20 | Part 2 concept | "12 o'clock counts as H = 0" was only in the key (needed for Q4) | Added one line to the concept section |
| 20 | Q19 key | Closing sentence muddled ("12:00 + 12 hours") | Rewritten: clock has run 192 hours = 8 days, shows 12:00; true time is noon |
| 20 | Pointer | "Book 13 Part 4" has seating and arrangements, no clock or calendar items | Now points to Book 6 Part 7 only |
| 21 | Q21 + key | Same template as Book 6 Part 7 Q45 (only data analysts attend, Priya attended) and same answer shape as Q26 | New two-step chain (shortlisted, interviewed, offer letter); answer still (a) |

## Overlaps
- Book 6 Part 7 Q40, Q42, Q45: fixed above. Checked Q38, Q51, Q52, Q64, Q66 (clocks, calendar): no copy (Ch20 uses other times and dates).
- Book 13 Part 5 and Book 6 Q68, Q72 (knights and knaves): Ch19 Ex2, Q2, Q3, Q12 and Q14 use the same classic ideas (mutual accusation, "we are both liars", "are you a truth-teller") but different statements, names and numbers; left as is, borderline. Ch19 Q11 is the "at least k" variant of Book 13 Q11 ("exactly k"); different.
- Within Book 14: Ch20 Q24 (Friday the 13th, 2027) is related to Ch18 Q21 (13th falls on Friday, three months given) but asks a different thing; no duplicates found in other chapters.

## Checked, no change needed
Template (self-check 3, 5 examples, 2 scenarios labelled illustrative, counts 20 / 25 / 40, easy to hard order with tags, mistake logs 5, recaps 5, no answers in chapter files, key entry for every item); no em or en dashes; no code fences; tables followed by blank lines; word counts 3,274 / 2,326 / 3,333; concept statements correct (negation of "and" / "or", 5.5 degrees per minute, leap rule, "most" means over half); cross-references Book 13 Part 5 (liar puzzles) and Book 13 Part 8 (critical reasoning), Book 6 Part 7 exist and match.

## Unresolved / unverified
- Ch21 assumption and course-of-action items (about 25) are judgement calls; they follow the chapter's stated tests, and no code can prove them. Q9, Q13 and Q23 could be argued either way on "should be followed" but the chapter's tests support the keyed answers.
- Ch19 Q12 depends on the stated idea that anyone asked "Are you a truth-teller?" answers yes (explained in the question and key); not code-checked.
- Ch20 Indian financial year convention (1 April to 31 March) is stated as a convention, not verified against a source. Spreadsheet pointers name functions only (no formulas shown), "see Book 1/2" not verified beyond the folders existing.
