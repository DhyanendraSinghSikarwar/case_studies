# Review: Book 7 Part 3 (Revenue & Operations Guesstimates)

Reviewer: Wave C. File: Book07_Part03.md. Script: scratchpad/C07_Part03/check.py (all 72 answers recomputed from inline data and stated assumptions).

## Counts
- Answers checked: 72. Answers recomputed by code: 72 (Q5 and Q27/Q29/Q43/Q45 concept answers: only their mini-example numbers).
- Answers with a numeric or consistency error fixed: 17 (Q3, Q12, Q28, Q31, Q34, Q38, Q41, Q43, Q57, Q59, Q61, Q64, Q69, plus Q53, Q60, Q71, Q11 for weak or inconsistent sanity checks).
- Answers touched in total (incl. honesty, jargon, style): 38.
- Template headers (Asked at, checking, Say this, Follow-ups, Mistakes): 72 of 72 present. No em dashes in answers (1 in the part title, allowed). No code fences, no scripts.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q3 | Say-this range 270k-450k disagreed with sensitivity (240k-480k); Result had no range | Range set to 240k-480k in both |
| Q11 | Sanity cited "rates seen in sale news" as fact | Reworded to the Q16 exercise figure, marked assumed |
| Q12 | Said 250,000 is 45-50% of Q19's market; Q19 gives 417,000, so 60%. Sanity check was circular | Share corrected to 60%; new second-route check (250,000 / 17 orders per rider = 14,700); roster explained |
| Q13 | 16-hour opening and the 12 off-peak hours were unstated | Marked as an assumption |
| Q17, Q54 | Asserted real take rates are "usually lower" / "high for such platforms" | Reworded as exercise input to be checked |
| Q28 | Sensitivity: 30% occupancy gave "9.6 lakh"; correct is 10.1 lakh. Typo "A 8-screen" | Fixed both |
| Q31 | Range 2.7-6.9 lakh wrong (10% gives 3.1, 20% gives 6.1). Sanity check mixed 40% and 80% online share, hid a 2x gap | Sensitivity fixed; honest bottom-up (0.9M tickets vs 0.46M), range 3-9 lakh; PNR explained |
| Q34 | Check "600,001 rides" (actually about 600,006) | "about 600,000" |
| Q38 | Range top 1,900 not reproducible (combined case gives 1,800) | 1,800 |
| Q40 | "Large metro airport" 80,000 passengers vs Q18's 150,000 for same label | Reason reworded, cross-referenced |
| Q41 | Result range 6-27 lakh contradicted sensitivity 5-22 lakh (computed 5.4-21.6) | 5-22 lakh |
| Q43 | Arithmetic error: 1.4 bn x 1% x 1/7 = 2 million, not 0.2 million | Chain rebuilt on 140 million served-city people (=0.2M); 3% x 3 orders = 9x example |
| Q50 | "Real load factors are about 80-90%" stated as fact | Marked as assumption |
| Q53 | Sanity check restated the same sum; day uplift "22%" is 22.5% | Added weighted-multiplier route (1.45); 367,500 and 22.5% |
| Q55 | "typical size for a sale" stated as fact; page-view ratio unmarked | Marked plausible/assumed |
| Q57 | Sensitivity 400,000 is really 420,000; sanity check vague; "registered 2-3x active" stated as fact | Fixed; new check (17 orders per distinct rider; 1 per 385 people); marked assumed |
| Q59 | Say-this "both give about 5,000" but routes give 7,500 and 4,500; Result range inconsistent | Say-this, Result and step 3 aligned on 6,000 (4,500-7,500) |
| Q60 | Say-this implied independent agreement; inputs were chosen to match | Caveat added |
| Q61 | Ads 140 crore did not match Q52's 153 crore; "high versus real network revenue" is an unverified claim | Used 153 crore (0.42/day, total 19.7 crore); claim marked unverified |
| Q64 | 60% peak utilisation gives 346, not 360; "believable for cloud kitchens" as fact | About 350; marked assumed |
| Q69 | 10 days of stock halves area to 13,300 m2, not 15,000 | Fixed |
| Q70 | "Analytics about 4-5% of corporate staff" unverified ratio | Replaced by ask-for-headcount |
| Q71 | Sanity divided all 50M by merchants (9.6), mixing person-to-person | Merchant payments only: 7.2 |
| Q1, Q9, Q10, Q12, Q20, Q31, Q44, Q57, Q62 | Jargon at first use (bottom-up, dark store, GMV, take rate, roster, UPI, PNR, tornado chart, multi-apping, DC/AC) | Short plain-word glosses |
| 40 answers | No blank line after the assumptions table (renders the next line as a table row) | Blank line inserted (mechanical edit) |

## Verified correct without change (recomputed)
Q1, Q2, Q4-Q10, Q14-Q16, Q18-Q27, Q29, Q30, Q32, Q33, Q35-Q37, Q39, Q42, Q44-Q52, Q56, Q58, Q63, Q65-Q68, Q72.

## Unresolved / report only
- Ordering: stars descending and difficulty ascending within star are correct; numbering continuous Q1-Q72 (target 70, actual 72).
- Overlap: Q32 and Q63 (same weekly-off plus absence roster maths); Q17 and Q54 (GMV to net revenue chain); Q9 and Q22 (dark store sizing); Q18 and Q40 (airport cabs); Q3, Q34, Q47 (ride-hailing); Q15, Q21, Q23 (Swiggy 2 million). Likely deliberate variants; consider merging Q32/Q63 elsewhere.
- Cross-question assumptions differ (Swiggy orders 1.6M in Q1, 2M in Q15/Q21, 1.8M platform in Q60; metro riders 2.5M in Q7 given vs 5M in Q2/Q52/Q59/Q61; rider orders per day 17 in Q8, 12 in Q57). Each is labelled as its own assumption; left as is.
- Q56 gives net revenue 24% of GMV, flagged in-answer as the number to challenge.

## Claims left unverified
All real-world base numbers (populations, UPI users, rail trains/seats, restaurants, fares, prices) are labelled assumed/unverified; none was checked (no web access). "Asked at" lines match research/Book07_Part03_sources.md (all prep-site or candidate claims marked unverified); no company-specific claim added.
