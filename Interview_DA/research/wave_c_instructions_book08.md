# Wave C instructions — Book 8 (Scenario-Based & Data Interpretation) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 8 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md`, `research/wave_b_instructions_book08.md`. Environment: Python 3.13 (fractions, math, numpy, pandas, scipy, sqlite3). No web access.

## Scope and edit rules
- Edit ONLY your assigned `Book08_Scenarios/Book08_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book08_Scenarios/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars or order, nor a question's inline data. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C08_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Independent accuracy by execution (mandatory):** recompute EVERY figure in every answer that has data or numbers (reconciliations, rates, shares, decompositions, z/chi-square/Fisher/DiD results, sample sizes, weights and scores, bridges, headcount and attrition arithmetic, time-zone and lakh/crore conversions) in code from the question's inline data and the answer's stated assumptions, WITHOUT looking at the written result first; then compare. Fix wrong arithmetic, rounding, units, percentage vs percentage-point statements, denominators, inconsistencies between working, result and caveats. Check that each "premise problem" the writer flagged is correctly diagnosed and that the answer handles ambiguities and states its assumptions. Writers' "verified by script" claims were not always true; do not trust them.
2. **Reasoning quality:** the checks are in a sensible order, decision rules follow from the findings, stakeholder scripts are honest about what is known and unknown, causal claims are not overstated, statistical statements are correct, simple methods come first, privacy/ethics answers state principles and defer legal specifics (for example India's DPDP Act, GDPR, US four-fifths rule) as "from memory, unverified, confirm with legal".
3. **Honesty:** no real statistic, law detail, tool limit or company practice stated as fact without the "from memory, unverified" label; invented example numbers labelled illustrative; Part 8 and Part 9 personal-experience or project model answers clearly marked as templates to replace with true experience ("say it only if true"). "Asked at" may only claim what `research/Book08_PartNN_sources.md` or `research/interview_processes.md` supports; otherwise "commonly asked (no company-specific report found)"; prep-site claims stay marked unverified.
4. **Beginner clarity:** a non-technical HR reader must follow every step; every term explained at first use; sounds like a confident analyst. Fix jargon without padding.
5. **Template completeness:** header lines (Asked at, interviewer check, Say this), the structure block that fits the question type, Likely follow-ups, Common mistakes. Add anything missing.
6. **Ordering/numbering:** report only. **Duplicates/overlap** with other parts or books: report only.
7. **Style/markdown:** no em dashes in answer text (the part-title line may keep one); balanced code fences; blank line after tables; no scripts pasted into answers.

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, answers whose numbers were recomputed by code, answers wrong or changed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
