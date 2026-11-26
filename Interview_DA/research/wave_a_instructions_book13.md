# Wave A instructions — Book 13 (Logical Reasoning & Analytical Thinking for Data Analysts) question lists (plan.md Sections 8.3, 8.4, Book 13 table)

You build the FROZEN QUESTION LIST for ONE part of Book 13. No answers: every question is followed by `<!-- ANSWER_PENDING -->`. Today is 2026-11-26.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9, the Book 13 section with its boundaries and part table), `style_guide.md` (Sections 2, 3, 7, 8), `research/interview_processes.md` (aptitude and reasoning gates at Infosys, Accenture, Wipro, Fractal, Mu Sigma, Tiger and others), `research/market_skills_2026.md`, and for format only the header and a few entries of `Book06_Aptitude/Book06_Part07.md` (do not copy questions).

## Book 13 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | Why analyst roles test logical reasoning; test formats (online assessments, Mu Sigma/Fractal-style rounds, service MNC tests); strategy, time management, accuracy vs speed | 40 |
| 2 | Deductive logic: syllogisms (Venn and possibility cases), "only/all/some/none", conditional logic (if-then, converse, contrapositive), common fallacies 🟡 | 70 |
| 3 | Inequalities (direct and coded), comparison, ranking, order and position puzzles 🟢🟡 | 50 |
| 4 | Linear and circular seating, floor, box, month and day arrangements 🟡🔴 | 70 |
| 5 | Multi-attribute puzzles (who-owns-what grids, schedules, tournaments), constraint puzzles, truth-teller and liar 🔴 | 70 |
| 6 | Deeper blood relations and family trees, direction and distance, coding-decoding, input-output and machine logic 🟡 | 60 |
| 7 | Letter and alphanumeric series, analogy, classification, pattern recognition 🟢🟡 | 50 |
| 8 | Critical reasoning: assumption, strengthen/weaken, inference, conclusion, cause vs correlation, evaluating a data-driven argument 🟡🔴 | 60 |
| 9 | Data-analyst logic: boolean logic, truth tables, IF/AND/OR logic, SQL and Excel logic puzzles (NULL and three-valued logic, NOT IN traps), decision tables, flowchart and pseudocode tracing, edge cases 🟡🔴 | 60 |
| 10 | Quantitative-logic puzzles and brain teasers (new variants only): weighing, measuring, age, set counting, combinatorial and estimation logic 🔴 | 50 |
| 11 | Timed mixed mock sets in online-assessment style, with strategy notes per set 🟡🔴 | 40 |
| 12 | How to develop logical reasoning: roadmap, daily practice plan, free resources, practice sets, mini-projects, self-check tests | 20 |

## Boundaries (do not duplicate; other agents' and other books' scope)
- `Book06_Aptitude/Book06_Part07.md` (80 questions: basic blood relations, syllogisms, seating, coding, directions, ranking, clocks, calendar, statement-assumption, classic brain teasers) stays as is. BEFORE writing, read ALL of its question headings (`grep '^### Q' Book06_Aptitude/Book06_Part07.md`) and never repeat or lightly reword any of them; Book 13 asks deeper and different questions (new scenarios, new numbers, harder structures, "why" and method questions).
- Book 6 owns number series and number system (Part 5), data interpretation (Part 8), data sufficiency (Part 9), permutation/combination/probability in aptitude style (Part 6), speed tricks and quantitative mocks (Part 10). Book 5 owns probability and correlation concepts. Book 2 owns SQL how-to (Part 9 here is logic puzzles and traps about SQL/Excel semantics, not syntax tutorials). Book 11 Part 10 owns structured-thinking soft-skill playbooks. Book 7 owns guesstimates and cases (Part 10 here is logic/measurement puzzles with exact answers, not market-size estimates; "estimation logic" means bounding and order-of-magnitude reasoning with checkable arithmetic).
- Non-verbal figure questions (mirror images, paper folding, figure series, embedded figures) cannot be shown faithfully in Markdown: do NOT write them. Use text-described versions only (for example cube painting, dice with stated faces, clock/calendar, grids given as Markdown tables).

## Question format (reasoning books need unique, checkable answers)
Entries are (a) concept/method questions ("How do you test whether a conclusion follows from two 'some' statements?", "What is the contrapositive of 'if a payment is late, a fee applies'?") and (b) fully specified solvable problems. At least ~70% of Parts 2-10 must be fully specified problems with a SINGLE checkable answer. Every puzzle must be self-contained: state every condition, all data, the number of items, and (for multiple-choice) the options inline as Markdown, so it can be solved without a picture. Puzzles must have a UNIQUE solution (the answer agent will brute-force each one; if a puzzle does not have a unique solution, rewrite it before freezing: you may run your own checks in scratch code). Never write a question whose answer depends on an unstated assumption. Part 1 and Part 12 are conceptual/how-to and strategy, with a few small worked items; Part 11 mock sets are groups of questions: write each as an individual entry labelled in the question text, for example "Mock Set 1, Q3 (suggested time 75 seconds): ...", with sets of 8 to 10 questions that mix topics from Parts 2-10 (new questions, not copies), and the set title/strategy in the Scope line.
HR and business flavour where natural (shifts, payroll batches, interview panels, attendance, hiring pipeline, sales regions) but do not force it.

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred; WebFetch is unavailable). At least 4 distinct searches for your topic (at least 6 for Part 1, Part 8, Part 9 and Part 12), for example "<topic> logical reasoning questions data analyst online assessment", "<topic> reasoning asked TCS NQT Infosys Wipro Accenture Cognizant", "<topic> logical reasoning 2025 2026", "Mu Sigma Fractal reasoning round", plus "how to prepare logical reasoning for data analyst". Glassdoor/AmbitionBox/Reddit/LinkedIn may be blocked; record that.
2. Record every source in `research/Book13_PartNN_sources.md` in the format of `research/Book06_Part07_sources.md` (URL, what it was used for, type, recency, honest note that it was only a search snippet). No invented sources or company claims; mark unverified items. State limits. Give star-assignment reasoning (stars are judgement unless a source gives frequency).
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Canonical wording, one question per entry, no duplicates inside the part or with Book 6 Part 7; do not write questions owned by another part.
- Stars: ⭐⭐⭐ appears in most reasoning gates, ⭐⭐ often, ⭐ occasional/differentiator. Difficulty 🟢🟡🔴. Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous. For Part 11 sort by mock set instead (set order, then question order inside the set) and state this in the Scope line.
- Target is a minimum; add important missing question types (common traps, "why is this wrong" questions, method and time-management questions).

## Files you write (only these)
1. `Book13_LogicalReasoning/Book13_PartNN.md` (mkdir -p):
```
# Book 13 — Logical Reasoning & Analytical Thinking | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
(inline data/options lines, if any)
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book13_PartNN_sources.md`.
3. `research/index_rows/B13PNN.md`: rows `| B13PNNQn | 13 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B6P07.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/A13_PartNN` (yours only). Do not commit or push.

## Final reply (short)
Files, actual count vs target, number of searches, which sources were blocked, how many questions are gap-fills, how many puzzles you brute-force-checked for uniqueness, anything uncertain.
