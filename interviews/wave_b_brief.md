# Wave B brief (answer agents) — read fully, with style_guide.md and plan.md §4/§11.4

Goal: replace each `<!-- ANSWER_PENDING -->` in YOUR assigned Q-range of ONE part file with a full interview answer.
Audience: candidate for DS/MLE roles (₹30–80 LPA India MNCs/product cos + Europe/global). Answer as a strong candidate SPEAKING in the interview.

## Answer format (per question; keep the existing `### Q<n> ⭐ 🟡 …` heading and `**Asked at:**` line untouched)
**Say this first (1 line):** direct answer, plain words
**Then explain:** 2–5 bullets/table, simple language, jargon explained in one line
**Example:** short real-world or numeric example
**Code:** only where practical (Python/NumPy/pandas/scipy/sklearn); keep it short, runnable, seeded
**Follow-ups:** 1–3 likely follow-ups with short answers
**Common mistakes:** what candidates get wrong
Length: ~150–350 words for conceptual Qs (⭐ senior Qs may run longer); system-design Qs use a compact framework (requirements → data → features → model → eval → serving → monitoring → trade-offs). For "AI code review" Qs, show the buggy snippet, list the bugs, give the fix. No filler, no textbook density, formulas only when expected. Facts, formulas, complexities must be correct.

## Rules
- Edit ONLY your part file and ONLY Qs in your assigned range. Never reorder, renumber, retitle, or touch other Qs, the header, other files (except your own scratch files).
- Do not rewrite the whole file from a script/stale copy: other agents may edit other parts concurrently, and a second agent will later edit the SAME file's other range. Use the Edit tool per question (or batches of adjacent questions) so only your range changes. Re-read the file section right before each edit.
- Before inserting any code, RUN it (Python available: numpy 2.4, scipy 1.16, sklearn 1.8, pandas 2.3, statsmodels, xgboost, lightgbm; torch is NOT installed — Parts 8/9 agents may `pip install --user torch --index-url https://download.pytorch.org/whl/cpu`; if torch can't be installed, say so in your report and mark each unexecuted torch snippet with a comment `# not executed: torch unavailable`). Fix every failure; shown outputs/numbers in answers must come from actual runs.
- Scratch files: use ONLY your own subfolder `scratch/<your_part_and_range>/` under the interviews folder (e.g. scratch/P04_Q01-27/). Never use the shared scratchpad with generic names like gen.py.
- Web search is optional (only to verify a fact); never invent sources/stats.
- When done: grep your range to confirm zero ANSWER_PENDING remain in it; do not touch the rest.
- FINAL REPORT (short): range done, # code snippets run, any code that failed/was changed, any question whose premise you corrected, issues.
