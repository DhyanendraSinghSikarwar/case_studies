# Review: Book 4 Part 11 (Copilot and AI features in Power BI)

Reviewer: Wave C. File: Book04_PowerBI_Viz/Book04_Part11.md. No git commit.

## Counts
- Answers checked: 27 (Q1-Q27).
- Pandas snippets run OK: 5 of 5 (Q3, Q12, Q13, Q23, Q24), pandas 3.0.5, scratch at .../scratchpad/C04_Part11/t.py. All printed values and Result lines match (0.25; HR 0; HR/IT/Sales 0.0/0.25/0.40; Overtime No 0.0, Yes 0.6; IT-Yes 1, Sales-Yes 2).
- DAX re-derived by hand: Headcount 12, Leavers 3, Attrition Rate 0.25; by dept HR 0, IT 1/4, Sales 2/5; matches. Syntax of the DAX snippets (COUNTROWS, CALCULATE, DIVIDE, EVALUATE ROW, SUMMARIZECOLUMNS + ORDER BY) is valid by reading.
- Answers fixed: 14 (Q2, Q3, Q4, Q7, Q12, Q13, Q18, Q20, Q23, Q24, Q26; plus Q3/Q12/Q13/Q23/Q24 snippet fixes counted in these).

## Fixes
| Q | Wrong / missing | Fix |
|---|---|---|
| Q3, Q12, Q13, Q23, Q24 | Pandas snippets used `e` but it was never defined, so they could not run as shown | Q3 now builds the 12-row Employees DataFrame; the others carry a "uses the DataFrame e built in Q3" comment; "run with pandas 3.0.5" added to outputs |
| Q12, Q13, Q23, Q24 | Printed output shown as `0.000/0.250/0.400` but pandas prints `0.00/0.25/0.40` | Outputs corrected to the real printed format |
| Q12 | Markdown table had no blank line before it or after it (the note line would be swallowed into the table) | Blank lines added; note reworded (rows 7-9 and 10-11 grouped) |
| Q3 | DAX step lacked the "not run here" label and ROW/DIVIDE were unexplained | Label added, one-line gloss added; Sample data line now points to Q12 |
| Q13 | Result implied it depends on the `[Attrition Rate]` measure without saying so; vague "summarise" wording | Dependency on the Q12 measure stated; "reproduced with pandas (not a DAX engine)" added |
| Q2 | "14 of them" ambiguous; Analytics-pane click path not labelled | Now "14 of the 19"; "menu names from memory" added |
| Q7 | Click path lacked "from memory" | Added |
| Q4 | "SKU" and "Private Link"/"sovereign clouds" unexplained | Short plain glosses added |
| Q18 | "about 10,000 characters per file" garbled (the source says prompt limit); streaming datasets / live Analysis Services unexplained | "per prompt, per the research file"; glosses added |
| Q20 | Azure OpenAI and RLS unexplained at first use | Glosses added |
| Q23 | DirectQuery unexplained; Result mixed two runs | Gloss added; Result notes Sales/IT/HR rates come from Q12 |
| Q24 | Leavers measure not tied to Q12 | Reference added |
| Q26 | Example said month-end report refreshes cause Copilot usage (refreshes are not Copilot usage) | Example changed to analysts asking Copilot to summarise reports |

## Template completeness
All 27 answers have Asked at, Checking, Say this, Explain simply, Example, Version note, Edge cases, Follow-ups, Common mistakes. Measure/modelling questions (Q3, Q12, Q13, Q23, Q24) have Sample data (or pointer to Q12), DAX/Steps, Alternative, Result and Pandas check. Concept answers omit Sample data/Result/Pandas check, which is allowed. Q11 uses "Example prompt" and "Why good" in place of Sample data; acceptable.

## Ordering / numbering (report only)
Stars descending (Q1-Q4 two stars, Q5-Q27 one star) and within one-star group green (Q5-Q9) then yellow (Q10-Q24) then red (Q25-Q27); but the two-star group is Q1-Q2 green then Q3-Q4 yellow, correct. Numbering continuous Q1-Q27. Header says target 20, actual 27 (left as is).

## Overlap (report only)
- Q4, Q5, Q22, Q25 repeat the capacity/licence facts deliberately (consistent: F2+/P1+, trial unsupported, Pro/PPU alone not enough).
- Q12 attrition measure may overlap with Book04 DAX parts (attrition rate, DIVIDE, CALCULATE) and Q23/Q24 with any earlier visuals part (key influencers, decomposition tree); not compared in depth.

## Markdown
Code fences balanced (14 markers), tables followed by blank lines after the fix.

## Unresolved / left unverified
- All version, licensing, GA/preview, menu-name, admin-setting and region claims remain "from memory, unverified" (learn.microsoft.com unreachable); they rest on the research file's page summaries, which I did not re-check. Includes: F2+/P1+ requirement, standalone Copilot default-on since Sept 2025, Prep data for AI preview status, 10,000-character prompt limit, 200-character description limit, 24-hour cache, Private Link, FCC rules, Q&A retirement date (February 2027 vs December 2026, conflict stated in Q10).
- "Asked at" lines all say no company-specific report found; consistent with the sources file. Q1 cites "8 of 40 pooled JDs" which the sources file ties to GenAI/AI tools generally, not Copilot specifically; wording kept as "AI tools such as Copilot".
- Q27 example "18 of 20 test questions" and Q14 "excludes contractors" are illustrative, not factual.
