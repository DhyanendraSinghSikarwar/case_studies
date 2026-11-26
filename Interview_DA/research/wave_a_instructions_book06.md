# Wave A instructions — Book 6 (Aptitude & Business Maths) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 6. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9, Book 6 table), `style_guide.md` (Sections 2, 3, 7, 8), `research/interview_processes.md` (aptitude gates at Infosys, Accenture, Wipro, Fractal, Mu Sigma, GfG campus report: ~20 aptitude/maths + 10 CS fundamentals + 2 coding; Accenture English communication test), `research/market_skills_2026.md`, and for format only the header of `Book05_Stats_Maths/Book05_Part12.md` and `research/index_rows/B5P12.md` (do not copy questions).

## Book 6 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Percentages, profit & loss, discounts | 70 |
| 2 | Ratio, proportion, averages, mixtures | 60 |
| 3 | Time & work, time-speed-distance | 60 |
| 4 | Simple/compound interest, business finance basics | 50 |
| 5 | Number series, number system | 50 |
| 6 | Permutation, combination, probability (aptitude style) | 60 |
| 7 | Logical reasoning: puzzles, seating, blood relations, syllogisms | 80 |
| 8 | Data interpretation: tables, bar/pie/line charts | 80 |
| 9 | Data sufficiency | 40 |
| 10 | Speed tricks & mock test sets | 50 |
| 11 | English/communication assessment (Accenture-style) + embedded SQL/CS-fundamentals items seen in online tests | 30 |

Boundaries: interview-style probability/Bayes and stats are Book 5 (do not duplicate); business metrics and guesstimates are Book 7; scenario-based data interpretation and mock-style business cases are Book 8. Part 10 here is speed tricks and full timed mock sets built from other parts' topics (mock sets reference the topic, they are not copies of the other parts' questions).

## Question format (aptitude books are different from concept books)
Entries are a mix of: (a) concept/method questions ("How do you find the successive discount?"), and (b) fully specified solvable problems with numbers, written so an answer agent can compute and verify the result ("A shirt is marked Rs 1,200 and sold at 15% and then 10% successive discounts; what is the selling price?"). At least ~60% of each quantitative part must be fully specified numeric problems with a single checkable answer. Logical-reasoning and data-interpretation entries must be self-contained (state all conditions and the data in the question text; for DI, include the small table/series inline in the entry as Markdown so the question can be solved without a picture). Never write a problem whose answer depends on an unstated assumption.

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred; WebFetch is unavailable). Run at least 6 distinct searches for your topic, e.g. "<topic> aptitude questions data analyst online assessment", "<topic> aptitude TCS Infosys Wipro Accenture Cognizant", "<topic> quantitative aptitude questions asked 2025/2026", company-specific experiences (Glassdoor/AmbitionBox/GfG/LinkedIn/Reddit may be blocked; record that).
2. Record every source in `research/Book06_PartNN_sources.md` in the format of `research/Book05_Part05_sources.md`: URL, what it was used for, type, recency, honest note that it was only a search snippet (pages cannot be fetched). No invented sources or company claims; mark unverified items. State sample size and limitations. Give your star-assignment reasoning.
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Questions a real online assessment or interviewer asks a 0-3 year data/MIS/business analyst candidate. Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part.
- Stars: ⭐⭐⭐ appears in most aptitude gates, ⭐⭐ often, ⭐ occasional/differentiator, judged from the research (honestly say stars are judgement when sources are thin).
- Difficulty 🟢🟡🔴. Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous.
- Target is a minimum; add important missing question types (classic patterns, traps, formula-recall, time-saving shortcuts). Use business/HR flavour (salary, attrition, headcount, payroll, bonus, sales) for word problems where natural.

## Files you write (only these)
1. `Book06_Aptitude/Book06_PartNN.md` (mkdir -p):
```
# Book 6 — Aptitude & Business Maths | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book06_PartNN_sources.md`.
3. `research/index_rows/B6PNN.md`: rows `| B6PNNQn | 6 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B5P12.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/A6_PartNN` (yours only). Do not commit or push.

## Final reply (short)
Files, actual count vs target, number of searches, which sources were blocked, how many questions are gap-fills, anything uncertain.
