# Wave B instructions — Book 5 (Statistics & Maths for Data Analysts) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (ESPECIALLY Section 10, code readability), this file, and `research/Book05_PartNN_sources.md` for YOUR part (resolve or label every "uncertain" item it lists). Tone/layout reference: any finished chunk in `Book01_Excel/answers_chunks/`.

## Who you write for
A non-technical HR professional switching to data analytics. Plain words; explain every term at first use; sound like a confident candidate speaking in an interview. HR examples (attrition, salary, attendance, hiring funnel, engagement scores) where natural.

## What you produce
- Read your range from `Book05_Stats_Maths/Book05_PartNN.md` (read-only; do NOT edit it).
- Write ONE chunk file `Book05_Stats_Maths/answers_chunks/B05P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/B05P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py`. numpy 2.5.3, pandas 3.0.5, scipy 1.18.1 and statsmodels are installed.

## Answer template
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
**Asked at:** <only what Book05_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1–2 plain-spoken lines>
**Explain simply:**
- 2–5 bullets, jargon explained
**Formula in plain words:** <where a formula applies: words first, then symbols>
**Worked example:** <real-life/HR-friendly example with numbers; every number computed in Python and verified>
**Excel / Python:** <readable code in ```python or an Excel formula, with real printed output pasted>
**Likely follow-ups:** 1–3 with short answers
**Common mistakes:** <what beginners get wrong>
```
Concept-only questions may omit Formula / Excel-Python where not meaningful. About 150–350 words, shorter for easy ones. No filler. Never use em dashes (user preference): use commas, colons, semicolons, parentheses.

## Code readability (mandatory, user rule)
All code in human-understandable form: descriptive variable names (`monthly_salaries`, not `x`), one step per line, a short plain-English comment above each step, step-by-step rather than clever one-liners, and 1-2 lines after the code explaining the output in plain words. Excel formulas: state the cell layout, then the formula, then what it returns.

## Verification rules
- Run every calculation and snippet before inserting it; paste the real printed output. Excel formulas: check by hand/Python against the sample data and state the Excel version needed (e.g., STDEV.S needs 2010+); label "not run in Excel here".
- Check probability puzzle answers by exact calculation or simulation. If a question's premise is wrong or ambiguous, say so and answer the sensible version.
- Never invent company claims, statistics or sources. "Asked at" must follow the sources file. Web is not reliably available; do not cite pages you did not read.

## Reporting
Final reply (short): chunk path, number of answers, premise changes, what was verified by execution, anything unverified.
