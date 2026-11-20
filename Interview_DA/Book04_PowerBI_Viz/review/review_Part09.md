# Review: Book 4 Part 9 (Q1-Q70), Wave C

## Counts
- Answers checked: 70 (all read in full).
- Pandas snippets: 42 in the part. 34 self-contained ones were run as written (pandas 3.0.5), all OK, printed output matches the answer and its Result. 8 (Q6, Q9, Q12, Q13, Q14, Q15, Q16, Q23) use pre-defined frames; I rebuilt the frames from the sample tables and ran them: all OK. 4 new snippets added (Q10, Q43, Q44, Q50) and run OK.
- Every DAX result was re-derived by hand on the sample data (Q6, Q13, Q25-Q29, Q39-Q42, Q47, Q58-Q61, Q67, Q69): all agree with the Results.
- Answers fixed: 26 (Q3, Q10, Q13, Q14, Q21, Q33, Q34, Q36, Q37, Q42, Q43, Q44, Q46, Q47, Q48, Q50, Q51, Q52, Q57, Q58, Q59, Q61, Q63, Q65, Q68, Q69).
- Markdown: fences balanced, every table followed by a blank line, 70 headings untouched.

## Fixes
| Q | Wrong | Fix |
|---|---|---|
| Q13 | Example said Offered-to-Joined (80%) was the "weakest" stage; it is the strongest (lowest is Interviewed to Offered, 30%) | Example rewritten; edge case added: total row of `% of Previous Stage` compares with stage 4 |
| Q14 | `[Total Sales]` used but never defined | Definition added |
| Q21 | "Last refreshed" via DateTime.LocalNow() would show UTC in the Service | Caveat added, labelled from memory |
| Q3, Q46 | Missing "DAX / Steps" field | Added ("not applicable" / start click-path) |
| Q10 | Modelling answer lacked Result and Pandas check | Added and run (Electronics 9,000, Furniture 3,000) |
| Q33 | Measure `[Sales]` had the same name as table Sales (confusing) | Renamed `Total Sales` |
| Q34 | Premise muddled: with no relationship nothing multiplies; inflation comes from a flat merge or many-to-many | Premise-check bullet added |
| Q36 | `FORMAT(..., "YYYY-MM")` risky; "without a date table TOTALYTD gives wrong results" overstated; "first rows" wording wrong; no Sample data | `"yyyy-MM"`; softened and labelled unverified; wording fixed; Sample data added |
| Q37 | No Sample data field | Added (dates and sales rows used by the pandas check) |
| Q42 | Measures `[Sales]`, `[Profit]`, `[Quantity]` undefined and clash with column names | Replaced by `Total Sales/Profit/Quantity` with definitions |
| Q43, Q44 | Transformation answers lacked Sample data, Result, Pandas check | Added and run |
| Q47 | DAX used `AppliedDate`/`JoinedDate`, sample has `Applied`/`Joined` | DAX aligned to sample; apology note removed |
| Q48 | M comment said Table.Distinct keeps the "last" row; it keeps the first | Comment corrected (sort descending and buffer for newest-wins) |
| Q50 | No Sample data / Pandas check; measures undefined | Added sample line, one-line arithmetic check, note on placeholder measures |
| Q52 | Curly quotes in `DATEADD(‘Date’[Date]...)` (syntax error); sample has no date column | Straight quotes; caveat added |
| Q57 | "Hike %[Hike % Value]" garbled | Reworded, labelled from memory |
| Q58 | `[Total Sales]` summed `Sales[Amount]`, but sample table is `Products[Sales]`; float-comparison risk | Measure fixed; edge case added |
| Q59 | Customers table assumed but not stated | Assumptions stated in code comment |
| Q61 | DAX tested `LeaveDate = BLANK()`; sample column is `Left` (Yes/No) | DAX now `Employees[Left] = "No"` |
| Q63 | Cited "research notes" to a reader | Replaced with "from memory, unverified" |
| Q65, Q51 | "Asked at" said Cognizant and Deloitte RLS; interview_processes.md has Deloitte Sept 2025 and an older (2022) Cognizant report | Wording made exact |
| Q68 | "Native query blocks later folding" too absolute | Softened, labelled unverified |
| Q69 | Sample columns `Join/Leave` vs DAX `JoinDate/LeaveDate` | Sample headers renamed |

## Unresolved / report only
- Ordering: stars descending then green, yellow, red holds in all groups; numbering Q1-Q70 continuous (unchanged).
- Overlap with other parts (not checked line by line, only by topic): Q14/Q67 Top N; Q36/Q37 date tables, fiscal year; Q43/Q48 folder combine; Q49/Q68/Q70 optimisation; Q51/Q65 RLS/OLS; Q60 vs Q27/Q6 hires and leavers. Likely overlap with Parts 1-8; deduplication was done at Wave A, left as is.
- Q7, Q49, Q68, Q70 cite "research notes" for Performance Analyzer in the Service and incremental refresh folding. The sources file records those pages as fetched in Wave A; not re-verifiable now.
- Many pandas snippets in Q6-Q23 depend on a frame defined only in the sample table (not self-contained); left as is.
- Q51/Q27 minor: variable names MS/ME and boolean `NOT ISBLANK(col)` as a CALCULATE filter look valid but are untested.

## Claims left unverified (no DAX engine, learn.microsoft.com unreachable)
All DAX/M/click-path "not run here". From memory, unverified, and consistently labelled: Desktop Windows-only (Q1, Q20, Q52), Pro/Premium/PPU licence rules and refresh counts (Q19, Q45), Mac options, DISTINCTCOUNT counting a blank as a value (Q29), Table.Distinct keeps first row after buffered sort (Q29, Q48), TOTALYTD year-end string format (Q37), field parameter and What-if menu names (Q42, Q57), RLS roles that bypass RLS, OLS via Tabular Editor (Q51, Q65), paginated report capacity needs (Q66), alert tile types (Q56), folding breakers (Q68), "Keep all filters" (Q63), DateTime.LocalNow in the Service (Q21). No company claim added; "Asked at" limited to Deloitte (Q7, Q51, Q65) and Cognizant 2022 (Q51, Q65).
