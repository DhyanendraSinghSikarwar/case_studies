# Cross-part duplicate resolution (Book 9, Wave A)

Method: token-overlap scan (Jaccard >= 0.55 on question headings) of all 643 Book 9 questions across and within the 12 parts, then manual judgement. Two true duplicates removed; the rest (three "Name three ways ML is used in X" questions with different domains, three "what is wrong with this code" questions with different code, AI vs ML vs GenAI in Part 9 against the AI/ML/deep learning/data science difference in Part 1) differ in angle or content and were kept.

| Removed (old ID) | Question | Kept copy (old ID) |
|---|---|---|
| B9P6Q30 | What is regularisation (Ridge and Lasso) in intuitive terms, and how does it help against overfitting? | B9P2Q43 |
| B9P2Q32 | What does it mean to train or fit a model, and what is the difference between a parameter and a hyperparameter? | B9P1Q9 |

Result: 641 questions (target 600 met). Part counts: P1 77, P2 84, P3 43, P4 66, P5 87, P6 39, P7 45, P8 33, P9 100, P10 22, P11 21, P12 24.
Note for answer agents: question texts were written without running code or computing figures; every inline-data question and every code snippet must be run (sklearn 1.9.1, statsmodels 0.15.0, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1) before the answer is written, and outputs pasted from real runs. Version-specific API claims (for example root_mean_squared_error, removed squared=False) must be checked by running. Overlaps by design: Part 1 base-rate/baseline and column-exclusion ideas with Parts 5 and 6; Part 9 RAG and tokens/temperature items with Part 10; regression interpretation with Book 5 Part 7 (here the ML/sklearn angle).
