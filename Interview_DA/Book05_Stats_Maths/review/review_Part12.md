# Review: Book 5 Part 12 (How to Develop Statistics & Maths Skills)

## Counts
- Answers checked: 25 of 25. Python snippets run: 8 of 8 reproduced pasted output (Q4, Q5, Q11, Q12, Q13, Q16, Q19, Q24); all prose numbers re-derived (Q1, Q8, Q9, Q14 dice, Q15, Q24).
- Answers fixed: 8 (Q10, Q13, Q15, Q16, Q18, Q20, Q21, Q6). Headings, numbers, stars, order untouched.

## Verification highlights
- Q4 simulation (seed 1): gap 0.09, share 0.0052. Q5 chi-square 8.62, p 0.0033 (with correction 0.0056). Q11 SD 4.12 (ddof=0 gives 3.69). Q12 Welch t 2.98, p 0.0109 (pooled t would be 0.0099). Q13 11.0 to 19.0. Q16 11.8 to 22.2. Q19 chi-square 21.65, p 3.28e-06. Q24 64.2%. Q15 36%. All match.
- No em dashes in answer text; code fences balanced.

## Fixes
| Q | Issue | Fix |
|---|---|---|
| Q6 | Resource names stated without a verification label | Added "from memory, unverified" |
| Q10 | Dataset facts labelled "general knowledge" | Relabelled "from memory, unverified" |
| Q13 | Called the assistant's 10% to 20% "too wide" (it is a rounded range, not wrong) | Softened wording |
| Q15 | Worked example said "calculated in Python" but no code shown | Added readable code and output (80 hits, 45 false alarms, 36%) |
| Q16 | "Asked at" claimed the sources file supports it as a communication test; it does not | Changed to commonly asked, no direct source |
| Q18 | Mini-projects (Section 7 requirement) only implied | Added 5 mini-project ideas |
| Q20 | Self-check tests described but no actual test | Added an 8-question closed-book test with verified answers and scoring |
| Q21 | Roadmap lacked a "job-ready" definition and pointers to resources/datasets | Added two bullets |

## Section 7 coverage
Roadmap (Q7, Q21), daily plan (Q9, Q21, Q23), free resources (Q6, Q17), datasets (Q10, Q19), mini-projects (Q18, Q19), self-check tests (Q20). All present.

## Unresolved / report only
- Ordering: fine. Overlap: Q9/Q21/Q23 (study routines) and Q5/Q19 (same chi-square pattern) overlap lightly; Q15 and Q24 both cover p-value misreading (cross-referenced). Not changed.
- Many answers (Q2, Q7, Q17, Q21, Q23, Q25) have no Worked example; judged not meaningful for planning questions.

## Claims left unverified
- Resource names (StatQuest, Khan Academy, OpenIntro, Kaggle Learn, Statology) and dataset facts (IBM HR about 1,470 rows, Titanic, Iris, Palmer Penguins, Gapminder) are from memory; no page was fetched (sources file: snippet-level only).
- "Asked at" lines are all "commonly asked"; no company-specific report exists in the sources.
- Self-check scoring bands and hour estimates are the author's rules of thumb, labelled as such.
