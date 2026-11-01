### C9 Grab (super-app)

**Entity and office note:** Grab Holdings is headquartered in Singapore [S3]. Sources below refer to different offices: Singapore (Glassdoor and postings), Kuala Lumpur (Malaysia), Jakarta (Indonesia), Bangkok and Bengaluru, and each is named where the source says so [S1][S6][S5][S11]. Office is not always stated in a snippet; where it is not, it is marked "office not stated".

**Evidence level:** Thin. There is an official careers page with a timeline and stage length [S2] and an official engineering-blog post, but that post is about software engineers in Singapore and is older [S3]. Data science and ML evidence is a handful of anonymous Glassdoor reviews across roles, years and offices, plus third-party guides [S1][S6][S7][S8]. No Reddit or Blind thread appeared [U].

**Roles seen in sources:** Data Scientist (analytics, Singapore, 2025 report) [S1]; Senior Data Scientist (Kuala Lumpur, 2021 report) [S1]; Machine Learning Engineer (Kuala Lumpur, August 2025 report) [S6]; Data Engineer (take-home reports, offices not confirmed) [S5]; postings for Senior Data Scientist (recommendation, Singapore), Senior ML Engineer (fulfilment) and Data Scientist (GrabFin) [S10]. Research Scientist guide exists [S7]. No Applied Scientist or GenAI-titled interview report was found [U].

**Process overview (as reported):**
1. Official statement: the process takes about a month from first conversation to outcome, and each interview stage typically lasts 30 minutes to 1 hour [S2]. Number of rounds depends on role and seniority [S3]. Candidate reports of 2 to 4 weeks, and one of about 40 days as a Glassdoor average for Senior Data Scientist from 9 submissions, differ [S1][S4].
2. Recruiter or HR call first [S1][S4].
3. For some data roles, an online test or take-home: MCQ on statistics and ML, basic SQL and algorithm questions (Singapore, 2025, anecdotal) [S1]; a take-home SQL and data analysis assignment on a Grab-provided dataset (anecdotal) [S1]; a Python and SQL assessment of about two hours described as tough (Kuala Lumpur 2025 and Jakarta 2023, Data Engineer, anecdotal) [S5].
4. Technical interviews. One Senior Data Scientist report (Kuala Lumpur, 2021, anecdotal): tech lead round on SQL, manager round on ML theory and past projects, director round on behavioural questions [S1]. One ML Engineer report (Kuala Lumpur, August 2025, anecdotal): four rounds, mostly technical with live coding, candidate expected to talk through reasoning [S6].
5. Case study variants: a 2025 Data Scientist report mentions a case study covering stats and ML, then a long wait and rejection (anecdotal) [S1]; one sequence reported as HR, case study, hiring manager, hiring manager's boss (role not stated, anecdotal) [S4].
6. Hiring-manager or senior-leader conversation focused on values and fit; the engineering blog says technical and cultural fit are weighed about equally and fit is critical at the end [S3].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / HR call | Call | Role alignment, background | [S4][S1] |
| Online test or take-home | MCQ, SQL and data analysis, or Python and SQL (about 2 hours, DE) | Statistics, ML basics, SQL, algorithms | [S1][S5] anecdotal |
| Technical interview(s) | Live, with tech lead or engineers | SQL (DS), live coding and reasoning (MLE) | [S1][S6] anecdotal |
| Manager round | Discussion | ML theory, past projects | [S1] anecdotal, 2021 Kuala Lumpur |
| Case study | Presentation or written | Stats, ML, business problem (for example retention drop) | [S1][S4] anecdotal |
| Senior leader / values round | Conversation | Behaviour, values, fit | [S3][S1] |

**Question types:**
- SQL with CTEs and A/B test sizing; walk through a past data science project (candidate-reported) [S7][S1].
- ML theory and algorithms, ranked as very frequent in one guide's question table; a sibling guide rates ML system design and general ML as high-frequency for ML engineer [S7][S8].
- Business case: "how would you solve a drop in customer retention" (anecdotal, 2025) [S1].
- Market-sizing or product questions, for example how many GrabFood orders per day (Bangkok, anecdotal, non-DS role not stated) [S4].
- Behavioural, and a mock-interview opener asking to summarise relevant experience [S8].
- Culture and values: Heart, Hunger, Honour, Humility as listed in a third-party guide [S9].

**Sample questions (illustrative):**
- Write a SQL query using a CTE to find the top three pickup zones by completed rides per week, and note data quality traps. [illustrative] Book 3 Part 3 (Subqueries, CTEs) and Book 3 Part 4 (Window functions: ranking, top-N per group).
- Size an A/B test for a new driver-incentive message and say what metric you would guard. [S1] Book 1 Part 10 (A/B testing, causal inference, experimentation).
- Customer retention in a food-delivery app has dropped; how do you find out why and what do you propose? [S1] Book 6 Part 1 (Product metrics and metric drops) and Book 6 Part 5 (Business case studies).
- Walk me through a past data science project end to end and what you would change. [S7] Book 6 Part 10 ("Design a solution end-to-end" open scenarios).
- Design a ranking model for restaurant recommendations: data, features, metric, serving. [illustrative] Book 1 Part 7 (Recommenders, ranking, search, learning-to-rank) and Book 1 Part 11 (ML system design).
- Design a system to compute average speed of all cars in a city from GPS pings. [S5] Book 4 Part 9 (Feature stores, streaming) and Book 1 Part 11 (ML system design).
- Group words by anagram, then explain the hash-map complexity (live coding warm-up). [illustrative] Book 5 Part 1 (Arrays and hashing) and Book 5 Part 3 (Strings).
- Describe a time you pushed back on a stakeholder deadline. [illustrative] Book 6 Part 6 (Stakeholder conflicts and trade-off decisions).

**What they score:**
- Official statement: each stage is designed to assess specific skills or qualities for the role, and technical candidates are advised to show their problem-solving process [S2].
- Technical and cultural fit weighted roughly equally, with fit decisive at the end (engineering blog, software engineers) [S3].
- Data science: SQL, ML theory, past-project depth, and business reasoning in case studies (anecdotal) [S1][S7].
- Reasoning aloud during live coding (anecdotal) [S6].

**Level notes:**
- Posting titles seen: Data Scientist, Senior Data Scientist, Lead Data Scientist (Analytics), Principal Machine Learning Engineer [S10].
- One Lead Data Scientist posting snippet asked for at least 7 years in large-scale ML systems and at least 3 years in a senior or lead data scientist role; entry-level data scientist postings ask for much less (aggregator snippets, may be stale) [S10].
- Level-specific interview differences were not found in sources [U].

**Preparation plan (2 weeks):**
- Days 1-3: SQL CTEs, windows, cohorts and funnels. Book 3 Parts 3, 4, 6 and 8.
- Days 4-5: Experiment design and sizing. Book 1 Part 10; Book 6 Part 4 (Experiment design and ambiguous A/B results).
- Days 6-7: ML fundamentals and ranking or recommendation. Book 1 Parts 1 and 7.
- Days 8-9: Live coding in a plain editor, talking through reasoning. Book 5 Parts 1 and 3; Book 1 Part 12 (NumPy/pandas/sklearn live-coding) [S6].
- Days 10-11: Case studies: metric drops, retention, marketplace trade-offs. Book 6 Parts 1, 5 and 9 (Domain sets).
- Days 12-13: ML system design and streaming basics. Book 1 Part 11; Book 4 Part 9.
- Day 14: One project walkthrough and values stories, then a timed mock. Book 6 Part 6 [G].

**Common mistakes:**
- Treating every role as a coding-only loop when reports show case studies and take-homes for data roles [S1].
- Skipping the project walkthrough; reports and guides list it as a standard ask [S7][S1].
- Coding silently when interviewers ask for reasoning [S6].
- Ignoring the values and fit stage, which the company says matters at the end [S3].

**Recent changes and AI-era notes:**
- Most recent anecdotes are 2025 (Singapore analytics, Kuala Lumpur ML engineer) and a 2026 Singapore engineering report of two coding and system design rounds plus a manager round (software engineering, anecdotal) [S1][S4]. Older ones are 2019 to 2023 [S5][S11].
- No Grab-specific policy on AI tools in interviews was found; a search returned only other companies' policies. Ask your recruiter [U].
- Postings list Python, SQL and TensorFlow or PyTorch as common skills [S10].

**Sources:**
- S1. https://www.glassdoor.sg/Interview/Grab-Interview-E958580-RVW99961380.htm : first of several Glassdoor Grab reviews returned for the data science query; search summary reports Senior Data Scientist Kuala Lumpur 2021 (three rounds), take-home SQL assignment, Singapore 2025 analytics MCQ, aggregate about 40 days from 9 submissions, 3-week and 2-week reports; per-URL attribution uncertain; snippet-only. Seen 2026-10-31.
- S2. https://grab.careers/en/how-we-hire/ : official Grab page; process about a month, each stage typically 30 minutes to 1 hour, stages assess role-specific skills, show problem-solving; snippet-only. Seen 2026-10-31.
- S3. https://engineering.grab.com/how-grab-hires-engineers-in-singapore : official engineering blog (software engineers, Singapore, older); rounds depend on role and seniority, technical and cultural fit weighed about equally, fit critical at the end; snippet-only. Seen 2026-10-31.
- S4. https://hyring.com/jobseeker-toolkit/interview-questions/company/grab : third-party guide; recruiter call, case study, hiring manager flow, 2026 Singapore engineering report, Bangkok market-sizing question; summary combined several pages; snippet-only. Seen 2026-10-31.
- S5. https://www.glassdoor.sg/Interview/Grab-Interview-E958580-RVW30314473.htm : anecdotal Glassdoor Data Engineer review, second-round geohash surge/congestion take-home (2019), Jakarta/Kuala Lumpur Python and SQL assessments in other results; office not confirmed; snippet-only. Seen 2026-10-31.
- S6. https://www.glassdoor.com.hk/Interview/Grab-Interview-E958580-RVW28318559.htm : first of the Glassdoor results for Grab ML engineer; search summary reports Kuala Lumpur August 2025 four rounds with live coding; exact URL for that review not identified; snippet-only. Seen 2026-10-31.
- S7. https://interviewquery.com/interview-guides/grab-data-scientist : third-party DS guide; 10-12 question topics, ML frequent, SQL/A-B/project walkthrough from Glassdoor; snippet-only. Seen 2026-10-31.
- S8. https://interviewquery.com/interview-guides/grab-machine-learning-engineer : third-party MLE guide; ML system design and general ML high-frequency; snippet-only. Seen 2026-10-31.
- S9. https://www.designgurus.io/answers/detail/what-is-the-grab-interview-process-like-round-by-round : third-party guide; stage list (software engineer) and values Heart, Hunger, Honour, Humility; snippet-only. Seen 2026-10-31.
- S10. https://jobs.spacetalent.org/companies/grab-com/jobs/31801613-senior-data-scientist-recommendation-singapore : aggregator posting, Senior Data Scientist recommendation, Singapore; also builtinsingapore.com Lead Data Scientist posting (7 years, 3 years senior), jobs.spacetalent.org/companies/grab-com/jobs/40006807-senior-machine-learning-engineer-fulfilment, and a Principal ML Engineer marketplace simulation listing; may be stale; snippet-only. Seen 2026-10-31.
- S11. https://leetcode.com/discuss/interview-experience/1169330/grab-sde1-bangalore-mar-2021-offer : title only, software engineer Bengaluru March 2021 (office evidence, not data science); also Naukri Code360 Grab Data Scientist entry (2 rounds, 3 coding problems, campus February 2023, location not stated) at https://www.naukri.com/code360/interview-experiences/grab/grab-interview-experience-on-campus-feb-2023-2 ; snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low. Verify on grab.careers and with your recruiter: the stages for your team, whether there is a take-home or online test, which office runs the loop, and any rules on AI tools [S2]. Treat all round counts as anecdotal [U].

### C10 Shopee (e-commerce)

**Entity and office note:** Shopee is the e-commerce business of Sea Limited; Sea's other businesses are outside this profile. Shopee Singapore Private Limited appears as an employer name on a university career-fair page, and a trade-press item describes a Shopee regional headquarters in Singapore [S9][S10]. Candidate reports in snippets are mostly Singapore, with some Jakarta and Kuala Lumpur; the office is named where the source gives it and otherwise marked "office not stated" [S1][S6][S12]. No Bangalore or India-office interview report appeared [U].

**Evidence level:** Thin. No official Shopee or Sea hiring-process page appeared; the only company-side material is job postings seen via aggregators. Interview content is anonymous Glassdoor reviews (2017 to 2026, mixed roles and offices) and third-party guides [S1][S3][S4][S6]. Reports for 2025-2026 algorithm and LLM roles exist but are few [S6][S11].

**Roles seen in sources:** Data Scientist (reviews, Singapore and Jakarta) [S1][S2]; Machine Learning Engineer (Singapore, mostly 2018-2022 reports) [S3]; Algorithm Engineer (Singapore, 2025-2026 reports) [S6]; AI LLM Engineer (Singapore, January 2026 review) [S11]; Data Analyst and Data Analytics intern (case study and take-home reports) [S7][S12]; postings for LLM Algorithm Engineer (Post Training), AI Agent Application Algorithm Engineer and Agentic Commerce LLM roles [S8][S13]. Shopee titles ML work "Algorithm Engineer" in these sources [S6][S8].

**Process overview (as reported):**
1. Online assessment, where used: Python and SQL (Jakarta, 2025, anecdotal) [S12]; two LeetCode-style problems on a proctored platform for data science in other reports (anecdotal) [S12]; for an MLE-track candidate, three algorithm questions on DFS, BFS, heap, sorting and two pointers (anecdotal) [S7].
2. Data Scientist loop, as reported in a small sample: about three rounds, two interviews with team members and a mini project (anecdotal) [S1]; another review lists online assessment, technical coding, then manager interview (Data Scientist Intern, anecdotal) [S2]. Technical round with a senior data scientist covering live data-manipulation coding [S2].
3. Machine Learning Engineer, older reports: a coding challenge then two interviews, with efficient matrix operations and ML questions (Singapore, anecdotal) [S3]; a 2018 loop of coding, then ML plus algorithms, then coding (anecdotal) [S3].
4. Algorithm Engineer, 2025-2026 reports: a one-hour technical round split about 30 minutes basic ML/DL and 30 minutes medium algorithm question (Singapore, anecdotal) [S6]; a March 2026 fresh-graduate report of three rounds, two technical (LeetCode, resume deep dive, system design) and one behavioural (anecdotal) [S6]; a 2022 report of online coding, three technical rounds and a project round with the department head (anecdotal) [S6].
5. Duration varies: Glassdoor aggregate averages of 17 days for Data Scientist from 26 submissions, individual reports from 1 week to about 2 months [S2][S6]. Not official.
6. One MLE reviewer suspected a shared question pool with other engineers, since the first interviewer asked backend questions (anecdotal) [S6].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Online assessment | Python and SQL, or algorithm problems, platform-based | SQL, pandas, DSA | [S12][S7] anecdotal |
| Technical 1 | Live, about 1 hour (Algorithm Engineer) | Basic ML/DL plus a medium coding problem | [S6] anecdotal |
| Technical 2 / senior DS | Live coding | Data manipulation, SQL, ML, big data, projects | [S2][S1] anecdotal |
| Resume / project deep dive | Discussion | Past ML project, how you would redo it today | [S6][S3] anecdotal |
| System design (some loops) | Discussion | Example: how to search efficiently | [S3][S6] anecdotal |
| Mini project or case study | Take-home or presented to team lead | Problem-solving, domain knowledge (mostly analyst reports) | [S1][S12] anecdotal |
| Manager / behavioural | Conversation | Fit, motivation | [S2][S6] anecdotal |

**Question types:**
- Python and SQL data manipulation [S2][S12].
- LeetCode medium data-structure questions; graphs, heaps and two pointers in an online assessment [S6][S7].
- ML basics: AUC from sorted scores, k-means, overfitting, linear versus nonlinear classifiers, efficient matrix multiplication [S3].
- 2025-2026 generative topics: normalisation layers in a transformer, BERT, generative recommendation [S6].
- Project discussion and how you would implement it now [S6].
- Case prompts for analyst roles: diagnosing a drop in users, handling bad data [S12].

**Sample questions (illustrative):**
- Compute AUC from predicted scores sorted by score, then explain what it does not tell you. [S3] Book 1 Part 3 (Classification metrics, imbalance, calibration, thresholding).
- Explain k-means, its failure modes, and how you would choose k. [S3] Book 1 Part 5 (Clustering, PCA/UMAP, anomaly detection).
- Explain where layer normalisation sits in a transformer block and why. [S6] Book 2 Part 1 (Transformer internals) and Book 1 Part 8 (Deep learning).
- Explain what generative recommendation means and how it differs from two-tower retrieval plus ranking. [S6] Book 1 Part 7 (Recommenders, ranking, search, learning-to-rank).
- Given order and user tables, write SQL and pandas to find users whose weekly orders dropped by half. [illustrative] Book 3 Part 5 (Window functions: running totals, LAG/LEAD) and Book 1 Part 12 (NumPy/pandas/sklearn live-coding).
- Number of islands or shortest path on a grid, then complexity. [S7] Book 5 Part 9 (Graphs).
- Merge sorted lists or find the top-k items with a heap. [S7] Book 5 Part 8 (Heaps, intervals, greedy).
- Build a small RAG assistant for seller-support questions: chunking, retrieval, reranking, evaluation. [illustrative] (based on posting language [S8]) Book 2 Part 6 (RAG basics) and Book 2 Part 7 (Advanced RAG).

**What they score:**
- Coding fluency on medium problems under time pressure (reports from several years) [S6][S7].
- ML fundamentals and ability to explain past projects in depth [S3][S6].
- For data science: SQL and Python data manipulation [S2][S12].
- For LLM roles, posting language points to RLHF, LLM-as-a-judge evaluation, RAG, reranking and prompt engineering as skills sought; interview weighting is not confirmed [S8].
- No official rubric was found [U].

**Level notes:**
- Titles seen: Data Scientist, Algorithm Engineer, Senior Algorithm/ML Engineer (Paid Ads), AI Engineer and LLM Algorithm Engineer, plus internship and fresh-graduate tracks [S6][S8][S13].
- One senior posting snippet asked for a bachelor's degree or higher and 2 to 4 years of experience (aggregator, may be stale); a 2019 article said Shopee generally prefers postgraduate degrees for data scientists [S8][S14].
- Interview differences by level were not found [U].

**Preparation plan (2 weeks):**
- Days 1-3: SQL and pandas fluency. Book 3 Parts 2, 3, 4 and 5; Book 1 Part 12 [S2].
- Days 4-6: LeetCode-medium practice in a plain editor. Book 5 Parts 1, 2, 8 and 9 [S6][S7].
- Days 7-8: ML fundamentals the reports list: metrics, clustering, regularization. Book 1 Parts 2, 3 and 5 [S3].
- Days 9-10: Recommenders and ranking, then deep learning basics. Book 1 Parts 7 and 8.
- Days 11-12: Transformers, RAG and agents if the role is LLM or agent focused. Book 2 Parts 1, 6, 7 and 8 [S8].
- Day 13: Rehearse a project walkthrough, including how you would redo it today. Book 6 Part 10 [S6].
- Day 14: Timed mock with one coding problem plus ML basics. Book 6 Part 9 (Domain sets: e-commerce) [G].

**Common mistakes:**
- Preparing only ML theory when reports show LeetCode-style coding in most loops [S6][S7].
- Not being able to explain a past project in depth, or how you would redo it now [S6].
- Ignoring SQL and pandas speed for data science tests [S2][S12].
- Assuming the question pool is role-specific; one report suggests shared engineering questions (anecdotal) [S6].

**Recent changes and AI-era notes:**
- 2025-2026 anecdotes add generative AI questions (transformer details, generative recommendation, a generative AI discussion before a technical test) to an otherwise coding-plus-ML format [S6][S11].
- Postings for LLM post-training, agent applications and agentic commerce roles exist in Singapore [S8][S13].
- No Shopee policy on candidates using AI tools in interviews was found. Ask your recruiter [U].
- Older reports (2017-2022) predate these changes [S3].

**Sources:**
- S1. https://www.glassdoor.sg/Interview/Shopee-Interview-E1263091-RVW17730914.htm : anecdotal Glassdoor review, Data Scientist about three rounds, two team interviews and a mini project; search summary also covered other reviews; snippet-only. Seen 2026-10-31.
- S2. https://static.glassdoor.com.br/Interview/Shopee-Data-Science-Interview-Questions-EI_IE1263091.0,6_KO7,19_IP7.htm : Glassdoor Shopee data science interview list; intern online assessment, technical, manager rounds, senior DS live data-manipulation, aggregate 17 days from 26 submissions; snippet-only. Seen 2026-10-31.
- S3. https://www.glassdoor.sg/Interview/Shopee-Interview-E1263091-RVW48823053.htm : anecdotal Glassdoor MLE-related review (Singapore), coding challenge plus two interviews, matrix operations; AUC, k-means, linear versus nonlinear questions came from other reviews in the same result set; attribution uncertain; snippet-only. Seen 2026-10-31.
- S4. https://www.interviewquery.com/interview-guides/shopee-machine-learning-engineer : third-party MLE guide; 3-4 question topics (another guide says 10-12); snippet-only. Seen 2026-10-31.
- S5. https://www.interviewquery.com/interview-guides/shopee-data-scientist : third-party DS guide; multi-stage with HR screen; snippet-only. Seen 2026-10-31.
- S6. https://www.glassdoor.sg/Interview/Shopee-Interview-E1263091-RVW103333801.htm : Glassdoor Algorithm Engineer results (Singapore, 2025-2026): one-hour round 30 minutes ML/DL plus 30 minutes algorithm, March 2026 three-round fresh-graduate report, 2022 four-step loop, transformer and generative recommendation questions, shared-pool comment; mapping across RVW87603952 and others uncertain; snippet-only. Seen 2026-10-31.
- S7. https://static.glassdoor.com.br/Interview/Shopee-Interview-E1263091-RVW42934542.htm : Glassdoor results for MLE and data science; online assessment with three algorithm questions (DFS, BFS, heap, sorting, two pointers), medium data-structure coding; mapping uncertain; snippet-only. Seen 2026-10-31.
- S8. https://nodeflair.com/jobs/shopee-ai-llm-algorithm-engineer-post-training-515431 : posting, LLM Algorithm Engineer (Post Training), RLHF, LLM-as-a-judge; also https://nodeflair.com/jobs/shopee-ai-ai-agent-application-algorithm-engineer-515429 (RAG, reranker, prompt engineering) and the foundit.in Senior ML Engineer Paid Ads Singapore posting (bachelor's or higher, 2-4 years); aggregators may be stale; snippet-only. Seen 2026-10-31.
- S9. https://careerfair.comp.nus.edu.sg/Company0221/Shopee_Singapore_Private_Limited.html : university career-fair page naming Shopee Singapore Private Limited as employer; snippet-only. Seen 2026-10-31.
- S10. https://www.humanresourcesonline.net/shopee-launches-new-regional-hq-in-singapore-with-new-job-positions-and-specialities : trade-press title on a Shopee regional headquarters in Singapore; snippet-only. Seen 2026-10-31.
- S11. https://fr.glassdoor.ch/Entretien/Shopee-Entretien-E1263091-RVW102410378.htm : Glassdoor review, AI LLM Engineer Singapore January 2026 (employee referral, positive, no offer), plus May 2026 Algorithm Engineer review mentioning generative AI discussion before a technical test; snippet-only. Seen 2026-10-31.
- S12. https://fr.glassdoor.ca/Entretien/Shopee-Entretien-E1263091-RVW45562084.htm : first Glassdoor result for the take-home/case study query; search summary: Python and SQL online assessment (Jakarta 2025), 7 SQL plus 7 Python questions (Singapore 2022), analyst case study March 2026, 2024 Kuala Lumpur dashboard take-home; also https://www.interviewquery.com/guides/shopee-data-analyst (assessment portal, analyst); attribution uncertain; snippet-only. Seen 2026-10-31.
- S13. https://sg.jobstreet.com/job/94981245 : posting title, AI Engineer LLM Algorithm Engineer (Agentic Commerce), Singapore; details not retrieved; snippet-only. Seen 2026-10-31.
- S14. https://www.efinancialcareers.com/news/2019/09/shopee-data-jobs-singapore : 2019 article, Shopee data scientist degree preference per its careers site; old; snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low. Verify on Shopee's careers site and with your recruiter: which Sea or Shopee entity and office hires for your role, the stage list, whether an online assessment or mini project applies, and AI-tool rules [U]. Treat all round counts and durations as anecdotal.
