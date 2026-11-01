# Wave C instructions — Book 4 (Power BI & Visualization) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 4 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md`, `research/wave_b_instructions_book04.md`. Environment: Python + pandas 3.0.5 only; no Power BI, no DAX engine, no Power Query, and learn.microsoft.com / help.tableau.com are unreachable (do not try to fetch them).

## Scope and edit rules
- Edit ONLY your assigned `Book04_PowerBI_Viz/Book04_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book04_PowerBI_Viz/review/review_PartNN.md` (create the folder if missing). Never change question headings, numbers, stars or order. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C04_PartNN`. Run python with plain `python script.py`.

## Checks (every answer in the part)
1. **Accuracy by execution:** extract every "Pandas check" snippet and run it (pandas 3.0.5). Compare printed output to the answer's printed output and to its "Result" line. Fix wrong code, wrong outputs, wrong Results. Re-derive by hand any DAX measure's result on the sample data and confirm it matches the Result (filter context, totals, blanks, ties).
2. **DAX / M syntax and semantics (by reading):** check function names, argument order, balanced brackets/quotes/VAR-RETURN, column vs measure references, and that the measure returns what the answer says. Fix errors. Every DAX/M snippet and click-path must be labelled "not run here"; add the label if missing. No result may be presented as if a DAX engine produced it (must say "reproduced with pandas").
3. **Factual claims:** version, licensing, Desktop/Service, preview/GA, menu-name and DAX-behaviour claims must be correct or labelled "from memory, unverified" (nothing could be fetched). Never add invented company claims, statistics, prices or sources. "Asked at" may only claim what `research/Book04_PartNN_sources.md` or `research/interview_processes.md` supports. Check consistency of recurring claims (e.g. Desktop Windows-only, refresh limits, licence tiers, DISTINCTCOUNT blank handling) with the unverified labelling used elsewhere in the part.
4. **Beginner clarity:** a non-technical HR reader must follow it; every term explained at first use; answer sounds like a confident candidate speaking. Fix jargon without padding.
5. **Template completeness:** each answer has Asked at, What the interviewer is checking, Say this in the interview, Explain simply, Example, Version / licensing note, Edge cases, Likely follow-ups, Common mistakes; measure/modelling/transformation questions also Sample data, DAX / Steps, Alternative, Result, Pandas check. Add any missing field.
6. **Ordering / numbering:** stars descending then 🟢→🔴, numbering continuous (do not change; just report).
7. **Duplicates / overlap** with other parts: report only.
8. **Markdown validity:** balanced code fences, tables render (blank line after every table).

## Report (`review/review_PartNN.md`, ≤ 60 lines)
Counts (answers checked, pandas snippets run OK, answers fixed), a table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply to me: report path, numbers, anything you could not verify. Keep it short.
