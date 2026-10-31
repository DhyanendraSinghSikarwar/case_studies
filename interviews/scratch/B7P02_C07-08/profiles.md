### C7 Meesho (Indian e-commerce unicorn)

**Evidence level:** Thin. No official Meesho interview page appeared; the data science material is aggregator guides, a few job listings and anecdotal reviews that disagree on the number of rounds (2 to 4), and nothing specific to applied scientist or GenAI interview loops was found [S1][S2][S4][S9].

**Roles seen in sources:** Data Scientist I (campus and experienced, 0-2 years listings) [S2][S4], Data Scientist 2 (a Blind thread title only) [S12], Principal and senior principal data scientist postings mentioning LLM operations [S11], AI Engineer (third-party guide, few specifics) [S5]. No Applied Scientist interview write-up was found [S6]. Work areas listed in a posting: ranking and recommender systems, computer vision for seller listings, fraud detection, ads and monetisation modelling [S4].

**Process overview (as reported):**
1. Resume screening [S2][S3].
2. Online or AI-judged screening and/or an online coding test. One write-up reports an AI-judged screen followed by a coding test of 3 problems in 105 minutes (anecdotal, one candidate) [S3]. The 2025 open-campus drive used a virtual 165-minute HackerEarth test with elimination rounds (campus, mostly software roles) [S10].
3. One or two technical interviews. A Data Scientist I listing tied to the 2025 campus drive lists two technical interviews [S2]. A ClanX listing for Data Scientist 1 lists four stages: DSA, math and statistics (90 minutes), ML breadth (60 minutes), ML depth (60 minutes), then hiring manager [S4]. Interview Query, based on about five candidate reports, describes two rounds, the first about 90 minutes mixing coding, SQL, maths and statistics, resume projects, ML/DL fundamentals and PySpark [S1].
4. Hiring manager or HR/managerial round [S2][S4][S6].
5. Guides stress that there is no single Meesho process and that rounds vary by role, level, team and hiring programme [S9]. Total rounds: 2 to 4 depending on source [S1][S2][S4]. Overall calendar duration not found in sources.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Resume screen | Offline | Fit with role | [S2][S3] |
| Online screen / coding test | AI-judged screen and/or timed test (105 min in one anecdote) | Coding, SQL, statistics, PySpark | [S3][S1] anecdotal |
| Technical 1 | Live, about 90 min in one guide | Resume walkthrough, DSA, broad ML, SQL, statistics | [S1] |
| Technical 2 / ML depth | Live, 60 min in one listing | Project deep dive, ML/DL depth, trade-offs | [S1][S4] |
| Hiring manager | Live | Experience, problem solving, fit | [S2][S4][S6] |

**Question types:**
- SQL and analytics [S6][S1].
- Statistics, listed as a very high frequency topic in one guide [S1].
- DSA coding: one reported question was a graph problem solved with union-find (anecdotal) [S1].
- PySpark in the online assessment or interview (anecdotal) [S1].
- ML project follow-ups: feature engineering, loss functions, imbalanced data, leakage, monitoring, A/B testing, concept drift (candidate-reported) [S1].
- Recommendation and ranking design: "how would you build a recommendation engine for Meesho" [S3].
- LLM inference cost: how to speed up and cut cost for a fine-tuned LLM product search system (one interview write-up, secondhand, anecdotal) [S9].

**Sample questions (illustrative):**
- How would you build a recommendation engine for a marketplace with many new sellers and sparse history? [S3] Book 1 Part 7 (recommenders, ranking, search).
- Write a SQL query for week-over-week repeat purchase rate by city. [illustrative] Book 3 Part 6 (retention, cohorts) and Part 8 (funnels, product metrics).
- You have equations like a=b, b=c, a!=c; decide if all can be satisfied. [S1] Book 5 Part 9 (graphs, union-find).
- Your fraud model has high accuracy but misses most fraud; what do you change? [illustrative] Book 1 Part 3 (imbalance, thresholding) and Book 6 Part 3 (imbalanced data situations).
- Design an A/B test for a new ranking on the home feed and say how you would read an ambiguous result. [illustrative] Book 1 Part 10 (A/B testing) and Book 6 Part 4 (ambiguous A/B results).
- How would you make a fine-tuned LLM product search system faster and cheaper to serve? [S9] Book 2 Part 10 (deployment, latency, cost) and Part 4 (fine-tuning, distillation).
- Pick a project from your resume: what were the leakage risks and how did you monitor drift afterwards? [S1] Book 4 Part 8 (monitoring, drift) and Book 6 Part 2 (model degraded in production).

**What they score:**
- Core fundamentals: coding, SQL, statistics, ML basics, as the first technical stage mixes them [S1][S4].
- Depth on your own projects, with technical follow-ups on algorithms you name [S1].
- Practical, scale-aware ML: engineering write-ups describe a ranking platform with many concurrent experiments and many ranking models, which suggests experimentation familiarity matters, but this is inference from engineering blogs, not an interview statement [S7][S8][U].
- Manager fit and problem-solving approach [S6].

**Level notes:**
- Data Scientist I: 0-2 years of experience listed, campus and experienced hiring [S2][S4].
- Data Scientist 2 appears as a Blind thread title; contents not seen [S12].
- Principal / senior principal postings emphasise distributed computing, large-scale model training, LLM operations and inference optimisation [S11]. Interview format for these levels not found.

**Preparation plan (2 weeks):**
- Days 1-2: SQL window functions, cohorts, funnels. Book 3 Parts 4-6 and 8.
- Days 3-4: Statistics and hypothesis testing. Book 1 Parts 13-14; A/B testing Book 1 Part 10.
- Days 5-6: Core ML, metrics, imbalance, boosting. Book 1 Parts 2-4.
- Days 7-8: Recommenders and ranking, since Meesho work areas are ranking and recommendations [S4][S7]. Book 1 Part 7.
- Days 9-10: DSA with a timer, including graphs and union-find, arrays, sliding window. Book 5 Parts 1, 2, 9 [G].
- Days 11-12: Be ready to defend each resume project end to end; production ML and drift. Book 4 Parts 8 and 6; Book 6 Part 2.
- Days 13-14: GenAI/LLM serving if the role is GenAI (Book 2 Parts 4, 10, 12), then two full mocks. Behavioural: Book 6 Part 6.

**Common mistakes:**
- Listing a project you cannot explain at algorithm level; guides warn of technical follow-ups on any named method [S1].
- Preparing only ML theory and skipping SQL or DSA when the first stage mixes both [S4][S1].
- Treating one candidate's round count as the standard; sources disagree [S9][G].
- Ignoring scale: a ranking answer with no experimentation or serving plan [U].

**Recent changes and AI-era notes:**
- An AI-based screening round appears in one intern track and a write-up of a data science candidate, a recent practice for some programmes; scope beyond those is not confirmed [S9][S3].
- 2025 campus hiring ran fully virtual with elimination rounds [S10].
- LLM-related postings exist at principal level [S11]. No reliable source on Meesho's policy on AI tools during interviews was found.
- Older: Glassdoor and Naukri reports are mostly software engineering and span several years [S6].

**Sources:**
- S1: https://www.interviewquery.com/guides/meesho-data-scientist . Supports: 2-round description (about 90 min first round), topics (statistics, SQL, PySpark, ML/DL, projects), project follow-up themes, union-find DSA example; the project-follow-up and DSA details come from the search summary of this and related Interview Query pages. Seen 2026-10-31. Snippet only.
- S2: https://jobs.weekday.works/meesho-data-scientist-i-57fq . Supports: Data Scientist I listing with resume screen, two technical interviews, hiring manager round (campus drive, May 2025); the four-round outline was attributed to a Data Scientist-I listing in the search summary, page-to-detail match not certain. Seen 2026-10-31. Snippet only.
- S3: https://www.placementpreparation.io/blog/?p=17256 . Supports: one candidate's 4 rounds with AI-judged screen and 3-problem 105-minute test; recommendation-engine question; last updated Oct 2025 (anecdotal). Seen 2026-10-31. Snippet only.
- S4: https://jobs.clanx.ai/o/data-scientist-1 . Supports: four-stage format (DSA/math/statistics 90 min, ML breadth 60, ML depth 60, hiring manager), work areas, 0-2 years. Job listing by a third-party board. Seen 2026-10-31. Snippet only.
- S5: https://www.interviewquery.com/prep-guides/meesho-ai-engineer . Supports: AI Engineer guide, recruiter screen then loop on algorithms, ML systems, experimentation, communication; few specifics, third party. Seen 2026-10-31. Snippet only.
- S6: https://fr.glassdoor.ch/Entretien/Meesho-Entretien-E1503776-RVW89484253.htm . Supports: Glassdoor reviews of two technical rounds on SQL and analytics then HR/managerial round (anecdotal; the page-to-detail match is from a summary of several Glassdoor results); no Applied Scientist reports surfaced. Seen 2026-10-31. Snippet only.
- S7: https://www.meesho.io/blog/rebuilding-meeshos-ranking-platform . Supports: Meesho engineering blog on ranking platform, nearly a hundred ranking experiments running, third-generation architecture. Seen 2026-10-31. Snippet only.
- S8: https://aws.amazon.com/blogs/machine-learning/how-meesho-built-a-generalized-feed-ranker-using-amazon-sagemaker-inference . Supports: generalized feed ranker case study on SageMaker (vendor blog). Seen 2026-10-31. Snippet only.
- S9: https://www.designgurus.io/answers/detail/what-is-the-meesho-interview-process-like-round-by-round . Supports: no single Meesho process; rounds vary by role, level, team and programme; AI-based screening for an internship track (summary also drew on a Fueler guide); LLM inference-cost question write-up is from the same search summary, source page not pinned. Seen 2026-10-31. Snippet only.
- S10: https://www.hackerearth.com/challenges/hackathon/meesho-open-campus-recruitment-2025/custom-tab/hiring-process/ . Supports: 2025 open campus test, 165 minutes, virtual, elimination rounds. Seen 2026-10-31. Snippet only.
- S11: https://career.io/job/principal-data-scientist-bengaluru-meesho-54d412d96557a42f3dd82b20047d78f7 . Supports: Principal Data Scientist posting, distributed computing, large-scale model training, LLM Ops, inference optimisation. Seen 2026-10-31. Snippet only.
- S12: https://www.teamblind.com/post/interview-for-data-scientist-2-meesho-vljumdtk . Supports: existence of a Data Scientist 2 interview thread; no answers or details seen. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence in round count and order; the only stable pattern is screening, one or two technical rounds mixing coding, SQL, statistics and ML, then a manager round [S1][S2][S4].
- Nothing found for applied scientist or GenAI loops specifically; do not assume they match the data scientist I listings [S6][S11].
- Duration of the whole process and per-round time (other than the listing figures) not found in sources.
- Verify on Meesho's careers page and with the recruiter: round list for your role, whether an AI-judged screen applies, and any AI-tool policy.
- Pay is out of scope for this book.

### C8 Ola (Indian mobility company)

**Entity note:** Three names appear in sources and they are not the same hiring pool. "Ola" below means the consumer ride-hailing and mobility company (listed on Glassdoor under Ola; the registered entity name ANI Technologies was seen in one search summary) [S1][S7]. Ola Electric is the separate EV maker; its interview material is EV, battery and manufacturing focused and ML-specific reports are sparse [S5][S14]. Krutrim is the group's AI venture; sources cover hiring pushes and layoffs, not its interview loop [S10][S11][S12][S13]. Where a source does not say which entity it means, the profile says so.

**Evidence level:** Thin. There is no Ola-specific data science or ML engineer process page; the data science evidence is a handful of small, dated Glassdoor reports (4 submitted interviews in the data science view), a question bank and software-engineer-focused prep guides [S1][S2][S3][S8].

**Roles seen in sources:** Data Scientist and Data Scientist III on Glassdoor, mostly Ola, 2016-2021 era (anecdotal) [S1][S6]; ML questions for "Ola data scientist" on Prepfully (entity not stated) [S8]; a Research Engineer, Machine Learning profile mentioning smart mobility, entity unclear (profile only, no interview details) [S9]; Ola Electric AI Research listing (no process) [S14]; Krutrim foundation-model roles: generative AI research engineer, distributed training, speech and audio foundation models, alignment/RL research engineer [S10]. No Applied Scientist or GenAI interview reports for any Ola entity were found.

**Process overview (as reported):**
1. Entry is by recruiter, online application or campus; for software engineer roles guides describe 3 to 5 rounds plus a short HR call, varying by team and level [S2][S4].
2. Data science, as reported (anecdotal, small sample): a video interview with machine learning and data science questions and detailed discussion of past projects and resume [S6][S1]; one Data Scientist III report covered ANOVA and a sliding window coding problem (New Delhi, Nov 2021, no offer) [S1]; another listed tree-based algorithms, NLP and data structure coding [S1].
3. Another candidate described three rounds: technical, manager, HR, with advanced SQL (not role-specific) [S1].
4. Managerial round: one guide says it focuses on ownership and asks about one project in detail, including the parts you did not build yourself (software engineer context) [S2][S3].
5. Timeline: a guide says the process typically wraps up in 2 to 4 weeks (software engineer context); the data science Glassdoor view reports about 1 day to hire, from 4 submissions, which is too small to rely on [S3][S1].
6. Ola Electric and Krutrim loops: not found. Guides note that consumer mobility, Krutrim, software, operations and Ola Electric roles can use different screens [S4].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / application screen | Call or online | Background, role match | [S2] (SWE context) |
| Technical (DS) | Video call | ML and data science concepts, DL/ML algorithms, tree-based models, NLP, project and resume discussion | [S6][S1] anecdotal |
| Coding | Live | Data structures, sliding window style problem | [S1] anecdotal |
| SQL / Python | Live or test | Advanced SQL, Python scripting (role not stated) | [S1] anecdotal |
| Manager | Live | Ownership, project depth | [S2][S3] SWE context |
| HR | Short call | Fit | [S1][S2] |

**Question types:**
- Deep learning and ML fundamentals: gradient descent in training, batch normalisation versus instance normalisation (Prepfully question bank; entity not stated) [S8].
- Statistics: ANOVA (one Data Scientist III report, anecdotal) [S1].
- Tree-based algorithms and NLP (anecdotal) [S1].
- Coding: sliding window, data structures [S1].
- SQL and Python scripting (anecdotal) [S1].
- Project and resume deep dive [S6][S1].
- Ola Electric interviews, per one prep page, centre on EV, battery, cell, manufacturing, software and field topics; ML content sparse [S5].

**Sample questions (illustrative):**
- Explain how gradient descent behaves in training and what changes with a smaller batch. [S8] Book 1 Part 8 (deep learning, optimizers).
- Compare batch normalisation and instance normalisation; when would each be used? [S8] Book 1 Part 8 (deep learning, PyTorch from scratch).
- Run a one-way ANOVA by hand on three driver-incentive groups and say what the F statistic tells you. [S1] Book 1 Part 13 (hypothesis tests incl. ANOVA).
- Find the longest window of trips with at most K cancellations. [S1] Book 5 Part 2 (sliding window).
- Predict ride ETA or surge demand per zone; choose features, metric and a fallback when data is late. [illustrative] Book 1 Part 6 (time series) and Part 11 (ML system design: ETA, pricing).
- Write SQL for driver acceptance rate by hour with a 7-day moving average. [illustrative] Book 3 Part 5 (running totals, moving averages) and Part 8 (product metrics).
- Walk me through one project, including the parts you did not build yourself. [S2] Book 6 Part 6 (stakeholder conflicts, trade-offs) and Part 10 (design a solution end to end).

**What they score:**
- ML and data science concept depth, tied to projects on your resume [S6][S1].
- Basic coding and data structures [S1].
- Ownership and honesty about your contribution (manager round, SWE context) [S2][S3].
- Beyond this, no stated rubric was found [U].

**Level notes:**
- Level names seen: Data Scientist and Data Scientist III on Glassdoor [S1]. Expectations by level not found.
- Krutrim postings span lead and senior research and engineering titles in foundation AI (speech and audio models, distributed training, alignment/RL) [S10]; interview expectations not found.

**Preparation plan (2 weeks):**
- Days 1-2: ML fundamentals and tree models. Book 1 Parts 1-4.
- Days 3-4: Deep learning basics: optimizers, normalisation, PyTorch. Book 1 Part 8; NLP basics Part 9.
- Days 5-6: Statistics including ANOVA and hypothesis tests. Book 1 Parts 13-14.
- Days 7-8: SQL: windows, cohorts, product metrics. Book 3 Parts 4-6 and 8.
- Days 9-10: Coding: sliding window, arrays, strings, no autocomplete. Book 5 Parts 1-3 [G].
- Days 11-12: Time series and ML system design for mobility problems (ETA, pricing, demand). Book 1 Parts 6 and 11 [G].
- Days 13-14: Walk through two resume projects at full depth, then mocks. Book 6 Parts 2, 6, 10.
- If aiming at Krutrim GenAI roles: swap days 9-12 for Book 2 Parts 1, 2, 4, 10 [G]; loop format unknown.

**Common mistakes:**
- Applying the same prep to Ola, Ola Electric and Krutrim; sources suggest different screens and focus areas [S4][S5].
- Being unable to discuss project parts you did not build [S2].
- Weak statistics basics when ANOVA-style questions appear in reports (anecdotal) [S1].
- Treating a single Glassdoor report from 2016-2021 as the current process [S1][G].

**Recent changes and AI-era notes:**
- No source describes Ola's use of AI tools or in-person versus virtual policy in interviews. Not found.
- Krutrim (group AI venture): a hiring push for foundation AI roles was reported (date not clear in snippet) alongside senior exits [S10][S11]; about 100 staff reportedly let go in July 2025 and 50 more in September 2025, mostly linguistics roles [S13]; in July 2026 reports said Krutrim let go of roughly half its remaining staff as it pivots to AI cloud, with product and engineering affected, though Krutrim did not confirm numbers and sources conflict on counts [S12]. This affects job stability research, not the interview format.
- Older: nearly all Glassdoor interview reports for Ola data science predate 2023 [S1][S6].

**Sources:**
- S1: https://static.glassdoor.co.in/Interview/Ola-Data-Science-Interview-Questions-EI_IE587383.0,3_KO4,16.htm . Supports: Glassdoor data science view for Ola (difficulty 3.7 of 5, 4 submitted interviews, about 1 day to hire), DL/ML discussion based on projects, tree-based and NLP topics, Data Scientist III Nov 2021 report (ANOVA, sliding window), three-round technical/manager/HR report; several items come from a search summary of Glassdoor pages whose exact URLs were not pinned. Anecdotal, small sample. Seen 2026-10-31. Snippet only.
- S2: https://www.designgurus.io/answers/detail/what-is-the-ola-interview-process-like-round-by-round . Supports: 3-5 rounds plus HR call for SWE, shorter campus process, manager round on one project incl. parts you did not build. Third party. Seen 2026-10-31. Snippet only.
- S3: https://www.techprep.app/blog/ola-interview-process . Supports: 2-4 weeks, 4-5 rounds, managerial round focused on ownership (SWE context). Third party, 2026. Seen 2026-10-31. Snippet only.
- S4: https://hyring.com/jobseeker-toolkit/interview-questions/company/ola . Supports: different screens across consumer mobility, Krutrim, software and Ola Electric roles. Editorial prep site. Seen 2026-10-31. Snippet only.
- S5: https://hyring.com/jobseeker-toolkit/interview-questions/company/ola-electric . Supports: Ola Electric interviews EV, battery, manufacturing focused; ML sparse. Editorial prep site. Seen 2026-10-31. Snippet only.
- S6: https://static.glassdoor.co.in/Interview/Ola-Interview-E587383-RVW49830263.htm . Supports: recruiter-sourced candidate, video interview on ML and data science with project questions (anecdotal; date not seen). Seen 2026-10-31. Snippet only.
- S7: https://www.glassdoor.co.uk/Interview/Ola-Interview-E587383-RVW13356756.htm . Supports: Ola Glassdoor interview page (entity listing; the ANI Technologies incorporation detail was in the accompanying search summary, not clearly this page). Seen 2026-10-31. Snippet only.
- S8: https://prepfully.com/interview-questions/ola/data-scientist?page=3 . Supports: Ola data scientist ML question bank (gradient descent, batch versus instance normalisation); entity not stated. Seen 2026-10-31. Snippet only.
- S9: https://www.weekday.works/people/aravind-naidu-aravind-naidu . Supports: a Research Engineer ML profile (smart mobility); entity unclear; no interview detail. Seen 2026-10-31. Snippet only.
- S10: https://analyticsindiamag.com/ai-news-updates/krutrim-begins-hiring-for-multiple-foundation-ai-roles . Supports: Krutrim foundation AI roles in US, Singapore, Bengaluru; role titles. Krutrim entity. Seen 2026-10-31. Snippet only.
- S11: https://inc42.com/buzz/ola-steps-up-hiring-for-krutrim-ai-labs-amid-exits-report . Supports: Krutrim hiring push amid senior exits. Krutrim entity. Seen 2026-10-31. Snippet only.
- S12: https://yourstory.com/2026/07/krutrim-lays-off-nearly-half-workforce . Supports: July 2026 reported cuts and AI cloud pivot. Krutrim entity. Seen 2026-10-31. Snippet only.
- S13: https://www.outlookbusiness.com/start-up/news/bhavish-aggarwals-ola-krutrim-cuts-50-more-jobs-in-its-third-layoff-round . Supports: 2025 Krutrim layoff rounds. Krutrim entity. Seen 2026-10-31. Snippet only.
- S14: https://www.teamlease.com/jobs/product-ai-research-jobs-in-bangalore-ola-electric-1416181 . Supports: Ola Electric Product AI Research listing exists (no process detail). Ola Electric entity. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence overall. Data science reports are few, small and mostly older; software-engineer guides are the only structured descriptions [S1][S2][S3].
- Nothing was found for applied scientist or GenAI interview loops at any Ola entity; Krutrim sources are hiring and layoff news only [S10][S12].
- Confirm which entity (Ola, Ola Electric or Krutrim) the posting belongs to, and ask the recruiter for the round list, durations and any AI-tool policy; none was found in sources.
- Pay is out of scope for this book.
