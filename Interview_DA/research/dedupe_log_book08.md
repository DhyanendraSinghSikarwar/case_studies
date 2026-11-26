# Cross-part duplicate resolution (Book 8, Wave A)

Method: token-overlap scan (Jaccard >= 0.55 on question headings) of all 641 Book 8 questions across and within the 9 parts, then manual judgement. One hit: B8P7Q13 "How do you say no, or not now, to a request without damaging your relationship with the requester?" duplicates B8P2Q21 (same question, stakeholder-handling angle owned by Part 2); removed from Part 7. Several near-templated questions (rate versus mix decompositions in Part 4, headcount reconciliations in Parts 1 and 3) differ in data and context and were kept.

| Removed (old ID) | Question | Kept copy (old ID) |
|---|---|---|
| B8P7Q13 | How do you say no, or not now, to a request without damaging your relationship with the requester? | B8P2Q21 |

Result: 640 questions (target 600 met). Part counts: P1 72, P2 79, P3 70, P4 80, P5 101, P6 92, P7 60, P8 62, P9 24.
Note for answer agents: question texts were written without computing answers; every inline-data question must be solved by code before the answer is written. Writers flagged: Part 8 Q25 duplicate-row wording should be checked (2,650 - 120 - 130 = 2,400); Part 4 Q12/Q28 share a data table (rate and mix decomposition); overlaps between Part 2 and Part 7 (triage, conflicting priorities, layoff exclusion), Part 2 and Part 3 (dashboard with everything on it, spreadsheet total differs) are by design with different angles.
