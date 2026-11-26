# Review: Book 14, Chapters 22, 23, 24 (chapters and answer keys)

Scratch: `/tmp/claude-0/.../scratchpad/C14_Ch22-24/v.py` (brute force for Ch22 Q13, Q17, Q21, Q23, Q24, Q28, Q29, Q30 and for the Ch24 table numbers; all other items are single-step arithmetic or classification, re-derived by hand without reading the key first).

## Counts
| Chapter | Practice re-solved / total | Wrong answers | Items rewritten (overlap, duplication or ambiguity) |
|---|---|---|---|
| 22 Data sufficiency | 30 / 30 | 0 | 4 (Q17, Q19, Q23, Q27) |
| 23 Logical fallacies | 30 / 30 (judgement items; sound-argument items checked for connection of reasons to conclusion) | 0 | 4 (Q1, Q7, Q21, Example 4 wording) |
| 24 Correlation vs causation | 20 / 20 | 0 | 9 (Q2, Q4, Q6, Q7, Q8, Q9, Q13, Q16, Scenario 1) |

Also re-solved: all 5 solved examples and 2 scenarios per chapter, and all self-checks. Ch22 example 5 (36,000 / 78,000), scenario figures (18%, 11.25%, 18.75%, 196) and Ch24 figures (hot avg 996.7 and 9.17, cool 395 and 2.67, CORREL 0.95, 5% budget rule, 0.7 orders, 720 vs 480) all correct. Counts: 5 examples, 2 scenarios, 30 / 30 / 20 questions, 3 self-checks, mistake log 5, recap 5 lines in every chapter; no answers in chapter files; no em or en dashes; tables followed by blank lines; word counts 3,611 / 2,672 / 2,290.

## Fixes
| Ch | Item | Problem | Fix (key updated in step) |
|---|---|---|---|
| 22 | Q19 | Statements I (total 2,50,000) and II (listed salaries total 2,30,000) contradicted each other; also mirrored Book 6 Part 9 Q20 | Replaced by a range question on delivery times (I average 30, II lists 22,25,30,33,40); answer still B, statements now consistent |
| 22 | Q23 | Same-equation trap (2A+3C vs 4A+6C) is a reword of Book 6 Part 9 Q34 | New "same ratio in different words" item (Pune office, contract two thirds of full-time vs full-time 60%); answer still E, verified by code |
| 22 | Q17 | Men/women ratio plus difference too close to Book 6 Part 9 Q16 | Day/night shift agents, same numbers and answer C (30 night agents) |
| 22 | Q27 | Flat-discount item close to Book 6 Part 9 Q11 | Agency fee percentage (8% from either statement); answer still D |
| 23 | Q21 | Near copy of solved Example 5 (payroll auditor) | New supplier delivery-log passage; answer still None |
| 23 | Q1, Q7 | Light rewords of Example 1 (joined last week) and Example 2 (shorter workday trial); Q7 also close to Book 13 Part 2 Q69 | New ad hominem (talks fast, odd clothes) and new straw man (quiet hour vs ban all talking) |
| 23 | Example 4 | First sentence close to Book 13 Part 2 Q34 ("hire ten more analysts") | Now software-purchase either/or, alternatives listed |
| 24 | Q2 | Shoe size and reading score duplicates Book 13 Part 8 Q39(ii) | Grey hair and savings (T, age) |
| 24 | Q16, Scenario 1 | Optional course and ratings close to Book 13 Part 8 Q16; gym and sick days duplicates Book 13 Part 8 Q7 | Voluntary mentoring scheme; money-management webinar and salary-advance requests |
| 24 | Q4, Q6, Q7, Q8, Q9, Q13 | Q4 repeated the concept-table example; Q6, Q7, Q9 were rewords of solved Examples 4, 5, 2; Q8 near Scenario 1; Q13 close to Book 13 Part 8 Q5 | New scenarios (physiotherapy visits R; marathon runners vs gold jewellery C; onboarding video P; newsletter T; recruitment budget R; free-delivery offer T); labels unchanged |
| 22 | Key header | Claimed "brute-force" for every item | Reworded to "re-checked in review by code" |

## Overlaps and duplicates
Overlaps with Book 13 Part 2, Part 8 and Book 6 Part 9 were found and removed (above). Remaining shared ground is classic and unavoidable: ice-cream vs drowning (Ch24 Example 1 has its own figures; Book 13 Part 8 only mentions it in one line) and the "numerator in one statement, denominator in the other" pattern (Ch22 Q26 vs Book 6 Part 9 Q19: different context, numbers and threshold, left as is). No Book 6 Part 7 overlap. Grep inside Book 14 found no duplicated question text between Ch22 to Ch24 and other chapters (Ch22 scenario 1 attrition and Ch24 scenario themes are distinct).

## Cross-references checked
Ch1 (premise, conclusion), Ch6 (valid, sound), Book 6 Part 9 (data sufficiency), Book 13 Part 2 (deductive and fallacies) and Part 8 (critical reasoning, cause vs correlation) all exist and cover the topic.

## Unresolved or judgement notes
- Ch23 labels depend on judgement (for example Q13 tu quoque vs ad hominem, Q22 "None"); the key states its reasoning for each.
- Ch24 Q12 (R) and Q13 (T) are defensible labels; the key gives the reasoning.
- Spreadsheet pointers (CORREL, COUNTIF, GROUP BY) are only named, no formulas shown, so nothing to label "not run".
- No real people, firms or statistics appear; invented brand names (GlowBright, Zing Tea, Zest Bank, Orbit, Heritage Ghee, FastDrop) are fictional.
