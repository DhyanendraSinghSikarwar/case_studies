# Wave C instructions — Book 7 (Guesstimates, Case Studies & Business Metrics) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 7 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md`, `research/wave_b_instructions_book07.md`. Environment: Python 3.13 (fractions, math, numpy, pandas, scipy, sqlite3). No web access.

## Scope and edit rules
- Edit ONLY your assigned `Book07_Guesstimates_Cases/Book07_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book07_Guesstimates_Cases/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars or order, nor a question's inline data. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C07_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Independent accuracy by execution (mandatory):** recompute EVERY number in every answer (guesstimate chains, ranges, sensitivities, metric formulas, case arithmetic, sample-size and test figures, decompositions) in code, from the question's inline data and the answer's own stated assumptions, WITHOUT looking at the written result first; then compare. Fix wrong arithmetic, wrong rounding, wrong units (lakh/crore conversions!), wrong percentage vs percentage-point statements, wrong denominators, and inconsistent numbers between the table, steps, result and sanity check. Verify that each Sanity check really is a second route and that the stated range follows from the stated sensitivity. Writers' "verified by script" claims were not always true; do not trust them.
2. **Reasoning quality:** the structure is MECE, the clarifying questions are sensible, the decision rules follow from the data shown, premise flaws or ambiguities in the question are flagged and handled, causal claims are not overstated, and statistical statements (z-tests, DiD, Simpson's paradox, sample sizes) are correct.
3. **Honesty about facts:** every real-world base number (population, households, vehicles, prices, wages, usage, company volumes) must be labelled assumed/approximate/unverified; no real statistic or company figure may be stated as fact; numbers from the question's text are exercise inputs. Fix violations. Assumptions reused across answers must stay consistent. "Asked at" may only claim what `research/Book07_PartNN_sources.md` or `research/interview_processes.md` supports; otherwise "commonly asked (no company-specific report found)"; prep-site claims stay marked unverified.
4. **Beginner clarity:** a non-technical HR reader must follow every step; every term (CAC, LTV, NRR, DiD, MECE, TAM...) explained at first use; sounds like a confident candidate thinking aloud. Fix jargon without padding.
5. **Template completeness:** header lines (Asked at, interviewer check, Say this), the structure block that fits the question type (guesstimate / metric / case / concept), Likely follow-ups, Common mistakes. Add anything missing.
6. **Ordering/numbering:** report only. **Duplicates/overlap** with other parts or books: report only.
7. **Style/markdown:** no em dashes in answer text (the part-title line may keep one); balanced code fences; blank line after tables; no scripts pasted into answers.

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, answers whose numbers were recomputed by code, answers wrong or changed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
