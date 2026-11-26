# Review G3: Book12_Guide.md front matter, Sections 5, 6, Section 7 table

Counts: about 75 claims/numbers checked; 8 edits. Arithmetic recomputed in Python (all OK). No code blocks in scope (the formula in 6.4 matches the table columns D and G).

## Number audit
| Claim | Source | Result |
|---|---|---|
| n=186, about +/-7 points; Tableau 33%, Power BI 40% | MS Addendum (61/186, 75/186) | OK |
| 0 of 40 first-sample JDs name a certification; two say "certifications" | MS Sec 5 | OK |
| Certificates named only as advantages (Tableau/PBI, Google DA, MS DA Assoc, CBAP) | MS Addendum | OK |
| CBAP only in a 4-6 yr posting | MS Sec 5 | OK |
| Google DA: 9 courses, about 6 months at 10 h/week, India page 3-6 months | A12c sources | OK (snippet label present) |
| PL-300 score 700, outline "as of April 20, 2026", price by country | A12c | OK |
| Tableau Desktop Specialist USD 100, no expiry | A12c | OK |
| PL-300 renewal free, online | A12c; Book 0 Q17 (12 months) | OK; pointer corrected (was Book 0 Q55) |
| DP-600 more advanced | A12c blog | OK (unverified label) |
| Cost worked example: 40 x 300 = 12,000; +10,000 = 22,000; +10,000 = 32,000 | Python | OK, labelled invented |
| Notice example: 50,000/30 = 1,667; 60-20 = 40; 40 x 1,667 = 66,667 (about 66,700) | Python | OK |
| Tracker: Naukri 2/5=40%, LinkedIn 1/3=33%, Career 1/2=50%, Referral 1/1, Consultancy 0/1, v1 1/6=17%, v2 4/6=67%, All 5/12=42% | Python recount of the 12 rows | OK |
| 6 to 10 tracker columns; follow-up 1-2 weeks, max 2-3 | A12c (blog, convention) | OK, labelled |
| Indeed Hiring Lab India skew | A12c | OK |
| cybercrime.gov.in / 1930 | A12c | OK, snippet label present |
| Book 0 Q55, Q56, Q57 (certs vs projects, placement, bootcamp) | Book00_FAQs | OK |
| Book 0 Q83 (HR achievements to resume lines) | Book00_FAQs | OK |
| Book 12 Q86, Q94, Q98, Q99, Q100, Q101, Q103, Q106 | Book12_FAQs headings | OK, topics match |
| Section 7 table ranges (Q1-24, 25-48, 49-66, 67-84, 85-94, 95-108; 108 total) | FAQ section headings | OK |
| Book 11 Parts 1, 2, 8; Books 1, 2, 4, 7, 8 pointers | plan.md Sec 6 | OK |

## Fixes
| Location | Problem | Fix |
|---|---|---|
| Front matter, "How to read" | "Every number comes from research" contradicted by invented worked examples | Reworded to exclude numbers marked illustrative/invented/our design |
| 5.2 Renewal bullet | "Book 0 Q55" does not mention PL-300 renewal (it is in Book 0 Q17) | Changed to Q17 |
| 6.9 | "Labour Codes leave it to the contract" not in any source file | Removed |
| 5.4 A | "course says about 40 hours" read as a fact | Marked as invented figure |
| 5.3 | Thresholds 0-2 and 4 of 10 unlabelled | Added "our own rules of thumb" line |
| 6.4 row 3 | "Ghosted" in week 1 contradicts the 6.6 cut-off rule | Status changed to Applied (summary unaffected) |
| 6.7 | "CompTIA blog snippet" claim about rigid JD requirements not supported by the sources (they only say general rejection advice) | Relabelled as our reasoning plus general blog advice, unverified |
| 6.1 | Missing pointer to the FAQ about 10 applications with no reply | Added Q98 |

## Claims still unverified
All certificate facts and the notice, scam and follow-up points remain snippet or blog level; labelled as such in the text. Book 0 Q17 says PL-300 is a 100-minute exam; Book 12 does not repeat it.

## Could not check
No web access: live prices, PL-300 rupee fee, platform wording. Did not review FAQ bodies (other reviewers).

## Overlaps / ordering notes (report only)
- Book 0 Q83 says "Where covered: Book 12 Part 1" (Book 12 uses Sections); in the Book 0 reviewers' scope.
- Section 5 intro says Google DA is on Coursera; Book 0 Q17 lists its tools (Python, SQL, Tableau); no contradiction.
- No em or en dashes, no ANSWER_PENDING, code fences balanced (6 fences in file), blank lines after tables present in scope.
