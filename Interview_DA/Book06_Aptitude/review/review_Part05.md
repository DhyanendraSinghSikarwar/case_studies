# Review of Book06_Part05 (Number Series and Number System)

## Counts
- Answers checked: 70 of 70.
- Answers re-solved by code: 68 (all except the two pure-concept items, Q2 checklist and Q22 definitions; Q1 rules, Q54 reasoning, Q68 and Q67 were also run numerically). Script: scratchpad/C06_Part05/v.py. Includes brute force for Q16, Q18, Q48 (uniqueness), Q49, Q63 (LCM and HCF of fractions), Q61, Q62, Q43 to Q45.
- Answers with a wrong final answer: 0. Every final answer, step, fast method and follow-up number matched the independent computation.
- Answers changed (wording, claims, assumptions, format): 15 (Q1, Q2, Q10, Q14, Q21, Q24, Q25, Q26, Q27, Q30, Q48, Q49, Q50, Q64, Q66).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q1 | Check line had a confusing factorisation | Replaced by 9 x 594 and 11 x 486, plus the non-divisibility by 8 |
| Q2 | "Asked at" credited JobCannon with the first-differences claim; the sources file supports that only for FACE Prep | Split the attribution |
| Q10 | Trap text ("0 for a digit sum that looks round") was meaningless | Rewrote to real traps |
| Q14 | Cyclicity limits incomplete | Added that units digits 0, 1, 5, 6 never change |
| Q21 | Check said the test "was designed as a trap" (unsupported); no uniqueness assumption | Removed claim; stated the assumption (simplest rule fitting all five terms) |
| Q24 | "Say this" lacked quotes; fast method (test 3 and 7) was muddled | Quoted; replaced with correct limit (below 49 only 2, 3, 5 matter) |
| Q25, Q26 | "Say this" unquoted; Gauss stated as fact | Quoted; Gauss marked as the well-known story |
| Q27 | Check used an approximate decimal product "= 4.0"; trap claimed test setters offer 36/99 (unsupported) | Reworded both |
| Q30 | Unsupported "also appears in business series"; AP follow-up confusing | Reworded both |
| Q48 | "Asked at" claimed prep-site support the sources file does not give | Marked as gap-fill, no source |
| Q49, Q66 | "In every prep-site syllabus" overstated; "stock prep-site pattern" unsupported | Narrowed to the FACE Prep remainders guide / gap-fill |
| Q50 | Fast method missed the case where the alternating sum is 11 or more | Added |
| Q64 | No blank line between table and "Asked at"; Check overstated ("only the squares rule works"); ambiguity of a 2-row pattern not stated | Added blank line; reworded Check; stated assumption (rule uses only the row's own columns; a row-number rule would give 37) |

## Verified with no change needed
All numeric answers and follow-ups: Q3 to Q21, Q23 to Q70 (e.g. Q16 only divisor is 12; Q18 only other number is 60; Q48 unique solution 36, variant 24; Q49 gives 5 for every k; Q63 LCM 20/3, HCF 1/18; Q69 4; Q70 07; Q43 93; Q44 41; Q45 28; Q62 21; Q46 12; Q47 24; Q53 57,500 and 5,25,000).

## Unresolved / report only
- Ordering: stars are not monotone (Q1 to Q21 are three-star, then two-star, then one-star groups mixed with difficulty colours); acceptable but not sorted by topic. Q2 and Q22 have no Check line (concept items).
- Q64 and Q21: pattern-completion items are inherently non-unique; assumptions are now stated in the answers.
- Overlap with other parts: remainders by cyclicity (Q14, Q15, Q20, Q65, Q69, Q70) and HCF/LCM word problems (Q16 to Q19, Q42, Q66) likely overlap with Book 6 Part 3 or Part 4 topics (arithmetic/percentages) only in method; not checked line by line. Excel MOD (Q34, Q67) may overlap with Book 3 Excel material.
- Heading says Target 50 / Actual 70 (frozen, not edited).

## Claims left unverified
All company or prep-site attributions (TCS NQT syllabus, Infosys 5-8 series items, PrepInsta tagging, CCBP, FACE Prep) rest on the sources file, which itself marks them as unverified prep-site snippets. I did not re-check any web source. The 30-second labels on "Fast method" are rule-of-thumb headings, not measured times.
