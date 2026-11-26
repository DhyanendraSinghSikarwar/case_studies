# review_Book07.md — Book 7 (Guesstimates, Case Studies & Business Metrics) review summary (Wave C, plan.md Section 8.6)

Date: 2026-11-12. One reviewer per part (9 parts) recomputed every number in every answer by code (guesstimate chains, ranges, sensitivities, metric formulas, case arithmetic, z/chi-square/DiD/sample-size figures, lakh/crore conversions) WITHOUT looking at the written results first, compared with the answers, fixed errors in place and wrote `review/review_PartNN.md` (per-fix detail there). Two reviewers (Parts 2 and 3) were interrupted by a usage limit and resumed after the reset. Reviewer counts are the reviewers' own and approximate.

## Pass criteria (plan.md 8.6)
| Check | Result |
|---|---|
| Completeness | 633 of 633 answered; 0 `ANSWER_PENDING` (script check) |
| Count | 633 vs target 600 (met) |
| Ordering / numbering | Continuous Q1..Qn in all 9 parts (script check) |
| Template fields | Asked at, interviewer check, Say this, follow-ups, common mistakes present in all 633 (script check) |
| Markdown / style | Code fences balanced; no em dashes in answers (script check); blank lines added after inline data tables where missing |
| Accuracy | Every number recomputed by code; real arithmetic errors found and fixed (below) |

## Per part
| Part | Answers | Answers edited | Main fix types |
|---|---|---|---|
| 1 | 32 | 21 | consistency (Q13 400 cups/stall, 140 crore / 4.5 = 31 crore), non-independent sanity checks relabelled, Q26 simulation re-run (12% shared error, 26% joint bias), unsupported claims removed |
| 2 | 94 | ~40 | arithmetic errors (Q25, Q37, Q47, Q51, Q76, Q79, Q92 lakh/crore slip), cross-answer consistency (Q40, Q42, Q50, Q58, Q59, Q62, Q71, Q74, Q75, Q89, Q90 now reuse earlier assumptions), invented source claim removed (Q61) |
| 3 | 72 | 38 (17 numeric/consistency errors) | wrong chains and sensitivity ranges (Q43, Q31, Q41, Q69, Q28, Q57, Q64, Q12), circular sanity checks strengthened, 40 table blank lines |
| 4 | 87 | 27 | 6 wrong figures or statements (Q34, Q38, Q41, Q58 45 days, Q60 43% rise, Q85), asked-at claims narrowed, jargon explained |
| 5 | 91 | 26 (16 content) | Q86 reasoning wrong, Q75 timezone example, Q30 mixed bases, Q52 range derivation, Q45 -17.5 SD |
| 6 | 76 | ~20 | wrong figures Q3 (margin of safety), Q7 inverted rule, Q32 (contribution Rs 6,000, break-even 2,667), Q47 two readings; Q20 conclusion changed (B unproven, extend test) |
| 7 | 71 | ~22 | Q16 sample size 69,000 and underpowered, Q40 6,500, Q37 62.5%, Q47 independent sanity check, unsupported Dataford claim removed |
| 8 | 57 | 11 | Q34 accuracy 1,770 not 1,850, Q14 wrong stage, Q24 overstated claim, definitions added |
| 9 | 53 | 17 | Q15 time split sums to 5 hours, Q3 scoring, personal-experience answers flagged as templates, asked-at narrowed |

## Known limits (not fixed; honest status)
- **All real-world base numbers** (populations, households, vehicles, prices, wages, usage, company volumes) are exercise assumptions labelled "assumed, approximate, unverified"; no web verification was possible. Reviewers removed or hedged claims that read as facts. Numbers given in question text are exercise inputs.
- **Assumption consistency:** reviewers aligned many cross-answer assumptions (Part 2), but some variation remains by design or scope: household size 4 vs 4.5, Swiggy order volume (1.6M in Part 3 Q1, 2M in Q15/Q21, 1.8M in Q60), metro riders (2.5M in Part 3 Q7 vs 5M elsewhere). Part 1 Q12 national funnel and Q17 metro model are not reconciled.
- **Sources:** "Asked at" claims rest on search-snippet prep-site and candidate reports and stay marked unverified; no first-hand company reports were found for most case types; stars are judgement.
- **Overlap:** many deliberate overlaps inside parts (chai example, Tuesday case, mix-shift/DiD ideas, four-fifths rule) and with other books (A/B-test arithmetic with Book 5, metric-drop cases between Parts 5 and 7, attrition metrics between Parts 4 and 8); kept and cross-referenced.
- Part headers: target vs actual counts differ (all parts meet or exceed targets).
- Personal-experience answers (Part 9) are templates; the candidate must replace them with true experience.
- A human read-through by a non-technical reader is still advisable.
