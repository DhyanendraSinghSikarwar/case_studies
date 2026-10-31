# Book 6 Part 6 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five answer agents). Scope: 45 questions, Q1-Q45 (stakeholder conflicts and trade-off decisions). No salary figures; all numbers are invented illustrative numbers.

## Process
Five agents answered Q1-9, 10-18, 19-27, 28-36, 37-45; merged by heading: 45 of 45 merged, 0 skipped, 0 pending. All five agents stopped once at the spend limit and were resumed after the reset; finished work on disk was kept. Four agents were re-run on their own questions after prompt corrections (Q4; Q13/Q14/Q15; Q26; Q43/Q44).

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q45; star order and counts 15 / 20 / 10 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 45 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 45 of 45 exit 0 (every question has a numeric Code block; none uses "Not applicable") |
| Cross-references (Book 1 Part 1 Q7, Part 3 Q1 and Q41, Part 10 Q9; Book 6 Part 4 Q12; in-part Q40) | headings grep-checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, question_index.md, index_rows.txt)
- Q4: net effect assumes the click-through gain passes through to conversions one for one (stated in the prompt; the 60% pass-through case, -0.93%, is a sensitivity).
- Q13: the four-fifths rule is an employment-selection guideline, so the prompt now says "a four-fifths style screening heuristic".
- Q14: the 450,000 is an upper bound (assumes supply ordered to the forecast and recovered none); prompt now says "up to 25 each ... (450,000 at most)".
- Q15: the 94% is a pilot sample rate projected to monthly volume; prompt now says so (30,000 wrong answers projected, 600,000 a month).
- Q26: three definitions are two changes; the prompt now says 9 days, 45% of the sprint (6 days, 30%, if the first build was planned work).
- Q43: "2 AUC points better" became "an AUC 0.02 higher on a holdout, with a paired bootstrap interval that excludes zero" (simulated gap 0.020, 95% CI 0.014 to 0.028).
- Q44: the original recall and precision gave fractional items; the prompt now has X at 60% recall and 80% precision (cost 41,500) and Y at 75% recall and 75% precision (cost 27,500).

## Findings kept in the text
- Prompt numbers recomputed in code for all 45 questions, for example Q5 3% of rows is 3.09% of the corrected revenue, Q10 build 1,350 vs vendor 1,200 with break-even 3.6 years, Q12 greedy by value per week gives 470 but the best plan is A plus B at 480, Q21 Wilson interval 1.72% to 5.17%, Q22 break-even 10,000 million tokens (3.33x today), Q28 family-wise error 22.6%, Q36 "predict none" and a useful model both score 99% accuracy.
- Gaps handled by stated assumptions in the answers (prompts left as is): Q31 "approval-rate gap" is a raw gap, Q32 no size given for the small-creator gain, Q35 no sample size or interval for the flat test, Q39 sole-attributable 1.8M equals the cost so ROI is exactly 0% on that basis, Q24 single-feature top reasons varied across retrains while the group-level reason was stable.

## Not run / hedged
Judgement parts are spoken advice with weak-versus-strong sentences; every numeric trade-off is reproduced in code. Evidence: WebFetch unavailable, 8 search snippets; pressure to inflate metrics, headcount disputes, ML versus rules politics, AI-written analysis review and several one-star items are editor-designed; see research_notes/Book6_Part06_sources.md.
