# Book 5 (Statistics & Maths) — Wave C review summary

Reviewed 2026-11-06, one reviewer per part (per-part reports in `review/review_PartNN.md`). Environment: Python 3, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels; no Excel, no web access.

## Totals
| Part | Answers checked | Answers edited | Notable fixes |
|---|---|---|---|
| 1 | 61 | 6 | Harmonic mean wording, contribution-to-growth definition, lambda code rewritten |
| 2 | 60 | 22 | Misleading "nearly doubled" claim, SE explanation, plain-words lines |
| 3 | 50 | ~22 | Q22 output/prose mismatch, Q50 ratio (42,000x not 12,000x) |
| 4 | 71 | 19 | Float noise in outputs, "biggest leak" wording, Q54 explanation |
| 5 | 51 | 17 | Q22 gap, Q51 finite-population rule, jargon explained |
| 6 | 74 | 12 | Rounding slip Q19, readability, memory labels |
| 7 | 54 | 14 | Q9 code failed alone, Q35 wrong range, Q54 ratio |
| 8 | 43 | 17 | Q4 H1 wrong, Q22 simulation missing from code, 7 unsupported "Asked at" lines |
| 9 | 41 | 11 | Q20 "one-third" was 25%, Q15 worst quarter, Q38 masking caveat |
| 10 | 64 | 12 | Q44 follow-up (16/33 not 48/165), Q6 example scale, Tiger claims labelled |
| 11 | 34 | 12 | PERCENTILE.EXC wording, STANDARDIZE version, Accenture claim narrowed |
| 12 | 25 | 8 | Added mini-projects, self-check test, job-ready definition; resources labelled unverified |
| **Total** | **628** | **~172** | |

All ~600 Python snippets ran and reproduce their pasted outputs after the fixes. Every worked number was re-derived independently. Final automated check: 628 answers, balanced code fences, zero `ANSWER_PENDING`, zero em dashes outside file titles.

## Still unverified (labelled in the text)
- Every "Asked at" line rests on search-snippet sources; no first-hand Hyderabad/Bengaluru reports were found. Company mentions (Tiger Analytics, Fractal, Wells Fargo, Accenture) are unverified candidate reports.
- No Excel was available: all Excel formulas were checked by logic against Python and are labelled "not run in Excel here". Excel version claims are from memory.
- From-memory facts: Anscombe 1973, Datasaurus Dozen, Tukey 1.5 rule, modified z-score constants, Campbell's law, Sturges/Freedman-Diaconis, Rule of 72/114/144, ToolPak details.
- Part 12 resource and dataset names (StatQuest, Khan Academy, OpenIntro, Kaggle datasets) are from memory; check links before relying on them.
- matplotlib was not installed: plotting lines (e.g. Part 9 Q11 box plot) were not run.

## Open items for a later pass (report-only)
- Light overlap between parts: z-scores and outliers (Parts 2, 3, 9), CI interpretation (Parts 5, 6, 8, 10), confounding (Parts 7, 9, 10), n-1 (Parts 2, 6, 11), Bayes base-rate family (Part 4), Q44/Q50/Q74 in Part 6. Kept because each asks a different angle.
- A few answers reuse a table built in an earlier answer (e.g. Part 5 Q14/Q15 reuse Q13's data) and do not run standalone.
