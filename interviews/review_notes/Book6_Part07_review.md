# Book 6 Part 7 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five answer agents). Scope: 55 questions, Q1-Q55 (GenAI scenarios: hallucinations, cost, latency, evaluation). No salary figures; token prices are round illustrative numbers, not vendor prices; no benchmark claims.

## Process
Five agents answered Q1-11, 12-22, 23-33, 34-44, 45-55; merged by heading: 55 of 55 merged, 0 skipped, 0 pending. One agent was re-run on its own questions after prompt corrections (Q37, Q41). No spend-limit stops.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q55; star order and counts 18 / 25 / 12 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 55 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 55 of 55 exit 0 |
| Cross-references (Book 2 Part 1 Q6, Q19, Q24, Q32; Part 2 Q1, Q5, Q17, Q21; Part 3 Q36; Part 9 Q4, Q5, Q6; in-part) | headings grep-checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, question_index.md, index_rows.txt)
- Q18: two online readings for three releases were ambiguous; the prompt now says 61% before and 61.5% after the three releases, on 20,000 conversations a month in each period.
- Q37: the "20,000 tokens if no history were resent" baseline omitted each turn's own 300 new tokens, and "t-1 earlier turns" excluded the current turn; the prompt now counts the current turn (total 83,000 tokens, 3.19x against a 26,000-token baseline).
- Q41: the 5-day gap understates the overrun; the prompt now also asks for the day the last backup copy expires if live data is deleted on day 1 (day 36).

## Findings kept in the text
- Prompt numbers recomputed in code for all 55 questions, for example Q3 the three cost levers overlap (standalone 15,435, combined 12,141), Q5 the best filter threshold flips with the cost ratio, Q7 +15 net (86% to 89%) is not significant on a paired test (exact McNemar p = 0.151), Q16 24,500 is a sample projection (Wilson 17,100 to 34,800), Q35 the cascade's mean improves 2.5 s to 1.8 s while p95 gets worse, Q43 the chance of seeing 100 failures in 5,000 answers is about 51%, Q50 the valid range is 354 to 418 (78 plus 400 times the Wilson interval), Q52 break-even 18.5% utilisation is a floor, Q53 overlapping Wilson intervals do not mean no difference (Newcombe CI 2.9 to 23.0 points), Q55 thresholds 0.7 and 0.9 are almost a tie (2.08 vs 2.13; cross at wrong-answer cost 21.05).
- Wording looseness handled in the answers (prompts left as is): Q1 "55 of 100" is a failure share, Q4 time to first visible text needs streaming at the client, Q12 83% equals the old prompt's own second run, Q25 input-only cost, Q27 mean versus p95, Q29 parallel moderation still 100 ms over budget, Q30 and Q32 how items were chosen, Q46 "one point or more" with integer scores, Q48 the other 99,000 users simplification.

## Not run / hedged
Provider features (schema-constrained output, minimum cache lengths) are labelled editor knowledge, not tested here. Evidence: WebFetch unavailable, 7 search snippets; prompt versioning and rollback, API versus self-host break-even, long context versus retrieval, DPDP specifics, thumbs-up bias and semantic-cache incidents are editor-designed; see research_notes/Book6_Part07_sources.md.
