# Review: Book 13 Part 7 (letter and alphanumeric series, analogy, classification, pattern recognition)

## Counts
- Answers checked: 50 of 50.
- Questions independently re-solved by code (before reading the written answers): 42 (all fully specified items, scratch script C13_Part07/s.py), including a coefficient search over row-rule formulas for Q35 and Q42. The 8 method/"why" questions (Q1, Q7, Q15, Q17, Q27, Q28, Q43, Q44) were checked by hand; Q28 arithmetic (900/20) by code.
- Final answers wrong: 0. Answers non-unique or changed: 0. Written follow-up variants re-run and all correct.
- Prose or reasoning fixes: 9 (below). Heading, numbering, stars, order, option and data lines untouched.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q9 | Follow-up "Cell is to row as ? is to table" was muddled; row and column both fit | Reworded: both are parts of a table, natural reading is row, item would need options |
| Q10 | Check named only one second rule (COUNTIF counts) and the dismissal reason was weak | Added SUMIFS (only multi-condition) as second rule, why lookup-vs-summary is preferred, rule used stated |
| Q12 | Fast method "29 - 25 = 4" was unclear | Now says the gap from Y (25) to 29 is 4 |
| Q17 | False claim "any letter is at most 2 steps from an anchor" (A is 4 from E) | Restricted to F to Y; A to D and Z explained |
| Q21 | Claimed the first-letter rule "also points to PR"; it does not (starts 3,7,11,16,20, no single removal gives a constant step) | Rewritten: second rule is not clean, gap-inside-pair rule used |
| Q27 | Unsupported generalisation about test setters | Labelled "our suggestion, not a guarantee" |
| Q31 | "jump of 2 letters skipped over" wrong (one letter, W, is skipped) | Corrected |
| Q35 | "No other simple rule" slightly overclaimed (156 contrived formulas fit two rows, all give 42) | Check now says natural variants also give 42 and only two complete rows exist |
| Q42 | "Found only this one" was false: search found two other six-term fits giving 56 and 62 | Check rewritten honestly; x squared minus Col 2 is the simplest rule, answer 59 kept |
| Q47 | Common-mistake line "Adding 4 and 6" meaningless | Reworded (differences 4, 12, 36 not constant) |

## Rule and second-rule audit (all stated rules fit every term)
- Series Q2, Q3, Q4, Q5, Q6, Q11, Q12, Q13, Q14, Q30, Q31, Q33, Q34, Q47, Q48: stated rule fits all given terms; no rival rule of comparable simplicity. Q27 is the deliberate ambiguity item (16 vs 14, stated). Q33: doubling and differences-doubling are the same rule.
- Q32 anomaly (S should be T): unique single-change repair. Q37 (J49): letter rule fits all, number rule 2n^2 breaks at J; "only odd number" agrees.
- Odd one out: Q8 BDG (+2,+2 rule, WYA fits with wrap), Q40 RTU (same), Q21 PR (gap 3; no clean second rule, fixed), Q22 UNION (set operator vs joins; second rule CROSS JOIN has no ON, stated), Q23 PF deduction (earnings vs deductions; second rule Basic pay not an allowance, stated), Q24 February (days in month; letter-count rule fails), Q10 VLOOKUP (returns vs summarises; second rules now stated), Q43 deliberately multi-rule (9 intended; 2 and 11 stated).
- Analogy: Q9 part to whole, Table (Column is a sibling, stated); Q19 shift +2; Q20 antonym; Q25 sum of positions (also equals 3 x middle letter, same answer 12); Q26 cube; Q29 tool to purpose (Selecting); Q45 position-dependent shift; Q46 position squared.
- Computed items match code: Q16 Morning, Q18 M, Q36 P, Q38 4 pairs (P-T, V-T, V-S, T-S), Q39 3, Q41 J, Q49 D, Q50 M.

## Honesty, style, template
- Asked-at lines claim only "commonly asked (no company-specific report found)" or prep-site claims marked unverified; consistent with research/Book13_Part07_sources.md. Time splits and give-up rules are labelled "our suggestion". Q22 SQL behaviour is textbook and labelled "not run here".
- No em or en dashes in answers (title line only); code fences: none; no scripts pasted. Template complete (concept questions use the concept variant, no Fast method or Check by design).
- Many Checks say "Verified by script"; the writers' claim was unproven, but I re-ran every one and they hold.

## Overlap / ordering (report only)
- Numbering 1 to 50 intact; star order is consistent (3-star Q1-16, 2-star Q17-42, 1-star Q43-50). Q13 and Q47 share the "n(n+1) / x3 track" teaching but are different items; Q2/Q12 and Q3 are same-family variants, acceptable.
- No near copy of a Book 6 Part 7 question found by reading titles against the dedupe log (log reports none); pure number series stay in Book 6 Part 5 (Q27 and Q35 touch number patterns briefly).

## Unresolved / unverified
- None blocking. Prep-site statements (TCS NQT, CCBP) remain "reported, unverified". Excel function behaviour in Q10 and salary conventions in Q23 are standard knowledge, from memory, not run here.
