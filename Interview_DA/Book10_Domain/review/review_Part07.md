# Review: Book 10 Part 7 (IT services / GCC reporting & MIS, Workday, Alteryx)

## Counts
- Answers checked: 76 of 76 (headings, numbers, stars, order untouched).
- Answers with numbers recomputed by code (independent script, before comparing): 40 (Q15, 19, 20, 23-26, 30-32, 46-53, 55-59, 65-67, 71-75, plus the SQL in Q50 and Q73 and the pandas in Q69, all executed).
- Answers wrong or changed: 12 (arithmetic wrong: 0 of the headline figures; 2 worked examples had internal problems, Q31 and Q72; the rest are wording, consistency and labelling).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q4 | Follow-up stated "onsite is a smaller share of headcount but a larger share of revenue" as a flat fact | Softened to "often", with reason, "check the firm's own data" |
| Q3 | 70% gross / 80% net example looked like a real figure | Labelled "for example ... (illustrative)" |
| Q11 | Illustrative RAG bands (0.9/0.8) differed from Q20 (0.95/0.85), while its own "common mistakes" warns against differing thresholds | Aligned to the Q20 bands, cross-referenced |
| Q20 | "Say this" said "amber to red on schedule"; on the stated bands SPI 0.90 is amber | Now "amber on schedule, red on cost" on the illustrative bands |
| Q22 | "72 hours a year, so it is worth automating" was an unconditional claim | Made conditional on build and upkeep effort; labelled my rough rule |
| Q31 | Worked example: estimated cost 90 lakh on a 60 lakh contract (a loss-making contract, confusing) with 36 lakh incurred | Changed to est. cost 45, incurred 18: still 40% complete, 24 lakh recognised |
| Q33 | "2 a.m. India time is a day early for the US reader" (wrong: it lands on the previous calendar date) | Reworded; says state the "as of" date |
| Q40 | "One worker holds a job through a position or job requisition" (muddled Workday claim) | Replaced by plain statement for position-managed companies (still labelled from memory) |
| Q50 | SQL ran and output matched, but input data was not shown | Added one line describing the sample rows (re-run on rebuilt data: Beta 4/2/50.0, Alpha 3/2/66.7) |
| Q62 | Utilisation formula used "available hours" that neither input file contains | Added where available hours come from (calendar/leave file) |
| Q69 | Pandas snippet used undefined `workers` | Added one line defining the 4-row sample; rebuilt data reproduces the pasted output exactly |
| Q72 | "remaining 6.8 percentage points" added 12% as 5.2 + 6.8, contradicting its own "not additive" warning | Replaced with ratio: 4.48 vs 4.21 is 6.4% higher |
| Q73 | Output "100.0 / 40.0" could not be reproduced from the answer (table not shown) | Added a one-line description of the 10-row sample; rebuilt table reproduces 100.0 and 40.0 |

## Verified by code (all matched the written values)
Q15 70/10/20%, 1,280 idle hours = 8 people; Q19 86.0% and 80.2%, 175 breached; Q20 SV -10, CV -30, SPI 0.90, CPI 0.75; Q23 44.4%; Q24 90%; Q25 9.6 and 13.8, +43.75% (stated 44%); Q26 60 lakh; Q30 24 days; Q32 12 lakh; Q46 45.0%, markup 81.8%; Q47 88%, leakage 1.8 lakh; Q48 12.2 lakh, 45.9% of cost, alt mix 10.98 (-10.0%); Q49 60 lakh; Q51 29.2%; Q52 27 days; Q53 18%, 4.5%, 18%, 20%; Q55 33.3%; Q56 75/85/95/97.9, blended 95.0, simple mean 88.2; Q57 1.23%; Q58 17.5%, 67.9%, 3,357 h, 1,007 h remaining; Q65 60/70/75/80%; Q66 38%/32%; Q67 70%, 87.5%, 63.75%; Q71 11,453,760 and 11,533,936 (+0.7%); Q72 +3.04%, 8.7%, 5.2%; Q73 95.6%, 85.0%; Q74 53.9 and 93.5; Q75 67.5/65.0, 270,000/312,000, 50/55.

## Checks passed
Template: all 76 have Asked at, interviewer check, Say this, Explain simply, Likely follow-ups, Common mistakes (Worked example, Data and tables, Regulation note present where needed). No em dashes outside the part-title line. Code fences balanced (8). "Asked at" lines claim only generic prep-site/vendor support consistent with research/Book10_Part07_sources.md; no company-specific claim. Workday, Alteryx, GDPR and DPDP statements all carry "from memory, unverified" and the compliance caveat.

## Unresolved / report only
- Header says Target 65 vs Actual 76 (sources note explains the 11 gap-fills); consider trimming later.
- Overlap: Q8/Q35/Q54 (response vs resolution vs MTTR) and Q9/Q19/Q56 (SLA by priority) cover related ground; Q3/Q15/Q67 (utilisation) and Q21/Q61 (Alteryx Join) also overlap. Intentional layering, but a cut candidate. Q45/Q60 repeat the privacy theme. Possible overlap with Part 1-6 HR-analytics attrition and headcount answers (not compared here).
- Q43 "no extra licence for standard reporting" and Q70 per-user licensing left as labelled from-memory claims.
- Q19 uses "within SLA / closed + open breached" as one convention; the contract-defined denominator rule is flagged in the answer.

## Claims left unverified
All Workday (calculated fields, report types, Prism, EIB/RaaS, position/supervisory org, business process) and Alteryx (tools, Join L/J/R, Unique U/D, licensing) feature statements; GDPR/DPDP summaries; accounting treatment in Q31 (confirm with finance); EVM and ITIL terminology; industry patterns (pyramid, onsite mix). No web access, so none could be checked.
