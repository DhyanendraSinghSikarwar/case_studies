# Review of Book07_Part04.md (Business Metrics), Wave C

## Counts
- Answers checked: 87 (Q1 to Q87), all read in full.
- Answers whose numbers were recomputed by code (independent script in the scratch folder, run before comparing): 87 of 87 (concept-only answers had their illustrative numbers and examples recomputed; Q8, Q10, Q11, Q22, Q26, Q31, Q36, Q55, Q61 and similar contain only small illustrative figures, all checked).
- Answers with an arithmetic or logic error fixed: 6 (Q34, Q38, Q41, Q58, Q60, Q85).
- Answers changed in total (errors, clarity, honesty, style): 27.
- Everything else recomputed matched the written result (including Q13, Q18, Q20, Q28, Q42 to Q45, Q47 to Q49, Q63, Q64, Q69, Q80 to Q87).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q34 | Common mistake said "dividing by 160 (leaving out passives)"; leaving out the 50 passives gives 150 | Changed to 150 |
| Q38 | "Biggest loss at KYC (50%)": KYC is the lowest step rate, but the largest user loss is install to registration (4,000) | Rewritten with step rates 60/50/67% and both readings |
| Q41 | Garbled caveat ("a 30% offer acceptance gap, 30% decline offers") | Rewritten: acceptance 70%, so 30% of offers are declined |
| Q58 | Time to fill 1 March to 15 April stated as 46 days; correct is 45 | Corrected to 45 (time to hire 26 days was right) |
| Q60 | "Agency cost per hire rises 29% (1/0.7)"; 1/0.7 = 1.43, a 43% rise | Corrected to 43% (referral 18% was right) |
| Q85 | Decision rule claimed that churn rising by under 20% makes option 2 "match" option 1; 20% is the break-even against the baseline, and option 2 (2.0) trails option 1 (2.08) unless churn falls to about 4.8% | Rule rewritten |
| Q52 | Overall figure "36%" from cohorts of 40% and 30% with no weights given | Changed to "about 35% blends the two" |
| Q80 | Caveat wording "net of customers who joined and left" was misleading (lost count includes them) | Reworded |
| Q86 | "Asked at" overclaimed Flipkart/Meesho marketplace take-rate case reports | Limited to the Interview Query Flipkart trade-off guide, stated no report of this question found |
| Q46 | "Asked at" said PhonePe "report KPI and metric rounds"; the notes support only a prep guide mentioning funnel metrics | Reworded, marked unverified |
| Q23 | Real-world claim about ride-hailing usage frequency stated as fact | Marked as assumption, unverified |
| Q56, Q71, Q75 | Delivery-promise time, download numbers and grocery usage example not labelled | Labelled assumed or illustrative |
| Q63 | Grammar ("A 8%", "an 10%") | Fixed |
| Q3, Q21, Q25, Q26, Q43, Q61, Q65, Q73, Q82 | Jargon not explained at first use: SaaS, recurring revenue, MECE, take rate, contribution margin, confidence interval, Simpson's paradox, 90th percentile, LAG(), MRR/GRR/NRR/expansion/contraction, AUC, burn/runway, EBITDA, funnel plot | Short plain-words explanations added |

## Checks with no change needed
- Template completeness: every answer has Asked at, interviewer check, Say this, follow-ups and traps, plus a structure block matching its type.
- Style: no em dashes in answer text (the part-title line keeps one); no code fences or scripts; no tables in the file.
- Sanity checks are genuine second routes in the cases checked (Q20 cumulative profit, Q47 revenue route, Q48 weighted average, Q49 ratio route, Q63 reverse decomposition order).
- Stated ranges and break-evens follow from the arithmetic (Q64 mix shifts, Q85 6.25% and 6%, Q86 2.44%).

## Unresolved or report-only
- Ordering and numbering: star and difficulty order is correct throughout (Q1-29 three-star, Q30-69 two-star, Q70-87 one-star; green, yellow, red within each); 87 answers, continuous numbering. Header says target 80, actual 87, consistent.
- Overlap within the part (kept, since headings are frozen): Q33 and Q34 (NPS definition versus calculation), Q13 and Q80 (churn arithmetic), Q19, Q20 and Q84 (LTV chain), Q4, Q14, Q48 and Q51 (CAC), Q12 and Q1 (stickiness), Q18 and Q40 (attrition). Likely overlap with Part 5 (root-cause cases) and Book 5 (A/B tests, DiD) is deliberately avoided by cross-reference only; not checked against other part files.
- Many answers end with the phrase "Verified by script"; it is true after this review but reads oddly for a candidate voice. Left in place; a later style pass could remove it.
- The "Likely follow-ups" label is inconsistent between "(1)" and "1)" styles across answers; cosmetic.

## Claims left unverified
- All "Asked at" lines rest on prep-site, snippet-level or candidate-report evidence in `research/Book07_Part04_sources.md` and `research/interview_processes.md`; none verified at a named company.
- All benchmarks (LTV:CAC 3:1, payback under 12 months, stickiness levels, Rule of 40) are rules of thumb, already labelled unverified in the text.
- Every rupee, user and rate figure in the answers is either an exercise input from the question or a labelled illustrative or assumed number; no real company statistic is stated as fact.
