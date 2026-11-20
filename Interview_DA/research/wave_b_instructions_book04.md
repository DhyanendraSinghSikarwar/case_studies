# Wave B instructions — Book 4 (Power BI & Visualization) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md`, this file, `research/Book04_PartNN_sources.md` for YOUR part (resolve or label every "uncertain" item it lists) and `research/book04_answer_notes.md` (open items for your part; resolve them from pages you fetch, or keep them labelled unverified). Reference for tone and layout: any finished chunk in `Book01_Excel/answers_chunks/`.

## Who you write for
A non-technical HR professional switching to data analytics (Power BI is common in Hyderabad/Bengaluru analyst roles). Plain words; explain every term at first use; sound like a confident candidate speaking in an interview. HR examples (attrition, headcount, attendance, payroll, hiring funnel) where natural, otherwise sales.

## What you produce
- Read your range from `Book04_PowerBI_Viz/Book04_PartNN.md` (read-only; do NOT edit it).
- Write ONE chunk file `Book04_PowerBI_Viz/answers_chunks/B04P<NN>_Q<from>-<to>.md` (create the folder if missing): for each question in your range IN ORDER, the exact heading line copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Do not touch any other file.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/65c5a153-2270-59c7-806a-2ca081fd6877/scratchpad/B04P<NN>_Q<from>-<to>` (yours only). Plain `python script.py` (pandas 3.0.5 is installed; no Power BI, no DAX engine).

## Answer template
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
**Asked at:** <only what Book04_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1–2 plain-spoken lines>
**Explain simply:**
- 2–5 bullets, jargon explained
**Example:** <real-life/HR-friendly example with numbers>
**Sample data:** <small Markdown table(s), 4–10 rows, for measure/modelling/transformation questions; table names stated above each table>
**DAX / Steps:** <the exact DAX measure(s) in a ```dax block, or Power Query M in a ```m block, or a numbered Desktop/Service click-path (Ribbon tab > group > command) for feature questions>
**Alternative:** <second way: another measure, a different feature, or a simpler approach>
**Result:** <the values the measure/step returns on the sample data, from your pandas reproduction>
**Pandas check:** <the pandas snippet that reproduces the result, with its real printed output>
**Version / licensing note:** <Desktop vs Service, free vs Pro/PPU/Fabric, Windows/Mac, preview vs GA: only what you verified on a fetched Microsoft Learn page; otherwise "from memory, unverified">
**Edge cases:** <blanks, ties, filters, totals, many-to-many, time zones… whatever matters>
**Likely follow-ups:** 1–3 with short answers
**Common mistakes:** <what beginners get wrong>
```
Concept/feature questions (no measure): omit Sample data / Result / Pandas check where not meaningful, but keep click-path, Version note and the rest. About 200–400 words; shorter for easy concept questions. No filler.

## Verification rules (mandatory)
- You cannot run DAX, Power Query M, the Power BI Service or visuals here. Every DAX/M snippet and every click-path is therefore labelled **"not run here"** in its section. What you CAN do and must do: build the sample data in pandas and reproduce, by explicit calculation, exactly what the measure/transformation should return (including filter-context behaviour, totals, blanks); print that real output as the Result. Never print an unexecuted result as if a DAX engine produced it; say "reproduced with pandas".
- Check DAX syntax and semantics against the Microsoft Learn DAX function page for every function you use (WebFetch; load with ToolSearch `select:WebFetch,WebSearch` if deferred; search for the correct URL when one 404s). Cite fetched pages by title ("Microsoft Learn: CALCULATE function (DAX)"). Do not cite pages you did not read.
- Version, licensing, preview/GA and platform facts (free vs Pro/PPU/Premium/Fabric, Windows-only Desktop, Copilot capacity requirements, refresh limits, gateway options) must come from a fetched Microsoft Learn page and be cited with the page title; otherwise write "from memory, unverified". Where two Microsoft pages conflict, state the conflict. Prices: do not quote unless fetched, and say they change.
- Tableau (Part 10): cite only fetched Tableau Help pages; otherwise "from memory, unverified".
- If a question's premise is wrong or ambiguous, say so and answer the sensible version.
- Never invent company-specific claims, statistics or sources. "Asked at" must follow the sources file.

## Reporting
Final reply (short): chunk path, number of answers, premise changes, which results were reproduced in pandas vs "not run here", which Microsoft/Tableau pages you fetched, which version/licensing facts remain unverified.
