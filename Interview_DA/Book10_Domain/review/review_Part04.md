# Review: Book 10 Part 4 (Healthcare & pharma), Wave C

## Counts
- Answers checked: 79 of 79 (Q1-Q79).
- Answers with figures recomputed by code (scratch: C10_Part04/a.py, s.py): 44 (Q10-Q17, Q31-Q37, Q39-Q44, Q47-Q50, Q56-Q58, Q60, Q64, Q72, Q73, Q76, Q77, plus Q49 SQL). Both SQL snippets (Q17, Q49) were run in SQLite.
- Answers with wrong arithmetic: 0. Every figure matched the written result (Q47 Fisher exact p = 0.2003, Q33 90th percentile = 129, Q58 mix 2.8 + rate 3.2 points, Q57 ARPOB 5,435 and 7.8% fall all confirmed).
- Answers changed: 14 (Q13, Q14, Q16, Q17, Q33, Q39, Q49, Q50, Q52, Q54, Q57, Q60, Q63, Q72). All edits were targeted; no heading, number, star, order or inline question data changed.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q17 | SQL output quoted for "8 invented claims" that were never shown, so it could not be reproduced; output was an inline sentence | Added the 8 invented rows, noted SQLite/MySQL syntax, pasted real output as a table (verified identical) |
| Q49 | Same: 7-row table not shown; "only 4 rows are clean stays" was inconsistent (open, impossible and duplicate rows leave A1, A2, A5, A6, with A5 a day case) | Added the 7 rows, noted syntax, rewrote the plain-words line to 4 usable rows with A5 flagged |
| Q13 | "Appeal" never explained | Added one-line definitions of denial and appeal |
| Q14 | Unclear wording "only you can see your own hospital" | Reworded to plain meaning |
| Q16 | Dropout follow-up gave no numbers | Added 200/0.9 = 222.2 so 223, then 223/0.6 = 371.7 so 372 |
| Q33, Q72 | lakh not explained for a beginner | Added Rs 5 million / 100,000 conversions |
| Q39 | Confusing analogy ("salary arrears in reverse") | Replaced with unpaid invoices |
| Q50 | Actual ALOS 4.2 and 8.24 were not labelled invented | Labelled "invented" |
| Q52 | Regulation statement in the "Say this" line had no label | Added "from memory, unverified" |
| Q54 | "Pseudonymised data still personal data in most regimes" asserted as fact | Softened and labelled from memory, unverified |
| Q57 | Used the rupee symbol (rest of part uses Rs); tiny ARPOB (Rs 5,435) contradicts Q12 (Rs 50,000) with no explanation; "package" undefined | Rs everywhere, note that figures are small invented numbers (see Q12), defined package rate |
| Q58 | Blank line missing after the table | Added |
| Q60 | Remaining months not stated in the 11-per-month step | Added "months left = 2" |
| Q63 | Real company description stated without label | Added "from memory, unverified" |

## Domain checks (no change needed)
Occupancy, ALOS, ARPOB, denial rate, readmission, evolution index (labelled "state yours"), screen-failure sizing, A/R days, MAT, coverage vs frequency, case mix and Pareto are standard or carry "my definition" labels. Regulation items (DPDP, HIPAA, IRDAI, 21 CFR Part 11, GCP, NABH, PM-JAY, EDI 837/835) were already labelled "from memory, unverified" and awareness-level.

## Asked-at claims
All "Asked at" lines are either "commonly asked (no company-specific report found)" or match the sources file (IQVIA reports: Q8, Q9, Q15, Q59, Q63, Q77; Novartis Hyderabad: Q7, Q24, Q60, Q62; PharmaForceIQ posting: Q22, Q46). All carry unverified labels.

## Unresolved / report only
- Ordering: no problems seen (stars descend 3, 2, 1; numbering Q1-Q79 continuous).
- Overlap: Q9, Q10-Q14 and Q31, Q49, Q56 and Q73 overlap on ALOS/occupancy by design (cross-referenced). Q58 overlaps conceptually with Q13 and Q17 (denials). Q69/Q70 and Q25 overlap on adverse events. Q64 seasonality may overlap Book 5/7 time-series material; not checked. Q8, Q45 (primary vs secondary) overlap lightly.
- Q15 evolution index: formula is a common Indian-pharma convention from memory; not verified against a company standard.
- Q57 rupee values are deliberately tiny; kept as invented teaching numbers.
- Q65 follow-ups 1 and 2 are near duplicates; left as is.

## Claims left unverified
All real-world facts (NABH under QCI, PM-JAY, IRDAI role of TPAs, HIPAA/DPDP scope, CPT mainly US, EDI 837/835, CDISC, GCP, Part 11, IQVIA description, phase sizes) remain "from memory, unverified" with no web access.
