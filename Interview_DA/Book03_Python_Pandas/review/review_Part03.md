# Review: Book 3 Part 3 (NumPy Basics)

Reviewer wave C. Environment: Python 3.13, NumPy 2.5.3, pandas 3.0.5.

## Counts
- Answers checked: 30 (Q1 is concept-only, no code).
- Code snippets run: 30 of 30 (29 main snippets plus the Q30 loop alternative); all 29 pasted Outputs matched exactly on rerun.
- Answers edited: 18 (Q1, Q2, Q3, Q7, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q20, Q21, Q22, Q23, Q29, Q30), all prose-level except the Q13 unused import.
- Code or output errors found: 0. Prose errors found: 3 (Q9 timing, Q13 storage claim, Q17 keepdims claim).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q1 | "every pandas column is NumPy underneath" is wrong for text columns in pandas 3 | Reworded to number columns |
| Q2 | Unsupported claim "first question in most NumPy lists" | Removed; plain "commonly asked" |
| Q3, Q11, Q12, Q14, Q15 | "(checked)" verification notes inside answers (style_guide Section 11) | Removed |
| Q7 | "(checked)" note; float noise claim | Verified (49500.00000000001); reworded without "checked" |
| Q9 | Timing "47 ms vs 1 ms, 40x" did not match the pasted loop (loop over a NumPy array took about 1.6 s here; 47-53 ms only for a plain list); "compiled C" unexplained | Rewrote with the three measured times and labelled machine-dependent; explained compiled C in plain words |
| Q13 | Unused `import numpy as np` in code; Arrow claim unverified; to_numpy read-only behaviour missing | Removed import; stated `str` dtype is not NumPy (Arrow part kept "from memory, unverified"); added read-only note (verified: writing raised "assignment destination is read-only") |
| Q16 | Asked-at claim "appears in general NumPy lists" not in sources | Plain "commonly asked" |
| Q17 | Claim "without keepdims shapes do not line up" incomplete: for a square 3x3 table there is no error, results are silently wrong | Clarified: error for 2x3, silent wrong numbers for 3x3 (both run) |
| Q20 | Asked-at claim "standard analyst task in NumPy prep lists" not supported | Tied to the sourced Algocademy NaN pitfall (snippet only) |
| Q21 | Pandas Copy-on-Write marked unverified | Verified on 3.0.5 (editing a column taken from a DataFrame did not change it); label dropped |
| Q22 | "argmax treats NaN as the largest" imprecise | Now: returns position of the first NaN (run), use `nanargmax` |
| Q23 | Jargon "binds tighter"; same-error claim | Plain wording; verified ValueError without brackets |
| Q29 | "object" type unexplained | Added plain-words explanation; TypeError text verified |
| Q30 | Pandas rolling note marked "not run"; alternative loop not self-contained | Verified (NaN, NaN, 3.33, 3.67, 4.0, 6.33); alternative notes it reuses `daily_hires` |

## Checks that passed (no change)
- Q3 float64 upgrade, Q8 total 46, Q10 error text for `np.zeros(2, 3)` (TypeError), Q11 ValueError text, Q14 text-to-int and round-half-to-even, Q15 unique alternative, Q26 ravel copies on non-contiguous slice, Q28 seed-7 sample, Q24 seed-42 output, boolean indexing returns a copy (Q21).
- No em dashes in answer text (only the file title line 1 has one; headings left untouched per rules). Code fences balanced (118). All 11 template fields present in every answer (code answers include Sample data, Code, Output).

## Unresolved / report only
- Ordering: stars descend 3,3,...,2,...,1 and numbering Q1-Q30 is continuous; no issue. Within the 2-star group difficulty colours are mixed (green then yellow); acceptable.
- Overlap: Q8 and Q19 (axis sums) are near duplicates by design; Q9 and Q7 both show `* 1.10`. Q25/Q27 pandas equivalents may overlap with Book 3 pandas parts (not checked against them). Q12 and Q5 overlap lightly.
- Q16 and Q17 use a different follow-up layout (numbered inline) and `text` fence labels; harmless.

## Claims left unverified
- Q3: int64 vs int32 on Windows with older NumPy (from memory, unverified).
- Q13: pandas str dtype uses Arrow storage when pyarrow is installed (from memory; pyarrow presence not tested).
- All "Asked at" entries: sources file is snippet-level only; the Tiger Analytics report (Q1, Q15) was not opened.
- Q28/Q24 random outputs hold for NumPy 2.5.3 `default_rng`; may differ across versions.
