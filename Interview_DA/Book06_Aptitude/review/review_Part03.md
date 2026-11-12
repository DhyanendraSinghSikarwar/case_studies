# Review: Book 6 Part 3 (Time & Work, Time-Speed-Distance)

File reviewed and fixed in place: `Book06_Aptitude/Book06_Part03.md`. Scratch: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C06_Part03/` (`solve.py`, `edit.py`).

## Counts
- Answers checked: 65 of 65.
- Re-solved independently by code (exact fractions, brute force over integers, simulation of alternating cycles, root search for equations) before comparing: 58 numeric items plus all their follow-up variants and Check lines. The 7 concept items (Q2, Q24, Q25, Q33, Q37, Q58, Q64) were checked by hand and by their worked examples in code.
- Wrong final answers or option letters: 0. Wrong intermediate steps or follow-up numbers: 0.
- Answers edited: 26 (one wrong qualitative Check claim, one over-general claim, the rest wording, claims, missing assumptions, clarity and template gaps).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| 11 | Check said 48 is "closer to 40"; 48 is closer to 50 | Reworded: below the simple average 50 and pulled towards 40 |
| 11 | "LCM" and "harmonic mean" used without explanation | LCM defined at first use; one bullet explaining harmonic mean, pointing to Q24 |
| 24 | "Arithmetic mean is always larger" true only for equal distances | Added "For equal distances" |
| 3 | Confusing "mistake" wording about 3.6 | Rewritten plainly |
| 9 | "Inverse proportion" unexplained; equal-pace assumption unstated | Defined; assumption added |
| 13, 29 | "Asked at" implied prep-list support not in sources file | Reworded to what the sources support |
| 14 | "Asked at" credited Byju's with a "worker leaves" variant (its snippet lists efficiency, group work, work in a duration) | Now "standard variant (prep-site pattern, unverified)" |
| 48, 49, 55, 56, 61, 62, 63, 65 | "Asked at" said "listed in prep sources / standard in prep lists"; the sources file only gives these as judgement star patterns | Reworded to "N-star pattern in the sources file (judgement, not measured frequency)" |
| 16 | "Relative speed" not defined at first use | Defined in Explain simply |
| 17 | "Harmonic effect" jargon in Check; downstream/upstream not defined; no Fast method | Plain wording; terms defined; short Fast method line |
| 18 | ab/(b-a) shortcut gave no validity limit | Added "a = inlet hours, b = outlet hours, valid only when b > a" |
| 19, 20, 29, 35 | Missing Fast method where one exists | Added one-line fast methods (gap/sum, gap/difference, half the sum of pair rates, average and half-difference) |
| 23, 39, 41 | Unstated assumptions | Added (both work every day; equal productivity; equal rate per analyst-hour) |
| 37 | Excel formulas used placeholder names and were not flagged as unrun | Real range placeholders; labelled "not run in Excel here" |
| 63 | Awkward "B's partner C" wording | Rewritten ("while B runs 80 m, C runs 72 m") |
| 64 | Mini-example numbers looked like facts; Brooks's law unnamed | Labelled illustrative; named Brooks's law |

## Verified results (all matched the written answers)
Q1 20/3, Q11 48, Q14 24 (follow-up 21), Q26 28 2/3 so day 29 (B-first 29), Q28 u=5 d=11 (unique), Q29 8 (C alone 40), Q38 14 (13.2), Q46 72 (unique), Q47 9.6 (8), Q48 12 (B-first 12; 10 h/20 h case 13), Q49 70 (schedule 1.5 h; 30 km variant), Q54 75 (unique), Q55 A 24 / B 12, Q56 3:2 (t = 6 h; 16 h/25 h gives 5:4), Q57 x=8 (unique positive root), Q63 28 (56 in 200 m; B beats C by 8), Q65 5 (4 2/3 variant), and every other numeric answer and follow-up in the part.

## Shortcuts checked
Product over sum (two workers only), 5/18 and 3.6 conversion, harmonic mean (equal distances only), LCM units, inverse-ratio wage split (valid because all work the same days), successive/percentage speed-time rule x/(x+y), square-root meeting rule, d = s1 s2 / (s2 - s1) x gap. All valid for the stated cases; limits now stated where they were missing.

## Unresolved / report only
- Ordering: stars descend (3, 2, 1 stars) and numbering is continuous 1 to 65. Within the 3-star block Q26 to Q29 (red) follow green/yellow items; fine.
- Duplicates inside the part: Q3 and Q30 (km/h and m/s, two directions), Q1/Q2/Q25 (together-time formula and LCM), Q18/Q31/Q58 (outlet as negative rate), Q11/Q24/Q43/Q54/Q60 (average speed), Q12 and Q55 (subtract a rate).
- Overlap with other parts: Part02 Q47 and Part10 Q16 repeat the round-trip average speed (60 and 40 km/h); Part10 Q21 repeats Q44 (200 m train, 300 m bridge, 25 s). Not removed.
- Q26 answer "29 days" counts the day the work finishes; exact elapsed time 28 2/3 days is stated. Q10 trap "or 5.33 (direct proportion)" kept; "or 5" in the same line is a loose trap.
- Not every concept item has a Check line (Q2, Q24, Q33, Q58, Q64); acceptable for concept answers.

## Claims left unverified
All "Asked at" prep-site statements (Q1, Q2, Q3, Q5, Q6, Q7, Q11, Q15, Q16, Q17, Q18, Q22, Q25, Q27, Q31, Q33, Q40, Q43, Q44, Q45, Q47 and similar) are search-snippet level in `research/Book06_Part03_sources.md`, unverified, with no company-specific report found. Excel formulas in Q37 not run in Excel. Brooks's law attribution in Q64 is from general knowledge, no source checked.
