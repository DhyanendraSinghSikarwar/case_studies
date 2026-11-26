# Review: Book 13 Part 4 (seating, floor, box, month and day arrangements)

Reviewer: Wave C. File edited in place: `Book13_Part04.md` (10 targeted edits, no heading, number, star, order or data-line change).

## Counts
- Answers checked: 74 (Q1 to Q74).
- Re-solved independently by code from the question text only (before reading the written answer): 59 puzzles and counting items: Q1-Q10, Q16-Q30, Q39-Q58, Q61-Q74 (puzzles by itertools brute force with an explicit convention; counting and date items by enumeration and Python datetime). Q11-Q15, Q31-Q38, Q59, Q60 are method or trap items: their numeric claims (Q13 counts 60/20/6, Q31 mini-example, Q33 table n=3 to 7, Q34 pair counts, Q35 examples, Q38 72/24, Q59 3600/3360/960/1200) were re-run.
- Written answers wrong: 0. Non-unique or zero-solution puzzles: 0 (every puzzle has exactly one arrangement; my first Q54 run showed 6 solutions, which was a bug in my own clue 3, fixed and rerun: 1 solution, E).
- Answers changed: 0. Reasoning or wording fixed: 10 items (table below).
- Follow-up and "drop a clue" claims re-run and confirmed: Q1 (4 arrangements, Asha or Bala on 5), Q2 (5), Q5 (2), Q8 (even-floor variant), Q10, Q16 (2 rows), Q18, Q19 (2), Q21 (3), Q22 (0), Q41 (only 1 of 8 order-and-seat cases), Q45 (reading clue 1 the other way gives none, clues 2-4 still Esha), Q47 (second circle, answer Esha), Q54 (reversed clue 3: 2 rows, answer F), Q71 (2027: August; 1 to 3 per year), Q73, Q74 (4 couples: 12).

## Conventions (checked, stated in the answers, applied consistently)
- Row facing north: right = east = higher seat number from the left end. Two rows: row 1 faces south (its right is west), row 2 faces north (its right is east); "faces" = same column.
- Circle facing the centre: right = anticlockwise, left = clockwise; facing outside: right = clockwise. "k-th to the right of Y" counted from Y's own facing. "Exactly k between" = gap k+1 (circle: stated per puzzle). "Opposite" on 8 seats = 4 apart. Q12 numbers seats anticlockwise, Q17 to Q67 clockwise; each answer states its own numbering, both consistent.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q4 | Follow-up 1 read "E... G is seat 1" (garbled) | Reworded cleanly |
| Q16 | Step 4 skipped the option B-A in seats 3-4 (it fails, F would need seat 1 or 5) | Added the case and its reason |
| Q21 | Step 1 said the other option Python = SQL - 2 was "tried only where it exists" but never tested it | Explained why it never fits |
| Q33 | "Explain simply" definition of distinct was unclear | Reworded |
| Q36 | Check claimed all puzzles in the book were brute-forced | Replaced by what this review actually re-solved |
| Q41 | Step 4 example omitted Bala's seat | Added Bala = seat 4 |
| Q11 | "north row on top (facing south)" ambiguous | Clarified: the row on the north side faces south |
| Q68 | Step 3 said p = 2 and p = 3 leave no legal place for Blue; false for p = 3 (Blue can sit at 2) | Gave the true reasons for p = 2 and p = 3 |
| Q70 | Step 4 option list missed F G B E (fails: A faces E at the end, no seat for C) | Added it to the list and the failing case |
| Q73 | Follow-up 1 ambiguous (A and B together, with or without the end rule) | Stated "instead, no end rule" |

## Template, honesty, style
- Template: all answers carry Asked at, interviewer check, Say this, Answer, steps, Fast method or Explain simply, Check, follow-ups, mistakes. Q11-Q15 and Q31-Q38 use the concept variant (no Fast method in some); acceptable.
- Asked-at lines match `research/Book13_Part04_sources.md` (prep-site, single-claim, unverified; no company-specific report). Q59 Excel formulas are labelled "from memory, not run here"; Q37 and Q60 suggestions are labelled "our suggestion"; Q71 follow-up 2 labelled from memory.
- No em or en dashes in answer text (title line only); 24 code-fence markers (balanced); no script text pasted.

## Report only
- Q26 question line ends with a full stop instead of a question mark ("...on the same day."); heading text left unchanged per rules.
- Q23, Q27-Q30, Q71-Q74: counting and date items have no Fast method gaps but are generic textbook problems; no near copy found. Source file says Book 6 Part 7 was checked; I did not re-open Book 6 Part 7 and make no new overlap claim. Counting items Q27-Q30, Q72-Q74 may overlap permutation items in other aptitude books (not checked).
- Q16 and Q56, Q54 follow-ups mix "Fast method" with long case lists; acceptable.
- Q12 numbers anticlockwise while Q6/Q17 etc. differ in numbering direction; flagged for a one-line note if the book wants a single convention.
- Header says Target 70, Actual 74: consistent with 74 headings.

## Unverified claims left
- All prep-site and company statements (TCS NQT, Infosys, Wipro, Cognizant, Accenture, Capgemini, Mu Sigma, FACE Prep 3 to 4 minutes per set, GeeksforGeeks formats) remain "reported, unverified"; no web access here.
- Excel formulas in Q59 were not run (no Excel here).
