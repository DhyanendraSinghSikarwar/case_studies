# Book 1 Part 2 sources (core functions: IF, AND/OR, COUNTIF(S), SUMIF(S), text and date functions)
Accessed 2026-10-21. 8 web searches attempted (6 returned results, 2 hit a rate limit and were re-run with different wording); 6 official/guide pages fetched. Sample is small: results were snippet-level summaries from the search tool, and no first-hand Hyderabad/Bengaluru 2025-26 interview report was found. Company-specific attributions are therefore not made anywhere in this part.

| Source | URL | Used for | Type | Recency | Fetched? |
|---|---|---|---|---|---|
| Microsoft Support: COUNTIFS | https://support.microsoft.com/en-us/office/countifs-function-dda3dc6e-f74e-4aee-88bc-aa8c2a866842 | syntax, 127 pairs, equal-size ranges, wildcards ?, *, ~, availability 2016 to 365 | official docs | current | fetched in full |
| Microsoft Support: IFS | https://support.microsoft.com/en-us/office/ifs-function-36329a26-37b2-467c-972b-4a39bd951d45 | IFS syntax, TRUE default, #N/A, availability Excel 2019+ (not 2016) | official docs | current | fetched in full |
| Microsoft Support: DATEDIF | https://support.microsoft.com/en-us/office/datedif-function-25dba1a4-2812-480b-84dd-8b32a451b35c | units Y, M, D, MD, YM, YD; MD bug; #NUM! | official docs | current | fetched in full |
| Microsoft Support: TEXTJOIN | https://support.microsoft.com/en-us/office/textjoin-function-357b449a-ec91-49d0-80c3-0e8fc845691c | syntax, availability 2019+ | official docs | current | fetched in full |
| Microsoft Support: NETWORKDAYS | https://support.microsoft.com/en-us/office/networkdays-function-48e717bf-a7a3-495f-969e-5005e3eb18e7 | holidays argument, #VALUE!, NETWORKDAYS.INTL pointer | official docs | current | fetched in full |
| Guru99 Excel formulas interview questions | https://www.guru99.com/excel-formulas-interview-questions.html | topic list: SUMIF, COUNTIF, CONCATENATE, IF, MAX/MIN | prep blog | 2026 per title | fetched in full |
| Glassdoor MIS interview pages (search results) | https://clear.glassdoor.nl/Interview/mis-interview-questions-SRCH_KO0,3_IP50.htm and https://static-pc.glassdoor.fr/Interview/mis-interview-questions-SRCH_KO0,3_IP54.htm | candidate-reported: nested IF for grades, COUNTIF vs COUNTIFS, SUMIF vs SUMIFS, attrition, SUMIF/COUNTIF/IF scenarios, "explain every formula you used" | candidate reports | undated | search snippet only; page not fetched |
| Glassdoor MIS analyst/intern pages (search results) | https://static.glassdoor.fr/Interview/mis-analyst-interview-questions-SRCH_KO0,11_IP58.htm | Google Sheets ARRAYFORMULA/QUERY/IMPORTRANGE mentions; COUNTIFS/SUMIFS test | candidate reports | undated | search snippet only |
| Careers360 Excel and MIS questions | https://www.careers360.com/courses-certifications/articles/excel-interview-questions-and-answers | general Excel question lists | prep blog | 2025 | search snippet only |
| Towards Data Science: Excel for BI/DA at FAANG | https://towardsdatascience.com/how-to-ace-technical-interviews-excel-for-business-intelligence-engineer-data-analyst-at-faang-8b5b0788e4ea/ | COUNTIF / COUNTIFS practice framing | blog | undated | search snippet only |
| Exceljet: count cells that contain errors | https://exceljet.net/formula/count-cells-that-contain-errors | SUMPRODUCT(--ISERROR()) pattern | tutorial | undated | search snippet only |
| Microsoft Support: IFERROR | https://support.microsoft.com/en-US/Excel/iferror-function | error types covered; IFNA as narrower option via bettersolutions snippet | official docs | current | search snippet only |
| Chandoo forum: SUMPRODUCT and #N/A | https://chandoo.org/forum/threads/sumproduct-n-a.12403 | SUMPRODUCT fails if range holds errors | forum | undated | search snippet only |
| LinkedIn HR-formula posts; Maven Analytics HR attrition project | https://mavenanalytics.io/project/14358 | HR flavour (COUNTIF absent, DATEDIF tenure, attrition dashboard) | social/project | undated | search snippet only |
| PCWorld / open-exam-prep date function pages | https://www.pcworld.com/article/410499/excel-date-time-functions-tutorial-edate-yearfrac-eomonth-networkdaysintl.html | EDATE, EOMONTH, NETWORKDAYS, WORKDAY, serial numbers | tutorials | undated | search snippet only |
| JD samples in this repo | research/jd_sample_*.md and market_skills_2026.md | Excel in 60% of 0-2 yr JDs; MIS roles (Tata Play Fiber, TMI, Tya, Udaan, EXL) | repo research | Oct 2026 | read locally |

## Star reasoning
- Three stars: IF, nested IF, AND/OR, COUNTIF(S), SUMIF(S), COUNTIF vs COUNTIFS, SUMIF vs SUMIFS and attrition appear repeatedly in MIS/DA candidate reports and every prep list seen, and Excel is the top JD tool (60%). Basic text (LEFT/RIGHT/&), TODAY, DATEDIF tenure and IFERROR are in every fundamentals list.
- Two stars: other text/date functions, error types, AVERAGEIF, IFS, NETWORKDAYS/EDATE/EOMONTH, wildcards, SUMPRODUCT: common but listed less consistently.
- One star: version/Google Sheets differences, newer 365 text functions, edge cases (DATEDIF MD, 15-digit matching, 255-character limit), differentiators.

## Notes and limitations
- Source-seen (topic appeared in at least a snippet): 33 questions. Gap-fills (standard practice, not seen in any source): 43.
- Blocked or not surfaced: Glassdoor/AmbitionBox pages were visible only as search snippets (not fetched); Reddit and AmbitionBox gave no results. Two searches were rate-limited and were retried.
- Unverified from my sources, written from general knowledge: attrition formula (leavers / average headcount), COUNTIF 255-character limit, COUNTIF treating 16+ digit numbers as text-matched at 15 digits, MAXIFS availability (2019+), TEXTBEFORE/TEXTSPLIT availability (365). Answer writers must verify these against Microsoft Support before freezing answers.
- The Google Sheets COUNTIFS/SUMIFS comparison question rests only on an ARRAYFORMULA snippet; verify against Google Docs Editors Help.
