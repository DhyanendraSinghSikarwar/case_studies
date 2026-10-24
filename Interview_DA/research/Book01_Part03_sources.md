# Book 1 Part 3 sources (Lookups: VLOOKUP, HLOOKUP, INDEX-MATCH, XLOOKUP)
Accessed 2026-10-21 via WebSearch (6 searches returned results, 1 further search failed with a rate-limit error) and WebFetch (2 Microsoft pages fetched). No first-hand Hyderabad/Bengaluru 2025-26 interview reports were found; company-specific attributions are not made. Sample size: about 40 distinct result links seen, 2 pages fetched (answered via a summarising fetch tool, not read verbatim). Limitation: most search results were snippet-level summaries of commercial prep blogs; the 2026-specific hiring picture is inferred from JD files, not from interview reports.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Microsoft: XLOOKUP function | https://support.microsoft.com/en-au/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929 | Syntax, if_not_found, match_mode (0/-1/1/2), search_mode (1/-1/2/-2), multi-column return, version note (not in 2016/2019; page's own list conflicts) | official docs | fetched in full (via summariser), undated |
| Microsoft: VLOOKUP function | https://support.microsoft.com/en-us/office/vlookup-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1 | range_lookup default approximate, leftmost-column rule, #N/A and #REF! causes, text/number and space problems | official docs | fetched in full (via summariser), undated |
| DataCamp XLOOKUP vs VLOOKUP | https://www.datacamp.com/tutorial/xlookup-vs-vlookup | Exact-vs-approximate default, left lookup, if_not_found, multi-column return | tutorial | snippet-level (search summary only), undated |
| GoodSpace Excel interview questions | https://goodspace.ai/interview-questions/excel | VLOOKUP limits, INDEX-MATCH as fix for column insertion, XLOOKUP basics | prep site | snippet-level, undated |
| WallStreetMojo Excel interview questions | https://new.wallstreetmojo.com/excel-interview-questions/ | Lookup questions appear in standard lists | prep site | snippet-level, undated |
| x0pa MIS executive interview questions | https://x0pa.com/hiring/mis-executive-interview-questions/ | MIS list includes VLOOKUP, its limits, INDEX-MATCH, RANK | hiring guide | snippet-level, undated |
| Exceljet two-way approximate match multiple criteria | https://exceljet.net/formula/two-way-approximate-match-multiple-criteria | Two-way INDEX/MATCH pattern | reference | snippet-level, undated |
| Ablebits INDEX MATCH multiple criteria | https://www.ablebits.com/office-addins-blog/excel-index-match-multiple-criteria-formula-examples/ | Array formula and helper-column patterns | reference | snippet-level, undated |
| Microsoft Tech Community lookup multiple criteria | https://techcommunity.microsoft.com/discussions/excelgeneral/excel-lookup-function-multiple-criteria/216089 | Concatenated helper key | forum | snippet-level, undated |
| Spreadsheet Planet / Trump Excel HLOOKUP pages | https://spreadsheetplanet.com/excel-functions/hlookup/ | HLOOKUP use case, top-row limitation | tutorial | snippet-level, undated |
| JD samples (internal) | research/jd_sample_hyderabad.md, research/jd_sample_mis_people.md | Ninjacart MIS (VLOOKUP, Hyderabad), Tata Advanced Systems (VLOOKUP, Bengaluru), Vee Technologies (INDEX-MATCH, Bengaluru) | JD | as in those files |

Star reasoning
- ⭐⭐⭐: VLOOKUP syntax, exact vs approximate, #N/A, limitations, VLOOKUP vs INDEX-MATCH vs XLOOKUP, left lookup, column-insertion breakage: appear in every prep list seen and in the MIS JDs naming VLOOKUP/INDEX-MATCH.
- ⭐⭐: HLOOKUP, slabs via approximate match, two-way and multi-criteria lookups, IFERROR vs IFNA, XLOOKUP arguments: common in lists but less universal.
- ⭐: wildcard-heavy, CHOOSE, INDIRECT, LOOKUP trick, binary search, case-sensitive, Google Sheets differences: differentiators; no source reported them as frequently asked.

Notes
- Gap-fills (not seen in any source, added from standard practice and the part brief): about 30 of 60, including most HR-flavoured scenarios (attendance, payroll, attrition), #SPILL!, XMATCH, structured references, return-0-for-blank, INDIRECT, CHOOSE, LOOKUP trick, Google Sheets, nth match, replace-all-VLOOKUPs.
- Unverified: Google Sheets support for XLOOKUP and INDEX-MATCH (question asks it; to be verified in Wave B from Google docs); XLOOKUP availability in Excel 2021 vs 2016/2019 per Microsoft's own note (the page's applies-to list conflicts).
- Not accessible/no result: Glassdoor, AmbitionBox, Reddit, GfG interview-experience pages (not surfaced; not fetched). The company-experience search (Accenture/Infosys/Novartis/Meesho) failed with a rate-limit error and was not retried with results.
