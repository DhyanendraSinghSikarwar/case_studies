# Book 13 Part 3 sources (inequalities, comparison, ranking, order and position puzzles)
Accessed 2026-11-26 via web search (snippet-level; no page fetched, WebFetch unavailable). 4 WebSearch calls issued, all returned result lists. Glassdoor, AmbitionBox, Reddit and LinkedIn pages were not fetched (Glassdoor appeared only as search-result links, content not read). No first-hand 2025-26 report of an inequality or ranking question asked to a data analyst was found. All question wording is written fresh; no source question was copied.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Placement-prep page "inequality questions placement" | https://placementprep.pages.dev/article/inequality-questions-placement | claim that inequalities appear in placement reasoning sections (TCS, Infosys, Wipro, Cognizant named; no formats given) | prep site | undated (snippet) |
| Testbook inequality reasoning | https://testbook.com/reasoning/inequality-reasoning | direct, coded, either-or types; decode symbols then solve; worked example P < S < R < T > Q gives no P-Q relation | prep site | undated (snippet) |
| Testbook coded inequality tips | https://testbook.com/blog/tips-to-solve-coded-inequality-in-reasoning | coded-inequality method (replace symbols, chain, check) | prep site | undated (snippet) |
| Unacademy coded inequality | https://unacademy.com/content/cat/study-material/data-interpretation-and-logical-reasoning/what-is-coded-inequality | coded inequalities and either-or noted as harder | prep site | undated (snippet) |
| IBPS/SATHEE coded inequalities theory | https://www.ibps.iitk.ac.in/sathee-bank-exam/bank-exams/ibps-po/study-materials/memory-based-questions/inequality/theory | symbol-decoding theory (bank-exam context, not analyst hiring) | exam-prep material | undated (snippet) |
| Unstop order and ranking | https://unstop.com/blog/order-and-ranking-explained | typical ranking variants: rank from top/bottom, total number, people between | prep site | undated (snippet) |
| Careers360 order and ranking | https://www.careers360.com/reasoning/order-and-ranking-topic-pge | question types and method (arrange data systematically) | prep site | undated (snippet) |
| PlacementPreparation order and ranking | https://www.placementpreparation.io/logical-reasoning/order-and-ranking/concepts/ | topic listed with "2025-2026 mock tests" label | prep site | 2025-2026 (snippet) |
| Mettl logical reasoning test | https://mettl.com/test/logical-reasoning-ability-test/ | lead only: pre-employment platform lists analyst roles for reasoning tests (not confirmed for DA) | assessment vendor | undated (snippet) |
| FACE Prep Mu Sigma aptitude / logical reasoning | https://faceprep.in/article/mu-sigma-aptitude-questions-for-mu-sigma-muapt-aptitude-test-2018/ | MuApt has quant, logical reasoning, verbal sections; no inequality or ranking item confirmed | prep site | 2018 (snippet) |
| PrepInsta Mu Sigma logical reasoning | https://prepinsta.com/?p=158105 | listed topics: statements and conclusions, seating, blood relations; inequalities/ranking not listed | prep site | undated (snippet) |
| Fractal aptitude guide | https://placementpapers.app/fractal/aptitude-questions/ | Fractal test has reasoning section; site says its items are practice-style, not leaked papers | prep site | undated (snippet) |
| FACE Prep / PrepInsta Cognizant reasoning | https://www.faceprep.in/article/cognizant-logical-reasoning-questions-with-answers/ | Cognizant reasoning module (AMCAT) per FACE Prep; PrepInsta says logical reasoning is no longer in GenC (sources conflict) | prep sites | 2025-2026 (snippets) |
| FACE Prep Capgemini reasoning | https://www.faceprep.in/article/capgemini-logical-reasoning-questions-with-answers/ | one source says Capgemini moved to game-based aptitude; another lists puzzle-solving (conflict) | prep site | 2026 (snippet) |
| research/interview_processes.md (local) | (local) | aptitude gates at service MNCs and analytics firms | earlier research notes | Nov 2026 |

Star-assignment reasoning (judgement, not measured frequency)
- 3 stars: direct inequality conclusions, coded inequalities, rank-from-top/bottom arithmetic, simple comparison and order puzzles. These are the staple items in every generic placement reasoning list found; the one page tying inequalities to TCS, Infosys, Wipro and Cognizant gives no format or frequency.
- 2 stars: either-or cases, ranges of rank, tie handling, Borda-type aggregation, rearrangement counts, multi-clue order puzzles (7-8 items, exactly-two-true statements). Plausible in online assessments but no source places them in a specific gate.
- 1 star: counting possible orders and minimum-comparison questions. They are differentiators for analytics-firm puzzle rounds; no source confirms them.

Limitations
- 4 searches, all commercial prep sites; no official test-maker material. No source confirms inequality or ranking questions in Mu Sigma, Fractal, Capgemini or Cognizant 2025-26 tests; test patterns conflict and none is used as a claim in the questions.
- All 51 questions are original constructions on topics the sources name; all are gap-fills at question level. Only topic coverage and star levels trace to sources.
- Every numeric and puzzle item was either computed by hand or checked in Python (inequality conclusions by enumeration of integer assignments; order puzzles by full permutation search) to have a unique answer to the question asked. Minimum-comparison answers (15, 10, 9) rely on known results (n-1; ceil(3n/2)-2; n + ceil(log2 n) - 2) not re-derived by code.
