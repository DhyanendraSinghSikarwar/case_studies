# Book 7 — Part 1: Big Tech Interview Processes (Google, Microsoft, Amazon, Meta, Apple, Netflix, Uber, LinkedIn, Adobe, Salesforce)

**Topic:** How the data science, ML engineer, applied scientist and GenAI interview loops at ten large technology companies are reported to work, built from live search research, with an evidence tag on every claim.

**Target:** 10 companies  |  **Actual:** 10 (Google, Microsoft, Amazon, Meta, Apple, Netflix, Uber, LinkedIn, Adobe, Salesforce)  |  **Date:** 2026-10-31  |  **Status:** Complete (profiles merged, checked, reviewed)

**Scope note:** each profile covers rounds as reported, question types, illustrative sample questions mapped to Books 1-6 by part topic, what the loop scores, level notes (names and expectations only), a 2-week preparation plan, common mistakes, recent and AI-era changes, sources and what to verify. Pay is out of scope in this book, and so are visa and legal topics (Book 8 covers regions and points to official sources).

**How to read the evidence tags:** `[S1]`, `[S2]`... point to the numbered sources at the end of the same profile; `[G]` is a general pattern for large technology companies, not a statement about that company; `[U]` is unverified or weakly sourced and should be checked; `[illustrative]` marks a sample question written by the editor to match the question types the sources describe. "Anecdotal" means a single candidate report or forum thread, which is never the process itself.

**Evidence limits:** WebFetch does not work in this environment, so no page was opened; every source is a WebSearch result snippet or summary. Official pages mostly surfaced as short snippets, and several third-party sources were summaries of more than one page, so some source entries say that a detail cannot be tied to one URL. Round counts and durations differ between sources for almost every company, and India-specific interview evidence is thin for all ten. Treat every profile as a starting map and confirm the current process with the recruiter and the company's own careers page. Evidence levels: Google Medium, Microsoft Medium, Amazon Medium, Meta Medium, Apple Medium, Netflix Thin, Uber Medium, LinkedIn Medium, Adobe Thin, Salesforce Thin. See research notes in `scratch/B7P01_C*/sources.md` and `review_notes/Book7_Part01_review.md`.

---

## Comparison at a glance (only what the profiles support; check each profile for tags and caveats)

| Company | Evidence | Data science loop as reported | ML engineer loop as reported | AI-tool signal reported (check with your recruiter) |
|---|---|---|---|---|
| Google (C1) | Medium | Recruiter screen, SQL/schema-style screens, loop on measurement and modelling, experimentation and applied analysis, Googleyness; committee review and team matching | Coding, ML system design, ML domain deep dive, Googleyness (4-5 rounds, anecdotal) | In-person round reporting (Aug 2025); a software-engineering AI-assisted pilot reported in 2026, scope unconfirmed |
| Microsoft (C2) | Medium | Recruiter screen, technical screen (SQL, statistics, core ML), one-day loop of 4-5 rounds (ML, experimentation, product case, behavioural) | Screen with ML coding (senior anecdote), project deep dive, behavioural, live coding | Careers pages cover AI use in preparation; AI-assisted coding reported only for AI-focused orgs (guide, anecdote) |
| Amazon (C3) | Medium | Phone screens, some timed SQL/coding tests (India anecdote), loop of about 4-5 interviews with a Bar Raiser and Leadership Principles focus; debrief | Applied Scientist loop with ML depth, coding and Leadership Principles; sources conflict on loop size | Reported disqualification for unauthorized GenAI tools (secondary reporting; Amazon policy text not seen) |
| Meta (C4) | Medium | Recruiter call, SQL plus product sense screen, loop of 4-5 rounds (SQL, product sense, statistics/experimentation, behavioural) | Full loop of up to six 45-minute conversations per Meta ML page; coding, ML system design, behavioural | AI-enabled coding round reported as a limited, invite-only pilot; sources partly conflict |
| Apple (C5) | Medium | Decentralised by team; 3-5 loop rounds in one guide; screens then loop then team match | 4-7 rounds in guides; counts differ widely | Conflicting: a third-party tracker lists a ban; an unconfirmed software-engineer thread claims an AI-assisted round |
| Netflix (C6) | Thin | Prep-site stages (SQL, statistics and experimentation, ML, product case, culture); long-loop anecdotes of 11-12 rounds are not the standard process | Prep-site six-round loop (ML depth, coding, ML system design, culture) | Weakly sourced and unverified |
| Uber (C7) | Medium | SQL/Python plus experimentation screen; loop with product case, experimentation, behavioural, sometimes a bar-raiser; marketplace emphasis | Coding, ML coding, ML system design, behavioural | No official statement found; one third-party claim tagged unverified |
| LinkedIn (C8) | Medium | SQL/Python screen, virtual onsite of 4-5 rounds (SQL, product sense and experimentation, statistics, hiring-manager behavioural) | Coding, ML design, ML or data mining, behavioural | AI-enabled coding reported for software-engineer onsites; DS/ML scope unconfirmed |
| Adobe (C9) | Thin | Online assessment, technical, manager and director rounds in one guide; another reports a presentation and case study | Thin coverage; one 2026 guide for an AI-engineer loop (coding, ML depth, ML system design) | Third-party guide says AI tools generally not allowed in live engineering interviews unless invited |
| Salesforce (C10) | Thin | Recruiter screen, technical rounds (SQL, ML, statistics), behavioural interspersed; guides say 4, 6 or 7 rounds | Coding/assessment, ML theory, generative AI "under the hood" in one guide | No candidate AI policy found |

Patterns across several companies, each supported in the profiles it is tagged in: product sense and experimentation rounds recur for data science loops (Meta, Uber, LinkedIn, Microsoft, Google) [G]; ML system design recurs for ML engineer loops (Meta, Uber, LinkedIn, Google, Netflix) [G]; behavioural and values-based rounds carry weight everywhere, most explicitly at Amazon [G]; many processes are decentralised by team, so round counts vary [G].

---

### C1 Google (Big Tech)

**Evidence level:** Medium. Many third-party guides and candidate reports agree on the broad shape (recruiter screen, technical screens, a loop of about 45-minute interviews, a Googleyness round, committee review), but no official Google process page appeared in any result, round counts differ between sources, and the AI-era changes are pilot reports with unclear scope [S1][S8][S5].

**Roles seen in sources:** Data Scientist (product / analytics flavour) [S1][S2], Machine Learning Engineer [S3][S4], Research Scientist and applied research-engineer tracks including Gemini/DeepMind postings [S12], and Data Engineer in Hyderabad [S10]. India-specific data science reports are few and small [S11].

**Process overview (as reported):**
1. Recruiter screen [S1][S3].
2. One or two technical screens. For data science, SQL and schema design are reported [S13]; for ML engineer, a 45-60 minute coding interview mixing data structures, algorithms and ML concepts, in Python or C++ (anecdotal) [S3].
3. Onsite or virtual loop. Data science: measurement and modeling concepts, experimentation and applied analysis, plus a leadership and Googleyness behavioural interview, in one guide's description [S1]. ML engineer: reports of 4-5 rounds covering coding, ML system design, an ML domain deep dive and Googleyness (anecdotal) [S3][S4]. Another guide says the loop is typically five interviews of about 45 minutes each [S1].
4. Review by a committee that reads written feedback, then team matching; passing the committee is not the same as an offer [S8].
5. Total duration varies by source: roughly 4-8 weeks for data science in guides [S1], about 28 days average for ML engineer in a three-review Glassdoor estimate [S4]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call | Fit, background, role match | [S1][S3] |
| Technical screen (DS) | Live, SQL and schema design | SQL, data modelling | [S13][S2] |
| Technical screen (MLE) | 45-60 min live coding | DSA plus ML concepts | [S3] anecdotal |
| Loop: stats / experimentation (DS) | Interview, about 45 min | Hypothesis tests, A/B design, causal reasoning | [S1][S2] |
| Loop: measurement and modeling (DS) | Interview | Metrics, modeling concepts, product sense | [S1][S13] |
| Loop: coding / ML design (MLE) | Interviews | Algorithms, ML system design, ML domain depth | [S3][S4] anecdotal |
| Googleyness and leadership | Behavioural | Teamwork, ownership, decision-making | [S1][S9] |
| Committee and team match | Offline review | Written packet review | [S8] |

**Question types:**
- SQL with joins, window functions, CTEs, often with follow-ups that add complexity [S13][S2].
- Statistics and experimentation: hypothesis testing, A/B design, t-statistic style questions [S1][S2].
- Product sense: clarify the question first (who counts as active, late events) [S13].
- ML coding and concepts: attention-class implementation, language-model head, SVM training complexity (candidate-reported, anecdotal) [S3].
- ML system design (example reported: an indoor-navigation app for blind users, anecdotal) [S3].
- Behavioural / Googleyness [S1][S9].

**Sample questions (illustrative):**
- Write a SQL query for 7-day rolling active users per country, then handle late-arriving events. [illustrative] Book 3 Part 5 (running totals, moving averages) and Part 8 (DAU/MAU product metrics).
- Design an A/B test for a new video thumbnail layout and say how you would pick the primary metric. [S11] Book 1 Part 10 (A/B testing) and Book 6 Part 4 (experiment design).
- Implement multi-head attention from scratch and explain what changes at inference time. [S3] Book 2 Part 1 (transformer internals).
- What is the training time complexity of an SVM, and when would you pick something else? [S3] Book 1 Part 1 (ML fundamentals).
- Design a ranking model for a search feature: data, features, metric, serving. [illustrative] Book 1 Part 7 (ranking) and Book 1 Part 11 (ML system design).
- Find the shortest path in a weighted graph, then explain complexity. [illustrative] Book 5 Part 9 (graphs).
- Tell me about a time you disagreed with a teammate on an analysis. [illustrative] Book 6 Part 6 (stakeholder conflicts).

**What they score:**
- Structured interviewing: standardized rubric, each interview focused on one attribute such as general cognitive ability, role knowledge, leadership or Googleyness [S8][S9].
- Role knowledge for data science: statistics, experimentation, SQL, product reasoning [S1][S2].
- Googleyness: curiosity, collaboration, user focus [S9].
- Evidence is written up and judged by a committee, not the single interviewer [S8].

**Level notes:**
- Levels L3 and L4 reported with a loop of four DSA rounds plus one Googleyness-and-leadership round (software engineer track; DS and MLE mix may differ) [S8].
- Senior data scientist experiences exist on candidate sites [S13]; level-specific expectations were not found in snippets.
- Research roles: stronger emphasis on research depth, with your own work examined closely and a research presentation commonly reported [S12].

**Preparation plan (2 weeks):**
- Days 1-2: SQL windows, cohorts, funnels. Book 3 Parts 4-6 and 8.
- Days 3-4: Statistics and A/B testing. Book 1 Parts 10, 13, 14; Book 6 Part 4.
- Days 5-6: ML fundamentals, metrics, boosting. Book 1 Parts 1-4.
- Days 7-8: Coding practice in a plain editor or shared doc, no autocomplete. Book 5 Parts 1-9 and Book 1 Part 12 [G].
- Days 9-10: Transformers and GenAI basics if the role is ML or GenAI. Book 2 Parts 1, 6, 9.
- Days 11-12: ML system design. Book 1 Part 11, Book 4 Part 12, Book 2 Part 12.
- Days 13-14: Googleyness stories and two full mocks. Book 6 Parts 6 and 10; Book 9 when available [G].

**Common mistakes:**
- Writing SQL without first stating the definition of the metric [S13].
- Preparing only DSA for a data science loop that is stats and SQL heavy [S1][S2].
- Weak statistics and A/B fundamentals, a self-reported worry on Blind (anecdotal) [S13].
- Skipping the behavioural round because it is "soft" [S9].
- Treating one candidate's loop as the standard [G].

**Recent changes and AI-era notes:**
- Aug 2025 reporting: Google's CEO said at least one in-person round would be added for technical roles [S5]. An in-person pilot ran at large sites including Bangalore, reported as 2 virtual plus 3-4 in-person interviews; this is secondhand from interviewing.io and not an official description [S6].
- 2026 reporting (based on a Business Insider review of an internal document): a pilot lets software engineering candidates use an approved AI assistant in a code comprehension round, "human-led, AI-assisted". Scope and levels are unconfirmed, and it is for software engineering, not clearly for data science or ML roles [S7].
- Older: the standard structured loop and committee review [S8].

**Sources:**
- S1: https://www.tryexponent.com/guides/google-data-scientist-interview . Supports: DS loop description (measurement and modeling, experimentation, Googleyness), five 45-minute interviews, 4-8 weeks. Seen 2026-10-31. Snippet only.
- S2: https://www.interviewquery.com/guides/google-data-scientist . Supports: DS stages, statistics/SQL emphasis, t-statistic style questions. Seen 2026-10-31. Snippet only.
- S3: https://www.jointaro.com/interviews/companies/google/work-experiences/machine-learning-engineer-mountain-view-ca-february-17-2025-4-310c9db2/ . Supports: MLE experience listing (Feb 2025, anecdotal); the 45-60 min coding and onsite 4-5 round detail comes from the search summary of Glassdoor MLE reviews. Seen 2026-10-31. Snippet only.
- S4: https://www.glassdoor.ca/Interview/Google-Interview-E9079-RVW95711844.htm . Supports: MLE review (rounds DSA, ML system design, domain deep dive, Googleyness; 28-day average, anecdotal). Seen 2026-10-31. Snippet only.
- S5: https://www.hcamag.com/ca/news/general/google-opts-for-in-person-interviews-amid-surge-in-ai-aided-candidates/545945 . Supports: in-person round for technical roles reported Aug 2025. Seen 2026-10-31. Snippet only.
- S6: https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot . Supports: in-person pilot sites (incl. Bangalore) and 2 virtual plus 3-4 in-person format, secondhand. Seen 2026-10-31. Snippet only.
- S7: https://letsdatascience.com/news/google-pilots-ai-assistants-in-engineering-interviews-1737eba2 . Supports: AI-assisted code comprehension pilot, unclear scope. Seen 2026-10-31. Snippet only.
- S8: https://www.levels.fyi/blog/google-software-engineer-interview-process.html . Supports: structured interviewing, committee review, team matching, SWE L3/L4 loop shape. Seen 2026-10-31. Snippet only.
- S9: https://dglearning.substack.com/p/inside-the-google-2026-loop-rounds . Supports: per-interview attributes and Googleyness round (blog, third party). Seen 2026-10-31. Snippet only.
- S10: https://www.jointaro.com/interviews/companies/google/experiences/data-engineer-hyderabad-may-10-2025-accepted-offer-positive-6bad0095/ . Supports: Hyderabad data engineer recruiter screen on AWS, Python, Spark (anecdotal). Seen 2026-10-31. Snippet only.
- S11: https://www.glassdoor.com/Interview/Google-Interview-RVW87918743.htm . Supports: Bengaluru data scientist reports (time series, coding, YouTube thumbnail A/B design; anecdotal, small sample; the page-to-question match is from a summary of several Glassdoor results). Seen 2026-10-31. Snippet only.
- S12: https://www.interviewquery.com/interview-guides/google-research-scientist . Supports: research roles, presentation, research depth, 4-6 weeks. Seen 2026-10-31. Snippet only.
- S13: https://www.teamblind.com/post/google-product-data-science-interview-a8go2v8y . Supports: product DS candidate thread (SQL, A/B shakiness; anecdotal); SQL-in-shared-doc and product-sense details come from the search summary of several guides. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium confidence in the overall shape; low confidence in exact round counts and durations, which differ by source [S1][S8].
- India: only a few small, mixed-role reports found; do not assume Indian loops differ or match [S11][S10].
- Verify on Google's careers site: current rounds for your role, whether an in-person round is required, and whether any AI-assisted round applies to your role [S5][S7].
- No claim here that any question will be asked.

### C2 Microsoft (Big Tech)

**Evidence level:** Medium. Microsoft's own careers pages appeared in results (hiring tips, virtual interviews, AI-tool preparation guidance) but only as short snippets that say little about rounds. Round-level detail comes from third-party guides and anecdotal reports that agree on a recruiter screen, technical screen and final loop but disagree on counts and vary by team [S1][S3][S5]. AI-assisted round evidence is thin [S8].

**Roles seen in sources:** Data Scientist [S1][S2], Data and Applied Scientist / Applied Scientist at levels L60-L63 [S3][S4][S9], Machine Learning Engineer [S3], AI Engineer [S10], and Microsoft Research data scientist, which one report describes as a lighter, different process [S1]. India: Hyderabad and Bengaluru reports and a Hyderabad Data and Applied Scientist II posting [S7].

**Process overview (as reported):**
1. Recruiter screen, described as about 30 minutes on background and fit [S1].
2. Technical screen of about 45 minutes with a hiring manager or senior data scientist, on SQL, statistics and core ML for data science [S1]. For a Senior Applied Scientist (L63), a 60-minute phone screen with ML coding such as K-means from scratch then vectorized (anecdotal) [S4].
3. Final loop, described as one day with four to five back-to-back rounds of 45-60 minutes: ML, experimentation, product case, behavioural [S1]. Another account lists screening, project deep dive, behavioural and live coding [S1].
4. Each interviewer submits independent feedback, then the team debriefs [S1].
5. Duration: about 4-8 weeks in one guide, about two weeks in another; sources disagree [S1]. Microsoft says it will give timely updates and prep materials as candidates advance [S5].
6. Format varies between teams and product groups [S6][S1].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | About 30 min call | Background, fit | [S1] |
| Technical screen | About 45-60 min live | SQL, stats, ML basics; coding for applied scientist | [S1][S4] |
| Loop: coding | Live, LeetCode-medium style reported | Algorithms; ML coding at senior levels | [S4] anecdotal |
| Loop: ML / experimentation | Interview | ML fundamentals, A/B, drift, calibration | [S1][S4] |
| Loop: ML system design | Open-ended, L63 and above reported | End-to-end design, product and collaboration | [S3][S4] |
| Behavioural / manager | Interview | Learning from experience, culture fit | [S1][S3] |
| AI-assisted coding (some orgs) | VS Code with Copilot, per one guide quoting a manager | Working with AI on ML or data tasks | [S8] unconfirmed |

**Question types:**
- SQL and analytics: rolling 7-day retention from a daily events table, cohorts with sharp week-over-week drops (Hyderabad, Feb 2026, anecdotal) [S7].
- ML fundamentals: bias versus variance, missing data handling (Hyderabad, anecdotal) [S7]; Thompson sampling versus epsilon-greedy, Platt scaling, offline versus online metric gap, covariate shift versus label drift (reported for L63, anecdotal) [S4][S3].
- ML coding: K-means from scratch and vectorized [S4].
- ML system design: next-word prediction for an app [S3]; a RAG application design question reported at senior level in Nov 2025 [S10].
- Project walk-through and past research [S7][S1].
- Behavioural [S1][S3].

**Sample questions (illustrative):**
- Write SQL for 7-day rolling retention and flag cohorts whose retention drops sharply week over week. [S7] Book 3 Part 6 (retention, cohorts) and Part 5 (window functions).
- Implement K-means in NumPy, then vectorize the distance step. [S4] Book 1 Part 5 (clustering) and Book 1 Part 12 (NumPy live coding).
- Offline AUC looks good but the online metric did not move: list causes and checks. [S4] Book 6 Part 2 (model degraded in production) and Book 1 Part 3 (calibration, leakage).
- Covariate shift versus label drift: how do you detect each? [S3] Book 4 Part 8 (monitoring, drift).
- Design a RAG assistant over internal documents: chunking, retrieval, evaluation, hallucination controls. [S10] Book 2 Parts 6, 7 and 9 (RAG, advanced RAG, evaluation).
- Design next-word prediction for a mobile keyboard under latency limits. [S3] Book 1 Part 11 (ML system design) and Book 2 Part 10 (deployment).
- Walk through your most recent project: what was your own contribution and what would you change? [illustrative] Book 6 Part 10 (end-to-end open scenarios).

**What they score:**
- Technical fluency in SQL, statistics and ML at the screen [S1].
- Problem solving and applying AI in a collaborative setting, per an AI Engineer loop outline [S10].
- Independent feedback from each interviewer, combined in a team debrief [S1].
- Honest self-representation at every stage is an explicit Microsoft expectation [S5].
- Project depth for senior applied scientist roles (past research focus, reported) [S7].

**Level notes:**
- L60 and L61: heavier on data structures and algorithms, per one guide [S3].
- L63 and above: extra rounds such as ML system design [S3].
- Level can shift during the process (a Blind thread reports a posting edited from Data and Applied Scientist II to Senior; anecdotal) [S9].
- Hyderabad Data and Applied Scientist II posting lists an advanced degree in a quantitative field plus several years of data science experience [S7].

**Preparation plan (2 weeks):**
- Days 1-2: SQL windows and retention. Book 3 Parts 4-6.
- Days 3-4: Statistics and experimentation. Book 1 Parts 10, 13, 14; Book 6 Part 4.
- Days 5-6: ML fundamentals, metrics, clustering. Book 1 Parts 1, 3, 5.
- Days 7-8: Coding in NumPy and DSA. Book 1 Part 12; Book 5 Parts 1-9.
- Days 9-10: Drift, monitoring, serving. Book 4 Parts 6 and 8; Book 6 Part 2.
- Days 11-12: RAG and GenAI design if role is AI-focused. Book 2 Parts 6, 7, 9, 12.
- Days 13-14: ML system design mocks, project deep-dive rehearsal, Azure ML basics. Book 1 Part 11; Book 4 Part 11 [G].

**Common mistakes:**
- Struggling with matrix broadcasting when vectorizing (reported by one candidate, anecdotal) [S4].
- Assuming one loop shape; format is team dependent [S6][S1].
- Not being able to explain your own project contribution [S7][G].
- Using AI tools in a way that misrepresents your abilities [S5].

**Recent changes and AI-era notes:**
- Microsoft's careers pages say interviews for students are virtual and that candidates may use AI tools while preparing if done ethically and reflecting true capabilities [S5]. This is about preparation, not use during the interview.
- One prep guide says AI-assisted coding interviews (VS Code with Copilot) exist only in AI-focused orgs such as CoreAI and Copilot, quoting a manager; a Blind post (anecdotal) says the bar is slightly higher with help. No official policy found [S8].
- Recent anecdotal reports from Hyderabad in 2026 show SQL retention and ML basics still appear [S7]; older Microsoft Research and 2021 L60/L61 reports exist but were not relied on [S1].

**Sources:**
- S1: https://www.interviewquery.com/guides/microsoft-data-scientist . Supports: DS stages (recruiter 30 min, technical screen about 45 min, loop of four to five rounds), feedback and debrief, team variation, MSR lighter process. Seen 2026-10-31. Snippet only.
- S2: https://www.tryexponent.com/guides/microsoft-data-scientist-interview . Listed as a DS guide in results; no distinct claim taken from its snippet. Seen 2026-10-31. Snippet only.
- S3: https://www.interviewquery.com/interview-guides/microsoft-machine-learning-engineer . Supports: level emphasis L60/L61 vs L63+, ML topics, system design example, behavioural rounds (summary of several sources). Seen 2026-10-31. Snippet only.
- S4: https://leetcode.com/discuss/post/7791470/microsoft-senior-applied-scientist-l63-i-jvy4/ . Supports: L63 phone screen with K-means coding and ML topics (anecdotal). Seen 2026-10-31. Snippet only.
- S5: https://careers.microsoft.com/us/en/interviewtips . Supports: support and updates through the process, accommodations, honesty expectation, AI use in preparation (from the search summary of Microsoft careers pages); virtual student interviews are from https://careers.microsoft.com/us/en/student-interviewing. Seen 2026-10-31. Snippet only.
- S6: https://www.levels.fyi/blog/ace-microsoft-hiring.html . Supports: no single format, varies by team. Seen 2026-10-31. Snippet only.
- S7: https://static.glassdoor.at/Interview/Microsoft-Interview-E1651-RVW98366441.htm . Supports: Hyderabad and Bengaluru candidate reports (SQL retention, bias-variance, missing data; anecdotal). The page-to-claim match is from a summary of multiple Glassdoor results; Hyderabad Data and Applied Scientist II posting: https://abs.dejobs.org/hyderabad-ind/data-applied-scientist-ii/EB356439E535485987223A902EC78016/job/ . Seen 2026-10-31. Snippet only.
- S8: https://www.teamblind.com/post/microsoft-ai-coding-interview-1c67wvu3 . Supports: Blind post on Microsoft AI-assisted round (anecdotal); org scope and Copilot detail from https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/ via search summary. Seen 2026-10-31. Snippet only.
- S9: https://www.teamblind.com/post/up-leveled-for-interview-microsoft-gvdkcsqv . Supports: level shifts during process (anecdotal; title only). Seen 2026-10-31. Snippet only.
- S10: https://www.interviewquery.com/prep-guides/microsoft-ai-engineer . Supports: AI Engineer loop outline recruiter to stakeholder interview; RAG design question reported on https://www.hellointerview.com/community/questions/rag-application-design/cmhy2xydo009f08ads2e3ujij . Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium for the broad stages; low for exact counts and durations, which differ [S1].
- Official Microsoft pages gave support and policy statements, not round structures [S5].
- India: individual 2024-2026 reports only, no IDC-specific process confirmed [S7].
- Verify with your recruiter: loop shape for your team, level, whether any AI-assisted round applies, and rules on AI use during interviews [S5][S8].
- No claim that any question will be asked.

### C3 Amazon (Big Tech)

**Evidence level:** Medium. Amazon's own interview guide appeared as a search result [S2], but all other detail is third-party prep sites and anecdotal candidate reviews that vary by team and year. Snippets only; no page was opened.

**Roles seen in sources:** Applied Scientist (including Senior and AGI/LLM-flavoured postings) [S3][S8], Data Scientist (mostly intern reviews, some India listings) [S4][S9], GenAI Engineer and AI Engineer prep guides [S6], Research Scientist prep page on the Amazon jobs site [S1]. India reports (Bengaluru, Hyderabad) are anecdotal and few [S5][S9].

**Process overview (as reported):**
1. Recruiter screen / online application [S3]. Duration not found in sources.
2. One or two phone screens, possibly followed by role-specific assessments; screens mostly check basic qualifications [S2]. Third-party guides say about 45 minutes [S2 snippet, third-party part]; one Bengaluru anecdote describes a 60-minute screen mixing ML depth, live coding and Leadership Principles (LP) [S5] (anecdotal).
3. Timed SQL or coding test for some Data Scientist candidates in India (anecdotal) [S9].
4. Virtual or onsite "loop": third-party guides say 4 to 5 back-to-back interviews [S3]; one Applied Scientist guide says four 55-minute interviews plus a tech talk [S3]; sources conflict on size, so confirm with the recruiter [S3].
5. Bar Raiser: an interviewer from another team, focused on LPs; guides disagree on whether it is the last round and on veto power [S3] (third-party, conflicting).
6. Debrief after the final interview, judged against the LPs and role requirements; Amazon states it aims to give feedback about two business days after phone screens and about five after the loop [S2].
7. For Senior Applied Scientist, some reports mention a research or project presentation of roughly 45-60 minutes with Q&A, sometimes with an abstract sent ahead (anecdotal) [S7].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call | Fit, role match | [S3] |
| Phone screen(s) | 45-60 min call, live coding and/or ML and LP questions | Basic qualifications | [S2][S5] |
| SQL / coding test (DS, India) | Timed online | SQL and programming basics | [S9] anecdotal |
| Loop: ML breadth | Interview with scientist | Loss functions, optimizers, regularisation, transformers | [S5] anecdotal |
| Loop: ML depth | Interview | Deep dive on your own recent project | [S5] anecdotal |
| Loop: coding | Live coding | Correctness, explanation, complexity; difficulty varies by interviewer | [S5] anecdotal |
| Loop: LP / Bar Raiser | Behavioural | Past examples against LPs | [S2][S3] |
| Research talk (Senior) | Presentation plus Q&A | Depth, communication, defending methods | [S7] anecdotal |

**Question types:**
- Behavioural questions tied to Leadership Principles, using real past examples [S2]; LP questions appear embedded in every interview in several reviews [S5] (anecdotal).
- Data Scientist reviews: SQL window functions, GROUP BY, subqueries, CTEs, Pandas manipulation, statistics (regression assumptions, Pearson vs Spearman), confusion matrix, deep learning concepts [S4] (anecdotal, intern-heavy).
- Applied Scientist: ML breadth and depth, coding, ML design [S3][S5][S8].
- LLM-era reports: LLM training techniques, LLM evaluation metrics, RAG versus fine-tuning, seq2seq, L1/L2 [S8] (anecdotal).
- Case or use-case discussion with a hiring manager appears in some reports [S10] (anecdotal).

**Sample questions (illustrative):**
1. Write a SQL query to rank each customer's orders by value and return the top 3 per customer. [illustrative] Book 3 Part 4 (window functions: ranking and top-N per group).
2. Explain the assumptions of linear regression and how you would check each. [S4] Book 1 Part 2 (linear/logistic regression), Book 1 Part 13 (statistics).
3. Walk me through a recent ML project in depth: why this model, what failed, what you would change. [S5] Book 1 Part 11 (ML system design); Book 6 Part 10 (design a solution end-to-end).
4. Compare Pearson and Spearman correlation and when each misleads. [S4] Book 1 Part 1 (stats basics), Book 1 Part 14 (statistics deep dive II).
5. When would you use RAG instead of fine-tuning, and how would you evaluate the result? [S8] Book 2 Part 6 (RAG basics), Book 2 Part 4 (fine-tuning), Book 2 Part 9 (LLM evaluation).
6. Solve an array/hash problem and state time and space complexity. [illustrative] Book 5 Part 1 (arrays and hashing).
7. Tell me about a time you disagreed with a stakeholder and what you did. [illustrative] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).
8. A key metric dropped 10% week over week; how do you investigate? [illustrative] Book 6 Part 1 (product metrics and metric drops).

**What they score:**
- Leadership Principles evidence, with the panel debriefing against LPs and role requirements [S2]. Each interviewer is reported to own specific principles [S2 snippet, third-party part].
- Technical correctness with explanation and complexity (anecdotal) [S5].
- ML fundamentals and depth on own work [S5][S3].
- For Senior scientist roles, depth and communication in a talk (anecdotal) [S7].

**Level notes:** One prep guide describes Applied Scientist at L5 and Senior Applied Scientist at L6, with L6 leading projects and setting direction; the same guide's L5 title mapping looks questionable, so verify against job postings [S8] [U].

**Preparation plan (2 weeks):**
- Days 1-2: LP story bank (8 to 10 stories with measurable results, STAR format) [S2][S3]; Book 6 Part 6.
- Days 3-4: SQL timed practice: Book 3 Parts 3, 4, 5 and 12 [S4][S9].
- Days 5-6: ML and stats fundamentals: Book 1 Parts 1, 2, 3, 13 [S4][S5].
- Days 7-8: Deep learning, transformers, NLP: Book 1 Parts 8 and 9; for GenAI roles Book 2 Parts 1, 4, 6, 9 [S5][S8].
- Days 9-10: Coding practice with spoken complexity: Book 5 Parts 1, 2, 7, 9 [S5].
- Days 11-12: Prepare a deep dive on one own project; Senior roles also a 45-minute talk [S5][S7]; Book 1 Part 11.
- Days 13-14: Mixed mock loop with LP in each round [S5]; Book 6 Parts 1 and 10.

**Common mistakes:**
- Hypothetical answers to behavioural questions instead of real examples [S2 snippet, third-party part].
- Treating LPs as one round only; reports say they are embedded throughout [S5] (anecdotal).
- Not being able to go deep on your own project (ML depth) [S5] (anecdotal).
- Using AI tools during the interview (see below) [S6].

**Recent changes and AI-era notes:**
- Reported 2025: Amazon disqualifies candidates caught using unauthorized GenAI tools in interviews, and candidates acknowledge they will not use them; teleprompter-style tools are named. Reporting traces to Business Insider via secondary outlets; Amazon's own policy text was not seen [S6].
- Amazon's guide mentions 16 Leadership Principles; older guides cite 14, so check the current list [S2 snippet, third-party part].
- LLM topics (training, evaluation, RAG versus fine-tuning) appear in recent Applied Scientist reviews (anecdotal, undated) [S8].
- Older: 2021-2022 Bengaluru loops (anecdotal) [S5].

**Sources:**
- S1. https://amazon.jobs/content/en/how-we-hire/research-scientist-interview-prep : page titled "Amazon Leadership Principles" on Amazon's jobs site, appeared for the Applied Scientist query; snippet gave no content, so used only to note it exists. Seen 2026-10-31. Snippet only.
- S2. https://aboutamazon.com/news/workplace/amazon-interview-guide : Amazon's guide: LP-rooted process, debrief, feedback timing, phone screens vs loop. Seen 2026-10-31. Snippet only (also https://www.aboutamazon.com/md/news/workplace/amazon-interview-process-phone-screens-loops appeared).
- S3. https://www.cleverprep.com/companies/amazon/applied-scientist : third-party; 4 rounds, four 55-minute loop interviews plus tech talk, research presentation advice. Seen 2026-10-31. Snippet only. Also https://hyring.com/jobseeker-toolkit/interview-questions/company/amazon and https://prepfully.com/interview-guides/amazons-bar-raiser-interview for Bar Raiser descriptions (third-party).
- S4. https://www.glassdoor.co.uk/Interview/Amazon-Interview-E6036-RVW99965159.htm : Glassdoor reviews, mostly Data Scientist Intern, SQL/Python/stats/ML, LPs (anecdotal). Seen 2026-10-31. Snippet only. Also https://www.glassdoor.co.uk/Interview/Amazon-Interview-E6036-RVW103632729.htm.
- S5. https://leetcode.com/discuss/interview-experience/1585287/amazon-msft-google-apple-fb-zoom-applied-scientist-multiple-sep-21-offer-rest-reject ; https://www.teamblind.com/post/applied-scientist-interview-amazon-4udsobcp ; https://www.glassdoor.sg/Interview/Amazon-Interview-E6036-RVW79375451.htm : Bengaluru and other Applied Scientist anecdotes (screen, ML breadth/depth, coding, LPs). The search summary did not attribute each detail to a single URL, so details are attributed to this group. Seen 2026-10-31. Snippet only.
- S6. https://itpro.com/business/careers-and-training/amazon-bans-ai-tools-during-job-interviews : AI-tool ban reporting; also https://dataford.io/interview-guides/amazon/genai-engineer and https://www.interviewquery.com/prep-guides/amazon-ai-engineer as GenAI/AI Engineer prep guides (third-party). Seen 2026-10-31. Snippet only.
- S7. https://www.teamblind.com/post/amazon-science-sr-applied-scientist-interview-presentation-requirement-tgrgowoo : Blind anecdote on Senior Applied Scientist presentation (about 50 + 10 min). Seen 2026-10-31. Snippet only.
- S8. https://interviewkickstart.com/odio/amazon-applied-scientist-interview-guide : level descriptions; plus https://www.glassdoor.fr/Entretien/Amazon-Entretien-E6036-RVW100110012.htm (LLM questions, anecdotal) and https://igotanoffer.com/en/advice/amazon-applied-scientist-interview. Seen 2026-10-31. Snippet only.
- S9. https://www.ambitionbox.com/interviews/amazon-interview-questions/data-scientist : India Data Scientist anecdotes (timed SQL test, coding questions). Seen 2026-10-31. Snippet only.
- S10. https://www.interviewquery.com/guides/amazon-data-scientist?exp_page=1 : third-party description of DS loop and case prompts. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium for the existence of LP-driven loops, Bar Raiser and ML breadth/depth/coding split; low for exact round counts, durations and which levels get a talk (sources conflict) [S3].
- India-specific evidence is thin and anecdotal [S5][S9].
- Verify with your recruiter and Amazon's jobs site: loop size, Bar Raiser, presentation requirement, AI-tool policy, current LP count.

### C4 Meta (Big Tech)

**Evidence level:** Medium. Meta's own careers pages for the ML full loop appeared in results [S1][S2], but their content reached me only as short snippets. Data Scientist structure, coding and AI-era details come from prep sites, press reports and anecdotal reviews. India-specific interview evidence is thin.

**Roles seen in sources:** Data Scientist (product analytics) [S3], Machine Learning Engineer / Software Engineer, Machine Learning [S1][S4], AI/Research Scientist and GenAI-flavoured loops [S6]. India: job listings in Bangalore for Data Scientist and Senior ML Engineer, offices in Bengaluru and Hyderabad per a low-authority blog [S7].

**Process overview (as reported):**
1. Recruiter call: non-technical, role fit and motivation; one guide says 30-45 minutes [S3].
2. Data Scientist technical screen: one or two interviews of about 45 minutes (one guide says 45-60), with SQL plus a product sense case [S3].
3. Data Scientist full loop: estimates of four to five interviews covering SQL, product sense, statistics or A/B testing, analytical reasoning and behavioural; one candidate described four 45-minute virtual rounds (anecdotal) [S3].
4. ML Engineer: Meta's ML page says the full loop is up to six 45-minute conversations with engineers [S1]; third-party guides describe screening, coding, ML system design and behavioural [S4].
5. Timeline: guides say 4-6 weeks; Glassdoor candidates report about 2 to 2.5 months (anecdotal) [S3].
6. Recruiter tells you ahead of time which round is which, and which allow AI (reported for the AI-enabled pilot) [S5].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter call | Phone | Fit, motivation | [S3] |
| DS technical screen | 45-60 min, SQL + light product case | SQL, product thinking | [S3] |
| DS loop: SQL / analytical reasoning | About 45 min | Query writing, data reasoning | [S3] |
| DS loop: product sense | About 45 min | Success metrics, launch decisions, opportunity sizing | [S3] anecdotal |
| DS loop: statistics / experimentation | About 45 min | A/B test design | [S3] |
| DS loop: behavioural | About 45 min | Past behaviour, collaboration | [S3] |
| MLE: coding | LeetCode-style, several short problems | Correct, clean code, edge cases | [S4] anecdotal |
| MLE: ML system design | Open design, e.g. recommendation | Data, features, model, offline/online evaluation, trade-offs | [S4] anecdotal |
| MLE/RS: AI-enabled coding (pilot) | 60 min in CoderPad with built-in assistant | Working with AI on a larger problem | [S5] reported, limited pilot |
| Research Scientist: research fit | Present own research, open questions | Depth on own work | [S6] anecdotal |

**Question types:**
- DS: SQL, product sense (measure success of Facebook Groups, define a success metric, decide whether to launch a feature), A/B test design, opportunity sizing [S3] (anecdotal).
- MLE: LeetCode easy-to-hard coding, ML system design (recommendation and ranking recur), behavioural described as comparatively smooth [S4] (anecdotal).
- Research/GenAI: own-research defence, ML coding without PyTorch, LLM training efficiency such as gradient checkpointing, designing an LLM assistant with retrieval and safety guardrails [S6] (anecdotal).

**Sample questions (illustrative):**
1. How would you measure the success of Facebook Groups? [S3] Book 6 Part 1 (product metrics and metric drops); Book 3 Part 8 (funnels, conversion, DAU/MAU).
2. Write a query for day-7 retention by signup cohort. [illustrative] Book 3 Part 6 (date/time: retention, cohorts).
3. A new feature shows a lift on one metric and a drop on another; do you launch? [illustrative] Book 6 Part 4 (experiment design and ambiguous A/B results); Book 1 Part 10 (A/B testing).
4. Design a place-recommendation system for users. [S4] Book 1 Part 7 (recommenders, ranking); Book 1 Part 11 (ML system design).
5. Design an LLM-based conversational assistant with retrieval and safety guardrails. [S6] Book 2 Part 6 (RAG basics), Book 2 Part 5 (alignment, safety, guardrails), Book 2 Part 12 (GenAI system design).
6. Explain gradient checkpointing and when it helps training. [S6] Book 2 Part 2 (pretraining and scaling), Book 1 Part 8 (deep learning).
7. Solve a graph or array problem cleanly with edge cases handled. [S4] Book 5 Part 9 (graphs), Book 5 Part 1 (arrays and hashing).
8. Implement logistic regression training loop in NumPy without a framework. [illustrative] Book 1 Part 1 (from-scratch code), Book 1 Part 12 (live-coding).

**What they score:**
- Technical skill per round; the loop is described as assessing technical skills and giving candidates a view of the work [S2].
- For DS: product sense and metric reasoning alongside SQL and statistics [S3].
- Behavioural performance can move the level outcome: one Blind anecdote reports a candidate at IC5 on design but IC4 on behavioural [S8] (anecdotal).
- Edge cases and clean code in coding [S4] (anecdotal).

**Level notes:** Data Scientist levels appear as IC4 and IC5 and above; guides disagree on years of experience, and one Blind report says the final level is decided after the rounds [S8] (anecdotal). Engineering-track E-level names for ML roles appear in AI-coding reports (E6 and below, E7 and above) [S5]; DS equivalents not confirmed [U].

**Preparation plan (2 weeks):**
- Days 1-2: SQL timed sets: Book 3 Parts 1-5 and 8 [S3].
- Days 3-4: Product sense and metrics: Book 6 Parts 1, 4, 5 and Book 3 Part 8 [S3].
- Days 5-6: Stats and experimentation: Book 1 Parts 10, 13, 14 [S3].
- Days 7-8: ML fundamentals and recommenders: Book 1 Parts 2, 3, 4, 7 [S4].
- Days 9-10: Coding practice, short problems at speed: Book 5 Parts 1, 2, 7, 9; Book 1 Part 12 for ML coding [S4].
- Days 11-12: ML system design and, for GenAI roles, Book 1 Part 11 and Book 2 Parts 6, 9, 12 [S4][S6].
- Day 13: Practise a coding task with an AI assistant, plus writing your own tests and reviewing generated code: Book 1 Part 12 (AI-code-review rounds) [S5].
- Day 14: Behavioural stories and one full mock: Book 6 Part 6 [S3][S8].

**Common mistakes:**
- Treating the behavioural round as free, though one anecdote ties it to level outcome [S8] (anecdotal).
- Jumping to a model in ML design without covering data, features, offline and online evaluation [S4] (anecdotal).
- Using AI tools in a round where they are not allowed; Meta's full-loop guide is reported to ask candidates not to use unauthorized outside assistance [S5].
- Product answers without a clear success metric and guardrail metrics [G].

**Recent changes and AI-era notes:**
- Reported 2025: Meta confirmed building a coding interview with an AI assistant; one source says a pilot from October 2025 replaces one onsite coding round with a 60-minute CoderPad round with a built-in assistant, invite-only, and not universal [S5].
- Conflicting signal: Meta's careers guide is reported to still ask candidates not to use unauthorized AI tools; confirm in writing which round allows AI [S5].
- 2026 research scientist reports mention behavioural, ML design, AI-enabled coding and traditional coding in one loop (anecdotal) [S6].
- Older: DS loop structure from 2025 prep guides and reviews; undated for some [S3].

**Sources:**
- S1. https://www.metacareers.com/ML-prep-onsite/ : Meta ML full-loop page; snippet says up to six 45-minute conversations with engineers. Seen 2026-10-31. Snippet only.
- S2. https://www.metacareers.com/swe-prep-onsite/ : Meta SWE full-loop page; snippet describes loop as assessing technical skills and giving insight into work. Seen 2026-10-31. Snippet only.
- S3. https://www.interviewquery.com/interview-guides/facebook-data-scientist ; https://www.tryexponent.com/guides/meta-data-scientist-interview ; https://interviewkickstart.com/blogs/articles/meta-data-scientist-interview-process ; https://www.glassdoor.co.in/Interview/Meta-Interview-E40772-RVW97721021.htm : DS stages, SQL plus product sense, loop of four to five, timelines (third-party and anecdotal). Seen 2026-10-31. Snippet only.
- S4. https://www.interviewquery.com/guides/meta-ml-engineer ; https://app.igotanoffer.com/blogs/tech/facebook-machine-learning-engineer-interview ; https://dataford.io/interview-guides/meta/machine-learning-engineer/experiences : MLE rounds, coding, ML system design, behavioural (third-party, anecdotal). Seen 2026-10-31. Snippet only.
- S5. https://hellointerview.com/blog/meta-ai-enabled-coding ; https://www.techradar.com/pro/meta-is-going-to-let-candidates-use-ai-in-job-interviews ; https://www.businesstoday.in/amp/technology/news/story/meta-to-test-job-applicants-with-ai-assisted-coding-interviews-amid-ai-expansion-plans-487200-2025-07-31 ; https://www.greatfrontend.com/blog/ai-assisted-coding-interviews-for-frontend-developers : AI-enabled coding pilot, format, conflicting careers-guide note. Seen 2026-10-31. Snippet only.
- S6. https://www.glassdoor.sg/Interview/Meta-Interview-E40772-RVW92650100.htm ; https://www.1point3acres.com/interview/thread/1141203 ; https://www.interviewquery.com/guides/meta-ai-research-scientist : research/GenAI loop anecdotes. Seen 2026-10-31. Snippet only.
- S7. https://blog.kowatek.com/?p=99262 ; https://www.jointaro.com/jobs/meta/software-engineer-machine-learning-85dfab93 : India offices and Bangalore openings (low-authority). Seen 2026-10-31. Snippet only.
- S8. https://www.teamblind.com/post/ic5-behavioural-interview-expectations-at-meta-j0k1dwnv ; https://codemia.io/guides/meta-data-scientist : DS level and behavioural anecdotes; experience ranges conflict. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium for DS (SQL plus product sense screen, product/stats/behavioural loop) and MLE (coding, ML design, behavioural); low for exact round counts per role and team [S3][S4].
- Low for the AI-enabled round: pilot, limited, sources partly conflict [S5].
- India interview evidence: none firsthand found; only locations and openings [S7]. Assume the standard process only as [U].
- Verify on Meta's careers prep page for your role and with your recruiter: loop length, which rounds permit AI, level, and whether a research presentation applies.

### C5 Apple (Big Tech)

**Evidence level:** Medium. Many candidate write-ups and prep-site summaries exist, but all are snippet-only, anecdotal or commercial, they disagree on round counts, and Apple's own pages were not found. [S1][S6]

**Roles seen in sources:** Machine Learning Engineer [S1][S2], Data Scientist [S4], Applied Scientist (one forum thread) [S9], AI/Research Scientist [S10], general Apple loop guides [S6]. India-specific: only a handful of Bengaluru and Hyderabad mentions, with almost no process detail [S5][S11].

**Process overview (as reported):**
1. Recruiter or screening call; one guide calls it an informal chat of about 30 minutes about interest and team fit [S6]. Some ML guides add a hiring-manager call before the technical screen (four-round version: screen, manager call, technical screen, remote onsite) [S1].
2. One or more technical or role-specific phone/video screens [S6][S4].
3. Onsite or virtual loop. Counts differ by source: 4 to 6 back-to-back interviews in one guide, "up to 10" in another [S6]; 4 to 7 rounds for ML engineer [S1]; 3 to 5 loop rounds for data scientist [S4]. Anecdotal: a six-round ML onsite thread [S2].
4. Team match and final decision [S6]. Overall duration is quoted from one to three weeks [S1] to about 4 weeks for data scientist [S4] to 4 to 6 weeks for general loops [S6]; treat as rough, anecdotal ranges.
5. Apple's process is decentralised and varies by team, per guides [S6]. Each team runs its own hiring [G].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call, about 30 min per one guide | Interest, team fit | [S6] |
| Hiring manager call (ML engineer, some reports) | Call | Background and fit | [S1] |
| Technical screen | Phone/video | Coding; for data scientist SQL, Python, statistics | [S6][S4] |
| Loop: algorithm coding | Live coding | LeetCode-style problems (anecdotal) | [S3][S9] |
| Loop: ML coding / theory | Live | ML coding problem, ML/NLP questions (anecdotal) | [S3][S2] |
| Loop: ML system design | Discussion | Design of an ML product; some loops add a general system design round | [S3][S9] |
| Loop: project deep dive / behavioral | Discussion | Past projects, behavioral questions | [S3][S1] |
| Research talk (research roles) | 45-minute presentation to team (anecdotal) | Research depth | [S3][S10] |
| Data scientist loop | Virtual onsite | SQL, statistics, metric design, A/B test, project walkthrough, case studies on Apple app lines | [S4] |

Round durations other than those named above: duration not found in sources.

**Question types:**
- Coding (LeetCode-style) and ML coding [S3][S9]
- ML/NLP fundamentals and ML system design [S3][S9][S1]
- Project deep dives [S1][S4]
- For data scientist: SQL, statistics, A/B testing, metric design, anomaly detection, regression critique, time series, telemetry data [S4]
- Behavioral [S3][S6]

**Sample questions (illustrative):**
- Walk me through an ML project you shipped: data, model choice, offline and online metrics, what you would change. [illustrative] Book 1 Part 3 classification metrics; Book 1 Part 11 ML system design.
- Write a function on a graph or binary tree (medium difficulty). [S5] Book 5 Part 7 trees and BST; Book 5 Part 9 graphs. (Source: an intern-level Glassdoor report, anecdotal.)
- How would you conduct an A/B test? [S4] Book 1 Part 10 A/B testing; Book 6 Part 4 experiment design.
- Design an ML-powered feature for an app (data, features, model, serving, monitoring). [illustrative] Book 1 Part 11 ML system design; Book 4 Part 8 monitoring ML in production.
- Given a table of usage events, write SQL for a retention or per-user metric. [illustrative] Book 3 Part 6 retention and cohorts; Book 3 Part 8 product metrics.
- Implement a simple ML algorithm (for example logistic regression) in NumPy. [illustrative] Book 1 Part 2 regression; Book 1 Part 12 NumPy/pandas live-coding.
- A metric on a telemetry dashboard moves; how do you investigate? [illustrative] Book 6 Part 1 product metrics and metric drops.

**What they score:**
- Coding correctness and communication [S3][S6]; ML depth and project ownership [S1][S4]; for data science, SQL, statistics and metric judgement [S4]. Specific scoring rubrics: not found in sources; the above is inferred from round content. [U]

**Level notes:**
- Level names and expectations: not found in sources for this snippet set. [U] Check the job posting for the title and years-of-experience line.

**Preparation plan (2 weeks):**
- Days 1-3: coding fluency, arrays/hashing, trees, graphs (Book 5 Parts 1, 7, 9) and NumPy/pandas live coding (Book 1 Part 12). [G]
- Days 4-6: ML fundamentals, metrics, tree models, NLP basics (Book 1 Parts 1-4, 9). [G]
- Days 7-8: SQL and statistics for data-scientist roles (Book 3 Parts 4-6, 8; Book 1 Parts 13-14). [S4]
- Days 9-10: A/B testing and metric scenarios (Book 1 Part 10; Book 6 Parts 1, 4). [S4]
- Days 11-12: ML system design (Book 1 Part 11; Book 4 Part 6 serving). [S3][S9]
- Day 13: prepare two project deep dives, and a research talk if the role is research. [S1][S10]
- Day 14: mock loop, plus ask the recruiter about the exact format. [S6]

**Common mistakes:**
- Treating one candidate's round list as the process; reports vary by team [S1][S6].
- Weak project stories: project deep dives recur [S1][S4].
- Skipping SQL/statistics basics for data-scientist roles [S4].
- Assuming AI tools are allowed in live rounds (see below) [S7].

**Recent changes and AI-era notes:**
- A 2026 policy tracker lists Apple as prohibiting AI tools in interviews [S7]; this is a third-party aggregator (recent, unconfirmed by Apple).
- One 1point3acres thread title says Apple added an AI-assisted coding round for software engineer full-time interviews; the date and details could not be confirmed and it is about software engineers, not ML roles [S8][U].
- Sources do not say whether ML roles differ [U]. Ask the recruiter what applies.

**Sources:**
- S1: https://www.interviewquery.com/interview-guides/Apple-Machine-Learning-Engineer ; ML engineer guide; supports 4-round and 4-7 round descriptions and 1 to 3 week timeline; seen 2026-10-31; snippet only (prep site, partly paywalled).
- S2: https://www.1point3acres.com/interview/thread/1172960 ; title "Apple Machine Learning Onsite Interview Experience: Six Rounds Overview"; supports a six-round ML onsite report (anecdotal); seen 2026-10-31; snippet only (title and listing).
- S3: https://www.glassdoor.co.uk/Interview/Apple-Interview-E1138-RVW83470630.htm ; one of the Glassdoor reviews returned for ML engineer; the search summary reported a 6-round loop (algorithm coding, ML coding, system design, behavioral) and a 45-minute research presentation loop, without naming which review held which detail, so attribution is approximate; anecdotal; seen 2026-10-31; snippet only.
- S4: https://www.interviewquery.com/guides/apple-data-scientist?exp_page=1 ; data scientist guide; supports 3-6 rounds, about 4 weeks, SQL/Python/statistics, metric design, A/B test question; seen 2026-10-31; snippet only. Bengaluru (1-hour coding, manager, behavioral) and Cork (8 rounds) candidate reports came from the Glassdoor results of the same search, not attributable to one URL (anecdotal).
- S5: https://www.glassdoor.co.in/Interview/Apple-Interview-E1138-RVW73678830.htm ; one of the Glassdoor results of the India-focused search; the summary mentioned a Bengaluru referral process of about six weeks, a Hyderabad February 2023 neutral review and an ML intern report (HR screen, 2-3 tech rounds, graph/tree problems); attribution approximate; anecdotal; seen 2026-10-31; snippet only.
- S6: https://igotanoffer.com/en/advice/apple-interview-process ; general Apple loop guide among results; supports stages, decentralisation, 30-min recruiter chat, 4-6 or up to 10 loop interviews, timelines (the summary pooled several guides in the result set, so figures are approximate); seen 2026-10-31; snippet only.
- S7: https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/ ; supports Apple listed as AI-prohibited; seen 2026-10-31; snippet only.
- S8: https://www.1point3acres.com/interview/thread/1174445 ; title "Apple Adds AI-Assisted Coding Round for Software Engineer Fulltime Interviews"; seen 2026-10-31; snippet only; unconfirmed.
- S9: https://www.levels.fyi/community/thread/OuE1gQ/what-to-expect-for-apple-applied-scientist-interview ; supports applied scientist: phone screen then onsite, LC-style and ML design questions, team-dependent (anecdotal); seen 2026-10-31; snippet only.
- S10: https://www.interviewquery.com/guides/apple-ai-research-scientist ; supports research scientist loop with research talk and 5-6 researcher interviews; seen 2026-10-31; snippet only.
- S11: https://www.teamblind.com/post/apple-applied-machine-learning-team-mqyjagy3 ; Blind thread about the applied ML team (Hyderabad per the summary); snippet showed no answers; seen 2026-10-31; snippet only.

**Confidence and what to verify:**
- Confidence: medium on the general shape (recruiter, technical screens, loop with coding, ML, design and behavioral), low on exact round counts and durations. [S1][S6]
- India: very thin; no India-specific round structure found [S5][S11]. Verify with the recruiter.
- Verify on Apple's careers page and with the recruiter: loop length, whether coding is on a shared editor, the AI-tool policy, and team-specific rounds. All sources are snippet only; no page was opened.

### C6 Netflix (Big Tech)

**Evidence level:** Thin to Medium (rated Thin). Candidate reports are few, long-loop anecdotes differ widely, prep sites contradict each other, and the official page found covers culture, not interview steps. [S7][S2][S3]

**Roles seen in sources:** Data Scientist [S1][S2][S3], Machine Learning Engineer [S4][S5], ML Infra software engineer [S6], Research Scientist [S11], AI Engineer guides [S4]. India-based Netflix hiring: nothing found.

**Process overview (as reported):**
1. Recruiter chat, then hiring manager phone screen, then technical phone screen (Senior Data Scientist, Member UI team, 2021 review; anecdotal and dated) [S10].
2. Prep-site data scientist rounds: recruiter screen, technical phone screen, SQL, statistics and experimentation, machine learning, product case study, culture fit, about 4-6 weeks [S1] (commercial guide; another guide says these are question categories, not separate rounds [S1]).
3. Prep-site ML engineer loop: six rounds (recruiter screen, technical phone screen, ML depth, coding, ML system design, culture) [S4].
4. Anecdotal long loops: a 12-round data scientist process over about two months [S2] and an 11-round loop of about two and a half months with a hiring-manager swap (October 2025) [S3]. Single anecdotes, not the standard process.
5. General Netflix guides mention roughly 8 interviews over two stages and a unanimous team decision; not role-specific and unverified [S8][U].
6. Reapply wait of 6-12 months is quoted by one general guide [S8][U].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter chat | Call | Fit and logistics | [S10][S4] |
| Hiring manager screen | Phone | Background, team fit | [S10] |
| Technical phone screen | Phone | Product analytics/experimentation (DS); in one ML anecdote a behavioral interview plus an ML system design interview | [S10][S5] |
| SQL / data manipulation | Live | SQL | [S1] |
| Statistics and experimentation | Discussion | A/B testing, causal inference | [S1] |
| ML and modeling / ML depth | Discussion | ML fundamentals, past ML project | [S1][S4][S5] |
| ML system design | Discussion | Recommendation system design (prep site); anomaly detection design (anecdote) | [S4][S6] |
| Coding | Live | Coding, short warm-up in one anecdote | [S4][S6] |
| Product case / culture | Discussion | Product reasoning, culture fit | [S1][S4] |

Round durations: duration not found in sources.

**Question types:**
- Experimentation and causal inference, product metrics, behavioral [S1]
- Past ML project, loss-function choice, computer vision experience (anecdotal) [S5]
- Recommendation system design [S4]
- ML infra loop: coding, data science collaboration, system design (anecdotal) [S6]

**Sample questions (illustrative):**
- Tell me about a machine learning project you worked on. [S5] Book 1 Part 3 classification metrics; Book 1 Part 11 ML system design.
- How would you choose a loss function for this problem? [S5] Book 1 Part 2 regression and regularization; Book 1 Part 8 deep learning.
- Design a recommendation system from data collection to serving. [S4] Book 1 Part 7 recommender systems; Book 1 Part 11 ML system design.
- Design an anomaly detection system for a streaming metric. [S6] Book 1 Part 5 anomaly detection; Book 4 Part 8 monitoring ML in production.
- A new feature shows a lift in one metric and a drop in another; how do you decide whether to ship? [illustrative] Book 6 Part 4 ambiguous A/B results; Book 1 Part 10 A/B testing.
- Write SQL for weekly retention of members by signup cohort. [illustrative] Book 3 Part 6 retention and cohorts.
- Describe a time you gave a colleague direct feedback or disagreed with a decision. [illustrative] Book 6 Part 6 stakeholder conflicts and trade-offs.

**What they score:**
- Prep sites list strong ML fundamentals, a record of shipping impactful ML, collaboration [S4]; for data science, technical depth, statistical rigour, with a strategic roadmap discussion at senior level [S1]. The careers site frames culture around context over control, with managers coaching actively [S7]. Culture fit weight is the opinion of prep writers, unverified [S8][U].

**Level notes:**
- Mid-level data science focuses on coding fluency, statistical rigour and project ownership; senior adds roadmap and strategic impact [S1]. Research scientist IC4-IC5 focuses on technical depth and system design [S11]. Role posting titles seen use L4/L5 style names (data scientist L4, L5 postings) [S1][U].

**Preparation plan (2 weeks):**
- Days 1-3: experimentation and causal inference (Book 1 Part 10; Book 6 Part 4). [S1]
- Days 4-5: SQL and product metrics (Book 3 Parts 4-6, 8). [S1]
- Days 6-8: ML fundamentals and recommenders (Book 1 Parts 2-4, 7). [S4]
- Days 9-10: ML system design (Book 1 Part 11; Book 4 Part 8). [S4][S6]
- Day 11: coding refresh (Book 5 Parts 1, 7, 9; Book 1 Part 12). [S4][S6]
- Day 12: read the careers culture page and prepare examples of candid feedback and ownership (Book 6 Part 6). [S7]
- Days 13-14: mock loop; ask the recruiter about the format, as it varies by team and year. [S8]

**Common mistakes:**
- Preparing a fixed round list; reports range from 6 to 12 rounds [S4][S2][S3].
- Ignoring the culture material when it is part of the discussion [S7].
- Shallow experimentation answers for data-scientist roles, where it is central [S1].

**Recent changes and AI-era notes:**
- A Greek news site reports Netflix lets candidates use AI tools when writing code while still assessing code quality, system design and testing; not confirmed from a primary source [S9][U].
- A mirror page says interviews now discuss how candidates think about and use AI [U]; weakly sourced.
- A 2026 tracker lists AI policies by company; the snippet did not give a Netflix-specific line [S9].
- The October 2025 long-loop anecdote is the most recent candidate evidence [S3].
- India: no Netflix India hiring information found in sources.

**Sources:**
- S1: https://www.interviewquery.com/interview-guides/netflix-data-scientist ; data scientist guide; supports round list, 4-6 weeks, mid versus senior focus, experimentation emphasis; seen 2026-10-31; snippet only (commercial).
- S2: https://www.1point3acres.com/interview/thread/1123435 ; title "Two-Month Journey Through 12 Rounds of Netflix Data Science Interviews"; supports a 12-round anecdote only; seen 2026-10-31; snippet only (title and listing).
- S3: https://prachub.com/interview-experiences/netflix-data-scientist-interview-experience-11-rounds-10-people-and-a-hiring-manager-swapped-mid-loop ; supports an 11-round, long, hiring-manager-swap anecdote (October 2025 per the summary); seen 2026-10-31; snippet only.
- S4: https://www.cleverprep.com/companies/netflix/machine-learning-engineer ; supports six-round ML engineer prep-site list, recommender design prompt, hiring criteria; seen 2026-10-31; snippet only (commercial).
- S5: https://www.teamblind.com/post/ml-engineering-interview-at-netflix-rponqss8 ; Blind thread; the search summary cited a candidate report of a behavioral plus ML system design screen and questions on past ML project and loss functions; attribution to this URL approximate; anecdotal; seen 2026-10-31; snippet only.
- S6: https://www.1point3acres.com/interview/thread/1170648 ; ML infra software engineer onsite (coding, data science collaboration, system design); anecdotal; seen 2026-10-31; snippet only. The anomaly-detection design and short coding warm-up anecdote came from another result in the same search, not attributable to one URL.
- S7: https://jobs.netflix.com/culture ; official culture page; supports context-not-control and active coaching wording only; seen 2026-10-31; snippet only.
- S8: https://igotanoffer.com/en/advice/netflix-interview-process ; general Netflix process guide among results; the summary pooled several guides (about 8 interviews, unanimous decision, reapply 6-12 months, culture emphasis), so attribution is approximate; seen 2026-10-31; snippet only.
- S9: https://www.secnews.gr/en/722863/netflix-ai-fluency-dexiotita-ergazomenoi/ ; Greek news item on Netflix AI use in coding; unconfirmed; and https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/ for the general tracker; seen 2026-10-31; snippet only.
- S10: https://www.glassdoor.co.uk/Interview/Netflix-Interview-E11891-RVW44407200.htm ; 2021 Senior Data Scientist, Member UI review; supports recruiter, hiring manager, technical phone screen; anecdotal and dated; seen 2026-10-31; snippet only.
- S11: https://www.interviewquery.com/interview-guides/netflix-research-scientist ; supports IC4-IC5 focus; seen 2026-10-31; snippet only.

**Confidence and what to verify:**
- Confidence: low on round structure, medium on question themes (experimentation, ML design, recommenders). [S1][S4]
- Process varies by team and year; aggregators say live recruiter instructions decide it [S8].
- India: nothing found. Check the Netflix careers page for current India listings.
- Verify with the recruiter: number of rounds, AI-tool policy, coding format. All sources are snippet only; no page was opened.

### C7 Uber (Big Tech)

**Evidence level:** Medium. Uber's own page gives only a general outline [S1]; the round detail comes from prep sites and anonymous candidate reports that partly disagree [S2][S3][S4].

**Roles seen in sources:** Data Scientist (including Senior), Machine Learning Engineer, Applied Scientist (driver and marketing measurement flavours), Research Scientist, AI Engineer guide pages [S2][S3][S5][S9]. India postings seen: Data Scientist II in Bangalore (fraud, risk and ML focus), a Hyderabad Data Scientist posting, a Bangalore Scientist II listing, all as job-board snippets [S7].

**Process overview (as reported):**
1. Recruiter / Talent Acquisition conversation about the role and background. Official page says this comes first [S1].
2. Technical phone screen. Data science reports: one or two screens; one guide describes about 30 minutes of SQL and Python plus about 15 minutes of A/B testing and statistics (anecdotal and guide-based) [S2][S5]. ML engineer reports: a coding screen, with one report titled as 45 minutes of coding plus 15 minutes of free-form ML design (anecdotal) [S3].
3. Virtual or onsite loop of about four to five interviews of 45 to 60 minutes each, per prep guides (not official) [S3][S4][S9].
   - Data science: coding, case study or product sense, statistics and experimentation, technical deep dive, behavioural; some reports add a bar-raiser round [S2][S10].
   - ML engineer: LeetCode-style coding, ML coding, ML system design, leadership or behavioural; senior levels may add another design round. Sources conflict on whether ML coding is a separate round [S3][S4][S6].
4. Total process length quoted as roughly 2 to 6 weeks by guides; individual anecdotes range wider [S2][S1].
5. Uber states the process can differ between regions and teams [S1].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter conversation | Call | Background and role fit | [S1] |
| Technical screen (DS) | Live, SQL and Python, then stats | Joins, window functions, data manipulation; A/B testing and variance reduction | [S2][S5] anecdotal |
| Technical screen (MLE) | Live coding, sometimes short ML design | Coding correctness, basic ML design | [S3] anecdotal |
| Experimentation / statistics (DS) | Virtual loop round | Marketplace A/B tests, network effects, switchback, difference-in-differences | [S2][S9] guide-based |
| Product case (DS) | Virtual loop round | Uber-style metrics and business problems | [S2] |
| ML system design (MLE, some DS) | Whiteboard-style discussion | ETA, pricing, fraud, restaurant recommendation; latency, features, serving | [S3][S4] |
| Coding (MLE) | Live coding | LeetCode-style, rate limiter or scheduler style tasks | [S3][S5] anecdotal |
| Behavioural / hiring manager | Conversation | Leadership, teamwork, project deep dive | [S3][S10] |
| Bar raiser | Interview by someone from another team | Values and consistent hiring bar | [S10] third-party description |
| Duration per round | not found in sources for most rounds beyond the 45 to 60 minute guide figure | | [S4] |

**Question types:**
- SQL and pandas data manipulation, window functions [S2][S5].
- Python coding functions, e.g. cumulative sum style tasks (anecdotal Bengaluru report) [S7].
- A/B testing, variance reduction (CUPED), sample size, interference in two-sided marketplaces [S2][S9].
- Causal methods when randomisation is impossible: synthetic control, difference-in-differences, instrumental variables [S9].
- ML basics (trees, forests, boosting, imbalanced data) and production trade-offs [S10].
- ML system design on marketplace problems [S3][S4].
- Behavioural and project deep dive [S3].

**Sample questions (illustrative):**
- Design an experiment for a rider incentive when drivers and riders interact, and say how you handle interference. [illustrative] Book 1 Part 10 (A/B testing, causal inference, experimentation); Book 6 Part 4 (experiment design and ambiguous A/B results).
- How would you reduce variance in a control-versus-test comparison? [S2] Book 1 Part 14 (CUPED, variance reduction).
- A key marketplace metric drops 10 percent week over week; how do you diagnose it? [illustrative] Book 6 Part 1 (product metrics and metric drops).
- Write a SQL query for the rolling retention of riders by signup cohort. [illustrative] Book 3 Part 6 (date/time: retention, cohorts) and Part 5 (running totals).
- Design a real-time ETA or fraud-scoring system, covering features, serving latency and failure handling. [S3] Book 1 Part 11 (ML system design); Book 4 Part 6 (serving) and Part 9 (feature stores, streaming).
- Implement a rate limiter or simple scheduler. [S5] Book 5 Part 14 (design problems).
- How do you handle a highly imbalanced fraud label when moving a model to production? [S10] Book 1 Part 3 (imbalance, calibration, thresholding).
- Estimate the effect of a safety feature when an A/B test is not allowed. [S9] Book 6 Part 4 and Book 1 Part 10 (causal inference).

**What they score:**
- Correct, working code and clear communication in coding rounds [S3].
- Experimentation and causal depth, especially marketplace settings; one guide calls this the most distinctive part of the data science loop [S2][S9].
- Structure, data flow and failure handling in ML design; trade-off depth more important at senior levels [S3].
- Project ownership and values fit in behavioural and bar-raiser rounds [S10]. Uber's values are cited by one source as Go Get It, See Every Side, Build With Heart; the same source warns they have changed, so verify [S10].

**Level notes:** Postings show Data Scientist I / II and Scientist II, with Scientist II described as needing about four years of experience in one snippet [S7]. ML engineer guides mention L4 and senior levels, with an extra design round at senior [S4][S6]. Expectations beyond that: not found in sources.

**Preparation plan (2 weeks):**
- Days 1-2: SQL and pandas on retention, cohorts, funnels (Book 3 Parts 6 and 8) [G].
- Days 3-5: experimentation, CUPED, power, network effects, switchback and diff-in-diff (Book 1 Parts 10, 13, 14; Book 6 Part 4) [S2][S9].
- Days 6-7: product metrics and metric-drop cases (Book 6 Part 1) [S2].
- Days 8-10: ML fundamentals, imbalance, boosting (Book 1 Parts 3, 4) and ML system design for ETA, fraud, recommendation (Book 1 Part 11; Book 4 Parts 6, 9) [S3][S4].
- Days 11-12: coding practice, arrays, graphs, design problems (Book 5 Parts 1, 9, 14) for MLE roles [S3][S5].
- Days 13-14: behavioural stories and project deep-dive rehearsal, mock loop [S3][S10].

**Common mistakes:**
- Preparing only SQL when Python is also tested (reported by one anecdotal 2026 candidate) [S2].
- Using a plain A/B design for a two-sided marketplace and ignoring interference [S9].
- Giving ML design answers with no latency, serving or failure discussion [S3].
- Vague project deep dives with no personal ownership [S10].

**Recent changes and AI-era notes:**
- No official Uber statement on AI use in interviews was found. One third-party blog (2026) claims Uber embeds an AI assistant in coding rounds; another page from the same publisher does not list Uber, so treat as [U] [S8].
- Prep guides are dated 2025 to 2026 [S3][S8]; many candidate reports are older. Ask the recruiter whether AI tools are allowed in each round [S8][G].
- India: only job postings and sparse anecdotes were found; no detailed Bangalore or Hyderabad loop write-up [S7].
- Michelangelo, Uber's ML platform, has moved from predictive to generative AI per Uber's engineering blog, useful context for ML and GenAI roles [S11].

**Sources:**
1. S1: https://www.uber.com/careers/interviewing - Uber official: starts with Talent Acquisition conversation, ERG meeting later, process differs by region and team. Seen 2026-10-31. Snippet only.
2. S2: https://www.interviewquery.com/guides/uber-data-scientist - DS loop summary, experimentation emphasis, phone screen SQL/Python/stats, process length. Seen 2026-10-31. Snippet only; commercial prep site.
3. S3: https://www.interviewquery.com/interview-guides/uber-machine-learning-engineer - MLE loop 4-5 rounds, coding, ML design, behavioural. Seen 2026-10-31. Snippet only.
4. S4: https://www.cleverprep.com/companies/uber/machine-learning-engineer - onsite 4-5 rounds, 45-60 min, ML design prep topics. Seen 2026-10-31. Snippet only; commercial.
5. S5: https://dataford.io/interview-guides/uber/data-scientist/experiences - candidate-reported DS experiences and coding examples. Seen 2026-10-31. Snippet only; self-reported.
6. S6: https://www.1point3acres.com/interview/thread/1119874 - MLE onsite candidate report (virtual onsite: coding, ML coding, leadership, ML design). Seen 2026-10-31. Snippet only; anecdotal.
7. S7: https://www.themuse.com/jobs/uber/data-scientist-ii-ea4331 - Bangalore Data Scientist II posting (job-board snippet, India). Seen 2026-10-31. Snippet only.
8. S8: https://www.techinterview.org/post/3233476840/uber-interview-guide/ - 2026 Uber loop guide and AI-in-coding-round claim. Seen 2026-10-31. Snippet only; weakly supported.
9. S9: https://dataford.io/interview-guides/uber-drivers/applied-scientist - applied scientist causal inference themes. Seen 2026-10-31. Snippet only; partly gated.
10. S10: https://www.educative.io/blog/uber-interview-process-and-questions - bar-raiser round description (also values/behavioural summaries from related search results). Seen 2026-10-31. Snippet only.
11. S11: https://uber.com/blog/from-predictive-to-generative-ai - Uber engineering post on Michelangelo's move toward generative AI. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium for the shape of the loop; low for exact round counts, durations and order, which vary by team, level and region [S1].
- Verify on https://www.uber.com/careers/interviewing and the role's interview guide: round list, whether AI tools are allowed, whether a bar raiser is used, and India-specific format.
- Every candidate report here is anecdotal and often years old.

### C8 LinkedIn (Big Tech)

**Evidence level:** Medium. LinkedIn's own "How We Hire" snippet gave no process detail [S1]; the picture comes from prep sites and anonymous candidate reports spanning 2018 to 2026 that differ on round counts [S2][S3][S4].

**Roles seen in sources:** Data Scientist (including Senior), Machine Learning Engineer, Software Engineer (Data Science / Machine Learning) [S2][S4][S5]. India: a Bengaluru ML engineer anecdote (2021), a Bengaluru data scientist report (2024) and an India listing for a data science software engineer role at LinkedIn's India entity [S6][S7].

**Process overview (as reported):**
1. Recruiter screen, described by one guide as a casual conversation of about 30 minutes (guide-based) [S3].
2. Technical phone screen. Data science: SQL and Python on CoderPad, 45 to 60 minutes per one guide; a January 2026 senior data scientist screen reportedly covered product sense (measuring a feed change) and a short Python round after SQL (anecdotal) [S3][S4][S8].
3. Virtual onsite: four to five rounds of 45 to 60 minutes with a panel, per one guide; candidate reports mention about five 45-minute interviews and, for ML engineers, a six-round onsite (anecdotal) [S3][S6][S9].
   - Data science content: SQL and data analysis, product sense and experimentation, statistics and modelling, hiring manager behavioural [S3][S4].
   - ML engineer content: coding, ML design, ML or data mining, behavioural [S5][S6].
4. For engineering roles, one guide says the final stage includes a one-hour system design interview, and that hiring is centralised with team matching afterwards (guide-based, [U] for ML roles) [S3].
5. Timeline quoted as 4 to 6 weeks by a guide; a Glassdoor-based summary mentions about 6 weeks for some candidates (anecdotal) [S4][S2].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call, about 30 min | Fit and background | [S3] guide |
| Technical screen (DS) | CoderPad, 45-60 min | SQL (joins, group-bys, self joins, graph-flavoured), Python/pandas, product sense | [S3][S4][S8] |
| SQL / data manipulation (onsite) | Live | Joins, CTEs, aggregation | [S2] anecdotal |
| Product sense / experimentation | Discussion | Feed or homepage metric success, A/B design, Simpson's paradox, multivariate tests | [S4][S8] anecdotal |
| Statistics and modelling | Discussion | Hypothesis testing, power, multiple comparisons | [S4] guide |
| ML design (MLE) | Discussion | Recommender system, job-posting surfacing by location and activity | [S5] anecdotal |
| Coding (MLE) | Live | LeetCode-medium and graph problems; one 2024 report leaned ML/DS | [S5] anecdotal |
| AI-enabled coding (SWE onsite reports) | CoderPad with AI | Using AI tool while coding | [S10] anecdotal; whether it applies to DS/ML roles: [U] |
| Behavioural / hiring manager | Conversation | Experience, teamwork, project depth | [S3][S7] |
| Duration | 45-60 min per onsite round per guide; other durations not found in sources | | [S3] |

**Question types:**
- SQL with joins, window functions, CTEs, graph-style tables [S4].
- pandas group-by and Python manipulation [S8].
- Product metrics for feed and homepage changes [S8].
- A/B design and decision-making, Simpson's paradox [S4].
- ML theory: decision trees, AUC, evaluation metrics [S5].
- Recommender and job-matching design [S5].
- Project deep dive, reported for a Bengaluru internship interview [S7].

**Sample questions (illustrative):**
- How would you measure success after the homepage feed shows only more relevant content? [S8] Book 6 Part 1 (product metrics and metric drops); Book 1 Part 10 (experimentation).
- Your A/B test shows an overall lift but each segment shows a decline; explain. [S4] Book 1 Part 14 (probability puzzles, conditional probability and Bayes) and Part 10.
- Write SQL to find second-degree connections from an edge table of member connections. [illustrative] Book 3 Part 9 (recursive CTEs, hierarchies, graphs) and Part 2 (self joins).
- Do a pandas group-by to compute weekly active members per region. [S8] Book 3 Part 8 (DAU/MAU) and Book 1 Part 12 (NumPy/pandas live coding).
- Design a job recommender that ranks postings for a member using location and past activity. [S5] Book 1 Part 7 (recommenders, ranking) and Part 11 (ML system design).
- Explain AUC and when it misleads for a ranking model. [S5] Book 1 Part 3 (classification metrics).
- Design an LLM-based ranking service and explain how you would cut latency. [illustrative] Book 2 Part 10 (deployment, latency/cost) and Part 12 (GenAI system design).
- Solve a medium graph or array/binary-search problem. [S5][S7] Book 5 Parts 5 and 9.

**What they score:**
- Clean SQL and Python correctness [S4][S8].
- Tying a data anomaly to a product change; one 2026 report says product questions were examined carefully (anecdotal) [S8].
- Statistical reasoning in experiments [S4].
- ML design structure for ranking and recommendation [S5].
- Communication and storytelling; one report names "data storytelling" in the format (anecdotal) [S2].
- Scoring rubrics and levelling criteria: not found in sources.

**Level notes:** Postings and reports show Senior Data Scientist, Staff Data Scientist, Sr Software Engineer (Data Science) and an India L4 ML engineer mention [S7][S11]. Expectations by level: not found in sources; one guide says the loop varies by junior versus senior [S2].

**Preparation plan (2 weeks):**
- Days 1-3: SQL incl. self joins, graph-flavoured and window queries (Book 3 Parts 2, 4, 9) plus pandas (Book 1 Part 12) [S4][S8].
- Days 4-6: experimentation, power, multiple comparisons, Simpson's paradox (Book 1 Parts 10, 13, 14; Book 6 Part 4) [S4].
- Days 7-8: product metrics for feed and search changes (Book 6 Part 1) [S8].
- Days 9-11: recommenders, ranking, metrics and ML design (Book 1 Parts 3, 7, 11) [S5].
- Day 12: GenAI and LLM ranking, latency and cost (Book 2 Parts 10, 12) for GenAI roles [S12].
- Day 13: coding drills and, if asked, practice with an AI assistant while verifying output (Book 5 Parts 1, 9; Book 1 Part 12) [S10][G].
- Day 14: behavioural stories and project deep dive [S3][S7].

**Common mistakes:**
- Treating the data anomaly as purely statistical without linking it to the product change (reported) [S8].
- Weak SQL on graph-shaped data [S4].
- Over-relying on an AI tool or not verifying its output when allowed [G].
- Giving ML design answers with no metric or latency discussion [S5][G].

**Recent changes and AI-era notes:**
- 2026 candidate and prep-site reports say LinkedIn onsite loops for software engineers include a coding round with AI enabled in CoderPad; no official policy was found, and whether data science or ML roles get it is not confirmed [S10][U].
- LinkedIn's own engineering blog (March 2026) describes an LLM-based feed retrieval and sequential ranking rebuild, and other posts cover LLM ranking served with SGLang, useful context for ML and GenAI roles [S12][S13].
- Several candidate reports are 2018 to 2023 and are older than the AI-era items [S5][S6].
- India: sparse; one 2021 Bengaluru ML anecdote, one 2024 data scientist report, and a listing, no recent detailed loop [S6][S7].

**Sources:**
1. S1: https://careers.linkedin.com/Howwehire - LinkedIn "How We Hire"; snippet only covered accommodation requests, no round detail. Seen 2026-10-31. Snippet only.
2. S2: https://static.glassdoor.com/answers/what-is-the-interview-process-for-linkedin-data-scientist - Glassdoor answer summary: process lengths, SQL and data storytelling format reports. Seen 2026-10-31. Snippet only; anecdotal.
3. S3: https://www.tryexponent.com/blog/linkedin-interview-process - guide: recruiter screen, virtual onsite 4-5 x 45-60 min, DS 1-2 rounds, hiring manager behavioural, system design for technical roles. Seen 2026-10-31. Snippet only; commercial.
4. S4: https://codemia.io/guides/linkedin-data-scientist - guide: DS round list, SQL graph flavour, stats topics, 4-6 weeks. Seen 2026-10-31. Snippet only; vendor page.
5. S5: https://www.jointaro.com/interviews/companies/linkedin/experiences/machine-learning-engineer-dublin-dublin-january-16-2024-no-offer-negative-a2167ca8/ - 2024 Dublin MLE report: coding, ML design, behavioural; recommender prompts. Seen 2026-10-31. Snippet only; anecdotal (Dublin, not India).
6. S6: https://www.jointaro.com/interviews/companies/linkedin/experiences/machine-learning-engineer-bengaluru-april-1-2021-no-offer-positive-9cea5dbd/ - Bengaluru 2021 MLE report, six rounds. Seen 2026-10-31. Snippet only; anecdotal, single person.
7. S7: https://apna.co/job/1080810623 - India listing, data science software engineer role at LinkedIn's India entity (also the Bengaluru Glassdoor items in the same search). Seen 2026-10-31. Snippet only.
8. S8: https://prachub.com/interview-experiences/linkedin-data-scientist-interview-experience-product-sense-sql-and-a-pandas-group-by-slip - candidate report: product sense, SQL, pandas slip (the January 2026 screen details came from the search summary of related results). Seen 2026-10-31. Snippet only; anecdotal.
9. S9: https://www.1point3acres.com/interview/thread/710489 - MLE onsite with six rounds report. Seen 2026-10-31. Snippet only; anecdotal.
10. S10: https://www.hellointerview.com/blog/linkedin-ai-enabled-coding - reports an AI-enabled coding round in LinkedIn onsite loops (see also https://www.1point3acres.com/interview/thread/1153220). Seen 2026-10-31. Snippet only.
11. S11: https://pcdn-global.jobboardly.com/jobs/staff-data-scientist-754ac1d7 - Staff Data Scientist posting at LinkedIn (level name). Seen 2026-10-31. Snippet only.
12. S12: https://www.zenml.io/llmops-database/next-generation-feed-ranking-with-llms-and-sequential-transformers - summary of LinkedIn's 2026 LLM feed ranking engineering post. Seen 2026-10-31. Snippet only; third-party summary.
13. S13: https://scour.ing/p/https://www.linkedin.com/blog/engineering/ai/turbocharging-linkedins-recommendation-systems-with-sglang - mirror of a LinkedIn engineering post on LLM ranking served with SGLang (the mirror URL is the one seen). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium on loop shape for data science; low-to-medium for ML and GenAI roles and for India specifics.
- Verify with the recruiter and https://careers.linkedin.com: round list, whether AI tools are allowed per round and per role, whether team matching comes after the loop, and India-specific format.
- All candidate content is anecdotal and often older than 2025.

### C9 Adobe (Big Tech)

**Evidence level:** Thin. Adobe's own page was only partly captured; everything about rounds comes from third-party prep sites and anonymous candidate reports that disagree on details [S1][S2].

**Roles seen in sources:** Data Scientist (India and US reports) [S3][S4]; Machine Learning Engineer [S5][S9]; Applied Scientist / ML Scientist / Firefly generative-AI roles appear mainly as job postings, with no published loop [S6][S10]. India postings for ML Engineer and Senior ML Engineer (Firefly) exist in Bangalore and Noida [S9][S10].

**Process overview (as reported):**
1. Recruiter call, described as about 30 minutes: background and motivation [S2] (third-party guide).
2. Hiring manager screen, in some guides before a technical online assessment [S2].
3. Technical online assessment for engineering roles, covering coding and problem solving [S2].
4. Technical interviews, then a final manager, director or behavioural round [S3][S4]. Guides count 4 to 6 rounds in total, varying by role, level and location [S2].
5. For Data Scientist, one guide lists: online assessment, technical interview, manager round, director behavioural round [S3]. Another describes a final round with a take-home presentation to a panel and a case study [S4].
- Duration of individual rounds: not found in sources, except a 75-minute virtual technical interview in software-engineer reports [S8] (anecdotal, not DS/ML). End-to-end time estimates range from 10-15 days (one anecdote) to 2-6 weeks [S2][S3].
- The process varies by team, for example Sensei, Experience Manager or Creative Cloud [S2].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Phone, about 30 min | Background, motivation | [S2] |
| Online assessment | Online, coding-style | Coding and problem solving (engineering); DS guide lists an OA | [S2][S3] |
| Technical interview | Interview with a data scientist or engineer | SQL, ML questions, coding such as k-nearest neighbours or a basic random forest from scratch (anecdotal) | [S3][S5] |
| ML / system design | Design discussion | Design a production fraud-detection system (one DS report); end-to-end ML design (guide) | [S4][S5] |
| Manager / director round | Behavioural, possibly project presentation | Behavioural and business-impact discussion | [S3] |
| Case study / presentation | Panel presentation, per one guide | Analytical case; guide calls it the most critical part | [S4] |

**Question types:**
- SQL, described as consistently and heavily weighted in DS reports [S4].
- Probability and statistics; web analytics and Adobe Analytics questions in one India-based report (anecdotal) [S4].
- ML fundamentals plus coding from scratch (k-nearest neighbours, matrix multiplication, a PyTorch classifier, basic random forest), anecdotal [S5].
- ML system design, for example fraud detection with data pipelines and A/B testing (one Bengaluru report, anecdotal) [S4].
- For Firefly-type roles, a third-party guide lists coding, ML and generative-AI depth, and system design on diffusion and LLM features [S6]; a Blind post on a software-engineer Firefly loop reports 2 coding, 1 system design, 1 behavioural/GenAI round (anecdotal, not an ML role) [S7].

**Sample questions (illustrative):**
- Write a SQL query for week-over-week retention of users of a creative app. [illustrative] (Book 3 Part 6 date/time retention and cohorts)
- Implement k-nearest neighbours from scratch in NumPy and discuss complexity. [S5] (Book 1 Part 8 deep learning/from scratch and Book 1 Part 12 live-coding)
- Design a production fraud-detection system: data, features, model, monitoring. [S4] (Book 1 Part 11 ML system design)
- Our A/B test on a new export button shows a small lift; do you ship? [illustrative] (Book 1 Part 10 A/B testing; Book 6 Part 4 experiment design)
- Explain how you would add a text-to-image feature check for quality drift in a diffusion model. [illustrative] (Book 2 Part 9 LLM evaluation; Book 6 Part 7 GenAI scenarios)
- Walk through a project where your analysis changed a business decision. [illustrative] (Book 6 Part 6 stakeholder trade-offs)
- Compute the median session length from a skewed events table using window functions. [illustrative] (Book 3 Part 4 window functions)

**What they score:** The sources do not publish a rubric. Guides say the process is built around company values such as honesty and creativity, from a low-authority source [S2]. Reports emphasise SQL, ML fundamentals, case-study reasoning and business impact [S3][S4]. Treat as unverified beyond that [U].

**Level notes:** An ML Scientist posting lists level P40 with P30 and P50 as additional levels [S10]. India reports mention MTS-1 and MTS-2 titles for software roles; MTS-2 candidates are reportedly asked to present a business-impact project [S4] (anecdotal). Expectations by level are otherwise not found in sources.

**Preparation plan (2 weeks):**
- Days 1-3: SQL, cohorts, retention, window functions (Book 3 Parts 4, 5, 6, 8).
- Days 4-6: ML fundamentals and from-scratch coding (Book 1 Parts 8 and 12; Book 5 Part 1 arrays and hashing for the coding screen) [G].
- Days 7-9: Statistics, A/B testing, probability (Book 1 Parts 10, 13, 14).
- Days 10-11: ML system design and generative-AI design (Book 1 Part 11; Book 2 Parts 12 and 9).
- Days 12-13: Case study and project presentation practice (Book 6 Parts 4, 5, 10).
- Day 14: Mock loop and behavioural stories [G].

**Common mistakes:**
- Treating one candidate's round list as the process; reports disagree and teams differ [S2].
- Neglecting SQL because the role says ML; reports call SQL a heavy theme [S4].
- Presenting model accuracy without business impact for the case or manager rounds [S3][S4].
- Preparing only DSA for a Firefly-type role when guides list ML and generative-AI depth [S6] (unverified, third-party).

**Recent changes and AI-era notes:**
- A third-party guide says AI tools are generally not allowed in live Adobe software-engineering interviews unless the interviewer invites them or an accommodation is approved, and that Adobe asks candidates not to use AI recording or scribing tools [S11]. This is not an Adobe statement and concerns engineering interviews; confirm with the recruiter.
- A 2026-dated guide describes an AI-engineer loop with coding, ML depth and ML system design rounds [S6] (third-party).
- Report dates span 2015 to 2026; older reports (such as take-home analysis on an open dataset) may be out of date [S4].

**Sources:**
- S1. https://www.adobe.com/careers/interviewing-at-adobe : Adobe careers page; snippet-only, partly captured; supports that recruiters follow up after interviews. Seen 2026-10-31.
- S2. https://designgurus.io/answers/detail/how-many-rounds-of-interview-are-there-in-adobe : third-party answer; 4 to 6 rounds, team variation, recruiter call and manager screen as described in the search summary (several guides summarised together, per-URL attribution not visible); snippet-only. Seen 2026-10-31.
- S3. https://www.interviewquery.com/guides/adobe-data-scientist : DS loop as OA, technical, manager, director; SQL heavy; snippet-only. Seen 2026-10-31.
- S4. https://dataford.io/interview-guides/adobe/data-scientist/experiences : DS candidate reports (final round presentation, case study, fraud-detection design, India-based reports); the search summary also drew on Glassdoor India reviews, e.g. https://www.glassdoor.co.in/Interview/Adobe-Interview-E1090-RVW28151557.htm; per-claim mapping uncertain; snippet-only. Seen 2026-10-31.
- S5. https://interviewquery.com/interview-guides/adobe-machine-learning-engineer : ML engineer guide, ML design round, candidate coding reports; snippet-only. Seen 2026-10-31.
- S6. https://codemia.io/guides/adobe-ai-engineer : 2026 third-party guide for AI engineer loop (Firefly-era); snippet-only. Seen 2026-10-31.
- S7. https://www.teamblind.com/post/swe-interview-at-adobe-firefly-uyv1jj1q : anecdotal SWE Firefly loop; snippet-only. Seen 2026-10-31.
- S8. https://www.designgurus.io/answers/detail/what-is-the-adobe-interview-process-like-round-by-round : third-party; used for the 75-minute virtual technical interview report as summarised for software engineers; per-URL attribution uncertain; snippet-only. Seen 2026-10-31.
- S9. https://careers.adobe.com/us/en/job/R151663/Machine-Learning-Engineer : Adobe job posting for ML Engineer; supports roles existing; snippet-only. Seen 2026-10-31.
- S10. https://jobs.anitab.org/companies/adobe-software-2/jobs/49581714-machine-learning-scientist : job board posting, level P40; snippet-only. Seen 2026-10-31.
- S11. https://www.datainterview.com/blog/adobe-software-engineer-interview : third-party guide on AI-tool policy for live interviews; snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low to medium. Rounds, counts and timelines are third-party and anecdotal; the Adobe page gave little. Verify on adobe.com/careers and with your recruiter: the number of rounds for your team, whether a take-home or presentation is used, whether AI tools are allowed, and the India office loop (no Bangalore or Noida DS/ML-specific loop was found beyond a few reports) [U].

### C10 Salesforce (Big Tech)

**Evidence level:** Thin. No Salesforce-published process was found; sources are third-party guides and a small number of anonymous candidate reports that conflict on round counts [S1][S2].

**Roles seen in sources:** Data Scientist [S1]; Research Scientist / applied scientist (AI research) [S3][S4]; Machine Learning Engineer, including Hyderabad and Bangalore postings and Agentforce platform ML roles [S5][S6][S7]; India software engineer (MTS/SMTS) reports used as a proxy only, none ML-specific [S8].

**Process overview (as reported):**
1. Recruiter screen, consistently the first step, short call on resume and background [S1].
2. Technical phone screen or online coding assessment; for ML Engineer a guide describes a coding and problem-solving assessment (Python, ML frameworks) followed by an introductory interview [S5].
3. Technical rounds covering SQL, ML, statistics (Data Scientist) [S1]; ML theory and generative AI "under the hood" (ML Engineer, per a guide built from candidate reports) [S6].
4. Final or onsite rounds with behavioural questions often interspersed through each interview [S2]; for research roles, reviews describe a research screen then an onsite of 4 interviews [S4] (anecdotal).
- Round count: guides say 4, 6 or 7 rounds for Data Scientist [S1]; the process is described as decentralised, varying by team [S2].
- Duration of each round: not found in sources. End to end, 2 to 6 weeks by guides [S1][S2]; one 2023 applied scientist reviewer reported 2 months (anecdotal) [S3].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Short phone call | Resume, qualifications, background | [S1] |
| Technical screen / assessment | Phone or online | SQL (DS); Python and ML coding (MLE) | [S1][S5] |
| Technical rounds | Interviews | ML, statistics, probability, DSA; ML theory and GenAI for MLE | [S1][S6] |
| Research / applied science onsite | 4 interviews per one review | ML basics, simple coding, system design, discussion of own research | [S4] |
| Final / behavioural | Interspersed or separate | Values and culture fit, past experience | [S1][S2] |

**Question types:**
- A guide's tally of reported DS question categories: data structures and algorithms, SQL, machine learning, probability, statistics (counts from the guide, not verified) [S1].
- Case-style business reasoning for Data Scientist in one guide's 4-round version [S1].
- Research roles: project deep-dives, ML and deep-learning fundamentals, easy-to-medium coding, implementing sparse self-attention (one anecdotal report) [S3][S4].
- India engineering reports (not ML): three medium coding problems in an hour, low-level design, system design [S8] (anecdotal).

**Sample questions (illustrative):**
- Write a SQL query for the top 3 accounts by monthly usage with a ranking window function. [illustrative] (Book 3 Part 4 window functions)
- Explain how you would predict opportunity win probability and validate it. [illustrative] (Book 1 Part 11 ML system design; Book 6 Part 5 business cases)
- Implement sparse self-attention and explain its trade-offs. [S3] (Book 2 Part 1 transformer internals)
- Describe a complex mathematical problem you solved, the methods used and the impact. [S3] (Book 6 Part 6 stakeholder trade-offs; Book 1 Part 13 statistics)
- Your RAG agent for customer support hallucinates account details; how do you evaluate and reduce it? [illustrative] (Book 2 Parts 6, 9 and 8; Book 6 Part 7 GenAI scenarios)
- Solve a medium graph or matrix BFS problem and state complexity. [S8] (Book 5 Part 9 graphs)
- Explain precision versus recall for lead scoring when positives are rare. [illustrative] (Book 6 Part 3 imbalanced data)

**What they score:** No published rubric. Sources point to technical depth (SQL, ML, coding), communication in ambiguous problems [S1] and culture and values fit [S1][S2]; for research roles, depth on your own work [S3].

**Level notes:** India engineering postings use MTS, SMTS and LMTS titles, and a Lead ML Engineer title appears [S7][S8]; Salesforce data-science level expectations were not found in sources [U]. Senior roles may add a panel interview [S2].

**Preparation plan (2 weeks):**
- Days 1-3: SQL and metrics (Book 3 Parts 3, 4, 6, 8).
- Days 4-6: ML fundamentals, statistics, probability (Book 1 Parts 3-5, 13, 14).
- Days 7-8: Coding practice at easy-to-medium level (Book 5 Parts 1, 7, 9) [G].
- Days 9-11: GenAI and agents, RAG evaluation (Book 2 Parts 6-9, 12) since Agentforce roles list LLM experience [S7].
- Days 12-13: Business case and behavioural stories (Book 6 Parts 5, 6, 10).
- Day 14: Project deep-dive rehearsal and mock [G].

**Common mistakes:**
- Assuming one round count; sources range from 4 to 7 [S1].
- Giving only technical answers when behavioural questions are woven into every round [S2].
- Skipping coding prep for DS roles, where DSA was the most-reported category in one guide [S1].
- Weak project narratives for research or applied roles [S3][S4].

**Recent changes and AI-era notes:**
- Salesforce postings say AI tools help recruiters assess resumes, and that humans make selection and hiring decisions [S9].
- No policy on candidates using AI tools in interviews was found; check with your recruiter [U].
- Current ML postings (for example November 2025) reference LLMs, prompt engineering and the Agentforce platform [S7]. Older candidate reports (2019 to 2023) predate this [S3][S8].

**Sources:**
- S1. https://www.interviewquery.com/interview-guides/salesforce-data-scientist : DS guide; round counts 4/6/7, question categories, 2-4 week timing; snippet-only. Seen 2026-10-31.
- S2. https://tryexponent.com/blog/salesforce-interview-process : third-party guide; search summary combined several guides (decentralised process, 3-6 weeks, behavioural interspersed, panel for senior roles); per-URL attribution uncertain; snippet-only. Seen 2026-10-31.
- S3. https://www.interviewquery.com/interview-guides/salesforce-research-scientist : research scientist guide and Glassdoor-based reports (2019, 2023, 2024 anecdotes); snippet-only. Seen 2026-10-31.
- S4. https://www.glassdoor.com.hk/Interview/Salesforce-Interview-E11159-RVW25902909.htm : anecdotal Glassdoor review, research screen plus 4-interview onsite (mapping among listed reviews uncertain); snippet-only. Seen 2026-10-31.
- S5. https://interviewquery.com/interview-guides/salesforce-machine-learning-engineer : ML engineer stages; snippet-only. Seen 2026-10-31.
- S6. https://dataford.io/interview-guides/salesforce/machine-learning-engineer : ML theory and generative AI emphasis, built from candidate reports; snippet-only. Seen 2026-10-31.
- S7. https://www.themuse.com/jobs/salesforce/machine-learning-engineer-hyderabad-bangalore : ML Engineer posting, Hyderabad and Bangalore, posted November 2025; snippet-only. Seen 2026-10-31.
- S8. https://leetcode.com/discuss/interview-experience/4205025/ : anecdotal SMTS Bengaluru October 2023 software-engineer report (one hour, three medium problems); snippet-only. Seen 2026-10-31.
- S9. https://builtin.com/job/lead-forward-deployed-engineer-agentforce/6225088 : Salesforce posting language on AI tools used by recruiters and human decisions (statement appeared across postings in results); snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low. Verify with your recruiter: your team's round count and format, whether there is a take-home or live ML exercise, behavioural expectations, India (Hyderabad, Bangalore) loop details, and the policy on AI tools. No India DS/ML-specific interview rounds were found [U].

