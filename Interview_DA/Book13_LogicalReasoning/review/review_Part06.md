# Review: Book 13 Part 6 (Wave C)

Reviewer scope: Book13_Part06.md (60 answers). Edited in place with targeted replacements; no headings, numbers, stars or order changed. No commit.

## Counts
- Answers checked: 60 of 60.
- Questions independently re-solved by code (python, scratch folder C13_Part06) before comparing with the written answers: 47 (Q2, Q5-Q10, Q16, Q23-Q30, Q32-Q40, Q44-Q45, Q47-Q56, Q58-Q60, plus the Q16/Q36/Q37 uniqueness searches by brute force). The remaining 13 (Q1, Q3, Q4, Q11-Q15, Q17-Q22, Q31, Q41-Q43, Q46, Q57) are blood-relation, coded-relation or method items solved by hand from the family-tree rules (the coded relations Q18-Q20 and Q22 re-derived symbol by symbol).
- Written final answers wrong: 0. All 60 stated answers confirmed and unique (Q36 has 2 valid code assignments, but "audit" = pe in both; Q58 checked over whole hours 0-99, only 51; no duplicate net pay values).
- Follow-up variants re-run: all numeric and string variants reproduced (Q5, Q6, Q8, Q9, Q16, Q23, Q26, Q27, Q29, Q30, Q32-Q35, Q39, Q40, Q44, Q45, Q47-Q49, Q57, Q59, Q60). One wrong (Q18).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q18 | Follow-up 2 said "R / S" is contradictory because "R was Q's sister (female)". Wrong: Q x R says only that Q is female; R's gender is open. R / S is consistent (R is Q's brother), P becomes S's paternal grandfather. | Follow-up rewritten with the correct result. |
| Q58 | Check claimed "net pay rises with h, so no other value matches". False: net is 980 at h = 46 but 909 at h = 47 (deduction cliff). Whole-hour assumption was unstated. | Check rewritten (non-monotonic net stated, whole hours assumed, no-deduction branch excluded even for part hours, brute force over 0-99 gives only 51); one explain bullet added. |
| Q54 | Did not warn about the cliff the payroll rule creates (46 h gives 980, 47 h gives 909). | One sentence added to the explanation. |
| Q49 | "Explain simply" bullet about order was muddled (said dedupe order matters while arguing it does not). | Bullet rewritten: reversing decides which copy is first; the shift never merges digits, so dedupe before or after the shift gives the same output. |
| Q1, Q12, Q17, Q43 | "Asked at" named Infosys, Cognizant or Accenture for blood relations; research/Book13_Part06_sources.md supports blood relations only for TCS NQT and Mu Sigma (Cognizant, Accenture and Infosys appear there for direction or coding items). | Narrowed to "TCS NQT and Mu Sigma ... (prep sites, unverified)". |

## Checked and left as is
- Conventions: full siblings, "mother's husband = father", "only" collapsing a clue, clockwise-positive bearings, strict "below 5" (Q47), "first occurrence" (Q49), Y as consonant (Q39), Z excluded from the 5 x 5 grid (Q10) are all stated and applied consistently.
- Wrong-option reasoning, Fast methods and Check lines were verified true except the two fixed above. Q38's claim that reversing and vowel replacement commute is true.
- Q3 and Q16 "brute force by script" claims: both results are correct (Q16 re-run: only s = 3, d = 4; Q3 minimum 3 is forced by three generations); I did not re-run the writers' own script for Q3.
- Style: no em or en dashes outside the part-title line; 14 code fences (balanced); no pasted scripts.
- Q4, Q11, Q21, Q22, Q31, Q41, Q46, Q57 are concept answers and use the concept template (no step-by-step block), which is acceptable.

## Overlap with Book 6 Part 7 (report only)
No near copies. Same formats with different data: Book 6 Q16 (walk 5N, right 3, right 5) vs Q5 here; Book 6 Q26 (overlapping-sentence word code) vs Q36-Q37; Book 6 Q28 (coded relation) vs Q18-Q20; Book 6 Q12-Q13 (letter shift) vs Q32-Q35; Book 6 Q27 (walk, net displacement) vs Q27 here; Book 6 Q1/Q4/Q32 (only brother/daughter) vs Q1, Q4, Q15. Overlap is topic-level only.

## Ordering
Stars run 3-star (Q1-Q43), then 2-star (Q44-Q58), then 1-star (Q59-Q60); difficulty labels green to yellow to red within blocks (Q43 red among yellow, Q58 red among yellow; acceptable). No numbering gaps.

## Unresolved / unverified
- All "Asked at" topic-list claims remain "prep site, unverified"; no company-specific report exists (sources file says so).
- Q51 uses the "n + sqrt(n) + 1" rule; it fits all five pairs and is the only simple rule found, but other rules could fit five points.
- Q50 three-digit generalisation is explicitly left untested in the answer.
