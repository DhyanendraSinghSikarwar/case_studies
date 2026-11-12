# Review: Book 8 Part 02 (Stakeholder Request Scenarios)

Reviewer pass: Wave C. File edited in place: `Book08_Scenarios/Book08_Part02.md` (targeted edits only; headings, numbers, stars, order and inline data untouched). No git commit.

## Counts
- Answers checked: 79 of 79.
- Answers with numbers recomputed by code: 28 (Q5-Q6 examples, Q10, Q11, Q22, Q24-Q27, Q31, Q35, Q41, Q43-Q46, Q57-Q60, Q66, Q69, Q73, Q74, Q76, Q77, Q79). Script: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C08_Part02/chk.py`.
- Answers with a wrong or inconsistent figure or statement: 6 (Q11, Q27, Q28, Q58, Q76, Q9). Answers changed in total: 14.
- Structure: all 79 have Asked at, interviewer check, Say this, Likely follow-ups, Common mistakes. Zero em dashes in answer text (only the part-title line), code fences none, no scripts pasted.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q5 | Example figures (12%, 10%) not labelled as made-up | Added "illustrative figures" |
| Q9 | Mini-example said headcount 1,180 "distinct employees"; per Q24 that includes 90 exited staff | Changed to 1,090 active IDs (illustrative, see Q24) |
| Q11 | "Through last week the number is 4,200" clashed with a latest week of 4,500 (looked cumulative vs weekly); scale-up to 5,000 never sanity-checked | Reworded to "last complete week was 4,200"; added that 5,000 is about 19% above it (computed) so plausibility must be checked |
| Q21 | "groups of at least five" stated as if a rule | Marked as an example threshold; use company rule |
| Q27 | 8 to 10 hours of 90-minute requests is 5.3 to 6.7, not "5 to 6" | Changed to "5 to 7 (5.3 to 6.7)" |
| Q28 | Script said A (12 h) plus B (15 h) cannot both fit in a week; 27 h fits in 40 h | Added assumption: other commitments leave about 20 h; marked illustrative |
| Q30, Q37, Q46 | Script numbers not labelled as invented | Added "illustrative" |
| Q32 | "Asked at" did not use the standard no-company-report wording | Aligned wording |
| Q41, Q59 | Minimum group size "5 or 10" given without the unverified label | Added "from memory, unverified" |
| Q58 | Pilot 62% vs 55% (n=200 each) presented without a chance check; the 7-point gap is not significant | Added chi-square p about 0.16 (Fisher about 0.19), "encouraging, not proven" |
| Q76 | "48 hours in four weeks, leaving 28 hours (70%)" mixed four-week and weekly totals | Now "28 hours a week (70%)" |

## Verified correct without change (recomputed)
Q6 6%; Q10 12%; Q11 4,500/0.9 = 5,000; Q22 mean 51.7, median 42; Q24 70 duplicates, 1,090 active, overstatement 160 (12.8% of 1,250); Q25 590 baseline, 10 extra units, 2 pp, 1.7%, relative 11%; Q26 sum 51, mean 10.2, median 3, 2.75, 78%, 80% within 4 h; Q27 18 h = 45%, 20 to 25% = 8 to 10 h; Q31 1.5 h; Q35 96/92 = 1.043, bar heights 6 vs 2; Q41 group total 160; Q43 34/40 = 85%, 5% response, Wilson 70.9% to 92.9%, margin 11.1 points, floor 4.25%; Q44 5% to 10%, +5 pp, exact Poisson ranges 0.24 to 7.22 and 1.09 to 10.24, 40% annualised; Q45 2.5%, 3.125%, 1.25 ratio; Q46 9 + 3 = 12; Q57 15%, Rs 3,00,000; Q58 124 vs 110, 12.7% relative; Q59 25% both; Q60 24+8+8 = 40; Q66 4; Q69 1 pp = 50% relative; Q73 1,010 closing, 1,005 average, 2.99%; Q74 9%, 15%, 6 pp; Q77 100-4-8 = 88; Q79 8 h.

## Premise checks
- Q24: flagged problem (duplicates, exited, contractors) correctly diagnosed; contractor count correctly left unknown.
- Q25: 20% vs 18% baseline handled; percentage vs percentage-point stated correctly.
- Q43: low response rate correctly diagnosed; bounds correct.
- Q44: "doubled" correctly separated from the rate change and noise.
- Q45: denominator choice correct; no premise flaw.

## Unresolved / report-only
- Ordering: stars and difficulty order look consistent (3-star block Q1-Q30, 2-star Q31-Q60, 1-star Q61-Q79); numbering continuous.
- Overlap: Q1 and Q70 (vague asks), Q16/Q25/Q42 (causal claims), Q40/Q41/Q53/Q59 (privacy), Q17/Q28/Q60/Q76/Q79 (prioritisation and intake), Q14/Q57 (error correction) overlap with each other; some likely overlap with Part 01 and Part 03 of this book and Book 11 (soft skills); not checked across files.
- Q53-Q56, Q58-Q63 etc. contain stray blank lines between answer fields; renders fine, left as is.
- Q12 accounting definitions (booked vs recognised) are general knowledge, not labelled; low risk, left.

## Claims left unverified (by design)
DPDP Act relevance (Q40, Q53), minimum group sizes (Q41, Q59), e-commerce conversion convention (Q45), ledger as closest-to-money source (Q77), survey response-rate norms (Q43). All carry "from memory, unverified" or "confirm with legal/owner". "Asked at" claims limited to "commonly asked (no company-specific report found)", consistent with `research/Book08_Part02_sources.md`. No Part 8/9 style personal-experience templates in this part.
