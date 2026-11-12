# Wave C instructions — Book 6 (Aptitude & Business Maths) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 6 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md`, `research/wave_b_instructions_book06.md`. Environment: Python 3.13 with fractions, itertools, math, numpy, pandas, sqlite3.

## Scope and edit rules
- Edit ONLY your assigned `Book06_Aptitude/Book06_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book06_Aptitude/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars or order, nor a question's data body. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C06_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Independent accuracy by execution (mandatory):** re-solve EVERY numeric, probability, puzzle, data-interpretation and data-sufficiency question yourself in code (exact fractions, brute force over arrangements/orders/values, enumeration of models for syllogisms and data sufficiency) WITHOUT looking at the written answer first, then compare with the answer, its step-by-step working, fast method, Check line and follow-up numbers. Fix wrong answers, wrong intermediate steps, wrong follow-up variants, wrong option letters. Also verify the ambiguity notes (non-unique puzzle solutions, unstated assumptions): the answer must state any assumption it relies on. Writers' "verified by script" claims were not always true (some verdicts and follow-ups were hand-checked): do not trust them; fix any overstated "Check" wording.
2. **Shortcuts and rules:** confirm each "fast method" is mathematically valid for the stated case and its limits are stated (e.g. successive change formula, alligation, 5/18 conversion, divisibility rules, cyclicity).
3. **Concept/English/SQL items:** correctness of rules and claims (grammar, vocabulary, SQL/CS fundamentals); run any SQL on sqlite3 and compare with the printed output; label dialect- or database-specific claims.
4. **Claims:** "Asked at" may only say what `research/Book06_PartNN_sources.md` or `research/interview_processes.md` supports; otherwise "commonly asked (no company-specific report found)". No invented companies, statistics or sources; prep-site claims stay marked unverified. Time-per-question or pass-mark guidance is rule of thumb and must be labelled so.
5. **Beginner clarity:** a non-technical HR reader must follow every step; every term and shortcut explained at first use; sounds like a confident candidate. Fix jargon without padding.
6. **Template completeness:** Asked at, What the interviewer is checking, Say this in the interview, Answer, Step-by-step working (numeric/puzzle items), Fast method (where one exists), Check, Explain simply, Likely follow-ups, Common mistakes / traps. Add anything missing.
7. **Ordering/numbering:** report only. **Duplicates/overlap** with other parts: report only.
8. **Style/markdown:** no em dashes in answer text (the part-title line may keep one); balanced code fences; blank line after tables; no scripts pasted into answers (SQL blocks for SQL items are fine).

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, answers re-solved by code, answers wrong or changed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
