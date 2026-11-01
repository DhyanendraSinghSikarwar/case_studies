# B7P01 C01-02 profiles

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
