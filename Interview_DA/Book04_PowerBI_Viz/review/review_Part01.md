# Review: Book 4 Part 01 (Power BI basics), Wave C

Scope: `Book04_PowerBI_Viz/Book04_Part01.md`, Q1 to Q55. Edited in place with targeted edits. No headings, numbers, stars or order changed. No git commit.

## Counts
- Answers checked: 55 of 55.
- Pandas snippets: 10 found (Q14, Q16, Q20, Q25, Q27, Q28, Q29, Q48, Q49, Q50). All 10 run OK on pandas 3.0.5 after the fixes below. All printed values and Result lines match; every Result was also re-derived by hand (e.g. Q20 2/8 = 25.0%, Q49 total 18/300 = 6.0%, Q29 High total 229,000, Q50 RLS sums 112,000 / 84,000 / 0 / 381,000).
- Answers fixed: 26 (list below).
- Template: all 55 have every required field. Q37 has Result (not run here, no calculation). Q54 reuses the Q49 pandas run by reference.
- Markdown: code fences balanced; all tables have a blank line before and after (after fix).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q3 | DAX, composite models used without explanation | Added plain-word glosses |
| Q4 | "capacity", "dataflow" unexplained | Glossed with cross-ref |
| Q5 | Pinned-page drill-down claim unlabelled | Added "from memory, unverified" |
| Q6 | "star schema", RLS, gateway unexplained | Glossed in place |
| Q7 | privacy levels, gateways, credentials unexplained | Glossed |
| Q10 | .pbit "from memory, unverified" contradicted Q41 (verified there) | Replaced by cross-ref to Q41 |
| Q14 | Snippet used undefined `emp`; table directly after text line (no blank line); DISTINCTCOUNT "returns BLANK on no rows" stated as fact | Self-contained snippet, blank line added, BLANK claim labelled from memory |
| Q15, Q18 | "Analysis Services" unexplained | Glossed |
| Q16 | Snippet had no data/print; "Fields pane" vs Data pane (Q22); table without blank line; Headcount ticked before measure created | Self-contained snippet with prints, wording and order fixed, blank line added |
| Q17 | Mobile layout path unlabelled | Labelled from memory |
| Q19 | Service Download-icon path unlabelled | Labelled from memory |
| Q20, Q25, Q29 | Snippets used undefined `emp` | Made self-contained; output marked "run with pandas 3.0.5" |
| Q27 | Printed "Output" line did not match what the code prints (`8 -> 9`); undefined `emp`/`new_row`; "View/Optimize ribbon" asserted | Snippet self-contained, output corrected, ribbon tab labelled from memory |
| Q28 | Called a DATATABLE calculated table a "measure"; pandas snippet lacked `import pandas` | Wording fixed; import added |
| Q29 | Said icon glyphs confirmed on Learn's export page (not credible); cross-ref to "Q Employee ID summed" | Icon claim relabelled from memory; cross-ref now Q14 |
| Q32 | "Desktop only: more than 100 connectors" contradicts Q1/Q7 (Service connects to sources too) | Softened, marked approximate |
| Q36 | "Entra" unexplained; "dataset settings" old term | Glossed; "semantic model settings (formerly dataset)" |
| Q37 | Premise quotes an error text that is probably not the exact Desktop wording | Edge case note added, labelled unverified |
| Q48 | "dictionary encoding", "high-cardinality" unexplained | Glossed |
| Q50 | "PAN" unexplained for non-Indian-tax readers/HR newcomers | Glossed |
| Q52 | 0.6 GB compression example looked like a fact | Marked illustration only |
| Q54 | Desktop path (Home > Data) inconsistent with Q33 (Get data) | Aligned to Q33 wording |
| Q55 | "Delta tables" unexplained | Glossed |

## Verified by reading (DAX/M)
All DAX measures (Q14, Q16, Q20, Q25, Q27, Q28 DATATABLE, Q29, Q49, Q50 role filter, Q54) have balanced brackets, valid function names/argument order, and return what the answer says. M snippets in Q8 and Q37 are syntactically valid (Table.SelectRows; Excel.Workbook with DelayTypes option, Table.PromoteHeaders). Q2, Q4, Q12, Q13 contain no click-path or code, so no "not run here" label is needed; Q6 has none either.

## Unresolved / notes
- No Microsoft or Tableau page could be fetched in Wave C. Every "Verified on Microsoft Learn" statement in this part is Wave B's claim and was NOT re-verified here. Highest-risk specifics: Q25 export row limits (500,000 / 150,000 / 30,000), Q19 system requirements (.NET 4.7.2, RAM), Q35 licensing sentence (Pro to publish to Report Server), Q52 1 GB limit, Q53 audiences/user limits, Q55 SKU guardrails.
- Q42 refers to "from October" and an August 2026 What's New page; date-sensitive, check at publication.
- Q25 and Q46 cite different pages for Analyze in Excel (Q25 cites the Desktop getting-started page); consider aligning.
- Claims left "from memory, unverified" (kept as labelled): menu paths in Q14, Q17, Q22, Q30, Q36, Q37, Q44, Q51; Mac "no support" (Q3, Q19, Q31); DISTINCTCOUNT/COUNTROWS BLANK on empty (Q14, Q28 cites Learn for COUNTROWS only).
- "Asked at" claims (Q6 Deloitte USI Hyderabad Sept 2025; Q34 Microsoft Hyderabad Jan 2024) match research/interview_processes.md; all others say "commonly asked".

## Ordering / numbering
Stars descending then green to red within each star is respected (Q1-14 3-star green, Q15-16 3-star yellow, Q17-29 2-star green, Q30-40 yellow, Q41-43 1-star green, Q44-52 yellow, Q53-55 red). Numbering continuous 1 to 55.

## Overlap with other parts (report only)
- Q40 (yellow Apply-changes banner) vs Part 2 Close & Apply (sources file says Part 2 covers only the step).
- Q50 and Q54 touch RLS and shared models, likely deeper in the DAX/modelling/admin parts; Q15/Q33/Q55 storage modes may recur in later parts. Not checked in detail.
