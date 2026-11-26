# Review: Book 13 Part 12 (How to Develop Logical Reasoning)

Reviewer: Wave C. Scratch script: /tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/C13_Part12/s.py

## Counts
- Answers checked: 23. Questions with checkable content independently re-solved by code before reading answers: 11 (Q4, Q6, Q10, Q11, Q12, Q13, Q14, Q17, Q18, Q19, Q23 arithmetic and examples). Q16 example sums checked by hand. The other 12 are template, advice or judgement answers with nothing to execute.
- Answers wrong: 0 factual errors in computed values. Non-unique puzzles: 0 (Q11 has exactly 1 of 24 orders; Q17 has exactly 1 of 6; Q11 follow-up with the clue dropped gives 2, as stated).
- Answers changed: 3 (Q12, Q14, Q9) plus the part scope line and one Q18 follow-up.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Scope line | said "remaining 540 practice questions" | now states 554 in current files vs 540 in the question and plan |
| Q12 | 540 vs 554 mismatch only mentioned in the Check line | Answer, Say-this, steps, Check and follow-up now give both: 540 gives 36 days, 6 weeks, 45 min, drop 180; 554 gives 37 days, 7 calendar weeks, 45 min, drop 194. Part counts 73+51+74+70+60+50+62+60+54=554 re-tallied by grep and sum. Heading unchanged |
| Q18 | follow-up said "all 540 practice questions" | changed to 554 |
| Q9 | style_guide Section 7 "practice datasets / practice sets" only partly covered | added a table of ready-made sets (Parts 2-10 counts, Part 11 = 40, Book 6 Part 7 = 80) and the small invented datasets (Q14 table, Q10 log, 20-row HR table for Q13) inside the answer |
| Q14 | Excel formula used "Yes" text while SQL uses 1/0; blank behaviour not explained | added one sentence on the text coding and that a blank notice cell counts as not on notice (still from memory, not run) |

## Section 7 coverage
Roadmap Q3, daily plan Q4, free resources Q5 and Q20, practice sets and datasets Q9 (added), mini-projects Q10, Q11, Q13, Q14, self-check tests Q8, Q18, Q23. All present.

## Re-run results (all match the written answers)
Q4 30, 60, 270 min. Q6 55/65/75/80 percent, 108/96/90/78 s; Week 3 first meets both. Q10 pivot rows total 8. Q11 B,C,A,D unique. Q14 sqlite3 plain/blank-safe output identical to the table (only Gita differs). Q13 10% of 200 = 20 and 20% of 300 = 60 people left (not stated in the answer). Q18 2+1+2+1+2+1+1+1+1 = 12. Q19 20-hour splits sum to 20 each. Q23 example 85%, 75%, 84 s.

## Unresolved / notes
- Q6 "which target was harder" is a judgement (both met in Week 3); the answer labels it as such.
- Q12 asks for 540 while the book holds 554; the question text could not be changed.
- Overlap: Q11 and Q17 mini puzzles are tiny seating items; no near copy of a Book 6 Part 7 question was detected by title check (not a full text comparison).
- Em dashes: none in answer text (only part-title line). Code fences balanced (3 blocks).

## Claims left unverified
Puzzle Baron, Daydream Puzzles, GPuzzles, IndiaBix, GeeksforGeeks, Khan Academy, folj.com (labelled from memory, unverified, check link and whether still free); PMC4569435 study (snippet only); Mu Sigma/Fractal formats (prep-site reports); Excel behaviour in Q14 (not run here); all plan durations and pass marks are labelled "our suggestion".
