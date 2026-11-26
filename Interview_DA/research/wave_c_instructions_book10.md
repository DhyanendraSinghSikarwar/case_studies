# Wave C instructions — Book 10 (Domain Knowledge) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 10 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md` (Sections 10, 11), `research/wave_b_instructions_book10.md`. Environment: Python 3 (math, fractions, numpy, pandas, scipy, sqlite3). No web access.

## Scope and edit rules
- Edit ONLY your assigned `Book10_Domain/Book10_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book10_Domain/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars or order, nor a question's inline data. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/C10_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Independent accuracy by execution (mandatory):** recompute EVERY figure in every answer that has data or numbers (rates, shares, ratios, bridges, decompositions, break-evens, projections, test results, sample sizes, conversions between lakh/crore, percentage vs percentage-point statements) in code from the question's inline data and the answer's stated assumptions, WITHOUT looking at the written result first; then compare. Fix wrong arithmetic, rounding, units, denominators, and any inconsistency between working, result and caveats. Run every SQL/pandas snippet shown and compare to the pasted output. Writers' "verified by script" claims were not always true; do not trust them.
2. **Domain correctness:** definitions and formulas (for example NPA, NIM, loss ratio, ARPOB, OTIF, EOQ, safety stock, utilisation, realisation, attrition, compa-ratio) must be standard or clearly labelled "my definition; varies by company". Fix wrong or misleading domain statements. Where unsure, relabel "from memory, unverified" rather than assert.
3. **Honesty and compliance:** no real statistic, benchmark, regulation detail (RBI, IRDAI, CDSCO, HIPAA, DPDP, GST, PF/ESI, labour law), tool feature (Workday, Alteryx) or company practice stated as fact without the "from memory, unverified" label; regulation text only at awareness level with "confirm with the compliance/legal team"; no legal, medical or financial advice; invented example numbers labelled illustrative; personal-experience answers clearly templates ("say it only if true"). "Asked at" may only claim what `research/Book10_PartNN_sources.md` or `research/interview_processes.md` supports; otherwise "commonly asked (no company-specific report found)".
4. **Beginner clarity:** a non-technical HR reader with zero domain knowledge must follow every answer; every domain term explained at first use; sounds like a confident analyst. Fix jargon without padding.
5. **Code rule (style_guide Sections 10-11):** any code shown is the interview version: short, readable, descriptive names, real output pasted, plain-words line after it. Fix scaffolding.
6. **Template completeness:** Asked at, interviewer check, Say this, Explain simply, Likely follow-ups, Common mistakes (plus Worked example / Data and tables / Regulation note where the question needs them). Add anything missing.
7. **Ordering/numbering:** report only. **Duplicates/overlap** with other parts or books: report only.
8. **Style/markdown:** no em dashes in answer text (the part-title line may keep one); balanced code fences; blank line after tables; no verification scripts pasted into answers.

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, answers whose numbers were recomputed by code, answers wrong or changed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
