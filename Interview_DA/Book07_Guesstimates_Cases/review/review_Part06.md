# Review report: Book07 Part 06 (profitability, pricing and growth cases)

Reviewer pass: Wave C. File edited in place: Book07_Guesstimates_Cases/Book07_Part06.md (targeted replacements only; headings, numbers, stars, order and inline question data untouched).

## Counts
- Answers checked: 76 of 76 (Q1 to Q76, numbering continuous, star and difficulty order correct).
- Answers whose numbers were recomputed by code: 76 (all arithmetic ones in full; the purely conceptual ones, e.g. Q1, Q24 to Q29, Q61, Q73, have no numbers beyond small mini-examples, which were also recomputed where present).
- Answers with a wrong figure or statement fixed: 4 (Q3, Q7, Q32, Q47). Answers with other substantive edits: 2 (Q20 statistics, Q74 honesty). Answers with clarity/format edits only: about 14.
- Em dashes in answers: none (only the part-title line has one). Code fences: none, balanced. Scripts pasted into answers: none.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q3 | "1,000 units or 16.7% above" break-even is wrong wording: 1,000 is 20% above 5,000; 16.7% is of actual sales | States both: 20% above break-even, 16.7% of actual sales |
| Q7 | Decision rule inverted ("break-even volume fall below the likely fall means go") | Rewritten: go if expected volume loss is smaller than the break-even loss (20% in the example) |
| Q20 | Recommended rolling out B although profit-per-visitor gap is not significant (recomputed z about 1.49, SE about Rs 0.27); only conversion z (3.4) was shown | Say-this, Result and Check now say B leads but is unproven; added the profit z; extend test |
| Q32 | Sensitivity wrong: 25% refunds gives contribution 20,000 x 0.75 - 9,000 = Rs 6,000 (not 5,000) and break-even about 2,667 (not 3,200) | Corrected both numbers |
| Q47 | Premise ambiguity: "10% below" read strictly makes prices equal after the cut; text only used the loose 100 vs 110 reading. Also a vague hold-vs-match sentence | Both readings stated; replaced vague line with computed rule: holding (40) beats matching (30) unless more than 25% of volume is lost |
| Q74 | "Raising money typically takes 6 months" stated as a general fact | Marked as an assumption |
| Q59 | Western comma format inconsistent with the Indian format used elsewhere | Converted to lakh style (-Rs 1,80,000) |
| Q4, Q7, Q14, Q22, Q38, Q44, Q48, Q51, Q58, Q59, Q67, Q74 | Terms used without explanation (churn, elasticity, contribution, GMV, LTV, marginal CAC, CSAT, regression, soundbox, MECE, difference-in-differences, power/significance, runway, burn multiple) | One-clause plain-word glosses added at first use |
| Q11, Q16, Q20, Q38, Q42, Q45 | No blank line after the inline data table (the next text line would be read as a table row; Q20 especially) | Blank line inserted (data unchanged) |

## Verified without change (recomputed, all match)
Q2, Q6, Q9 to Q13, Q15 to Q19, Q21, Q23, Q26, Q27, Q30, Q31, Q33 to Q46, Q49 to Q57, Q60, Q62 to Q71, Q75, Q76. Examples of non-obvious checks: Q16 log shares (85.5%, -24.1%, 38.6%); Q53 tie churn 4.16% (stated about 4.2%) and 3% churn gives Rs 5,103; Q67 sample sizes 39,475 and about 3.79 million per group; Q68 values 13.2, 15.0, 15.6, 14.1, 11.7 lakh; Q60 series sums to 1,000; Q33 break-even utilisation 76.4%; Q23 break-even retention 36.7%.
Sanity checks and stated ranges follow from the stated assumptions in all the above; Q42 sanity check is a second route (payback and yearly return per rupee). Q26, Q51, Q54, Q56, Q68, Q69, Q71 are explicitly labelled assumed.

## Honesty and "Asked at"
- All "Asked at" lines are either "commonly asked (no company-specific report found)" plus prep-site/unverified qualifiers, or match Book07_Part06_sources.md and research/interview_processes.md (Mu Sigma, Fractal, Flipkart, Meesho, Swiggy, Tiger Analytics, PhonePe patterns). No change needed.
- No real statistic or company figure is stated as fact; all rupee figures are exercise inputs or labelled assumed. Benchmarks (LTV:CAC of 3, NRR above 100%, GRR in the 90s, NRR 115% "strong") are marked rule of thumb or unverified.

## Unresolved / report-only
- Ordering: no problems found.
- Overlap inside the part: Q11 and Q58 both reference the same "car manufacturer profit fell 40%" snippet; Q9, Q22 and Q39 share the food-delivery per-order contribution theme; Q14 and Q22 are near-identical diagnostic trees; Q31 (price-volume bridge) overlaps Q12/Q39 conceptually; Q61 and Q1 both teach the profit tree; Q75 and Q12/Q43 reuse break-even-uplift logic. Possible overlap with other Book 7 parts (unit economics, metrics) not checked against those files.
- Q10 follow-up "variable cost 400" and several other follow-up numbers were verified but kept as is.
- Q20 profit-per-visitor z (about 1.5) uses a simple Bernoulli variance approximation; a full test would use per-visitor data.
- Template note: Q51 to Q60 and Q68 use the case template without a separate "Explain simply" block, which fits the case type; no change.

## Claims left unverified
Real-world base figures were not fact-checked (no web access); none are asserted as facts. Prep-site, AmbitionBox and candidate-review mentions in "Asked at" rely on the sources file snippets and stay marked unverified.
