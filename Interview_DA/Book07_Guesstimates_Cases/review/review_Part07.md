# Review: Book07_Part07 (Product Analytics Cases: Feature Launch, Funnel Drop)

## Counts
- Answers checked: 71 (all). Template fields (Asked at, checker, Say this, follow-ups, mistakes): 71/71 present.
- Answers whose numbers were recomputed by code (scratch script, independent of the written results): 53 (every answer containing arithmetic: Q3-Q4, Q9-Q19, Q23-Q25, Q28, Q31-Q39, Q41-Q55, Q58, Q61-Q64, Q66, Q68, Q70, plus Q47-Q48). The remaining 18 are pure concept answers with no figures beyond illustrative ones, which were checked by hand.
- Answers with wrong numbers: 2 (Q16, Q40). Answers edited in total: 22 (numbers 2; honesty/hedging 4; beginner clarity 14; sanity-check 1; some overlap).
- Arithmetic confirmed correct (no change needed): Q4, Q10-Q12, Q15, Q17-Q19, Q24-Q25, Q31, Q33-Q36, Q38, Q41-Q45, Q47-Q48, Q51, Q53-Q55 (month-by-month compounding table re-run: +42,300, +10,570, -3,596, cumulative -10,474 in month 7, about -350,000 in month 12), Q58, Q61 (log split 38.7% / 61.3%), Q62-Q64, Q66, Q68, Q70 (net Rs 39.43 lakh vs 39.69 lakh, +0.65%; refund 3.5% gives 38.85 lakh, below control), Q63 (chi-square 22.84, p = 1.8e-6).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q16 | Sample size per arm stated "about 68,000"; recomputed 69,379 (95% confidence, 80% power) | Changed to about 69,000, stated confidence and power, said 50,000 per arm is underpowered; explained z-test and power in plain words |
| Q40 | Sample size "about 6,300" per group; recomputed 6,509 | Changed to about 6,500 |
| Q37 | "62% relative rise" (13/8 = 62.5%); causal wording "comes from 5-star turning into 1-star" overstated from shares alone | 62.5%; reworded to "shares suggest" |
| Q39 | Overclaimed that existing users are coming more often and the streak made the app stickier | Hedged ("look to be", "may be"); DAU/MAU defined |
| Q47 | Sanity check just restated the chain (not a second route) | Added scale reality check vs an assumed (unverified) 3 orders per user per month base, about +3% |
| Q15 | Blended 1.95 vs 2.1 silently assumes old-version group is typical | Stated the assumption in step 2 |
| Q17 | 8,000 "moved" orders presented as fact; "contribution margin" unexplained | Added "if the whole standard-tab loss is moved orders"; defined cannibalisation and contribution margin |
| Q44 | "7.5 times their share" ambiguous | Reworded to "7.5 times the average user's revenue" |
| Q28 | "Asked at" cited Dataford for HEART; sources file does not support that | Kept TryExponent (metric questions), noted HEART not found in sources |
| Q61 | Log-share split not explained for a non-technical reader | One-line plain explanation added |
| Q9, Q13, Q20, Q22, Q35, Q41, Q43, Q46, Q59, Q64, Q70, Q10 | Unexplained terms: mix shift, difference-in-differences gap, contamination, pre-register, KYC, OTP, D1/D7/D30, DAU, p95 latency, kill-switch, NPS, contribution, COD | Short plain-word explanations added at first use (Q10: "COD-averse" replaced) |
| Q40 | "SRM" used without explanation | Defined sample ratio mismatch |

## Checked, no change needed
- No em dashes in answer text (only the part-title line); no code fences; tables are followed by the header lines; headings, numbers, stars, order and inline data untouched.
- Q66 already flags the mixed "orders per user" vs "conversion" wording of the question and solves the percentage-point version; Q55 and Q70 inputs are labelled made up; Q47 inputs are given in the question.
- "Asked at" lines are otherwise consistent with research/Book07_Part07_sources.md and research/interview_processes.md (prep-site claims marked unverified; Q3/Q14/Q27 internal-research mentions of PhonePe/Fractal rest on a guide, kept as unverified).

## Unresolved / report only
- Ordering: stars/difficulty order is monotone (3-star green, yellow, red; then 2-star; then 1-star). No numbering problems found (Q1-Q71 continuous).
- Overlap: Q10 and Q18 (payment success decomposition) and Q71 (UPI drop) overlap in method; Q13/Q44/Q45 (selection bias), Q21/Q42 (novelty effect) and Q51/Q5 (validate the metric first) overlap within the part. Q63 (SRM) and Q16 (A/B readout) likely overlap with Book 5 A/B-test answers; Q58/Q5/Q6 overlap with generic metric-drop cases in Part 5. Not changed, per instructions.
- Q54: the answer says "do not ship" on revenue per visitor alone; reasonable but margin could change it (already in caveats).

## Left unverified
- All "asked at" claims remain community or prep-site level; no company-specific candidate report was verified.
- Real-world base numbers: the part uses only question-given or labelled made-up figures (the 3 orders per user in the new Q47 check is labelled assumed, unverified).
