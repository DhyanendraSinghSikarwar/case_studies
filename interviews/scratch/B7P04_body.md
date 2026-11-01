### C1 Spotify (Music streaming)

*Entity note: Spotify is headquartered in Stockholm; sources below refer to Stockholm, New York, Toronto, London, Boston, Gothenburg and Mumbai postings or reviews, and each is named where it matters. Most candidate reports do not say which office they refer to.*

**Evidence level:** Thin. One official page exists (principles and an AI-use notice, no stage list), and everything about rounds comes from small, anonymous Glassdoor samples and prep-guide sites that disagree on round count (3-4, 4-5 and 7 rounds all appear) [S1][S2][S3][S4]. Almost nothing is Stockholm- or ML-specific.

**Roles seen in sources:** Data Scientist (several offices) [S2][S3][S5], Senior Data Scientist (causal inference focus) [S6], Machine Learning Engineer, including a Personalization posting listing London and Stockholm [S7][S8], Research Scientist (research presentation reported by one guide) [S9], and a Mumbai Data Scientist posting that has since been removed [S10]. No applied scientist or GenAI-specific process was found.

**Process overview (as reported):**
1. Recruiter or HR screen, described as friendly and clear by one Stockholm candidate (anecdotal) [S2][S11].
2. Technical screen: Python, SQL, statistics and data manipulation for data science per one guide [S2]; online coding is mentioned in a Glassdoor summary [S3]. Spotify names CoderPad and Mural as interview tools in one aggregator's description (secondary) [S12].
3. Case study or take-home plus presentation: reported by several candidates for data science (a dataset and a slide deck, estimated 3 to 16 hours by one candidate; a panel of four; or a one-hour case in another report). These are different offices and years, so they are not one process [S13][S6].
4. Final conversation with a hiring manager or data science manager, mostly project walk-through and product-metrics scenarios [S3].
5. Round count and length: Interview Query estimates 3-4 rounds over 4-6 weeks from very few reports; Glassdoor reviewers report 4-5 rounds; one other guide lists 7 including system design; Glassdoor timings range from about 1 week to several months [S2][S3][S4]. Treat all as rough.
6. One 2022 senior candidate said team interviews repeat everything after the technical screen for each team (single anecdote) [S3][S14].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / HR screen | Call | Fit, motivation, role match | [S2][S11] anecdotal |
| Technical screen (DS) | Live or online coding | Python, SQL, pandas, statistics | [S2][S3] |
| Technical screen (MLE) | Coding plus ML concepts | BFS-style algorithms, ML use cases | [S8] anecdotal |
| Case study / take-home | Analysis plus slides, panel | Insight, communication, causal reasoning | [S13][S6] anecdotal |
| Hiring manager / DS manager | Conversation | Project depth, product-metric scenarios | [S3] anecdotal |
| Values / behavioural | Conversation | Fit with values, collaboration | [S1][S4] |
| Research talk (research roles) | Presentation | Own research | [S9] guide only |

**Question types:**
- Python and SQL data manipulation, for example applying a markdown rate to song streams (candidate-reported) [S5][S3].
- A/B testing, dashboards, sampling and distribution questions [S2][S8].
- Product metrics, for example "what makes a successful playlist" (anecdotal) [S5].
- Causal inference and experimentation case study; conflict-resolution behavioural questions [S6].
- ML use cases and "favourite algorithm" style questions at other offices (Boston, Gothenburg; anecdotal) [S8].
- ML system design problems listed by an aggregator: podcast recap generation, premium-user propensity (crowdsourced, unverified) [S8].

**Sample questions (illustrative):**
- Write a pandas function that applies a markdown rate to streams for selected songs, then total by artist. [S5] Book 1 Part 12 (NumPy/pandas/sklearn live-coding) and Book 3 Part 1 (aggregation, GROUP BY).
- What makes a successful playlist? Define metrics and say how you would test a change. [S5] Book 6 Part 1 (product metrics) and Book 1 Part 10 (A/B testing).
- Walk through a causal inference case: a feature rolled out to a self-selected group, how do you estimate its effect? [S6] Book 1 Part 10 (causal inference) and Book 6 Part 4 (experiment design).
- Design a premium-propensity model: labels, features, metric, leakage risks. [S8] Book 1 Part 3 (classification metrics, imbalance) and Book 1 Part 11 (ML system design).
- Design candidate generation and ranking for personalised podcast recommendations, including cold start. [illustrative] Book 1 Part 7 (recommenders, ranking).
- Run BFS on a graph and discuss complexity. [S8] Book 5 Part 9 (graphs).
- Tell me about a conflict with a stakeholder over an analysis. [S6] Book 6 Part 6 (stakeholder conflicts).

**What they score:**
- Official statement: fit matters as much as skill, and the process aims at inclusivity at each stage [S1].
- Technical depth in SQL, Python and statistics for data science [S2].
- Product sense and communication through a presentation or case [S13][S3].
- Causal and experimentation reasoning, backed by senior postings that stress it [S6][S15].
- Weights per round were not found in sources [U].

**Level notes:**
- Levels seen as titles only: Data Scientist, Senior Data Scientist, Data Scientist II in postings [S6][S15]; the ML Personalization posting asks for 5+ years [S7]. Level-specific round differences were not found.
- Research Scientist: a research presentation is expected per one guide [S9].

**Preparation plan (2 weeks):**
- Days 1-2: SQL aggregation and windows for streaming data. Book 3 Parts 1, 4, 5.
- Days 3-4: Python and pandas live coding. Book 1 Part 12; Book 5 Part 1.
- Days 5-6: A/B testing and causal inference. Book 1 Parts 10, 13, 14; Book 6 Part 4.
- Days 7-8: Product metrics and metric drops. Book 3 Part 8; Book 6 Part 1.
- Days 9-10: Recommenders, ranking, ML design for ML roles. Book 1 Parts 7 and 11.
- Days 11-12: Build a 10-slide case presentation on a public dataset and present it aloud [G]. Book 6 Part 10.
- Days 13-14: Behavioural stories and two mocks. Book 6 Part 6; Book 9 when available [G].

**Common mistakes:**
- Spending all prep on algorithms when sources emphasise SQL, statistics and cases [S2][S6].
- Skipping causal inference, a topic senior postings stress [S6][S15].
- A take-home without a clear recommendation or limits of the analysis [G].
- Assuming one candidate's loop is the standard [S4].

**Recent changes and AI-era notes:**
- Official: Spotify's AI notice says AI and automated tools help recruiters organise and evaluate information, and humans make selection, advancement and hiring decisions [S16]. This covers Spotify's tooling, not candidate AI use.
- No official rule on candidate AI use in interviews was found; one guide says ask the recruiter [S12]. Ask in writing for each round [G].
- Most candidate reports are 2016-2023; a few 2025-2026 reviews carry no detail [S11][S12]. No evidence of a recent loop redesign.

**Sources:**
- S1: https://lifeatspotify.com/how-we-hire . Supports: official principles (fit as much as skill, inclusivity at each stage), official-domain warning; no stage list. Seen 2026-10-31. Snippet only.
- S2: https://www.interviewquery.com/guides/spotify-data-scientist . Supports: 3-4 rounds over 4-6 weeks estimate, technical round topics (Python, SQL, statistics), take-home/presentation note; synthesised from few reports. Seen 2026-10-31. Snippet only.
- S3: https://www.glassdoor.co.uk/Interview/Spotify-Interview-E408251-RVW102663640.htm . Supports: Glassdoor DS reports (4-5 rounds, hiring manager and case, product-metrics scenarios, per-team repeat anecdote, 34-day average from 7 interviews as summarised in results). Seen 2026-10-31. Snippet only.
- S4: https://www.tryexponent.com/blog/spotify-interview-process . Supports: guide with 3-4 stages and values emphasis; timing varies by source. Seen 2026-10-31. Snippet only.
- S5: https://www.glassdoor.com.hk/Interview/Spotify-Interview-E408251-RVW66272474.htm . Supports: reported questions (markdown rate function, playlist success, product metrics); Toronto candidate hiring manager plus case study (anecdotal). Seen 2026-10-31. Snippet only.
- S6: https://www.glassdoor.ca/Interview/Spotify-Interview-E408251-RVW68433570.htm . Supports: August 2022 Senior Data Scientist review (causal inference case study, experimentation, conflict resolution; take-home plus panel of four, as summarised). Seen 2026-10-31. Snippet only.
- S7: https://peerlist.io/company/lifeatspotif/careers/machine-learning-engineer-personalization/jobh7b8o98gpk7n66h6r9pggkajqbb . Supports: ML Engineer, Personalization posting, hybrid London / Stockholm, 5+ years. Seen 2026-10-31. Snippet only.
- S8: https://prachub.com/companies/spotify/positions/machine-learning-engineer . Supports: crowdsourced MLE question categories (ML, coding, ML system design; podcast recap, premium propensity); BFS mention and Boston/Gothenburg sampling questions come from the search summary of Glassdoor entries. Seen 2026-10-31. Snippet only.
- S9: https://www.interviewquery.com/interview-guides/spotify-research-scientist . Supports: guide statement that research scientist candidates usually prepare a research presentation. Seen 2026-10-31. Snippet only.
- S10: https://www.glassdoor.co.in/Interview/Spotify-Interview-E408251-RVW68300981.htm . Supports: Mumbai-related Glassdoor listing (search summary: positive, no offer, no stage detail); Mumbai DS posting removed April 2025 per the same summary. Seen 2026-10-31. Snippet only.
- S11: https://www.glassdoor.nz/Interview/Spotify-Interview-E408251-RVW63419652.htm . Supports: Stockholm candidate reports (recruiter call pleasant; Feb 2025 ML engineer easy, no offer; 2026 DS review without detail), as summarised. Seen 2026-10-31. Snippet only.
- S12: https://www.techinterview.org/companies/spotify/ . Supports: guide stating no published candidate AI rule, interviews on Meet/Zoom with shared coding environment and Mural. Seen 2026-10-31. Snippet only.
- S13: https://www.1point3acres.com/interview/thread/1147417 . Supports: Spotify data scientist onsite interview experience listing (anecdotal). Take-home hours estimate comes from the search summary. Seen 2026-10-31. Snippet only.
- S14: https://www.glassdoor.ca/Interview/Spotify-Interview-E408251-RVW68233661.htm . Supports: senior DS anecdote that each team repeats post-screen interviews. Seen 2026-10-31. Snippet only.
- S15: https://pcdn-global.jobboardly.com/jobs/senior-data-scientist-music-mission-27b6d279 . Supports: Senior Data Scientist posting (experimentation, causal inference). Seen 2026-10-31. Snippet only.
- S16: https://lifeatspotify.com/ai-notice . Supports: official AI notice; AI assists recruiters, humans decide. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Confidence in the broad shape (recruiter, technical, case or presentation, manager) is low to medium; in round count and timings, low.
- Verify with the recruiter: which office the role sits in (Stockholm, London, other), the stages for your role, whether there is a take-home and its time limit, tools used, and AI-tool rules for candidates.
- India-based candidates: only general process evidence exists (one Mumbai review without detail, a removed Mumbai posting); eligibility and relocation questions belong to Book 8 and official sources [S10].
- Check lifeatspotify.com for current postings; apply only through its official domains [S1].

### C2 Zalando (Fashion e-commerce platform)

*Entity note: Zalando SE is headquartered in Berlin. Sources are mostly Berlin reviews; one report mentions Zurich; no Dublin, Helsinki or India-office process was found. Where a source does not name the office, it is not assumed to be Berlin.*

**Evidence level:** Thin to Medium on applied scientist (an official Zalando blog describes the technical interview, though only fragments appeared in snippets), Thin on data scientist, machine learning engineer and GenAI roles. Candidate reports are small, anonymous, mixed and often 2020-2023 [S1][S2][S3][S4].

**Roles seen in sources:** Applied Scientist, including Senior and Principal levels, Berlin [S1][S5][S6]; Data Scientist [S2][S7]; Machine Learning Engineer (guide only) [S8]; Applied Scientist / Senior Applied Scientist in LLMs and agentic AI, and Principal AI Scientist for Zalando Assistant (postings only, no interview detail) [S9][S10]; Senior Data Analyst (adjacent) [S11].

**Process overview (as reported):**
1. Official: after the hiring team reviews an application positively, the applied scientist process has several steps depending on seniority, meant to help candidates learn about the role, culture and future manager [S1].
2. Official, general: first a 15-45 minute video or phone call with a Talent Acquisition Partner about motivation and "Why Zalando?" [S12]; for tech roles a deeper technical conversation with an engineer or hiring manager follows [S12].
3. Official, applied scientist: a one-hour coding interview on understanding requirements, implementing a solution and data wrangling, usually in a live coding environment [S1][S13].
4. Technical rounds as candidates describe them for Berlin applied scientist roles (anecdotal): a screening of about 90 minutes on statistics, applied deep learning, ML theory and an easy TF-IDF coding question, then an onsite of about five rounds that includes ML depth, a research chat, coding, hiring manager and HR [S5][S6].
5. Data scientist (anecdotal): one report describes round one as a coding interview plus a data science interview, then a second stage with data science deep dive, coding, hiring manager, "talent champion" and HR interviews [S2][S7]. Another describes three interviews of up to one hour each after an HR stage [S2].
6. Total duration: reports range from about 2 weeks to 4 months; one guide estimates 3 rounds over 3-5 weeks (secondary) [S3][S4][S7].
7. The official page says stages are flexible and depend on the role [S14].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Talent acquisition call | 15-45 min call | Motivation, background | [S12] official |
| Coding (applied scientist) | 1 hour, live | Requirements, implementation, data wrangling | [S1][S13] official |
| Technical screen | About 90 min | Statistics, deep learning, ML theory, easy coding | [S5] anecdotal |
| Statistics / DL expert round | About 1 hour | Theory depth | [S6] anecdotal |
| Principal / problem round | Interview | Approach on past projects | [S6] anecdotal |
| Hiring manager, stakeholder, peer | Interviews | Experience, collaboration | [S2][S12] anecdotal |
| Data science deep dive (DS) | Interview | Project depth, modelling | [S7] anecdotal |

**Question types:**
- Short coding in Python without libraries: histogram from a list of floats without numpy; sum of a nested list; TF-IDF (anecdotal) [S5][S13].
- A floodfill problem and optimisation questions reported for a senior applied scientist loop (one guide, anecdotal) [S13][S15].
- Statistics, deep learning theory, ML theory, metrics for imbalanced data [S6][S7].
- Decision tree and logistic regression questions for data science (anecdotal) [S2].
- SQL and data manipulation emphasis for data scientist per one guide [S2]; one Glassdoor report mentions a Codility test with SQL, Spark and general coding (engineering-style, may not apply) [S13].
- Project walk-through and behavioural: explain a project in detail, a situation with difficult communication, "Why Zalando?" [S5][S12].

**Sample questions (illustrative):**
- Build a bucket histogram from a list of floats without numpy. [S13] Book 1 Part 12 (NumPy/pandas/sklearn live-coding) and Book 5 Part 1 (arrays and hashing).
- Sum all elements of an arbitrarily nested list. [S13] Book 1 Part 1 (from-scratch code) [illustrative mapping].
- Implement TF-IDF and explain when it fails. [S5] Book 1 Part 9 (NLP and embeddings).
- Which metrics would you use for a heavily imbalanced return-risk classifier, and how do you set the threshold? [S7] Book 1 Part 3 (classification metrics, imbalance, thresholding).
- Explain regularisation in logistic regression and how you would tune it. [S2] Book 1 Part 2 (regression, regularization).
- Flood fill a grid and state the complexity. [S13] Book 5 Part 9 (graphs) and Book 5 Part 13 (2D grids).
- Design an LLM-based shopping assistant with retrieval and evaluation. [illustrative] Book 2 Part 12 (GenAI system design) and Book 2 Part 9 (LLM evaluation).
- Explain a past project end to end and where it went wrong. [S5] Book 6 Part 10 (end-to-end scenarios).

**What they score:**
- Official: coding skills for requirements, implementation and data wrangling [S1].
- ML, statistics and deep learning theory depth for applied scientists (anecdotal) [S5][S6].
- Past-project depth and approach [S6][S7].
- Cultural fit and collaboration, called significant in one guide (secondary) [S2][S3].

**Level notes:**
- Titles seen: Applied Scientist, Senior Applied Scientist, Principal Applied Scientist, Principal AI Scientist [S9][S10][S5]. Official blog says steps depend on seniority [S1]. Specific expectations by level were not found.

**Preparation plan (2 weeks):**
- Days 1-2: Plain-Python coding without libraries, data wrangling. Book 1 Part 12; Book 5 Parts 1, 3.
- Days 3-4: Statistics and ML theory. Book 1 Parts 1, 2, 13.
- Days 5-6: Metrics, imbalance, trees and boosting. Book 1 Parts 3, 4.
- Days 7-8: Deep learning and NLP. Book 1 Parts 8, 9.
- Days 9-10: SQL and pandas refresh for data science roles. Book 3 Parts 1-5.
- Days 11-12: For LLM or agentic roles: RAG, agents, evaluation. Book 2 Parts 6, 8, 9, 12.
- Days 13-14: Project walk-through practice, behavioural stories, mocks. Book 6 Parts 6, 10 [G].

**Common mistakes:**
- Treating the coding round as LeetCode only when the official description stresses requirements and data wrangling [S1].
- Weak recall of ML theory basics, a recurring candidate complaint pattern (anecdotal) [S5].
- Not preparing a clear project story, since several rounds revolve around past work [S6][S2].
- Assuming engineering-style loops (Codility, system design) apply to science roles without checking [S13].

**Recent changes and AI-era notes:**
- No Zalando policy on candidate AI use in interviews was found; a general tracker did not list Zalando [U]. Ask the recruiter in writing [G].
- An April 2026 Glassdoor applied scientist review (negative, anecdotal) mentions repeated identical questions across five rounds [S16].
- Postings for LLM and agentic AI roles show the topics the team works on (agents, RAG, prompt engineering), not interview content [S9][S10].
- Zalando's recruiting team has publicly acknowledged rescheduling problems in one Glassdoor response (anecdotal context) [S12].

**Sources:**
- S1: https://jobs.zalando.com/en/blog/technical-interview-for-applied-science . Supports: official applied scientist process (several steps by seniority; one-hour live coding on requirements, implementation, data wrangling). Only fragments seen. Seen 2026-10-31. Snippet only.
- S2: https://dataford.io/interview-guides/zalando/data-scientist . Supports: guide with 3 rounds over 3-5 weeks, SQL and data manipulation emphasis, take-home mention, cultural fit weight (secondary). Seen 2026-10-31. Snippet only.
- S3: https://interviewquery.com/interview-guides/zalando-data-scientist . Supports: guide for Zalando data scientist; Zalando Outlet variant mentions past-project walk-throughs. Seen 2026-10-31. Snippet only.
- S4: https://www.designgurus.io/answers/detail/what-is-the-zalando-interview-process-like-round-by-round . Supports: third-party round-by-round summary; engineering stages and 2 weeks to 4 months timeline (secondary). Seen 2026-10-31. Snippet only.
- S5: https://www.glassdoor.com/Interview/Zalando-Interview-RVW53268012.htm . Supports: Berlin applied scientist report (90-minute screen with statistics, deep learning, ML theory, TF-IDF coding; onsite rounds; anecdotal). Seen 2026-10-31. Snippet only.
- S6: https://www.glassdoor.com/Interview/Zalando-Interview-RVW84395986.htm . Supports: report of coding, expert statistics/deep learning round and principal interview; feedback on ML knowledge; histogram coding question (anecdotal). Seen 2026-10-31. Snippet only.
- S7: https://static-pc.glassdoor.de/Interview/Zalando-Data-Science-Interview-Questions-EI_IE613421.0,7_KO8,20_IP3.htm . Supports: DS reports (coding plus DS interview, then deep dive, coding, hiring manager, talent champion, HR; imbalance metrics; anecdotal). Seen 2026-10-31. Snippet only.
- S8: https://www.interviewquery.com/interview-guides/zalando-machine-learning-engineer . Supports: existence of a Zalando MLE guide only; no details seen. Seen 2026-10-31. Snippet only.
- S9: https://www.arbeitsagentur.de/jobsuche/jobdetail/18251-31922-S . Supports: Applied Scientist LLMs / Agentic AI posting (Zalando SE, German job portal). Seen 2026-10-31. Snippet only.
- S10: https://jobs.zalando.com/de/jobs/2723791 . Supports: Principal AI Scientist, Zalando Assistant posting (agents, RAG, prompt engineering, agent frameworks), Berlin. Seen 2026-10-31. Snippet only.
- S11: https://www.teamblind.com/post/help-in-preparation-for-senior-data-analyst-role-at-zalando-npmebzbw . Supports: Blind thread on a senior data analyst role; commenters call coding easy-medium (anecdotal, adjacent role); pay comments ignored. Seen 2026-10-31. Snippet only.
- S12: https://womentech.net/en-gb/node/52132 . Supports: recruiter talk on the process (TA call 15-45 min, technical deep dive for tech roles, honesty message); rescheduling response comes from the search summary of Glassdoor. Seen 2026-10-31. Snippet only.
- S13: https://www.glassdoor.com/Interview/Zalando-Interview-RVW62945188.htm . Supports: candidate coding questions (nested list sum, histogram), Codility/SQL/Spark report, floodfill senior applied scientist detail as summarised (anecdotal). Seen 2026-10-31. Snippet only.
- S14: https://jobs.zalando.com/en/how-we-hire . Supports: official how we hire page; stages flexible by role, general tips. Seen 2026-10-31. Snippet only.
- S15: https://www.interviewquery.com/guides/zalando-outlet-data-scientist . Supports: Zalando Outlet DS and senior applied scientist reports (project walk-through, optimisation questions); secondary. Seen 2026-10-31. Snippet only.
- S16: https://www.glassdoor.com/Interview/Zalando-Interview-RVW82275698.htm . Supports: Glassdoor applied scientist listing, 2026 negative report as summarised (anecdotal). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Confidence: medium that applied scientist interviews include a one-hour live coding round (official); low for everything else, including round counts, durations and which questions recur.
- Verify with the recruiter: the exact stages for your role and level, the office (Berlin or elsewhere), whether a take-home or case exists, coding tools, and AI-tool rules.
- India-based candidates: no India-office process or India-candidate report was found; only a third-party guide mentions location setups. Eligibility and relocation belong to Book 8 and official sources [U].
- Check jobs.zalando.com for the current how-we-hire page and the posting itself [S14].

### C3 Booking.com (online travel platform; Amsterdam HQ plus other offices)

**Entity note:** Booking.com is headquartered in Amsterdam; its data science and ML postings seen are in Amsterdam, Tel Aviv and Manchester [S9][S10]. Most candidate reports below are for Amsterdam [S2][S3]; Glassdoor pages also mix in other cities and roles. Each claim names the office where the source does. No India-office reports were found.

**Evidence level:** Thin. There is an official "how we hire" page (generic timeline) and an official AI-use guide for candidates, but process detail for data science and ML roles comes from small, mixed-year anecdotal Glassdoor reports (2014 to 2026) and prep-site guides that often disagree [S1][S2][S3][S6][S7].

**Roles seen in sources:** Data Scientist (Amsterdam reports) [S1][S2]; Machine Learning Engineer (Amsterdam) [S3][S4][S8]; Machine Learning Scientist (a single report, anecdotal) [S4]; GenAI Applications roles (Machine Learning Engineer II and Senior Machine Learning Scientist, Tel Aviv postings; Senior Machine Learning Scientist on a Travel LLMs and Agentic team, Amsterdam posting), postings only with no interview detail [S9][S10].

**Process overview (as reported):**
1. Official: the recruitment process can take about 3 to 6 weeks depending on the interviews a role needs, and a pre-employment screening process exists [S6].
2. Data scientist, third-party guide: HR phone call, then an online technical test; sometimes a presentation round on a case study [S1]. One Amsterdam candidate (anecdotal): HR phone interview, a statistics and machine learning test, then a technical phone interview [S2].
3. Data scientist, anecdotal Amsterdam account: two one-hour face-to-face interviews, each with two data scientists and two business cases; a final interview with a senior data scientist and one more case [S2]. A 2025 candidate reported three rounds: technical, a role-linked business case, and company alignment (anecdotal) [S1].
4. Take-home (anecdotal, mostly older): a business case with a window of about three days, then presenting findings to the team, then a cultural fit round; follow-ups on experimentation [S2][S13]. One third-party guide calls the take-home optional [S13].
5. Machine learning engineer (anecdotal Amsterdam): an online assessment (a HackerRank coding question plus multiple-choice ML questions in a March 2024 report), an HR screen, coding rounds, and for one 2025 report a hotel-pricing design question [S3][S14]. A Glassdoor aggregate from three interviews lists LeetCode-style graphs and trees in Python, system design, then HR [S4]. A 2021 Amsterdam candidate described four rounds starting with an online ML, statistics and probability test [S4].
6. Time to hire: Glassdoor summaries of a few interviews give about 47 days for data scientists and about 30 days for ML engineers (rough, tiny samples) [S1][S4].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter or HR screen | Phone call | Fit, role match | [S1][S2][S6] |
| Online technical test | Online test | Statistics and ML basics (DS); HackerRank coding plus ML multiple choice (MLE) | [S1][S2][S3] anecdotal |
| Technical phone interview | Call | Technical depth | [S2] anecdotal |
| Business case interviews (DS) | Face to face or video, about 1 hour | Analytical reasoning on product and hotel cases, experimentation follow-ups | [S2] anecdotal |
| Take-home and presentation | Case over a few days, then team presentation | Analysis, communication | [S2][S13] anecdotal, older |
| Coding and design (MLE) | Live | Graphs and trees in Python; ML system design such as hotel pricing | [S4][S14] anecdotal |
| Company alignment or culture fit | Interview | Values and fit | [S1][S2] |

**Question types:**
- Business cases such as estimating a hotel's star rating or measuring product health [S2].
- Experimentation, including how to analyse a change in a cancellation policy and predicting days until a hotel is fully booked (candidate-reported) [S2].
- Statistics, ML and probability basics in an online test [S2][S4].
- Coding: HackerRank question, graphs and trees in Python [S3][S4].
- ML system design with a pricing flavour [S14].
- Project deep dives [S1]. Booking.com's experimentation leader said in 2018 he looks for customer impact focus and people who explain their reasoning and update when challenged (a 2018 podcast, older) [S12].

**Sample questions (illustrative):**
- Estimate a hotel's star rating from available platform data; say which features and what error you accept. [illustrative] Book 6 Part 5 (business case studies) and Book 1 Part 2 (regression, feature engineering).
- Cancellation policy changes for some properties: how do you measure the effect on bookings and on guest behaviour? [S2] Book 1 Part 10 (A/B testing, causal inference) and Book 6 Part 4 (experiment design).
- Predict how many days before a stay a property becomes fully booked. [S2] Book 1 Part 6 (time series and forecasting).
- Design a hotel pricing recommendation model: data, model, metric, serving. [S14] Book 1 Part 11 (ML system design).
- Solve a graph traversal problem in Python and state complexity. [S4] Book 5 Part 9 (graphs).
- Walk through a past project and what you would change; defend a modelling choice. [S1] Book 6 Part 6 (stakeholder conflicts and trade-offs).
- Build an agentic trip-planning assistant: retrieval, tool use, evaluation. [illustrative] Book 2 Part 8 (agents) and Book 2 Part 12 (GenAI system design).

**What they score:**
- Reasoning on business cases and how clearly you explain it [S2][S12].
- Experimentation fundamentals [S2][S12].
- Technical basics: statistics, ML, Python coding [S2][S4].
- Alignment with company values; candidates are advised to read about them (anecdotal) [S1].
- Outcomes can depend on the interviewer (one Machine Learning Scientist review, anecdotal) [S4].

**Level notes:**
- Postings show Machine Learning Engineer II and Senior Machine Learning Scientist I levels [S9][S10]; level-specific interview expectations were not found.
- One guide lists a recruiter screen, a 60-minute technical screen and a four-to-five round virtual onsite for technical roles generally, not data-science specific [S11].

**Preparation plan (2 weeks):**
- Days 1-2: Business cases and metrics. Book 6 Parts 1 and 5.
- Days 3-4: Experimentation and causal inference. Book 1 Parts 10, 13; Book 6 Part 4.
- Days 5-6: Statistics and ML basics under test conditions. Book 1 Parts 1-4 and 14.
- Days 7-8: Python coding, graphs and trees. Book 5 Parts 7 and 9; Book 1 Part 12.
- Days 9-10: Forecasting and ranking or recommenders (travel use cases). Book 1 Parts 6 and 7.
- Days 11-12: ML system design and, for GenAI roles, agents. Book 1 Part 11; Book 2 Parts 8 and 12.
- Days 13-14: Take-home practice with a short team presentation, then values stories and two mocks. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Jumping to a model before defining the business question in a case [S2][S12].
- Not preparing for experimentation follow-ups after a case [S2].
- Skipping research on how Booking.com uses ML (a 2021 candidate's advice, anecdotal) [S4].
- Using AI tools live in interviews or independent assessments, which the official guide advises against [S7].
- Treating one candidate's loop as the process [G].

**Recent changes and AI-era notes:**
- Official, recent: Booking.com publishes "How to use AI fairly and effectively in your Booking.com interviews". Using AI to practise is fine; for some technical roles it may test how you use AI in a controlled setting such as pair coding; real-time AI use in interviews, coding tasks or independent assessments is not recommended, nor is AI recording or transcription of interviews [S7]. Date of the page not shown in the snippet.
- GenAI and agentic teams are hiring (postings in Tel Aviv and Amsterdam); no interview reports for them were found [S9][S10].
- Older: take-home and presentation reports date from 2016 onwards and may no longer apply [S2][S13].

**Sources:**
- S1: https://www.interviewquery.com/interview-guides/bookingcom-data-scientist . Supports: DS stages (HR call, online test, optional presentation), 2025 three-round report, experimentation and deep dives, 47-day figure (third-party guide plus Glassdoor summary). Seen 2026-10-31. Snippet only.
- S2: https://www.glassdoor.ca/Interview/Booking-com-Interview-E256653-RVW23859925.htm . Supports: Glassdoor DS reviews (Amsterdam; two one-hour interviews with business cases; take-home with three days; cancel-policy and days-to-fully-booked prompts; anecdotal). The page-to-detail match comes from a summary of several Glassdoor results returned together. Seen 2026-10-31. Snippet only.
- S3: https://www.1point3acres.com/interview/thread/1065770 . Supports: Amsterdam MLE thread (online assessment, HR screen, coding rounds; anecdotal). Seen 2026-10-31. Snippet only.
- S4: https://static.glassdoor.nl/Interview/Booking-com-Machine-Learning-Engineer-Interview-Questions-EI_IE256653.0,11_KO12,37.htm . Supports: MLE aggregate (graphs and trees, system design, HR; about 30 days; 2021 four-round report; ML Scientist interviewer-dependence note from the search summary). Seen 2026-10-31. Snippet only.
- S5: https://www.teamblind.com/post/bookingcom-data-scientist-interview-gd2s7bvg . Supports: existence of a Blind thread on Booking.com data scientist interviews; no content seen, so nothing relies on it. Seen 2026-10-31. Snippet only.
- S6: https://careers.booking.com/how-we-hire/ . Supports: official page; about 3 to 6 weeks, pre-employment screening, interview preparation tips. Seen 2026-10-31. Snippet only.
- S7: https://careers.booking.com/candidate-ai-usage-recommendations/ . Supports: official AI-use guidance for candidates. Seen 2026-10-31. Snippet only.
- S8: https://www.interviewquery.com/interview-guides/bookingcom-machine-learning-engineer . Supports: third-party MLE guide (coding assessment, system design, culture fit, final hiring-manager or panel conversation). Seen 2026-10-31. Snippet only.
- S9: https://www.themuse.com/jobs/bookingcom/machine-learning-engineer-ii-genai-applications . Supports: GenAI Applications ML Engineer II posting (Tel Aviv per search summary). Seen 2026-10-31. Snippet only.
- S10: https://magnet.me/en/opportunity/1051919/senior-machine-learning-scientist . Supports: Senior Machine Learning Scientist posting (Amsterdam, Travel LLMs and Agentic team per search summary). Seen 2026-10-31. Snippet only.
- S11: https://www.techprep.app/blog/booking-interview-process . Supports: generic technical-role stage list (recruiter screen, 60-minute screen, virtual onsite, hiring manager); not DS-specific. Seen 2026-10-31. Snippet only.
- S12: https://www.datacamp.com/community/podcast/online-experiments-booking . Supports: 2018 podcast with Booking.com's experimentation director on hiring mindset (older). Seen 2026-10-31. Snippet only.
- S13: https://jobrise.io/en/blog/booking-com-data-scientist-resume-interview-2026/ . Supports: third-party prep guide; take-home presented to team as an optional stage, pandas and scikit-learn readiness. Seen 2026-10-31. Snippet only.
- S14: https://www.glassdoor.com.au/Interview/Booking-com-Interview-E256653-RVW65256550.htm . Supports: possibly the Feb 2025 Amsterdam hotel-pricing design report (anecdotal); page match is uncertain, from a result summary. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium confidence in the overall shape (screen, online test or take-home, case interviews, alignment); low confidence in round counts, durations and which part applies to your team [S1][S2][S4].
- India: no India-based reports found; treat as general process evidence only [S2].
- Verify on Booking.com careers: the stages for your role, whether a take-home or pair-coding exercise applies, and the current AI-use guidance [S6][S7].
- No claim here that any question will be asked.

### C4 Klarna (fintech and payments; Stockholm HQ plus other offices)

**Entity note:** Klarna is headquartered in Stockholm. Candidate reports below are mostly Stockholm, with one Berlin report and some Glassdoor pages with no city shown [S1][S8]. Each claim names the office where the source does. No India-office reports were found.

**Evidence level:** Thin. No official Klarna interview-process page appeared. Evidence is anonymous Glassdoor reports (2011 to 2026, many for other roles) and commercial prep guides that disagree on take-home length and round counts [S1][S2][S5][S6].

**Roles seen in sources:** Data Scientist [S2][S3][S5]; Machine Learning Engineer (guides only, no first-hand report found) [S4][S5]; Analytics Manager, Data Analyst and Product Analyst (adjacent roles, used for process shape only) [S1][S10]; Senior Software Engineer (Stockholm, Mar 2026 listing, no content used) [S11].

**Process overview (as reported):**
1. Early online logic or cognitive test. Stockholm anecdotes: an 18-question logic test (2018), two logic tests with strict cut-offs for a 2019 data scientist, and in a 2023 analytics-manager review a logic test, a 15-minute HR call, then the logic test again proctored [S1]. A 2026 guide gives about 15 to 30 minutes for this round [S2].
2. HR or recruiter screen [S1][S6].
3. Technical task for data science: exploratory analysis, an ML model, and deployment on a cloud provider (guide) [S3]. Anecdotes: train a credit risk model and deploy it behind an API on any cloud provider; one candidate said it took over 10 hours [S7]. Guides disagree on size: about 7 days and 10+ hours in one, a 3 to 4 hour take-home in another [S2][S5].
4. Presentation of the case and technical deep dive, plus behavioural questions (guide) [S4][S5].
5. Team and culture interviews. A Berlin report from May 2025 (anecdotal): HR, ML task, technical interview, Klarna fit interview, another technical interview, team fit [S8]. A 2019 Stockholm data scientist reported interviews with HR, a team lead and a data science lead [S1].
6. Length: reports range from two weeks to several months; a guide says up to two months; one analysis of Glassdoor data gives about 36 days [S5][S6]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Logic or cognitive test | Online, timed | Pattern recognition, reasoning; strict cut-offs reported | [S1][S2] anecdotal |
| HR or recruiter screen | Call, about 15 to 30 minutes | Fit, motivation | [S1][S6] |
| ML case or take-home | Remote, hours to days (sources disagree) | EDA, model, cloud deployment, credit risk or similar | [S3][S7] anecdotal |
| Case presentation and technical deep dive | Interview | Explaining choices, deployment, reproducibility | [S4][S5] |
| Team and culture fit | Interviews | Fit with team; Klarna principles (bar-raiser-style round mentioned by some, mainly non-engineering) | [S6][S8] anecdotal |

**Question types:**
- Logic puzzles in an online test [S1].
- Building and deploying a credit risk model; imputing missing values (candidate-reported) [S7][S9].
- Fraud detection design and credit scoring, MLOps and fairness (guide, not confirmed) [S4].
- SQL, statistics and ML modelling categories on a question-bank site [S9].
- Behavioural and team-fit questions [S6][S8].

**Sample questions (illustrative):**
- Train a credit risk model on a messy dataset and serve it behind an API. [S7] Book 1 Part 3 (classification metrics, imbalance, calibration) and Book 4 Part 6 (serving).
- How would you impute missing values, and when is each approach risky? [S9] Book 6 Part 3 (imbalanced, noisy, missing data).
- Design a real-time fraud detection system for card and pay-later payments. [S4] Book 1 Part 11 (ML system design) and Book 6 Part 9 (domain sets, fintech).
- How would you monitor a credit scoring model after launch for drift and fairness? [S4] Book 4 Part 8 (monitoring, drift).
- Choose a decision threshold when false declines and defaults have different costs. [illustrative] Book 1 Part 3 (thresholding).
- Present your take-home to a panel and defend one modelling choice you rejected. [S5] Book 6 Part 6 (stakeholder conflicts and trade-offs).
- Write a SQL query for default rate by customer cohort. [illustrative] Book 3 Part 6 (cohorts).

**What they score:**
- Passing the logic-test cut-off first [S1].
- Hands-on ML delivery: analysis, model, deployment, shown in the take-home [S3][S7].
- Ability to explain and present your work [S4][S5].
- Team fit and values; one Stockholm reviewer said team placement may be unclear until late (anecdotal) [S6].

**Level notes:**
- Level names and expectations were not found in snippets. Guides list a five-round ML engineer process without level detail [S4].

**Preparation plan (2 weeks):**
- Days 1-2: Practise timed logic and reasoning puzzles [G].
- Days 3-4: Classification, credit risk metrics, calibration, thresholds. Book 1 Parts 3 and 4.
- Days 5-6: Messy data, imputation. Book 6 Part 3; Book 1 Part 2.
- Days 7-8: Serving and cloud deployment of a model. Book 4 Parts 6, 10 and 11.
- Days 9-10: Monitoring, drift, fairness. Book 4 Part 8; Book 6 Part 2.
- Days 11-12: Fraud and credit ML system design, SQL cohorts. Book 1 Part 11; Book 6 Part 9; Book 3 Part 6.
- Days 13-14: Build and present a mock take-home in a time box; values and team-fit stories. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Treating the logic test as a formality when cut-offs are reported to be strict [S1].
- Underestimating the take-home: one candidate reported 10+ hours because of data exploration [S7].
- Delivering a model with no deployment or reproducibility story [S3][S4].
- Not asking the recruiter which stages remain, since Klarna reportedly does not publish one fixed process [S15].
- Relying on SEO pages with unverified claims about 2026 loops [G].

**Recent changes and AI-era notes:**
- Reported hiring context, not interview policy: in late 2024 Klarna's CEO said hiring had effectively stopped a year earlier because of AI, then in May 2025 said Klarna was hiring again for customer service [S12][S13]. A July 2026 Swedish headline reports a hiring freeze and AI investment; the article itself was not seen [S14].
- No official Klarna statement on AI use in interviews was found. Claims of "AI fluency" as a hiring signal come from low-quality aggregator pages and are unverified [U].
- Take-home reports mix 2019 to 2026; the Berlin report is May 2025 [S1][S8].

**Sources:**
- S1: https://static.glassdoor.com.au/Interview/Klarna-Analytics-Manager-Interview-Questions-EI_IE389854.0,6_KO7,24.htm . Supports: Stockholm Jul 2023 analytics-manager review (logic test, HR call, proctored retest, skills, team, culture); 2018 and 2019 Stockholm logic-test and data scientist details come from a summary of several Glassdoor results. Anecdotal. Seen 2026-10-31. Snippet only.
- S2: https://interview.norahq.com/interview-guides/klarna-data-scientist-interview-guide-2026 . Supports: third-party 2026 guide; logic test about 15 to 30 minutes, about 7-day ML case study of 10+ hours. Seen 2026-10-31. Snippet only.
- S3: https://www.interviewquery.com/interview-guides/klarna-data-scientist . Supports: third-party DS guide; technical task of EDA, ML model and cloud deployment. Seen 2026-10-31. Snippet only.
- S4: https://www.interviewquery.com/interview-guides/klarna-ml-engineer . Supports: third-party MLE guide; five rounds, fraud and credit scoring prompts, MLOps and fairness, presentation (not confirmed by first-hand MLE reports). Seen 2026-10-31. Snippet only.
- S5: https://www.cleverprep.com/companies/klarna/data-scientist . Supports: third-party guide; 3 to 4 hour take-home on ML, statistics, SQL and Python; up to two months. Seen 2026-10-31. Snippet only.
- S6: https://www.techprep.app/blog/klarna-interview-process . Supports: third-party five-stage outline, about 36 days, team-fit and bar-raiser mentions, recruiter-ask advice. Seen 2026-10-31. Snippet only.
- S7: https://static.glassdoor.com.ar/Interview/Klarna-Interview-E389854-RVW76138712.htm . Supports: anecdotal case study to build an ML model and host via API on a cloud provider; credit risk model over 10 hours; exact page-to-detail match from a result summary. Seen 2026-10-31. Snippet only.
- S8: https://www.glassdoor.co.nz/Interview/Klarna-Interview-E389854-RVW73266522.htm . Supports: possibly the May 2025 Berlin report (HR, ML task, technical, Klarna fit, technical, team fit; anecdotal); page match uncertain, from a result summary. Seen 2026-10-31. Snippet only.
- S9: https://prepfully.com/interview-questions/klarna/data-scientist?page=8 . Supports: question-bank categories (ML modelling, statistics, SQL) and imputation question; user-submitted. Seen 2026-10-31. Snippet only.
- S10: https://www.hackingthecaseinterview.com/pages/klarna-case-interview . Supports: third-party case-interview guide, mainly non-engineering roles; used only as context. Seen 2026-10-31. Snippet only.
- S11: https://static.glassdoor.com.au/Interview/Klarna-Senior-Software-Engineer-Interview-Questions-EI_IE389854.0,6_KO7,31.htm . Supports: existence of a Stockholm Mar 2026 report (software engineer; no content used). Seen 2026-10-31. Snippet only.
- S12: https://www.aol.com/klarna-ceo-says-company-stopped-205638908.html . Supports: CEO said hiring stopped about a year earlier because of AI (late 2024). Seen 2026-10-31. Snippet only.
- S13: https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/ . Supports: May 2025 reversal, hiring customer service agents again. Seen 2026-10-31. Snippet only.
- S14: https://www.realtid.se/bors-finans/bank-fintech/klarna-fryser-anstallningar-och-satsar-pa-ai/ . Supports: July 2026 headline only; article not seen. Seen 2026-10-31. Snippet only.
- S15: https://ophyai.com/blog/company-guides/klarna-interview-guide . Supports: third-party 2026 guide; Klarna reportedly has no single fixed process, ask the recruiter. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium confidence that a logic test, an ML case or take-home, and team and culture interviews feature for data science; low confidence in durations, take-home size and ML engineer specifics [S1][S2][S5].
- India: no India-based reports found; general process evidence only.
- Verify with the Klarna recruiter and careers page: which stages apply to your role and office, the take-home scope, and any AI-use rules.
- No claim here that any question will be asked.

### C5 SAP (Enterprise software; Walldorf, Berlin, SAP Labs India)

**Evidence level:** Thin. No official SAP interview-process page appeared in any result, no Walldorf- or Berlin-specific interview report for data science or ML roles was returned, and the reports that did appear are few, mixed across locations and mostly older (2017-2022, with a few 2025-2026 items) [S1][S3][S6].

**Roles seen in sources:** Data Scientist (guide and Glassdoor summaries, location mostly not stated) [S1][S3]; Machine Learning Engineer in Bengaluru (anecdotal) [S4]; AI Engineer and Senior AI Engineer (Glassdoor, location not stated) [S6]; Senior and Lead Applied Research Scientist, Machine Learning Scientist and ML Engineer postings in Walldorf and Berlin (job listings only, no interview content) [S7]; Research Scientist (generic guide) [S8].

**Process overview (as reported):**
1. Application and recruiter or HR screen. A generic stage list (HR screen, technical assessment, manager discussion, final HR round) comes from a general review-site FAQ, not from a data science source [S9].
2. Online assessment or take-home. One guide lists an online technical assessment [S1]. Anecdotal Glassdoor items mention a take-home ML task (a Singapore candidate around 2018, a text-classification task) and a later report of a first-round take-home on AI/ML [S5]. A 2018 candidate reported a 3-day data challenge, then a manager phone chat about a past project (anecdotal, old) [S1].
3. Technical interviews. A guide describes a behavioural interview, a technical panel mixing whiteboard-style data structures with situational prompts, and sometimes a hands-on coding round [S1]. A Bengaluru ML candidate reported two technical rounds, the first on basic to intermediate ML and the second deeper on deep learning (anecdotal) [S4]. A Feb 2026 "Senior AI Engineer" report (location not stated) describes a recruiter call, a technical round with a LeetCode-style problem and an ML system design question, then a hiring-manager conversation (anecdotal) [S6].
4. Manager or panel round on past projects [S1][S4].
5. Duration is not found in a reliable source. A guide says 3-5 weeks for data science; a Glassdoor summary of four submissions gives a much longer average; one FAQ says 2 weeks to 3 months. Treat all as rough [S1][S9].
6. Location note: Walldorf and Berlin: no interview reports found [S6]. SAP Labs India (Bengaluru and other cities): small anecdotal set only [S4][S10][S11].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter or HR screen | Call | Background, role fit, profile details | [S9] generic |
| Online assessment or take-home | Online test or multi-day task | ML or analytics task, sometimes an IQ-style test | [S1][S5][S6] anecdotal |
| Technical round 1 | Live, coding or ML basics | DSA (medium level), SQL and analytics, ML fundamentals | [S1][S10] anecdotal |
| Technical round 2 / panel | Live, panel or team | Deep learning or ML depth, project deep dive, ML system design | [S4][S6] anecdotal |
| Manager round | Conversation | Past work, setbacks, working with non-technical stakeholders | [S10][S1] anecdotal |
| Final HR | Conversation | Culture fit, expectations | [S9] generic |

**Question types:**
- Coding at roughly medium LeetCode level (strings, linked lists, trees; a matrix rotation problem; a dynamic programming problem in a text editor) [S10][S1].
- ML fundamentals: regression, SVM, recommendation systems, Z-test, logistic regression (anecdotal, older) [S10][S5].
- Deep learning: CNN implementation, a question on Boltzmann machines (Bengaluru, anecdotal) [S4][S5].
- Modern AI: projects with RAG, transformers, evaluation metrics (Singapore and other locations, anecdotal) [S6].
- Project walkthroughs and behavioural questions about setbacks and stakeholders [S1][S10].

**Sample questions (illustrative):**
- Explain logistic regression, its loss and how you would handle class imbalance. [S5] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding) and Book 1 Part 2 (regression, regularization).
- Walk through a past ML project: data, features, model choice, what you would change. [S1] Book 6 Part 10 (design a solution end-to-end).
- Design an A/B test and explain a Z-test on conversion. [S10] Book 1 Part 10 (A/B testing, causal inference, experimentation).
- Rotate a matrix in place, then state the complexity. [S10] Book 5 Part 13 (matrices and 2D grids).
- Build a simple RAG pipeline for support documents and say how you would evaluate it. [illustrative] Book 2 Part 6 (RAG basics) and Book 2 Part 9 (LLM evaluation).
- Design an ML system that tags invoices with a category: data, model, serving, monitoring. [S6] Book 1 Part 11 (ML system design) and Book 4 Part 8 (monitoring).
- How do you explain a model result to a non-technical stakeholder who disagrees? [S10] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).

**What they score:**
- Practical, fit-focused and manager-driven style, per one guide [S1].
- Ability to explain past projects, since several reports centre on them [S1][S6][S10].
- AI and RAG project experience helped in one Glassdoor comment (anecdotal) [S6].
- One reviewer felt a role advertised as ML leaned on general software engineering skill (anecdotal, single opinion, not the process) [S5].

**Level notes:**
- Job listings name Senior and Lead Applied Research Scientist and Senior or Expert ML Engineer levels in Walldorf and Berlin; expectations are in the postings, not in interview sources [S7].
- Associate-level and campus items exist for SAP Labs India but cover associate developer roles, not data science [S11].
- Level-specific interview differences were not found in sources.

**Preparation plan (2 weeks):**
- Days 1-2: Medium DSA in a plain editor: arrays, strings, linked lists, trees, matrices. Book 5 Parts 1, 3, 6, 7, 13.
- Days 3-4: SQL and analytics fluency. Book 3 Parts 3-5 and 8.
- Days 5-6: ML fundamentals and metrics. Book 1 Parts 1-4.
- Days 7-8: Deep learning and a CNN from memory. Book 1 Part 8.
- Days 9-10: GenAI and RAG basics with an evaluation story. Book 2 Parts 6, 7, 9.
- Days 11-12: ML system design and one project walkthrough per role. Book 1 Part 11, Book 6 Part 10.
- Days 13-14: Behavioural stories on setbacks and stakeholders, then two mocks. Book 6 Part 6 [G].

**Common mistakes:**
- Preparing only ML theory when reports mention medium-level coding and LeetCode-style items [S10][S6].
- Being unable to go deep on your own project, which several reports centre on [S1][S6].
- Using one location's report (for example Singapore or Bengaluru) as a Walldorf or Berlin template [S6].
- Treating a decade-old report as the current loop [S1].

**Recent changes and AI-era notes:**
- No SAP candidate-facing AI-tool policy was found. Results only showed SAP selling a generative AI interview-question feature to customer interviewers, which says nothing about SAP's own hiring [S12].
- Newer (2025-2026) reports in snippets: a Feb 2026 Senior AI Engineer report with coding plus ML system design, and a Dec 2025 Bengaluru-area report with medium-level coding; the older take-home items are from around 2018-2022 [S6][S10][S5].
- Whether AI tools are allowed in your rounds: not found in sources, ask the recruiter [U].

**Sources:**
- S1: https://www.interviewquery.com/guides/sap-data-scientist . Supports: 3-5 round data scientist outline, online assessment, behavioural, technical panel, 3-day data challenge (2018) and manager project chat, behavioural examples. Seen 2026-10-31. Snippet only (via search summary).
- S2: https://dataford.io/interview-guides/sap-labs/data-scientist . Supports: existence of a SAP Labs data scientist prep page with limited detail (paid-prep site). Seen 2026-10-31. Snippet only.
- S3: https://www.glassdoor.ie/Interview/SAP-Interview-E10471-RVW97417593.htm . Supports: Glassdoor data scientist report appearing for the process query; detail used only through the search summary. Seen 2026-10-31. Snippet only.
- S4: https://www.glassdoor.co.in/Interview/SAP-Interview-E10471-RVW76831815.htm . Supports: Bengaluru ML-related Glassdoor report appearing in the SAP Labs India query (two technical rounds, deep learning round, Boltzmann machine question, about 2 weeks; the summary did not tie each detail to one URL). Anecdotal. Seen 2026-10-31. Snippet only.
- S5: https://www.glassdoor.com.br/Entrevista/SAP-Entrevista-E10471-RVW20161798.htm . Supports: Glassdoor review appearing for the take-home and ML query (take-home ML tasks, three-stage report, CNN and logistic regression questions; summary did not tie each detail to one URL). Anecdotal, 2017-2022 mostly. Seen 2026-10-31. Snippet only.
- S6: https://static-pc.glassdoor.de/Interview/SAP-AI-Engineer-Interview-Questions-EI_IE10471.0,3_KO4,15_IP2.htm . Supports: SAP AI Engineer Glassdoor page (two reports, group panel, IQ-style test, project and RAG emphasis); the Feb 2026 Senior AI Engineer description came from the search summary of Glassdoor results, location not stated. Anecdotal. Seen 2026-10-31. Snippet only.
- S7: https://jobs.sap.com/go/Germany/8806101/0/ . Supports: SAP careers listing pages with Berlin and Walldorf applied research scientist and ML engineer openings (postings only, no interview content). Seen 2026-10-31. Snippet only.
- S8: https://interviewquery.com/interview-guides/sap-research-scientist . Supports: generic statement that interviews at SAP vary by role and team; no research-talk format. Seen 2026-10-31. Snippet only.
- S9: https://in.indeed.com/cmp/SAP/faq/hiring-process . Supports: generic stage list (HR screen, technical assessment, manager discussion, final HR); timelines 2 weeks to 3 months. Seen 2026-10-31. Snippet only.
- S10: https://www.glassdoor.com.hk/Interview/SAP-Interview-E10471-RVW97417593.htm . Supports: mirror of the data scientist report in S3; Glassdoor India data scientist summary (5 interviews: one-on-one, skills test, phone, presentation), medium-level coding, project explanation, setbacks and stakeholder questions; summary did not tie each detail to one URL. Anecdotal. Seen 2026-10-31. Snippet only.
- S11: https://www.geeksforgeeks.org/?p=482694 . Supports: SAP Labs (India) on-campus 2021 associate developer experience, with ML concepts mixed in; campus, not data science. Anecdotal, older. Seen 2026-10-31. Snippet only.
- S12: https://www.sap.com/use-cases/generating-interview-questions . Supports: SAP product page on generative AI for interviewer question generation; not a candidate policy. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Confidence is low on round count, order and duration. Verify with the recruiter: number of rounds, whether there is a take-home, whether the loop is coding-heavy for your team, and whether AI tools are allowed.
- Verify the location and team for each interview: Walldorf, Berlin and SAP Labs India (Bengaluru and other cities) may differ and the evidence here is not location-specific [S6].
- Check jobs.sap.com for the exact posting and its listed requirements [S7].
- India-only candidates: the India items here are general process evidence only; this profile makes no statement on relocation or legal matters (see Book 8) [G].


### C6 Delivery Hero (Food and quick-commerce delivery; Berlin and other hubs)

**Evidence level:** Medium. An official careers page and an official tech-blog interview post exist, and several 2025 Glassdoor reports describe a similar five-step shape, but the official material is aimed at engineering and is dated (2019-2023), data-science reports are anecdotal and differ on round count, and no interview content for India or other hubs was found for data science [S1][S2][S4][S3].

**Roles seen in sources:** Data Scientist and Senior Data Scientist in Berlin (Glassdoor, guides) [S4][S5][S3]; ML Engineer (guide only, no role-specific Glassdoor report found) [S6][S9]; Data Engineer in Berlin (Glassdoor, Dec 2025) [S8]; logistics-optimization, search and quick-commerce data science and ML postings in Berlin (postings only) [S10]. Data Analyst in Navi Mumbai appeared once, not data science [S11].

**Process overview (as reported):**
1. Recruiter call, about 30 minutes in the official engineering description; HR screen of 30 minutes in a July 2025 senior data scientist report (anecdotal) [S2][S4].
2. Technical interview, about one hour in the official engineering description, run by a senior engineer from the hiring team, with live coding where reasoning matters more than exact syntax [S2]. For data science, Glassdoor reports describe SQL/Python or a coding round and a data-science deep dive where a case scenario is given and candidates write and run code live (anecdotal) [S12][S8][S4].
3. System design interview for senior-and-above engineering roles, one hour, a real-world problem scenario [S2]. A June 2025 Berlin report says the bar raiser covered system design and ML questions (anecdotal, wording unclear) [S7].
4. Hiring manager interview, about one hour officially; a report mentions 90 minutes plus a take-home and a case study with a head of function (anecdotal) [S2][S12].
5. Bar raiser interview with an interviewer from another team, reported at 1.5 hours in one senior data scientist report and as LeetCode-medium plus past experience in another (anecdotal) [S4][S7][S3].
6. Number of stages and order vary by role and location, per the careers page [S1]. Data-science reports range from 4 to 5 rounds, versus a Dataford "5 rounds" label [S3][S4].
7. Duration: one senior report says about one week per round, so at least 1-1.5 months; others report about 2 weeks or 1 to 2 months; Dataford says 3 to 5 weeks for data science (anecdotal and guide figures, not official) [S4][S3][S12].
8. Location note: Berlin is the main location in the data-science evidence; other hubs and India: no data-science interview evidence found [S5][S11].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter or HR screen | Call, about 30 min | Background, role fit | [S2][S4] |
| Technical round | About 1 hour, live | Coding, SQL and Python; reasoning aloud | [S2][S8] |
| Data-science deep dive | Case scenario plus live code | Applied modelling, analysis, metrics | [S12][S3] anecdotal |
| System design (senior-and-above, engineering) | About 1 hour | Real-world solution design | [S2] |
| Hiring manager | About 1 hour, past work | Experience, trade-offs | [S2][S8] |
| Take-home or case (some reports) | Task plus discussion | Analysis and presentation | [S12] anecdotal |
| Bar raiser | 1-1.5 hours, interviewer from another team | System design, ML, past experience, fit | [S4][S7][S3] |

**Question types:**
- SQL and Python coding [S8][S2].
- Diagnosing a sudden 10% drop in a key product metric (Dataford sample) [S3].
- ML model building basics, with one candidate noting repeated questions on basics (anecdotal, June 2025) [S13].
- ML system design for scalable ML, API deployment, production ML (guide topics) [S6][S9].
- LLM question on keeping a model's customer answers within company policy (July 2025 senior report, anecdotal) [S4].
- Past-experience and business-understanding questions, including ranking and search metrics (garbled single report) [S7].

**Sample questions (illustrative):**
- Orders per hour dropped 10% in one city overnight; how do you find out why? [S3] Book 6 Part 1 (product metrics and metric drops) and Book 3 Part 8 (funnels, conversion, DAU/MAU, product metrics).
- Write SQL to compute delivery time percentiles by zone and flag zones with a rising trend. [illustrative] Book 3 Part 4 (window functions) and Part 5 (running totals, LAG/LEAD).
- Design a model to estimate preparation plus delivery time for an order and say how you would monitor it. [illustrative] Book 1 Part 11 (ML system design) and Book 4 Part 8 (monitoring).
- How would you stop an LLM support assistant from giving answers that break company policy? [S4] Book 2 Part 5 (alignment, safety, guardrails) and Book 2 Part 11 (LLMOps, security).
- Design an experiment for a new search ranking change and name guardrail metrics. [S7] Book 1 Part 7 (recommenders, ranking, search) and Book 1 Part 10 (A/B testing).
- Given a delivery dataset, run an analysis live and present trade-offs to a hiring manager. [S12] Book 6 Part 5 (business case studies) and Book 1 Part 12 (live-coding rounds).
- Solve a medium graph problem such as the shortest route between two points, with complexity. [illustrative] Book 5 Part 9 (graphs).

**What they score:**
- Official engineering guidance: problem-solving and reasoning over exact syntax; narrate your thinking [S2].
- Hiring standards checked by an interviewer from another team (bar raiser), per a guide and reports [S3][S7].
- Experimentation rigor and code quality appear in a senior posting's expectations [S10].
- Business and metric understanding is a recurring theme in case and bar-raiser reports (anecdotal) [S3][S7].

**Level notes:**
- System design is described as required for senior-and-above engineering roles [S2].
- Senior Data Scientist reports show the longer five-round loop [S4].
- Postings name Data Scientist, Senior Data Scientist and Staff-level roles in logistics, search and quick commerce; expectations are in postings, not interview sources [S10].

**Preparation plan (2 weeks):**
- Days 1-2: SQL windows, cohorts and funnels on delivery-style data. Book 3 Parts 4-6 and 8.
- Days 3-4: Metric drops and diagnosis frameworks. Book 6 Parts 1 and 5.
- Days 5-6: Experiments, ranking and search. Book 1 Parts 7 and 10; Book 6 Part 4.
- Days 7-8: ML fundamentals and time series for ETA and demand. Book 1 Parts 1-4 and 6.
- Days 9-10: Live coding in a plain editor, speaking aloud. Book 5 Parts 1, 2, 9 and Book 1 Part 12.
- Days 11-12: ML system design and deployment; GenAI guardrails if relevant. Book 1 Part 11, Book 4 Parts 6 and 8, Book 2 Parts 5 and 11.
- Days 13-14: Past-experience stories for hiring manager and bar raiser, then a mock case with a take-home style presentation. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Jumping into code before clarifying the case or metric definition (guide advice) [S12].
- Preparing only ML theory when reports describe live coding and case work [S2][S12].
- Silent coding; the official post asks candidates to narrate [S2].
- Assuming the loop is fixed; the careers page says stages vary by role [S1].
- Reading Deliveroo material as Delivery Hero material; they are different companies [U].

**Recent changes and AI-era notes:**
- Official engineering post (2023) and a 2019 post describe live coding at every level and a bar raiser step; these are older and for engineering [S2].
- 2025 reports: July 2025 five-round senior data scientist loop, June 2025 Berlin bar-raiser report, Dec 2025 data engineer report (anecdotal) [S4][S7][S8].
- A generative-AI question about LLM policy compliance appeared in a July 2025 report, showing GenAI knowledge can be asked in data science loops (single anecdote) [S4].
- No Delivery Hero candidate AI-tool policy was found; ask the recruiter [U].

**Sources:**
- S1: https://careers.deliveryhero.com/howwehire . Supports: official statement that the number of stages and their order may vary by role. Seen 2026-10-31. Snippet only.
- S2: https://tech.deliveryhero.com/preparing-for-your-technical-interview-delivery-hero-2 . Supports: official tech-blog loop (recruiter call about 30 min, 1 hour technical, 1 hour system design for senior-and-above, 1 hour hiring manager, bar raiser), live coding emphasis on reasoning, may vary by role and location; the 2019 live-coding detail came via the careers search summary of earlier posts. Engineering-oriented. Seen 2026-10-31. Snippet only.
- S3: https://dataford.io/interview-guides/delivery-hero/data-scientist . Supports: guide with Berlin hybrid team, recruiter screen first, 10% metric drop sample, 3-5 weeks, bar raiser from another team; paid-prep site, offer-rate figure judged unreliable. Seen 2026-10-31. Snippet only.
- S4: https://www.glassdoor.co.uk/Interview/Delivery-Hero-Interview-E504556-RVW97097113.htm . Supports: July 2025 Senior Data Scientist report: HR 30 min, hiring manager 1 hour, two technical rounds, 1.5-hour bar raiser, about a week per round, LLM policy question (anecdotal). Seen 2026-10-31. Snippet only.
- S5: https://static.glassdoor.co.nz/Interview/Delivery-Hero-Data-Scientist-Interview-Questions-EI_IE504556.0,13_KO14,28.htm . Supports: Glassdoor data scientist listing; Berlin reports, common stages phone interview, presentation, one-on-one (3 interviews, tiny sample). Seen 2026-10-31. Snippet only.
- S6: https://www.interviewquery.com/interview-guides/delivery-hero-ml-engineer . Supports: ML engineer guide topics (ML theory, scalable ML system design, API deployment, communication); scope disagrees across guide versions. Seen 2026-10-31. Snippet only.
- S7: https://static.glassdoor.sg/Interview/Delivery-Hero-Interview-E504556-RVW99785483.htm . Supports: Glassdoor Berlin report (June 2025 per search summary): four-round loop with deep dive and bar raiser covering system design, ML and past experience; summary did not tie each detail to one URL. Anecdotal. Seen 2026-10-31. Snippet only.
- S8: https://static.glassdoor.sg/Interview/Delivery-Hero-Data-Engineer-Interview-Questions-EI_IE504556.0,13_KO14,27.htm . Supports: Berlin data engineer report, Dec 2025: recruiter call, SQL and Python technical round, hiring manager on past projects (role is data engineering). Anecdotal. Seen 2026-10-31. Snippet only.
- S9: https://interviewquery.com/interview-guides/delivery-hero-data-scientist . Supports: guide listing 10-12 question topics for data scientist with ML system design as a frequent topic. Seen 2026-10-31. Snippet only.
- S10: https://careers.deliveryhero.com/job/data-scientist-logistics-optimization-in-berlin-germany-jid-10905 . Supports: Berlin logistics-optimization data scientist posting (Python, pandas, scikit-learn, SQL, ML pipelines); experimentation-rigor expectation seen in a senior search posting summary. Postings only. Seen 2026-10-31. Snippet only.
- S11: https://dataford.io/interview-guides/delivery-hero-india/data-scientist . Supports: existence of a Delivery Hero India guide page with role description only; the only India Glassdoor item seen was a Navi Mumbai data analyst report (not data science). Seen 2026-10-31. Snippet only.
- S12: https://interviewquery.com/interview-guides/delivery-hero-data-analyst . Supports: guide statement that take-homes mean analysing a dataset and presenting; case presentation to a panel; plus Glassdoor items in the same results (hiring manager round of 90 minutes, take-home, case with a head of function, deep-dive with live code; analytics-adjacent roles). Seen 2026-10-31. Snippet only.
- S13: https://www.glassdoor.es/Entrevista/Delivery-Hero-Entrevista-E504556-RVW99675065.htm . Supports: June 2025 report with repeated questions on ML basics such as building a model (anecdotal; role not confirmed as ML engineer). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium confidence on the shape (recruiter, technical, hiring manager, bar raiser, system design for senior engineering); low on exact data-science rounds and durations.
- Verify with the recruiter: stage list for your role, whether there is a take-home, whether coding is live with a shared editor, and whether AI tools are allowed.
- Verify location: Berlin dominates the evidence; other hubs and India are not covered for data science [S5][S11].
- Re-check careers.deliveryhero.com/howwehire for current wording [S1].
- India-only candidates: any India item here is general process evidence only; no statement on relocation or legal matters (see Book 8) [G].

### C7 Revolut (fintech; London and other offices)

**Entity note:** Revolut is a global fintech with engineering and data hubs in several cities. Most Glassdoor and guide material mixes offices. Where a source names an office it is stated below: London (take-home reports for ML and data roles, mostly 2019-2020 and older) [S2], Kraków (a data scientist posting) [S16]. The official hiring-sprint page is for product owners, not data roles [S5]. No source in the results gave a usable process description for a Bengaluru or Hyderabad data scientist loop [S17].

**Evidence level:** Thin. No official Revolut page describes the data science or ML loop; guides disagree on round counts (three, four, five); detailed Glassdoor material seen is old (2018-2020) or for other titles; and recent ML, applied scientist and GenAI reports are guide-level, not candidate accounts [S1][S7][S6].

**Roles seen in sources:** Data Scientist [S1][S3], Machine Learning Engineer (London, older take-home reports) [S2], AI Engineer and Applied AI Engineer, including a graduate Applied AI Engineer programme [S7][S8][S9], Deep Learning Engineer for NLP / applied research [S10], Data Analyst (adjacent) [S3].

**Process overview (as reported):**
1. Recruiter or HR screening call; one London review says it included technical questions (anecdotal, old) [S2][S1].
2. Online or take-home assessment. Guides report intermediate SQL, Python and statistics in an online test (a HackerRank-style test is mentioned by candidates) [S1]. London reviews from about 2019-2020 describe a take-home data or ML challenge with a deadline of a few days to a week, with an ETL step, a model, an evaluation, and a per-user action algorithm in one ML engineer account (anecdotal, old) [S2].
3. Live technical interview: reports of a 45-minute live SQL coding round [S1] and of a technical interview that includes presenting the take-home plus live coding (anecdotal, old) [S2][S3].
4. Team or manager interview and an HR interview in one five-stage candidate description [S1]; other candidate summaries mention a hiring manager interview, a problem-solving round and a bar-raiser round for various roles [S6]. The only official stage names found (Skills, Bar Raiser, Team Fit) are from a product-owner hiring sprint, not data roles [S5].
5. For AI engineer roles, a third-party guide lists recruiter screen, deep technical rounds, a behavioural round and a stakeholder interview with senior staff [S7]. Treat as unverified for any given team [U].
6. Duration: guides say about 2-4 weeks [S1]; Glassdoor and Indeed summaries conflict widely [S6]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / HR screen | Call | Fit, background, role match | [S1][S2] |
| Online assessment | Timed test | SQL, Python, statistics | [S1] |
| Take-home challenge (older London reports) | Days to a week, then presented | Data work, ETL, modelling, evaluation, communication | [S2] anecdotal, old |
| Live technical | Live SQL or coding, about 45 min in one report | SQL, Python, DS questions such as regression and hypothesis tests | [S1][S3] anecdotal |
| Team / manager / HR | Interviews | Fit, project depth, motivation | [S1][S6] |
| Deep dive and stakeholder (AI engineer, guide only) | Interviews | Technical depth, system design, senior stakeholder fit | [S7] unverified |

**Question types:**
- SQL and Python coding, described by one guide as notably coding-heavy [S1].
- Statistics and classical ML: linear regression, hypothesis tests, regularisation, collaborative filtering (anecdotal, mostly older) [S3][S2].
- Case or product scenario: a transactions database where some users have only one or two transactions and you must suggest how to raise usage (anecdotal) [S3]. One senior analyst report describes several case questions built around an in-app ads widget for partner offers (analyst role, anecdotal) [S3].
- Take-home presentation: explain your approach, code quality and thinking, not only accuracy (guide statement, third party) [S2].
- LLM topics for AI engineer roles: LLM evaluation metrics and handling hallucinations (sample question from a prep site) [S8].
- Behavioural and motivation questions [S1][S6].

**Sample questions (illustrative):**
- Users with one or two transactions: how would you analyse the data to increase their usage? [S3] Book 6 Part 5 (business case studies: pricing, churn, fraud, supply chain) and Book 6 Part 9 (domain sets: fintech).
- Write SQL to find each customer's second transaction and the days since the first. [illustrative] Book 3 Part 4 (window functions: ranking, top-N per group) and Book 3 Part 5 (running totals, LAG/LEAD).
- Explain regularisation in linear regression and how you would choose the penalty. [S3] Book 1 Part 2 (linear/logistic regression, regularization, feature engineering).
- Test a hypothesis that a new in-app offer widget raises click-through, and say what could go wrong. [illustrative] Book 1 Part 10 (A/B testing, causal inference, experimentation) and Book 6 Part 4 (experiment design).
- Design a fraud-scoring model for card payments: features, label delay, threshold, monitoring. [illustrative] Book 1 Part 11 (ML system design) and Book 1 Part 3 (classification metrics, imbalance).
- Which metrics would you use to evaluate an LLM assistant, and how do you handle hallucinations? [S8] Book 2 Part 9 (LLM evaluation) and Book 6 Part 7 (GenAI scenarios).
- Take-home style: build and evaluate a model on a transactions file and present it in 15 minutes. [illustrative] Book 1 Part 12 (NumPy/pandas/sklearn live-coding) and Book 6 Part 10 (design a solution end-to-end).

**What they score:**
- Practical data science and coding skill, per prep guides [S1].
- For take-homes, code quality, documentation and thought process, not accuracy alone (third-party guide statement) [S2].
- One candidate said each interviewer has a veto on the hiring decision (anecdotal, role unknown) [S6].
- Official materials for other roles name Skills, Bar Raiser and Team Fit stages; the data-role equivalent is not confirmed [S5][U].

**Level notes:**
- Seen titles: Data Scientist, Senior Data Scientist (Kraków posting), Senior Data Analyst (candidate report), Deep Learning Engineer, Applied AI Engineer, and a graduate Applied AI Engineer programme with a stated recruitment window of July to December 2026 and graduation years 2025-2027 [S16][S3][S10][S9].
- Level-specific round differences were not found in snippets [U].

**Preparation plan (2 weeks):**
- Days 1-2: SQL windows, cohorts, retention on transaction data. Book 3 Parts 4-6 and 8.
- Days 3-4: Statistics, regression, hypothesis tests, regularisation. Book 1 Parts 2, 13, 14.
- Days 5-6: Classification, imbalance, fraud and risk metrics. Book 1 Part 3 and Book 6 Part 9 (fintech).
- Days 7-8: Timed coding in a plain environment, pandas and Python. Book 1 Part 12, Book 5 Parts 1-3 [G].
- Days 9-10: Mock take-home: a small modelling task, a short written summary, a 15-minute presentation. Book 6 Part 10 [G].
- Days 11-12: Experimentation and product cases. Book 1 Part 10, Book 6 Parts 4-5.
- Days 13-14: If the role is AI or GenAI, LLM evaluation and RAG basics; then behavioural stories and a mock. Book 2 Parts 6 and 9, Book 6 Part 7 [G].

**Common mistakes:**
- Treating old London take-home reports as the current process [S2].
- Submitting a model without explaining code structure and reasoning, since reviewers are said to look beyond accuracy (guide claim) [S2].
- Assuming the loop matches a software engineer or product owner loop described elsewhere [S4][S5].
- Not asking the recruiter for the stage list and prep material; one candidate advised reading the recruiter's prep material closely (anecdotal) [S6].
- Treating one candidate's round count as the standard [G].

**Recent changes and AI-era notes:**
- April 2025: Revolut launched an AI-driven people product that includes an AI interview and summarisation tool, reported by industry press [S12]. This is a product announcement, and its scope in actual data-role hiring is not stated.
- Official privacy notice for a Revolut interview process (official, undated in snippet) says candidates can ask for a non-AI interview before the interview by replying to the invitation or contacting the recruiter [S11].
- June 2026 Glassdoor review (anecdotal, one person) says to expect AI to play a significant role in the technical evaluation with limited direct interaction [S13].
- A commercial prep site says its HireVue round is scored by humans against a rubric, which conflicts with the AI-scoring reports; weighted low [S15][U].
- Industry press reported a very large number of applications and slower hiring, and possible changes to the interview structure (details not in snippet) [S14].
- No official statement was found on whether candidates may use AI tools during coding or take-home rounds [U].
- Older: the 2018-2020 take-home presentation format [S2].

**Sources:**
- S1: https://www.interviewquery.com/guides/revolut-data-scientist . Supports: DS process (HR screen, live coding, SQL/Python), 2-4 weeks, coding-heavy; a five-stage candidate version (screen, HackerRank, 45-minute live SQL, team, HR) comes from the search summary of several results. Seen 2026-10-31. Snippet only.
- S2: https://static.glassdoor.ch/Interview/Revolut-Interview-E1176471-RVW22155164.htm . Supports: London ML-role Glassdoor review set (take-home challenge, later calls with a Lead Data Scientist, ETL/model/evaluation take-home from a 2019 ML engineer review; anecdotal, old). The page-to-detail match is from the search summary of several Glassdoor results, and the code-quality statement is from a third-party guide in the same results. Seen 2026-10-31. Snippet only.
- S3: https://www.tryexponent.com/experiences/revolut-data-scientist-interview-ac4820 . Supports: a data scientist interview experience listing; case and take-home details (customer-transactions scenario, regression and hypothesis tests, a senior analyst ads-widget case) come from the search summary of several Glassdoor and Exponent results. Seen 2026-10-31. Snippet only.
- S4: https://www.efinancialcareers.com/news/revolut-reveals-its-five-stage-interview-process-for-software-engineers . Supports: five-stage process for software engineers with a coding assessment then a tech conversation (software engineers, not data roles). Seen 2026-10-31. Snippet only.
- S5: https://www.revolut.com/hiring-sprint-product-owners/ . Supports: official Revolut page for the product owner hiring sprint (initial screening, problem-solving interview, then Skills, Bar Raiser and Team Fit in one day). Not a data role. Seen 2026-10-31. Snippet only.
- S6: https://ie.indeed.com/cmp/Revolut/faq/hiring-process . Supports: anecdotal Indeed answers (recruiter call, hiring manager, problem solving, bar raiser; veto claim; inconsistent feedback; conflicting timelines), mixed roles. Seen 2026-10-31. Snippet only.
- S7: https://www.interviewquery.com/prep-guides/revolut-ai-engineer . Supports: AI engineer guide (recruiter screen, deep technical rounds, behavioural round, stakeholder interview), third party. Seen 2026-10-31. Snippet only.
- S8: https://dataford.io/interview-guides/revolut/ai-engineer . Supports: LLM evaluation and hallucination sample question; third-party prep site. Seen 2026-10-31. Snippet only.
- S9: https://www.revolut.com/careers/position/d149dd16-43e9-4372-a4f7-e706d7840797/ . Supports: official Graduate Programme 2027 Applied AI Engineer posting (recruitment July-December 2026, graduation years 2025-2027, LLM-based features). Office not stated in the snippet. Seen 2026-10-31. Snippet only.
- S10: https://jobs.coatue.com/companies/revolut-com/jobs/49001583-deep-learning-engineer-applied-research . Supports: Deep Learning Engineer applied research posting (April 2025; applied research mindset; agentic systems a plus), job board copy. Seen 2026-10-31. Snippet only.
- S11: https://www.revolut.com/legal/culturalfit-privacy-notice/ . Supports: official privacy notice, AI interview and the option to request a non-AI interview. Seen 2026-10-31. Snippet only.
- S12: https://fintech.global/2025/04/14/revolut-enhances-hr-tech-with-ai-driven-hiring-and-performance-platform/ . Supports: April 2025 launch of AI-driven hiring tools including an AI interview and summarisation tool. Seen 2026-10-31. Snippet only.
- S13: https://www.glassdoor.com/Interview/Revolut-Interview-E1176471-RVW102772059.htm . Supports: June 2026 anecdotal review about AI in technical evaluation. Role and office not shown in the snippet. Seen 2026-10-31. Snippet only.
- S14: https://www.efinancialcareers.com/news/revolut-hiring-slows-down-average-pay . Supports: report of high application volume, slower hiring and possible interview-structure changes (pay content in the article not used). Seen 2026-10-31. Snippet only.
- S15: https://www.intervyo.co.uk/firms/revolut/hirevue . Supports: commercial prep-site claim that the HireVue round is scored by humans against a rubric. Seen 2026-10-31. Snippet only.
- S16: https://justjoin.it/offers/revolut-data-scientist-krakow-data . Supports: a Kraków data scientist posting exists (pay content discarded). Seen 2026-10-31. Snippet only.
- S17: https://www.fishbowlapp.com/post/hi-all-anyone-data-scientists-working-at-revolut-i-am-currently-at-the-final-interview-stages-for-a-data-scientist-remote-position . Supports: only that a candidate was at a final stage for a remote data scientist role; no process detail in the snippet. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence in round counts and order; guides say three, four or five stages and detailed take-home accounts are from 2018-2020 [S1][S2][S4].
- India: no process detail for Bengaluru or Hyderabad data roles was found; Glassdoor listings tagged to those cities showed no usable detail. Do not assume an Indian loop differs or matches London [S17].
- Verify with the recruiter and the role's careers page: the stage list, whether there is a take-home or online test, whether the AI interview tool is used for your role, how to request a non-AI interview, and the rules on AI tools during assessments [S11][S12].
- Nothing here says any question will be asked; sample questions are illustrative unless tagged to a source.

### C8 Wise (fintech; London, Tallinn and other offices)

**Entity note:** Wise (formerly TransferWise) lists engineering hubs in London, Tallinn and Budapest in one job-board posting [S12]. Offices named by sources: London (data scientist and data analyst reviews, 2019-2026) [S2][S3], Tallinn (a June 2025 review with role not shown, an April 2026 Data Science Intern review, and Senior Data Scientist reviews from 2017 and 2019 per a search summary) [S10][S14], Tallinn or Budapest (Servicing ML and Data Engineering team posting) [S11][S12]. No source gave a process specific to an India-based candidate.

**Evidence level:** Thin to Medium. Wise has official pages on the analytics case study and on AI use in recruitment [S5][S6], and several recent Glassdoor accounts exist, but there is no official page listing the data scientist or ML engineer rounds, accounts mix roles and offices, and ML engineer and applied scientist interviews are barely covered [S1][S2][S9].

**Roles seen in sources:** Data Scientist (London) [S1][S2], Data Analyst and Senior Data Analyst (adjacent) [S4][S2], Data Science Intern (Tallinn) [S14], Senior and Lead Machine Learning Engineer / Scientist postings (Servicing team, Tallinn or Budapest; London lead posting, expired) [S11][S12], Machine Learning Platform software engineers (Tallinn) [S11]. No applied scientist or GenAI-titled Wise posting appeared in results [U].

**Process overview (as reported):**
1. Recruiter or HR screen [S2][S3].
2. Hiring manager call or screen; in one 2021 account an interview with the data science manager for a position overview came first [S3][S2].
3. A technical test. Reports include a HackerRank-style test and a home assignment (2021) [S3], and a 3-hour take-home covering algorithms and statistics reported in a recent review (anecdotal) [S3]. Wise's official page says many roles include a practical test or take-home task [S6].
4. Case study or live coding. One London account from November 2024 describes a hiring manager interview, a case study and a live coding interview with four SQL questions on a Google Doc [S2]. Wise's official analytics case-study page says it assesses quality and depth of insights, technical approach and customer-centric recommendations [S5].
5. Technical discussion of the take-home, a business case interview, or a stakeholder interview, depending on the account [S3][S4].
6. Third-party description: five stages starting with an online or take-home assessment, followed by live pair programming or case rounds, based on candidate reports [S15]; another guide describes four rounds of about 3-5 weeks for data scientist [S1]. Another guide says there is no single fixed process and the mix depends on role, team, location and seniority [S9].
7. A final non-technical round asked about views on data science, including how a Data Scientist differs from a Machine Learning Engineer, in an April 2026 Tallinn intern report (anecdotal) [S14][S1].
8. Duration: reports range from days to several months; one Tallinn review says 2 months [S10][S9]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / HR screen | Call | Fit, background | [S2][S3] |
| Hiring manager | Call | Role overview, experience | [S2][S3] anecdotal |
| Technical test | HackerRank-style or take-home | Python, SQL, algorithms, statistics | [S3][S6] |
| Case study | Take-home analysis, reviewed with a panel | Insight quality and depth, technical approach, recommendations | [S5][S4] |
| Live coding | Live SQL on a shared document in one report | SQL fluency | [S2] anecdotal |
| Business case / stakeholder | Interview | Business judgement, communication | [S3][S4] anecdotal |
| Final (some accounts) | Non-technical conversation, department lead | Views on role, fit | [S14] anecdotal |

**Question types:**
- SQL, including multi-question live SQL [S2].
- Python and algorithm questions in HackerRank-style tests [S3].
- Statistics and experimentation: a guide says Wise relies on experimentation to drive product changes, so designing tests and interpreting data is evaluated (third party) [S1].
- Case study on a dataset: open-ended analysis, then a presentation or review with analysts; in one account a panel of four gave feedback after a rejection (anecdotal, older) [S4].
- Role-framing questions such as the difference between a data scientist and an ML engineer [S1][S14].
- ML engineer role content is thin in sources; one third-party guide says the AI work is applied to real, messy financial data [S13].

**Sample questions (illustrative):**
- Four SQL questions on a shared doc: for each customer, find first and latest transfer, then monthly retention of senders. [S2] Book 3 Part 6 (date/time: retention, cohorts, MoM/YoY) and Book 3 Part 4 (window functions: ranking, top-N per group).
- Design an experiment to test a new fee display on a transfer screen and say how you would read the results. [S1] Book 1 Part 10 (A/B testing, causal inference, experimentation) and Book 6 Part 4 (experiment design and ambiguous A/B results).
- Here is a dataset of transfers: find what drives drop-off between quote and payment and recommend two actions. [S5] Book 3 Part 8 (funnels, conversion, DAU/MAU, product metrics) and Book 6 Part 1 (product metrics and metric drops).
- What is the difference between a data scientist and a machine learning engineer, and where do you sit? [S1] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).
- Build a fraud or risk model for new-customer onboarding: features, class imbalance, threshold and monitoring. [illustrative] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding) and Book 1 Part 11 (ML system design).
- Write Python to merge two transfer tables, handle missing currencies and compute a conversion-rate summary. [illustrative] Book 1 Part 12 (NumPy/pandas/sklearn live-coding) and Book 3 Part 10 (pivot/unpivot, string ops, NULL traps).
- Explain how you would serve a model with a low-latency requirement and watch it for drift. [illustrative] Book 4 Part 8 (monitoring: drift, data quality, alerting, retraining) and Book 4 Part 6 (serving: FastAPI, batch vs real-time, Triton, BentoML).

**What they score:**
- Official: for the analytics case study, quality and depth of insights, technical approach and customer-centric recommendations [S5].
- Third party: experimentation and test interpretation [S1]; for engineering take-homes, reviewers are said to look at tests, error handling and clear naming (software roles, guide-level) [S9][U].
- Official on AI use: candidates are encouraged to use AI for analysis, prototyping or structuring work, but not to submit fully AI-generated work or uncredited AI solutions for take-home assessments [S6].

**Level notes:**
- Titles seen: Senior Data Scientist, Lead Data Scientist, Senior and Lead ML Engineer / Scientist, Senior II Software Engineer (ML Platform), Data Science Intern [S11][S12][S14].
- What each level is expected to do was not found in snippets [U].

**Preparation plan (2 weeks):**
- Days 1-2: SQL on transfers-style data: windows, cohorts, retention. Book 3 Parts 4-6 and 8.
- Days 3-4: Python and pandas under a timer; HackerRank-style problems. Book 1 Part 12 and Book 5 Parts 1-3 [G].
- Days 5-6: Experiments and statistics. Book 1 Parts 10, 13, 14 and Book 6 Part 4.
- Days 7-9: Practise a case study: open dataset, 2-3 hours, a short write-up, then present it in 15 minutes. Book 6 Parts 1 and 5 [G].
- Days 10-11: Classification, imbalance and risk models; ML system design. Book 1 Parts 3 and 11, Book 6 Part 9 (fintech).
- Day 12: If an ML engineering role, serving and monitoring. Book 4 Parts 6 and 8.
- Days 13-14: Read Wise's AI-use page, plan where you use AI in take-homes and note how you will credit it; behavioural mock. Book 6 Part 6 [G].

**Common mistakes:**
- Submitting a take-home that is AI-generated or uses AI without saying so, contrary to the official page [S6].
- Spending far more than the suggested time on the take-home; a guide for the analyst role suggests about 2 hours and asks candidates not to exceed 3 (third party, other role) [S4].
- Presenting charts without a recommendation, when the official rubric names customer-centric recommendations [S5].
- Treating London reports from 2019-2021 as the current process [S3].
- Using an AI notetaker or recording bot in a live interview; one policy directory says personal bots are not permitted (fragmentary, third party, verify) [S7][U].

**Recent changes and AI-era notes:**
- Official Wise page on AI in recruitment: many roles include a practical test or take-home; AI use is encouraged for data analysis, rapid prototyping or structuring work; fully AI-generated submissions and uncredited AI solutions are not allowed [S6].
- A third-party policy directory says live interviews do not allow AI tools, which is fragmentary; confirm with the recruiter [S7][U].
- A March 2026 Glassdoor review lists the question "Why did you opt out of using our AI tool?", suggesting an AI tool may be offered in some process; one anonymous report, weak evidence [S8].
- Older: the 7-day take-home and panel presentation reported for analyst roles, and the 2021 HackerRank plus business case sequence [S4][S3].

**Sources:**
- S1: https://dataford.io/interview-guides/wise/data-scientist . Supports: four rounds, about 3-5 weeks, experimentation emphasis, data scientist versus ML engineer question; third-party guide. Seen 2026-10-31. Snippet only.
- S2: https://www.glassdoor.co.uk/Interview/Wise-Interview-E637715-RVW102994967.htm . Supports: London reviews (recruiter call, hiring manager call, live coding; a November 2024 account with case study and four SQL questions on a Google Doc). The page-to-detail match comes from the search summary of several Glassdoor results, one of which was for a Senior Data Analyst. Anecdotal. Seen 2026-10-31. Snippet only.
- S3: https://www.glassdoor.co.in/Interview/Wise-Interview-E637715-RVW51879751.htm . Supports: Glassdoor result set for Wise data scientist roles: a 2021 four-step account (data science manager, HackerRank home assignment, technical interview, business case) and a recent 3-hour take-home account; which page holds which account was not shown. Anecdotal. Seen 2026-10-31. Snippet only.
- S4: https://www.interviewquery.com/prep-guides/transferwise-data-analyst . Supports: analyst take-home guidance (7 days, about 2 hours suggested, not to exceed 3) and panel presentation reports; data analyst role, older. Seen 2026-10-31. Snippet only.
- S5: https://wise.jobs/analytics-case-study . Supports: official Wise page on the analytics case study criteria (quality and depth of insights, technical approach, customer-centric recommendations). Seen 2026-10-31. Snippet only.
- S6: https://wise.jobs/using-ai-in-our-wise-recruitment-process . Supports: official AI-in-recruitment guidance (take-home or practical test common; AI encouraged for analysis and prototyping; no fully AI-generated or uncredited work). Seen 2026-10-31. Snippet only.
- S7: https://ophyai.com/blog/interview-tips/companies-that-allow-ai-in-interviews . Supports: third-party directory claim that Wise live interviews do not allow AI tools and personal notetaker bots are not permitted; fragmentary. Seen 2026-10-31. Snippet only.
- S8: https://static.glassdoor.com.ar/Interview/Wise-Interview-E637715-RVW98241950.htm . Supports: a March 2026 review listing the question about opting out of Wise's AI tool; the page-to-question match is from a search summary. Anecdotal. Seen 2026-10-31. Snippet only.
- S9: https://hyring.com/jobseeker-toolkit/interview-questions/company/wise . Supports: generic stage flow and the statement that Wise does not use one fixed process; third party. Seen 2026-10-31. Snippet only.
- S10: https://static.glassdoor.com.ar/Interview/Wise-Interview-Questions-E637715_P68.htm . Supports: a Tallinn candidate who interviewed in June 2025 and reported a process of about 2 months (role not shown). Anecdotal. Seen 2026-10-31. Snippet only.
- S11: https://wise.jobs/job/senior-machine-learning-engineer-servicing-in-tallinn-jid-1721 . Supports: official Senior Machine Learning Engineer posting, Servicing team, Tallinn (pay content in the listing not used). Seen 2026-10-31. Snippet only.
- S12: https://wise.jobs/job/lead-ml-engineer-scientist-in-london-jid-2657 . Supports: official Lead ML Engineer / Scientist posting (London; expired per the search summary); the Tallinn or Budapest and hub-list wording comes from the search summary of job-board results. Seen 2026-10-31. Snippet only.
- S13: https://jobrise.io/en/blog/wise-ai-engineer-resume-interview-2026/ . Supports: third-party guide statement that Wise AI work uses real, messy financial data. Seen 2026-10-31. Snippet only.
- S14: https://www.glassdoor.co.uk/Interview/Wise-Interview-E637715-RVW103747002.htm . Supports: an April 2026 Tallinn Data Science Intern account with a final non-technical round (the page-to-detail match is from a search summary). Anecdotal. Seen 2026-10-31. Snippet only.
- S15: https://dataford.io/interview-guides/wise . Supports: five-stage description (online or take-home assessment, then live pair programming or case rounds) from candidate reports; third party. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium-low confidence in the sequence: recent accounts agree on recruiter or manager screens, a technical test or take-home and a case or live round, but order and counts vary by role, team and office [S2][S3][S9].
- ML engineer and applied scientist processes: almost no candidate accounts; do not infer them from data scientist or analyst reports [U].
- India: no India-specific or India-based-candidate process evidence found; treat the loop as general process evidence only.
- Verify with the recruiter and wise.jobs: stage list, take-home length, which tools and AI use are allowed in each round, and whether live interviews are in person or video [S6][S7].
- Nothing here says any question will be asked; sample questions are illustrative unless tagged to a source.

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

