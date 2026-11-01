# Book 5 Part 3 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (DSA in Python: strings). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A ran every prompt example (`scratch/B5P03_wavea/check_examples.py`) before freezing and replaced one example that did not demonstrate its point (a ligature does not separate casefold from compatibility normalisation; the example now uses a circled digit one against '1'). Each answer agent re-ran the examples.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 13 / 15 / 12 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 40 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 40 of 40 exit 0 |
| Cross-references (Part 1 Q3, Q24; Part 2 Q1, Q20; within-part Q5, Q23, Q30, Q31) | verified against headings |

Each block holds the brute force, the optimal solution, a seeded randomised cross-check (3,000 to 6,000 cases) or an exhaustive check, and edge-case asserts. Timings (Q4, Q6, Q33) are sandbox-only and differ on a re-run.

## Prompt examples
All examples in all 40 prompts were correct as written after Wave A's one replacement.

## Findings kept in the text (observed on Python 3.13.17, Unicode database 15.1.0)
- Exhaustive and large checks: all 3,999 integers round-trip for Roman numerals (Q3, Q18 area); a number validator is checked against a regex over all 335,923 strings up to length 7 (Q28); the 3-step caseless key (normalise, casefold, normalise) matches the Unicode standard's formulas for every code point (Q30).
- `int()` of a 10,000-digit decimal string raises ValueError (limit 4,300 digits) but `int(a, 2)` works (Q14, Q15); `'1.2' > '1.10'` is True as strings (Q20); `'٣'.isdigit()` is True so digit tests use `'0' <= c <= '9'` (Q7); Python `//` floors so truncation uses `abs` (Q13).
- The standard library has no grapheme segmenter; reversing a flag swaps it for a different flag (IN becomes NI); `combining()` is 0 for ZWJ, Hangul jamo and regional indicators (Q29, Q31); the real UTF-8 decoder rejects overlong forms, surrogates and values above U+10FFFF that a structural check accepts (Q32); `casefold` maps U+0130 to 'i' plus a combining dot (Q30); 26 code points have casefold output that NFC changes.
- Rabin-Karp without verification and a small modulus gives a wrong answer on a seeded example (`cabccaac` / `cb` returns `[5]`); hash-hit counts 265 vs 0 for modulus 7 vs 2^61-1, labelled a seeded observation, not proof (Q24). `+=` stayed fast on CPython 3.13 but prepend and a second-reference loop degrade (Q6). A regex with nested quantifiers backtracks catastrophically (Q33; about 2x per extra letter in the sandbox).

## Hedged / not verified
Q12's note that CPython's `str.find` uses a two-way algorithm and Q33's claim that Python 3.13's `re` has no timeout argument are marked as not verified; Q20's mention of the `packaging` library was not run; the third-party `regex` module and `grapheme` package are named but not installed or run; Q10's "O(1) extra space" treats the short digit string as constant.

## Evidence limits
No company-reported problems found; every WebFetch failed, so sources are snippets (4 searches). Several problems (zigzag, wildcard matching, valid number and others) come from standard lists known to the Wave A agent, not opened pages. Casefold and grapheme claims rest on the sandbox run and editor knowledge. See research_notes/Book5_Part03_sources.md.
