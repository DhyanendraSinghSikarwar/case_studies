# Review: Book 5 Part 11 (Stats in Excel & Python)

## Counts
- Answers checked: 34 (Q1-Q34). Python snippets run: 33 blocks (all but Q23, which has no Python and points to Q24). All 33 reproduce the pasted output after the Q27 spacing fix (pandas 3.0.5, numpy 2.5.3, scipy 1.18.1).
- Answers edited: 12 (Q10, Q12, Q17, Q18, Q19, Q22, Q23, Q25, Q27, Q29, Q30, Q34). No number, output or formula was wrong.
- All worked numbers re-derived independently (t-tests, chi-square, CI, regression, percentiles, normal/binomial/Poisson, skew/kurtosis, ToolPak confidence level 4.4027).
- No em dashes in answer text; 132 code fences (balanced); no ANSWER_PENDING; template fields present in all answers.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q10 | "`.EXC` works with positions 1 to n+1" was confusing/wrong | Now says position = p x (n+1) must lie between 1 and n, hence #NUM! outside 1/(n+1) to n/(n+1) |
| Q12 | "imputing before splitting data" was unexplained jargon | Explained in plain words (information leaks into the test data) |
| Q17 | Accenture claim said "Bangalore" | Narrowed to the one Jan 2026 Bangalore-Rural Glassdoor report in interview_processes.md |
| Q18 | Asked-at pointed at "Part 11 sources"; no Excel counterpart | Cites interview_processes.md accurately; added Excel QUARTILE.INC note pointing to Q17 |
| Q19 | STANDARDIZE labelled "Excel 2010+" | Corrected: exists in all versions |
| Q22, Q25, Q27, Q29, Q30, Q34 | Setup lines without the plain-English comment (style_guide Section 10) | Added comments above each step |
| Q23 | p-value definition loose ("difference this large") | Now "at least this large" and states it is not the probability the groups are the same |
| Q27 | Pasted covariance matrix column misaligned by one space | Aligned to real output |

## Unresolved / report only
- Q23 has Excel only; Python run is in Q24 (cross-referenced). Not duplicated, by design.
- Overlap: Q6/Q8 (STDEV.S vs ddof), Q7/Q30 (correlation), Q17/Q18 (IQR), Q21/Q22/Q34 (regression), Q31/Q1 (mode) overlap with each other and likely with Book 5 descriptive-stats, outlier and regression parts; check cross-part duplicates at integration.
- Ordering: stars sorted correctly (3-star Q1-Q8, 2-star Q9-Q26, 1-star Q27-Q34). Within star 2, difficulty order is 🟢 then 🟡 (OK). Q8 is 🟡 inside the 🟢 group but is last in the 3-star block (OK).
- Header says target 30, actual 34 (consistent with file).

## Claims left unverified
- All "Asked at" lines are generic ("commonly asked, no company-specific report found"); based on snippet-level search per research/Book05_Part11_sources.md. Only the Accenture Bangalore-Rural basic-statistics mention (Q17/Q18) is source-backed.
- No Excel available: every Excel formula is labelled "not run in Excel here"; logic verified against Python. Excel version claims (2007/2010/2016/365) are from memory, unverified.
- Q29 sample rows and Q31 dtype label are pandas/numpy-version dependent (already stated in the text).
- Q29 department codes S/H/F (F = Finance) are illustrative.
