# Book 6 Part 3 review (Wave C)

Date: 2026-10-30. Reviewer: lead session (independent of the five answer agents). Scope: 50 questions, Q1-Q50 (imbalanced, noisy and missing data situations). No salary figures; Example numbers are invented illustrative numbers.

## Process
Five agents answered Q1-10, 11-20, 21-30, 31-40, 41-50; merged by heading: 50 of 50 merged, 0 skipped, 0 pending. No spend-limit stops.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q50; star order and counts 16 / 23 / 11 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 50 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 50 of 50 exit 0 |
| Cross-references (Book 1 Parts 2, 3, 4, 5, 11, 12; Book 6 Parts 2; in-part) | headings grep-checked by the agents |

## Correction to a frozen prompt
Q33: 800 real plus 50,000 synthetic fraud rows give 50,800 fraud rows of 450,000 (11.3%), not a balanced set (balance would need 398,400 synthetic rows); prompt now says "to make the data more balanced". Applied to the part file, agent heading, qs.py, question_index.md, index_rows.txt.

## Findings kept in the text
- Arithmetic checked in code for the prompts of every question; simulated numbers that differ from the prompt (labelled illustrative): Q3 PR-AUC 0.143 vs 0.18; Q8 row split 0.668 vs group split 0.571; Q9 random 0.813 vs time 0.776; Q16 0.833 to 0.786; Q31 leaky 0.861 vs 0.782; Q26 response rates 4.1% and 3.8%.
- Q1: accuracy cannot separate a good model from a useless one (two models with 4,000 errors each, recall 0.75 versus 0); Q9: a 50% random test set is just as optimistic as a smaller one, so the manager's "more reliable" claim is wrong; Q6: the 0.50 mean score only holds for a weak-signal model.
- Honest negative findings reported as observed: Q17 plain, class weights, undersampling and SMOTE showed no real difference in a simulated linear setup; Q22 plain, weighted and focal losses ranked about the same while weighted and focal inflated probabilities; Q33 the synthetic-row gain is within noise and fitting the generator on all frauds leaks (PR-AUC 0.311); Q34 drop, relabel and no cleaning gave the same accuracy (only 13.9% of true noise flagged); Q32 weighted voting beats majority on coverage, not accuracy; Q44 the target-informed imputer cost is small in a linear toy (R2 0.763 vs 0.768) though its coefficient is wrong (1.209 vs 1.000).
- Q37: native tree handling of missing values was not demonstrated (no sklearn); the text says "untested here".
- Wording ambiguities answered as clarifying questions: Q24, Q25, Q27, Q29, Q38, Q43, Q44.

## Not run / hedged
Judgement-only questions say "Not applicable". Evidence: WebFetch unavailable, 11 search snippets; positive-unlabelled/delayed labels, label-noise estimation, subgroup under-representation, partial pooling and AI-era items are editor-designed; see research_notes/Book6_Part03_sources.md.
