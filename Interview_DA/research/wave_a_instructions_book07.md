# Wave A instructions — Book 7 (Guesstimates, Case Studies & Business Metrics) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 7. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9, Book 7 table), `style_guide.md` (Sections 2, 3, 7, 8), `research/interview_processes.md` (guesstimates, case studies, KPI and metric-diagnosis rounds at Flipkart, Meesho, Swiggy, PhonePe, Mu Sigma, Fractal, Tiger Analytics and others), `research/market_skills_2026.md` (business acumen/product sense frequency), and for format only the header of `Book06_Aptitude/Book06_Part09.md` and `research/index_rows/B6P09.md` (do not copy questions).

## Book 7 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Guesstimate framework (top-down, bottom-up, sanity checks) + India population base numbers 🟢 | 30 |
| 2 | Market-size guesstimates (e.g., cars in Hyderabad, chai cups sold daily) 🟡 | 90 |
| 3 | Revenue/operations guesstimates (Swiggy orders/day, metro riders) 🟡🔴 | 70 |
| 4 | Business metrics: KPIs, DAU/MAU, CAC, LTV, churn, retention, conversion 🟢🟡 | 80 |
| 5 | Root-cause cases: "sales dropped 20%", "orders fell on Tuesdays" 🟡🔴 | 90 |
| 6 | Profitability, pricing, growth cases 🟡🔴 | 70 |
| 7 | Product analytics cases (feature launch, funnel drop) 🔴 | 70 |
| 8 | HR/People analytics cases (attrition, hiring funnel, pay equity) 🟡 | 50 |
| 9 | How to develop structured thinking | 50 |

Boundaries: aptitude maths and data-interpretation tables are Book 6/8; statistics and A/B-testing theory are Book 5 (cases here may use them but must not repeat the theory questions); SQL/Excel/Power BI mechanics are Books 1, 2, 4; scenario-based "what would you do" data-quality questions are Book 8; Part 9 is the skill-development part (learning-journey interview questions plus scope for a skill-building plan, like other books' final parts).

## Question format
Entries are interview prompts a candidate must answer by structuring a problem aloud:
(a) guesstimates, written as the interviewer would ask ("Estimate the number of cups of chai sold in Hyderabad in a day"). Include only facts the question itself needs; never put real-world statistics in the question text as facts. Answer agents will state assumptions explicitly and label every base number "assumed/approximate, unverified".
(b) metric definitions and calculations with the data inline (small table or numbers) so a single checkable figure exists.
(c) cases ("Orders on Tuesdays fell 20%; how do you find out why?"): state the available data in the question so the answer can be a structured diagnosis (hypothesis tree, data cuts, decision rule), and include numeric cases with inline data where a figure can be derived.
(d) concept/difference/how-to questions ("How do you sanity-check a guesstimate?").
Keep about 40-60% of Parts 2-3 as fully specified, self-contained estimation prompts; Parts 4, 6, 8 need many with inline numbers. HR/people-analytics flavour (headcount, attrition, payroll, hiring funnel, attendance) where natural, and a good share of generic Indian consumer/startup contexts (food delivery, quick commerce, UPI payments, e-commerce, ride-hailing, edtech, fintech, SaaS).

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred; WebFetch is unavailable). Run at least 6 distinct searches for your topic, e.g. "<topic> interview questions data analyst", "<topic> guesstimate/case interview Flipkart Swiggy Mu Sigma Fractal", company-specific experiences, "<topic> 2025 2026". Glassdoor/AmbitionBox/Reddit/LinkedIn may be blocked; record that.
2. Record every source in `research/Book07_PartNN_sources.md` in the format of `research/Book06_Part09_sources.md`: URL, what it was used for, type, recency, honest note that it was only a search snippet. No invented sources or company claims; mark unverified items. State sample size and limitations. Give your star-assignment reasoning.
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part. Vary industries and difficulty; avoid near-identical templates with only a noun changed unless the numbers/structure differ meaningfully.
- Stars: ⭐⭐⭐ appears in most guesstimate/case/metric rounds, ⭐⭐ often, ⭐ occasional/differentiator, judged from the research (state honestly when stars are judgement).
- Difficulty 🟢🟡🔴. Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous.
- Target is a minimum; add important missing question types.

## Files you write (only these)
1. `Book07_Guesstimates_Cases/Book07_PartNN.md` (mkdir -p):
```
# Book 7 — Guesstimates, Case Studies & Business Metrics | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer; any inline data for a question goes on the lines under its heading, before the ANSWER_PENDING marker).
2. `research/Book07_PartNN_sources.md`.
3. `research/index_rows/B7PNN.md`: rows `| B7PNNQn | 7 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B6P09.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/A7_PartNN` (yours only). Do not commit or push.

## Final reply (short)
Files, actual count vs target, number of searches, which sources were blocked, how many questions are gap-fills, anything uncertain.
