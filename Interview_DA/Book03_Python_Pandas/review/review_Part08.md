# Review: Book 3 Part 8 (Visualization: matplotlib, seaborn)

Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, matplotlib 3.11.2, seaborn 0.13.2 (Agg backend). plotly was not installed, so I pip-installed it into the scratch folder only, to run Q47.

## Counts
- Answers checked: 50 of 50 (Q1 to Q50).
- Python snippets: 80 blocks extracted. All 80 run OK, either standalone or chained with the answer's Sample data block. Exceptions are intended or environmental: Q24 (Jupyter `%` magic, run without the magic line), Q38 (last line raises the ValueError the answer is about), Q47 (ran after installing plotly).
- Printed outputs (Q26, Q29, Q34, Q37, Q38, Q39, Q45, Q48, Q19) match the pasted Output exactly. Numbers in prose checked by code: Q5 bin counts 6,5,2,1,0,1; Q11 and Q42 correlations; Q13, Q14, Q30, Q40 and Q48 values.
- Answers fixed: 11 (Q9, Q30, Q33, Q36, Q38, Q39, Q45, Q46, Q47, Q49, Q50).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q9 | No blank line after the table | Added blank line |
| Q30 | Mistake line said forgetting `x="region"` makes region "a third bar series or errors". I ran it: pandas silently drops the text column and labels groups 0 to 3 | Reworded to the real behaviour |
| Q33 | Sample dates began Sunday 1 March 2026, so the low days (index 5,6) fell on Friday and Saturday, not weekends; prose said "weekends" | Start date changed to 2026-03-02 (Monday), so the dips are Saturday and Sunday; sample line updated; 30 days now end on 31 March, so the title "March 2026" holds |
| Q36 | Output claimed overlap "without the last line" without rendering both | Softened to "can crowd or be clipped" and stated it was not compared |
| Q38 | Variable `it_hiring` filtered a month named "Dec" (misleading name); Output did not show the error the code ends with | Renamed `december_hiring`; Output now states the ValueError message (verified text) |
| Q39 | Code built a plot but never showed it, and lacked the matplotlib import | Added `import matplotlib.pyplot as plt` and `plt.show()` |
| Q45 | "About 1 in 12 men" stated as fact | Marked as a commonly quoted figure |
| Q46 | `print(sorted(os.listdir("charts")))` is verification scaffolding (style_guide 11) | Removed; Output now says no printed text and the two files were created (checked by listing) |
| Q47 | Output said the code ran, but plotly was not installed here | Installed plotly in scratch, ran it, `attrition.html` written (4.8 MB); Output wording updated |
| Q49 | Sample data inconsistent: 30 joined in the funnel, but monthly hires summed to 69 and sources to 100 | Monthly hires now 3,4,4,6,5,8 (sum 30) and sources 12,10,5,3 (sum 30); Output prose updated |
| Q50 | Variable named `it` (poor name) | Renamed `sales_hires` and `it_hires` |

## Concept checks (all by running on pandas 3.0.5 / seaborn 0.13.2 / matplotlib 3.11.2)
- `corr()` on a text column raises ValueError (Q11 claim holds). `distplot` still runs and warns it will be removed in v0.14.0 (Q28). `ax=` on `catplot` and `displot` is ignored with a UserWarning (Q28, Q43 hold).
- `countplot` with both x and y raises TypeError (Q26 holds). `resample("ME", on=...)` works (Q33). `pivot_table(observed=True)` works (Q48). Q35 KDE has two modes for Sales (about 34 and 69) and one for IT (Q35 holds).
- seaborn boxplot (Q12, Q34, Q43) emits a MatplotlibDeprecationWarning ("vert ... deprecated in Matplotlib 3.11") from seaborn 0.13.2 internals on this matplotlib; the charts still draw. Not changed in the answers (library-version noise, not the candidate's code). Q42 heatmap emits a PendingDeprecationWarning for `set_bad`, same reason.

## Claims
- Every "Asked at" line says "commonly asked (no company-specific report found)", which matches `research/Book03_Part08_sources.md` (no company report found). No invented companies or statistics.
- Left unverified: Q7 and Q24 notebook/backend behaviour (already labelled "from memory"); Q33 "ME" alias in older pandas (labelled from memory); Q45 colour-blind prevalence and Q36 "constrained is more reliable" are general knowledge, not tested; Q20 "bar_label needs matplotlib 3.4+" from memory.

## Unresolved / report only
- Template: Q8 and Q9 have no Sample data or Code (conceptual answers), which is acceptable; every answer has Asked at, Checking, Say this, Explain simply, What it means or equivalent, Follow-ups and Common mistakes.
- Q25-Q34 samples build 60 random rows with a seeded generator, longer than the 3 to 8 row guidance in style_guide 11; kept because distribution charts need volume. Q35 to Q50 plot-only answers show no pasted image (outputs are described in words).
- Overlap: chart-choice and boxplot-reading concepts overlap Book 4 Part 8 (noted in the sources file); Q34 outlier IQR rule overlaps statistics parts elsewhere; Q14 attrition calculation likely overlaps pandas groupby parts. Not edited.
- Ordering/numbering: ordered by stars then difficulty; no problems seen. Header says Target 45 / Actual 50, consistent with 50 questions.
- Style: no em dashes in answer text (only the file title line); code fences balanced (180).
