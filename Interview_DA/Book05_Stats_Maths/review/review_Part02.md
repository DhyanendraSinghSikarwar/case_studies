# Review: Book 5 Part 2 (Descriptive Statistics), Wave C

Reviewer scope: `Book05_Stats_Maths/Book05_Part02.md` only. Snippets extracted and run with `python3 -I`; pasted output compared line by line.

## Counts
- Answers checked: 60 (Q1 to Q60). Python snippets run: 59, all 59 reproduce the pasted output exactly (seeded ones included).
- Every worked number re-derived independently (quartiles by interpolation, grouped median, combined SD, Welford, trimmed mean, percentile-rank/Excel PERCENTRANK logic, weighted and geometric means, c4 for n=5). No numeric errors found.
- Answers edited: 22 (Q4, Q7, Q8, Q10, Q11, Q13, Q14, Q32, Q35, Q44-Q52, Q57-Q60).
- Template: all 7 required fields present in all 60 answers. Em dashes in answers: none (title line only). Code fences balanced.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q4, Q7, Q8, Q10, Q11, Q13, Q14 | No plain-words line after the output (style guide Section 10) | Added a one-line plain explanation after each output |
| Q44, Q45, Q46, Q47, Q48, Q49, Q50, Q51, Q57, Q59, Q60 | Same: output followed straight by the Excel line | Added plain-words line |
| Q32 | "one month nearly doubled the average" overstated (2.4% to 4.0% is +67%) | Reworded to "lifted by about two thirds" |
| Q35 | Mean in the example is 5.1 but prose said "Average 6 would mislead"; "maternity-related medical leave" is not sick leave | Reworded to "a headline average near 6"; replaced with "a long illness" |
| Q46 | Prose blamed the gap between 1.77 and 2 only on small-company sampling; actually the simulated company SD was 11.08 (not 12) and finite-population effect | Explained both causes; combined prediction 1.76 verified by script |
| Q52 | Anscombe data and year given as fact with no source | Labelled "from memory, unverified", noting the output matches the published summary figures |
| Q57 | "a form of Simpson's paradox" is inaccurate (averaging ratios is a weighting error) | Changed to "related to Simpson's paradox" |
| Q58 | Example weak: mean (8.65) also happens to cover 90% of tickets, so it did not show why p90 is better | Added after-output explanation that this is luck of the data and that p90 is defined to carry the guarantee |

## Checks passed without change (notable)
- Q7/Q28/Q42 percentile logic: Excel PERCENTILE.INC and numpy linear agree; PERCENTRANK.INC(72)=5/9=0.555 (correctly flagged as different from 60); PERCENTILE.EXC at 0.9 on 8 values is #NUM! in Excel while numpy "weibull" caps at 120 (correctly stated).
- Q43 combined SD 7.861 matches pooled raw data; Q55 c4 factor 0.94 for n=5 correct; Q49 normal-data fence 2.698 SD and 0.698% flagged correct.
- Excel versions: STDEV.S, VAR.S, PERCENTILE.INC, QUARTILE.INC, MODE.SNGL/MULT stated as 2010+; Box-and-Whisker/Histogram charts 2016+ (from memory, unverified). All Excel formulas labelled "not run in Excel here".
- Q24/Q37: Python skew (scipy population formula) differs from pandas/Excel (sample-adjusted); Q24 states this, Q37 uses pandas and prints 2.09 correctly.

## Asked-at claims
All company statements match `research/Book05_Part02_sources.md`: Q10/Q49 (Glassdoor IQR Python-function report, company not stated), Q6 (Glassdoor title-only snippet), Q24/Q40 (single anecdote of an Indian company, unnamed), Q2 (Dataford), Q31 (Exponent snippet), Q1/Q5/Q12/Q13 (upGrad/365 Data Science snippets). Everything else says "commonly asked (no company-specific report found)". No invented companies or statistics found.

## Unresolved / report only
- Ordering: sequence follows star then difficulty rules; Q10/Q11 are 🟡 after the 🟢 Q9, consistent. Q39 (⭐⭐ 🟡) and Q40 (⭐⭐ 🔴) fine. No numbering problems found.
- Overlap with other parts: Q6/Q16/Q49 (outliers/IQR), Q12/Q55 (n-1), Q46 (standard error), Q13 (population/sample) will likely recur in the sampling/CLT and inference parts; Q30 z-score overlaps the normal-distribution part; Q41/Q57 averaging-ratios overlaps Excel/SQL aggregation books. Left in place for the dedupe pass.
- Code style: short names remain in a few spots (`data` in Q8/Q10, `q1/q3`, `x/y` in Q52 helper `describe`); judged acceptable as they are standard and commented.

## Claims left unverified
- Anscombe (1973) and the typed dataset values (Q52), Datasaurus Dozen mention (Q52), Excel 2016+ chart availability (Q11, Q19, Q59), "1.5 chosen by Tukey" rationale (Q49). No web access, so Excel behaviour was checked by logic against Python, not executed in Excel.
