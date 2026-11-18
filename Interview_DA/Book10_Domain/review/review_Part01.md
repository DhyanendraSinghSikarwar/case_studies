# Review: Book 10 Part 1 (HR / People Analytics), Wave C

Reviewer script: scratchpad `C10_Part01/check.py` (recomputes every figure; SQLite and pandas snippets re-run on reconstructed sample tables).

## Counts
- Answers checked: 150 of 150 (Q1-Q150, numbering and order verified sequential, no heading changed).
- Answers with numbers recomputed by code: about 95 (every answer with data, rates, bridges, projections, SQL or pandas).
- Answers wrong or changed: 17 (3 arithmetic or consistency errors, the rest clarity, labelling or scaffolding fixes).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q20 | Answer text claimed "all figures computed by code" | Claim removed (figures are correct, 1,248) |
| Q42 | Case answer had no "Explain simply" field | Proposal block relabelled "Explain simply (the proposal)" |
| Q47 | "Small invented table" not shown, so result unverifiable | Reporting structure stated in the heading; result 2.5 reproduced |
| Q59 | "Notice commonly 30 to 90 days" stated as fact | Labelled from memory, unverified |
| Q60 | "Top performers 10 to 15%" unlabelled | Marked illustrative |
| Q65 | Unexplained "simple test, p about 0.48" | Named Fisher's exact test (0.485 confirmed) and explained in plain words |
| Q85 | "(computed)" label | Removed; 50.4%, 39.8, 42.7 confirmed |
| Q91 | Sub-bullet titled "percentage vs percentage points" but is not that | Reworded to "paid 85.7% of market = 14.3% below" |
| Q92 | 7-pair claim had no data | Sample table described; 7 pairs reproduced |
| Q108 | Code had placeholder `pd.DataFrame(...)` (not runnable); forecast L2 = 394 | Real counts added and run; L2 corrected to 395 (total 1,125 now ties) |
| Q109 | "Seven nominations" but output shows six (and "two roles with no successor") | Changed to six nominations rated ready now or 1-2 years; SQL output reproduced |
| Q111 | "From what I have seen reported" implied evidence | Reworded "my impression, unverified" |
| Q121 | "Companies commonly pick 5 to 10" unlabelled | Labelled from memory, unverified |
| Q124 | Margin of error jargon; rise (9 pts) vs margin (7.1) not compared | Explained in plain words; added comparison |
| Q132 | "Compa-ratio = pay / market midpoint" conflicts with Q35 and Q90 (internal midpoint) | Relabelled market ratio, noted strict definition |
| Q133 | "190 + 164 = 355" does not add up as rounded; lead-time statement loose | Rewritten with unrounded 190.5 + 164.3 = 355; lead time = about 1 January for 1 April |
| Q134 | "Standard error" unexplained | Plain-words gloss added |

## Recomputed and confirmed correct (no change)
Q6, Q9, Q20, Q22, Q28, Q31, Q32, Q34-Q39, Q53, Q57, Q63, Q64, Q67, Q69 (SQL 4 candidates, 6 sessions), Q73, Q74, Q76, Q79, Q80, Q82, Q83, Q84 (SQL 5 eligible, 4 retained), Q89, Q93-Q95, Q98 (17 working days, 39,230.77), Q102 (output matches), Q103, Q105, Q107, Q112, Q121, Q128-Q133 (arithmetic), Q135, Q137-Q141, Q143, Q147-Q150. Q148 SQL output reproduced.

## Template and style checks
- All 150 have Asked at, interviewer check, Say this, Explain simply (Q42 fixed), follow-ups, common mistakes.
- No em dashes outside the part-title line; code fences balanced (18); tables followed by blank lines.
- "Asked at" lines all say "commonly asked (no company-specific report found)", consistent with the sources file.

## Unresolved / report only
- Q86-Q102 and several later answers use a different follow-up and "Say this" layout (bullets, no quotes) from Q1-Q85; cosmetic inconsistency, not changed.
- Q35/Q90/Q132 compa-ratio vs market-ratio terminology should be kept consistent across Part 5 (compensation) if it repeats these.
- Overlap candidates: Q22/Q28 with Book 7 Part 8 attrition rate questions (angle differs: denominator and annualising); Q25/Q67/Q125 (early attrition) overlap each other; Q40/Q115/Q119/Q120 DPDP awareness repeated across questions (each hedged); Q103 vs Q38 (both HR vs other-system headcount reconciliation).
- Ordering: star order is non-monotonic only by design (3-star block Q1-Q43, 2-star Q44-Q134, 1-star Q135-Q150); no issue.

## Claims left unverified (labelled in text)
DPDP Act content, PF/ESI/professional tax/gratuity rules, harassment-law confidentiality, Workday and SAP feature mentions, Kirkpatrick levels, Bradford factor definition, HCVA/HCROI formulas, notice-period ranges, agency fee percentages. All carry "from memory, unverified" or are illustrative.
