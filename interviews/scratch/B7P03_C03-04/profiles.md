### C3 JPMorgan Chase (global bank)

**Evidence level:** Thin to Medium. No official JPMorgan interview page for data science or ML appeared in any snippet; the picture comes from third-party prep guides, job postings and a few anecdotal candidate reports, several of which describe software engineering rather than data science, and India-specific data science reports were sparse [S1][S4][S5].

**Roles seen in sources:** Data Scientist Associate and Senior Associate (Bengaluru) and a Data Scientist Associate posting in Hyderabad, plus a Vice President Data Scientist posting listed for Bangalore/Mumbai [S1][S2]. Applied AI/ML Associate, Associate Senior and Lead (ML engineer / science tracks) in Bengaluru and Hyderabad [S3][S10]. Entity: the postings are for the bank's India technology and data centres (JP Morgan Services India appears as the employing name in listings) [S3]; Corporate and Investment Bank, Consumer and card analytics, and risk analytics groups appear in US postings, not India ones, so do not assume the same group in India [S6]. No Mumbai-specific interview information was found [S1].

**Process overview (as reported):**
1. Application, then an online assessment. Guides say a HackerRank test, about 60 to 90 minutes in one guide; one adds that it may include basic ML concepts (third-party, not official) [S4][S7].
2. For technical roles a technical phone or video interview with a team member covering ML background, algorithms and tools (generic guide for ML engineer) [S8].
3. Final stage: a Superday, described as three to four interviews of 45 to 60 minutes in one day, with coding, a short code review and behavioural interviews, and a system design discussion at senior levels (guide, mainly software engineering) [S4]. Another guide lists technical screening, technical phone interview and a virtual onsite of 3-4 rounds [S6].
4. Candidate reports for ML roles: Python coding at easy-to-medium difficulty, an ML deep dive from traditional ML to transformers and LLMs, a behavioural round touching ML ethics, fairness and privacy, and a resume-focused fit round (anecdotal, Glassdoor) [S8][S9]. An older 2020 account for an AI/ML role: a 45-minute Zoom interview on ML and AI, then a Superday of four 45-minute interviews covering ML, AI, probability and game theory (dated, anecdotal) [S4].
5. Timing: a 3-5 week, 3-round loop in one data-science guide; about 37 days average application-to-decision for Data Scientist in Glassdoor reviews; one Hyderabad Applied AI ML Associate Senior review said 2 weeks (anecdotal; all rough) [S1][S6][S3].
6. Official site, as paraphrased by third parties: four stages (explore, apply, interview, decision); assessment types include structured live interviews, recorded video interviews, virtual skills assessments and technical assessments; process varies by position [S11].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Online assessment | HackerRank, about 60-90 min in one guide | Coding; possibly basic ML concepts | [S4][S7] guide |
| Technical screen | Live call with a team member | ML background, algorithms, tools, a past project | [S8] guide |
| Superday coding | One of 3-4 interviews, 45-60 min | Medium coding problem, short code review | [S4] guide (SWE-focused) |
| Superday ML / AI round | Conversational, 45-60 min in one guide | Project depth, ML knowledge, transformers/LLMs for newer roles | [S8][S9] anecdotal |
| Superday behavioural | Interview | Teamwork, incidents, ethics and fairness for ML roles | [S4][S9] |
| Design round (senior) | Discussion | System design, production ML | [S4][S5] |

**Question types:**
- Python coding, easy to medium, often with a code-review element [S9][S4].
- Core ML: bias-variance and model performance, class imbalance in fraud data, metrics to monitor after deployment [S6][S12][S13].
- SQL, Python and ML for data science roles [S6][S13].
- Project deep dive: a challenging data science project and how you handled its complexity [S13].
- Newer Applied AI/ML postings list prompt design, RAG and production ML system design as skills, which hints at GenAI topics but is not an interview report [S5].
- Behavioural, including a team with internal issues [S6].

**Sample questions (illustrative):**
- How would you handle class imbalance in a card-fraud dataset, and which metrics would you report? [S12] Book 1 Part 3 (classification metrics, imbalance, calibration).
- Explain the bias-variance trade-off and how you would diagnose it from learning curves. [S6] Book 1 Part 1 (stats, probability, ML fundamentals) and Part 2 (regularization).
- After deploying a model, which metrics do you monitor and what triggers retraining? [S13] Book 4 Part 8 (monitoring, drift, alerting) and Book 6 Part 2 (model degraded in production).
- Write a SQL query for the top 3 transactions per customer per month, then do it in pandas. [illustrative] Book 3 Part 4 (window functions, top-N per group).
- Design a RAG assistant for internal policy documents and say how you would evaluate it. [illustrative] Book 2 Part 6 (RAG basics) and Part 9 (LLM evaluation).
- Review this short function that computes a rolling feature and spot the bug. [illustrative] Book 1 Part 12 (live-coding and AI-code-review rounds).
- Describe a time your team had internal issues and what you did. [S6] Book 6 Part 6 (stakeholder conflicts and trade-offs).

**What they score:**
- Coding at medium level in Python and clear explanation [S4][S9].
- ML fundamentals and how deeply you know your own project [S8][S13].
- Thinking process: a 2018 candidate write-up said the interviewer cared more about reasoning than the correct answer (anecdotal, old) [S14].
- Behavioural fit, teamwork and, for ML roles, ethics, fairness and privacy awareness (anecdotal) [S9][S4].
- Production-minded design at senior levels [S5][S4].

**Level notes:**
- Titles seen in postings: Associate, Senior Associate, Vice President, Executive Director in the US results; Applied AI ML Associate, Associate Senior and Lead in India [S6][S3].
- Hyderabad ML postings ask for formal software engineering training, several years of applied experience, strong Python or Java and Pandas/NumPy [S3].
- Senior levels reportedly add a design discussion [S4]. Level-specific rubric not found.
- Glassdoor VP data: 12 interviews only, stages listed as skills test, one-on-one and phone interview; too small to rely on [S6].

**Preparation plan (2 weeks):**
- Days 1-2: Python coding warm-up, arrays and strings, in a plain editor. Book 5 Parts 1-3 [G].
- Days 3-4: ML fundamentals, metrics, imbalance. Book 1 Parts 1-3.
- Days 5-6: Trees and boosting, plus SQL windows. Book 1 Part 4; Book 3 Parts 4-5.
- Days 7-8: Transformers, RAG and LLM evaluation if applying to Applied AI/ML. Book 2 Parts 1, 6, 9.
- Days 9-10: Production: monitoring, serving, drift. Book 4 Parts 6 and 8; Book 6 Part 2.
- Days 11-12: Code-review practice and a project deep-dive script. Book 1 Part 12.
- Days 13-14: Behavioural stories and a full mock Superday. Book 6 Part 6 [G].

**Common mistakes:**
- Preparing from software engineering Superday guides alone for a data science loop [S4][S1].
- Not being able to go deep on your own project, which is the centre of the ML round [S8].
- Ignoring the behavioural round [S9].
- Treating one candidate's loop or a third-party round count as official [G].

**Recent changes and AI-era notes:**
- A third-party prep site says JPMorgan's HireVue guidance tells candidates not to use software to generate answers unless invited; this was not confirmed against JPMorgan's own page [S15].
- Reporting says the CEO stated the bank would hire more AI people and fewer bankers in some categories; this concerns hiring mix, not interview format [S16].
- Bloomberg (Nov 2025) framed the tension that banks want staff to use AI but not applicants in interviews; the snippet does not describe JPMorgan's specific rule [S17].
- No official announcement of AI interviewers or AI-assisted rounds was found.

**Sources:**
- S1: https://dataford.io/interview-guides/jp-morgan-chase/data-scientist . Supports: guide estimate of about 3-5 weeks and 3 rounds for data scientist (ML, probability and statistics, case studies, pipelines); third-party, possibly AI-generated. Seen 2026-10-31. Snippet only.
- S2: https://themuse.com/jobs/jpmorganchase/vice-president-data-scientist-bangalore-mumbai-db2c12 . Supports: Vice President Data Scientist posting for Bangalore/Mumbai. Seen 2026-10-31. Snippet only.
- S3: https://builtinhyderabad.in/job/applied-ai-ml-associate-ml-engineer/3695876 . Supports: Hyderabad Applied AI ML Associate (ML engineer) posting; the search summary also covers Hyderabad ML postings' requirements and a Glassdoor Hyderabad Mar 2025 review (2 weeks, anecdotal). Seen 2026-10-31. Snippet only.
- S4: https://www.techprep.app/blog/jpmorgan-interview-process . Supports: HackerRank first step, Superday of 3-4 interviews, coding plus code review plus behavioural, senior design; the 2020 AI/ML account came from the same search summary of guides. Seen 2026-10-31. Snippet only.
- S5: https://builtinbengaluru.in/job/applied-ai-ml-lead-ml-engineer-science-lead/3695879 . Supports: Bengaluru Applied AI ML Lead posting; skills (Python, PyTorch/TensorFlow, prompt design, RAG, ML system design) come from the search summary of several Bengaluru postings. Seen 2026-10-31. Snippet only.
- S6: https://www.cleverprep.com/companies/jpmorgan/data-scientist . Supports: Data Scientist guide with stages, bias-variance question and Glassdoor-derived averages (about 37 days, VP 12 interviews); the stage summary came from a search summary of Glassdoor and guide results. Seen 2026-10-31. Snippet only.
- S7: https://www.designgurus.io/answers/detail/what-is-the-jpmorgan-chase-interview-process-like-round-by-round . Supports: HackerRank online assessment of 60-90 minutes then Superday (guide). Seen 2026-10-31. Snippet only.
- S8: https://www.interviewquery.com/interview-guides/jp-morgan-chase-machine-learning-engineer . Supports: ML engineer technical screen with hiring-team member; ML round 45-60 min conversational; candidate Glassdoor rounds (coding, ML deep dive, behavioural, resume fit). Seen 2026-10-31. Snippet only.
- S9: https://static.glassdoor.com.mx/Interview/JPMorganChase-Interview-E5224839-RVW88664785.htm . Supports: JPMorganChase ML-flavoured interview review (anecdotal); round detail is from the search summary and the page-to-detail match is uncertain. Seen 2026-10-31. Snippet only.
- S10: https://www.1point3acres.com/interview/thread/1007544 . Supports: existence of an Applied AI/ML VP full-time ML engineering interview thread; contents login-gated. Seen 2026-10-31. Snippet only.
- S11: https://www.joinleland.com/library/a/jp-morgan-interview . Supports: third-party paraphrase of JPMorgan's How We Hire stages and assessment types (via search summary of several guides). Seen 2026-10-31. Snippet only.
- S12: https://dataford.io/interview-guides/jp-morgan-chase/machine-learning-engineer . Supports: class imbalance in fraud detection as a fundamentals question. Seen 2026-10-31. Snippet only.
- S13: https://tryexponent.com/blog/jp-morgan-chase-interview-process . Supports: project deep-dive question; post-deployment metrics and imbalanced data questions via search summary of guides. Seen 2026-10-31. Snippet only.
- S14: https://www.geeksforgeeks.org/?p=253451 . Supports: 2018 data science interview write-up (thinking process over correct answer; anecdotal, old). Seen 2026-10-31. Snippet only.
- S15: https://prachub.com/resources/jpmorgan-hirevue-interview-questions-2027-video-prompts-coding-explanations-and-timeline . Supports: third-party report of HireVue guidance on not using answer-generating software. Seen 2026-10-31. Snippet only.
- S16: https://finance.yahoo.com/news/ceo-dimon-says-jpmorgan-hire-092441143.html . Supports: statement on hiring more AI people and fewer bankers. Seen 2026-10-31. Snippet only.
- S17: https://www.bloomberg.com/news/articles/2025-11-20/wall-street-wants-everyone-using-ai-except-its-job-applicants . Supports: Nov 2025 framing that banks restrict applicants' AI use. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium confidence in the shape; low in round counts, durations and which rounds apply to data science rather than software engineering [S4][S1].
- India: Bengaluru and Hyderabad postings exist; Mumbai appears only for one VP posting; no India-specific loop description was found [S1][S3].
- Verify on JPMorgan's careers page and with the recruiter: assessment platform and length, number of Superday interviews, whether a design or ML round applies to your title, and the current AI-use rules for candidates [S11][S15].
- No claim here that any question will be asked.

### C4 Goldman Sachs (global bank)

**Evidence level:** Thin to Medium. One official page (an engineering recruiter Q&A on the careers blog) supports the engineering-hiring principles, but no snippet describes a data science or ML loop from Goldman itself; the round shapes come from third-party guides, many written for software engineering, and a handful of anecdotal candidate reports [S1][S2][S5].

**Roles seen in sources:** Data Scientist (Bengaluru listing on an aggregator) [S3]; Applied AI Strat / Quantitative Engineer Associate in the FICC FAST XAsset Strats team in Bengaluru [S6]; PhD-hiring Applied Researcher (language models for financial use cases) in Hyderabad/Bengaluru [S7]; AI Research Vice President in Bengaluru [S6]; Data Engineer Associate and Vice President in Hyderabad [S8]; Software Engineering Associate in Bengaluru (candidate reports) [S9]. Many Applied AI/AI-ML quant research postings are in New York, London and Singapore, not India [S6]. Entity: Goldman Sachs Services (India) is named on aggregator listings; the team (Strats, Engineering, Asset and Wealth Management tech) matters and sources differ by team [S6][S8].

**Process overview (as reported):**
1. Application and recruiter or HR screen; one guide gives a 30-45 minute recruiter phone screen on background, interest in the role and behavioural fit [S2].
2. Online coding assessment. Goldman's own recruiter Q&A says coding platform scores are paired with a structured interview; third-party guides name HackerRank (some CoderPad) with 2-3 problems in 60-90 minutes, and candidate posts in Bengaluru describe a HackerRank DSA test as round 1 (anecdotal) [S1][S4][S9]. Campus flow guides add a recorded HireVue video of about 30 minutes (third-party) [S1][S4].
3. Technical interview(s). For data scientist, one guide describes a roughly one-hour phone or video interview on ML fundamentals, hypothesis testing, probability distributions, SQL and coding [S2][S10]. A Bengaluru data scientist listing describes three steps: resume screening, a technical or aptitude round possibly with a short task or case study, then a hiring manager or HR discussion [S3]. A Hyderabad data engineer listing mentions a technical screen with a short practical exercise or take-home [S8].
4. Superday: two to five back-to-back interviews, 45-60 minutes, covering ML depth, statistics, coding, sometimes a case on applying ML to a financial problem (data science guide); engineering Superdays are reported to mix DSA, resume or project deep dives, system design and Java or SQL, varying by team and level [S2][S4][S10]. A candidate post describes 3 rounds of 45 minutes starting with projects and Java (undated, anecdotal) [S9].
5. Timing varies widely: estimates of about 54 days, 2-4 months and 4-12 weeks in different guides; one Bengaluru senior data analyst report said 2 weeks (anecdotal) [S1][S3].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call, about 30-45 min in one guide | Background, role interest, behavioural fit | [S2] |
| Video interview (campus flow) | Recorded HireVue, about 30 min; 30 seconds prep and 2 minutes answer reported | Communication, motivation | [S1][S11] guide / news |
| Online coding test | HackerRank or CoderPad, 2-3 problems, 60-90 min | DSA coding, sometimes hard level (anecdotal) | [S4][S9] |
| Technical screen (DS) | Phone or video, about 1 hour in one guide | ML fundamentals, hypothesis testing, distributions, SQL, coding | [S2][S10] |
| Superday | 2-5 interviews, 45-60 min | ML depth, statistics, coding, finance case, project deep dive | [S2][S4][S10] |
| Values / behavioural | Interview | Past projects, problem-solving approach, core values | [S10] |

**Question types:**
- Probability and statistics with depth: distributions, a coins probability question, hypothesis testing (candidate and guide reports) [S2][S10].
- ML concepts: pipeline design, hyperparameter tuning, metrics, feature selection, data leakage, missing data; one intern report of being asked to derive logistic regression (anecdotal) [S10].
- SQL and coding for data roles; DSA at hard level reported in Bengaluru (anecdotal, May 2026 Glassdoor) [S2][S9].
- Case questions: clarify business goal, data and success metric before modelling [S10].
- For engineering-track Superdays, Java internals and project questions are recurring (anecdotal) [S4][S9].
- Behavioural tied to firm values and your past projects [S10].

**Sample questions (illustrative):**
- What is the probability of at least one head in two coin tosses, and how does the answer change with a biased coin? [S10] Book 1 Part 14 (probability puzzles, Bayes).
- Derive the gradient of the log-loss for logistic regression and explain regularization. [S10] Book 1 Part 2 (regression, regularization).
- Describe how data leakage can happen in a credit-risk model and how you would prevent it. [illustrative] Book 1 Part 3 (classification metrics, imbalance, calibration) and Book 6 Part 3 (imbalanced, noisy, missing data).
- Write a SQL query for a rolling 30-day average trade volume per client. [illustrative] Book 3 Part 5 (running totals, moving averages).
- Design a model to flag unusual trades for compliance review: data, features, metric, monitoring. [illustrative] Book 1 Part 5 (anomaly detection) and Part 11 (ML system design).
- Solve a hard array problem such as the median of two sorted arrays, and explain the complexity. [S9] Book 5 Part 5 (binary search).
- Walk me through your most complex project and what you would change. [S10] Book 6 Part 10 (end-to-end open scenarios).
- Design an LLM-based summarizer for research notes and say how you would evaluate it. [illustrative] Book 2 Part 9 (LLM evaluation) and Part 12 (GenAI system design).

**What they score:**
- Problem-solving process over the final answer: the official recruiter Q&A says interviewers give a problem and assess how you reason toward it [S1].
- Coding ability rather than a specific language [S1].
- How you reason about ML, not recitation of a toolkit (guide) [S10].
- Depth in your past projects and statistical fundamentals [S10][S2].
- Fit with firm values in a behavioural round [S10].

**Level notes:**
- Titles seen: Analyst, Associate, Vice President (Hyderabad and Bengaluru postings) [S6][S8]; one Fishbowl thread says people with varied years of experience hold the VP title, so title does not map cleanly to experience (anecdotal) [S12].
- Bengaluru Applied AI Strat Associate: Python, data structures and algorithms, plus about two years as a data scientist or equivalent academic ML, deep learning or NLP work [S6].
- AI Research Vice President (Bengaluru): language models and NLP focus; about three years AI/ML industry experience for Bachelor's/Master's holders and about one year for PhD holders in the posting [S6].
- Interview rubric by level was not found.

**Preparation plan (2 weeks):**
- Days 1-2: HackerRank-style DSA practice, timed. Book 5 Parts 1, 2, 5 and 7 [G].
- Days 3-4: Probability and statistics. Book 1 Parts 13 and 14.
- Days 5-6: ML fundamentals, regression, metrics, leakage. Book 1 Parts 1-3.
- Days 7-8: SQL windows and pandas. Book 3 Parts 4-5.
- Days 9-10: Trees, boosting, anomaly detection for finance cases. Book 1 Parts 4 and 5; Book 6 Part 5 (business case studies).
- Days 11-12: GenAI basics for Applied AI roles. Book 2 Parts 6, 9, 12.
- Days 13-14: Project deep-dive and values stories, then a mock Superday. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Assuming a software engineering Superday guide describes a data science loop, or the reverse [S4][S10].
- Reciting methods without clarifying the goal, data and metric in case questions [S10].
- Using ChatGPT or other outside tools in the recorded video interview, which the bank said is prohibited [S11].
- Weak probability fundamentals for a bank with a quantitative culture [S10][G].
- Treating one candidate's loop as the standard [G].

**Recent changes and AI-era notes:**
- June 2025 news: Goldman's campus recruiting team told students not to use ChatGPT, Google or other outside sources during interviews, and its HireVue pre-assessment gives 30 seconds to prepare and 2 minutes to answer (reported by news outlets) [S11].
- Nov 2025 Bloomberg framing: banks encourage staff AI use but restrict applicants in interviews; snippet does not give Goldman's current rules for experienced hires [S13].
- Postings for Applied AI and AI/ML quant research roles show active hiring in AI-specific titles, including language-model work in Bengaluru [S6][S7].
- Older: HackerRank plus Superday as the long-standing engineering path [S1][S4].

**Sources:**
- S1: https://www.goldmansachs.com/careers/blog/posts/engineering-qna-recruiters.html . Supports: official engineering recruiter Q&A: problem-solving focus, no required language, coding platform scores paired with structured interview (from search summary of this and a sister page). Seen 2026-10-31. Snippet only.
- S2: https://interviewquery.com/interview-guides/goldman-sachs-data-scientist . Supports: data scientist guide: 30-45 min recruiter screen, technical interview content, later stage. Seen 2026-10-31. Snippet only.
- S3: https://myinternships.in/internships/goldman-sachs-data-scientist-bengaluru-aed83a . Supports: Bengaluru data scientist listing with 3-step process; Bengaluru senior data analyst 2-week report and process-length estimates from the same search summary. Seen 2026-10-31. Snippet only.
- S4: https://www.techprep.app/blog/goldman-sachs-interview-process . Supports: HackerRank/CoderPad 2-3 problems 60-90 min, Superday of 2-5 interviews covering coding, design, behaviour; varies by team and level (search summary of several guides). Seen 2026-10-31. Snippet only.
- S5: https://hyring.com/jobseeker-toolkit/interview-questions/company/goldman-sachs . Supports: aggregated guide; process-length distribution. Seen 2026-10-31. Snippet only.
- S6: https://higher.gs.com/roles/150921 . Supports: Goldman careers posting, PhD hiring Hyderabad/Bengaluru Associate; Bengaluru Applied AI Strat, AI Research VP and Sales Strats AI details come from a search summary of Bengaluru postings (themuse and aggregator listings); other Applied AI postings are outside India. Seen 2026-10-31. Snippet only.
- S7: https://higher.gs.com/roles/150921 . Supports: applied researcher focus on language models for financial use cases (same page as S6, listed separately for the claim). Seen 2026-10-31. Snippet only.
- S8: https://myinternships.in/job/goldman-sachs-data-engineer-hyderabad-38b10d . Supports: Hyderabad data engineer listing with technical screen and practical exercise; Hyderabad Associate/VP data engineering postings via refresh.cv listings. Seen 2026-10-31. Snippet only.
- S9: https://leetcode.com/discuss/interview-experience/6344866/ . Supports: Bangalore Associate Jan 2025 candidate post, HackerRank first round (anecdotal); Superday project and Java rounds and the median-of-two-sorted-arrays Glassdoor mention come from other results in the same search summary. Seen 2026-10-31. Snippet only.
- S10: https://www.interviewquery.com/interview-guides/goldman-sachs-machine-learning-engineer . Supports: ML interview topics, probability and statistics depth, case guidance, values round; the search summary mixed this with other Goldman guides and intern reports. Seen 2026-10-31. Snippet only.
- S11: https://fortune.com/2025/06/11/goldman-sachs-students-ai-chatgpt-interviews-amazon-anthropic . Supports: June 2025 report on no-ChatGPT guidance and HireVue timing. Seen 2026-10-31. Snippet only.
- S12: https://www.fishbowlapp.com/bowl/goldman-sachs-gmd/7 . Supports: thread on varied experience at VP title (anecdotal). Seen 2026-10-31. Snippet only.
- S13: https://www.bloomberg.com/news/articles/2025-11-20/wall-street-wants-everyone-using-ai-except-its-job-applicants . Supports: Nov 2025 framing of banks restricting applicants' AI use. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium confidence in the shape; low in round counts and durations, which differ widely by source and team [S4][S1].
- India: Bengaluru and Hyderabad postings exist for AI, data and engineering roles; no data science Superday write-up from India was found, so the DS loop here is mostly from global guides [S2][S6].
- Verify on Goldman's careers site and with your recruiter: whether HireVue and HackerRank apply to your hiring route (campus versus experienced), the Superday length, which team's loop you are in, and the current AI-tool rules [S1][S11].
- No claim here that any question will be asked.
