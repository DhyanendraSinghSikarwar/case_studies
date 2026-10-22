# review_Part08.md (Book 1, Part 8: Charts and Excel Dashboards, Wave C)

Date: 2026-10-22. Reviewer re-ran every numeric claim behind the charts (charts cannot run here). Scratch: `.../scratchpad/C1_Part08`.

## Counts
- Answers checked: 54 of 54 (template fields present in all; code fences balanced; blank line after every table, script check).
- Formula results re-executed with `tools/xl_eval.py` and matching the printed Result: 29 (Q2-Q6, Q8-Q11, Q14, Q15, Q17, Q21-Q27, Q29-Q31, Q37, Q41, Q44, Q46 and Q5/Q9 annual figures). Q38, Q39, Q48 and Q43/Q45/Q47/Q49/Q52 arithmetic confirmed by pandas/Python/hand. Q44 EXC needed `_xlfn.` prefix; values match.
- Answers edited: 15 (Q1, Q2, Q4, Q5, Q6, Q9, Q16, Q17, Q18, Q23, Q27, Q28, Q35, Q43, Q44). Q36 left unchanged (see unresolved).
- Not run here (labelled in the answers): chart drawing, pivots, slicers, timelines, protection, Power Query, VBA, form controls.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 2 | Sample sheet columns did not match formula `C2/AVERAGE(B2,D2)` and mixed departments into the monthly table | Sample rebuilt as Opening/Leavers/Closing/Attrition plus a separate headcount table |
| 4, 6 | "Full 12-row sample" showed 4 rows (different IDs in each) | Full consistent 12-row table (Sales 5, IT 4, HR 3; 4 leavers; South 8 with 3 left) re-run: 12, 4, 33.3%, Sales 5/2, South 8/3 |
| 5 | Formulas pointed to an undefined `Data` sheet | Noted that Data = Q9 table (109, 466.4167, 23.37% re-run) |
| 9 | Sample showed 6 of 12 months ("omitted for space") while formulas ran to row 13 | Full 12-month table reconstructed from the printed rates; all 12 rates, 109, 466.42, 23.37%, peak Oct, min Aug reproduced |
| 27 | Rows for Apr-Dec closing headcount missing; 494.25 not reproducible | Full 13-row table; closings chosen to match; re-run: 54, 494.25, 10.93%, sum of monthly rates 10.94% |
| 28 | No sample sheet (Jan-Mar 5 joiners claim unverifiable) | 8-joiner sample table added (Q1 = 5, Q2 = 3, matching pandas claim) |
| 43 | "Biggest drop is interview to offer (25%)" wrong in absolute terms | Reworded to weakest conversion |
| 44 | Sample cells held text ("Q1 4.95") so formula refs did not work; INC/EXC mapping claim unsupported | Numeric layout matching formulas; fence formula points at D column; Microsoft page defines the options as median inclusion for odd N only, claim relabelled unverified |
| 1, 17, 35 | Histogram/Pareto/box/treemap/sunburst availability from memory | Updated from fetched pages (below); Q35 table gained a Sunburst row; Q1 and Q35 now use the same labels |
| 16 | Rule quoted second-hand | Quoted from fetched page; version note states page lists only 365/2024/2021 |
| 18 | WCAG 4.5:1 and "1 in 12 men" unverified | Confirmed from W3C and NEI pages; contrast ratios recomputed |
| 23 | Bin boundary rule "from memory" | Confirmed wording from Microsoft histogram page |
| 35 | Google Sheets chart list included "geo" | Now lists only types named on the fetched Google page; geo/gauge labelled unverified |

## Claims newly verified (fetched pages)
- "Create a histogram": Applies To includes 2016, 2019, 2021, 2024, 365; upper bin bound included.
- "Create a box and whisker chart": Applies To includes 2016-365; Inclusive/Exclusive median defined for odd N only.
- "Create a Pareto chart": Applies To lists only 2024, 2021, 365 (iPad/iPhone); no introduction date stated.
- "Create a treemap chart in Office": Applies To 365, 2024, 2021; no 2016 statement beyond an image caption.
- "Create a sunburst chart in Office": Applies To includes Excel 2016.
- "Change how rows and columns of data are plotted in a chart": default-plot rule and equal case; Applies To 365, 2024, 2021.
- "Create a chart from start to finish": Alt+F1 confirmed; Applies To 2016-365 (F11 not mentioned).
- "Available chart types in Office": gives no introduction versions except Dynamic charts (2024).
- W3C "Understanding SC 1.4.3 Contrast (Minimum)": 4.5:1. NEI "Color Blindness": about 1 in 12 men.
- Google "Add & edit a chart or graph" (answer 63824): lists waterfall, histogram, candlestick, treemap; mentions error bars; no gauge/geo/box/funnel/SPARKLINE.

## Still unverified (left labelled)
- Pareto and treemap in Excel 2016/2019 (Microsoft pages silent or list only 2021+); switch Row/Column and data labels on 2016/2019.
- F11 chart sheet, Quick Analysis Ctrl+Q, Google Sheets Timeline/auto-refresh/gauge/geo/box-plot claims, Excel quartile method vs QUARTILE.INC/EXC for the box chart, Excel for the web limits, Power BI licensing, 10-million-cell Sheets limit.
- XLOOKUP is not used in this part; no conflict statement needed.

## Unresolved / report only
- Q35's separate Q1-style version statements are consistent now; Q1 still points to Q35 for detail.
- Q4/Q6/Q9/Q27 reconstructed data are illustrative, not the author's original rows; the printed results were preserved.
- Order/numbering fine: Q1-Q54 continuous; stars descending. No duplicate questions (Q21/Q46 overlap on OFFSET vs Table is intentional).
- "Asked at" lines all claim only what the sources file supports.
