# Review: Book 6 Part 9 (Data Sufficiency)

Reviewer: Wave C. No git commits. Scratch: .../scratchpad/C06_Part09/a.py (model enumeration), ed.py (edit script).

## Counts
- Answers checked: 49 (Q1-Q49).
- Re-solved by code: 38 items (Q3-Q12, Q15-Q27, Q30-Q32, Q34-Q40, Q42, Q43, Q45, Q46, Q49). Each statement was tested alone and together over a grid of integer, fraction and negative values, and every numeric or letter follow-up was recomputed. The other 11 (Q1, Q2, Q13, Q14, Q28, Q29, Q33, Q41, Q44, Q47, Q48) are concept or business-reasoning items: read for correctness, examples spot-checked, not coded.
- Wrong option letters or wrong final answers: 0. All 49 verdicts, step-by-step numbers and follow-up numbers agree with the code (e.g. Q8 800/9, Q22 48, Q26 only 36 and 72, Q27 father 30, Q42 B = 30,000 and 35,454.55, Q43 E, Q49 A).
- Answers edited: 17 (wording, label and completeness fixes only).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q13 | Time per question and "pick E when unknowns exceed equations" stated as fact | Labelled as rule of thumb and heuristic |
| Q14 | "Every A or B becomes a false D" overstated (borrowing I into II cannot damage a true B) | Reworded: can turn C into false B or D, and A into false D |
| Q29 | Guess advice contradicted itself (said "not penalised" as a fact) | Now conditional on no negative marking or two options ruled out; time labelled rule of thumb |
| Q22 | 2ab/(a+b) shortcut had no limit stated | Added: valid only for equal distances each way |
| Q32 | "154 = 22 x 7, verified by script" claim was loose | Replaced with the arithmetic itself |
| Q44 | Attrition denominator conflicted with Q19 (opening) | Says opening or average, depending on company definition |
| Q49 | Garbled trap sentence; "verified below 50" | Trap rewritten (n = 2 is allowed by II); check now says every odd n below 500 by code, plus the factor proof |
| All with Check lines | "verified by script (brute force over all cases)" overstated for infinite domains | Reworded to "verified by code (enumerated a wide range of test values ...)" (Q3-Q12, Q15-Q27, Q30-Q32, Q34-Q40, Q42, Q43, Q45, Q46, Q49) |
| Q5, Q8, Q10, Q11, Q16, Q17, Q18, Q23, Q25 | Missing Fast method line | Added short, valid fast methods |

## Other checks
- Asked at: every line is "commonly asked (no company-specific report found)" plus the prep-site AMCAT/TCS NQT claim marked unverified; it matches research/Book06_Part09_sources.md (prep-site snippets only; no company report). No change.
- Em dashes: only the part-title line. Code fences: none, balanced. Tables: none.
- Ordering/numbering (report only): Q1 to Q49 sequential, stars non-increasing (3, 2, 1). Header says Target 40, Actual 49. Q43 and Q49 are marked red but sit in the 2-star and 1-star bands; Q44 to Q48 (1 star) are lighter items.
- Duplicates/overlap (report only): Q1 and Q3 and Q14 reuse the same Priya/Ravi example (intentional teaching reuse); Q2 and Q6 reuse the n+1-odd example; Q28 and Q40 both use x squared > x; Q17 overlaps Part trains items; Q18, Q22, Q23, Q42 overlap work, speed, SI and partnership parts.

## Unresolved / left unverified
- Prep-site claim that DS appears in AMCAT, TCS NQT and company rounds is unverified (no official specification).
- "C and E are the most common answers" (Q29) is flagged in the answer as an unverified prep-site rule of thumb.
- Q47 states that real DS statements never contradict; this is the standard convention, not testable by code.
- Q5, Q12, Q37 assume profit % is on cost price unless stated (stated in Q5 and Q12 answers).
