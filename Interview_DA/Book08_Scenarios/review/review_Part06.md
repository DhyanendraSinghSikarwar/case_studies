# Review of Book 8 Part 6 (Wave C)

File: Book08_Scenarios/Book08_Part06.md. Scratch script: /tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C08_Part06/v.py (independent recomputation, written before comparing with the text).

## Counts
- Answers checked: 92 of 92 (headings, numbering, stars and order untouched; no ANSWER_PENDING).
- Answers whose numbers were recomputed by code or exact hand arithmetic: 66 (all 43 with inline data plus every answer with a worked number, including z, Fisher, Wilson, NPS standard errors, correlations, price-volume splits, mix effects).
- Answers with a wrong figure: 0. All stated figures matched the recomputation (including z 1.27 / p 0.20 in Q17, Fisher p 0.17 in Q30 and 0.03 in Q56, Wilson ranges in Q57, correlation 0.80 / 0.997 in Q68, z 2.35 in Q76).
- Answers changed: 16 (Q16, Q17, Q22, Q24, Q30, Q33, Q38, Q42, Q43, Q51, Q56, Q57, Q60, Q75, Q76, Q77), all for reasoning, premise handling or clarity; plus blank lines after 41 tables.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q17 | "much more than 10,000 per arm" was vague; z and p unexplained | Added computed need (about 48,000 per arm, 80% power, 5% level); glossed z and p-value |
| Q16 | Follow-up said acceptance was lower only for portal; agency is also 60% | Follow-up now names portal and agency |
| Q22 | Muddled "30% drop is either like-for-like or off" | Spelled out: a -30% on a 12-day versus 30-day view implies run-rate +75% (0.70 / 0.40), so implausible |
| Q24 | Sample-size sentence conflated two ideas (1,300 for a +/-5 range vs detecting a 7-point fall); "400 to 1,300" advice inconsistent; standard error unexplained | Recomputed: about 1,230 for +/-5, about 2,500 per quarter to detect 7 points; advice reworded; standard error glossed |
| Q30 | Fisher test unexplained | Plain-words gloss (p 0.17 confirmed; triple-sample p 0.008 confirms follow-up) |
| Q33 | Premise: definitions table missing; tax test text vague; bridge silent on tax | Tax check now a flat-share test (0.5 / 10.4 = 4.8%); bridge labelled invented and same-tax-basis assumption stated |
| Q38 | Premise note wrongly said the question gave only the current mean (it says flat at 32 both periods); overclaimed "slow orders must have got slower" | Removed the wrong note; reasoning restated (middle order faster, upper half slower on average), softened to "probably", percentiles to confirm |
| Q42 | Cause of the 5 gap stated as fact | Marked as likely cause and hypothesis (500+40-20-5+3-8 = 510 confirmed; 515 = transfers omitted) |
| Q43 | "After adjusting they are flat" is true by construction with one year of data (circular) | Say-line and Result now state this and call it a method illustration |
| Q51 | "One top customer is worth about 26 small ones" wrong for the average top-five customer (about 17) | Added step 6: C1 = about 26 average small customers; average top-five = about 17 |
| Q56 | Fisher test unexplained | Gloss added (p 0.031 confirmed) |
| Q57 | Wilson interval unexplained | Gloss added (ranges confirmed) |
| Q60 | t value unexplained; "0.30 is low for pay, yes" asserted as fact | Gloss added; follow-up reworded as an expectation to test |
| Q75 | Stakeholder script claimed "data load issue, not lost sales" before confirmation | Reworded to "may be ... not confirmed yet" |
| Q76 | z score unexplained | Gloss added (z 2.35, interval 0.12 to 1.38 confirmed) |
| Q77 | "The 200 extra heads added 6 crore (3.0 lakh each)" assumes existing payroll unchanged; Say-line "usually means cheaper roles" overclaimed | Assumption stated, framed as upper limit; Say-line softened, part-year hires and grade split named |
| All tables | 41 tables were followed directly by the next line (it would render as a table row) | Inserted blank line after each table |

## Premise problems checked
- Q42 (bridge gives 510, not 515): diagnosis correct, now hedged. Q44 (seven-day average but five days given): correctly handled by computing the 3-day average, 90 / 110 / 100. Q45 ("by region" but one total row): correct to treat as a total; price +10.0% confirmed, split +19 / -10 (alternative +20 / -11) confirmed. Q33 (missing definitions table): fixed as above. Q38, Q67 (both statements true: 66.7% and 75%), Q64 (open requisitions, so times are incomplete) all handled correctly.

## Unresolved / report only
- Ordering: stars descending and numbering continuous (Q1 to Q92), no issue found.
- Overlap: Q18, Q23, Q46 and Q78 all teach mix or Simpson-type reversals, and Q42, Q74, Q77 are all bridge checks; deliberate but worth a dedupe glance. Q41 (MAPE) and Q43 (seasonal index) may overlap with Book 5 or Book 6 Part 8 calculation drills; not compared.
- Several answers (Q1, Q11, Q13, Q22, Q26 to Q28, Q53 to Q55, Q58, Q65, Q75, Q89 to Q92) have no inline data; they use clarify, check, script structure instead of a single "Example" line. Left as is.

## Claims left unverified
- All "Asked at" lines say "commonly asked (no company-specific report found)" and prep-site claims carry "(unverified)", consistent with research/Book08_Part06_sources.md. The 80% rule (Q30), benchmark mention (Q70), Granger assumptions (Q90) are labelled from memory or unverified. Rules of thumb (30 surveys in Q52, 15 to 20% customer cap in Q51, shrinkage weights in Q81, staffing 80% occupancy and 30% shrinkage in Q54) are labelled illustrative or judgement. No law or tool-limit detail is stated as fact.
