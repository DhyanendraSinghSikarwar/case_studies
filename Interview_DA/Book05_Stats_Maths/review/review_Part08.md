# Review of Book 5 Part 8 (A/B Testing for Analysts), Wave C

Reviewer: Wave C. File edited in place: `Book05_Stats_Maths/Book05_Part08.md`. Scratch scripts in the session scratchpad (C05_Part08).

## Counts
- Answers checked: 43 of 43 (all template sections present in all 43; Q14 and Q6 label the worked example with a suffix).
- Python snippets extracted and run: 38 of 38 ran without error and reproduced the pasted output exactly (seeds reproduce). Q22 was changed to include a simulation (new output pasted); Q11, Q12, Q15, Q22, Q25, Q27 re-run after edits.
- Answers fixed: 17 (Q4, Q10, Q11, Q12, Q13, Q14, Q15, Q18, Q22, Q24, Q25, Q27, Q28, Q29, Q32, Q36, plus Asked-at wording on Q26, Q31, Q33, Q35, Q39, Q41, Q43).
- Independently re-derived: sample sizes 3,839 / 14,749 / 57,760 / 1,091 / 248 / 10,327 / 1,772 / 213,797 / 2,302; z = 2.021, p = 0.0432; Q25 p = 0.38; Q29 chi-square and p; Q28 and Q43 arithmetic; Pocock 2.413 (confirmed by simulation 0.049). All match.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| 4 | H1 written as "conversion is not 10%", which confuses a comparison of A and B with a test against a fixed 10% | Rewritten: H0 same true rate for both buttons, H1 true rates differ |
| 10 | No Excel formula for a key calculation | Added ROUNDUP/NORM.S.INV formula (2010+, labelled "not run in Excel here", logic checked in Python = 3,838.1 before rounding up to 3,839); plain-words line |
| 11 | Inline trailing comments, no comment above steps; 5.56% vs 5% unexplained | Comments moved above each step; plain-words line noting the simulation noise |
| 12 | Single-letter names a, b; no plain-words line after output | Descriptive names, comments, plain-words line added |
| 13, 14, 36 | No plain-words line after output | Added |
| 15 | Unlabelled setup lines | Comments added |
| 18 | Say-this "usually one to two weeks" contradicted the 3-week worked example | Now "often one to three, never less than one" |
| 22 | Prose quoted a simulation (64.4%, 4.7%) that was not in the code and did not reproduce | Added seeded simulation to the snippet; prose and output now 64.0% and 5.0% (0.64045, 0.0495) |
| 24 | "Bootstrap" used before it is explained (explained only in Q33) | Added short plain gloss |
| 25, 27 | Code steps without comments | Comments added |
| 28 | Worked example did not say that control pays the Rs 30 fee on every order (needed to reproduce Rs 26,000) | Assumption stated |
| 29 | "Many teams alarm at p below 0.001" was an unsourced fact | Labelled "from memory, unverified" |
| 32 | Said "Simulated and computed below" but nothing is simulated | Now "Computed below" |
| 26, 31, 33, 35, 39, 41, 43 | Asked-at lines added generic or unsupported claims (e.g. "standard item in prep lists", "experimentation-heavy companies") | Reduced to "commonly asked (no company-specific report found)"; Q41's remaining remark labelled from memory, unverified |

## Checked and found correct (no change)
Definitions of p-value, CI, Type I/II, power, one vs two-tailed, SRM, CUPED variance formula (1 minus correlation squared), delta-method code, Bonferroni, DiD, Bayesian numbers. Excel functions used (NORM.S.DIST 2010+, CHISQ.TEST 2010+) are correctly named and labelled as not run in Excel here. No em dashes in answer text (only the file title heading has one). Code fences balanced (104). No tables in the file.

## Ordering, numbering, overlap (report only)
- Header says Target 40, Actual 43; numbering Q1 to Q43 is sequential, stars descend 3 to 2 to 1 with no disorder.
- Overlap with other parts (not checked against their files in detail): p-value, CI, Type I/II and power (Q7, Q12, Q15, Q20) likely repeat hypothesis-testing and CI parts of Book 5; Q22/Q36 multiple comparisons; Q24 test selection; Q43 causal inference. Suggest cross-referencing rather than deleting.
- Q9, Q30 and Q37 are the only places where other parts' numbers (Q41 CUPED) are referenced; internal cross-references Q-numbers checked and valid.

## Unresolved / left unverified
- No company-specific Asked-at evidence exists; all lines say "commonly asked (no company-specific report found)". Source pages were read at snippet level only (see `research/Book05_Part08_sources.md`), so claims such as "A/B appears in about 50% of DS interviews" are not used in the answers and remain unverified.
- Q28 (Swiggy) is a Swiggy-style scenario, not a verified Swiggy question; numbers are invented and labelled made-up.
- Q39 delta-method false-alarm rate 6.2% vs 5% is attributed partly to simulation noise; with 1,000 runs that is about 1.7 standard errors, so a small genuine excess cannot be ruled out. Wording left as is.
- Q42 Pocock constant 2.413 is from memory but confirmed by the in-answer simulation.
- Q23 hash example: md5 assignment is illustrative; a 6-person list cannot show balance (already stated).
