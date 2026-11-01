# Book 6 Part 1 review (Wave C)

Date: 2026-10-30. Reviewer: lead session (independent of the five answer agents). Scope: 55 questions, Q1-Q55 (product metrics and metric drops). No salary figures; all numbers in Examples are invented illustrative numbers.

## Process
Five agents answered Q1-11, 12-22, 23-33, 34-44, 45-55; merged by heading: 55 of 55 merged, 0 skipped, 0 pending. No spend-limit stops.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q55; star order and counts 18 / 25 / 12 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 55 |
| At most one python block per answer, each re-run standalone with `python3 -I` by the lead | 55 of 55 exit 0 |
| Cross-references (Book 1 Part 10 Q3, Q6, Q8, Q10, Q12, Q13, Q14, Q16, Q17, Q19, Q24, Q27, Q28, Q42, Q44, Q49, Q56; in-part references) | headings checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, index rows)
- Q1: 1.00M to 0.98M to 0.90M is -8.2% week over week and -10.0% over two weeks; the prompt now says 10% over two weeks (8.2% in the latest week).
- Q6: ambiguous blended versus Android rate; the prompt now says Android conversion fell from 3.1% to 2.6% while iOS is flat.
- Q53: "average price per unit +2%" cannot give Rs 112 crore with +6% volume (100 x 1.06 x 1.02 = 108.12); prompt now says like-for-like price within each tier rose 2%. The answer shows the split 6.00 / 3.80 / 2.20 and the opposite order.

## Findings kept in the text
- Ambiguities left in prompts and handled in the answers as clarifying questions: Q27 (5% of what base), Q28 (fee or total revenue), Q29 (voluntary versus failed payments), Q31 (accuracy definition), Q37 ("usually moves 1.5%" read as standard deviation), Q45 (exact day 7 versus window), Q22 (counts versus rupees).
- Q32: the simulated session-timeout change gave +26.8% sessions per user against the prompt's 20%; the text says so.
- Q41: per-query standard errors come out too small (0.00250) against the user-level delta (0.00276). Q42: the built rule has recall 0.596, so it under-states abuse. Q12: month length accounts for about 3.2 of the 8 points.

## Not run / hedged
Q-scenarios that are purely judgement say "Not applicable". Evidence: WebFetch unavailable, 8 search snippets only; retention and cohort scenarios (Q9, Q20, Q26, Q33) and Q14, Q24, Q32, Q36, Q40, Q42, Q44-Q47, Q50-Q55 are editor-designed; see research_notes/Book6_Part01_sources.md.
