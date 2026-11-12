# style_guide.md — Rules for Every Agent

Read `plan.md` first. This file is the writing contract. Markdown only; bullets and tables; no filler.

## 1. Reader and voice
- Reader: a non-technical career switcher (HR → Data Analyst). Assume zero technical background.
- Voice: a confident candidate speaking in an interview, not a textbook.
- Every technical term is explained in plain words the first time it appears in an answer.
- Add a real-life example with numbers; use HR examples (attrition, hiring funnel, payroll, attendance) where natural.
- Never invent sources, statistics, or company processes. If unsure, say so or omit.

## 2. Star and difficulty rules (plan.md Section 4)
| Mark | Meaning |
|---|---|
| ⭐⭐⭐ | Asked in most DA interviews; must know |
| ⭐⭐ | Asked often; expected from good candidates |
| ⭐ | Occasional; differentiator at 8–10 LPA or product companies |
| 🟢 / 🟡 / 🔴 | Easy / Medium / Hard |

Sort order inside every part: ⭐⭐⭐ → ⭐⭐ → ⭐; within the same star, 🟢 → 🟡 → 🔴.
Numbering is continuous within a part (Q1…Qn) and never changes after the list is frozen.

## 3. Question-file format (Wave A)
```
### Q<n> ⭐⭐⭐ 🟢 <Canonical question>
<!-- ANSWER_PENDING -->
```
File header: part title, target count, actual count, one-line scope. Footer: nothing.
Question IDs in `question_index.md`: `B<book>P<part>Q<n>` (e.g., B2P5Q12).

## 4. Answer template (Wave B) — plan.md Section 5
```
### Q<n> ⭐⭐⭐ 🟢 <Question>
**Asked at:** <service MNC / GCC / analytics firm / product / startup / consulting>
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1–2 lines, plain words>
**Explain simply:**
- 2–5 points, no unexplained jargon
**Example:** <real-life / HR-friendly, with numbers>
**Code / Steps:** <SQL / pandas / Excel formula / DAX / click-steps where relevant>
**Likely follow-ups:** 1–3 with short answers
**Common mistakes:** <what beginners get wrong>
```

## 5. Book-specific additions
| Book | Extra fields |
|---|---|
| 2 SQL | Sample table(s) + data, SQL answer, **pandas equivalent**, output table, edge cases (NULLs, duplicates, ties) |
| 1 Excel | Formula, alternative formula, sample sheet layout |
| 4 Power BI | DAX, text model diagram, click-path |
| 5 Stats | Formula in plain words, worked numeric example, Excel/Python one-liner |
| 6 Aptitude | Shortcut method + time-saving trick |
| 7 Guesstimates/Cases | Framework → clarifying questions → step-by-step numbers → sanity check |
| 8 Scenarios | Clarify → hypotheses → data needed → analysis → recommendation |
| 11 Soft skills | Weak answer vs strong answer, STAR breakdown |

## 6. Verification rules (plan.md Section 8.5, Section 9)
- Run every SQL query (SQLite/DuckDB/Postgres on sample data), every pandas/Python snippet and every stats calculation before inserting it. Paste the real output.
- Check Excel formulas and DAX logic by hand against the sample data; state the Excel version needed (e.g., XLOOKUP needs 365/2021).
- Never reorder, renumber or edit questions outside your assigned file / Q-range.
- Every question gets an answer; zero `ANSWER_PENDING` left when done.

## 7. "How to Develop This Skill" part (last part of each skill book)
Must contain: zero-to-job-ready roadmap · daily practice plan · free resources · practice datasets · mini-projects · self-check tests.

## 8. Research rules
- Cite a source (URL/site + date accessed) for every figure. Mark unverified items "unverified".
- If a site blocks access or needs login, record it in the research file; do not guess its content.
- Counts must be real tallies from sampled postings; state the sample size and how it was gathered.

## 9. Agent rules (plan.md Section 8.7, 9)
- Read `plan.md` and `style_guide.md` first.
- Edit only your assigned file(s). Append only your own rows to `question_index.md`.
- Question targets are minimums; add important missing questions.
- After finishing, report counts and issues; do not start the next wave.

## 10. Code readability (user rule, applies to every answer in every book)
- Write all code (SQL, pandas/Python, Excel formulas, DAX, M) in a human-understandable form for a non-technical reader.
- Use descriptive names (e.g. `employees_who_left`, not `df2`; `total_salary`, not `ts`), one step per line, consistent indentation and spacing.
- Add a short plain-English comment above each step or clause saying what it does and why.
- Prefer clear step-by-step code (CTEs, small named variables, intermediate columns) over clever one-liners; if a compact form is worth showing, give the readable version first.
- Follow each code block with 1-2 lines in plain words explaining what the output means.

## 11. Interview-ready code (user rule, stricter, applies to every answer)
- The code in "Code / Excel-Python / Steps" must be exactly what a candidate would type or write live in the interview for that question: the shortest clear, correct solution a beginner can explain line by line. No test harnesses, no helper scripts, no build/verification scaffolding, no `print` of debugging values that the interviewer would not ask for.
- Keep it simple and readable: plain loops or standard built-ins over clever tricks, descriptive names (`employees`, `total_salary`), one idea per line, a short comment on the non-obvious steps. If a short interview version and a more complete version both matter, show the interview version first and label the other "Alternative".
- Show a tiny sample dataset only as far as needed to run the answer (3 to 8 rows), then the code, then the real output, then one plain-words line about what it means.
- Verification (running the code to get the output) happens outside the answer; the answer shows the interview code and its real output only.

