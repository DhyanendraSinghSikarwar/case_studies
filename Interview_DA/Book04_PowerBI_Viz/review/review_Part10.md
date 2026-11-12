# Review: Book 4 Part 10 (Tableau basics, Power BI vs Tableau)
Reviewer: Wave C. Environment: pandas 3.0.5 only; no Tableau, DAX engine or Microsoft/Tableau docs.

## Counts
- Answers checked: 43 of 43 (Q1-Q43). Template fields: all 9 core fields present in every answer (scripted check); all "DAX / Steps" fields carry "not run here".
- Pandas snippets run: 17 snippets across Q8, Q15, Q17, Q18, Q19, Q20, Q22, Q24, Q25, Q31, Q34, Q35, Q36, Q42, Q43 (Q13 reuses Q8). All 17 ran OK and matched the printed outputs and Results, except the items fixed below.
- Snippets added: 4 (Q23, Q32, Q37, Q43 extra line) and each was run.
- Answers fixed: 16 (Q4, Q8, Q13, Q15, Q17, Q22, Q23, Q24, Q25, Q26, Q32, Q36, Q37, Q39, Q42, Q43).
- DAX re-derived by hand on sample data: Q22 (FIXED 42000/100000/60000; INCLUDE South-only 95000), Q23, Q24, Q25 (2.02/1.03/2.60/1.58%), Q42. All match.

## Fixes
| Q | Wrong or missing | Fix |
|---|---|---|
| Q4 | "Pill" never defined; green "Month" example ambiguous (date part also folds years together) | Defined pill; added the two-kinds-of-Month note, labelled from memory |
| Q8 | "ATTR" used unexplained | Added one-line meaning |
| Q13 | Reference line "Average" on bars gives 38.9%, but text said 37.5% | Step 6 and bullets now explain 38.9 vs true company rate 37.5 (verified by pandas) and give a table-wide `{ AVG([Left Flag]) }` for the true rate; Result extended |
| Q15 | "Marks card" undefined | Defined |
| Q17 | pandas used column `Rev`, table says Revenue; Alternative suggested an INCLUDE LOD for Top N (not sound) | Comment added to snippet; Alternative now rank table calc or set; temporary-table claim labelled unverified |
| Q22 | Context-filter analogy via KEEPFILTERS was misleading; REMOVEFILTERS described as long-standing | Follow-up reworded (no direct equivalent); REMOVEFILTERS flagged newer, from memory |
| Q23 | Measure question lacked Sample data/Result/Pandas check | Added Jan example 6/198 = 3.03% with pandas line |
| Q24 | Printed tuple comment hid pandas 3 / NumPy 2 np.float64 wrappers | Comment now states values and the wrapper display |
| Q25 | Wrong menu ("Format > Analytics", "Model view mark Date table"); text month names cannot give a continuous axis | Corrected to Visualizations pane > Analytics > Constant line and Table tools > Mark as date table; added real-dates edge case |
| Q26 | "download the data" stated flatly | Labelled from memory, author can disable |
| Q32 | Modelling question without sample, result or pandas | Added 3-employee/5-leave sample; join gives 5 rows, avg 64 vs true 60 (run) |
| Q36 | DAX alternative said it "does not depend on layout" (it depends on filter context) | Reworded |
| Q37 | "Data > Create User Filter" (menu is under Server); no sample/pandas | Menu fixed and labelled from memory; added 6-row sample and pandas (b@co.com sees E3, E4, E5) |
| Q39 | Garbled "Tableau Cloud Server admin" | Reworded |
| Q42 | Result said "five different headcounts" (only 4 distinct values: 8, 7, 6, 5); measure named Headcount same as its table; last count (6) had no code | Fixed text; renamed measure Distinct Headcount; added pandas line for 6; added DISTINCTCOUNT vs nunique/COUNTD blank handling (from memory) |
| Q43 | `{ FIXED [Month] : SUM([Rev]) }` does NOT remove the fan-out (it still sums duplicated rows); "divide by a LOD count" vague | Replaced by `SUM({ FIXED [Sale] : MAX([Rev]) })` in Steps and Explain, with a pandas check giving 800 |

## Unresolved / for the editor
- Q13-Q17 etc. rely on Tableau order of operations from memory: placement of Sets and Top N relative to FIXED LODs is stated as "same stage as dimension filters" in Q16 and Q35 but Q10 notes sets as an early step. Consistent with the labelled unverified status, but should be checked on the Tableau Help page when reachable.
- Q15: Feb attrition is 1.995 unrounded and displays 2.00 (pandas rounds to 2.0); fine, noted only.
- Part has 43 questions vs target 40 (header already says so).

## Claims left unverified (labelled "from memory, unverified" in the text)
Desktop OS support (Power BI Windows-only, Tableau Windows and macOS), Tableau Public non-commercial and download behaviour, Tableau Cloud rename from Online, Relationships in 2020.2, Performance Recorder and Create User Filter menu paths, extract/context filter behaviour, order of operations, Power BI licence tiers and Premium viewer rules, Prep licensing, Bridge/gateway, COUNTD vs DISTINCTCOUNT blank handling, REMOVEFILTERS age, visual calculations. No prices or invented company claims found. "Asked at" claims (Wells Fargo Hyderabad Tableau topics, Indium, LatentView, Infosys Tableau/Power BI; Tableau 33% pooled n=186 and 12.5% = 5 of 40) check out against research/interview_processes.md and research/market_skills_2026.md.

## Other checks
- Ordering: stars descending (⭐⭐⭐ Q1-3, ⭐⭐ Q4-25, ⭐ Q26-43) and 🟢 then 🟡 then 🔴 within each; numbering continuous. No changes made.
- Overlap (report only): Q22/Q23/Q40 overlap with Power BI DAX parts on filter context and CALCULATE; Q27 and Q38 overlap with licensing/installation items likely in Parts 1-2; Q37 overlaps with the Power BI RLS question elsewhere in Book 4; Q43 overlaps with SQL join fan-out in Book 2.
- Markdown: 54 code fences, balanced; every table followed by a blank line.
