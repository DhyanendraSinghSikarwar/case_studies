# Wave C instructions — Book 3 (Python & pandas) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 3 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md` (Sections 10 and 11: interview-ready, human-readable code), `research/wave_b_instructions_book03.md`. Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2, seaborn 0.13.2 (use the Agg backend), requests. No internet for docs; live API calls cannot run (use a local mock if needed).

## Scope and edit rules
- Edit ONLY your assigned `Book03_Python_Pandas/Book03_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book03_Python_Pandas/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars or order. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C03_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Accuracy by execution:** extract every Python snippet (rebuild its sample data from the answer's own Sample data table or code) and run it; compare the printed output to the pasted Output and to numbers in the prose ("What it means"). Fix wrong code, outputs and numbers. Snippets must run exactly as shown (imports included).
2. **Correctness of concepts:** pandas/NumPy/Python behaviour claims (Copy-on-Write, `str` dtype, removed or deprecated APIs, `inplace`, `apply` vs vectorised, merge/groupby semantics, NaN handling). Verify by running on pandas 3.0.5. Anything about pandas 2.x or other versions you cannot run must be labelled "from memory, unverified".
3. **Claims:** "Asked at" may only say what `research/Book03_PartNN_sources.md` or `research/interview_processes.md` supports; otherwise "commonly asked (no company-specific report found)". No invented companies, statistics or sources.
4. **Beginner clarity:** a non-technical HR reader must follow it; every term explained at first use; sounds like a confident candidate speaking. Fix jargon without padding.
5. **Interview-ready code (user rule, style_guide Sections 10, 11):** the code block is what a candidate would write live: simple, descriptive names, a comment on non-obvious steps, no test scaffolding or debug prints, plain-words line after the output. Fix violations.
6. **Template completeness:** Asked at, What the interviewer is checking, Say this in the interview, Explain simply, What it means, Likely follow-ups, Common mistakes; code questions also Sample data, Code, Output. Add anything missing.
7. **Ordering/numbering:** report only. **Duplicates/overlap** with other parts or books: report only.
8. **Style/markdown:** no em dashes in answer text; balanced code fences; blank line after tables.

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, snippets run OK, answers fixed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
