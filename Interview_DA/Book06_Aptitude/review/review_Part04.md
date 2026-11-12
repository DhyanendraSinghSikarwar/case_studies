# Review: Book06_Part04 (Simple/Compound Interest & Business Finance Basics)

## Counts
- Answers checked: 52 (Q1-Q52, headings, stars and order untouched).
- Answers re-solved by independent code (exact fractions, bisection for the EMI rate): 52 (every numeric item, plus all follow-up variants and trap numbers; concept items Q1, Q4, Q13, Q41, Q49 via their worked examples).
- Answers with a wrong final answer: 0.
- Answers changed: 8 (3 wrong follow-up/intermediate figures or explanations, 5 wording/clarity/claim fixes).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q27 | Follow-up "360-day year gives about Rs 740.28" is wrong; exact value is 36,500 x 10 x 73 / 36,000 = 740.14 | Corrected to Rs 740.14 and showed the formula |
| Q36 | Follow-up "10% yearly instead: difference is 0" is wrong and unclear; 10% yearly vs 5% half-yearly differs by Rs 25 | Rewrote the follow-up with the Rs 25 working |
| Q19 | "Explain simply" for year 3 (adds 210) was garbled | Rewrote as year-by-year gap: 100 + 210 = 310 (1,210 vs 1,000 in year 3) |
| Q12 | "Say this" line was awkward ("earned 1 times P ... so P per 8 years") | Reworded in plain language |
| Q42 | "roughly 16.2%" reducing-balance equivalent was unexplained and unlabelled | Verified (16.24% nominal, monthly basis; 17.5% effective) and labelled as nominal reducing-balance rate found by trial |
| Q52 | Follow-up "about 45%" effective rate | Precise value 44.6%; changed to "about 44.6%" |
| Q50 | "banker's discount" used without explanation | Added one-clause definition |
| Q49 | Follow-up 1 ("pick A") relied on unstated assumptions | Stated assumptions: mutually exclusive projects, NPVs at the required rate |
| Q20 | Asked-at said growth problems are "listed as common aptitude items", which the sources file does not state | Changed to similar-pattern-on-prep-sites, unverified |

## Verified without change (by code)
Q2-Q3, Q5-Q11, Q14-Q18, Q21-Q26, Q28-Q35, Q37-Q41, Q43-Q48, Q50-Q51: answers, step-by-step working, Check lines and follow-up numbers all match (e.g. Q15 quarterly 17,661.01; Q28 3-year gap 7,521.50; Q30 follow-ups 5,714.29 and 5,466.94; Q43 NPV at 15% +29.87 and at 20% -119.44; Q44 EMI 8,885 matches a 12-month loan, 8,884.88; Q45 follow-ups 4,222.2 and 6,872.73; Q46 monthly 21.94%; Q47 42.58%; Q51 follow-up 2,481.82; Q52 18.43% and 37.24%). Shortcuts checked valid: CI-SI difference (2 and 3 years), successive percentages a+b+ab/100, alligation, ratio of consecutive amounts, doubling-time scaling for SI vs CI, Rule of 72 (limits stated), Fisher real rate.

## Assumptions noted in answers (verified present)
- Q23 ROI (profit stated before campaign cost) has the alternative reading in follow-ups.
- Q29 fractional year (annual compounding, 1.5 years) states the convention used.
- Q44 gives no tenure; the answer uses only the stated EMI and notes the 12-month match.
- Q45 and Q51 state the end-of-year payment and interest conventions.

## Unresolved / report only
- Ordering/numbering: no problems; "Target: 50, Actual: 52" header is consistent with 52 questions.
- Overlap within the part: Q10/Q12/Q33 (n-times growth), Q13/Q14/Q19/Q28 (CI-SI gap), Q15/Q29/Q36/Q46 (compounding frequency) are deliberate variants. Overlap with other Book 6 parts (percentages, ratios) was not examined.
- Q1, Q4, Q13 have no separate "Check" line (the check is inside the mini-example); concept items, left as is.
- Q41 (Rule of 72) rests on ln 2 explanation; "6% to 12%" accuracy range is a rule of thumb.

## Claims left unverified
- All "Asked at" company tags (TCS, Infosys, Wipro, Cognizant GenC) rest on prep-site snippets in research/Book06_Part04_sources.md and remain labelled unverified. No time-per-question or pass-mark guidance appears in the part.
- No em dashes in answer text (only the part title line); code fences balanced (none used); no SQL in this part.
