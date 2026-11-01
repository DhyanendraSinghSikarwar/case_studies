# Book 6 Part 2 review (Wave C)

Date: 2026-10-30. Reviewer: lead session (independent of the five answer agents). Scope: 50 questions, Q1-Q50 (model performance degraded in production). No salary figures; all Example numbers are invented illustrative numbers.

## Process
Five agents answered Q1-10, 11-20, 21-30, 31-40, 41-50; merged by heading: 50 of 50 merged, 0 skipped, 0 pending. No spend-limit stops.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q50; star order and counts 16 / 23 / 11 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 50 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 50 of 50 exit 0 |
| Cross-references (Book 1 Parts 3, 6, 7, 10, 11; Book 4 Parts 1, 6, 7, 8, 9; Book 6 Part 1 Q15, Q33, Q37, Q39; in-part) | headings grep-checked by the agents |

## Correction to a frozen prompt
Q48: "costs about 2% of the model's revenue benefit" is only an upper bound (holdout users still get the frozen model, so the real cost is 2% of the new model's gain over the frozen one); prompt now says "up to about 2%". Applied to part file, agent heading, qs.py, question_index.md, index_rows.txt.

## Findings kept in the text
- Prompt numbers checked in code: Q8 both aggregates 89.6%; Q9 precision 67.0% to 50.2% with FPR 0.5606%; Q17 z = 2.70, p = 0.0069 (not noise at the 5% level); Q28 1.5% apparent rate; Q32 z = 2.22, p = 0.027; Q41 prior estimate 0.19/0.70 = 27.1% (the expected flag rate at a 20% prior is 24%); Q42 optimum T* = sqrt(10) = 3.16 weeks.
- Simulations that only approximate the prompt's figures (the text labels them illustrative): Q5 AUC 0.862 to 0.835 (prompt 0.88 to 0.84), Q20 0.852 to 0.808, Q23 hit rate depends on the embedding mix, Q32-adjacent Q35 0.96/0.705, Q36 a base-rate fall alone explains 62% to 48%, Q45 judge 4.09 to 4.34.
- Ambiguities left in prompts and answered as clarifying questions: Q15, Q21, Q26, Q29, Q39, Q6; Q13's "excellent default prediction" cannot hold for AUC under range restriction (the answer says so); Q14 a fixed 0.5 threshold gives 18.7% recall at a 14% base rate; Q49 shrinkage toward old coefficients showed no clear gain over new-only in the seeded run (0.906 vs 0.903), reported as observed.

## Not run / hedged
Judgement-only questions say "Not applicable". Evidence: WebFetch unavailable, 11 search snippets; forecasting drift, adversarial fraud, calibration/prior shift and AI-era items are practitioner/vendor sources or editor-designed; see research_notes/Book6_Part02_sources.md.
