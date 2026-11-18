# Review: Book 10 Part 3 (BFSI), Wave C

Reviewer pass: all 113 answers read in order. Scratch scripts: calc.py (every figure) and sql.py (all 4 SQL snippets run in SQLite 3.53) in the scratchpad folder C10_Part03.

## Counts
- Answers checked: 113 of 113.
- Answers with numbers recomputed by code: 76 (all answers with data, worked examples or SQL: Q10, 13, 15-18, 20, 21, 23-29, 34, 45-66, 68, 74, 76-78, 85-90, 97-102, 104-107, 110, 111, 113).
- Arithmetic wrong: 0 (all written figures matched, including lakh/crore conversions and pp vs percent statements).
- Answers changed: 20 (Q2, 10, 15, 16, 17, 19, 23, 29, 54, 61, 68, 69, 76, 85, 86, 88, 90, 98, 101, 102).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 2 | "Asked at" claimed fintech loops stress licence knowledge; sources do not say that | Reworded to what the sources support |
| 10, 15, 16, 17, 86, 88 | "computed by code / checked by code" verification claims left in answer text | Removed; calculation shown instead |
| 19 | Grammar "masked of direct identifiers" | Fixed |
| 23 | SQL result claimed but sample table not shown | Added 5-row invented sample; output verified (ABCDE1234F, 2) |
| 29 | "p about 0.055" given without naming the test; uncorrected chi-square gives 0.040 | Named Fisher test (0.055), stated the 0.04 alternative |
| 54 | FPD denominator assumes first EMI is due for all loans, not stated | Added assumption line |
| 61 | SQL sample not shown; FULL OUTER JOIN not in MySQL | Added sample data and portability note; output verified |
| 68 | Table had no blank line before/after | Added blank lines |
| 69 | "days overdue by code" confusing wording | Reworded |
| 76 | KS 61.5, AUC 0.881, Gini 0.761 could not be reproduced (no band data shown) | Replaced with a 5-band table; recomputed KS 46.2, AUC 0.792, Gini 0.584 |
| 85 | Worked example said 12 new + 38 experienced = 50 while end headcount is 48 (confusing) | Clarified it refers to the 50 at month start |
| 86 | Contribution method assumes constant segment mix, unstated | Stated |
| 90 | "per 100 of value" unit unclear (index) | Clarified as per index point |
| 98 | ln not explained for HR reader | One-phrase explanation added; PSI 0.127 and 0.0008 verified |
| 101 | Sample not shown; tie order in output nondeterministic | Added sample, added tiebreak in ORDER BY, pasted real output (D1, D4) |
| 102 | Sample not shown; alias in HAVING not portable | Added sample, real output (9 | 130000 | 128500 | 0.99), portability note |

## Checks passed with no change
- All 113 answers have Asked at, checker, Say this, Explain simply, Likely follow-ups, Common mistakes; Data/Regulation notes present where needed.
- Code fences balanced (5 blocks); no em dashes in answer text (only the part-title line); no ANSWER_PENDING.
- Regulation-type claims (NPA 90 days, SMA, CASA, DPDP, PMLA, digital lending, AA, Basel 9%/8%, MDR zero, dormancy periods, APE 10%) all carry "from memory, unverified" and a confirm-with-compliance pointer. No financial advice found.
- "Asked at" lines otherwise claim only what research/Book10_Part03_sources.md supports (Q109, Q110, Q81 cite listing/community case as unverified).

## Unresolved / report-only
- Ordering: stars descend 3 to 2 to 1; within-star difficulty order is respected (green, yellow, red). Numbering Q1-Q113 continuous. Header says target 100 / actual 113, which is correct.
- Overlap inside the part: NPA (Q3, Q40, Q69), DPD buckets (Q6, Q69), CASA (Q4, Q25, Q44), expected loss (Q10, Q49, Q77), earned premium (Q17, Q104), collection efficiency (Q16, Q87), NAV/AUM (Q38, Q62, Q63), persistency (Q28, Q111). Different angles, left as is; coordinator may trim.
- Overlap with other books not checked against their files (sources note says UPI success rate, EMI maths, DPD SQL kept in Books 2, 6, 7).
- Q16: "Say this" says watch 90%, explanation says watch both; consistent enough, left.

## Claims left unverified (no web access)
All regulation and market-convention facts listed above, CIBIL range 300-900, IRDAI/NPCI roles, NSDL/CDSL, PSI rule-of-thumb 0.1/0.25, insurer persistency checkpoints, dormancy periods. They are labelled in the text, not confirmed.
