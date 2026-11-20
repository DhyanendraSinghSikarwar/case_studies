# Review: Book 4 Part 08 (dashboard design principles and storytelling)

Reviewer: Wave C. Environment: Python + pandas 3.0.5 only; no DAX engine, Power Query or Microsoft docs access.

## Counts
- Answers checked: 47 of 47 (Q1-Q47).
- Pandas snippets run OK: 9 of 9 (Q14, Q21, Q22, Q23, Q25, Q38, Q39, Q40, Q41); all printed values match the answers' Result lines.
- DAX measures hand-checked on the sample data: Q14, Q21, Q22, Q23, Q38, Q40 (numbers match; see fixes for naming).
- Answers fixed: 19 (Q4, Q9, Q14, Q21, Q22, Q23, Q24, Q25, Q27, Q29, Q33, Q37, Q38, Q39, Q40, Q41, Q42, Q43, Q47).
- Template fields: all 9 base fields present in all 47; measure-type answers have Sample data, DAX / Steps, Alternative, Result, Pandas check.
- Markdown: code fences balanced; every table followed by a blank line.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| 4, 9, 37, 47 | Invented-looking figures (12 hires, 40 managers, offer declines, 60% cite managers) not marked as examples | Labelled "illustrative" |
| 14 | Pandas snippet not runnable alone, no printed output; gap measure is a fraction | Added data setup and printed output; edge case on formatting the gap as points |
| 21 | Measures `Actual`/`Target` share names with columns in `Hiring` (a measure cannot share a column name in the same table) | Renamed to `Total Actual`/`Total Target`, updated Variance and Variance %; snippet now runnable and prints totals (146, 150, -4, -2.7) |
| 22 | Same measure/column name clash (`Candidates`); follow-up said biggest drop is Screened to Interviewed (31.2%), which is wrong (lowest conversion is Offered, 30.0%; biggest loss is Applied to Screened, 720); Result lacked "DAX not run" wording; snippet incomplete | Renamed to `Total Candidates`; rewrote follow-up answer; Result now says not a DAX engine; snippet runnable with printed output |
| 23 | Snippet had no data setup or output | Added setup and printed output |
| 24 | Claimed a Desktop colour-blind preview "if available" (not supported) | Replaced with built-in colour-blind-safe theme (from memory, unverified) plus an outside simulator |
| 25 | Snippet had no data setup, unrounded outputs | Added setup, rounding, printed output |
| 27 | "Home > Insert > Buttons" is not a real path | "Insert tab > Buttons > Navigator > Page navigator" |
| 29 | "Insert > Buttons > Web URL" (Web URL is an action type, not a button) | Blank button, then Action type Web URL; marked unverified |
| 33 | Sparkline menu path stated too firmly | Added field drop-down route and "path from memory, unverified" |
| 38 | Sample table `Exits` but DAX used `Attrition[Exits]`/`Dept[Dept]`; measure/column name clash | DAX now uses `Exits[Exits]`, `Exits[Dept]`, measure `Total Exits`; snippet runnable with printed output and the split of the Other group stated as illustrative |
| 39 | Steps said to set first and last bars as totals via Breakdown (doubtful; risks double-counting 530) | Rewrote: opening value as first category, rely on automatic Total bar (from memory, unverified); snippet runnable with output |
| 40 | "IT above 90% every day" but Fri = 90; red-to-green gradient contradicts Q24; DAX uses Present/Scheduled columns the sample does not show; snippet incomplete | Fixed wording, suggested single-colour scale, added note on count columns, snippet runnable |
| 41 | Snippet had no data setup; mean/median not printed | Added series and printed output |
| 42 | "Analytics pane > Target line" may not exist | Changed to Constant line, unverified label |
| 43 | "File > Save as > Power BI template" | "File > Export > Power BI template (.pbit)", unverified label |

## Ordering and duplicates (report only)
- Stars descend (3 to 2 to 1) and within each star group colours run green to yellow to red; numbering Q1-Q47 continuous. Header says Target 45 / Actual 47, consistent.
- Overlap with other parts: Q21/Q23/Q42 (target vs actual, conditional formatting, gauges) and Q27/Q28 (drill-through, mobile layout) likely overlap with Part 9 and possibly earlier visual parts; Q10 pie charts, Q16 3D and Q35 data-ink overlap each other within this part by design (cross-referenced).

## Unresolved / left unverified
- All Power BI menu paths, Desktop-only / Windows-only claims (Q26), licensing statements (Q5, Q9, Q28, Q43), sparkline release year (Q33), Top N and waterfall behaviour (Q38, Q39), and "no 3D chart or histogram built in" (Q16, Q41) remain labelled "from memory, unverified"; none could be fetched.
- Third-party figures (4.5:1 contrast, about 8% of men colour-blind, Microsoft's "fewer than eight pie categories") remain labelled unverified.
- Inconsistency noted: research/Book04_Part08_sources.md says the Microsoft Learn design-tips page was "fetched in full", while the answers say it was unreachable. Answers keep the conservative "unverified" labels; the sources file should be reconciled.
- "Asked at" claims (Vertiv/Dataford, Taggd PDF, eduyush, Al Rafay, Meesho) match the sources file; all others are "commonly asked", no company claims added.
