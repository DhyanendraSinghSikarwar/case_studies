# Review of Book 13 Part 8 (critical reasoning), Wave C

Scratch: scratchpad/C13_Part08/v.py (all numeric and logic items recomputed; seed-fixed simulation for Q59).

## Counts
- Answers checked: 62 of 62.
- Re-solved independently by code: 38 (every numeric, rate, mix-effect, Simpson, p-value and fallacy-form item: Q6, 9, 10, 21, 24, 26-29, 32, 33, 39, 41-44, 47, 48, 49, 52, 53, 55-57, 59-61 and their follow-ups). The remaining 24 are judgement items (assumption, strengthen, weaken, flaw, definitions); there is nothing to compute, so I judged each option by hand against the argument's own link.
- Answers wrong (final letter or headline number): 0. Intended best answer confirmed for every MCQ.
- Non-unique or changed answers: 0. Fixes were to supporting numbers and wording only (6 items below).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 24 | "A rose 50%, B 30%, so on a rate basis A declined more" treated a rise in complaint count as a rate; the Explain bullet said the size fact was not needed, which contradicted the choice of (a). | Reworded the Say-this line to per-customer rises (A +5/N, B +3/N); replaced the bullet with a note that count growth is not a per-customer rate; updated the Check line (also the 2x follow-up: B +15/N vs A +5/N). Answer (a) unchanged and confirmed. |
| 44 | Upper bound "if all non-responders were satisfied, 98%" is wrong. | Corrected to (40 + 1,950) / 2,000 = 99.5% (lower bound 2% was right). |
| 48 | Worked example "9 people at 10 and 1 at 10 ... replace a 10" was garbled. | Rewrote: 10 people paid 10; one leaves, a new hire at 100 joins; average (9 x 10 + 100) / 10 = 19. |
| 55 | Step 4 said family 2 hired "50%" overall; actual is 46 of 100 (46%). 50% is only the women's rate. | Changed to "72 of 100 hired in family 1, 46 of 100 in family 2". Answer (b) confirmed. |
| 59 | "a simulation I ran, assumed numbers" gave no parameters, so not reproducible. | Re-ran: ability SD 8 and noise SD 8 reproduce 50.1 and 60.1; parameters now stated in the text. |
| 24, 59 | Wording only (see above). | n/a |

## Verified unchanged
Q6 (300, 90), Q9 (-5 points, -25%, +33.3%), Q10 (+6 vs +500, 98.8%), Q21, Q26 (166.7 s; 70+30+50+17), Q27 (96), Q28 (2.0, 1.0526, axis 94 gives 6), Q29, Q32 table (39% vs 72%), Q33 (3.52), Q39 (t-test p = 0.1158; 400 x p = 46.3), Q41-Q42, Q47, Q52 (trend predicts 26, 25), Q53, Q56 (15.4%, 47.6%, 81.8%), Q57 (76, 66, 78), Q60 (Fisher p = 0.8299; chi-square uncorrected 0.666; 5,000 each p = 0.195; 50,000 each p = 1.8e-5), Q61 (95%, 63%). Q49 enumeration over 3-element models: affirming-consequent form and (d) have counterexamples; (b) and (c) forms have none.

## Conventions, honesty, style
- "Asked at" lines only cite prep-site claims as unverified or "commonly asked"; no company claim beyond the sources file. Q26 time split is labelled "our suggestion". Q31 ranking is labelled "our ranking".
- No em or en dashes in answers (title line only). No code fences. Template: concept items (Q1-4, 12, 25, 30-34, 58, 59) use the concept variant; MCQs have Answer, steps, Check, follow-ups, traps. Q56-Q62 have a blank line after the heading (cosmetic, left).

## Unresolved / report only
- Overlap: Book 6 Part 7 Q57 (pay-hike attrition weaken) and Q45 ("only data analysts attend ... so Priya is one") touch the same themes as Q5/Q18/Q23 and Q49; none is a near copy. Q49 uses the same fallacy family as Book 6 Q45 with a different form.
- Q1-Q23 judgement-item options like Q8(b) "(ii) and (iv)" depend on the reader accepting "make" and "because of" as causal; stated in the answer.
- Header says target 60, actual 62; ordering of stars (3, 2, 1) is by design, not an error.

## Left unverified
Prep-site claims (Accenture 18 questions in 50 minutes, Magoosh "most common weaken type", Wipro/Infosys/TCS topic lists) are as reported in the sources file and not checked. Nothing could be run against Excel or other tools in this part.
