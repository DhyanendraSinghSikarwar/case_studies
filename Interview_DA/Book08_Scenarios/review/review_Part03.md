# Review of Book 8 Part 3 (Dashboard and report scenarios), Wave C

## Counts
- Answers checked: 70 of 70 (reasoning, honesty, template, style).
- Answers with numbers recomputed by code from the question data: 41 (Q1, 4, 7, 9 to 13, 16 to 19, 21, 28, 30 to 32, 34 to 40, 48 to 51, 58, 60, 61, 68, plus the mini-examples in Q5, 15, 33). Script: scratchpad C08_Part03/chk.py.
- Answers wrong or changed: 8 for substance (Q15, 17, 37, 60, 61 and wording in Q65), plus 3 label-only edits (Q5, 33, 45).
- Structure: all 70 have Asked at, interviewer check, Say this, Likely follow-ups and Common mistakes. No ANSWER_PENDING. No tables, so no table-spacing issue. Code fences balanced (2 = one DAX block, Q65). No em dashes in answer text (only the part-title line).
- "Asked at" claims match research/Book08_Part03_sources.md and research/interview_processes.md (Deloitte USI RLS/Power BI optimisation/SUM vs SUMX, Cognizant stakeholder management, Prepfully Deloitte/Apple unverified). No change needed.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q17 | Said "about 35 customers (or more, if some appear in three regions)". The 35 is the excess of row sum (325) over distinct total (290), so it is an upper bound on multi-region customers; a customer in three regions adds 2, so there would be fewer, not more. Say-this also stated exactly 35. | Result and Say-this reworded to "at most 35 customers (fewer if some appear in three regions)". |
| Q15 | Script said 4,100 to 4,180 is "80 late-entered orders; the rest is a definition fix", but 80 is the whole difference, leaving nothing for "the rest". Numbers not labelled illustrative. | Now 50 late orders plus 30 from the definition fix, labelled illustrative. |
| Q37 | Result and stakeholder script said North's share "lies between 40% and 45.5%". 45.5% is the proportional-allocation case, not a bound; if all 12 lakh Unknown were North, its share is 52%. | Range corrected to 40.0% to 52.0%, with 45.5% stated as the proportional case; stakeholder script updated. |
| Q60 | Premise problem not diagnosed correctly: four department figures sum to 1,170 and the 20 have a blank department, so they cannot be "inside those departments in the export" and also blank. | Premise caution rewritten: if blanks were a separate row the export would total 1,190 (40 unexplained); the consistent reading is a failed department lookup in the dashboard, to be confirmed by comparing per-department counts. |
| Q61 | "0.77% of the dashboard figure" is wrong rounding (6,500 / 8,36,500 = 0.777%, which rounds to 0.78%). | Corrected to 0.78% (0.777% unrounded). Result line clarified as % of Finance's figure. |
| Q65 | DAX behaviour (ALL, ALLSELECTED) stated as fact without label. | Added "from memory, unverified, test with a slicer selected". |
| Q5, Q33, Q45 | Invented example numbers not labelled illustrative. | Labelled "illustrative". |

All other figures matched the code: Q1 (400; 4.1% / 3.9%), Q7 (3,500; 38.9%; 28.0%; 1.39), Q9 (52, 47, 1,201, 5), Q10 (6 lakh; 1.3%), Q11 (905; +85; 10.4%), Q12 (1,400; 10.7%), Q16 (18.0%, 14.4%, 12.0%, 3.6 pp), Q18 (7,40,000; 48%; 700 rows), Q19, Q21 (3.5%, 4.19%), Q28, Q30, Q31 (99; 100.1), Q32 (70; 94), Q34, Q35, Q36 (-28%; +5.9%), Q38, Q39 (115,068; 0.64%; 2.7%), Q40 (10 s; 13 visuals), Q49, Q50 (3.8%), Q51, Q58 (540; 380; 96%), Q68.

## Unresolved items
- Q40: the answer's own caveat notes the sum-of-visual-times model is a simplification; kept as is.
- Q65: the question says every row shows 100% after a selection; with ALLSELECTED a single selected category is legitimately 100% (the answer covers this in follow-up 2). Left as is.
- Q60 premise remains ambiguous by construction of the question; answer now states both readings and asks the candidate to confirm.
- Ordering/numbering: stars descend and numbering is continuous (checked Q1 to Q70); no problem found.

## Duplicates / overlap (report only)
- Q9 (HRIS vs payroll), Q60 (HRIS vs dashboard headcount) and Q50 (as-of headcount) are close cousins within this part; each tests a different cause, acceptable.
- Q4 (5s to 40s slow), Q13 (refresh slow), Q26 (200M rows) and Q40 (24 visuals) overlap with Book 4 Power BI performance parts; this part keeps the on-the-job angle (per its stated boundary). Possible overlap of Q16 (attrition denominator) and Q30 (percentage vs pp) with Book 5/6 and Book 8 Part 4; not checked against those files.

## Claims left unverified
- Tool features (Power BI Performance Analyzer, incremental refresh, query folding, DirectQuery, ALLSELECTED, Tableau performance recording) are described from general knowledge; most carry "confirm with admin / from memory" notes, none verified here (no web).
- Deloitte/Apple/Cognizant "asked at" mentions remain anonymous and unverified, as labelled in the answers.
- DPDP Act mention in Q57 is already labelled "from memory, unverified" with a pointer to legal.
