# Review: Appendices A, B, D, E, F (Book 14)

Scope: AppA_Cheat_Sheet, AppB_Templates, AppD_Reading_List, AppE_Study_Schedule, AppF_Glossary. Scratch: scratchpad/C14_Appendices (v1.py, v2.py). Targeted edits only; nothing committed.

## Verified by code (all correct as written)
- AppA A3/A4/A5/A6: truth tables, De Morgan, distribution, converse/inverse/contrapositive, iff, "unless" = OR, negation of "if", all 9 argument-shape verdicts.
- A7/B2: two and three set formulas, exactly-two = pair sum - 3 x all, S rule (2000 random region sets); Yoga/Book (68, 30, 23, 12) and Training/Wellness/Mentoring (100, 25, 23, 19, 12, 9, 6, 6, 20; S = 139) worked examples.
- A11/B3: syllogism table and worked grid re-derived over all models with non-empty groups (160 pictures for the two-"Some" case); every Follows/Possible verdict correct.
- A12 triples, A14 ranking and tie formulas, A15 opposite seat and (n-1)!, A18 clock (overlaps M = 60H/11; 11/11/22 per 12 hours), leap rule, odd days (100/200/300/400 years = 5/3/1/0), month odd days, weekday shift next year.
- B1 tables (all 8 blocks) and B5 pets puzzle (exactly one solution of 6).
- Cross-check by grep against Ch 3-7, 9, 12-15, 17, 18, 20-25, 27-29: names, wordings and conventions agree.

## Fixes
| File | Item | Problem | Fix |
|---|---|---|---|
| AppA | A15 seating | Written before Ch16; row convention vague, no two-row rule | Rewritten to Ch16 exactly: row faces north (right = east, seat 1 west); centre-facing circle or rectangular table right = anticlockwise; outward reversed; top row faces south (right = west), bottom row faces north (right = east), opposite = same seat number. Ch36 M4 items already agree (left = clockwise facing centre; north row faces south). Ch17 and Ch18 have no seating items |
| AppB | B4.1, B4.2 | Same vagueness; no two-row template | B4.1 states Ch16 convention; new B4.1b two-row template; B4.2 notes rectangular table |
| AppA | A11 table | Rows 1 and 2 omitted certain conclusions found by code (Some X are Z; Some Z are X) | Added; added note that Some/No can be swapped |
| AppA | Part headings | Part 2 to 6 names and ranges differed from the index, Ch 7-11 etc. and from AppE | Renamed to the book's parts (2 Organising Information, 3 Classic Reasoning Problems, 4 Critical Thinking, 5 Problem Solving and Proof); intro notes Part 6 has no formulas |
| AppA | A18 | Century odd days and month odd days are correct but not taught in Ch20 | Labelled "Extra (not taught in Chapter 20, checked by code)" |
| AppF | intro and entries | Said Ch16 and Ch19 missing; no Ch35-37 terms | Intro updated; 36 entries added (Ch16 18, Ch19 8, Ch35 3, Ch36 1, Ch37 6), alphabetical, each with (Ch N), definition and tiny example; one row added to "Easy to confuse" (sitter's left vs yours). Total entries now 315. Ordering of every section re-checked by code |
| AppE | Ch37 | Said Ch37 has no practice count; it has 15 exercises | Stated treatment: excluded from all totals (845 and 965 if counted); Ch35 = 10 cases (5 sub-parts each, not counted separately); Ch36 = 120 mock questions only; Ch16 (30) and Ch19 (20) are in the index count |
| AppE | Plan B table | "Approx months" basis unstated | Header says 30-day months |
| AppD | labels | "What it is about" bullets not individually labelled | Each now says "from memory, unverified"; note added under table |

## Counts recomputed (AppE)
Chapter files: Ch1-34 practice = 820 (all 34 match the index); + 10 cases = 830; mocks 8 x 15 = 120; total 950. Weekly chapter practice 65, 65, 95, 65, 100, 95, 85, 80, 50, 55, 65, 10; per-day figures (rounded up over 5 days) 13, 13, 19, 13, 20, 19, 17, 16, 16, 17, 19, 8: all as printed, no change needed. All 37 chapters appear exactly once in 12 weeks. Plan B days 111 / 129.5 / 148 (alternating 3 and 4 = 129) correct.

## AppD
No years, prices, quotes, sales or effectiveness claims (grep). Three books, all labelled from memory, unverified; links to Ch 23-29 consistent with the index parts.

## Style
No em or en dashes, fences balanced, blank line after every table in all five files.

## Unresolved or unverified
- Book titles, authors and descriptions in AppD cannot be checked offline (labelled as such).
- Ch35 has no self-check section (not in scope, but AppE Plan A weekly checkpoint says each chapter has 3 self-check questions): flag for the Ch35 owner.
- The Ch16 queue/seating glossary example for "Somewhere right of" was written to match Ch16 (row faces north, seat 1 west).
