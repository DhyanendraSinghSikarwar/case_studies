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
