# Book 6 Part 8 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five answer agents). Scope: 45 questions, Q1-Q45 (MLOps incidents: pipeline failures, rollback, drift). No salary figures; all numbers are invented illustrative numbers.

## Process
Five agents answered Q1-9, 10-18, 19-27, 28-36, 37-45; merged by heading: 45 of 45 merged, 0 skipped, 0 pending. Four agents were re-run on their own questions after prompt tightening (Q4/Q7, Q10/Q12/Q14/Q15/Q16, Q19/Q22/Q25, Q29/Q30/Q34). No spend-limit stops.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q45; star order and counts 15 / 20 / 10 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 45 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 45 of 45 exit 0 |
| Cross-references (Book 4 Part 1 Q5, Q11; Part 2 Q27; Part 3 Q10; Part 4 registry; Part 5 Q3, Q6; Part 6 Q9, Q17, Q40; Part 7 Q12; Part 8 Q7, Q27; Book 6 Part 2 Q1, Q45; Part 7 Q25; in-part Q18) | headings grep-checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, question_index.md, index_rows.txt)
- Q4: "paged almost every day" understated the stated assumptions (48 expected false alerts a day, 87% of hours with at least one alert); now "several times a day, nearly every hour".
- Q7: "an average of 0.08" is now "a mean absolute difference of 0.08 in score per request".
- Q10: 2.2% is a share of days; now "about 2.2% of rows if volume per day is equal".
- Q12: 40 calls per second is now "40 original requests per second".
- Q14: "with only 9 errors" (pooled z 2.37, Fisher p 0.039, borderline).
- Q15: holdout now "10% positives, 1,000 rows" (AUC standard error depends on it).
- Q16: decision threshold stated as 0.5.
- Q19: baseline is now "the mean of the same hour over the previous 7 days".
- Q22: 3.6 standard errors holds only if the 2% baseline is treated as exactly known; about 2.4 against a concurrent control of 10,000 requests.
- Q25: "may make each day depend on the stored output of the previous day" (120 minutes if independent, 360 if chained).
- Q29: now asks for an estimate and how reliable it is (the 600 is a projection).
- Q30: the feature is now stated to be a running counter that does not expire old events (a true 60-minute window would age duplicates out within an hour).
- Q34: the reference set is now stated as 2,000,000 rows (critical KS D 0.00195; 0.0063 for a 100,000-row reference).

## Findings kept in the text
- Prompt numbers recomputed in code for all 45 questions: for example Q37 225,000 minus 200,000 is 11.1% of demand, Q38 4,000 is a worst-case bound (2.67 times capacity), Q39 one whole miss is allowed in 28 (27 of 28 is 96.4%), Q40 6 hours expected and 12 worst case, Q45 6.67 times average value per request.
- Hedges in the answers: registry alias caching and overwrite support, PSI above 0.2 as a rule of thumb, provider rate-limit behaviour, ONNX and safetensors claims, scheduler options and exactly-once behaviour are labelled editor knowledge; simulations (Q12 retry collapse, Q13 top-1% share 27% to 53%, Q38 never-recovers toy model) are labelled synthetic; legal and regulatory points go to compliance with nothing quoted.

## Not run / hedged
Evidence: WebFetch unavailable, 8 search snippets; no real public ML incident postmortem found; error-budget arithmetic, feedback-loop exposure concentration, secrets-leak response, fallback game days and the feature-view rollback deadlock are editor-designed; see research_notes/Book6_Part08_sources.md.
