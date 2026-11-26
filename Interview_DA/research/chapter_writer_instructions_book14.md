# Book 14 chapter writer instructions (Wave A+B combined: textbook chapters)

Read first: `plan.md` (Book 14 section), `style_guide.md` (sections 1, 10, 11), `research/book14_user_index.md` (the user's own design for your chapters: topics, scenarios, practice counts; do not drop or reorder anything).

## Output (only your assigned chapters; never touch other files)
- `Book14_LogicalThinking/Ch<NN>.md` per chapter (two digits).
- `Book14_LogicalThinking/answer_key/Ch<NN>_key.md` per chapter: full step-by-step reasoning for EVERY practice question, plus answers to the 3 self-check questions.
- Scratch code goes in the scratchpad, never in the repo.

## Chapter template (in this order)
1. `# Chapter N: <title>`; one-line "What you will learn".
2. **Self-check (3 questions)** at the start (answers in the key).
3. **Concept in plain language**: reader is a complete beginner (HR professional), zero jargon left unexplained, short paragraphs, bullets and tables.
4. **Why this matters for data work** box (2-3 lines, no effectiveness claims, no invented statistics).
5. **5 solved examples**, step by step, each with the "why" of every step.
6. **2 real-life scenarios** (commerce, data, daily life; HR examples welcome). Numbers are invented and labelled "illustrative".
7. **Practice questions**: exactly the count in the index table (index "15" is the minimum if the table says more, the table wins). Numbered Q1..Qn, ordered easy, then medium, then hard, each tagged 🟢/🟡/🔴. Questions only, NO answers in the chapter file.
8. **Mistake log**: 3 to 5 most common errors. **Recap**: exactly 5 lines.
9. Optional "Try it in a spreadsheet or SQL" pointer to Book 1 or Book 2 (no new tutorials). Cross-refer "for interview-style drills see Book 13 Part N" instead of repeating.

## Hard rules
- All examples and practice questions must be NEW: never copy or lightly reword anything in `Book13_LogicalReasoning/` or `Book06_Aptitude/` Part 7. Skim their question titles for your topic and use different scenarios, names, numbers and structures.
- Brute-force or otherwise verify by code every puzzle for a UNIQUE answer, and recompute every worked example and every answer-key result. If a puzzle is not unique, fix it. Beginner-level puzzles must not need tricks.
- Fallacy, bias and claim examples are invented; never real named people, companies, news items or "studies". No claims about sources you cannot verify; label such items "from memory, unverified".
- Non-verbal figure questions cannot be shown: text-described versions only.
- Code (Python, SQL, Excel) shown in a chapter must be what a beginner would write live, readable, descriptive names, short comment above non-obvious steps (style_guide sections 10 and 11).
- Never use em dashes or en dashes anywhere (use commas, colons, semicolons, parentheses). Fences balanced.
- Maths, Python and statistics are out of scope as subjects; use them only as light tools.
- Do not invent numbers about real-world facts. Keep the voice a patient teacher, not a textbook.

## Final reply (short)
Per chapter: practice count delivered vs index, number of puzzles brute-forced, anything unverified or not met. Do not start other chapters.
