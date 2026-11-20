# Wave B instructions — Book 8 (Scenario-Based & Data Interpretation) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (Sections 10 and 11), this file, and `research/Book08_PartNN_sources.md` for YOUR part. Tone/layout reference: any finished chunk in `Book07_Guesstimates_Cases/answers_chunks/` (same family of answers) and `Book06_Aptitude/answers_chunks/`.

## Who you write for
A non-technical HR professional switching to data analytics, facing scenario and project rounds. Plain words; explain every term at first use; sound like a confident analyst describing what they would actually do on the job. HR examples (attendance, payroll, attrition, hiring funnel, HRIS exports) where natural, plus sales, e-commerce, finance and operations contexts.

## What you produce
- Read your range from `Book08_Scenarios/Book08_PartNN.md` (read-only; do NOT edit it). Copy each heading AND any data lines under it exactly.
- Write ONE chunk file `Book08_Scenarios/answers_chunks/B08P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line (+ data body) copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file. Do not commit.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/B08P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py` (fractions, math, numpy, pandas, scipy, sqlite3).

## Answer templates (pick the one that fits; always keep Asked at, What the interviewer is checking, Say this, Likely follow-ups, Common mistakes)
Common header lines for every answer:
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
(data lines copied exactly, if any)
**Asked at:** <only what Book08_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1-2 plain-spoken lines: your first move and the headline>
```
A) Scenario (what do you do when X happens: data quality, stakeholder, dashboard, prioritisation, ethics):
```
**First, clarify / contain:** <what you ask or do in the first minutes, and what you do NOT do yet>
**What I would check, in order:** <numbered checks, each one line (a SQL/Excel/Power BI step may be named in a line, not taught)>
**If I find...:** <decision rules: finding A means action X, finding B means action Y>
**What I would tell the stakeholder:** <a short plain-language script, with what is known, unknown, next step and time>
**Prevent it next time:** <1-2 lines: controls, documentation, automation>
```
B) Investigation / data interpretation with inline data (metric change, tables and charts):
```
**What the data shows:** <the read-out in plain words>
**Working:** <numbered steps with every figure from the data, computed by code>
**Result:** <the figure(s) with units; percentage vs percentage-point stated carefully>
**Caveats / what else I would check:** <denominators, mix, seasonality, definitions, data lags, small numbers>
**Next step / recommendation:** <what to do and how to measure it>
```
C) Approach ("how would you analyse X"):
```
**Clarify first:** <questions and the decision the analysis supports>
**Plan:** <steps: data needed, cleaning, method, check, communication>
**Method choice and why:** <the simple method first; when to go further>
**Pitfalls:** <bias, confounders, data issues>
**Deliverable:** <what the stakeholder gets and how you present it>
```
D) Project deep-dive (Part 8; project-agnostic): give the answer STRUCTURE plus a short ILLUSTRATIVE model answer (clearly marked "illustrative project, replace with your real one"; use an HR-analytics example such as an attrition dashboard or hiring-funnel analysis with plausible numbers computed by code), and note what the candidate must not claim unless true.
E) Concept / how-to / learning-journey (Part 9, checklists, differences): "Explain simply" bullets, a short worked mini-example with numbers where it helps, a practice step; personal-experience answers are templates the candidate must replace with true experience ("say it only if true").
Then always:
```
**Likely follow-ups:** 1-3 with short answers
**Common mistakes / traps:** <what beginners get wrong>
```
About 150-350 words, shorter for easy ones. No filler. Never use em dashes (use commas, colons, semicolons, parentheses).

## Verification and honesty rules (mandatory)
- Compute EVERY number (reconciliations, percentages, decompositions, tests, weights, sizes) by code before writing; write the answer from computed values and state rounding. Where the question's inline data is inconsistent or the premise is flawed, say so in the answer and solve the sensible version; list it in your final report.
- Real-world facts (tools' limits and features, laws, regulations such as India's DPDP Act, company practices, benchmarks) are NOT verified here (no web fetch): label them "from memory, unverified" or state the principle and say to confirm with the legal/IT/owner team. Never state a real statistic or company figure as fact. Numbers in the question text are exercise inputs.
- Never invent company claims, statistics or sources. "Asked at" must follow the sources file; prep-site claims stay marked unverified.
- Verification code stays in the scratch folder; do not paste scripts into answers (a one-line SQL/Excel step inside a check is fine).

## Reporting
Final reply (short): chunk path, number of answers, questions with premise problems (IDs and what you changed), what was verified by script, anything unverified.
