# Review: Book 8 Part 05 (Analysis-Approach Scenarios), Wave C

Scratch script: /tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C08_Part05/v.py

## Counts
- Answers checked: 101 of 101 (all read in full; structure, headers, honesty labels, style).
- Answers whose numbers were recomputed by code: 26 (Q13, Q14, Q24, Q25, Q30, Q33, Q34, Q35, Q47, Q51, Q52, Q56, Q57, Q64, Q67, Q69, Q70, Q71, Q72, Q74, Q75, Q77, Q78, Q89, Q96, and Q10 example). Q57 and Q67 were reconstructed with new data.
- Answers changed: 7 (Q34, Q47, Q57, Q64, Q67, Q80, Q92). No arithmetic result was wrong; changes are reproducibility, statistical method and honesty labels.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q57 | "Illustration with 16 orders: mean 61.8, median 43.5, p90 110" gave no data, so unreproducible (original script not preserved). | Added a 16-value list (exercise data) that reproduces mean 61.8, median 43.5, p90 110 (linear percentile) and 9 of 16 within 45 min. |
| Q67 | "12 resolved tickets: mean 3.9, median 3.0" gave no data. | Added a 12-value list (mean 3.92, median 3.0, p90 8.6) and stated them. |
| Q64 | 3 of 10 interval "about 2% to 58%" used the normal approximation, which is unreliable at n=10 (Wilson: 10.8% to 60.3%). Also "30% looks higher" was not tied to overlap. | Changed to about 11% to 60%, said ranges overlap; footnote now names Wilson method in plain words. 120 of 600 (17% to 23%) confirmed. |
| Q34 | Follow-up said 41.7 vs 45.0 "could be noise"; actual tests: Mar vs Jan p about 1e-6 (real), Mar vs Feb p about 0.14 (unclear). | Follow-up rewritten with both results. |
| Q47 | Follow-up "(66 x 75/66 needs 3.41%)" garbled. | Now "it needs 75 / 2,200 = 3.41%". |
| Q80 | "commonly 5 or more" stated as practice without label. | Labelled "from memory, unverified; confirm the policy". |
| Q92 | Excel row-capacity statement in follow-up lacked the unverified label (main text had it). | Added "(from memory, unverified)". |

## Figures confirmed unchanged (recomputed independently)
Q13 funnel (12/50/40%, 2.4%, losses 44,000 and 1,800); Q14 (15% vs 12%, 3.0 points, 25% relative, 95% range -1.0 to +7.0, p 0.13 pooled z-test); Q24 (mean 74.8, median 38); Q25 (22% of 1,000 = 220; margin 6.6 points); Q30 (break-even -10.7%); Q33 (YoY 20.0%, QoQ -8.6%, +11.1%, +5.0%, base-80 figures 12.5/25.0/31.3/20.0, total 391); Q34 (52.0/45.0/41.7, pooled 46.0%, 10.3 gap); Q35 (9.0% vs 12.5%, 3.5 points, relative 28%, chi-square p 0.17 uncorrected); Q47 (5.0%/3.0%, 75 vs 66); Q51 (elasticity -0.8, revenue +1.2%); Q52 (p 0.63, interval -0.46 to +0.76 points, -9% to +15% relative, about 336,000 per arm); Q56 (+8%, -10%, +20%); Q69 (15/8/3%, 6.27%, 2.4x, 31.9%, 13.3%); Q70 (62 days, shares 8.1/14.5/9.7/19.4/48.4); Q71 (30%, 50%, 34%, +85/day); Q72 (2.80% to 4.24%, standardised 2.68%); Q74 (1,080; 120; 200); Q75 (2,000 expected); Q77 (87.1% at least one false hit, 2 expected, 0.00125); Q78 (10.0/13.6/12.0%, 11.9% a month, 1.6-point fall); Q89 (1/0.7 = 1.43); Q96 (leaver mean 3.5, observed-time mean 8.6, survival 90/80/70/60%).

## Premise checks
Q14, Q35, Q47, Q69, Q71 premises correctly diagnosed (rates not counts; selection; percent vs points). Q70 correctly warns medians do not add. No flawed premise found in inline data.

## Template, style, ordering
- All 101 answers have Asked at, interviewer check, Say this, Likely follow-ups, Common mistakes. Structure blocks fit type (B for data questions, C for approach, E for concept).
- No em dashes in answers (one in part-title line, allowed); no code fences; no scripts pasted.
- Stars/difficulty ordering and Q1-Q101 numbering are correct and continuous.
- "Asked at" lines match research/Book08_Part05_sources.md (no company-specific claim; prep-site claims marked unverified).
- Privacy/legal items (Q58 DPDP, Q84 four-fifths, Q100) already carry "from memory, unverified / confirm with legal".

## Unresolved / report only
- Overlap within and across parts: Q8 and Q35 (training/onboarding evaluation), Q22 and Q85 (training effect), Q49 and Q88 (rating calibration), Q32/Q97/Q55/Q73 (selection bias), Q58/Q84 (hiring fairness). Likely overlap with Part 6 numeric drills and Book 5 (Simpson's paradox Q72, A/B Q52, median vs mean Q24); not compared line by line.
- Q74 applies 12% attrition to today's 1,000 base while headcount grows to 1,080 (illustration only; simplification not changed).
- Several answers have a blank line before "Clarify first" (cosmetic).

## Claims left unverified
Real-world statements remain from memory: Excel row limit (Q92), four-fifths rule (Q84), DPDP Act (Q58, Q80), typical minimum group sizes (Q80, Q81), prep-site/question-bank themes in "Asked at" (all marked unverified).
