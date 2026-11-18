# Wave B instructions — Book 10 (Domain Knowledge for Data Analysts) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (Sections 10 and 11), this file, and `research/Book10_PartNN_sources.md` for YOUR part (resolve or label every "uncertain" item it lists). Tone/layout reference: any finished chunk in `Book07_Guesstimates_Cases/answers_chunks/` and `Book08_Scenarios/answers_chunks/`.

## Who you write for
A non-technical HR professional switching to data analytics, interviewing for roles in this domain. Assume ZERO prior knowledge of the domain (banking, pharma, supply chain...). Plain words; explain every domain term at first use; sound like a confident analyst. HR examples (headcount, attendance, payroll, attrition) where natural.

## What you produce
- Read your range from `Book10_Domain/Book10_PartNN.md` (read-only; do NOT edit it). Copy each heading AND any inline-data lines under it EXACTLY.
- Write ONE chunk file `Book10_Domain/answers_chunks/B10P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line (+ data body) copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file. Do not commit.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/B10P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py` (math, fractions, numpy, pandas 3.0.5, scipy, sqlite3).

## Answer template
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
(data lines copied exactly, if any)
**Asked at:** <only what Book10_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1-2 plain-spoken lines: the direct answer>
**Explain simply:**
- 2-5 bullets, every domain term explained, how the business actually works
**Worked example:** <for formula/metric/calculation questions: the inline data worked step by step with every figure computed by code; state units, rounding, percentage vs percentage-point>
**Data and tables involved:** <for "what data would you need" or analysis-task questions: the tables, key columns and typical first cuts; for others omit>
**Regulation / privacy note (awareness only):** <only where relevant; plain words; labelled "from memory, unverified, confirm with the compliance/legal team"; never legal, medical or financial advice>
**Likely follow-ups:** 1-3 with short answers
**Common mistakes:** <what beginners get wrong>
```
Include only the sections that fit the question; keep Asked at, interviewer check, Say this, Explain simply, Likely follow-ups, Common mistakes always. About 150-350 words, shorter for easy ones. No filler. Never use em dashes (use commas, colons, semicolons, parentheses).

## Code rule (style_guide.md Sections 10 and 11)
Most domain answers need no code. Where a SQL query, pandas snippet or Excel formula genuinely helps (for example computing a metric from a table), show EXACTLY what a candidate would write live: short, readable, descriptive names, a comment on non-obvious steps, followed by its real output and a plain-words line. Run it first (sqlite3 or pandas); no test scaffolding in the answer.

## Verification and honesty rules (mandatory)
- Compute EVERY number in the Worked example by code before writing; write from computed values; state rounding. If the inline data is inconsistent or the premise is wrong, say so, solve the sensible version, and list it in your final report.
- Real-world facts (regulations and their dates, RBI/IRDAI/CDSCO/HIPAA/DPDP/GST details, industry benchmarks, tool features such as Workday/Alteryx, company practices, standards such as ICD-10, CDISC, GS1) are NOT verified here (no web access): state the principle in plain words and label specifics "from memory, unverified". Never state a real statistic, benchmark or company figure as fact; numbers in questions are invented exercise inputs.
- Metric definitions differ across companies: say so where relevant and state the definition you use.
- BFSI, healthcare and employee-data topics: awareness only; no advice; privacy and consent principles stated plainly.
- Never invent company claims or sources. "Asked at" must follow the sources file; prep-site claims stay marked unverified.
- Verification scripts stay in the scratch folder; do not paste them into answers.

## Reporting
Final reply (short): chunk path, number of answers, questions with premise problems (IDs and what you changed), what was verified by script, anything unverified.
