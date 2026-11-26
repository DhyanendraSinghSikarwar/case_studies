# Wave C instructions — Book 13 (Logical Reasoning & Analytical Thinking for Data Analysts) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 13 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10, Book 13 section), `style_guide.md` (Sections 10, 11), `research/wave_b_instructions_book13.md`. Environment: Python 3 (itertools, fractions, math, numpy, pandas, scipy, sqlite3). No web access.

## Scope and edit rules
- Edit ONLY your assigned `Book13_LogicalReasoning/Book13_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book13_LogicalReasoning/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars, order, nor a question's option or data lines. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/C13_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Independent solution by execution (mandatory, FIRST):** for EVERY question, before you read the written answer, solve it yourself in code from the question text and its option or data lines only: brute-force puzzles (itertools.permutations, constraint enumeration), enumerate Venn regions or small models for syllogisms and conclusions, evaluate truth tables, run SQL on sqlite3, trace pseudocode, recompute numbers and series. Then compare with the written answer. Check UNIQUENESS: if a puzzle has zero or several consistent solutions, or the stated answer is not forced, fix the answer (state the problem and the sensible reading) and list it. The writers' "verified by script / brute force" claims were not always true: do not trust them.
2. **Reasoning quality:** step-by-step reasoning is correct, in a valid deduction order a beginner can follow, and reaches the stated answer; every wrong MCQ option has a correct reason for failing; the "Fast method" really works and is not a coincidence; the "Check" line is true; the "Likely follow-ups" variants give the stated results (re-run them).
3. **Conventions and definitions:** the convention used (every named group non-empty; "some" = at least one; clockwise or anticlockwise; "rank from the top"; whether a row faces north) is stated and applied consistently; series and analogy items state the rule and show it fits every term; if a second defensible rule exists, it is stated.
4. **Honesty:** prep-site facts, test formats, timings, counts and pass rates are "reported, unverified"; "Asked at" claims only what `research/Book13_PartNN_sources.md` or `research/interview_processes.md` supports, otherwise "commonly asked (no company-specific report found)"; Excel or other-database behaviour that cannot be run here is labelled "from memory, unverified"; no effectiveness claims, no invented company or statistic; suggestions (time splits, plans) are labelled "our suggestion". Part 12 resources: "from memory, unverified, check the link and whether still free".
5. **Beginner clarity:** a non-technical HR reader can follow every step; every term, convention and shortcut explained at first use; sounds like a confident analyst. Fix jargon without padding.
6. **Template completeness:** header lines (Asked at, interviewer check, Say this), Answer, Step-by-step (or the concept variant), Fast method where useful, Check, Explain simply, Likely follow-ups, Common mistakes. Part 11 answers also carry "Target time" and "If you are short of time". Add anything missing.
7. **Ordering/numbering:** report only. **Duplicates/overlap** with Book 6 Part 7 (80 reasoning items) or other parts and books: report only; flag any item that is a near copy of a Book 6 Part 7 question.
8. **Style/markdown:** no em dashes or en dashes in answer text (part-title line may keep one); balanced code fences; blank line after tables; no verification scripts pasted into answers (SQL blocks with real sqlite3 output for Part 9 are fine).

## Known flags from the answer wave
- Part 12 Q12 says Parts 2-10 hold 540 questions but the part files hold 554: keep the heading, make the answer consistent and explicit about both counts.
- Part 11 Q4: relation direction is ambiguous; the answer must state its reading.
- Part 12 practice-datasets coverage (style_guide Section 7) is only partly covered by Q1-14: check Q15-23 and add a short practice-sets/data section inside an existing answer if still missing.

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, questions independently re-solved by code, answers wrong, non-unique or changed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
