# Review: Book 10 Part 6 (Marketing & sales analytics)

Reviewer: Wave C. File edited: Book10_Domain/Book10_Part06.md (targeted edits only; headings, numbers, stars, order and inline data untouched). No git commit.

## Counts
- Answers checked: 93 (Q1 to Q93).
- Answers with numbers recomputed by code or by independent arithmetic from inline data: 41 (Q13-Q19, Q29, Q32, Q33, Q35, Q40-Q54, Q66, Q69, Q73-Q75, Q81, Q83-Q87, Q89, Q91, plus SQL in Q55 and Python in Q63 executed).
- Answers wrong or changed: 17 (1 arithmetic-presentation bug in code, 1 code bug, 1 data inconsistency flagged, rest wording or clarity). No headline arithmetic result was wrong.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q22 | Loose reference "see Q39 area" | Now "see Q39 for holdout, geo and before-and-after tests, and Q36 for incrementality" |
| Q16 | "Each column sums to total" but the sums are per row | Changed to "Each row sums" |
| Q35 | Stray "Rounded to whole units" (nothing rounded) | Removed |
| Q46 | "10% gain in any input gives the same lift" is false for cycle length (10% shorter = 11.1% lift) | Now "any of the first three inputs" |
| Q54 | Said the test "looks consistent", but implied unit cost differs (Rs 54,000 vs Rs 56,000 from the stated margins) | Flagged the gap and added check: with equal Rs 54,000 cost the 20% arm earns Rs 18.72 lakh, still below 21.6 lakh; conclusion holds |
| Q55 | SQL: `count(*)` after a left join to orders overcounts leads when a lead has several orders (checked: 4 leads instead of 3). Also integer division in SQLite gave 733.0, not the pasted 733.3 | Used `count(distinct l.lead_id)` and `1.0 * s.spend`; re-ran on rebuilt test data: 733.3 and 800.0, 3 leads, 2 orders, 8,000 |
| Q69 | "Brand A would need 2,000 units just to break even" was loose (ignores brand B) | "alone would need 2,000 units to match its old profit" |
| Q24 | Jargon "immature cohorts" | Plain-words gloss added |
| Q75 | Jargon "right-censoring" | Replaced with plain explanation |
| Q82 | "Needs one to three years of data" stated as fact; "regression" unexplained | Relabelled "from memory, unverified"; regression glossed |
| Q84, Q89 | Buckets (commit, best case, pipeline) summed as if separate, but Q84's own mistakes line warns about nesting | Stated that the buckets are treated as separate, not overlapping |
| Q93 | AUC unexplained | Plain-words gloss added |
| Q56 | k-means unexplained | Short gloss added |

## Verified without change (all recomputed, matched)
Q13 (CTR 2%, CPC 2.50, CPM 50, CPL 83.33, CPA 1,666.67, ROAS 3), Q14 (30/40/40/20%, 0.96%, Rs 12,500), Q15, Q17 (50% rise; formula d/(m-d)), Q18, Q19, Q29, Q32, Q33, Q40, Q41, Q42, Q43 (all RFM scores and ranks incl. ties), Q44 (-2.0; midpoint -1.73), Q45 (97.7%, 115%), Q47, Q48, Q49, Q50, Q51 (ROI -2.0%, break-even 2.86), Q52, Q53, Q66 (mix 24.5%, 3.5 and 5.5 points, 32% relative), Q73, Q74, Q75, Q81, Q83, Q86, Q87, Q91. Q63 hash prefixes (ea4e36a82998, 10571c2886aa) reproduced with SHA-256 on the trimmed, lower-cased emails.

## Checks passed
- No em dashes in answer text (only the part-title line). Code fences balanced (4 markers). Tables followed by blank lines or text.
- Asked-at lines all say "commonly asked (no company-specific report found)", consistent with research/Book10_Part06_sources.md.
- Regulation answers (Q61, Q62, Q63, Q64, Q65, Q88) already carry "from memory, unverified / confirm with compliance" labels; no penalty amounts or dates asserted.
- Template fields (asked at, interviewer check, say this, explain, follow-ups, mistakes) present in every answer.

## Unresolved / report-only
- Header says "Target: 80 | Actual: 93" and there are 93 questions; sources notes explain the surplus. Order of stars is 3-star, 2-star, 1-star blocks, consistent.
- Overlap: Q85 repeats Q46's pipeline velocity (different numbers; intentional but near-duplicate). Q38/Q45 (quota) and Q36/Q39/Q76/Q92 (causation) overlap by design. Q81 repeats MQL/SQL material from Q2. Book 7 Part 4 and Book 8 overlap not re-audited.
- The old chunk file answers_chunks/B10P06_Q17-32.md still contains the "Q39 area" text; not edited (outside scope).
- Q55 and Q63 snippets use invented tables; Q63 omits the DataFrame setup line (the pasted output was reproduced).

## Claims left unverified (labelled in text, not checkable offline)
DPDP Act, TRAI DND/DLT, ASCI, MRP rule, SHA-256 expectation of ad platforms, Apple mail preloading, Diwali dates 2024/2025, frequency-fatigue range, 3x coverage rule of thumb, browser cookie limits.
