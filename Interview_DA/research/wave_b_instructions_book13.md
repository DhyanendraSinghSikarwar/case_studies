# Wave B instructions — Book 13 (Logical Reasoning & Analytical Thinking for Data Analysts) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5, Book 13 section), `style_guide.md` (Sections 10 and 11), this file, and `research/Book13_PartNN_sources.md` for YOUR part. Tone/layout reference: a finished chunk in `Book06_Aptitude/answers_chunks/` (for example `B06P07_*`). Environment: Python 3.13 (fractions, itertools, math, numpy, pandas, scipy, sqlite3). No web access.

## Who you write for
A non-technical HR professional switching to data analytics who must clear online reasoning gates and analyst interviews. Plain words; explain every term, convention and shortcut at first use; sound like a confident candidate who knows the fast method AND why it works.

## What you produce
- Read your range from `Book13_LogicalReasoning/Book13_PartNN.md` (read-only; do NOT edit it).
- Write ONE chunk file `Book13_LogicalReasoning/answers_chunks/B13P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line copied unchanged AND any data/option/statement lines under the heading copied exactly (everything between the heading and the `<!-- ANSWER_PENDING -->` marker), then the full answer. Do not output the marker. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file. Do not commit.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/B13P<NN>_Q<from>-<to>` (yours only).

## Answer template (puzzles and problems)
```
### Q<n> ⭐⭐⭐ 🟢 <question, copied exactly>
(data/options lines copied exactly)
**Asked at:** <only what Book13_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line: which reasoning skill/pattern is probed>
**Say this in the interview:** <1-2 plain-spoken lines: the approach and the final answer>
**Answer:** <the final answer, bold, with units / option letter / the full arrangement or table where asked>
**Step-by-step reasoning:** <numbered steps a beginner can follow; for puzzles show the deduction order, a small text diagram or table of the final arrangement, and state WHY the solution is unique (or which assumption fixes it)>
**Fast method (30 seconds):** <the shortcut / elimination order / diagramming trick, with why it works; omit if none beyond the reasoning>
**Check:** <one-line independent check: re-read every clue against the final arrangement, or "checked by brute force over all N possibilities">
**Explain simply:**
- 2-4 bullets: the concept or rule behind it, jargon explained
**Likely follow-ups:** 1-2 with short answers (a variant with changed clue or numbers is ideal; verify it by code too)
**Common mistakes / traps:** <what beginners get wrong; the tempting wrong answer>
```
Concept/method/strategy questions (Parts 1, 8, 12 and the "why/how" items elsewhere): drop Step-by-step and Fast method if they do not fit; keep Answer, Explain simply, a worked mini-example with numbers, follow-ups, traps. About 120-300 words each (puzzles with a full arrangement table may run to about 350); shorter for easy ones. No filler. Never use em dashes or en dashes (use commas, colons, semicolons, parentheses).

## Part-specific rules
- Part 1 (formats, strategy, accuracy vs speed): numeric items (negative-marking expected value, time budgets) must be computed by code. Test patterns, counts and timings reported by prep sites are "reported, unverified" and must never be stated as fact; company-specific claims follow the sources file. Advice such as skip rules and time splits is "our suggestion", not a research finding.
- Part 2 (deductive logic): state the convention (every named group non-empty; "some" means at least one) where the question does; verify every syllogism conclusion by enumerating Venn regions or models (itertools over region occupancy), not by memory. Conditional logic: give converse, inverse, contrapositive correctly; name fallacies correctly.
- Parts 3-6 and 10: brute-force every puzzle (permutations, constraint enumeration) and confirm the stated answer is the ONLY consistent one; show the deduction and the final arrangement. If a puzzle is not unique, has no solution, is ambiguous, or its premise is flawed, say so inside the answer, solve the sensible version (state the assumption), and list it in your report. Counting questions: show the formula and the brute-force count.
- Part 7 (series, analogy, classification): the rule must be stated and shown to fit EVERY given term; for odd-one-out and analogy items, say which rule you used and, if a second defensible rule exists, state it and why the intended answer is preferred; note when only one rule is defensible.
- Part 8 (critical reasoning): the multiple-choice items have one intended best answer by design: justify why each wrong option fails (scope shift, reverse causality, correlation not cause, too strong, irrelevant); numeric parts (Simpson's paradox tables, rates, p-values) computed by code; a stated p-value must come from the exact test named.
- Part 9 (data-analyst logic): run every SQL snippet on Python's sqlite3 and print the real output in the answer; Excel and other-database behaviours that cannot be run here (Excel blank/text comparisons, COUNTIF with "<>", PostgreSQL integer division, SQL Server or Oracle specifics) must be labelled "from memory, not run here; confirm in the tool" and never stated more strongly than that; three-valued logic tables computed by code.
- Part 11 (mock sets): answer each question in the standard template plus "Target time" (as written in the heading) and one line "If you are short of time: skip or guess rule"; the set strategy notes are in the part file's Scope line; time guidance is a rule of thumb, labelled as such.
- Part 12 (how to develop): resources and courses only if confident, labelled "from memory, unverified, check the link and whether still free"; no effectiveness claims, pass rates or timelines presented as research (plans are "our suggestion"); worked items (schedules, accuracy tables) computed by code.

## Verification rules (mandatory)
- The question texts were written before answers were computed. Solve EVERY numeric, logical, puzzle, series, SQL and trace question by code BEFORE writing the answer, and write the answer from the verified value. Round only where the question asks; state the rounding.
- Verification code stays in your scratch folder: do NOT paste scripts into answers (SQL blocks for Part 9 are fine and must show real sqlite3 output). Say "Check: verified by script / brute force" only if you really ran it; otherwise say "hand-checked".
- Never invent company claims, statistics, tool facts or sources. Prep-site claims are unverified.

## Reporting
Final reply (short): chunk path, number of answers, questions with premise problems (IDs and what you changed), what was verified by script vs by hand, anything unverified.
