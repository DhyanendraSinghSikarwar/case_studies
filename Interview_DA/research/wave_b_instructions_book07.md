# Wave B instructions — Book 7 (Guesstimates, Case Studies & Business Metrics) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (Sections 10 and 11), this file, and `research/Book07_PartNN_sources.md` for YOUR part. Tone/layout reference: any finished chunk in `Book06_Aptitude/answers_chunks/` and `Book05_Stats_Maths/answers_chunks/`.

## Who you write for
A non-technical HR professional switching to data analytics who must handle guesstimate, case and metric rounds. Plain words; explain every term at first use; sound like a confident candidate thinking aloud in a structured way. HR examples (attrition, headcount, payroll, hiring funnel, attendance) where natural, plus Indian consumer/startup contexts.

## What you produce
- Read your range from `Book07_Guesstimates_Cases/Book07_PartNN.md` (read-only; do NOT edit it). Copy each heading AND any data lines under it exactly.
- Write ONE chunk file `Book07_Guesstimates_Cases/answers_chunks/B07P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line (+ data body) copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file. Do not commit.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/B07P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py` (fractions, math, numpy, pandas, sqlite3).

## Answer templates (pick the one that fits; always keep Asked at, What the interviewer is checking, Say this, Likely follow-ups, Common mistakes)
Common header lines for every answer:
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
(data lines copied exactly, if any)
**Asked at:** <only what Book07_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1-2 plain-spoken lines: the structure you will use and the headline number or recommendation>
```
A) Guesstimate (estimate X in Y):
```
**Clarify first:** <2-4 questions you would ask and the scope you will fix>
**Approach:** <top-down, bottom-up or both, and why>
**Assumptions (all assumed / approximate, unverified):** <small table: input, value, reason>
**Calculation:** <numbered steps with every number shown, rounded sensibly>
**Result:** <the figure with units and a sensible range>
**Sanity check:** <a second route or a reality check against a known scale>
**Sensitivity:** <which assumption moves the answer most and by how much>
```
B) Metric / calculation question with inline data:
```
**Definition in plain words:** <what it measures, formula in words then symbols>
**Worked answer:** <step-by-step from the inline data>
**Result:** <the figure(s) with units>
**Check:** <independent check or edge case>
**Caveats:** <definition variations, denominators, traps>
```
C) Case (diagnose, profitability, pricing, growth, product, HR):
```
**Clarify first:** <questions and the data you would ask for>
**Structure:** <MECE hypothesis tree or framework, in text/indented list>
**What I would check, in order:** <data cuts, comparisons, the query/Excel/Power BI step in one line each>
**If the data shows...:** <decision rules: finding A means X, finding B means Y>
**Numeric work (if data given):** <computed steps and result>
**Recommendation:** <what to do next and how to measure it>
```
D) Concept / how-to (framework, difference, learning-journey, structured-thinking skill): use "Explain simply" bullets, a short worked mini-example with numbers where it helps, and a short practice step.
Then always:
```
**Likely follow-ups:** 1-3 with short answers
**Common mistakes / traps:** <what beginners get wrong>
```
About 150-350 words, shorter for easy ones. No filler. Never use em dashes (use commas, colons, semicolons, parentheses).

## Verification and honesty rules (mandatory)
- Compute EVERY number (guesstimate chains, metrics, case arithmetic, sensitivity) by code before writing; write the answer from the computed values and state rounding. Where the question's inline data is inconsistent or the premise is flawed, say so inside the answer and solve the sensible version; list it in your final report.
- All real-world base numbers (population, households, vehicle counts, prices, wages, internet/phone/UPI usage, company volumes) are NOT verified here (no web fetch): present them only as clearly labelled assumptions ("assumed, approximate, unverified"), round, give a plausible range, and never state a real statistic or company figure as fact. Numbers given in the question's own text are exercise inputs: use them as given.
- Never invent company claims, statistics or sources. "Asked at" must follow the sources file; prep-site claims stay marked unverified.
- Verification code stays in the scratch folder; do not paste scripts into answers (a SQL/Excel line is fine where the case calls for the step).

## Reporting
Final reply (short): chunk path, number of answers, questions with premise problems (IDs and what you changed), what was verified by script, anything unverified.
