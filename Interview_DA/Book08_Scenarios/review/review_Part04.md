# Review of Book08_Part04.md (Wave C)

## Counts
- Answers checked: 80 (all read in full against the checks).
- Answers with data or figures recomputed by code from the inline data, without reading the written result first: 54 (Q4-Q7, Q10-Q18, Q23-Q27, Q31-Q56, Q59-Q63, Q75-Q76, Q79; scripts in the scratchpad C08_Part04). The other 26 are approach, ethics or communication answers with no figures to recompute.
- Answers with a wrong figure or statement fixed: 2 (Q34, Q54).
- Answers changed for clarity, honesty or style: 6 more (Q11, Q14, Q25, Q49, Q60, and table spacing in 8 answers).
- All other recomputed figures matched exactly (including Q15 z = -2.47 and population z = -2.65, Q25 Fisher p = 0.0486, Q43 z = 12.65, Q49 margins 6.5 and 20.3, Q50 z = 1.56, Q60 margins 6.5 and 11.3, Q48 revenue 23,77,950 and break-even churn 20.1%).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q54 | Working step 4 said X adds 2.75 points and the rest of the rise is 0.34 points; 2.75 + 0.34 = 3.09, not the 3.0-point jump. Two different bases were mixed. | Rewrote step 4: removing X cuts the rate from 5.00% to 2.34%, so X explains about 2.66 of the 3.0 points; other products sit 0.34 points above the old 2.0%. |
| Q34 | Caveat said late-evening IST orders shift between days under a UTC-date cut. Wrong: the orders that move are the early-morning IST orders (00:00 to 05:30 IST); month-end direction was also reversed; "last 5.5 hours of the IST day missing" was wrong. | Rewrote the caveat with the correct window and month-end direction (early 1 April IST orders land in March). Also tagged the "IST has no daylight saving" claim as from memory, unverified. |
| Q14 | Follow-up called 6.8% monthly attrition "high" and "annualised" as a general fact. | Reworded to compare against Support's own 2.8% and company history; no crisis call from one month. |
| Q25 | "Fisher exact test" and "p" used without explanation for an HR beginner. | Added a one-clause plain explanation of both. |
| Q49 | NPS promoter/detractor not defined. | Defined at first use (9-10 and 0-6 scale, from -100 to +100; standard NPS definition). |
| Q60 | eNPS not expanded or explained. | Added "employee Net Promoter Score" and what it measures. |
| Q11 | Simpson's paradox named in "Asked at" only, never explained. | Added a one-line plain definition in "What the data shows". |
| Q10, Q11, Q13, Q14, Q17, Q24, Q27, Q40 | No blank line after the inline table, so the following header line would be swallowed into the table in rendering (Q27 also its trailing data sentence). | Inserted a blank line after each table (no text or data changed). |

## Premise and ambiguity checks (all correct)
- Q6 (partial vs full month), Q18 (mix dilution), Q33 (duplicate rows), Q41, Q42, Q56 (mix effects), Q31 (month length), Q35 (net vs gross), Q47 (denominator), Q50 (bots), Q63 (currency) are diagnosed correctly and the stated assumptions are explicit.
- Q27 and Q11 give identical numbers under the stated conventions (decomposition order is flagged in both).
- Q60 gives no eNPS values; the answer correctly limits itself to margins and non-response bias.
- Q79 premise (survivorship usually flatters, here creates a false decline) is acknowledged by the writer; the numbers (survivor 10 vs 8, per sign-up 4.0 vs 4.8) are correct.

## Honesty and template checks
- "Asked at" lines claim only what the sources file supports (question banks marked unverified; "commonly asked (no company-specific report found)" otherwise). Q10 names Meesho and MakeMyTrip only as Dataford prompts, unverified; acceptable.
- Invented numbers are labelled exercise or illustrative (Q5, Q59, Q61, Q75, Q76, Q79). Law and privacy points (Q59 consent, Q73 privacy) are deferred to legal/HR policy. Q26 PF/ESI rates flagged from memory.
- Header lines, structure block, follow-ups and common mistakes present in all 80. No em dashes in answer text (only the part title line); no code fences; no scripts pasted.

## Unresolved items (report only)
- Duplicate/overlap: Q11 and Q27 are the same data and method (Q27 adds the explicit weights convention and the "who acts" angle). Q17 vs Q10 step 3 overlap on payment success. Q20 and Q64 overlap on metric tree vs monitoring. Q60/Q49 are similar small-sample survey items. Keep or merge at the editor's discretion.
- Ordering: star order is 3 stars (Q1-Q30), then 2 stars (Q31-Q64), then 1 star (Q65-Q80); within groups difficulty is mostly ascending, but Q31-Q36 (green) follow yellow Q30 items, and Q27-Q30 (red) sit inside the 3-star block. Q13 wording "26 units of revenue" is awkward but inline data states INR lakh; heading not changed.
- Q62 multiplicative price estimate (5.7%) compares A with B; the additive and multiplicative versions differ slightly and the answer says so.

## Claims left unverified
- All real-world statements (question-bank attributions, "late data and definition changes are common", NPS category cut-offs, IST having no DST, PF/ESI contributions) are from memory or source snippets and are labelled as such or are standard definitions; no web access to confirm.
