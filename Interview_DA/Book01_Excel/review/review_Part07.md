# Wave C review: Book 1 Part 7 (Power Query and Power Pivot)
Reviewed 2026-10-22. File: Book01_Excel/Book01_Part07.md (64 answers, Q1-Q64).

## Counts
- Answers checked: 64. Answers edited: 21 (Q1-Q64 headings, numbers, stars, order untouched).
- Runnable formulas re-executed with tools/xl_eval.py (LibreOffice 24.2): 6 values, all matching the printed Result: Q46 VLOOKUP C2:C5 = 50000, 60000, missing, missing; Q52 SUMPRODUCT 119500 and SUM*SUM 360000.
- pandas replicas re-run and matching the printed values: Q3, Q7, Q10, Q11-Q17, Q21, Q23, Q24, Q26, Q29-Q31, Q34, Q35, Q42 (Jaccard 0.67/0.23/0.0), Q43-Q45, Q49-Q57. No wrong numbers found.
- Everything else (Power Query, DAX, pivots, slicers, KPIs) is correctly labelled "not run here"; expected values checked by pandas or by hand (Q50 running total, Q51-Q54, Q55 1.005, Q57 66.7/66.7/28.6/50.0, 2.01%).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q1,Q8,Q25,Q39,Q44,Q46,Q48,Q62 | Cited page title "Where is Get & Transform (Power Query)" no longer matches the fetched title | Replaced by "Power Query data sources in Excel versions"; Q8 explains same article ID e9332067 |
| Q3 | "Default join: Left Outer" contradicted Microsoft's fetched Merge page | Now says Microsoft says inner, Left Outer usual, see Q26 |
| Q8 | Fuzzy merge in 2016 not stated | Added pointer to Q42 |
| Q16, Q60 | Claimed M null comparison result as fact | Labelled "from memory, unverified" |
| Q17, Q21 | Example data behind totals not shown | Listed the six employees / salaries |
| Q19 | Power Pivot edition/Mac claim unresolved | Added fetched "Turn on Power Pivot" facts (no Mac, no web, desktop yes); edition list stays unverified (snippet only); follow-up on Mac answered |
| Q23 | "5 rows" Skills x Projects without data | Added data (a,a,b x a,a,b = 5) |
| Q25 | Version note missing page | Added Unpivot page Applies-to (365, 2024, 2021) |
| Q26 | "six main kinds" then listed seven; default-join conflict vague; "Net" column not in sample | "seven kinds"; conflict stated with fetched Merge page quote; Left Outer preselect labelled from memory; wording fixed |
| Q31 | Sample sheet had no data; "Salary 1 and 4" unclear | Added 6-row sample, result Salary 50 and 60 |
| Q41 | Unpivot folding wording | Now says both Microsoft pages are silent |
| Q42 | 2016 fuzzy support unverified | Quoted "More features were added to 2019 perpetual than ... 2016 perpetual"; still unverified |
| Q46 | No Excel-vs-LibreOffice note; XLOOKUP conflict not stated | Added both |
| Q52 | Said SUMPRODUCT "can be run" | Actually run: 119500 and 360000 |
| Q57 | Closing headcount not in sample | Stated assumption (no joiners) |
| Q59 | 250 MB vs 10 MB conflict | Stated which page was re-read and that 10 MB was seen only in a search summary |

## Newly verified from fetched pages (2026-10-22)
- "About Power Query in Excel": import/connect then shape; refresh brings additions, changes, deletes (Q1, Q4).
- "Merge queries (Power Query)" (applies 365, 365 Mac, 2024, 2021): default join is inner; seven join kinds (Q26).
- "Turn on Power Pivot": not on Mac or web; desktop yes (Q19).
- "Data Model specification and limits" (applies 365, 2024, 2021): 250 MB for Excel for the web; SharePoint 2013 50 MB upload / 10 MB rendering; no 32/64-bit memory figures (Q59).
- "Power Query data sources in Excel versions": fuzzy merge in 365 not 2019 perpetual; Data Model refresh not yet supported in Excel for the web (Q42, Q62).
- "Refresh an external data connection in Excel", "Import data from a folder with multiple files (Power Query)", "Unpivot columns (Power Query)", "Handling data source errors (Power Query)", "Create a relationship between tables in Excel", "How Power Query and Power Pivot work together" (incl. Data Model refresh not supported in SharePoint): quoted claims in Q4, Q6, Q21-Q23, Q43, Q47, Q58, Q62, Q63 confirmed.
- Microsoft Learn "Understanding Query Evaluation and Query Folding in Power Query": M script, Advanced Editor, folding outcomes, CSV/Excel do not fold (Q38, Q41).
- XLOOKUP (Q46): added the known Microsoft conflict sentence (page note vs Applies-to list); treated as 2021/365. Not re-fetched here.

## Still unverified
- Power Pivot availability by Office edition (Home & Student, Professional 2016, Wikipedia's April 2018 claim); the "What versions of Office include Power Pivot?" page redirects to the overview.
- Whether Unpivot folds on SQL sources (neither Microsoft page says).
- Fuzzy merge in Excel 2016; Left Outer as the preselected join kind; the 10 MB SharePoint Online figure.
- All Google Sheets and Power BI statements, M null comparison, IFS 2019+, Trim/Clean/case-sensitivity of M, "Mark as Date Table" menu name.
- Pages cited but not re-fetched: Create a Data Model in Excel; Relationships between tables in a Data Model; Measures/KPIs/Dates in Power Pivot; Create a parameter query; Use slicers; Pivot columns; Use multiple tables; Fuzzy match; Behind the scenes of the Data Privacy Firewall.

## Unresolved / report only
- "Asked at" lines are consistent with the sources file (only EY/Mphasis snippets and repo research); no company claims added.
- Q17, Q36, Q37 and Q31 results are pandas on described data; fine but thin on sample grids.
- Numbering: 64 answers vs target 60 (stated in header); no duplicates found. Q3 and Q26 overlap on join kinds by design.
- Markdown: fences balanced; every table followed by a blank line.
