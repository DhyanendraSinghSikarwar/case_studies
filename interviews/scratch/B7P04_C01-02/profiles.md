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
