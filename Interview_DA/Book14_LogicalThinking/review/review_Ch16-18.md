# Review: Book 14 Chapters 16, 17, 18 (chapters and answer keys)

Scratch: /tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C14_Ch16-18 (scripts c16*.py, c17.py, c18*.py).
Method: every item solved by Python brute force (all permutations, rule-family search, date library, schedule search over all orders and worker assignments) before comparing with the written answer.

## Counts
| Chapter | Practice re-solved / total | Examples, scenarios, self-checks re-solved | Wrong answers found | Items changed |
|---|---|---|---|---|
| Ch16 Seating | 30 / 30 (count matches index) | 5/5, 2/2, 3/3 | 0 | 1 (Q29, overlap) |
| Ch17 Coding | 40 / 40 (count matches index) | 5/5, 2/2, 3/3 | 0 | 2 (minor) |
| Ch18 Puzzles | 25 / 25 (count matches index) | 5/5, 2/2, 3/3 | 0 | 1 (Q21, overlap) |

All answers in the three chapters and keys matched my independent solutions. Every puzzle was unique by brute force, except Ch17 Q38, which is deliberately ambiguous (grade/band) and says so.

## Known issues checked
- Ch16 Q12 "Silas at the east end": tested. Clue 5 says west end; the east reading gives 0 arrangements (Quentin is at the east end), the west reading gives exactly 1. Key answer 2 is correct. Added one sentence to the key.
- Ch16 Q9: key answer Yara matches (north person faces south, so right = west = Zoe, left = east = Yara).
- Ch18 key (different author): all 25 answers, all reasoning chains and the schedule/calendar claims re-verified; correct. Its stale "Notes" section (claimed example 3's check line said Sunday) was removed because Ch18.md already reads "Monday" correctly.

## Fixes
| Chapter | Item | Problem | Fix |
|---|---|---|---|
| Ch16 | Q29 and key | Overlap: counting "two people next / not next" in a row of 5 and a circle of 5 is the same structure as Book13 Part 4 Q27, Q28, Q30 with changed numbers | Rewrote: (a) six in a row, three must sit together (144); (b) six round a table, two directly opposite (24). Both recounted by code; key rewritten. Count and order unchanged |
| Ch16 | Q12 key | Alternative reading never documented | Added a sentence explaining why east-end reading is impossible |
| Ch17 | Concept table, constant-shift example | "CAT becomes ECV" is the exact stem of Book13 Part 6 Q7 | Changed to "DOG becomes FQI" (checked) |
| Ch17 | Q23 | Open-ended number rule; many curves fit four points | Added hint "one multiplication and one addition"; key's search (quadratics, only n squared + 1 fits) re-run and confirmed, answer 82 |
| Ch18 | Q21 and key | Inverse of Book13 Part 4 Q71 (Friday 13th in 2026 gives exactly Feb, Mar, Nov) with the same year type | Changed to "August is the only month with a Friday 13th" (non-leap). Unique by code: 1 Jan is Friday, 25 Dec is Saturday. Key rewritten with the offsets table |
| Ch18 | Key footer | Stale note about example 3 | Removed |

## Overlap results
- Grepped Book13 Parts 3 to 7 and Book06 Part07 for queue, seating, floor, box, Friday-13th, critical-path, coding and sentence-code items. After the fixes no practice question or example copies or rewords an existing one.
- Left in place, judged different enough: sentence-code questions (same method as Book13 Q36/Q37 and Book06 Q26 but different words and codes), Ch18 Q15/Q22 schedules (Book13 Part 5 Q36 uses other tasks and numbers), Ch18 Q12 box labels (Book06 Q76 is a different puzzle).
- Duplicates within Book 14: grepped the Ch16 names (Silas, Pilar, Hanne, Kemal, Odile, Dorit) in other chapters: none. Ch18 Q9/Q10/Q19 reuse the same six department names with different clues (intended, different puzzles).

## Other checks (all pass)
- Template: self-check (3), concept, why-it-matters box, exactly 5 examples, exactly 2 scenarios labelled illustrative, no answers in chapter files, mistake log of 5, recap of exactly 5 lines, spreadsheet pointer. Practice order easy, medium, hard with tags (Ch16 Q1-10 / Q11-22 / Q23-30; Ch17 Q1-14 / Q15-30 / Q31-40; Ch18 Q1-8 / Q9-18 / Q19-25). Keys have every self-check and practice item.
- No em or en dashes; code fences balanced; blank line after every table.
- Conventions (facing, left/right, opposite, queue front) stated in Ch16 concept and before the practice set; the two-row and outward-facing items follow them (verified by code).
- Scenario numbers recomputed: Ch16 sc.1 (8 plans, then 4, then Plan D), sc.2 (32 and 20 minutes); Ch17 sc.2 (5 valid, 3 invalid, 37.5%); Ch18 sc.1 (60 / 50 / 50 minutes), sc.2 (payday 28th, April 2023 example).
- Word counts: Ch16 about 5,100 (over 4,500, justified by 30 questions and four diagrams; not trimmed), Ch17 about 3,600, Ch18 about 4,400.
- Cross-references: Book 13 Part 4 (seating), Part 6 (coding) exist and cover the topics; Ch18 refers to Book 13 generally and Chapter 36 (exists).

## Unresolved / unverified
- Ch17 Q38 is intentionally non-unique for "grade" (teaches "cannot be determined"); kept.
- Spreadsheet/SQL pointers contain no formulas, so nothing needed running. No external claims or statistics are made in these chapters.
