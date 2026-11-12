# Review: Book 6 Part 6 (Permutation, Combination, Probability)

## Counts
- Answers checked: 69 of 69 (all headings, numbers, stars and order untouched).
- Answers re-solved by code before comparing with the written text: 59 numeric/probability/counting items (every item except the 10 concept items Q1-Q5, Q29, Q31 formula, Q35, Q37, Q38, checked by reasoning; Q1-Q2 examples, Q30 and Q31 numbers were also scripted). Brute force used for letter/seat/digit arrangements, dice, cards, balls, committees, leap-year Sundays, derangements, circular seating, rank of a word; exact fractions for probabilities.
- Follow-up variants re-solved by code too (BANANA, ASSESS, DESIGN, TEAR, 3-men/4-women gap, 5-point collinear, 4/5 teams, D5, sums 9/11/12 of three dice, etc.). All matched.
- Answers with a wrong final answer, wrong working or wrong option: 0.
- Answers edited: 12 (wording, missing template part, source claims, shortcut limits).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q29 | Template: no Check line | Added Check line |
| Q37 | Template: no Check line; stray "Actually," wording; edge case (probability 0) unstated | Added Check line with the die example and the zero-probability edge case; reworded bullet |
| Q30 | Garbled follow-up "nCr/NCr" | Rewrote as favourable selections over total selections, referencing 3C2/5C2 |
| Q63 | Fast-method formula stated without its limits | Added limit: needs digits equally often per place; adjust if a digit repeats or 0 cannot lead |
| Q64 | Garbled trap sentence | Rewrote: using 9 x 8 x 7 for both cases, ignoring leading zero |
| Q65 | Trap mentioned Y, which is not in EQUATIONS | Replaced with correct vowel/consonant lists |
| Q69 | "Inclusion-exclusion" used without explanation; trap line unclear | Explained in the spoken line; rewrote trap (stopping early, overlaps must be added back) |
| Q60-Q69 (10 items) | Asked at claimed "P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests", which the sources do not support for expected value, birthday, stars and bars, digit sums, multinomial, derangement items (sources file calls these gap-fills and one-star differentiators "not evidenced as frequent") | Replaced with "commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report" |

"Verified by script" wording in Check lines was true for every item once re-run; no overstated Check wording remained.

## Shortcuts checked (valid, limits stated)
Complement rule (Q5, Q15, Q23, Q58), glue method with internal order (Q18, Q25, Q56), gap method (Q28, Q56), (n-1)! and (n-1)!/2 with n at least 3 (Q24, Q38), floor-count of multiples (Q53), stars and bars (Q62), 7-day pairing (Q50, assumes each start day equally likely, stated), derangement recurrence (Q69), rank-of-word method (Q41), n!/e approximation (Q69, fine as an estimate).

## Assumptions and ambiguities
- Q50 and Q61: equal-likelihood assumptions are stated in the answer or question. Q49: assumes independent equal chance of boy/girl, stated in the question.
- Q57 two-way table is consistent (70 men, 50 women, 120 total). No ambiguous or non-unique items found.

## Unresolved / report-only
- Ordering/numbering: stars run 3,3,...,2,...,1 by design; no numbering gaps. Header says "Target 60 / Actual 69" (fine).
- Overlap: Q12 and Q31/Q46 (repeated-letter method; MISSISSIPPI is answered in both Q31 and Q46 with the same number, 34,650); Q10 and Q22 and Q55 share the two-dice space; Q24 and Q38 and Q68 circular arrangements; Q47 duplicates the card-pair setup of Q19. Q66 and Q59 both cover group splits. Cross-part duplicates with Part 5/Book 5 probability not checked beyond scope note.
- Q42 follow-up uses inclusion-exclusion (3^5 - 3 x 2^5 + 3) without explaining it; answer is correct (150, verified).

## Claims left unverified
All "Asked at" prep-site statements (TCS NQT, Wipro, Infosys, Mu Sigma, PapersAdda, Toprankers, FACE Prep) rest on snippet-level sources and remain marked unverified. No time-per-question or pass-mark guidance appears in this part beyond "30 seconds" fast-method labels, which are a rule of thumb.
