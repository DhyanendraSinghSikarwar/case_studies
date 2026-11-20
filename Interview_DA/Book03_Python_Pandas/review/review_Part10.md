# Review: Book 3 Part 10 (Basic Coding Logic), Wave C

## Counts
- Answers checked: 71 of 71.
- Python snippets run (Python 3.13, `-I`, each block standalone): 74 blocks. 69 reproduce the pasted output exactly. The other 5 are explained below (all fine or fixed). No pandas code in this part, so pandas 3.0.5 behaviour was not at issue.
- Answers edited: 24 (5 content fixes, 19 template/sample-data additions, some overlap).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q68 | "What it means" said 4 and 8 stayed in the list; real output `[4, 7]` shows only 4 stayed (8 was removed) | Prose corrected; added the correct answer `[7]` (verified) |
| Q21 | Alternative claimed the arithmetic swap fails "with very large numbers"; Python ints do not overflow | Now says it can lose accuracy with decimals and confuses readers |
| Q36 | Said a lambda "cannot contain comments" (irrelevant/wrong framing) | Now says a lambda holds only one expression |
| Q58, Q70 | "Asked at" cited "differentiator list/topic", not a source | Changed to "commonly asked (no company-specific report found)" |
| Q71 | "rarely asked of analysts" is an unsupported claim | Reworded to "an advanced topic that can set a candidate apart" |
| Q56 | Missing "What it means"; garbled sentence in Common mistakes | Added "What it means"; rewrote the mistake line |
| Q8, 13, 18, 46, 48, 49, 50, 51, 55, 57, 58, 59, 60, 65, 66, 67, 69, 70, 71 | Code answers lacked the "Sample data" line | Added (input values or "none needed") |

## Snippet results not matching literally (no fix needed)
- Q11: the second half deliberately raises `TypeError`; the pasted output shows the error line. Correct.
- Q52: timing values change per run (pasted 0.00869 s, my run 0.0146 s; set lookup shows 0.0). The prose already says times vary. Left as is.
- Q61, Q67, Q68 "Alternative" blocks are fragments that need the main block's variables; run with that context they give the pasted outputs (`{'A': ['Asha', 'Meena'], ...}`, `['Asha']` then `['Ravi']`, `[7]`). Q6's claim that `list(set(...))` printed `[104, 101, 102, 103]` was reproduced.
- Q71: output `0.0000 seconds` varies by machine; fine.

## Claims check
- "Asked at" lines checked against `research/Book03_Part10_sources.md` and `research/interview_processes.md`: Tiger Analytics (Python duplicate frequency), LatentView 2020 campus (OOP basics, GfG), Deloitte 2021 campus (diamond pattern, GfG), Accenture (AmbitionBox anagram, 2024 list comprehension), InkRevenue, PracHub, Dataford, DataLemur are all supported at snippet level. Others already say "no company-specific report found". No invented companies or statistics found.
- Sources file itself notes snippet-only evidence and about 40 gap-fill questions; stars are inference, not measured frequency.

## Report-only items
- Title line of the file contains one em dash ("Book 3 — Python..."); it is a heading, left unchanged. No em dashes in answer text. Fences balanced; blank lines after tables OK.
- Numbering: Q1 to Q71 in order; the header says "Target 65 / Actual 71", consistent. Stars are non-increasing (3, 2, 1) as intended; Q14 to Q17 are 3-star yet marked 🟡 (difficulty, not frequency), consistent with the sources file.
- Overlap: Q13 and Q51 (factorial loop vs recursion), Q2 and Q42 (palindrome basic vs cleaned), Q3, Q4, Q9 and Q16 (same counter pattern), Q5 and Q15, Q6 and Q9: intentional progressions, cross-referenced. Q46 and Q47 and Q11 touch mutability; Q16 and Q44 and Q36 reuse `key=lambda`. Possible overlap with Part 1-2 (strings, mutability) was not checked against those files.
- Q52 and Q71 contain timing code (`time.time()`); acceptable because the question is about speed, but they are the closest thing to scaffolding in the part.

## Unverified
- Statements about other Python versions (`|` on dicts needs 3.9+, `{**a, **b}` works from 3.5, the default recursion limit of about 1000) are from memory; the `|` merge and the recursion behaviour ran fine on 3.13 only.
- Big-O and bytecode explanations (Q52, Q56, Q64) are standard concepts, not executed.
