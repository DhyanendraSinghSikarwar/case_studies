# Book 6 Part 4 review (Wave C)

Date: 2026-10-30. Reviewer: lead session (independent of the five answer agents). Scope: 55 questions, Q1-Q55 (experiment design and ambiguous A/B results). No salary figures; Example numbers are invented illustrative numbers.

## Process
Five agents answered Q1-11, 12-22, 23-33, 34-44, 45-55; merged by heading: 55 of 55 merged, 0 skipped, 0 pending. Three agents were re-run on their own questions after prompt corrections (Q1/Q8, Q43). No spend-limit stops. A stale `.git/index.lock` from a crashed `git add` was removed once.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q55; star order and counts 18 / 25 / 12 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 55 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 55 of 55 exit 0 |
| Cross-references (Book 1 Part 10, Part 14 Q15 and Q33; in-part) | headings grep-checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, question_index.md, index_rows.txt)
- Q1: the stated p = 0.03 did not follow from 5.0% vs 4.8%; the prompt now uses 5.1% vs 4.8% (z = 2.19, two-sided p = 0.029).
- Q8: "p < 0.001" for 4.00% vs 4.05% on 2,000,000 impressions per arm is wrong (z = 2.54, p = 0.011); the prompt now says p = 0.01.
- Q43: "100,000 users per arm" did not match the platform counts (50,000 per arm); fixed.
- Q21: exact sample size for 2.0% to 2.1%, 80% power, two-sided 5% is 315,206 per arm (79 months at 4,000 per arm per month), not 300,000 / 75 months; fixed.

## Findings kept in the text
- Prompt claims verified in code: SRM chi-square 160 (Q1), 64% false-positive chance for 20 metrics (Q2), Q5 interval -0.3 to +0.5 and about 159,000 per arm, Q6 revenue per visitor -1.06%, Q10 chi-square 7,200, Q14 4%/0.45 = 8.9% of Android events, Q15 z about 2.6 / p about 0.009, Q17 1 - 0.99^40 = 33.1%, Q19 P(>=3 of 40) = 32.3%, Q23 all-null chance of any p < 0.05 is 16.0% (shared control), Q27 design effect 1.98, Q29 19 x 3.7 rounds to 70 and a level comparison would show +71%, Q33 1.01^12 = 12.68%, Q38 cost multiple 6.0, Q44 about 128,500 per arm, Q53 410 to 435 passes.
- Honest findings stated in answers: Q41 with 16 units the smallest placebo p-value is 1/16 = 0.0625, so placebo tests cannot reach 0.05 and the design cannot separate +2.5% from zero (launch ranks first in about 10% of worlds either way); Q42 an early-session covariate pulls the estimate toward zero (0.62 vs true 2.0) with 0% interval coverage; Q46 the problem is differential logging after assignment, not an assignment SRM (logged split chi-square about 254); Q47 daily peeks give about 16% false stops against 3.9% at a single look; Q50 the 6x faster read-out holds only for heavy-tailed users (7.6x versus 1.5x for even users); Q52 naive bias runs opposite to the usual intuition in the toy auction (setup dependent); Q54 phi = 0.8 so each readout equals a + 0.8b.
- Wording ambiguities answered as clarifying questions: Q11 (invites versus joins), Q18 (users lost per arm), Q22 (which weekend days), Q24 (no page-view counts), Q25 (5% of all users is 9.5% of each arm), Q30 (treatment-versus-control reading), Q45 (single readout sees only half the interaction), Q49 (human pairs a subset or not). Q16's "roughly one in five" simulated at 21.8% (acceptable).
- Q12: the sources note's 119,000 per arm is slightly off; the code gives 122,123 per arm (12.2 days); the answer uses the code value.

## Not run / hedged
Judgement-only questions say "Not applicable". Evidence: WebFetch unavailable, 8 search snippets; logging bugs, long-term holdouts, bandits vs A/B, winner's curse, interference between concurrent tests, interleaving, surrogate metrics, hash-salt collision and uplift targeting without randomization are editor-designed; LLM themes rest on 2026 practitioner blogs; see research_notes/Book6_Part04_sources.md.
