# Review: Book 5 Part 4 (Probability & Bayes), Wave C

## Counts
- Answers checked: 71 of 71 (all seven template fields present in every answer).
- Python snippets run: 69 of 69 ran without error; every printed output matches the pasted output (checked by script, seeds reproduce) and the numbers quoted in the prose.
- Worked numbers re-derived independently (Bayes, EV, birthday, Monty Hall, odds ratio, Beta credible interval, HH/HT expectations, spam, taxi, funnel, etc.): all correct.
- Answers edited: 19 (all listed in the table below; edits are small).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q12 | Output showed floating-point noise "99.00000000000009" | Code now rounds; pasted output "99.0" (verified by run) |
| Q18 | `6 - first_pick - host_opens` is an unexplained trick | Comment now says the door numbers 1+2+3 add to 6 |
| Q33 | "Biggest leak is the interview" misleading (screening loses most people) | Now states highest drop rate (interview, 60%) vs most people lost (screening, 500) |
| Q37 | Output "0.08000000000000002"; abbreviated names, comments mixed into code | Code rewritten with descriptive names, one step per line, rounding; output and prose updated (run verified) |
| Q40, Q43, Q47, Q49, Q50, Q51 | Code began with bare input lines, no plain-English comment | Added a comment above the inputs |
| Q54 | Frequentist wording "if I repeated this survey forever, 30% would be leavers" was loose and slightly wrong | Rewritten: true rate is one fixed number, 30% is the estimate from this sample; "senior or analytics-firm rounds" claim removed (unsupported) |
| Q58 | Unused import `comb` | Removed |
| Q10, Q31, Q33, Q36, Q64 | Excel formulas not labelled "not run in Excel here" | Label added |
| Q62 | Excel formula not in code style; clumsy "Asked at" double parentheses | Formula in backticks; sentence cleaned, wording kept within the sources file |
| Q68, Q70 | Same double-parenthesis "Asked at" wording | Cleaned; no claim added or removed |

## Checks passed (no change needed)
- No em dashes in answer text (only the file title); code fences balanced (278); no tables needing a trailing blank line.
- "Asked at" lines only cite what research/Book05_Part04_sources.md supports (Tiger Analytics: Bayes/conditional probability, 5 Sundays; question-bank mentions for dice sum 7, independent vs exclusive, EV, expected flips); everything else says "commonly asked (no company-specific report found)".
- Excel functions: BINOM.DIST (2010+, labelled), SUMPRODUCT, AVERAGE, AVERAGEIF are correct.

## Unresolved / report only
- Output blocks use two formats: ```text (Q1 to Q18, Q55 onward partly) and an "Output:" label plus unlabelled fence (Q19 to Q54). Harmless but inconsistent; left as is.
- Q67 prints the same value twice for "Seniors only: P(both)" and "product" (true by construction in the example); the prose explains it, so left.
- Several snippets import numpy/scipy mid-script (Q39, Q46, Q61); works, but imports at the top would be tidier.
- Ordering/numbering: stars descend 3 to 1 in order; no gaps. Header says target 70, actual 71, consistent.
- Overlap with other parts (report only): Q46/Q65/Q71 expected-tosses family; Q12/Q13/Q35/Q36/Q69 all base-rate Bayes variants; Q54 and Q63 touch confidence intervals and logistic regression (other parts); Q48 binomial overlaps Part 3; Q57 variance overlaps descriptive stats parts.

## Claims left unverified
- Tiger Analytics reports (conditional probability, 5 Sundays), Wipro/EXL/TCS/PwC puzzle claim, Glassdoor quant pages, quantt and PracHub items are snippet-level in the sources file only; not re-verified (no web).
- Q63 "use odds ratio in case-control studies and logistic regression" and Q54 "frequentist standard in A/B testing" are general statistics knowledge, from memory, unverified against a source.
