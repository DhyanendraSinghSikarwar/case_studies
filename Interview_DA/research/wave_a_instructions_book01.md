# Wave A instructions — Book 1 (Excel) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 1 (Excel for Data Analysts). No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9), `style_guide.md` (Sections 2, 3, 7, 8), `research/market_skills_2026.md` (Excel/Sheets/VBA numbers), `research/interview_processes.md` (Excel mentions; Novartis Excel case, Accenture, Meesho MCQs, Infosys), the JD samples in `research/jd_sample_*.md` (grep for Excel, Power Query, pivot, VBA, MIS), and for format only `Book02_SQL/Book02_Part12.md` header + one earlier part header (do not copy their questions).

## Book 1 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Basics: cell refs, sorting, filtering, formatting, shortcuts 🟢 | 60 |
| 2 | Core functions: IF, AND/OR, COUNTIF(S), SUMIF(S), text and date functions 🟢 | 70 |
| 3 | Lookups: VLOOKUP, HLOOKUP, INDEX-MATCH, XLOOKUP 🟢🟡 | 60 |
| 4 | Pivot tables, pivot charts, slicers 🟢🟡 | 70 |
| 5 | Data cleaning: duplicates, TRIM, text-to-columns, Flash Fill 🟢 | 50 |
| 6 | Dynamic arrays: FILTER, UNIQUE, SORT, LET 🟡 | 40 |
| 7 | Power Query and Power Pivot 🟡 | 60 |
| 8 | Charts and Excel dashboards 🟡 | 50 |
| 9 | What-if, Goal Seek, conditional formatting, data validation 🟡 | 40 |
| 10 | Scenario/practical tasks (MIS reports, HR attrition sheet) 🟡🔴 | 60 |
| 11 | VBA basics (12 Qs) + Copilot in Excel and Google Sheets (8 Qs), ⭐ priority | 20 |
| 12 | How to develop Excel skills (learning-journey interview questions + the skill-development scope) | 20 |

## Research (mandatory, before writing)
1. Use WebSearch/WebFetch (load them with ToolSearch `select:WebSearch,WebFetch` if deferred). Run at least 6 distinct searches for your topic, e.g. "<topic> Excel interview questions data analyst 2025/2026", "<topic> Excel interview questions Hyderabad/Bengaluru", company-specific experiences (Glassdoor/AmbitionBox/GfG/LinkedIn/Reddit may be blocked; record that). Fetch pages in full where possible (prefer official Microsoft Support pages for function behaviour and version availability).
2. Record every source in `research/Book01_PartNN_sources.md` in the format of `research/Book02_Part05_sources.md`: URL, what it was used for, type, recency, and an honest note on whether the page was fetched in full or only seen as a search snippet. No invented sources or company claims; mark unverified items. State sample size and limitations.
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Questions a real interviewer asks of a 0-3 year data/MIS/business analyst. Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part (cross-reference mentally; the scope column above is the contract).
- Stars: ⭐⭐⭐ asked in most DA interviews, ⭐⭐ asked often, ⭐ occasional / differentiator, assigned from the research (frequency, presence in sources and JDs); give your reasoning in the sources file. Difficulty 🟢🟡🔴.
- Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous.
- Target is a minimum; fill gaps with important questions (practical "write the formula / how would you do X in Excel" tasks, difference questions, error-handling, version differences: Excel 2016/2019/365 and Google Sheets where relevant, shortcuts, common errors like #N/A and #SPILL!). Many questions should be practical tasks a beginner could be asked live ("Given columns A to D, how do you ...").
- Reader is a non-technical HR career switcher: include HR-flavoured scenarios (attendance, attrition, payroll, hiring) where natural.

## Files you write (only these)
1. `Book01_Excel/Book01_PartNN.md`:
```
# Book 1 — Excel | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book01_PartNN_sources.md`.
3. `research/index_rows/B1PNN.md`: markdown table rows `| B1PNNQn | 1 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, one row per question, like `research/index_rows/B2P12.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/65c5a153-2270-59c7-806a-2ca081fd6877/scratchpad/A1_PartNN` (yours only).

## Final reply (short)
Files, actual count vs target, number of searches/fetches done, which sources were blocked, how many questions are gap-fills (not seen in any source), and anything uncertain.
