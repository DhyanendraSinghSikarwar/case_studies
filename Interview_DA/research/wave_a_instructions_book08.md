# Wave A instructions — Book 8 (Scenario-Based & Data Interpretation) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 8. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9, Book 8 table), `style_guide.md` (Sections 2, 3, 7, 8), `research/interview_processes.md` (scenario, project-walkthrough, data-quality and stakeholder rounds at Deloitte USI, Wipro, Infosys, Accenture, Flipkart, Meesho, Swiggy, Tiger Analytics, Mu Sigma, Fractal and others), `research/market_skills_2026.md` (communication/stakeholder skills are must-have in the JD sample), and for format only the header of `Book07_Guesstimates_Cases/Book07_Part08.md` and `research/index_rows/B7P08.md` (do not copy questions).

## Book 8 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Data quality scenarios (missing, wrong, duplicate data) | 70 |
| 2 | Stakeholder request scenarios (vague asks, urgent reports) | 70 |
| 3 | Dashboard/report scenarios (numbers mismatch, slow refresh) | 70 |
| 4 | Metric-change investigations | 80 |
| 5 | Analysis-approach scenarios ("how would you analyse X") | 90 |
| 6 | Data interpretation from given tables/charts | 80 |
| 7 | Prioritisation & ethics scenarios | 60 |
| 8 | Project deep-dive questions ("walk me through your project") | 60 |
| 9 | How to practise scenario thinking | 20 |

Boundaries (do not duplicate; write the on-the-job angle): Book 7 owns case-interview style estimation, root-cause, profitability, product and HR cases and the structured-thinking skill part; here the angle is "you are the analyst on the job and this happened: what do you do, what do you check, what do you say". Book 6 Part 8 owns aptitude-style data interpretation (calculation drills); Book 8 Part 6 is analyst-style interpretation (read the table/chart, state the insight, caveats, next step) with some computable figures. Statistics/A-B theory is Book 5; SQL/Excel/Power BI/pandas mechanics are Books 1-4 (a scenario may mention the check you would run, in one line, without teaching the tool). Part 8 (project deep-dive) must be project-agnostic: questions an interviewer asks about ANY analytics project, with the answer structure, because the candidate's real project is theirs; include HR-analytics project angles. Part 9 is the skill-development part (learning-journey interview questions plus scope for a practice plan, like other books' final parts).

## Question format
Scenario prompts an interviewer asks, written so an answer can be structured: state the situation, the available data and the constraint (time, access, stakeholder). Types: (a) "what would you do" scenarios; (b) investigation prompts with inline numbers/tables so a figure can be derived (Parts 4, 6 especially, and some in Parts 1-3); (c) "how do you handle/communicate" questions; (d) concept/difference/checklist questions. Never put real-world statistics in question text as facts; use clearly exercise data. HR/people-analytics flavour (attendance, payroll, attrition, hiring funnel, HRIS exports) where natural, plus sales, e-commerce, finance and operations contexts. At least ~35-50% of Parts 4 and 6, and a fair share of Parts 1 and 3, must have inline data with a single checkable figure.

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred; WebFetch is unavailable). Run at least 6 distinct searches for your topic, e.g. "<topic> interview questions data analyst scenario-based", "<topic> data analyst interview Deloitte Wipro Infosys Accenture Flipkart", company-specific experiences, "<topic> 2025 2026". Glassdoor/AmbitionBox/Reddit/LinkedIn may be blocked; record that.
2. Record every source in `research/Book08_PartNN_sources.md` in the format of `research/Book07_Part08_sources.md`: URL, what it was used for, type, recency, honest note that it was only a search snippet. No invented sources or company claims; mark unverified items. State sample size and limitations. Give your star-assignment reasoning.
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part. Vary contexts and difficulty; avoid near-identical templates with only a noun changed.
- Stars: ⭐⭐⭐ appears in most scenario/behavioural-technical rounds, ⭐⭐ often, ⭐ occasional/differentiator, judged from the research (state honestly when stars are judgement).
- Difficulty 🟢🟡🔴. Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous.
- Target is a minimum; add important missing question types.

## Files you write (only these)
1. `Book08_Scenarios/Book08_PartNN.md` (mkdir -p):
```
# Book 8 — Scenario-Based & Data Interpretation | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
(inline data lines, if any)
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book08_PartNN_sources.md`.
3. `research/index_rows/B8PNN.md`: rows `| B8PNNQn | 8 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B7P08.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/A8_PartNN` (yours only). Do not commit or push.

## Final reply (short)
Files, actual count vs target, number of searches, which sources were blocked, how many questions are gap-fills, anything uncertain.
