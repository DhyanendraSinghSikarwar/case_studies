# Book 1 Part 02 review (Wave C)

File: Book1_DS_ML/Book1_DS_ML_Part02.md, 51 questions (15 x 3-star, 24 x 2-star, 12 x 1-star). No ANSWER_PENDING, no duplicated or garbled content (51 sequential Q headings, 51 Asked-at lines, CRLF preserved).

## Code
48 python blocks extracted and run standalone (own imports/seed). All run. Failures found and fixed: Q6 and Q36 fixed block used `.round` on a Python float (AttributeError in current sklearn) -> `round()`. Cosmetic: Q8, Q45 printed `np.float64(...)` -> wrapped in float(). Q36 "buggy snippet" is an intentionally partial snippet (not run on its own; its claimed test AUC 0.763 was reproduced separately).

## Numbers that did not match the code (fixed)
- Q2: SE comment was [0.343 0.057]/[0.263 0.064]; actual classic [0.329 0.052], HC3 [0.224 0.053].
- Q29: rolling mean 80.6 -> 80.7 (hand calc 242/3).
- Q33: collinearity and suppressor example numbers had no code and did not reproduce. Added code; text now 2.01 (SE 0.04) -> 2.42 (SE 0.45); suppressor +0.89 -> -0.89.
- Q42: Tweedie slope 0.76 -> 0.81; Gamma/Tweedie code added (Gamma 0.80 confirmed).
- Q38: removed unreproducible statsmodels numbers (-10.6, 50.5, SE 1e6); now qualitative (one run gave slope ~60, SE ~1e12; behaviour varies by statsmodels version).
- Q30: "matched -0.117066" claim was not produced by code; added finite-difference check (both -0.01652).
- Q46/Q48/Q50/Q51: text quoted numbers (tabular-only 0.695; logistic/unconstrained AUC and monotonic violations; lambda=200 MSE; slopes at x=-3,0,3) not printed by the code; code extended so they are produced.
- Q44: 64 MB -> 64 MiB (2^24 x 4 bytes).

## Known items
- Q21/Q18/Q22 re-run: all numbers match (Q21 [0.994 -0.008 0.002 0.233 0.994]; Q18 OLS/Ridge raw and standardized; Q22 0.39/2.06/2.29).
- Q34: AUC 1.0 flagged as toy-corpus artefact in Example text and code comment; removed unsupported "real text 0.8-0.95".
- Q46: example rewritten honestly (random vectors, differences within CV noise, shows only that regularization matters; tabular-only 0.695 added).
- Q47: 0.39 vs 0.11 reproduced; text and code comment now state it is the share of runs with at least one "significant" selected feature, not a per-test FPR.
- Q37: stability frequencies [0.06 0.90 0.90 0 0 0] reproduced; text made honest (twin 1 dropped, twins 2/3 kept 90%, arbitrary within the group; one run, not a law).

## Structure
Header: added Stars line (15/24/12), replaced stale "Phase 1" status, removed stale remark in dedupe note. Q36 "Bugs:" heading renamed "Then explain (the bugs)"; Q36 summary corrected to "two leaks plus p-value selection".

## Unresolved / not verified
- Asked-at company lists are unverifiable and were left as is.
- Literature claims (Hoerl-Kennard, Lee et al. 2016 selective inference, Firth, glmnet differences) from memory, not web-checked; they are standard.
- Q20 Asked-at "Grigorev-style theory banks" kept per rules.
