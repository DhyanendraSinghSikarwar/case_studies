# Wave B instructions — Book 3 (Python & pandas for Analysts) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (ESPECIALLY Sections 10 and 11: interview-ready, human-readable code), this file, and `research/Book03_PartNN_sources.md` for YOUR part. Tone/layout reference: any finished chunk in `Book05_Stats_Maths/answers_chunks/` (but Book 3 code follows Section 11 below, even simpler).

## Who you write for
A non-technical HR professional switching to data analytics. Plain words; explain every term at first use; sound like a confident candidate speaking in an interview. HR examples (attrition, headcount, attendance, payroll, hiring funnel) where natural.

## What you produce
- Read your range from `Book03_Python_Pandas/Book03_PartNN.md` (read-only; do NOT edit it).
- Write ONE chunk file `Book03_Python_Pandas/answers_chunks/B03P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/B03P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py` (pandas 3.0.5, numpy 2.5.3 installed; matplotlib/seaborn may not be installed: check; if missing, say "plot not rendered here" and verify the data/calls that can run).

## Answer template
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
**Asked at:** <only what Book03_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1–2 plain-spoken lines>
**Explain simply:**
- 2–5 bullets, jargon explained
**Sample data:** <3–8 row table or small Python data, only when the question needs data>
**Code (what you write in the interview):** <```python block: the simple interview solution>
**Output:** <real printed output, from running exactly that code>
**What it means:** <1–2 plain words lines>
**Alternative:** <second way, only if useful>
**Likely follow-ups:** 1–3 with short answers
**Common mistakes:** <what beginners get wrong>
```
Concept-only questions may omit Sample data / Code / Output. About 150–350 words, shorter for easy ones. No filler. Never use em dashes (user preference): use commas, colons, semicolons, parentheses.

## Code rules (mandatory, user rule: style_guide.md Sections 10 and 11)
- The code block is EXACTLY what a candidate would write live: short, simple, readable, descriptive names, a comment on non-obvious steps. No test scaffolding, no asserts, no seeds-for-reproducibility noise unless the question is about randomness, no extra prints.
- Run exactly that code to get the Output you paste. Check edge cases (NULLs/NaN, duplicates, ties, empty input, wrong dtype) and mention the important ones in Explain/Common mistakes, not as clutter in the code.
- Version notes (pandas 2.x/3.x behaviour such as Copy-on-Write, `str` dtype, removed APIs) only if you verified them by running; otherwise "from memory, unverified".

## Reporting
Final reply (short): chunk path, number of answers, premise changes, what was verified by running, anything unverified.
