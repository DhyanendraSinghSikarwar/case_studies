# Wave B instructions — Book 6 (Aptitude & Business Maths) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (Sections 10 and 11), this file, and `research/Book06_PartNN_sources.md` for YOUR part. Tone/layout reference: any finished chunk in `Book05_Stats_Maths/answers_chunks/`.

## Who you write for
A non-technical HR professional switching to data analytics who must clear online aptitude gates. Plain words; explain every term and shortcut at first use; sound like a confident candidate who knows the fast method AND why it works. Business/HR flavour where natural.

## What you produce
- Read your range from `Book06_Aptitude/Book06_PartNN.md` (read-only; do NOT edit it).
- Write ONE chunk file `Book06_Aptitude/answers_chunks/B06P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line copied unchanged (and, for questions that carry a data table or statements/options below the heading, copy that body too, exactly), then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file. Do not commit.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/B06P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py` (numpy, pandas, scipy, sympy-free: use fractions, itertools, math).

## Answer template
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
**Asked at:** <only what Book06_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line: which skill/pattern the test is probing>
**Say this in the interview:** <1-2 plain-spoken lines (the approach and the final answer)>
**Answer:** <the final answer, bold, with units (and the option letter if options are given)>
**Step-by-step working:** <numbered plain-arithmetic steps a beginner can follow; every number shown>
**Fast method (30 seconds):** <the shortcut / mental-maths route, with why it works; omit if none beyond the working>
**Check:** <one-line independent check (reverse calculation, estimate, or "verified by script")>
**Explain simply:**
- 2-4 bullets: the concept or formula behind it, jargon explained
**Likely follow-ups:** 1-2 with short answers (a variant with changed numbers is ideal)
**Common mistakes / traps:** <what beginners get wrong; the wrong answer the test setter expects you to pick>
```
Concept/method questions: keep Answer, Explain simply, a worked mini-example with numbers, follow-ups, traps; drop what does not fit. Data-sufficiency (Part 9): state the verdict for Statement I alone, II alone, both together, then the final option; explain WHY each is or is not enough. Logical reasoning (Part 7): show the full deduction (a small diagram/table/arrangement in text) and confirm uniqueness. Data interpretation (Part 8): show which cells/values are used and the arithmetic. English items (Part 11): give the correct choice and the grammar/vocabulary rule; SQL/CS items: give the answer, explain simply, and a short runnable SQL block (run it on Python's sqlite3, show the real output) where relevant. About 120-300 words each; shorter for easy ones. No filler. Never use em dashes (use commas, colons, semicolons, parentheses).

## Verification rules (mandatory)
- The question texts were written without computing answers. Solve EVERY numeric/logical question by code (fractions, itertools, brute force for puzzles and arrangements, exact arithmetic for interest, ratios, probability) BEFORE writing the answer, and write the answer from the verified value. If a question is ambiguous, has no valid answer, or has a flawed premise (e.g. non-unique puzzle solution, impossible numbers), say so inside the answer and solve the sensible version; list it in your final report.
- Round only where the question asks; state the rounding.
- Verification code stays in your scratch folder: do NOT paste scripts into answers (style_guide Section 11: show the candidate's working, not scaffolding). Say "Check: verified by script" or give a hand check.
- Never invent company claims, statistics or sources. "Asked at" must follow the sources file; prep-site claims are unverified.

## Reporting
Final reply (short): chunk path, number of answers, questions with premise problems (IDs and what you changed), what was verified by script, anything unverified.
