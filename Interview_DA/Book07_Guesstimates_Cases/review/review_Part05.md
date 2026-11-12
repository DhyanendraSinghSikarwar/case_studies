# Review: Book07 Part05 (Root-Cause Cases, Q1-Q91)

## Counts
- Answers checked: 91 of 91 (all read in full; every header line, template block and follow-up/mistakes line present: 91 each of Asked at, interviewer check, Say this, Likely follow-ups, Common mistakes).
- Answers whose numbers were recomputed by code: 70 (every answer with arithmetic; the remaining 21 are pure method/concept answers with no figures beyond a count of steps). Script: scratchpad C07_Part05/v.py, written from the question data and stated assumptions.
- Answers with wrong arithmetic: 0 material errors; 1 rounding/precision slip (Q45).
- Answers changed: 20 (Q8, Q9, Q20, Q30, Q33, Q40, Q43, Q45, Q52, Q57, Q58, Q64, Q75, Q79, Q81, Q86, plus table spacing in Q13, Q14, Q24, Q25, Q26, Q42, Q43, Q44, Q48, Q62, Q63).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q86 | Reasoning error: said the naive -20% overstates "because the baseline was rising", but the synthetic control predicts 95 (below 100), i.e. the baseline was drifting down | Reworded: without the event the series was expected to slip to 95 |
| Q75 | Worked example claimed a UTC cut makes Tuesday 8% lower; a pure 5.5-hour shift moves orders between neighbouring days and nets to roughly zero | Rewrote with assumed numbers (Tuesday early hours 8% vs Wednesday 3%), net -5%, and stated that a pure shift only moves orders between days |
| Q30 | Illustrative numbers mixed group base and total base (control fell "500 on a 10,000 base" while total is 10,000); "common or competitor 25%" blurred competitor with baseline | Reframed as scaled-to-whole-business baseline; competitor needs its own exposure group; regression and SKU glossed |
| Q52 | Range "-15% to -26%" had no derivation | Range now derived: if an assumed 40% of blocked shoppers buy another in-stock phone, 26.3% x 0.6 = about -16% |
| Q45 | "about -17 SDs" for population SD; exact value is -17.5 | Corrected to -17.5 and noted divide by 8 vs 7 |
| Q33 | Overstated causal claim: "discounts cannot be the cause" from one equal-fall example | Softened to "unlikely to be the main cause" |
| Q64 | "nearly 10 swings below": exactly 10 | Corrected |
| Q58 | "each day of delay costs about 1,200 orders" assumed 10,000 is per day (not stated) | Made conditional |
| Q40 | Garbled caveat sentence ("same-weekday-versus-weekday") | Rewritten plainly |
| Q43 | Gross/net revenue retention used without explanation | Plain-words gloss added |
| Q9, Q8, Q20, Q57, Q79, Q81 | Jargon at first use (AOV, Simpson's paradox, ETL, difference-in-differences, last-click attribution) | One-line glosses added |
| Q13, Q14, Q24, Q25, Q26, Q42, Q43, Q44, Q48, Q62, Q63 | No blank line after the inline data table (the next bold line would render as a table row) | Blank line inserted; table contents untouched |

## Verified as correct (no change)
All percent changes, shares, funnels, DiD, mix/rate split (Q62 incl. order-dependence check), Shapley split (Q91), MRR bridge, payroll lakh/crore conversion (Q49: 1 crore = 100 lakh; Rs 1,09,804 per head, 83% from per-head), z-style SD figures (Q45 sample SD 12.25, range 963 to 1,037), seasonal index and baseline (Q29, Q53, Q67), outage sizing (Q74), censoring (Q83), cannibalisation profit (Q88). Percentage vs percentage-point usage is correct everywhere checked (Q13, Q38, Q46, Q48, Q50). Sanity checks are mostly genuine second routes; several are simple algebraic re-statements (Q9, Q23, Q60), which are acceptable for the difficulty.

## Asked-at and honesty
- All "Asked at" lines are consistent with research/Book07_Part05_sources.md and research/interview_processes.md (Meesho completed-orders case Q21, Swiggy WoW prompt Q22, Flipkart return-window Q23 and cart-addition Q28, PhonePe Q25). All stay marked unverified or "no company-specific report found". No change needed.
- No real-world statistic is stated as fact; every base number is a question input or labelled illustrative/assumed. Telecom, SaaS, lending, UPI and payroll figures are exercise inputs.

## Unresolved / report only
- Q15, Q44, Q55, Q40: question premises are ambiguous (customers vs orders; retained base; "non-promo unchanged" while promo ended; equal per-Tuesday figures). Each answer already flags and handles this; kept as is.
- Count: heading says Target 90, Actual 91 (a 91st question was added); intended, not changed.
- Ordering: star/difficulty order is correct; numbering Q1-Q91 continuous. Q70 and Q72 (1 star, easy) are tiny arithmetic items placed before harder 1-star ones, as expected.
- Overlap: Q2, Q19, Q20, Q61, Q64 all revolve on the same Tuesday case, and Q42, Q62, Q77 each teach mix shift; Q63, Q65, Q79 reuse DiD; Q16/Q45/Q64/Q73 reuse SD-band logic. Deliberate cross-references exist, but consider whether Part 5 overlaps Book 8 scenarios or other Book 7 parts (not checked, no other parts read).
- Style: Q45-type and similar answers use "Rs" in a few places (Q71, Q88) and the rupee sign elsewhere; left unchanged.

## Claims left unverified
- No web access: question-bank and company "asked at" claims remain unverified as in the sources file. Weather, UPI, telecom and similar context statements are general reasoning, not facts.
