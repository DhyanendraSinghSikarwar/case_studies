# Book 1 Part 6 sources (dynamic arrays: FILTER, UNIQUE, SORT, LET)
Accessed 2026-10-21. 9 web searches run (2 of them returned a rate-limit error and were retried once as a differently worded search; 1 of the retries succeeded) and 9 fetches attempted (5 fetched in full or in useful part, 2 returned HTTP 404, 1 partly read, 1 page body truncated). No first-hand Hyderabad/Bengaluru interview report naming FILTER/UNIQUE/LET was found. Company attributions: none made.

| Source | URL | Used for | Type | Recency | Fetch status |
|---|---|---|---|---|---|
| Microsoft Support: FILTER | https://support.microsoft.com/en-us/office/filter-function-f4f7cb66-82eb-4767-8f7c-4877ad80c759 | syntax, if_empty, #CALC! when no match, availability (365, 2024, 2021) | official docs | current | fetched (summarised by tool) |
| Microsoft Support: LET | https://support.microsoft.com/en-us/office/let-function-34842dd8-b92b-4d3f-b325-b8b8f9908999 | syntax, 126 pairs, naming rules, availability | official docs | current | fetched |
| Microsoft Support: UNIQUE | https://support.microsoft.com/en-us/office/unique-function-c5ab87fd-30a3-4ce9-9d1a-40204fb85e1e | by_col, exactly_once, examples; case sensitivity NOT stated | official docs | current | fetched |
| Microsoft Support: dynamic arrays and spilled array behaviour | https://support.microsoft.com/en-us/office/dynamic-array-formulas-and-spilled-array-behavior-205c6b06-03ba-4151-89a1-87a7eb36e531 | legacy CSE arrays, no spills inside Tables, closed-workbook #REF! | official docs | current | fetched |
| Exceljet: dynamic array formulas | https://exceljet.net/dynamic-array-formulas-in-excel | spill range, # operator, @, 8 new functions, 2021+/365 only | training site | undated | fetched |
| Microsoft Support: SORTBY, #SPILL! fix page | (two URLs guessed) | intended for SORT vs SORTBY and #SPILL! causes | official docs | n/a | HTTP 404, NOT used; #SPILL! causes and SORTBY details come from search-tool summaries and general knowledge (unverified) |
| ICAEW: dynamic arrays Google Sheets vs Excel | https://www.icaew.com/technical/technology/excel-community/excel-community-articles/2020/dynamic-arrays-google-sheets-vs-excel | Sheets vs Excel (QUERY, ARRAYFORMULA, # operator, tables) | professional body article | 2020 | search snippet only; body truncated on fetch |
| BetterSheets: Excel dynamic arrays vs Sheets | https://bettersheets.co/explained/dynamic-arrays-excel | ARRAYFORMULA role | blog | undated | snippet only |
| SpreadsheetWeb: same formula, different result | https://spreadsheetweb.com/excel-google-sheets-same-formula-different-result/ | FILTER/SORT conversion to Sheets | blog | undated | snippet only |
| ModelMonkey: spilled arrays not supported in tables | https://modelmonkey.io/blog/excel-spilled-array-formulas-not-supported-in-tables | Table limitation (confirmed by Microsoft page) | blog | undated | snippet only |
| XelPlus: availability of Excel dynamic arrays | https://courses.xelplus.com/courses/580829/lectures/10442640 | not in 2010-2019 | training site | undated | snippet only |
| Microsoft Tech Community: FILTER not in Office 2019 | https://techcommunity.microsoft.com/discussions/excelgeneral/i-cant-find-filter-function-in-office-2019/1442317/replies/1445546 | 2019 lacks FILTER | forum | ~2020 | snippet only |
| Telegram excel_analyst: Excel interview Q&A part 6 | https://t.me/s/excel_analyst/2102 | FILTER/SORT/UNIQUE appear in community interview lists | community channel | undated | snippet only |
| Scribd: data analyst Excel interview questions | https://www.scribd.com/document/900660747/Data-analyst-excel-interview-questions | advanced sets focus on dynamic arrays | user upload | undated | snippet only |
| Scribd: Excel interview FAQs | https://www.scribd.com/document/866454332/Excel-Interview-FAQS | XLOOKUP/dynamic arrays in lists | user upload | undated | snippet only |
| ZetCode / Ablebits / ExcelUser LET tutorials | https://www.ablebits.com/office-addins-blog/let-function-formula-examples | LET calculates a repeated expression once | tutorials | undated | search listing only |
| Phase 0: market_skills_2026.md, jd_sample_*.md, interview_processes.md | research/ (local) | Excel is a must-have (60% of JDs); Google Sheets 10%; no JD named FILTER/UNIQUE/dynamic arrays; Excel interview evidence from about 5 profiles (Novartis case, Accenture, Meesho MCQs, Infosys) | internal | Oct 2026 | read via grep |

## Star reasoning
- Basic questions on FILTER/UNIQUE/spill/versions get 3 stars: they are the core of this topic and the Excel evidence is that every Excel-listed JD (60%) can lead to them, but note no source directly shows frequency. Stars here are judgement, not measured: JD samples never name dynamic arrays; community lists (Telegram, Scribd) mention FILTER/SORT/UNIQUE and XLOOKUP as an "advanced" set. For that reason I did not give more than 6 questions three stars (the base is the same as for any entry-level Excel function topic: 0-3 year interviews usually test VLOOKUP/pivots first).
- Two stars: multi-condition FILTER, SORT/SORTBY, LET basics, # operator, practical HR tasks (common live-test formats).
- One star: Google Sheets differences, hard scenarios, backwards compatibility, edge cases.

## Limitations
- Sample: 9 searches, mostly generic prep sites; nothing city- or company-specific. Glassdoor/AmbitionBox/Reddit were not surfaced or fetched.
- Microsoft SORTBY and #SPILL! pages returned 404; claims on SORTBY and #SPILL! causes are standard knowledge, to be verified in the answer phase.
- Unverified: TAKE/CHOOSECOLS/HSTACK (365 only; the answer phase for the top-5, selected-columns and top-per-department questions should state this and show an INDEX/SEQUENCE fallback); UNIQUE case-insensitivity (the 'HR vs hr' question; general knowledge, to test in Excel); Excel 2024 availability stated by Microsoft page for FILTER/LET.

## Gap-fills (not seen in any source)
Questions drawn from standard practice, not from a source: nearly all the practical ones (about 33 of 45). Directly supported by a source: the questions on dynamic arrays/spill, FILTER, UNIQUE, versions, #SPILL! (partly), SORT, LET, exactly_once, #, @, Tables, legacy arrays, if_empty, function list, Sheets, closed workbook (Microsoft/Exceljet/ICAEW/Telegram lists). Approximate count: 34 gap-fills.
