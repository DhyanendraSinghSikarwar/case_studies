# Review: Book 6 Part 02 (Ratio, Proportion, Averages, Mixtures)

Reviewed file: `Book06_Aptitude/Book06_Part02.md`. No git commit. Scratch script: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C06_Part02/v.py`.

## Counts
| Item | Count |
|---|---|
| Answers checked | 67 |
| Answers re-solved by code (exact fractions, brute-force search over integers, replacement simulation) | 67 (every item has a numeric or algebraic result, including all follow-up variants) |
| Final answers wrong | 0 |
| Answers edited (reasoning, wording, claims, missing Check) | 12 |

All 67 final answers, step-by-step intermediates, Check lines and numeric follow-ups matched the independent solve. Rounded values (Q50 95.83, Q51 16.67, Q55 14.29, Q38 32.35 follow-up) match exact fractions. Brute force also confirmed uniqueness of Q3, Q7, Q15, Q18, Q19, Q23, Q24, Q34, Q35, Q36, Q52, Q54, Q58, Q62. No ambiguity or unstated-assumption problems were found (Q40 and Q42 to Q43, Q64 to Q65 already state the fixed-volume and well-mixed assumptions).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q6 | No Check line | Added a total-based reverse check |
| Q7 | LCM used at first appearance without explanation | Defined LCM in step 1 |
| Q8 | No Check line | Added direct (ratio) and inverse (product) check |
| Q9 | Check only buried in step 4 | Added a labelled Check line |
| Q15 | "Asked at" claimed a prep-bank pattern with no source | Reduced to "commonly asked (no company-specific report found)" |
| Q18 | Typo ("both age by"); the "fast route" was circular (used the gap 30 before it was known) | Typo fixed; fast route rewritten from 3x = 2x + 10 |
| Q19 | "Fast route" assumed "later 1 part = 4" before it was derived | Rewritten: gap = x, later A = 6x = 4x + 8, so x = 4 |
| Q28 | "Asked at" cited the 7:5 prep-blog example, which backs Q3 not this savings question | Reduced to "commonly asked (no company-specific report found)" |
| Q29 | Check was circular (repeated the fast method) | Replaced with a small-case check (first 3 evens and odds) plus the first-and-last cross-check |
| Q42 | Trap text said the second removal "takes out some water" (the milk is what matters) | Corrected to "takes out some milk too, because the mixture is no longer pure" |
| Q43 | No Check line | Added a round-by-round check (50, 45, 40.5, 36.45) |
| Q46 | "Asked at" cited "2-star topic in prep material", which is the writer's own star judgement, not a source | Reduced to "commonly asked (no company-specific report found)" |
| Q47 | Trap line asserted the test setter "places 50 first" (unsupported) | Reworded to "the tempting wrong option" |

"Verified by script" wording: 21 items still say it. After this review each of those was genuinely re-computed, so the claims now hold.

## Rules and shortcuts checked (all valid, limits stated)
Replacement shortcut (Q14), alligation (Q9, Q16, Q37, Q54), 2ab/(a+b) for equal distances (Q47), componendo-dividendo (Q46), V(1 - x/V)^n for constant volume and well-mixed (Q43), arithmetic-series averages (Q29, Q56), percent-base rules (Q27, Q59), ratio chaining by LCM (Q7, Q34, Q36, Q48).

## Unresolved / report-only items
- Numbering and order: star and difficulty order is correct (3-star Q1 to Q24, 2-star Q25 to Q55, 1-star Q56 to Q67; green, yellow, red within each star). Header says target 60, actual 67; count matches (67).
- Overlap within the part: Q7 and Q48 use the same chain (A:B 2:3, B:C 4:5; Q48 adds a total). Q42, Q43, Q64, Q65 overlap on replacement (different numbers). Q5, Q13, Q45, Q60 are the same "new value joins an average" pattern. Q21, Q63, Q66 partnership; Q38, Q51, Q55 mixture profit; Q9, Q16, Q54 alligation. Overlap with other parts was not checked (only this part was read).
- Q15, Q18, Q19 and similar items keep a second "difference" route in Explain simply; kept because it is correct and useful.
- Q37 step 3 wording ("quantity of the lower group is proportional to the gap on the other side") is correct but dense; left as is.

## Claims left unverified
All "Asked at" lines naming prep sites or companies (Wipro NLTH age pattern Q18, Q19; Accenture milk and acid mixtures Q17, Q39, Q41, Q64; TCS/Infosys/Wipro mixtures Q49; IT-services alligation Q9, Q16, Q37, Q54) are only as strong as the snippet-level prep-site evidence in `research/Book06_Part02_sources.md` and remain marked unverified. No timing or pass-mark guidance appears in this part. No em dashes in answer text (the part-title line keeps one); no code fences or tables; no scripts pasted.
