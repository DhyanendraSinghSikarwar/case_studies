# Review: Book 6 Part 01 (Percentages, Profit and Loss, Discounts)

File: Book06_Aptitude/Book06_Part01.md (edited in place). Scratch: /tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C06_Part01 (solve.py, orig.md = backup before edits).

## Counts
- Answers checked: 82 of 82.
- Re-solved by code: 76 numeric/puzzle answers (exact fractions; brute force over vote totals, pass marks, discount rates, x values; enumeration of overlap for Q59). The 5 concept items (Q1, Q4, Q8, Q27, Q70) were checked by derivation and worked examples recomputed in code.
- Final answers wrong: 0. All 82 headline answers and step-by-step numbers matched my independent results.
- Answers changed: 14 (2 wrong follow-ups, 1 misleading follow-up, 11 for wording, template or clarity). Plus a bulk clean-up of Check lines across the part (below).
- Follow-up variants recomputed: all (about 150); two were wrong or misleading.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q2 | Follow-up 2 asked "840 as a percent of 126" but gave 126/840 = 15% (that is 126 as a percent of 840; the asked value is 666.7%). | Reworded to "What percent of 840 is 126?". |
| Q59 | Follow-up 2 said 40% failed both gives 75% passed both. Impossible: Maths alone is 70% so at most 30% can fail both, and the overlap cannot exceed 65%. | Replaced with the impossibility explanation plus the valid boundary case (30% fail both gives 65% overlap). |
| Q28 | Follow-up 1 called unsold stock a "30% loss on paper" (misleading base). | Now says unsold stock is not a loss; 5 sold give 40% profit on their cost; cash is 30% short of the full outlay. |
| Q81 | Common mistake text "dividing by Rs 36 (11.11% + 25% = 36.11%)" was muddled (the figure came from adding gains). | Rewritten as adding the two gains instead of multiplying. |
| Q51 | Trap line "Adding 540 x 1.05" was unclear. | Rewritten: adding back 10% (594) or assuming net -5%. |
| Q43 | Check line ("Reverse: 50.4% of any price...") was confusing. | Reworded; exact fraction 62/125 kept. |
| Q11 | No Fast method and no Check. | Added both. |
| Q1, Q4, Q8 | No Check line (concept items). | Added Check lines using recomputed examples. |
| Q4 | "SP" used in the worked example before being defined. | Defined SP at first use. |
| Q37 | "Complement" used without explanation. | Explained as "the rest: 100% - 40% = 60%". |
| Q67 | "a 8%" grammar. | "an 8%". |
| Q2-Q21, Q28-Q31, Q33, Q36-Q38, Q41-Q42 and others | Template: no separate **Check:** line (check was buried in Explain simply, or empty after clean-up, or inside Common mistakes in Q2). | Moved or wrote a real Check line in all 82 answers (82 Check lines now). |
| Q2-Q82 (about 55) | Overstated "Verified by script" / "(script)" claims (writers' scripts not trusted). | Removed all such wording; arithmetic back-checks kept. Added a header method note stating that review re-solved everything by code. |
| Header | Timing labels "(30 seconds)" were not marked as guidance. | Added note: they are rule-of-thumb practice targets, not an official limit. |

## Shortcuts checked (valid, limits stated or added)
- x + y + xy/100 (and minus forms), successive discounts as multipliers, r/(100+r) price-consumption and base-flip formulas, equal-SP gain/loss x squared / 100, CP of m = SP of n formula (m - n)/n, margin to markup p/(100 - p), buy-a-get-b-free b/(a+b), false weight error/(weight given), reverse percentage by dividing by the multiplier. All hold for the stated cases. Q54 "add the percentages" is valid only for one loss plus one gain on the same cost (stated in Explain simply).

## Ambiguity and assumptions
- Q22 (every vote valid, two candidates), Q44/Q77/Q81 (profit measured on cost of goods actually handed over), Q49 (identical items), Q64 (10 overtime hours are extra to the 160 normal hours) are all stated in the question or answer. Unique answer in each case.
- Q22, Q23, Q80, Q82 uniqueness confirmed by enumeration (Q82 positive root only, stated).

## Claims
- "Asked at": all lines say "commonly asked (no company-specific report found)" with prep-site language marked unverified, or (Q62) an original item. Q77 cites a Careers360 prep question pattern, which matches research/Book06_Part01_sources.md and is marked unverified. No company attribution was added. Nothing in research/interview_processes.md was needed for this part.

## Unresolved / report only
- Ordering: stars and difficulty order correct (3-star, then 2-star, then 1-star; green, yellow, red within star; numbering Q1 to Q82 continuous). Q73 to Q76 are one-star yellow ahead of one-star red, as required.
- Duplicates within the part (report only, not removed): Q15/Q40/Q82 (+x% then -x%), Q18/Q71 (equal SP gain and loss), Q14/Q69/Q20 (base-flip), Q13/Q42/Q43/Q50 (successive discounts), Q44/Q72/Q77/Q81 (false weight), Q16/Q46/Q47 (markup then discount), Q57/Q58 (revenue). Variation in numbers and twist is present; overlap with other parts not checkable from this file alone.
- Target 70, actual 82 (stated in the header).
- Style: no code fences, no em dashes in answers (only the part-title line), no tables, no pasted scripts.

## Left unverified
- Prep-site claims in Asked at (frequency of percentages and profit-loss at service-company gates) and the Accenture/TCS/Infosys test-format figures in the sources file (single blogs, snippet-level). Not used in answers beyond the generic "unverified" phrase.
