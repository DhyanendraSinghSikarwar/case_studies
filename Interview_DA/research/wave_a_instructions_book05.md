# Wave A instructions — Book 5 (Statistics & Maths for Data Analysts) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 5. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9), `style_guide.md` (Sections 2, 3, 7, 8), `research/market_skills_2026.md` (statistics 23% of JDs pooled, A/B testing ~4%), `research/interview_processes.md` (Tiger Analytics: probability/stats "hardest part"; probability puzzles, stats asked in Hyd/Blr loops), the JD samples in `research/jd_sample_*.md` (grep statistics, hypothesis, A/B, regression), and for format only the header of `Book04_PowerBI_Viz/Book04_Part12.md` and `research/index_rows/B4P12.md` (do not copy questions).

## Book 5 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Maths foundations: percentages, ratios, averages, growth rates, weighted average 🟢 | 60 |
| 2 | Descriptive stats: mean/median/mode, variance, SD, percentiles, IQR 🟢 | 60 |
| 3 | Distributions: normal, binomial, Poisson, skewness, kurtosis 🟡 | 50 |
| 4 | Probability & Bayes (puzzles asked; analytics firms rate stats "hardest") 🟡 | 70 |
| 5 | Sampling, bias, CLT, confidence intervals 🟡 | 50 |
| 6 | Hypothesis testing: p-value, t-test, chi-square, ANOVA, errors 🟡 | 70 |
| 7 | Correlation vs causation, regression basics, R² 🟡 | 50 |
| 8 | A/B testing for analysts 🟡🔴 | 40 |
| 9 | Outliers, Simpson's paradox, misleading stats 🟡 | 40 |
| 10 | Scenario-based stats questions (asked in Hyd/Blr loops) 🔴 | 60 |
| 11 | Stats in Excel & Python (functions, one-liners) 🟢 | 30 |
| 12 | How to develop stats/maths skills (learning-journey interview questions + skill-development scope) | 20 |

Aptitude-style maths (profit/loss, time-work, etc.) belongs to Book 6, not here: Part 1 is business/analyst maths (percentage change, CAGR, weighted average, ratios in KPIs). Probability puzzles for aptitude (permutation/combination) are Book 6 Part 6; Part 4 here is interview-style probability and Bayes. Excel/Python stats functions are Part 11 only. Book 7 has business metrics; Book 9 has ML. Do not duplicate.

## Research (mandatory, before writing)
1. Use WebSearch/WebFetch (load with ToolSearch `select:WebSearch,WebFetch` if deferred). Run at least 6 distinct searches for your topic, e.g. "<topic> interview questions data analyst 2025/2026", "<topic> statistics interview questions Hyderabad/Bengaluru", company-specific experiences (Glassdoor/AmbitionBox/GfG/LinkedIn/Reddit may be blocked; record that). Fetch pages in full where possible.
2. Record every source in `research/Book05_PartNN_sources.md` in the format of `research/Book02_Part05_sources.md`: URL, what it was used for, type, recency, honest note whether fetched in full or only a snippet. No invented sources or company claims; mark unverified items. State sample size and limitations. Give your star-assignment reasoning.
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Questions a real interviewer asks a 0-3 year data/MIS/business analyst. Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part.
- Stars: ⭐⭐⭐ asked in most DA interviews, ⭐⭐ asked often, ⭐ occasional/differentiator, from the research. Difficulty 🟢🟡🔴.
- Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous.
- Target is a minimum; fill gaps with important questions (numeric "calculate X" tasks, difference questions, "explain to a non-technical manager", common misconceptions). Many should be practical, answerable live with a worked number.
- Reader is a non-technical HR career switcher: include HR-flavoured scenarios (attrition, salary, attendance, hiring) where natural.

## Files you write (only these)
1. `Book05_Stats_Maths/Book05_PartNN.md` (create the folder if missing, mkdir -p):
```
# Book 5 — Statistics & Maths for Data Analysts | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book05_PartNN_sources.md`.
3. `research/index_rows/B5PNN.md`: rows `| B5PNNQn | 5 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B4P12.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/A5_PartNN` (yours only). Do not commit or push.

## Final reply (short)
Files, actual count vs target, number of searches/fetches, which sources were blocked, how many questions are gap-fills, anything uncertain.
