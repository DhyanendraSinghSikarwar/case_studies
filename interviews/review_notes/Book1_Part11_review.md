# Book 1 Part 11 review (ML system design, 52 Qs)

Header: 18 x 3-star (Q1-18), 24 x 2-star (Q19-42), 10 x 1-star (Q43-52) = 52. Header has no star line; removed stale "star counts may be stale" remark from dedupe note.
No ANSWER_PENDING; all Qs have the template sections; the 8-step ladder is followed.

## Fixes
- Q21: example was wrong (1.6x does not balance 3x demand with elasticity -1.5; 3*m^-1.5=1.2 gives m=1.84). Corrected, labelled illustrative.
- Q38: RBI line said "data localisation ... (DPDP Act)" (inaccurate attribution); reworded to RBI digital-lending directions + DPDP consent/purpose. EU AI Act: added "phased/under revision, check current timelines". GDPR line (Art. 22 style) already hedged with "check current text".
- Q49: IPS printed 0.0306, text/comment said 0.0307; fixed both (SNIPS 0.0306, true 0.0312, logged CTR 0.0363 verified).
- Illustrative labels added: Q4, Q8, Q18 (AUC figures), Q21, Q22, Q25, Q9. Q10 and Q48 were already labelled.
- Header dedupe note cleaned.

## Code (10 blocks, run standalone with Windows python, not -I because packages are user-site)
All 10 passed; outputs match text: Q15 (cnt 2 / amt 290), Q16 PSI 0.0004/0.235, Q18 572/354/True, Q20 6944/20833/2083/100/36.5, Q36 [104 163 4733] 0.072, Q41 6.13/8.46, Q42 reconciliation sums = [14,31,9], Q48 0.0498/0.0384/0.0485, Q49 (after fix), Q52 0.3/33.7.
Arithmetic hand-checked: Q2 break-even 12.5%, Q8 Rs 50L/30L, Q11 eCPM 200 vs 100 and downsampling recalibration formula.

## Unverified / unresolved
- EU AI Act application dates and RBI circular specifics not web-verified; wording deliberately generic.
- Q16 PSI 0.1/0.25 thresholds are an industry rule of thumb (stated as such).
