# Book 13 dedupe log

- Frozen question lists: 657 questions across 12 parts (targets total 640): P1 40, P2 73, P3 51, P4 74, P5 70, P6 60, P7 50, P8 62, P9 60, P10 54, P11 40 (four mock sets of 10), P12 23.
- Method: token-Jaccard on full question bodies within Book 13 (threshold 0.8) and against all 80 Book 6 Part 7 questions (threshold 0.65); every flagged pair was read in full.
- Result: no question removed. Flagged pairs are different puzzles built on the same template (same people names and seating or floor layout with different clue sets and a different asked person), different asks on the same prompt (for example socks: "two of the same colour" vs "two blue socks"), or new variants of a classic genre requested by the plan ("new variants only", for example ropes: 90 minutes here vs 45 minutes in Book 6 Part 7 Q74; inequalities and coded-relation items with different chains and codes).
- Known weakness, report-only: Part 4 uses templated names (Asha, Bala, Chitra, Dev...) across many seating and floor puzzles, so the list reads repetitive; each puzzle has its own clues and a unique solution verified by the part writer's solver. A later pass could vary names and wording.
- Book 6 Part 7 was read in full by every writer; none of its questions is repeated.
- Part 11 mock-set questions were written while Parts 4-10 were still being drafted, so overlap with those parts was not checked by the Part 11 writer; the scan above covers it (no duplicate found).
