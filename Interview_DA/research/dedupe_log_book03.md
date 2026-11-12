# Cross-part duplicate resolution (Book 3, Wave A)

Method: token-overlap scan (Jaccard >= 0.6) of all 681 Book 3 questions within the book and against every question already in `question_index.md` (Books 0-2, 4, 5). Exact or near-identical questions were removed from one part, keeping the copy in the part that owns the topic (Part 10 owns coding-logic puzzles, Part 4 owns pandas read/write, Part 1 owns language basics). Kept on purpose: the Part 12 learning-journey questions (same template as Books 1, 2, 4, 5, tool-specific), Python/pandas tasks that mirror a SQL or Excel question in Books 1 and 2 (different tool, the book's stated "pandas equivalent" pairing), P1Q1/P1Q18 (false positive), P1Q38 vs P5Q81 (list vs per-department), P5Q5/P5Q8 (merge vs join vs concat), P10Q7/Q19 (prime vs Armstrong). Old IDs are pre-removal numbers.

| Removed (old ID) | Question | Kept copy (old ID) |
|---|---|---|
| B3P1Q16 | Write code to find the largest number in a list without using max(). | B3P10Q5 |
| B3P1Q53 | How do you flatten a nested list such as [[1,2],[3,4]] into [1,2,3,4]? | B3P10Q61 |
| B3P1Q63 | How do you swap two variables in Python without a temporary variable? | B3P10Q21 |
| B3P2Q27 | What does the UnicodeDecodeError mean when reading a CSV, and how do you fix it with the encoding argument? | B3P4Q46 |
| B3P10Q35 | What is the difference between == and is in Python? | B3P1Q18 |
| B3P10Q36 | What is the difference between append() and extend() on a list? | B3P1Q17 |
| B3P10Q38 | What do break, continue and pass do inside a loop? | B3P1Q34 |
| B3P11Q2 | How do you read an Excel file into a pandas DataFrame, and how do you read one specific sheet? | B3P4Q2 |
| B3P11Q3 | How do you save a DataFrame to an Excel file without writing the index column? | B3P4Q28 |
