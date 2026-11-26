# Appendix B: Truth Table and Venn Templates

How to use this appendix: copy a blank template into your notes, fill the empty columns by hand, then compare with the worked version next to it. Every filled table and every number in a worked example below was produced or checked by a short computer program, so you can trust them as a model answer.

Conventions used throughout: T means true, F means false. Rows start with all T and change the last column first (the standard order from Chapter 3). A blank cell is shown as an empty space for you to fill. Statements are written p, q, r.

---

## B1. Truth table templates

### B1.1 One variable (2 rows)

Blank, for one helper or output column of your own (for example NOT p):

| p | output |
|---|---|
| T |   |
| F |   |

### B1.2 Two variables (4 rows)

Blank, with three empty columns (write the formula you are testing in the header of each):

| p | q | helper | helper | output |
|---|---|---|---|---|
| T | T |   |   |   |
| T | F |   |   |   |
| F | T |   |   |   |
| F | F |   |   |   |

### B1.3 Three variables (8 rows)

Blank, with a helper column and an output column:

| p | q | r | helper | output |
|---|---|---|---|---|
| T | T | T |   |   |
| T | T | F |   |   |
| T | F | T |   |   |
| T | F | F |   |   |
| F | T | T |   |   |
| F | T | F |   |   |
| F | F | T |   |   |
| F | F | F |   |   |

Rule of thumb: n variables need 2 to the power n rows (1 variable: 2 rows, 2: 4, 3: 8, 4: 16). If your table has a different number of rows, you have missed or repeated a case.

### B1.4 Worked example: NOT, AND, OR together

Statement: p AND (NOT q), then p OR q, shown with helper columns.

| p | q | NOT q | p AND (NOT q) | p OR q |
|---|---|---|---|---|
| T | T | F | F | T |
| T | F | T | T | T |
| F | T | F | F | T |
| F | F | T | F | F |

Reading it: p AND (NOT q) is true only in row 2 (p true, q false). p OR q is false only in the last row, where both are false. OR in logic is inclusive, so row 1 (both true) is true.

### B1.5 Worked example: De Morgan check (two columns identical means equivalent)

| p | q | NOT (p AND q) | (NOT p) OR (NOT q) | NOT (p OR q) | (NOT p) AND (NOT q) |
|---|---|---|---|---|---|
| T | T | F | F | F | F |
| T | F | T | T | F | F |
| F | T | T | T | F | F |
| F | F | T | T | T | T |

Columns 3 and 4 match in every row, and so do columns 5 and 6, so both De Morgan laws hold.

### B1.6 Blank: conditional and biconditional

| p | q | p then q | q then p | p iff q |
|---|---|---|---|---|
| T | T |   |   |   |
| T | F |   |   |   |
| F | T |   |   |   |
| F | F |   |   |   |

### B1.7 Worked: conditional, converse, inverse, contrapositive, biconditional

| p | q | If p then q | Converse: if q then p | Inverse: if NOT p then NOT q | Contrapositive: if NOT q then NOT p | p if and only if q |
|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T |
| T | F | F | T | T | F | F |
| F | T | T | F | F | T | F |
| F | F | T | T | T | T | T |

What the table shows:

- Column 3 (original) and column 6 (contrapositive) are identical: they always mean the same.
- Column 4 (converse) and column 5 (inverse) are identical to each other, but differ from column 3 in rows 2 and 3.
- The biconditional (column 7) is true only when p and q have the same value. It equals "if p then q" AND "if q then p" (check: columns 3 and 4 are both T only in rows 1 and 4, exactly where column 7 is T).

### B1.8 Worked: three variables, p AND (q OR r)

| p | q | r | q OR r | p AND (q OR r) | (p AND q) OR (p AND r) |
|---|---|---|---|---|---|
| T | T | T | T | T | T |
| T | T | F | T | T | T |
| T | F | T | T | T | T |
| T | F | F | F | F | F |
| F | T | T | T | F | F |
| F | T | F | T | F | F |
| F | F | T | T | F | F |
| F | F | F | F | F | F |

The last two columns match in all 8 rows, which shows that AND spreads over OR (distribution).

---

## B2. Venn region tables and counting

### B2.1 Two sets: the 4 regions

Universe U (everyone in the study). Circles A and B. Fill the count column with the number of people in each region.

| Region | Meaning | Short name | Count |
|---|---|---|---|
| 1 | in A, not in B | only A | |
| 2 | in A and in B | both | |
| 3 | in B, not in A | only B | |
| 4 | in neither | neither | |

Check: region 1 + 2 + 3 + 4 = total in the universe.

Formulas (two sets):

- At least one = A + B - both
- Only A = A - both; Only B = B - both
- Neither = Total - at least one

Counting worksheet (two sets):

| Step | Write the number | Formula |
|---|---|---|
| Total in universe | | given |
| Size of A (whole circle) | | given |
| Size of B (whole circle) | | given |
| Both | | given or found |
| At least one | | A + B - both |
| Only A | | A - both |
| Only B | | B - both |
| Neither | | Total - at least one |
| Check | | only A + both + only B + neither = Total |

Worked example (illustrative): of 80 staff, 45 joined the Yoga club, 38 joined the Book club, and 15 joined both.

| Step | Value | Working |
|---|---|---|
| At least one club | 68 | 45 + 38 - 15 = 68 |
| Only Yoga | 30 | 45 - 15 = 30 |
| Only Book | 23 | 38 - 15 = 23 |
| Neither | 12 | 80 - 68 = 12 |
| Check | 80 | 30 + 15 + 23 + 12 = 80 |

### B2.2 Three sets: the 8 regions

Circles A, B, C inside the universe U. Fill the count column.

| Region | Meaning | Short name | Count |
|---|---|---|---|
| 1 | A only | A only | |
| 2 | B only | B only | |
| 3 | C only | C only | |
| 4 | A and B, not C | AB only | |
| 5 | A and C, not B | AC only | |
| 6 | B and C, not A | BC only | |
| 7 | A and B and C | all three | |
| 8 | outside all circles | none | |

Check: regions 1 to 8 add up to the total in the universe.

Formulas (three sets):

- At least one = A + B + C - (A and B) - (A and C) - (B and C) + (all three)
- Only A = A - (A and B) - (A and C) + (all three); same pattern for B and C
- AB only = (A and B) - (all three); same pattern for AC and BC
- Sum of the three circle totals S = (exactly one) + 2 x (exactly two) + 3 x (all three)
- None = Total - at least one

Counting worksheet (three sets), fill from the top down:

| Step | Write the number | Formula |
|---|---|---|
| Total in universe | | given |
| A, B, C (whole circles) | | given |
| A and B, A and C, B and C (pair totals, each includes the centre) | | given |
| All three | | given |
| At least one | | inclusion-exclusion formula above |
| None | | Total - at least one |
| Region 4, 5, 6 (exactly two) | | pair total - all three |
| Region 1, 2, 3 (exactly one) | | circle total - two pair totals involving it + all three |
| Check | | regions 1 to 8 add up to Total |

Worked example (illustrative): 120 employees. 52 attended Training (T), 47 attended Wellness (W), 40 attended Mentoring (M). 18 attended T and W, 15 attended T and M, 12 attended W and M, and 6 attended all three.

| Region | Name | Working | Count |
|---|---|---|---|
| 1 | T only | 52 - 18 - 15 + 6 | 25 |
| 2 | W only | 47 - 18 - 12 + 6 | 23 |
| 3 | M only | 40 - 15 - 12 + 6 | 19 |
| 4 | T and W only | 18 - 6 | 12 |
| 5 | T and M only | 15 - 6 | 9 |
| 6 | W and M only | 12 - 6 | 6 |
| 7 | all three | given | 6 |
| 8 | none | 120 - 100 | 20 |
| | At least one | 52 + 47 + 40 - 18 - 15 - 12 + 6 | 100 |
| | Check: regions 1 to 8 | 25 + 23 + 19 + 12 + 9 + 6 + 6 + 20 | 120 |

Second check with the S rule: S = 52 + 47 + 40 = 139. Exactly one = 67, exactly two = 27, all three = 6. Then 67 + 2 x 27 + 3 x 6 = 139, which equals S.

---

## B3. Syllogism checking grid

Method (Chapter 12): draw one circle per group, draw each statement, then try to break the conclusion with another legal drawing. A conclusion "follows" only if every legal drawing agrees. Convention: every named group has at least one member.

Blank grid (copy one row per conclusion):

| Statement 1 | Statement 2 | Drawing of statements (nest, apart, overlap, mark) | Conclusion to test | True in my first drawing? | True in every legal drawing? | Verdict (Follows / Possible / False) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Verdict rule: Follows if true in every legal drawing; False if false in every legal drawing; otherwise Possible (not certain).

Worked grid (all rows checked against every possible picture by computer):

| Statement 1 | Statement 2 | Conclusion to test | Verdict |
|---|---|---|---|
| All X are Y | All Y are Z | All X are Z | Follows |
| All X are Y | All Y are Z | Some Z are X | Follows (X has members, and they are inside Z) |
| Some X are Y | All Y are Z | Some X are Z | Follows |
| All X are Y | No Y are Z | No X are Z | Follows |
| Some X are Y | No Y are Z | Some X are not Z | Follows |
| All X are Y | Some Y are Z | Some X are Z | Possible (Z's overlap with Y may miss X) |
| Some X are Y | Some Y are Z | Some X are Z | Possible |
| All X are Y | All Z are Y | All X are Z | Possible |

Either-or check: if Conclusion I and Conclusion II are a statement and its negation (for example "All counters are open" and "Some counters are not open"), and neither follows alone, then "either I or II" follows.

---

## B4. Seating and ordering grid

### B4.1 Straight row (positions 1 to n)

State the convention first: all people face the same way (say, north), so each person's left is the viewer's left when the viewer also faces north. Number the positions from the left end.

| Position | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Person | | | | | |
| Clue used | | | | | |

Useful facts: position from left + position from right = n + 1 (n people). People between positions a and b (a smaller) = b - a - 1. If two rows face each other, the left of one row is the right of the other.

### B4.2 Circle (n seats)

Number the seats 1 to n going clockwise. Write which way people face.

| Seat (clockwise) | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Person | | | | | | |
| Faces centre or outside? | | | | | | |

Conventions (checked by code):

- Facing the centre: your left neighbour is the next seat clockwise; your right neighbour is the next seat anticlockwise.
- Facing outside: it is reversed. Your left neighbour is the next seat anticlockwise; your right neighbour is the next seat clockwise.
- In a circle of n seats (n even), the person opposite seat k is seat k + n/2 (wrap around after n).
- Distinct circular arrangements of n people (only relative positions matter) = (n - 1) factorial.

### B4.3 Order-chain worksheet

Write each clue as a link and join them:

| Clue | Link (use > for "is higher/taller/earlier than") |
|---|---|
| | |
| | |
| Joined chain | |

---

## B5. Constraint table for who-owns-what puzzles

Rules: put a tick for yes, a cross for no. One tick per row and per column within each pair of categories. After every tick, cross the rest of its row and column. A negative clue is a cross. When a row has only one open cell, tick it.

Blank (3 people, 3 items):

| | Item 1 | Item 2 | Item 3 |
|---|---|---|---|
| Person 1 | | | |
| Person 2 | | | |
| Person 3 | | | |

Blank (3 people, two other categories; also fill the link between the two other categories):

| | Dept 1 | Dept 2 | Dept 3 | City 1 | City 2 | City 3 |
|---|---|---|---|---|---|---|
| Person 1 | | | | | | |
| Person 2 | | | | | | |
| Person 3 | | | | | | |
| Dept 1 | | | | | | |
| Dept 2 | | | | | | |
| Dept 3 | | | | | | |

Worked example (illustrative). Asha, Bilal and Chen each own exactly one of a cat, a dog and a fish. Clue 1: Asha does not own the dog. Clue 2: Bilal owns neither the cat nor the dog. (A program tried all 6 ways to give out the pets; exactly one fits both clues.)

After the clues (X means no):

| | Cat | Dog | Fish |
|---|---|---|---|
| Asha | | X | |
| Bilal | X | X | |
| Chen | | | |

Bilal's row has only one open cell, so Bilal owns the fish. Cross the rest of the fish column:

| | Cat | Dog | Fish |
|---|---|---|---|
| Asha | | X | X |
| Bilal | X | X | tick |
| Chen | | | X |

Asha's row now has only the cat open, so Asha owns the cat. That leaves the dog for Chen.

| | Cat | Dog | Fish |
|---|---|---|---|
| Asha | tick | X | X |
| Bilal | X | X | tick |
| Chen | X | tick | X |

Final check against the clues: Asha (cat) does not own the dog, so clue 1 holds. Bilal (fish) owns neither the cat nor the dog, so clue 2 holds.
