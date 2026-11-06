# Wave C instructions — Book 5 (Statistics & Maths) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 5 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md` (incl. Section 10 code readability), `research/wave_b_instructions_book05.md`. Environment: Python with numpy, pandas, scipy, statsmodels (no Excel, no web).

## Scope and edit rules
- Edit ONLY your assigned `Book05_Stats_Maths/Book05_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book05_Stats_Maths/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars or order. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/C05_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Accuracy by execution:** extract every Python snippet and run it; compare printed output to the pasted output and to numbers quoted in the prose. Fix wrong code, outputs, numbers. Re-derive by hand/independently every worked number (probabilities, z/t/p-values, CIs, sample sizes, regression stats). Seeds: results must reproduce.
2. **Statistical correctness:** definitions (p-value, CI interpretation, Type I/II, SD vs SE, n vs n-1, one vs two tailed, assumptions), formulas, Excel function names/arguments and the Excel version they need (STDEV.S 2010+, etc.). Fix misconceptions. Excel formulas must be labelled "not run in Excel here"; verify their logic against Python.
3. **Claims:** "Asked at" may only say what `research/Book05_PartNN_sources.md` or `research/interview_processes.md` supports; otherwise "commonly asked (no company-specific report found)". No invented companies, statistics, prices or sources. Facts from memory must be labelled "from memory, unverified".
4. **Beginner clarity:** a non-technical HR reader must follow it; every term explained at first use; sounds like a confident candidate speaking. Fix jargon without padding.
5. **Code readability (user rule):** descriptive names, one step per line, a plain-English comment above each step, a plain-words line after each output. Fix code that violates it.
6. **Template completeness:** Asked at, What the interviewer is checking, Say this in the interview, Explain simply, Worked example, Likely follow-ups, Common mistakes (plus Formula / Excel-Python where meaningful). Add anything missing.
7. **Ordering/numbering:** report only. **Duplicates/overlap** with other parts: report only.
8. **Style/markdown:** no em dashes in answer text (user preference; headings of the file title may keep theirs); balanced code fences; blank line after tables.

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, snippets run OK, answers fixed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
