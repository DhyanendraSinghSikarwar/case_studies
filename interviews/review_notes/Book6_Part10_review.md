# Book 6 Part 10 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 ("Design a solution end-to-end" open scenarios). No salary figures; all numbers are invented illustrative numbers; no legal or regulatory claim is stated as fact; no tool or version claims were made.

## Process
Four agents answered Q1-10, 11-20, 21-30, 31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. All four agents stopped once at the spend limit and were resumed after the reset (finished work on disk was kept). Every agent was re-run on its own questions after prompt tightening.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q40; star order and counts 14 / 17 / 9 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 40 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 40 of 40 exit 0 |
| Answer shape: 7-8 step spoken Approach with a pacing line summing to 45 minutes; one sizing or trade-off calculation per answer; weak versus strong sample answers | present |
| Cross-references (Book 6 Parts 1, 2, 3, 4, 5, 7, 9; Book 4 Parts 6, 8, 12; Book 1 Part 6 Q30; Book 2 Part 12 Q24) | headings grep-checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, question_index.md, index_rows.txt)
Arithmetic was right everywhere; the prompts were tightened where a base, a bound or an assumption was missing:
- Q1 capacity is 1.4 times the peak (4 instances, 5 with N+1); Q4 the latency budget is to the first token and the token counts are per chat summed over all its turns; Q6 orders outside the lunch window are ignored (23,333 in flight, 777.8 refresh and 788.9 total requests per second); Q8 the gain is the incremental open probability per push versus no push; Q10 all 3,000 monthly loans are thin-file and the 36,000 are approved loans.
- Q11 servers sized at full load within the latency budget, headroom stated separately; Q12 "an assumption" and windows whose transactions are all 30 or all 90 days old; Q13 typical (mean) latency and slack against the mean, and what the 95th percentile needs; Q14 mean concurrent calls, servers at full load; Q19 payload "upper bound"; Q20 the pilot covered 500 flagged would-be-return orders.
- Q22 distinct users across two arms over the run; Q23 scan cost proportional to rows read; Q28 2.4 calls of 6,000 tokens each (540,000 rupees a month, 9x over budget); Q29 liveness-pass count as a best case if the 95% held for new attacks; Q30 the audit size so that a true 2% rate yields at least one unsupported note with probability at least 95% (a tripwire, not an estimate).
- Q34 stock level to the nearest whole unit (105); Q35 "generated tokens"; Q36 memory in decimal GB (3.2 GB, 2.98 GiB); Q39 accounts within two hops (156; 780,000 lookups per second; exactly-two-hop reading 144 kept as a one-line note).

## Findings kept in the text
- Q9 the 0.4% from a 50,000-row sample is only 200 violations (95% interval 0.345% to 0.455%, minimum precision 51.7% to 68.3%); Q21 19% is a precision floor only at a full 3,000-case queue; Q26 the 3% and 1.5% are sample rates; Q38 97% from 400 replays has a Wilson interval 94.8% to 98.3% that crosses the break-even 96.15%; Q40 the best subset uses 34 of 36 person-weeks with almost no slack (the 80%-capacity plan is offered); Q20 the 80,000 unflagged orders return at 15.6% against a 16.7% break-even; Q17 a 20% per-update cap limits speed, not level; Q18 the 5.2e-7 bound is an expected count.

## Not run / hedged
Evidence: WebFetch unavailable, 10 search snippets; notification uplift targeting, resume matching, OCR extraction, vernacular search, low-bandwidth payload limits, Hinglish label planning, healthcare triage, claims-photo vision, KYC liveness, graph mule detection, catalogue enrichment, predictive maintenance and team planning are editor-designed; see research_notes/Book6_Part10_sources.md.
