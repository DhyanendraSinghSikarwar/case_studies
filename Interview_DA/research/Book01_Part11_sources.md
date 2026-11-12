# Book 1 Part 11 sources (VBA basics, Copilot in Excel and Google Sheets)
Accessed 2026-10-21. 9 searches attempted (7 returned results, 2 hit rate limits and returned only model memory, which is NOT used as a source); 3 fetches (1 succeeded as Microsoft page in full, 1 succeeded for question headings, 2 returned 404). No first-hand Hyderabad/Bengaluru 2025-26 VBA interview transcripts were found; company claims are unverified. Sample size: a handful of snippets plus 72+32 JD rows from the repo's own research files.

| Source | URL | Used for | Type | Recency | Fetch status |
|---|---|---|---|---|---|
| Microsoft Support, COPILOT function | https://support.microsoft.com/en-us/excel/copilot-function | COPILOT function syntax; preview only; page says it is no longer available from 14 Sep 2026 and old cells return #NAME?; replaced by the Copilot pane | official | current (2026) | fetched in full |
| AnalysisTabs basic VBA questions | https://analysistabs.com/vba-interview-questions-answers/basics/ | typical basic VBA question headings (data types, scope, arrays, debugging, infinite loop) | prep blog | undated | fetched (headings only) |
| Naukri Code360 VBA questions | https://www.naukri.com/code360/library/vba-interview-questions | existence of fresher VBA lists | prep site | undated | search snippet only |
| Glassdoor/AmbitionBox/Naukri MIS Executive results (Springer Nature, Vilcart, Glassdoor MIS pages, Naukri MIS guide PDF) | https://www.ambitionbox.com/interviews/springer-nature-interview-questions/mis-executive ; https://www.ambitionbox.com/interviews/vilcart-interview-questions/mis-executive ; https://w10.naukri.com/mailers/2019/upload/sep/mis-executive-interview-guide.pdf | MIS interviews report basic VBA/macros questions ("VBA programming with practical", "Macro and VBA", simple VBA if-else) | candidate reports | some 2014/2019 | search snippet only, not fetched |
| Macro recorder tutorials (WallStreetMojo, TutorialsPoint) | https://wallstreetmojo.com/recording-macros-in-excel ; https://www.tutorialspoint.com/excel_macros/excel_macros_absolute_references.htm | absolute vs relative recording, Personal.xlsb, .xlsm, macro security | tutorials | older | search snippet only |
| VBA error-handling pages (MyOnlineTrainingHub, ExcelDemy) | https://www.myonlinetraininghub.com/?p=28597 ; https://exceldemy.com/?p=94635 | On Error Resume Next ignores rather than fixes errors; cleanup label restores ScreenUpdating | tutorials | undated | search snippet only |
| Google Docs Editors Help, Gemini in Sheets | https://support.google.com/docs/answer/13951830 | "Help me organize" builds new tables, cannot edit existing content; GEMINI() cell function per third-party guides | official (via snippet) | unknown | fetch returned 404; snippet only |
| Third-party Gemini in Sheets guides (numerous.ai, thebricks) | https://numerous.ai/blog/how-to-use-gemini-in-google-sheets | cell-level GEMINI() vs side panel; verify AI output | blogs | 2025 | snippet only |
| Repo: research/market_skills_2026.md, jd_sample_*.md | (local) | VBA 13% of JDs (24 of pooled sample), GenAI/AI tools 14-20%; VBA 40% in Amazon-heavy GCC sample; MIS JDs 18.8% | internal research | 2026 | read |

## Star reasoning
- VBA: only 13% of JDs overall (higher in MIS 19% and Amazon BA JDs 40%), so basic "what is a macro / have you used one" is rated ⭐⭐ (MIS interview reports and JD frequency); anything coding-specific is ⭐ (occasional).
- Copilot: "what is Copilot" and "how do you verify AI output" ⭐⭐ (AI tools named in 14-20% of JDs; verification is the standard interviewer follow-up); the rest ⭐.

## Gap-fills (not seen in any source as an interview question): about 14 of 21
Q7-Q8 recorder and security details come from tutorial snippets; Q9-Q10, Q12-Q21 are standard practice or JD-derived. Seen in sources (approx.): macro/VBA basics (Q1-Q4), error handling (Q16), data types/Option Explicit (Q9), Copilot function (Q18).

## Uncertain / for Wave B to verify
- COPILOT function retirement date (14 Sep 2026) taken from the Microsoft page text; Copilot licensing and Gemini plan names change often and were not verified (Microsoft page gave no licensing; search snippets of earlier versions conflict). Q12 and Q18 answers must cite the current Microsoft page.
- Office Scripts / Power Automate comparison searches were rate-limited; do not state details without verification.
- Glassdoor/AmbitionBox pages seen only as snippets; Reddit, Glassdoor not accessible via fetch.
