# Book 14 (Logical Thinking from Zero, for Future Data Scientists) — build and review summary

Built 2026-11-26 from the user's own chapter index (`research/book14_user_index.md`). 37 chapters in 6 parts, answer keys for every chapter (merged into Appendix C), and Appendices A, B, D, E, F. Reviewed the same day by 14 reviewers (12 for the chapter groups, 1 for Ch36, 1 for the appendices); per-reviewer reports in `review/review_*.md`.

## What was built
| Item | State |
|---|---|
| Chapters 1-37 (`Ch01.md`-`Ch37.md`, about 122,000 words) | Written to the user's template: self-check (3), concept, why-it-matters box, 5 solved examples, 2 real-life scenarios, practice questions, mistake log, 5-line recap. Ch35 (10 mixed cases) and Ch37 (error-log system) use adapted layouts. Ch36 holds the 8 mock tests |
| Practice items | 820 (Ch1-34, matching the user's table counts) + 10 mixed cases (50 sub-questions) + 120 mock questions + 15 error-log exercises |
| Answer keys (`answer_key/Ch<NN>_key.md`) | Full step-by-step reasoning for every question and self-check; merged in chapter order into `appendices/AppC_Answer_Key.md` (about 85,000 words) |
| Appendix A cheat sheet, B templates, D reading list, E study schedule (12-week plan plus the index's slower pace), F glossary (315 entries) | Written and reviewed |

## Review results
- Every practice question, solved example, scenario number and self-check was independently re-solved by code (brute force over arrangements, truth assignments and orders; Venn enumeration for syllogisms; calendar and clock items with Python's datetime and calendar). Verbal items (fallacy and bias naming, statement-assumption, course-of-action, analogies) rest on reasoning and are labelled so in the keys.
- No wrong final answers were found in any chapter. Fixes were: rewritten or re-timed puzzles that duplicated or lightly reworded Book 6 Part 7 and Book 13 questions or earlier Book 14 items (about 120 items in total, with keys updated), ambiguous conventions stated, missing definitions added, mislabelled checks corrected, unlabelled formulas marked "from memory, not run here", and cross-references pointed to the correct Book 13 parts.
- Specific real errors fixed: Ch18 worked example 3 check line (4 April is a Monday, not a Sunday), Ch19 key header (27 assignments, not 64), Ch27 Q11 ambiguity (segment heights), Ch22 Q19 contradictory statements, Ch37 Q5 classification, Ch12 and Ch11 key verification notes.
- Final automated checks: no em or en dashes in any chapter, key or appendix; code fences balanced; Appendix C has all 37 chapters; practice counts match the index in every chapter.

## Still unverified or judgement (labelled in the text)
- Reading-list titles, authors and descriptions (Appendix D) are from memory, unverified; no years, prices or effectiveness claims.
- Spreadsheet formulas (Ch4, Ch12, Ch37 and others) are labelled "from memory, not run here" unless run.
- Verbal items and open-ended practice (acceptance criteria stated in the keys for M6-Q10, Q11, Q13, M7-Q8, Q12) are judgement; Ch14 Q38 and Q39, and Ch36 M3-Q13 were not brute-forced; Ch29 Q19 assumes both timers start together.
- Timing, pace and study-plan advice (Ch36, Appendix E, the 12-week plan, the 3 to 4 days per chapter pace) is our suggestion, not research. No claims about learning effectiveness are made.
- Ch11, Ch14 and a few other chapters' alternative puzzle rules are reported in the individual reviews.

## Open items for a later pass (report-only)
- Chapter lengths vary from about 1,800 (Ch2) to about 5,100 words (Ch16); Ch16 is above the 4,500 guideline and was left because of its 30 questions and four diagrams.
- Some shared genres remain with Book 13 and Book 6 Part 7 (tie ranking, clock angles, knights and knaves, three-circle Venn) with different scenarios, numbers and structure; a later pass could vary them further.
- The plan table says "6 parts" for the chapters while the appendices follow the same six parts; AppA headings were aligned to the six parts.
- Ch35 has no self-check section (the user's index does not require one); Appendix E tells the reader to redo a case instead.
