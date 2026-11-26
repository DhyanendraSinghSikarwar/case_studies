# Review of Book07_Part01 (Wave C)

## Counts
- Answers checked: 32 (Q1-Q32). Answers whose numbers were recomputed by code: 32 (all numeric chains, ranges, sensitivities, Q26 simulation re-run independently).
- Answers changed: 21 (Q5, Q8, Q10, Q11, Q12, Q13, Q14, Q15, Q17, Q18, Q19, Q20, Q21, Q23, Q25, Q26, Q28, Q29, Q30, Q31, Q32), plus removal of "Answer (approach X)" meta-label lines in Q17-Q32.
- Answers with wrong arithmetic: 0. All written figures matched the recomputation (rounding only, e.g. 2.04% for the 100M rounding, 34.02M to 34M). Problems were consistency, reasoning, honesty and format.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q5 | "Factor of about 1.5" contradicted the 20-30% tolerance used later and in Q14 | Now "within about 1.3x (gap roughly 20-30%)" |
| Q8, Q10 | 140 crore / 4.5 = 31.1 crore, shown as "30 crore" while Q10/Q15 use 311 million | Table and Q10 now say about 31 crore, rounded to 30; blank lines added around the Q8 table |
| Q11 | "Second route" (200 wards x 2,500) reuses household size 4, so it is the same division, not independent | Relabelled as an arithmetic re-check; independent check named (outside housing/connection count) |
| Q12 | Sanity check promised a bottom-up check but did not do one | Reworded honestly as a reality check; true second route described |
| Q13 | 300 cups per stall conflicted with 400 in Q3 (same chai model) | Added cups-per-stall row at 400; check now 1.6M cups = 0.8 per person, consistent with Q3 |
| Q14 | "Within 20-30%" ignored that the gap is 33% of the lower figure | Stated 25% of higher, 33% of lower, at the edge of the convention |
| Q15 | Say-this said "too high", body said "plausible-to-slightly-high"; 5 crore claim not flagged as an input | Aligned wording; flagged as exercise input, real count unknown |
| Q17 | "10 orders per user over 6 million users" mixed all-app users with one app | Added the 25 per user figure for a 40%-share app (computed: 60M/2.4M) |
| Q18 | "Freshers leave faster" stated as fact | Marked as an assumption to test |
| Q19 | 140/8 = 17.5 shown as "about 17" | "17 to 18 crore (17.5)" |
| Q20 | Asked-at claimed prep sites list the same mistakes for named firms (not in sources); mini-example had no numbers | Claim narrowed to what sources support, list called a synthesis; example now 12 lakh a month = 40,000 a day |
| Q21 | Census-data certainty overstated | Softened to "usually easier to pin down (assumed)" |
| Q23 | "See the next question on correlation" pointed to Q24 (wrong) ; "20% off" vs sqrt(3) rule needs a stated meaning | Now points to Q26; says 20% is read as about one standard deviation, so range covers roughly two cases in three |
| Q25 | No blank line after table | Fixed |
| Q26 | "2.5 times too high" ambiguous; simulation claim ("13% with 12% bias") not reproducible | Reworded (2.5 times the true value, about 150% too high). Re-simulated 2M runs: independent errors give >2x in 0.08% (about 0.1%), 5th-95th percentile 0.63x-1.48x (both confirmed); one shared error gives 12%; each input leaning 12% high gives 26%. Text now states these two cases |
| Q28 | Claimed a 12% share of customers from a metro is "plausible" though it holds about 1.4% of people (20M of 1,400M) | Rewritten: plausible only if delivery is very concentrated, else a clue the 30% share is too high |
| Q29 | 8,300 riders is average-based and peak needs 7,500 on duty at once | Added note that the average figure is a floor and fleet must cover peak |
| Q30, Q32 | Missing blank lines after tables | Fixed |
| Q31 | "Mu Sigma guide suggests about 3 weeks of prep" not in the sources file | Replaced with "author's suggestion; no source for prep duration" |
| Q32 | "Heavy user a few a day, average a few times a week" did not support 1 per user per day; revision looked tuned to the hint | Reasoning fixed (average about 1 per user per day as a guess), states change is justified by reasoning not only the match; range tied to 0.8-1.4 per day (computed 0.4-0.7B) |
| Q17-Q32 | Stray "Answer (approach A/B/D...)" template labels | Removed (16 lines) |

## Checks passed without change
Arithmetic in Q1-Q4, Q9, Q16, Q21 (apart from wording), Q22, Q24, Q25, Q27; asked-at lines for Q1, Q6, Q30 match the sources file; no em dashes in answers (only the part-title line); no code fences; no scripts pasted.

## Unresolved / report only
- Ordering: part follows star then difficulty order; Q17 (3 stars, red) sits after the 3-star yellows as the rules require. Q26 (2 stars, red) and Q32 (1 star, red) are consistent. No numbering issue found.
- Overlap: Q12/Q17/Q28 reuse the delivery-app-in-a-metro model (30% usage, 3 orders a month, 40% share); Q14/Q3/Q13 reuse the chai model. Assumptions are now consistent within the part; Parts 2-3 (market sizes) likely re-estimate food delivery and chai and should reuse the same inputs. Q31 cheat sheet overlaps Q8.
- Q12 national funnel (3.4 crore potential users) and Q17 metro model (6M users in one 2-crore metro) are not reconciled with each other; left as separate illustrations.
- Q7 says "four clarifications" in its practice step but lists five bullets (minor, left).

## Claims left unverified
All population, household, urban share, UPI, car, delivery-company and price figures are labelled assumed/approximate/unverified; none was checked (no web access). "Asked at" lines rely on the sources file only (prep-site and candidate reports, unverified). Fermi/piano-tuner attribution in Q27 is general knowledge, not sourced.
