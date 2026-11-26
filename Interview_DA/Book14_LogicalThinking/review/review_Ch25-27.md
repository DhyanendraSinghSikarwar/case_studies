# Review Ch25-27 (Wave C, Book 14)

Scratch: scratchpad/C14_Ch25-27/c.py (Python -I; every worked example, scenario, self-check and practice number recomputed without reading the answers first, then compared).

## Counts
| Chapter | Practice (index) | Re-solved by code / total | Items wrong | Items changed |
|---|---|---|---|---|
| Ch25 Cognitive biases | 20 | 20 / 20 (+5 examples, 2 scenarios, 3 self-checks) | 0 | 0 |
| Ch26 Evaluating claims | 15 | 15 / 15 (+5, 2, 3) | 0 | 1 (Q9, overlap) |
| Ch27 Misleading charts | 15 | 15 / 15 (+5, 2, 3) | 0 arithmetic; 1 ambiguous (Q11) | Q11, Ex1 |

All counts match the index (20 / 15 / 15), numbering and easy-medium-hard order kept, no answers in chapter files, 5 examples, 2 scenarios, 5-item mistake logs, 5-line recaps, keys complete. No em or en dashes, no code fences, tables followed by blank lines.

## Fixes
| Ch | Item | Problem | Fix |
|---|---|---|---|
| 26 | Q9 + key | Near copy of Book 13 Part 8 Q44 (optional email survey, 50 replies, 80% satisfied; same response-rate and best/worst-case structure) | New scenario: shop feedback cards, 800 customers, 40 returned, 36 recommend; best/worst case 4.5% to 99.5%; key rewritten |
| 26 | Q11 | "median" used but never defined | Mean and median defined inside the question |
| 26 | Ex 3 | "percentage points" used without a definition | Defined at first use |
| 27 | Ex 1 | Same structure as Book 13 Part 8 Q28 (truncated bar axis, "looks twice as tall") and the self-check 1 repeated its numbers | Replaced by a three-branch revenue chart (axis from 400; 420/440/480; apparent 4x versus true 14.3%) |
| 27 | Q11 + key | Part (a) ambiguous: with Q2 segment A unchanged (40, 40), B also began at the same height, contradicting the key's explanation | Q2 value of A changed to 45; totals now 90 and 105; B and C both float; key (a), (b), (d) rewritten; % changes for B (-33.3%) and C (+100%) unchanged |
| 27 | Concept | Mean, median and "index to 100" used (Q7, Q14) but not defined | Two short definitions added under "light tools" |

## Checks passed without change
- Ch25: every figure verified (40% = 40%; 75% missing; 3.4 weighted score; 22.5% versus 8.3%; Q8 85.83 / 65 / 24.3%; Q9 8% versus 10%; Q15 80/175 = 45.7%; Q17 33.3 to 18 = 46%; Q18 65%; Q19 3 failures). Concepts (confirmation, anchoring, survivorship, sunk cost, base-rate neglect, outcome bias) stated correctly.
- Ch26: Q6 3.87, Q7 200 fewer, Q8 25% = 25%, Q11 mean 34 / median 27, Q12 1.0 versus 1.5 per 10,000 hours, Q13 99% accuracy of a do-nothing tool, scenario 2 20 to 23.3 per 1,000.
- Ch27: all percentages, areas (4x, 9x), densities (2.0, 1.5, 0.5; 2, 4, 1), rates (500 versus 1,500 per million), log-scale 900%, reversed axis -44.4%, index 100/110/125/150, 122/118 = 1.034 confirmed.

## Overlaps
- Theme-level only (different scenarios, numbers, structure), left as is: Ch25 Q18 and Ch25 Ex3 with Book 13 Part 8 Q33 (survivorship); Ch27 Q7 with Book 13 Part 8 Q43 (mean versus median salary); Ch25 Q15 and Ch26 Q13 with Book 13 Part 8 Q56 (vendor fraud tool, base rate); Ch25 Q4 with Self-check 3 (both survivorship, different cases).
- Within Book 14: Ch25 Q10 repeats the framing idea of Q7(e) and Ex5 (different numbers, acceptable as practice). Ch27 self-check 2 uses the same 45/40/33 pie as Ex4 (kept, a retrieval item).
- No hits in Book 6 Part 7.

## Cross-references
Chapter 24 (correlation versus causation), Book 13 Part 8 (critical reasoning, includes data and chart claims), Book 1, Book 2 and Book 4 (Power BI) all exist and fit.

## Unresolved / unverified
- Nothing unresolved. Ch26 "genuine employers do not normally charge candidates" is already labelled a rule of thumb; no real organisations, studies or statistics are named (the "Ministry of Labour notice 2026/44" is stated as made up).
- Spreadsheet or SQL pointers name topics only (COUNTIF, GROUP BY); no formulas shown, none run.
