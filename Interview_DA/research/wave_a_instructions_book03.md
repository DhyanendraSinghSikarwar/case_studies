# Wave A instructions — Book 3 (Python & pandas for Analysts) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 3. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9), `style_guide.md` (Sections 2, 3, 7, 8, 10), `research/market_skills_2026.md` (Python 32% of JDs pooled; MIS roles 16%; Bengaluru/Hyderabad/GCC ~40%), `research/interview_processes.md` (Python mentions: ~10 company profiles; Infosys, Cognizant, Wipro, Tiger Analytics, Accenture, etc.), the JD samples in `research/jd_sample_*.md` (grep Python, pandas, NumPy, Jupyter), and for format only the header of `Book05_Stats_Maths/Book05_Part12.md` and `research/index_rows/B5P12.md` (do not copy questions).

## Book 3 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Python basics: variables, types, lists, dicts, loops, functions 🟢 | 70 |
| 2 | Strings, file handling, error handling 🟢 | 45 |
| 3 | NumPy basics 🟢 | 25 |
| 4 | pandas: read, select, filter, sort 🟢 | 70 |
| 5 | pandas: groupby, merge, pivot, apply 🟡 | 70 |
| 6 | Data cleaning: missing values, duplicates, types, outliers 🟡 | 60 |
| 7 | Dates & time series in pandas 🟡 | 40 |
| 8 | Visualization: matplotlib, seaborn 🟢🟡 | 45 |
| 9 | EDA end-to-end tasks (live-coding style) 🟡🔴 | 50 |
| 10 | Basic coding logic asked in DA rounds (reverse string, palindrome, counts, easy list/string/dict problems, basic CS/OOP fundamentals) 🟢🟡 | 65 |
| 11 | Jupyter, APIs, Excel automation, using AI assistants correctly 🟡 | 40 |
| 12 | How to develop Python skills (learning-journey interview questions + the skill-development scope) | 20 |

Boundaries (do not duplicate): Book 2 SQL has "pandas equivalent" fields but no pandas questions; Book 5 Part 11 owns Excel/Python statistics one-liners (describe, corr, t-tests, regression): Book 3 stays on data wrangling, not inference; Book 5 owns statistics concepts; Book 9 owns scikit-learn/ML; Book 1 owns Excel/VBA (Part 11 here covers Python-driven Excel automation with openpyxl/pandas only). Check `question_index.md` rows for books 1, 2, 4, 5 for overlap before finalising.

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred; WebFetch may be unavailable: use the `web-fetch` agent only if essential, otherwise note pages as snippet-only). Run at least 6 distinct searches for your topic, e.g. "<topic> python pandas interview questions data analyst 2025/2026", "<topic> Hyderabad/Bengaluru", company-specific experiences (Glassdoor/AmbitionBox/GfG/Reddit may be blocked; record that).
2. Record every source in `research/Book03_PartNN_sources.md` in the format of `research/Book05_Part12_sources.md`: URL, use, type, recency, honest note whether fetched in full or snippet only. No invented sources or company claims; mark unverified. State sample size/limitations and your star reasoning.
3. If you cannot research (tools unavailable), STOP, write nothing, report why.

## Question rules
- Questions a real interviewer asks a 0-3 year data/MIS/business analyst. Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part.
- Stars ⭐⭐⭐/⭐⭐/⭐ from the research; difficulty 🟢🟡🔴. Sort: stars descending, then 🟢→🔴. Numbering Q1..Qn continuous.
- Target is a minimum; fill gaps. Many questions must be practical live-coding tasks ("Write code to ...", "How do you ... in pandas?") with small datasets answerable in 5 minutes, plus difference questions and common errors (SettingWithCopyWarning, KeyError, dtype issues).
- Reader is a non-technical HR career switcher: include HR-flavoured tasks (attrition, attendance, payroll, hiring funnel) where natural.

## Files you write (only these)
1. `Book03_Python_Pandas/Book03_PartNN.md` (mkdir -p):
```
# Book 3 — Python & pandas for Analysts | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book03_PartNN_sources.md`.
3. `research/index_rows/B3PNN.md`: rows `| B3PNNQn | 3 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B5P12.md`.
Touch no other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/A3_PartNN`. Do not commit or push.

## Final reply (short)
Files, actual count vs target, searches/fetches, blocked sources, gap-fill count, anything uncertain.
