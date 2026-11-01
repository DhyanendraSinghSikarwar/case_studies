# Book 5 Part 1 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the five answer agents). Scope: 50 questions, Q1-Q50 (DSA in Python: arrays and hashing). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Five agents answered Q1-10, Q11-20, Q21-30, Q31-40, Q41-50; merged by heading: 50 of 50 merged, 0 skipped, 0 pending. No spend-limit stops. Agents wrote per-question files and a build script (`build.py` re-runs each code file and pastes the real output), so a stop would have lost nothing.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q50; star order and counts 16 / 20 / 14 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 50 |
| Exactly one python block per answer, re-run standalone with `python3 -I` by the lead | 50 of 50 exit 0 |

Each block holds the brute force, the optimal solution, a seeded randomised cross-check against brute force (300 to 3,000 cases) and edge-case asserts. Outputs that print timings (Q9, Q38, Q40) differ slightly on a re-run and are labelled sandbox-only.

## Prompt examples (Wave A examples were hand-checked, never run)
Every example was re-run by the answer agents. One was wrong and the answer says so plainly: Q41's example (`['ab','ba','abb','bab']`) does not break the sum-of-character-codes key (sums 195, 195, 293, 293 group correctly); `frozenset(word)` is the key that breaks on it, and the sum key breaks on words like 'ad' and 'bc' (both 197). Other notes: Q42's "a few gigabytes" is about 120 MB at 1% false positives for 10^8 URLs; Q43 gave no numbers so the agent chose its own; Q46 overcounts with duplicate values; Q49 divides by zero on duplicate points; Q40's 10^7-int Python list is about 360 MB so it cannot fit in 200 MB and the answer uses `array('q')` with a multi-pass partition (the 10^7 memory figures are linear extrapolations from a 10^6 measurement, labelled as reasoned).

## Findings kept in the text (observed)
A 26-slot array breaks on Unicode with a silent wrong True from a wrapping negative index (Q3); Boyer-Moore needs a verify pass when no majority is guaranteed (Q4, Q30); 32-bit sum overflow at n=10^5 in a fixed-width language (Q8); `Counter -` drops non-positive counts while `subtract()` keeps them (Q18, Q39); `[1,2,3][-0:]` is the whole list (Q14); `hash(-1) == hash(-2)` (Q38); a comma join round-trips `['a,b','c']` wrongly (Q24); sorting on frequency alone interleaves tied values (Q29); a sliding window is wrong on negatives (Q13).

## Hedged / from memory
Q18: `Counter <= Counter` multiset comparison needing Python 3.10 or later was written from memory and not run.

## Evidence limits
No company-reported problems found; every WebFetch failed (neetcode.io unreachable), so sources are snippets only (4 searches). Company tags in community sheets contradict each other, so "Asked at" names source types only. See research_notes/Book5_Part01_sources.md.
