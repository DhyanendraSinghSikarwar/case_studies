# Review: Book 5 Part 1 (Maths Foundations), Wave C

## Counts
- Answers checked: 61 (Q1-Q61); all template fields present (Asked at, checking, Say this, Explain simply, Worked example, Excel/Python, follow-ups, mistakes).
- Python snippets run: 61; 61 reproduce the pasted output exactly (checked by an extraction script, `python3 -I`, after the edits too). No seeds needed (no randomness).
- Every worked number, Excel result and prose figure was re-derived by hand or in Python (percent change, attrition, CAGR 14.47%, 21.64%, weighted averages, funnel, rule of 72 table, break-even, CMGR 5.39%/87.7%, rate/mix split +2,300/-3,100, CPI real change -4.8%). All correct.
- Answers fixed: 6 (one substantive error, one wording error, four readability fixes).
- Code fences balanced (244 lines of fences); no em dashes in answer text; no tables.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q27 | Follow-up defined "contribution to growth" as a department's change divided by the company's total change. That gives share of growth, and contradicts Q35 (change divided by last year's total, in percentage points). | Reworded to "change divided by last year's company total, in percentage points (see Q35)". |
| Q51 | Interview line said the harmonic mean applies when "the same amount of the bottom quantity" is fixed. For speed and cost per hire the fixed quantity is the top one (distance, money). Explain-simply and example were already right. | Changed to "top quantity ... equal distance covered ... equal money spent". |
| Q34 | Follow-up said the median is "No" 63; it cannot be known from an average alone. | Now "Not necessarily; it needs the individual scores". |
| Q46 | Code used a lambda, list comprehensions and compact index loops (violates style_guide Section 10). | Rewrote as one-step-per-line loops with a comment per step (4 numbered steps). Output re-run: now [33.3, 33.3, 33.4] (tie goes to last item); pasted output and a plain-words line updated. Prose values unchanged. |
| Q17, Q19 | Printed bare numbers with no labels (`-50.0 15.0 -42.5`, `4.0 80.0`), hard for a non-technical reader. | Added labelled print lines; pasted outputs updated. |

## Checked and left as is
- Premises: Q15 (ambiguous "headcount 250") and Q16 (yearly path not given) already state the assumption; Q50 negative-base convention (divide by |old|) is hedged in the answer.
- Excel formulas are all labelled not run in Excel here or are trivial; versions stated where relevant (RRI 2013+, SUMPRODUCT 2007+, GEOMEAN/HARMEAN/NPER standard). Logic matched against the Python results.
- "Asked at" lines all follow `research/Book05_Part01_sources.md` (generic prep material, no company reports); none name a company as an asker. Q36 mentions the Dataford/Red Ventures practice-platform question, which is in the sources file.
- Cross-references (Q1->Q37, Q3->Q43, Q5->Q56, Q6->Q41, Q8->Q58/Q60, Q10->Q16/Q32, Q13->Q46, Q41->Q59, Q48->Q51, etc.) all point to the right questions.

## Unresolved / report only
- Ordering: stars then difficulty order is correct (Q1-Q16 3-star, Q17-Q42 2-star, Q43-Q61 1-star; green/yellow/red ascending within each star). File header says "Target 60 / Actual 61"; count matches.
- Several 2-star snippets (Q21-Q26, Q28-Q30) still print unlabelled value lists; each is followed by a plain-words line, so left (low priority).
- Overlap with other parts: Q18 (mean vs median for salary) overlaps Part 2 (mean/median/SD); Q41 and Q59 (Simpson/mix effect) may overlap with a later Simpson's-paradox question if Part 2-4 cover it; Q10/Q16/Q32/Q49/Q58/Q60 form a tight CAGR/geometric-mean cluster within this part (intentional but repetitive).
- Q32 "AM overstates growth when rates swing" and Q16 "arithmetic mean is at least CAGR" are consistent (AM-GM on growth factors).

## Claims left unverified
- Q38 Rule of 114/144 is labelled "from memory, unverified". Q48 inventory valuation (weighted average cost vs FIFO) labelled from memory.
- Q4 "stricter average uses all 12 month-end headcounts" and Q38 "roughly 4% to 15%" accuracy range are standard practice statements, not sourced (sources were snippets only; no page fetched in full).
- Q52 CPI values are made up and labelled as illustrative.
