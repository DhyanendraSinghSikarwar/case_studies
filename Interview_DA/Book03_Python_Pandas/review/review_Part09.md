# Review: Book 3 Part 9 (EDA End-to-End Tasks), Wave C

Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, matplotlib Agg.

## Counts
- Answers checked: 54 (Q1 to Q54).
- Python snippets run: 48 of 48 run without error and match the pasted Output after one fix (Q6). Q1, Q2, Q5, Q17, Q18, Q45, Q47 read CSV files, so I rebuilt the files from each answer's sample-data description and the pasted output (all matched). Q37 (charts) ran clean under Agg and its bar-chart numbers match; Q48 wrote the xlsx and the sheets and Summary table match. Q11, Q43, Q46, Q49, Q50, Q51 have no code.
- Answers edited: 18 (Q1, Q4, Q5, Q6, Q11, Q15, Q20, Q26, Q37, Q42, Q43, Q45, Q46, Q48, Q49, Q50, Q51, Q54).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q6 | Pasted output misaligned (`104  John` should be `104   John`) | Corrected to the real output |
| Q15 | Follow-up said the biggest drop is screening (40% lost); the real biggest drop is interview to offer (50% lost) | Rewrote the follow-up with all three step losses |
| Q4 | Claimed `sort_values` keeps original order for ties (default sort is not guaranteed stable) | Reworded: tied order can vary, add a second key |
| Q42 | "Missing at random (MCAR)" mislabelled; MNAR case unlabelled | MCAR spelled correctly, MNAR added; chi-square explained in plain words |
| Q46 | "Reverse direction" bullet confusing (overtime-pay) | Rewrote in plain words |
| Q26 | Follow-up 1 duplicated the Alternative; "pivot_table without aggfunc gives averages" is wrong for date/text values (TypeError on pandas 3, checked) | New follow-up (crosstab vs pivot_table); mistake line corrected |
| Q20 | Alternative ("take every second row after removing 1.0 values") was vague and could drop real 1.0 pairs | Removed |
| Q45 | Unsupported "often 5x or more" saving | Replaced with a reason |
| Q37, Q48 | Verification scaffolding wording ("code ran cleanly and saved", "Reading it back showed") | Reworded to plain output descriptions |
| Q11, Q43, Q46, Q49, Q50, Q51 | Missing "What it means" field | Added one plain-words line each |
| Q1 | CSV and DataFrame never explained | Added one bullet in Explain simply |
| Q54 | Fisher exact test unexplained | One-clause plain explanation added |
| Q50 | "they often give no internet or no install" unsupported | Softened to "may not be allowed" |
| Q5, Q11, Q15, Q37, Q43 | "Asked at" overstated (most common, stated evaluation point, standard task, normal part, typical format); not in sources | Reduced to the sourced wording or "commonly asked (no company-specific report found)" |

## Verified claims (pandas 3.0.5)
- Text columns show `str`; `select_dtypes(include="object")` warns and still returns str columns (Q17); `exclude="number"` works.
- Q14 claim confirmed: `format="mixed", dayfirst=True` reads `2026-03-02` as 3 Feb.
- Q29: no SettingWithCopyWarning, original unchanged; chained assignment raises `ChainedAssignmentError` and does not update the original.
- Q28: `MergeError` text matches the pasted output; Q18: `mean()` on text columns raises TypeError; Q27: `nunique()` skips NaN; Q7: `nlargest(..., keep="all")` works; Q34: `groupby().nlargest` works.

## Unresolved / report only
- Ordering: Part title says 🟡🔴 but Q1, Q2 and Q16 to Q19 are 🟢; Q47 is 🟢 at the start of the ⭐ block (consistent within star tiers). Heading line 1 contains an em dash (heading, left unchanged).
- Overlap: Q27 and Q36 (nunique, constant/ID columns), Q10, Q35 and Q42 (missing-value treatment), Q9, Q28 and Q44 and Q33 (merge/reconcile, also Book 2 merge mapping), Q21/Q22 vs Q5 (group comparison), Q12 and Q20 vs Book 5 Part 11 (IQR, corr). Q5 and Q43 overlap in content.
- Q29 intentionally shows the risky pattern before the fix, which a live candidate would not type; kept as teaching contrast.

## Claims left unverified
- Source snippets (Glassdoor Pivigo, PracHub, GoLinuxCloud, Tiger Analytics, IBM HR notebooks) are snippet-level only, per research/Book03_Part09_sources.md; not opened.
- Q50 tool names (ydata-profiling, sweetviz, D-Tale) from memory, not run (already labelled in the answer).
- Q30 BOM / `utf-8-sig` advice and Q29 pandas 2.x behaviour from memory, unverified.
- Q1, Q5 sample CSVs are reconstructions; memory-usage lines (516, 532 bytes) matched.
