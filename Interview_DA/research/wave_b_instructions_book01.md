# Wave B instructions — Book 1 (Excel) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md`, this file, and `research/Book01_PartNN_sources.md` for YOUR part (its "uncertain" items must be resolved or labelled).

## Who you write for
A non-technical HR professional switching to data analytics. Plain words; explain every term at first use; sound like a confident candidate speaking in an interview. HR examples (attendance, attrition, payroll, hiring) where natural, otherwise sales.

## What you produce
- Read your range from `Book01_Excel/Book01_PartNN.md` (read-only; do NOT edit it).
- Write ONE chunk file `Book01_Excel/answers_chunks/B01P<NN>_Q<from>-<to>.md` (create folder if missing): for each question in your range IN ORDER, the exact heading line copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Do not touch any other file.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/65c5a153-2270-59c7-806a-2ca081fd6877/scratchpad/B01P<NN>_Q<from>-<to>` (yours only). Plain `python script.py`.

## Answer template
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
**Asked at:** <only what Book01_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1–2 plain-spoken lines>
**Explain simply:**
- 2–5 bullets, jargon explained
**Example:** <real-life/HR-friendly example with numbers>
**Sample sheet:** <small Markdown table laid out like the Excel grid, with column letters and row numbers where cell addresses are used, 4–8 data rows>
**Formula / Steps:** <the exact formula(s) with cell addresses, or numbered click-path (Ribbon tab > group > command) for feature questions>
**Alternative:** <second way: another formula, a newer function, or a feature route>
**Result:** <the values the formula returns on the sample sheet>
**Version note:** <Excel 2016 / 2019 / 2021 / 365 / Google Sheets availability that matters for this answer>
**Edge cases:** <blanks, text-numbers, duplicates, errors, ties… whatever matters>
**Likely follow-ups:** 1–3 with short answers
**Common mistakes:** <what beginners get wrong>
```
Concept/feature questions (no formula): omit Sample sheet/Result if not meaningful, keep click-path, Version note and the rest. Length about 200–400 words; shorter for easy concept questions. No filler.

## Verification (mandatory)
- Use the helper `tools/xl_eval.py` (read its docstring): it recalculates formulas with headless LibreOffice 24.2 and returns computed values. The **Result** you print for a formula must be the value returned by running it, not hand-written. Build each answer's sample sheet in a script, run the formulas, and paste the real values.
- LibreOffice 24.2 does NOT support XLOOKUP, XMATCH, FILTER, UNIQUE, SORT, SORTBY, LET, TEXTSPLIT/TEXTBEFORE/TEXTAFTER, spill, LAMBDA; and cannot run pivot tables, Power Query, VBA, Copilot, charts. For those: write the formula/steps, reproduce the expected result with pandas (pandas is installed) or by explicit hand calculation shown in the answer, and label that part **"not run here"**. Never print an unexecuted result as if it ran.
- Formulas in Excel may behave differently from LibreOffice in edge cases (text-to-number coercion, locale, date serials). If an answer depends on such behaviour, say so in Edge cases and mark "from Microsoft documentation / memory" accordingly.
- Version/availability facts (e.g. XLOOKUP not in Excel 2016/2019, UNIQUE 365/2021 only, Power Query built in from Excel 2016) must come from a Microsoft Support page you actually fetched (WebFetch; search for the right URL if one 404s) and cited in the answer text as "(Microsoft Support)" with the page title; otherwise label "from memory, unverified". Resolve the 'uncertain' items listed in your part's sources file the same way.
- Google Sheets facts: from Google Docs Editors Help if fetched; otherwise "from memory, unverified".
- If a question's premise is wrong or ambiguous, say so and answer the sensible version.
- Never invent company-specific claims, statistics or sources. Do not cite pages you did not read.

## Reporting
Final reply (short): chunk path, number of answers, premise changes, which results were run vs "not run here", which version/Google facts are unverified.
