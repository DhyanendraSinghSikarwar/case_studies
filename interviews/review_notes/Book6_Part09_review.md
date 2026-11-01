# Book 6 Part 9 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five answer agents). Scope: 50 questions, Q1-Q50 (domain sets: fintech 13, e-commerce 13, healthcare 12, ads 12). No salary figures; all numbers are invented illustrative numbers; no legal or regulatory claim is stated as fact (answers say "ask compliance / legal / the regulator-facing team").

## Process
Five agents answered Q1-10, 11-20, 21-30, 31-40, 41-50; merged by heading: 50 of 50 merged, 0 skipped, 0 pending. Every agent was re-run on its own questions after prompt tightening. No spend-limit stops.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q50; star order and counts 16 / 23 / 11 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 50 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 50 of 50 exit 0 |
| Cross-references (earlier Book 6 parts, Book 1 Part 2 Q14 and Q28, Part 1 Q40, Part 3 Q23, Part 5 Q11) | headings grep-checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, question_index.md, index_rows.txt)
Arithmetic was right everywhere; the prompts were tightened where a base, a standard error, a bound or an assumption was missing or misleading:
- Q4 relative overbid now against the calibrated bid (25%); Q6 exposure is an upper bound on balances at risk (10,000,000) with the maximum loss at the stated loss per defaulter (8,000,000) kept separate; Q7 the 5% reserve is in addition to the 2% new sellers already get (5,000 lost orders); Q8 the stricter alerts are a subset of the current alerts; Q10 the 300-account holdout is small (95% interval about -0.7 to +10.7 points).
- Q11 "share of alert-followed events" (72%, not all events); Q12 invalid clicks are credited back (right bid is 2.0% of value).
- Q22 widget use was voluntary; Q23 retrospective counts come from a month in which all 10,000 alerts were reviewed; Q24 "if we assume all 600 recipients use the code" (the result flips below about 42% redemption); Q27 "10% of the 17,400 genuine customers" and block-band fraud counts from review and customer reports; Q29 "at least 100 expected events" (2,500 and 4,000 patients; 2,916 and 4,671 for a 95% chance of reaching 100); Q30 holdout drawn at random from the same lookalike audience before serving (95% interval on incremental conversions 331 to 669).
- Q34 loss from observed defaults at the assumed LGD (3,000,000 predicted, 4,500,000 observed, 1,500,000 shortfall); Q36 alert volume about 1,000 per 20,000 admissions (prevalence alone would only take PPV to about 25.3%); Q39 paused-region sales 4% lower than the kept regions' with-video level of 2,000,000 per region (4,000,000 attributable, four times the last-click credit).
- Q44 AUCs measured on different patient populations; Q45 standard error of the B-versus-A difference about 0.47 points (z about 1.07, not significant); Q46 the AUC lift is measured among the 70% with the features, on approved applicants only; Q47 the 35% is a minimum (85% upper bound if the 500 unflagged-chargeback flags were all fraud); Q49 paired comparison with 20 and 12 discordant positives (paired SE 0.014).

## Findings kept in the text
- Q2 logged position ratio 11.6 against a true examination ratio of 3 (ranker confounding); Q5 sample size uses an illustrative 5% checkout conversion; Q13 9.6% depends entirely on the assumed 3x ratio (ratio 1 gives 4.0%, 2 gives 6.8%, 5 gives 15.2%); Q14 flat hourly demand gives 557.1 uncensored against 442.9 in sales (20.5% understated), and the censored-normal fit gives an overconfident sd of 10; Q17 break-even bad rate 14.3% (profits 34.4, 41.525 and 40.6 million); Q18 interval 9.2% to 14.8%; Q33 any-error rate between 7% and 10% depending on overlap; Q38 best bid is a tie at 6 and 7 (both 1.80); Q43 about 10 million users per arm would be needed to detect a 0.5% GMV change; Q44 retraining at the low-ordering site does not recover AUC; Q50 the 7-day share rises to about 27% once the Poisson variation of the true count is included.
- Editor knowledge (not tested here): approximate unlearning (Q19), delayed-feedback conversion model (Q37), the "100 events" rule of thumb (Q29).

## Not run / hedged
Evidence: WebFetch unavailable, 8 search snippets; KYC/AML, collections, chargebacks, delivery promise, demand and pricing, cart abandonment, size recommendation, seller cold start, device bias, invalid traffic, signal loss and privacy scenarios are editor-designed; see research_notes/Book6_Part09_sources.md.
