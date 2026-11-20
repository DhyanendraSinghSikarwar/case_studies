# Review: Book 3 Part 5 (pandas: groupby, merge, pivot, apply)

Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3. Scratch: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C03_Part05` (run.py harness, claims.py).

## Counts
- Answers checked: 83 of 83.
- Snippets run: every Python block (sample data, code, alternatives) was executed with a fresh copy of the sample state per answer and compared with the pasted Output.
- 80 answers matched their pasted Output after fixes. 3 differ only by design: Q16 and Q47 end in a deliberate `MergeError` (message text matches; pandas prints extra "Duplicates in right" lines, already noted in the answer), Q29 prints a memory address (changes every run). Q76 reads CSV files, so it was run on three temporary files and matched.
- Answers edited: 33 (Q1, Q5-Q11, Q13, Q15, Q17-Q21, Q27, Q32-Q35, Q38, Q50, Q58, Q69, Q70, Q73, Q74, Q76-Q79, Q81).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q1 | Shared `employees` table lacked `emp_id`, `dept_id`, `gender`, which Q5-Q15 use ("Q1 plus gender") so those snippets could not run | Added the three columns to Q1's sample code (Q1 output unchanged); Q5, Q7, Q9, Q10 now say "from Q1 (includes ...)". Also explained Series/DataFrame/index at first use |
| Q5 | Sample `departments` block had no import | Added `import pandas as pd` |
| Q6 | No "What it means" | Added |
| Q8 | `jan`/`feb` not defined; output index 0,1,2,3 would not happen (both start at 0) | Added sample code; output now 0,1,0,1 and prose says why (points to Q33) |
| Q11 | Said `applymap` is "deprecated"; it is removed in pandas 3.0.5 (`hasattr` False) | Reworded; "renamed in 2.1" labelled from memory. Explained lambda and "vectorised" at first use |
| Q13 | "broadcast" jargon | "repeated on every row" |
| Q15 | Pasted output order wrong (HR shown before IT; real order Imran before Ravi); prose "sorted by luck" wrong | Output and prose corrected |
| Q17, Q18, Q19, Q27, Q32-Q34, Q38, Q50, Q69, Q70, Q73, Q74, Q77-Q79, Q81 | Verification narration in answer text ("I ran this", "checked by running", "my test", "the real error printed") breaks style_guide 11 | Removed or reworded to neutral wording |
| Q20 | "about 0.96 s" for apply(axis=1) | Re-timed (1.3 s here); now "about 1 second, hundreds of times faster, varies by machine" |
| Q21 | Copy-on-Write not explained | One-line plain explanation; claims re-verified (ChainedAssignmentError warning appears on chained set) |
| Q35 | Claimed identical suffixes raise an error | False on 3.0.5 (gives two same-named columns). Corrected |
| Q50 | "what I saw" | Reworded; int64 vs str ValueError verified; older behaviour labelled from memory |
| Q58 | Claimed `stack()` drops NaN by default | False on 3.0.5 (kept; `dropna=` now raises). Corrected, older behaviour labelled from memory |
| Q76 | Sample data was only a file list | Added table of the three files' contents |

## Verified claims (run on 3.0.5)
SettingWithCopy/ChainedAssignmentError behaviour (Q21), `groupby("a","b")` raises (Q23), empty-suffix keeps name (Q35), int vs str merge raises (Q50), `np.select` text choices without default raises TypeError, numeric fills 0 (Q63), `observed` default True (Q78), `transform("size")` (Q41), `pivot` duplicate error (Q18), `.loc[0]` returns 2 rows after concat (Q33), `DataFrame.append` absent (Q76), `nth(1)` alternative (Q81), timings for Q73 (0.004 s vs 0.6 s) and Q74 (3.3 s) consistent with the text.

## Claims left unverified (labelled "from memory" in the text)
- `applymap` renamed in 2.1 and deprecated before removal (Q11); `DataFrame.append` removed in 2.0 (Q76); `how="cross"` needs pandas 1.2 or newer (Q72); SettingWithCopyWarning on 2.x (Q21); `observed` default and warning in 2.x (Q78); older `stack` NaN behaviour (Q58); older int/str merge behaviour (Q50).
- "Asked at" lines: all are "commonly asked (no company-specific report found)" or cite snippet-level sources listed in `research/Book03_Part05_sources.md` (Tiger Analytics, PracHub, PapersAdda, Naukri Code360, Towards Data Science, freeacademy). Not re-checked online; no invented companies found.

## Unresolved / report only
- Ordering: stars descend 3 to 1 as intended; no numbering gaps. Cross-part overlap: Q39 and Q82 (attrition rate vs share) are deliberately distinct; Q69 crosstab overlaps Q27 and Q54 in technique (different task). Q47/Q16 both show `validate` (cross-referenced). Q5 vs Q31 and Q67 vs Q37 partial overlap (map vs replace).
- Q2-Q4, Q11-Q15, Q17 rely on Q1/Q5 sample data by reference; a reader opening them directly must look back. Left as designed.
- The title line contains an em dash (heading, not answer text); left unchanged.
- Q29 pasted memory address cannot match a re-run.
