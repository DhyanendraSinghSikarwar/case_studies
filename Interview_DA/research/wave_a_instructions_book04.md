# Wave A instructions — Book 4 (Power BI & Visualization) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 4 (Power BI, with Tableau basics, and Data Visualization for Data Analysts). No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9), `style_guide.md` (Sections 2, 3, 7, 8), `research/market_skills_2026.md` (Power BI 40%, Tableau 33%, DAX 5% pooled; per-sample numbers in the Addendum), `research/interview_processes.md` (Power BI/DAX interview mentions: Deloitte Power BI round with RLS, Wipro DAX topics SUM/SUMX/DATEDIFF, Infosys, Cognizant, Microsoft; Tableau at Wells Fargo; SUM vs SUMX, ALL vs ALLEXCEPT, RLS, incremental refresh, query optimisation), the JD samples in `research/jd_sample_*.md` (grep for Power BI, DAX, Tableau, dashboard), and for format only `Book01_Excel/Book01_Part12.md` header and one earlier Book 1 part header (do not copy their questions).

## Book 4 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Power BI basics: components, Desktop vs Service, workflow 🟢 | 55 |
| 2 | Power Query transformations 🟢🟡 | 60 |
| 3 | Data modelling: star schema, relationships, cardinality 🟡 | 60 |
| 4 | DAX basics: calculated column vs measure, SUM vs SUMX, COUNT, CALCULATE 🟡 | 75 |
| 5 | DAX advanced: filter context, time intelligence, ALL vs ALLEXCEPT, RANKX 🔴 | 35 |
| 6 | Visuals, slicers, drill-through, bookmarks, tooltips 🟢🟡 | 55 |
| 7 | Service: publishing, refresh, gateways, row-level security (RLS), workspaces 🟡 | 65 |
| 8 | Dashboard design principles & storytelling 🟢🟡 | 45 |
| 9 | Scenario tasks: build HR/sales dashboard, fix slow report 🔴 | 70 |
| 10 | Tableau basics & Power BI vs Tableau (33% of JDs pooled: ⭐⭐ not ⭐) | 40 |
| 11 | Copilot/AI features in Power BI ⭐ | 20 |
| 12 | How to develop Power BI skills (learning-journey interview questions + the skill-development scope) | 20 |

Other books already exist or are planned: Book 1 Excel (incl. Power Query/Power Pivot basics: do not duplicate its questions; Book 4 Part 2 goes deeper on Power BI-specific Power Query, and Part 7 covers the Power BI service), Book 2 SQL, Book 8 scenarios (dashboard/report scenarios live there too: here keep Power BI build/fix tasks).

## Research (mandatory, before writing)
1. Use WebSearch/WebFetch (load them with ToolSearch `select:WebSearch,WebFetch` if deferred). Run at least 6 distinct searches for your topic, e.g. "<topic> Power BI interview questions data analyst 2025/2026", "<topic> Power BI interview questions Hyderabad/Bengaluru", "<topic> DAX interview questions", company-specific experiences (Glassdoor/AmbitionBox/GfG/LinkedIn/Reddit may be blocked; record that); also the existing Power BI/DAX interview mentions in research/interview_processes.md. Fetch pages in full where possible (prefer official Microsoft Learn pages (learn.microsoft.com/power-bi, /dax) for behaviour, licensing and feature availability).
2. Record every source in `research/Book04_PartNN_sources.md` in the format of `research/Book02_Part05_sources.md`: URL, what it was used for, type, recency, and an honest note on whether the page was fetched in full or only seen as a search snippet. No invented sources or company claims; mark unverified items. State sample size and limitations.
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Questions a real interviewer asks of a 0-3 year data/MIS/business analyst. Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part (cross-reference mentally; the scope column above is the contract).
- Stars: ⭐⭐⭐ asked in most DA interviews, ⭐⭐ asked often, ⭐ occasional / differentiator, assigned from the research (frequency, presence in sources and JDs); give your reasoning in the sources file. Difficulty 🟢🟡🔴.
- Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous.
- Target is a minimum; fill gaps with important questions (practical "write the DAX measure / how would you do X in Power BI" tasks, difference questions, error-handling, version and licensing differences: Power BI Desktop vs Service, free vs Pro/Premium/Fabric, Mac limitation, common DAX errors, data-source privacy levels). Many questions should be practical tasks a beginner could be asked live ("Write a DAX measure for ...", "How would you model ...", "Your report is slow: what do you check?").
- Reader is a non-technical HR career switcher: include HR-flavoured scenarios (attendance, attrition, payroll, hiring) where natural.

## Files you write (only these)
1. `Book04_PowerBI_Viz/Book04_PartNN.md`:
```
# Book 4 — Power BI & Visualization | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book04_PartNN_sources.md`.
3. `research/index_rows/B4PNN.md`: markdown table rows `| B4PNNQn | 4 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, one row per question, like `research/index_rows/B2P12.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/65c5a153-2270-59c7-806a-2ca081fd6877/scratchpad/A4_PartNN` (yours only).

## Final reply (short)
Files, actual count vs target, number of searches/fetches done, which sources were blocked, how many questions are gap-fills (not seen in any source), and anything uncertain.
