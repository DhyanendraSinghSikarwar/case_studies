# Book 1 Part 13 review (Statistics I, 61 Qs)

Code: 60 python blocks (Q18 has none, conceptual by design). All 60 extracted and run standalone: 60 pass, 0 fail. Printed numbers match quoted numbers in all cases (Q34, Q37, Q39 re-run after cosmetic edits: match). No ANSWER_PENDING; all Qs have the full template.

Fixes (factual/clarity)
- Header: added Stars line (20/27/14); Actual 61 correct. No stale dedupe note present.
- Q41: "same d = 0.1 gives p = 0.31 at n = 50" was misleading (p = 0.31 came from observed d = 0.204 by chance); reworded to true effect vs the single run.
- Q53: removed claim that sklearn GLM summaries report observed-information SEs (statsmodels only).
- Q60: "variance is infinite" -> mean undefined, no finite variance (sample variance never settles).
- Q58: BH/PRDS wording: the proof covers one-sided p-values; two-sided with positive correlation is fine in simulation but not strictly covered.
- Q15: labelled p = 0.048 vs 0.0074 as one seeded run, not a general rule (verified numbers).
- Q47: re-ran with 1,500 sims: no-effect Welch .043 / MW .055 / log1p .051; real lift Welch .42, MW .044, log1p .113. Text now says ~36-42% Welch, ~5% MW; conclusion unchanged.
- Q56: re-ran with 600 sims: coverage percentile .56, BCa .66 (text .57/.63 at 150 runs); under-coverage claim holds, text now gives the range.

Checked and OK (no change): Q12 (14,745 vs 14,749), Q13, Q36 coverage, Q37 tolerance (Howe), Q38, Q39 (z=2.09, p=0.0366, n~89,866), Q45 Welch matches scipy to 5 dp, Q54 delta vs bootstrap, Q59 TOST, Q61 deff.

Unresolved / not verified
- Q18 has no code or numbers (conceptual); left as is.
- Illustrative simulation numbers are seed-dependent; the Q47/Q56 power/coverage ones are noisy at the quoted run counts (noted in text).
- No web citations needed; none were added.
