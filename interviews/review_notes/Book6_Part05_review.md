# Book 6 Part 5 review (Wave C)

Date: 2026-10-30. Reviewer: lead session (independent of the five answer agents). Scope: 55 questions, Q1-Q55 (business case studies: pricing, churn, fraud, supply chain). No salary figures; all numbers are invented illustrative numbers in one unnamed currency unit.

## Process
Five agents answered Q1-11, 12-22, 23-33, 34-44, 45-55; merged by heading: 55 of 55 merged, 0 skipped, 0 pending. Two agents were re-run on their own questions after prompt corrections (Q25/Q30/Q33, Q50/Q52). No spend-limit stops.

## Checks (`scratch/B6_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q55; star order and counts 18 / 25 / 12 | pass |
| All 11 template labels present and in order; fences balanced | pass for all 55 |
| At most one python block per answer, each re-run standalone with `python3 -I` | 55 of 55 exit 0 |
| Cross-references (in-part Q1, Q4, Q7, Q11, Q19, Q20, Q22, Q28, Q30, Q31, Q53; Book 6 Part 4 Q13, Q28, Q29, Q55) | headings grep-checked by the agents |

## Corrections to frozen prompts (applied to part file, agent heading, qs.py, question_index.md, index_rows.txt)
- Q25: 40.0 against 39.0 is +2.56%, so "+2.5%" became "+2.6%"; the 2,000,000 users are now stated as the users the model serves.
- Q30: after a 1% order cut there are 99,000 orders, so 20% late is 19,800, not 20,000; daily difference 89,100.
- Q33: "monthly revenue" is now "total monthly revenue (all sources)" (average ROAS includes revenue that arrives without search spend).
- Q50: the prompt now says the 4.00 return fee is kept as income on each returned order (margin 9.94M to 11.23M, break-even order drop 14.16%; 8.47% without fee income).
- Q52: "Fitting a line" became "A line through the two tested points" (two points give no error estimate; with 2% noise the optimum ranges 0.16 to 0.91).

## Findings kept in the text
- Prompt arithmetic recomputed in code for all 55 questions: for example Q3 cumulative margin 200.63 against CAC 200 (payback depends on the month-1 convention), Q24 LTV 140, LTV/CAC 2.33, payback 8.57 months, Q29 break-even default rate 20%, Q31 break-even late rate 35.5%, Q32 safety stock 32.9 and reorder point 232.9, Q43 allowing friction (10.56) is cheaper than declining (9.60).
- Honest findings stated in the answers: Q7 a naive forecast on censored sales data stays near 100 and never finds the 113.5 optimum; Q9 the +0.312 contribution edge is not significant (p about 0.07); Q14 the high-risk net of -0.60 per customer has a 95% band -2.14 to +0.94; Q34 net 3,000 a week goes to 0 if the click margin is 10% too high; Q40 the price cut is not profitable (net -8,000 after leakage); Q47 the dark store loses money on delivery savings alone (break-even 72,727 orders against a 24,000 forecast); Q53 normal versus lognormal demand fits change the answer (91.5 versus 98.5); Q54 the cascade (0.0411 per query) is cheaper but less accurate than large-only (89.3% vs 92%).
- Wording ambiguities answered as clarifying questions or stated assumptions: Q8, Q10, Q3, Q5, Q12, Q16, Q18, Q20, Q15, Q34, Q36, Q38, Q39.

## Not run / hedged
Judgement-only questions say "Not applicable". Evidence: WebFetch unavailable, 16 search snippets; Q38 (loyalty), Q46 (build vs buy for a fraud model), Q47 (dark store), Q50 (free returns), Q51 (insurance repricing) are editor-designed; AI-era items rest on vendor and practitioner posts whose figures disagree by an order of magnitude, so prompts use round invented numbers; see research_notes/Book6_Part05_sources.md.
