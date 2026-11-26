# Review Ch07-09 (Book 14, Wave C)

Scope: Ch07, Ch08, Ch09 and answer keys. Scratch scripts: scratchpad/C14_Ch07-09 (c7.py, c7b.py, c7c.py, c9.py).

## Counts
| Chapter | Practice re-solved by code or exact enumeration / total | Examples, scenarios, self-checks re-solved | Wrong answers found | Items changed (overlap or ambiguity) |
|---|---|---|---|---|
| Ch07 | 25 / 25 (region enumeration for all 3-set and min/max items) | 5/5, 2/2, 3/3 | 0 | 3 (Q9, Q17, Q22) |
| Ch08 | 30 / 30 (letters, digits, bands, counts by script; analogies by reasoning) | 5/5, 2/2, 3/3 | 0 numeric; 1 ambiguous (Q18) | 10 (see table) |
| Ch09 | 40 / 40 (rule-library solver plus exact polynomial fits; wrong-term items by single-term repair) | 5/5, 2/2, 3/3 | 0 | 2 (Q5, Q25) plus format |

All word counts are within range (Ch07 3,325; Ch08 2,425; Ch09 2,850). Practice counts match the index (25, 30, 40). No em or en dashes, fences balanced (none used), blank line after every table.

## Fixes
| Ch | Item | Problem | Fix |
|---|---|---|---|
| 07 | Q9 | Same template as Book 6 Part 7 Q49 (total, A, B, neither -> both) | Restated with only-A, only-B, neither given; asks both and phone total; key rewritten (answers 37 and 72) |
| 07 | Q17b | Min/max of "both" for 2 sets with 100 total duplicated Book 13 Part 2 Q68 structure | Part (b) now asks the smallest and largest number who buy neither (0 and 30); key rewritten, enumerated |
| 07 | Q22 | 3-set min of "all three" with 100 people duplicated Book 13 Part 2 Q14 | New numbers and "none = 5" condition: 60 employees, 45/40/35, answer 10 to 32; key shows both bounds |
| 08 | Self-check 2, Ex 3, concept table | "Pen : Write :: Knife : Cut" copied Book 6 Part 7 Q34 (also in Book 13 Part 7) | Broom : Sweep :: Needle : Sew; Scissors : Cut :: Spade : Dig; table example brush : paint; key updated |
| 08 | Concept table | "employee : payslip" listed under maker/product (wrong relationship, contradicted Q26 key) | Rows now "author : book" and "employee : payslip" (person and a record about them) |
| 08 | Q3 | Months with 30 days: lightly reworded Book 13 Part 7 Q24 | Replaced by shapes with straight edges (Circle); key updated |
| 08 | Q6 | Letter-gap item: P pair broke the first-letter step as well (second possible rule) | PR changed to RT so only NQ breaks; key updated |
| 08 | Q9 | Gave away the method sentence used in the concept (pilot/driver) | Author : Book :: Painter : Painting; key updated |
| 08 | Q11 | Reverse of Book 13 Part 7 Q20 (Expand : Contract) | Generous : Stingy :: Brave : Cowardly; key updated |
| 08 | Q12, Q15 | "Page : Book" and "Rain : Flood" are Book 13 Part 7 examples; Q15 answer was in the concept table | Wheel : Car :: Row : Table; Exercise : Fitness :: Study : Knowledge; keys updated |
| 08 | Q18 | "Overtime pay" is not clearly variable with sales (ambiguous) | Replaced by "Card payment fees"; key updated (still 4 fixed, 4 variable) |
| 08 | Q21 | Contained KMO and PRT, which are in Book 13 Part 7 Q8 | New group ADG, FIL, KNQ, PSV, UYB with wrap-around hint; answer UYB; key updated |
| 09 | Q5 | Same list as the concept-table example (1, 2, 4, 7, 11) | 3, 4, 6, 9, 13, 18 -> 24; key updated |
| 09 | Q25 | 3, 8, 15, 24, 35 duplicated Book 6 Part 5 Q26 / Part 10; first replacement (n squared plus 1) duplicated Book 6 Part 5 Q40 | New list 2, 4, 9, 17, 28, 43, 59 (gaps grow by 3), 43 should be 42; unique single-term repair confirmed |
| 09 | Practice format | Numbered 1..40 without Q prefix and no easy/medium/hard headings | Added Q1..Q40 labels and three headings (Q1-14, 15-28, 29-40), matching the key |

## Overlaps
- Fixed as above. Remaining generic templates (three-circle problems Ex5, Q13, Q24, Q19 in Ch07; letter-gap odd-one-out Ex2, Q6 in Ch08) share the standard method with Book 13 Part 10 Q13, Book 6 Part 7 Q65 and Book 13 Part 7 Q21 but use different numbers, letters and scenarios. Accepted.
- Within Book 14: Ch07 Q13, Q24 and Ex5 are the same template with different numbers (intentional graded practice). No exact duplicate found inside Ch07-09.
- Ch09 series checked by regex against all Book 6 and Book 13 parts after the fixes: no remaining four-term matches.

## Concept and cross-reference checks
- Set rules (inclusion-exclusion, sum-of-circles rule, De Morgan) correct. Cross-references exist: Book 1 (COUNTIFS), Book 2 (INTERSECT, LAG), Book 13 Part 7 and Part 10, Book 6 Part 5.
- Ch08 uses "wrap-around" in Q21 before Ch09 teaches it; a one-line hint was added in the question.

## Unresolved or unverified
- Ch08 analogies, odd-one-out by meaning (Q1, Q2, Q5, Q7, Q8, Q19, Q25, Q26) and Q24 (deliberately ambiguous) rest on judgement, not code; each has one natural rule.
- Ch09 uniqueness is relative to the rule families tried (polynomials to degree 3, linear recurrences, interleaved tracks, alternating operations, products); the chapter and key already say so. Q21 and Q36 depend on the hint or the place-number rule.
- "Kilogram : Weight" (Ch08 Q10 stem and table) uses everyday "weight" for mass; left as is.
- Appendix and glossary files were not in scope and were not checked for these chapters' terms.
