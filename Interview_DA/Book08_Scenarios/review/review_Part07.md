# Review: Book 8 Part 7 (Prioritisation and ethics scenarios)

## Counts
- Answers checked: 60 (all). Headings, numbers, stars, order and inline data untouched.
- Answers with figures recomputed by code (scratch C08_Part07/c.py, written before comparing): 14 (Q9, Q14, Q15 input arithmetic n/a, Q23, Q28, Q29, Q30, Q35, Q36, Q37, Q40, Q41, Q46, Q53). All figures matched the written results.
- Answers with wrong arithmetic: 0. Answers changed: 10 (wording, honesty, formatting, one added check).

## Verified by code (all correct)
ICE 192/360/135 (Q9); capacity 28 free hours, only 14+8+6 fits exactly of all 15 combinations (Q14); payback 6.67 weeks to 7, 156 and 136 hours, 80/3 = 26.7 (Q23); RICE 200/200/450, Z at 60% = 270, 2.25x (Q28); weighted 6.7/6.5/7.1 and alternate weights B 7.1, C 6.9, A 6.1 (Q29); INR 3,00,000 (Q30); +57.1%, +10.0%, -30.0% (Q35); 15% response (Q36); 50.0%, 11.1%, 12.5%, 18.2% (Q37); 40% vs 24%, ratio 0.60, gap 16 points, chi-square p 0.0153 plain, 0.0230 corrected, Fisher 0.0226 (Q40); accuracy 90%, recall 40%, precision 50% (Q41); 0.96% (0.97% on 1,238) (Q46); 25% drop (Q53).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q9 | "what you tell the loser" unclear, and not the stated pitfall | Reworded to "not telling the requester whose item waits" |
| Q14, Q28, Q29, Q37, Q9 | No blank line after the inline data table | Blank line added (data unchanged) |
| Q15 | Example figures (4,820, 40 records, 1%) not labelled | Added "(All figures here are illustrative.)" |
| Q29 | "I computed this by script" pasted into answer; A's sensitivity score missing | Removed script claim; added A 6.1 |
| Q36 | "head-office-weighted" wrongly suggested weighting had been done | Reworded to "mostly head-office responses", by group |
| Q40 | "checked by script"; p-value unexplained for a beginner | Replaced with plain explanation of the test and that p says nothing about cause |
| Q42 | Example 12%, 10-15% range unlabelled | Marked illustrative |
| Q46 | Equal totals (1,250 - 12 = 1,238) read as a good sign; could hide offsetting gaps | Added a two-direction person-by-person match check |
| Q50 | "likely unlawful" stated as legal fact | Softened to "possibly unlawful (confirm with legal)" |
| Q56 | Anonymised-data legal principle lacked the unverified label in the follow-up | Added "from memory, unverified" |

## Premise checks
- Q14: free 28 hours is correct; the unique exact fit is real, and the answer rightly says exact-fit is a puzzle, not policy.
- Q35: both growth figures are correct and the answer correctly says they answer different questions.
- Q40: ratio and percentage-point gap are stated correctly; four-fifths rule is labelled unverified and US-specific.
- Q46: premise handled (assumes one line per person); now also notes offsetting gaps.
- Q37: complementary disclosure (subtraction) correctly flagged.

## Legal and policy statements
All DPDP, GDPR, four-fifths, retention, breach-notification and purpose-limitation points are principle-only and labelled "from memory, unverified, confirm with legal" (Q5, Q6, Q16, Q20, Q21, Q30, Q37, Q38, Q39, Q40, Q45, Q48, Q49, Q51, Q56, Q57). Q22 and Q24 rule-of-thumb figures (RICE scales, 20-30% buffer) are labelled as convention or own rule.

## Style and template
- No em dashes in answer text (only the part title line). No code fences, no pasted scripts. Template fields present in all 60 (Asked at, interviewer check, Say this, Likely follow-ups, Common mistakes). "Asked at" claims follow the sources file: no company-specific claims, prep-site claims marked unverified.

## Unresolved / report only
- Ordering: stars descend and numbering is continuous (Q1-Q60); within-star difficulty order holds in my read (not checked mechanically beyond the headings).
- Count: sources file says 61 questions, part file has 60 (matches target 60); the sources note is stale.
- Overlap (report only): Q40 and Q58 (selection-rate ratio, deliberate cross-reference), Q17 and Q55, Q20 and Q56 (minimisation), Q43 versus Book 9 AI-tool-use topics likely overlap; Q41 (accuracy paradox) likely overlaps Book 5/9 classification metrics; Q23 payback may overlap Book 7. Not cross-checked against other parts.

## Claims left unverified
Real-world laws and practices (DPDP Act, GDPR, four-fifths rule, minimum cell size 5 or 10, breach-notification timelines, email recall behaviour, public AI tool retention) are stated only as labelled principles; no web access to verify.
