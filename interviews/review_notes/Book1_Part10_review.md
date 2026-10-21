# Book 1 Part 10 review (A/B testing, causal inference)

Questions reviewed: 56 (all complete, no ANSWER_PENDING). CRLF preserved.

## Code
- 24 python blocks extracted and run standalone (scratch: %TEMP%\claude\rev_p10): 24 pass, 0 fail. All printed numbers match the numbers quoted in the text (Q5, Q6, Q7 0.217 ("about 0.22"), Q9, Q10, Q14, Q20, Q21, Q25, Q26, Q27, Q28, Q30, Q31, Q32, Q34, Q41, Q47, Q48, Q49, Q52, Q53, Q54, Q56).
- Added a 25th block (Q50 interleaving simulation), run: A/B power 0.26, interleaving power 0.993 (300 sims, seed 0).

## Fixes
- Q50: the "9% vs 73%" figure came from an unshown simulation and could not be reproduced under the stated setup. Replaced with a shown, run simulation (26% vs 99%), labelled toy, with assumptions stated.
- Q21, Q27: added missing Example field (Q27 numbers taken from the run code output).
- Q22: verified 3.5x arithmetic ((2.50+0.84)^2/(1.96+0.84)^2 = 1.42 per arm x 2.5 arms = 3.55); corrected "40%" to "42%", added the working and "two-sided".
- Q6: added the counts behind the 1.6% gap (clarity).
- Q8, Q23, Q24, Q40, Q44: labelled example numbers illustrative/hypothetical.
- Header: 1-star count 12 -> 10 (counted 19/27/10 = 56); removed stale star-count remark from the dedupe note.

## Checked, no change needed
- Q10 Simpson table (all rates and pooled 14.0% vs 24.7% correct), Q25 whale example (raw +30.5, p 0.078; capped 0.40), Q27 delta-method formula and numbers, Q43 iROAS arithmetic (1.6), Q41 (2,200 baseline, 84% share), Q35 ATE 0.33, Q7 14-look peeking ~22%.

## Unresolved / not verified
- No external citations in this part to verify (no web lookups needed). Conceptual claims (Dunnett, sqrt(k) control allocation, F>10 rule of thumb, SMD<0.1) are standard but not web-checked.
