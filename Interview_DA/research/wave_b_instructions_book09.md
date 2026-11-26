# Wave B instructions — Book 9 (Basic ML + AI Tools for Analysts) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (Sections 10 and 11: readable, interview-ready code), this file, and `research/Book09_PartNN_sources.md` for YOUR part. Tone/layout reference: finished chunks in `Book03_Python_Pandas/answers_chunks/` (code answers) and `Book05_Stats_Maths/answers_chunks/` (statistics) and `Book08_Scenarios/answers_chunks/` (scenarios).

## Who you write for
A non-technical HR professional switching to data analytics, facing a few ML and AI-tool questions in analyst interviews (not an ML engineer). Plain words; explain every term at first use (feature, label, fit, overfit, precision...); sound like a confident analyst who knows the basics and the limits. HR examples (attrition, hiring funnel, payroll, attendance, engagement) where natural, plus sales, e-commerce and finance.

## What you produce
- Read your range from `Book09_ML_AI_Tools/Book09_PartNN.md` (read-only; do NOT edit it). Copy each heading AND any data/code lines under it exactly.
- Write ONE chunk file `Book09_ML_AI_Tools/answers_chunks/B09P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line (+ data/code lines) copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file. Do not commit.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/B09P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py`. Installed: Python 3.13, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, sqlite3; matplotlib/seaborn 0.13.2 (Agg) may be installed (check). No internet; no live LLM or API calls.

## Answer template
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
(data/code lines copied exactly, if any)
**Asked at:** <only what Book09_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1-2 plain-spoken lines>
**Explain simply:**
- 2-5 bullets, jargon explained
**Sample data:** <3-10 row table or small Python data, only when the question needs data>
**Code (what you write in the interview):** <```python block: the simple interview solution, only for code/calculation questions>
**Output:** <real printed output from running exactly that code>
**What it means:** <1-2 plain-words lines (and, for evaluation/fit questions, what number to report to a manager)>
**Worked example (concept questions):** <small HR/business example with numbers, computed by script>
**Alternative / pitfalls:** <second way, or the trap (leakage, imbalance, small sample, extrapolation) when relevant>
**Likely follow-ups:** 1-3 with short answers
**Common mistakes:** <what beginners get wrong>
```
Concept-only questions omit Sample data / Code / Output. About 150-350 words, shorter for easy ones. No filler. Never use em dashes (use commas, colons, semicolons, parentheses).

## Code rules (mandatory, style_guide Sections 10 and 11)
The code block is EXACTLY what a candidate would write live: short, simple, readable, descriptive names (`employees`, `X_train`), a comment above non-obvious steps, one idea per line, `random_state=42` where randomness matters, a plain-words line after the output. No test scaffolding, asserts or debug prints. Run exactly that code and paste the real output (state "output depends on the random seed" where true; give the seed).

## Verification and honesty rules (mandatory)
- Compute EVERY number (metrics, splits, coefficients, forecasts, k-means steps, tree impurity, lift, cost-benefit) by code before writing; write the answer from computed values. If the question's inline data is inconsistent or the premise is flawed, say so inside the answer and solve the sensible version; list it in your final report.
- API/version claims (sklearn function names, removed arguments, defaults, statsmodels attributes) must be verified by running on the installed versions; otherwise label "from memory, unverified". Anything about other versions is "from memory, unverified".
- GenAI/cloud/tool facts (Copilot, ChatGPT, Claude, Snowflake, BigQuery, Fabric, AWS/Azure/GCP: features, limits, licensing, prices, regions) and legal/privacy points (India's DPDP Act, GDPR) are NOT verified here: state principles, label "from memory, unverified", and say to confirm with official documentation, IT or legal. Never state real statistics, prices or company practices as fact; price/credit numbers in questions are exercise inputs.
- For GenAI answers: show example prompts as text, never claim an LLM was run; where an AI-generated SQL/Python example is shown, run it (sqlite3/pandas) and paste real output; always include a verification step (check totals, row counts, edge cases, independent calculation) and a data-privacy note (no real employee or customer data in public tools).
- Never invent company claims, statistics or sources. "Asked at" must follow the sources file; prep-site claims stay marked unverified.
- Verification code stays in the scratch folder; the answer shows only the interview code and its real output.

## Reporting
Final reply (short): chunk path, number of answers, questions with premise problems (IDs and what you changed), what was verified by script, anything unverified.
