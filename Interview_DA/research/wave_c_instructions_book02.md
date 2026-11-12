# Wave C instructions — Book 2 (SQL) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 2 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md`, `research/wave_b_instructions_book02.md`, `research/Book02_WaveB_parts9-12_verified_facts.md` (environment: Python sqlite3 = SQLite 3.45.1, pandas 3.0.5, no duckdb).

## Scope and edit rules
- Edit ONLY your assigned `Book02_SQL/Book02_PartNN.md` (use the Edit tool for targeted fixes, never rewrite the whole file) and write ONE report `Book02_SQL/review/review_PartNN.md`. Never change question headings, numbers, stars or order.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/65c5a153-2270-59c7-806a-2ca081fd6877/scratchpad/C_PartNN` (yours only). Run python with plain `python script.py`.

## Checks (every answer in the part)
1. **Accuracy (mandatory, by execution):** rebuild each answer's sample table(s) in SQLite from the markdown, run the main SQL, and compare with the printed Output. Run every pandas snippet (pandas 3.0.5) and compare with the SQL result. Fix wrong SQL, wrong output tables, wrong pandas, wrong claims. Where SQL is non-SQLite-only (TOP, DATEDIFF, etc.) it must be labelled "not run here"; check syntax by reading. An automated first-pass hint list is at `/tmp/claude-0/-home-user-case-studies/65c5a153-2270-59c7-806a-2ca081fd6877/scratchpad/merge/rerun.json` (key `PP.n`); `OK` means exact match; `MISMATCH`/`sqlerr` are mostly harness limits (tables the script could not parse), so verify yourself before editing; do not trust or edit based on it alone.
2. **Factual claims:** concept statements, dialect differences, defaults, version facts must be correct. If you cannot verify a claim (offline, no docs), mark it "from memory / not run here" rather than leaving it unqualified. Never add invented company claims or statistics. "Asked at" may only claim what `research/Book02_PartNN_sources.md` or `research/interview_processes.md` supports.
3. **Beginner clarity:** a non-technical HR reader must follow it; every term explained at first use; fix jargon without padding. Answer sounds like a confident candidate.
4. **Template completeness:** each answer has Asked at, What the interviewer is checking, Say this in the interview, Explain simply, Example, Likely follow-ups, Common mistakes; query questions also Sample data, SQL, Output, pandas equivalent, Edge cases. Add any missing field (e.g. a short Example with numbers for design/plan questions).
5. **Ordering / numbering:** stars descending then 🟢→🔴, numbering continuous (do not change; just report if wrong).
6. **Duplicates / overlap** with other parts: report only.
7. Markdown validity: balanced code fences, tables render.

## Report (`review/review_PartNN.md`, ≤ 60 lines)
Counts (answers checked, executed OK, fixed), a table of every fix (Q, what was wrong, how fixed), unresolved items, claims labelled unverified. Final reply to me: report path, numbers, anything you could not verify. Keep it short.
