# Wave C brief (review agents) — read fully, plus style_guide.md and plan.md §11.5

Role: reviewer for ONE part file of Book 1 (answers already written). Fix problems IN PLACE with minimal Edits. You are the independent check: do not trust the earlier agent's claims.

## Checks (plan §11.5)
1. Completeness: no `ANSWER_PENDING`; every Q has Say this first / Then explain / Example / Follow-ups / Common mistakes (Code optional).
2. Accuracy: verify every formula, complexity, definition, numeric claim and citation. Web-verify citations/stats you doubt (WebSearch); if unverifiable, soften wording or remove; never invent sources.
3. Code: extract EVERY python block and RUN it standalone (own imports/seed) from a local scratch dir `C:\Users\11624\AppData\Local\Temp\claude\rev_<part>\` (OneDrive Python is very slow; keep commands short, background long ones). Compare printed numbers with the numbers quoted in the answer; fix code or text so they match. A block that cannot run standalone (relies on variables from another block) must be made standalone or clearly marked as a continuation. Blocks that truly need unavailable libs/GPU stay marked `# not executed: <reason>` (stale reasons must be corrected; torch CPU IS installed; transformers, umap, hdbscan, faiss, prophet are NOT).
4. Clarity: the answer must sound like a strong candidate speaking, simple, structured. Trim textbook density; fix muddled sentences; ensure jargon explained.
5. Illustrative/hand-computed numbers must be labelled as such. No unverifiable stats presented as fact.
6. Header lines of the part file (Target / Actual / Stars counts) must match the actual file: recount stars (⭐⭐⭐/⭐⭐/⭐) and questions and correct them. Also remove the "Dedupe pass" note's stale remark about star counts if header now correct.

## Rules
- Edit only your part file (plus your own scratch/notes). Never reorder, renumber, retitle or delete questions; keep `**Asked at:**` lines. Preserve the file's line endings (some files are CRLF, some LF).
- Use Edit per fix (re-read the section first). Do not rewrite the file from a script.
- Write review notes to `review_notes/Book1_PartNN_review.md` (create the folder if missing): list of fixes (Q#, what, why), code blocks run (count, pass/fail), unresolved items, anything you could not verify. Be honest; list failures.
- Part-specific known items are given in your prompt; handle them first.
- FINAL REPORT (short): questions reviewed, # code blocks run / failed / fixed, # factual fixes, unresolved items.
