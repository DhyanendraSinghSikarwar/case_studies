# Review: Book 8 Part 01 (Data quality scenarios)

Reviewer: Wave C. File: `Book08_Scenarios/Book08_Part01.md`. Scratch script: `C08_Part01/v.py`.

## Counts
- Answers checked: 72 (all headings, stars and order untouched).
- Answers with numbers recomputed by code (written from the question data, then compared): 33 (Q1, Q3, Q4, Q8, Q11, Q12, Q13, Q17, Q18, Q19, Q23, Q24, Q27, Q28, Q29, Q34, Q35, Q36, Q37, Q38, Q39, Q46, Q50, Q51, Q54, Q56, Q59, Q60, Q65, Q66, Q68, Q70 range check by hand, Q72 illustrative only).
- Answers with a wrong figure: 1 (Q28). Answers changed in total: 8 (1 arithmetic, 1 technical accuracy, 6 honesty/clarity).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q28 | Trap line said the simple average of the three department rates is 6.7%. Code: (5+20+5)/3 = 10%. | Corrected to 10%, and added the true overall rate 12.5%. |
| Q50 | Check 1 implied a 12-digit ID loses digits just by opening in Excel. Excel keeps about 15 digits, so only the display changes until the file is saved as CSV (which writes the shortened value) or IDs exceed about 15 digits. | Rewrote check 1 to separate display-only from lost digits; labelled the 15-digit limit "from memory, unverified". |
| Q17 | Stakeholder script stated four days "appear to be weekend or holiday work" before confirmation. | Reworded as "may be ... I am checking". |
| Q51 | "I ran this check on them" (script claim voiced in interview). | Reworded to plain statement; code confirmed all three become 9876543210 and pass. |
| Q1 | Accuracy example (5,20,000 vs 52,000 a month) was ambiguous (monthly or annual). | Stated it is a monthly salary field with an extra zero. |
| Q10 | Invented attrition figures (14%, 13% to 15%, 5%) not labelled. | Added "(illustrative figures)". |
| Q58 | "22% of senior employees" is an invented figure, unlabelled. | Added "(illustrative figure)". |
| Q72 | Tenure 3.4 to 3.7 years was not labelled illustrative (only 63 was). | Labelled all figures illustrative. |
| Q68 | Maternity leave example was muddled ("a field where the rule does not apply"). | Replaced with "Notice-period end date for someone who has not resigned". |

## Verified correct without change (by code)
Q3 (1,200 unique; 50 extra; 4.17% of unique, 4.0% of rows), Q4 (7%), Q8 (400 = 8.0% of dashboard, 8.7% of CRM), Q11 (23.75x), Q12 (900, 9.0%), Q13 (42,000; 3.51% of Finance; 3.39% of dashboard), Q17 (18.2%), Q18 (42, 25, 17; 0.81% of payroll, 0.80% of HRIS), Q19 (157), Q23 (75 and 100), Q24 (01:30 IST 1 April), Q27 (mean 60, SD factor 0.893, sensitivity 56 and 64), Q29 (76.5%; 3.5 points; 4.6% relative), Q34 (3 of 4 fail), Q35 (Rs 9,36,000), Q36 (91.2%), Q37 (53.33 vs 50, +6.7%; median 55 vs 50; +20% headcount), Q38 (7.5%, 10%, 1.33), Q39 (94%; 700 to 850 complete), Q54 (28), Q56 (84.4%, 15.6%), Q59 (24 h; 45x), Q60 (1,200; 600; 541 to 659; with finite-population correction 552 to 648), Q65 (98.0%, 99.5%).
Premise checks: Q8, Q13, Q18 correctly diagnose definition/timing first; Q29 correctly counts people not submissions; Q39 correctly gives a range, not a point; Q60 correctly separates precision from recall; Q48 and Q59 premises diagnosed correctly.

## Other checks
- Honesty: no real statistic or law stated as fact; legal items (PAN-style IDs, government ID, gender data, location data, pay confidentiality) defer to HR/legal or the data owner. Q54 is clearly a template ("say it only if true"). "Asked at" lines all say "commonly asked (no company-specific report found)" with prep-site claims marked unverified; consistent with the sources file (Meesho/Swiggy mentions are snippet-level and marked unverified).
- Style: no em dashes in answer text (only the part-title line); no code fences; no tables; no pasted scripts; 72 headings present.
- Template: every answer has Asked at, interviewer check, Say this, structure block, Likely follow-ups, Common mistakes.

## Unresolved / report only
- Ordering: Q9/Q10 are marked 🟡 under the 3-star block and Q19 🔴 sits in the same block; order follows 🟢, 🟡, 🔴 correctly. Q63 (⭐ 🟢) precedes Q64 (⭐ 🟡): fine. No ordering fault found.
- Overlap: Q4/Q7/Q14/Q28/Q58/Q68/Q71 all touch missing data (distinct angles); Q12/Q44 (join fan-out) are near-duplicates; Q25/Q50 (Excel ID damage) overlap; Q9/Q62 and Q52/Q53 overlap in communication. Q2 and Q41 overlap (profiling checks). Overlap with other Book 8 parts and other books (Book 2 SQL join pitfalls, Book 3/Book 5 missing data) not checked here.
- Minor style: several answers have a blank line before "First, clarify" or "Likely follow-ups" (harmless in markdown). Q26 mixes LOWER and UPPER in steps 2 and 3 (left as is).
- Q59 "1,440 is exactly 24 hours so likely a default" is reasonable judgement, not proven; the answer already says so.

## Left unverified
All real-world facts remain "from memory, unverified" or deferred: Excel 15-digit limit, Indian mobile numbers starting 6 to 9, Little's test, dbt/Great Expectations features, heaping at 1 January dates, USD/INR rough ratio of 80 (marked assumption).
