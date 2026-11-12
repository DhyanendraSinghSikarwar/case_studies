## Section 3 - Interview process by company type (with reliability caveats)

### 3.0 Read this first: how reliable is this section?

Nobody publishes an official interview structure for data analyst roles. Everything below is what anonymous candidates said happened to them. Treat it as a map drawn from travellers' notes, not a timetable.

- **Candidate-reported, anonymous.** Reports span 2009 to 2026. Dates are given where known. (IP Section 1)
- **Blocked sources.** Glassdoor and AmbitionBox pages could not be opened by the researcher; Glassdoor content comes only from search-tool summaries of the pages. Reddit, LinkedIn and YouTube gave no evidence at all. (IP Section 1)
- **Few pages read in full.** Only about 9 pages were read directly. Everything else is a summary of a page or a third-party prep guide. (IP Section 1)
- **Anecdote rule.** A pattern backed by fewer than 3 independent sources is called an "anecdote" here. (IP Section 1)
- **Campus versus lateral.** Many reports are campus-drive reports. You are a lateral/switcher candidate, so the process you meet may differ. (IP Section 1)
- **Location.** Hyderabad and Bengaluru evidence is weak; many reports come from Chennai, Pune, Noida, Mumbai or an unstated city. (IP Section 1)

**Labels used in this guide:**

| Label | Meaning |
|---|---|
| [R] | The researcher read the page |
| [S] | Search-tool summary of a page that could not be opened; wording unverified |
| [G] | Third-party prep guide (InterviewQuery, Dataford, Hyring, FACE Prep and similar), not evidence of company policy |
| anecdote | Fewer than 3 independent sources |
| unverified | Single weak source or none |

**Do this before every interview:** ask the recruiter, in writing, "How many rounds are there, what does each one test, and how long is each?" Recruiters usually answer. That answer beats everything in this section.

### 3.1 Service MNCs (TCS, Infosys, Accenture, Deloitte USI, Cognizant, Wipro)

Reported shape: 2 to 4 rounds. Usually an online aptitude/assessment, a technical interview, sometimes a managerial/project round, then HR. (IP 2.1)

| Company | What was reported | Label |
|---|---|---|
| TCS | A guide says 3 rounds (technical, managerial, HR), driven by your resume. One Hyderabad review of an automated "bot-run" interview was for a data engineer role, not DA. | [G]; [S] |
| Infosys | Online assessment (aptitude plus basic analytics), then technical (SQL, Excel, Python, Power BI/Tableau, data interpretation, a case), then HR. A guide says 2-3 rounds. One Hyderabad review (interview March 2026) reports 4 rounds with a GenAI/LLM/RAG technical test; the role was not confirmed as DA. | [S]; [G]; anecdote (1 report) |
| Accenture India | Aptitude/cognitive test, a technical test, and an English communication assessment. A Bengaluru report describes an elimination round (verbal, logical, quant, core CS including databases, 1-2 coding problems) followed by a non-elimination English communication assessment. A January 2026 Bangalore-Rural report: aptitude, then technical on Python, SQL and basic statistics (INNER vs LEFT JOIN asked). A GfG DA post lists phone screen, technical (SQL, Excel, data scenarios), behavioural, case/technical, final, but gives no questions, location or date. | [G/S]; [S]; [R] |
| Deloitte USI (Hyderabad) | 2025-26 reviewers report 2 rounds: round 1 SQL (basics, window functions, duplicates, optimisation), round 2 Power BI (row-level security, optimisation, SUM vs SUMX) plus project workflow, with about a week's wait. A Nov 2025 analyst report: an aptitude-style first round, then a project explanation plus two medium-hard SQL questions, of which the candidate solved one. The 2021 campus process (GfG): a 75-minute AMCAT aptitude test, then one technical-cum-HR round described as easy; 36 of 103 shortlisted candidates were selected. | [S]; [S]; [R] (campus, 2021) |
| Cognizant (Hyderabad) | July 2025: two technical rounds (SQL, business analysis, stakeholder management) plus a casual HR round. A Feb 2025 report (role unstated): online communication round, MCQ plus coding with basic SQL, an in-person round focused on Java with two SQL questions, about 3 months in total. | [S]; [S] |
| Wipro | A guide says 3 rounds: online assessment (aptitude; sometimes coding), technical (SQL, analysis, Excel/Power BI, projects), HR. Candidate reports mention Power BI/DAX and SQL (joins, CTE, stored procedures) in Bangalore-Rural (2023) and joins/GROUP BY/HAVING in Noida (2025). One reviewer saw a technical round on ML and statistics (anecdote). | [G]; [S] |

**Pattern.** SQL basics, Power BI/DAX concepts, Excel, basic Python, a project walk-through, aptitude, then HR. Difficulty is mostly basic to medium; the Deloitte 2021 campus round was "easy" [R], and Accenture is rated "medium" by a Dataford aggregate (its claimed 58% offer rate comes from an unverified method, so do not rely on it) [G]. What interviewers were said to probe: resume and project depth (a 2015 Deloitte Hyderabad BI review said every point on the resume was probed [S]; the TCS guide says "resume-driven" [G]) and, at Accenture, English communication. No group discussion (GD) appears in any of these service-MNC sources. (IP 2.1)

**Timelines.** One week after round 2 (Deloitte, [S]); 1-2 weeks (TCS guide, [G]); 3 months (one Cognizant candidate, [S]). Accenture and Wipro timelines are not reliably stated. Treat all as unverified.

**GenAI.** One Infosys Hyderabad report (March 2026) is the only direct interview evidence. Call it "emerging, 1 report, not a pattern." (IP Section 4)

### 3.2 GCCs (global capability centres): Amazon, Wells Fargo, Novartis, HSBC, JPMorgan, Microsoft

| Company | What was reported | Reliability |
|---|---|---|
| Amazon (Bengaluru/Hyderabad; BA, BIE) | The most consistent GCC pattern. A LeetCode BA-II India post: 5 rounds, an SQL screen on a shared screen, then scenario and Leadership Principle (LP) rounds on Chime [S]. A GfG BIE Bangalore post (fresh graduate, early 2023): 5 rounds: online analytical/data-interpretation test, SQL plus data modelling, LP behavioural, a data-analysis/case study, a final with a senior manager [R]. A Hyderabad review rated it Easy with basic-to-medium SQL (GROUP BY, joins, window functions) and basic Python [S]. A Bengaluru 2025 review: third-highest salary per department using DENSE_RANK; rejection came after over a month with no explanation [S]. | About 4 India sources agree on "SQL early, LP-based behavioural in most later rounds" (IP 2.2). Best-supported GCC. |
| Wells Fargo (Hyderabad) | Reviews are for Senior Analytics Consultant, not plain DA. Nov 2024: first round on Teams with Tableau, SQL and logical reasoning; SQL joins, TRUNCATE vs DELETE, views vs temp tables; another reviewer reported about an hour of SQL plus SSIS/SSRS and window functions; the in-person managerial round was almost non-technical. 3 rounds (technical, managerial, HR) in about four weeks; one candidate was rejected as "not technically strong". | [S]; about 3-4 reviews |
| Novartis (Hyderabad) | Varies widely. March 2023: 6 rounds over 2 weeks including an Excel case study (pivots, rank, formulas). Sept 2025 campus: online MCQ, 4 technical rounds, HR. Another Sept 2025 report: a group discussion, project interview, HR. Roles not confirmed as DA. | [S]; anecdotes. Strong signal only for the Excel case and one GD |
| HSBC (Hyderabad) | One March 2026 report: 2 rounds, technical (SQL, Python, banking functions, resume) then HR. A Mumbai June 2026 report: 3 interview rounds plus 2 HR, a psychometric test, Python, Power BI, Looker. | [S]; thin, anecdotes |
| JPMorgan (Hyderabad) | One review calls the process long with too many rounds, with basic Python questions. A guide (not Hyderabad-specific) lists online assessment, recruiter screen, technical, superday, live coding over 4-6 weeks. | [S]; [G]. Treat all as unverified for full-time Hyderabad DA |
| Microsoft (Hyderabad/Bengaluru) | Very weak. Hyderabad DA: moderate difficulty, basic CTE SQL; another Hyderabad review (Jan 2024) lists Power BI, Fabric, Azure, DSA, Excel; a Bengaluru DA: HR screen, SQL technical, final case study; another Bengaluru report "very hard" with coding/DSA. | [S]; unverified for the India development centre |

**GCC common thread.** SQL (joins, window functions, ranking) is the one constant. Tools differ by team: Tableau at Wells Fargo, Power BI at Deloitte and Microsoft, an Excel case at Novartis. Behavioural/LP weight is high at Amazon; for Microsoft it is only guide-level evidence. Difficulty in India reports is basic to medium (Amazon Hyderabad "Easy", HSBC 2/5 on a small base) but not uniform. Timelines: Wells Fargo about 4 weeks, Novartis 2 weeks, JPMorgan guide 4-6 weeks. (IP 2.2)

### 3.3 Analytics firms (Tiger Analytics, Fractal, Mu Sigma, LatentView, Indium)

| Company | What was reported | Reliability |
|---|---|---|
| Tiger Analytics | GfG campus DA post (year unknown): 4 rounds, a roughly 90-minute proctored online assessment (about 20 aptitude/maths, 10 CS fundamentals, 2 coding), Technical 1 (coding, SQL, Bayes/conditional probability, projects), Technical 2 (probability, statistics, puzzles, project discussion), HR. The writer called stats/probability the hardest part. Funnel: 220 took the test, about 50 shortlisted, 5 selected. Summaries add SQL second-highest salary, self-join, window function and a hypothesis-test example. | [R] (campus); [S]. About 4 sources. |
| Fractal | One 2024 Bengaluru BA report: a 75-question aptitude test (quant, logical, verbal, some analytics, ending in a video introduction), a technical round built on the resume, then HR. Other reports: a technical test of 8 questions (4 SQL, 4 Python/R) and a business round with guesstimates, probability and market-entry cases, scored on structure. | [S]; about 3-4 sources. A "6-7 rounds" figure from an aggregator is unverified. |
| Mu Sigma | A FACE Prep guide: 3-4 rounds: aptitude plus psychometric, a video-synthesis observational test, a group case-study activity, a personal interview (technical, then HR). Technical content is guesstimates, case/metric design and puzzles, graded on structure and stated assumptions rather than the final number. Some 2026 cohorts reportedly add an AI-led conversational screening (AI as interviewer). Mostly campus/trainee hiring. A claim that only 15-20% clear the aptitude cutoff comes from a prep site and is unverified. | [R/G] (guide); [S] for candidate corroboration |
| LatentView | A Feb 2026 Chennai report: planned 3 rounds (technical screen, technical, client) with a project-manager round added. A guide says 4 rounds. A 2020 GfG campus post (Analytics Engineer, virtual) had 6 rounds, including a GD. **No Hyderabad or Bengaluru-specific report was found (Chennai is its base).** | [S]; [G]; [R] (2020 campus) |
| Indium Software (Hyderabad/Chennai) | The most Hyderabad-relevant of this group. July 2026: 4 rounds (2 technical, a client round, HR). Jan 2026: written test (aptitude, logical, SQL, analytical), then two technical levels. May 2026: a one-day process with a GD and 2 technical rounds covering ML basics and a market-estimation case. SQL joins, aggregates, window functions, CTEs; Tableau. | [S]; roughly 4-5 reviews. Review-to-detail mapping unverified. |

**Pattern.** An aptitude gate first, then 1-2 technical rounds (SQL, Python, probability), a case or guesstimate, a client round at Indium, then HR. The aptitude gate and the stats/probability questions are harder here than at service MNCs, while the interview rounds themselves are reported as "medium". Interviewers were said to look for structure, assumptions, project depth and "business understanding". Timelines: one Tiger candidate reported 3 weeks [S]; the rest are unverified. (IP 2.3)

### 3.4 Product companies and startups (Flipkart, PhonePe, Meesho; Swiggy and Zepto unverified)

| Company | What was reported | Reliability |
|---|---|---|
| Flipkart (Bengaluru) | A review of a 2023 interview: 4 rounds: pre-screen, guesstimates plus puzzles, case studies, a KPI round, plus hands-on SQL. A 2024 report: aptitude test with SQL, logical reasoning and statistics. Another: 2 rounds (resume-based, then business metrics). Round counts conflict (2-4). | [S]; about 4-5 reports |
| PhonePe | A BA online assessment: quant aptitude, logical reasoning, and 5 SQL questions (1 easy, 2 medium, 2 hard). Bengaluru April 2025 (role unstated): a 15-minute recruiter call, then a manager round that was "all SQL... LeetCode-hard" with 4-5 queries. April 2024: 3 rounds (SQL, puzzles/experience, case/scenario). A Hyring guide says there is no fixed path and calls itself an editorial map, not official. | [S]; [R/G]; 3 candidate reports |
| Meesho | An online SQL-coding assessment (reports vary: 10-12 SQL questions, or 4 medium-hard SQL plus 24 MCQs on SQL, aptitude and Excel), an SQL technical round, a case/product round, then HR/manager. Topics: window functions, CTEs, UNION vs UNION ALL, recursive CTE. Cases: declining completed orders, root-cause analysis. | [S]; about 4-6 sources. Strongest startup pattern. Bengaluru detail brief. |
| Swiggy | One guide says 5 rounds, another says 2-3 (conflicting). Candidate reports found were for Data Scientist 1, not DA. | [G]; [S]. **Unverified for DA.** |
| Zepto | No first-hand DA reports found. Guides say about 4 stages over 3-5 weeks with a take-home or live data exercise. | [G] only. **Unverified.** |

**Pattern.** The SQL online test replaces the aptitude test, followed by a hard SQL round, then a case/metrics round and a manager/HR round. SQL difficulty here is the highest of any type ("LeetCode-hard" at PhonePe, "moderate to tough" at Meesho). Interviewers were said to value first-principles thinking and a justified approach, not only the answer (Swiggy and PhonePe guides, [G]). GD appears only for PhonePe campus hiring, per a guide. Timelines are mostly unverified. (IP 2.4)

### 3.5 Comparison table (all cells candidate-reported and anecdotal)

| Dimension | Service MNCs | GCCs | Analytics firms | Product / startups |
|---|---|---|---|---|
| Typical rounds | 2-4 | 2-6 (Amazon 5; Wells Fargo 3; HSBC 2; Novartis 2-6) | 3-6 (Tiger 4; Mu Sigma 3-4; Indium 4; LatentView 3-6) | 2-5 (Meesho 2-3; PhonePe 2-3; Flipkart 2-4; see note below) |
| First filter | Aptitude / online test | SQL screen or analytical online test | Long aptitude plus coding/SQL test | SQL-heavy online test |
| SQL difficulty | Basic-medium | Basic-medium | Medium | Medium-hard |
| Case / guesstimate | Rare | Amazon case; Novartis Excel case | Common | Common |
| Stats / probability | Basic | Rare | Common and hard | Occasional |
| GD | None seen | Novartis (1 report) | LatentView 2020, Mu Sigma, Indium 2026 | PhonePe campus (guide) |
| Timelines reported | about 1-2 weeks to 3 months | about 2-6 weeks | about 3 weeks (1 report) | Mostly unverified |
| Evidence strength | Moderate (many thin reports) | Weak to moderate | Moderate (campus-skewed) | Moderate for Meesho/Flipkart/PhonePe; weak for Swiggy/Zepto |

(IP Section 3)

Note on conflict: the IP table gives Meesho and PhonePe as 2-3 rounds, but IP Section 2.4 describes Meesho as four steps (online test, SQL technical, case/product, HR/manager) and PhonePe as a recruiter call plus a manager round. Counting an online test as a round or not explains most of this. Use the ranges as rough only.

### 3.6 Group discussions, timelines and the typical loop

- **GD.** It is a campus/early-career screening device at mid-size analytics and BPO-adjacent firms, about 6 sources, mostly campus and mostly before 2023. Examples: Ugam 2021 (about 50% eliminated at the GD [R]), LatentView 2020 [R], Mu Sigma, Indium May 2026 (Hyderabad, [S]), Novartis Sept 2025 [S]. **No evidence of GD for lateral/switcher hires at service MNCs, GCCs or startups.** Treat the claim that some Hyderabad mid-size firms still use GDs as "few reports" (Indium 1, Novartis 1). Preparation is in Book 11 Part 7. (IP 2.5)
- **Timelines.** Roughly 1 week to 3 months at service companies; 2-6 weeks at GCCs; others mostly unverified. Ask the recruiter. (IP Section 3)
- **Typical loop.** Service MNCs and analytics firms: online test, then technical, then HR. GCCs and startups: an SQL screen takes the place of the aptitude test. (IP Section 5 item 13)

### Limitations (Section 3)

- No company confirmed any process. Reports are anonymous and unverifiable, the Glassdoor/AmbitionBox/Reddit/LinkedIn/YouTube gaps are real, and several review-to-URL mappings are unverified.
- Evidence for HSBC, JPMorgan, Microsoft, Swiggy and Zepto is thin or unverified, and LatentView has no Hyderabad/Bengaluru report.
- Salary and lateral-versus-fresher differences are not covered by these sources.
- Companies change processes. Nothing here predicts what a specific team will do next month.

---

## Section 4 - Round-by-round expectations

Each block says what the round tests, where it was reported, how long (only where the research gives a figure), and which book prepares you. Evidence labels as in Section 3. Counts of "profiles" come from about 20 company profiles in IP Section 4, are not a statistical sample, and one profile can rest on one report.

### 4.1 At a glance

| Round | Reported by (company type) | Frequency signal (IP Section 4) | Prepare with |
|---|---|---|---|
| Online test: aptitude / assessment | Service MNCs, analytics firms, Accenture, Deloitte | about 14 profiles | Book 6 |
| SQL (online and live) | All four types | about 19 of 20 profiles | Book 2 |
| Excel / Power BI / Tableau task | Deloitte, Wipro, Infosys (Power BI); Novartis (Excel case); Wells Fargo, Indium (Tableau) | Power BI about 7; Excel about 5; Tableau about 4 | Books 1 and 4 |
| Case / guesstimate | Analytics firms, Flipkart, Meesho, Amazon, Novartis | cases about 8; guesstimates about 6 | Book 7 (and Book 8) |
| Stats / probability | Tiger, Fractal; occasionally Flipkart | about 6 | Book 5 |
| Take-home / live data exercise | Zepto only, per guides | [G] only, unverified | Books 1, 2, 4, 8 |
| Project walk-through | Across types | about 14 profiles | Book 8 Part 8 |
| Managerial | Wells Fargo, startups, TCS guide | not tallied | Book 11 |
| HR / behavioural | Universal last round; Amazon is LP-heavy | about 15 profiles | Book 11 |
| Group discussion | Mostly campus-era; Indium and Novartis 2025-26 | about 6, mostly campus | Book 11 Part 7 |

### 4.2 Online test (aptitude, SQL, MCQ)

- **What is tested.** Quant, logical and verbal aptitude; data interpretation; basic CS or database questions; sometimes SQL or small coding tasks. Examples: Tiger's roughly 90-minute proctored test (about 20 aptitude/maths, 10 CS, 2 coding) [R]; Fractal's 75-question test with a video introduction [S]; Deloitte campus AMCAT, 75 minutes [R]; Accenture's elimination round plus a non-elimination English communication assessment [G/S]; a Novartis online MCQ with a pie-chart interpretation question [S]; PhonePe's quant/logical test plus 5 SQL questions [S]; one Meesho variant with 4 SQL questions plus 24 MCQs on SQL, aptitude and Excel [S].
- **Who uses it.** Service MNCs and analytics firms as a first gate; GCCs and startups swap in an SQL-flavoured test.
- **Length.** Only two durations are reported: Tiger about 90 minutes and Deloitte campus AMCAT 75 minutes. Fractal (75 questions) and the Meesho variant (4 SQL plus 24 MCQs) give question counts, not time. Do not assume others.
- **Prepare.** Book 6 for aptitude and data interpretation; Book 2 for SQL questions; Book 3 for small coding items.
- **Honest note (guidance, not research).** These tests act as a filter, so a switcher with a good resume could be cut here. Practise them under time limits.

### 4.3 Live SQL

- **What is tested.** Joins, GROUP BY/HAVING, Nth-highest salary (DENSE_RANK appears in an Amazon report), window functions, CTEs, duplicates, subqueries; at startups also recursive CTEs, self-joins, cumulative sums. (IP 2.1-2.4)
- **Difficulty by type (reports).** Service MNCs and GCCs basic to medium; analytics firms medium; product/startups medium-hard, with "LeetCode-hard" at PhonePe. Individual exceptions exist: a Deloitte Nov 2025 candidate solved one of two medium-hard questions [S]. (IP Section 3)
- **Format.** Shared screen (Amazon, [S]), Teams call (Wells Fargo, [S]), or in-person.
- **Prepare.** Book 2. Aim for the tier of the company type you target, and say your reasoning aloud while you write.

### 4.4 Excel, Power BI or Tableau task

- **What is tested.** Power BI/DAX concepts: SUM vs SUMX, ALL vs ALLEXCEPT, DATEDIFF, row-level security, incremental refresh, optimisation, Power Query, data modelling [S]. Tableau: blending, LODs, filters [S]. Excel: a Novartis case using pivots, rank and formulas [S].
- **Who uses it.** Power BI at Deloitte, Wipro, Infosys, Microsoft and HSBC; Tableau at Wells Fargo, Indium, LatentView, Infosys; Excel case at Novartis. Tool choice depends on the team, so read the JD.
- **Prepare.** Books 1 and 4. Match the tool named in the JD.

### 4.5 Case study and guesstimate

- **What is tested.** Structured thinking and explicit assumptions rather than the final number (Mu Sigma guide [R/G]; Fractal summary [S]). Examples reported: petrol stations in India, coffee shops in Bangalore, a 15% footfall-drop case, market entry, profitability, sweet shops in a hometown, number of stores in New Delhi, declining completed orders on an executive dashboard, and a KPI definition round at Flipkart.
- **Who uses it.** Analytics firms, Flipkart, Meesho, Amazon (data-analysis/case round), Novartis and Indium. Rare at service MNCs.
- **Prepare.** Book 7 for structure and estimation, Book 8 for metric-change investigations and data interpretation.

### 4.6 Take-home or live data exercise

Only guides mention it, for Zepto, and no first-hand DA report was found. Treat it as **unverified**. If you are told to expect one, ask the recruiter for the time limit, data format and expected output. Practise end to end with Books 1, 2, 4 and 8.

### 4.7 Statistics and probability

- **What is tested.** Bayes and conditional probability, hypothesis-test examples, probability puzzles. Tiger's campus writer called this the hardest part; it also appears at Fractal and, in MCQ form, at Flipkart. Service-MNC reports mention only basic statistics (Accenture). (IP 2.2-2.4, Section 4)
- **Prepare.** Book 5. Analytics firms justify the effort; for most service or GCC roles, basics suffice on this evidence.

### 4.8 Project walk-through

- **What is tested.** Whether you really did what the resume says and can explain it end to end. Near-universal: about 14 profiles, including Deloitte, TCS, Wipro, Fractal, Tiger, LatentView, Mu Sigma and Flipkart. The research does not say how decisive it is for switchers; as guidance, your projects are your main proof, so prepare this round well.
- **Prepare.** Book 8 Part 8 (project deep-dive questions), Book 12 for portfolio and resume, and have one project you can explain in plain business words.

### 4.9 Managerial and HR/behavioural rounds

- **What is tested.** Managerial rounds can be almost non-technical (Wells Fargo, [S]). HR rounds cover career goals, relocation and your switch story. Amazon is the only company with consistent LP evidence: scenario and LP rounds with STAR-style answers. (IP 2.2, Section 5 item 11)
- **How to do well.** Prepare your career-switch story first (Book 11 Parts 1-2), then STAR stories (Book 11 Part 3), HR logistics (Book 11 Part 8), and the Amazon Leadership Principles bank if you apply there (Book 11 Part 11).

### 4.10 Group discussion

See Section 3.6: mostly campus, mostly before 2023, with Indium (May 2026) and Novartis (Sept 2025) as the recent reports. Ugam's candidate advice was to be fluent, not interrupt, and make a few strong points [R]. Practise lightly with Book 11 Part 7.

### 4.11 When you blank or do not know

No research source measures how interviewers react, so this is guidance, not data. A simple rule: say what you do know, state your assumption, work the problem aloud, and ask a clarifying question. Interviewers at analytics firms were reported to score structure and assumptions, not only answers (Mu Sigma, Fractal, [R/G], [S]). Practise this with Book 11 Part 9.

### 4.12 Putting it together: what to expect by target

| If you target | Likely loop (candidate-reported) | Spend your time on |
|---|---|---|
| Service MNC | Online test, technical (SQL/Power BI/Excel/projects), HR | Books 6, 2, 1, 4, then Book 11 |
| GCC | SQL screen, tool-specific round, managerial, HR (Amazon: LP rounds) | Books 2, 4, 8, 11 |
| Analytics firm | Aptitude gate, technical (SQL/Python/probability), case, HR | Books 6, 2, 5, 7, 3 |
| Product / startup | SQL test, hard SQL round, case/metrics, manager/HR | Books 2, 7, 8, 5 |

Before any of these, confirm the structure with the recruiter.

### Limitations (Section 4)

- Round contents are candidate-reported. Durations are known for only two tests (Tiger, Deloitte AMCAT); Fractal and Meesho give question counts only.
- The IP tallies have small internal inconsistencies: the SQL count "about 19 of 20" lists three exclusions (Zepto, Swiggy, Microsoft), which would give about 17; the guesstimate count of "about 6" names Fractal twice (5 distinct companies). Read all counts as rough.
- Frequency counts are tallies of company profiles, not a sample of interviews, and several rest on one report.
- No reliable data was found on how often switchers (as against freshers) are cut at each round, or on how interviewers treat HR-to-analytics candidates specifically.
- The "how to behave" advice in 4.11 and the preparation priorities in 4.12 are guidance, not research findings.
