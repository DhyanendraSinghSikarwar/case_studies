# Cross-part duplicate resolution (Book 6, Wave A)

Method: token-overlap scan (Jaccard >= 0.5 on question headings, >= 0.6 on heading plus data) of all 729 Book 6 questions across and within the 11 parts, then manual judgement. Most hits are aptitude problems with the same template but different numbers or data (for example Part 3 work problems, Part 4 interest problems, Part 8 questions that share one data table); these are distinct practice problems and were kept. Removed only exact or name-swapped copies in Part 10 mock sets whose topic part already holds the same problem, keeping the copy in the part that owns the topic.

| Removed (old ID) | Question | Kept copy (old ID) |
|---|---|---|
| B6P10Q13 | Using the successive-discount shortcut, single discount for 20% and 10%? | B6P1Q13 |
| B6P10Q17 | Using the factor 5/18, convert 54 km/h to m/s and find the time for a 150 m train to cross a pole | B6P3Q6 |
| B6P10Q30 | Mock Set C Q1: man who is the son of my mother's only brother (name swapped) | B6P7Q1 |
| B6P10Q31 | Using a 10% + 10% + 1% idea, compound interest on Rs 10,000 at 10% for 2 years | B6P4Q3 |
| B6P10Q33 | Using cyclicity of unit digits, unit digit of 7^45 | B6P5Q14 |

Result: 729 questions before, 724 after (Part 10: 68 to 63). Target 600 met. Part counts: P1 82, P2 67, P3 65, P4 52, P5 70, P6 69, P7 80, P8 94, P9 49, P10 63, P11 33.
Kept on purpose: P6Q16/Q27 (digit problems with and without zero), P8Q67/Q68 (different products), P1Q13/Q43 (two vs three successive discounts), P10 mock questions with different numbers from their topic-part twins.
Note for answer agents: question text was written without computing answers; every numeric answer must be solved and verified by code before it is written.
