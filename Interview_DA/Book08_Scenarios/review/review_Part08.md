# Review: Book08 Part 08 (Project deep-dive)

## Counts
- Answers checked: 62 of 62 (all headings, header lines, structure blocks, follow-ups and mistakes lines present; star/difficulty order is correct).
- Answers whose numbers were recomputed by code: 40 (every answer with figures: Q1, Q4, Q5, Q7, Q8, Q9, Q12, Q13, Q15, Q18, Q21-Q26, Q28, Q35, Q37-Q40, Q42-Q45, Q47-Q49, Q51, Q53, Q57, Q60, Q62, plus Q17, Q19, Q27, Q33). Script: scratchpad C08_Part08/c.py.
- Answers wrong or changed: 9 numbered fixes below (Q1, Q4, Q22, Q27, Q36, Q38, Q40, Q53, plus clarity edits listed). All arithmetic otherwise reproduced (13.44%, 38.9%, 35.0% vs 9.66%, 14.00/14.19/13.82/14.80%, 2,400 unique, 22% vs 9%, 11.46%, 15% vs 7.5%, funnel 25/40/30/80/2.4%, precision 30% and recall 66.7%, cost of attrition 1.95 lakh per leaver, 2.34 crore, 4.9% of payroll, range 1.89-3.24 crore).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q4 | Illustrative data said 1,480 rows with 40 transfers, but Q5 uses 90 exact duplicates plus 40 transfers giving 1,350; Q4 alone implied 1,440 | Added the 90 duplicates and the 1,350 result (1,480 - 90 - 40) |
| Q38 | Say-line said look first at interview-to-offer, while the working looked first at screening and offer-to-join | Say-line now matches: screening (750 of 1,000) first, then the 6 lost offers |
| Q53 | Example said the join "doubled rows" but headcount only rose 1,200 to 1,250 | Reworded to "duplicated some rows"; added "say only if it happened to you" |
| Q27 | Say-line named "one year of data" and an unverifiable voluntary definition; the illustration is about 18% blank exit reasons | Say-line aligned to the free-text exit-reason weakness |
| Q22 | 2,400-employee export vs average headcount 1,500 looked contradictory | Stated the export holds 2,400 unique employees including past leavers (consistent with Q25) |
| Q1 | "25 seconds x 6" does not fit "two minutes"; HRIS undefined | 20 seconds each; HRIS explained at first use |
| Q36 | "Five people" minimum group size stated as common fact | Labelled "from memory, unverified", policy choice |
| Q16, Q40, Q23, Q35, Q44 | Jargon unexplained (logistic regression, stratified split, regretted attrition, service account, view); time to hire definition varies | One-line plain explanations added; time-to-hire definitions flagged as company-specific |

## Checks passed
- Premise problems: Q25 (two kinds of repeats, 2,400 unique), Q28 (flip vs 12% target), Q26 (correlation, 13 percentage points not percent), Q49 (10% denominator trap), Q48, Q50 are correctly diagnosed with assumptions stated.
- Honesty: every "Asked at" is "commonly asked (no company-specific report found)" with only source-supported extras (about 14 profiles, Flipkart/Meesho prep reports, Infosys AI anecdote), all marked unverified. Model answers carry "Illustrative project, replace with your real one" and "Do not claim unless true" or "say only if true". Privacy answers (Q36, Q56) defer DPDP and legal details.
- Style: no em dashes in answers (one in the part-title line, allowed); no code fences or tables; no pasted scripts.

## Unresolved / report only
- Overlap: Q1 vs Q22 (project walk-through); Q4 vs Q24 (data fitness and cleaning); Q15 vs Q57 (quantified claims); Q36 vs Q56 (privacy/ethics); Q9/Q24/Q25 reuse the transfer-duplicate story (intentional continuity). Possible overlap with Part 09 behavioural stories and Book 11 not checked.
- Illustrative project figures differ across clusters (Q57 uses 2,500 records and 120 duplicates, Q47 130 duplicates, Q44 12,000 rows); they are separate invented examples, but a candidate should use one consistent real project.
- Q35 and Q42-Q45 present some narrative details (HR ranked metrics, usage counts) in first person without an inline illustrative tag; covered by the "Do not claim unless true" lines.
- Q1 headline "about 3.5 times" is 3.6 by calculation; left as a rounded spoken figure.

## Unverified claims left
- Prep-site and internal-compilation frequency claims (about 14 profiles; prompts existence); DPDP/GDPR specifics (not stated); Power BI usage-report availability (flagged "confirm"); minimum-group-size conventions; cost-of-attrition percentages (labelled exercise values, confirm with finance).
