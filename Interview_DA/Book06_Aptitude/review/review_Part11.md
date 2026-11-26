# Review of Book 6 Part 11 (Wave C)

Scratch: /tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C06_Part11 (t.py)

## Counts
- Answers checked: 33 of 33
- Re-solved or re-run by code: 17 (all SQL items Q6, Q7, Q8, Q13, Q14, Q19, Q20, Q27 on sqlite3 3.53.1; Q26 loop sums; Q33 brute force over all 1,024 targets plus a 1,000,000 sample; word counts for Q12, Q15, Q25, Q31; weekday check for Q12 dates). The other 16 are grammar, vocabulary, reading and CS-concept items checked by rule, not by code.
- Answers with wrong content changed: 2 (Q6 printed output not reproducible, Q12 word count wrong); Q15 had a wrong claim and was corrected. Also 5 claim or completeness edits.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q6 | Second sample output (HR 2, Sales 3) could not be reproduced: sample salaries were never given | Added the 8 sample rows (Sales 30,40,50; HR 30,50; Ops 10,20,25); output re-run and matches; added the sqlite3 error for `WHERE COUNT(*)` |
| Q6 | Asked-at overstated ("candidate reports ... analyst online tests") | Reworded to what interview_processes.md supports; says the exact item is not a reported question |
| Q7 | Check block did not say dept 1 and row 1 must exist first | Added setup note; all five outcomes confirmed |
| Q12 | Body said 104 words; actual count is 100; "verified by script" gave no number | Corrected to 100 (greeting and signature excluded); dates verified (13 Nov 2026 Friday, 17 Nov Tuesday) |
| Q13 | Asked-at said a joins item is in a LeetCode 2026 report; source only says a three-table join item, and INNER vs LEFT is from a Glassdoor snippet | Reworded to both sources, marked unverified |
| Q15 | Claimed the model script is about 135 words / 60 s; it is 92 words (about 40 s) | Corrected, labelled 130-150 words per minute as rule of thumb, advised adding a proof example |
| Q18 | Missing Fast method and Check; step 4 about "were/was" was muddled | Added both; rewrote step 4 |
| Q22 | Asked-at implied Pearson's guide reports repeat-sentence tasks; sources file only lists Versant sections | Reworded; TalkDrill only, unverified |

## Verified correct, unchanged
Q1 to Q5, Q8 to Q11, Q13 answer, Q14, Q16, Q17, Q19 to Q21, Q23 to Q33. Q8: 5, 3, 2000.0 and 1200 confirmed. Q13: inner 2 rows, left 3, full 4 (needs SQLite 3.39 or later), right join follow-up confirmed. Q14: `= NULL` returns nothing, `IS NULL` returns Ravi and Kiran, `<> 101` returns only Meena (follow-up confirmed). Q19: join returns the 3 original rows. Q20: rollback of DELETE gives 2 then 3; DROP TABLE inside a transaction is also rolled back in SQLite (confirmed, already noted); error text matches. Q26: 18, follow-ups 15 and 63. Q27: CHECK failure text and totals match. Q31: summary is 19 words, shortened version 15. Q33: maximum 11 comparisons for 1,024 elements; 1,000,000 gives 20.

## Unresolved / judgement
- Q5: "the report" vs "a report" is context dependent; the answer already states the assumption.
- Q2, Q11, Q24, Q30: single best answers rest on usage judgement (singular "their" accepted, etc.); noted in answers.
- Q20 and Q7 contain dialect-specific claims (TRUNCATE rollback, SQL Server one-NULL unique rule) from general knowledge, not run (only SQLite was available); labelled by database in the text.
- Q22, Q29, Q32: no code check possible; rely on general knowledge.
- Ordering and numbering: stars descend 3, 2, 1 across Q1-Q33 but the part header says target 30 and actual 33; fine, no action. Overlap with other parts: Q6, Q8, Q13, Q14 (core SQL) may overlap with SQL books; not checked across parts.

## Claims left unverified
All "Asked at" format claims about Accenture communication assessment, Versant, Tiger Analytics CS MCQs (prep sites and one institutional note; sources conflict). Timing guidance in Q15 is a rule of thumb. No em dashes in answers; code fences balanced (22).
