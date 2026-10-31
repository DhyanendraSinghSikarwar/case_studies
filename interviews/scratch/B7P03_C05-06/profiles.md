### C5 American Express (Global payments and card company; India centres in Gurugram, Bengaluru and Chennai)

**Entity note:** Sources refer to the global company (American Express) and, in job posts, to India-centre teams such as Credit and Fraud Risk, Decision Science, Big Data Labs / Risk Information Management, Advanced Analytics (servicing) and the AI engineering teams. Candidate reports on Glassdoor are mostly tagged just "American Express" with a city; they do not name the business unit unless stated. The phrase "Big Data and Decision Science" itself did not appear in any interview report; "Credit Risk and Analytics" appeared only as a search label for credit-risk analyst reports [S2][S11][S12].

**Evidence level:** Thin. There is no official American Express process page in any result; evidence is aggregator guides (Interview Query, Dataford), a small number of Glassdoor reports (Gurgaon and others), and job posts. Round counts differ between sources (2, 3, 4-6) and the Bengaluru ML-engineer evidence is mostly guide text, not candidate reports [S1][S4][S6].

**Roles seen in sources:** Data Scientist and Analyst, Data Science (Gurugram, Bengaluru) [S12][S10], Data Scientist Manager and Senior Manager rounds (candidate reports) [S1][S3], Machine Learning Engineer guide [S4], AI Engineer II / III and Senior AI Engineer I postings with GenAI, agents and RAG in India [S13][S8], and Analyst, Big Data Labs / Risk Information Management [S11].

**Process overview (as reported):**
1. Recruiter or HR phone screen [S1][S6].
2. For analyst / junior data science: an online coding assessment (Python, SQL) is reported in Glassdoor snippets (anecdotal) [S15]; campus drives are reported as an online aptitude test, a technical interview and an HR interview [S9][S10]. Older campus reports exist (2018) and may be out of date [S9].
3. Technical interview(s): SQL, pandas, ML concepts, guesstimates and resume-based project discussion (anecdotal) [S15][S2].
4. Hiring-manager round, and in some reports a director, VP or skip-level round [S6][S5][S15].
5. Round counts vary: one guide says 4-6 rounds for data scientist [S1]; Glassdoor candidates describe 3 rounds over about 2 months or about 3 weeks, and 2 rounds over 4 weeks (Gurgaon) (anecdotal) [S6][S2]. For ML engineer, a guide says the final loop has four to five interviews of about 45-60 minutes [S4]. Treat all as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / HR screen | Phone | Background, fit | [S1][S6] anecdotal |
| Online assessment (junior roles) | Coding test and/or aptitude test | Python, SQL; aptitude on campus | [S15][S9][S10] anecdotal |
| Technical interview | Video, one panelist in some reports | SQL, algorithms, ML basics, past projects, case study | [S2][S15] anecdotal |
| Senior-manager round (senior DS) | Video | Credit-market domain, ensembles, ETL, data exploration | [S1] guide |
| Hiring manager / director / VP | Video | Project depth, domain and business fit | [S6][S5][S15] anecdotal |
| ML engineer final loop | 4-5 interviews, about 45-60 min each | ML tied to business goals, customer experience, compliance | [S4] guide, duration not confirmed |

**Question types:**
- SQL (joins, clauses, basic queries) and pandas manipulation such as intersecting two dataframes [S2][S15][S5].
- Statistics and ML concepts: bagging, random forest, XGBoost, ensembles, hyperparameters, loss functions, overfitting [S1][S15][S2].
- Data handling: outliers, missing data, imbalanced categories [S2][S5].
- Case study on confusion-matrix concepts (precision, recall, accuracy) [S15][S2].
- Business and domain: how the credit market works, factors affecting a credit score, how American Express makes money, how it differs from Visa and Mastercard, guesstimates such as estimating active credit card users in Delhi / India (anecdotal) [S1][S2][S15].
- Resume and project depth: explain a past project and the algorithms you used [S1][S2].
- GenAI (AI Engineer roles): evaluating LLM output quality in production is a sample on a prep site; postings name prompts, agents, copilots, RAG and LangChain-type frameworks [S8][S13].

**Sample questions (illustrative):**
- Explain precision, recall and accuracy for a card-fraud model and choose a threshold when fraud is rare. [S15] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding).
- How would you handle missing values and outliers in a transaction table before modelling? [S2] Book 6 Part 3 (imbalanced / noisy / missing data situations) and Book 1 Part 5 (clustering, PCA/UMAP, anomaly detection).
- Compare bagging with random forest and with gradient boosting; when would you pick XGBoost? [S1] Book 1 Part 4 (trees, RF, boosting, SHAP).
- Write SQL to find customers whose monthly spend rose for three straight months. [illustrative] Book 3 Part 4 (window functions: ranking, top-N per group) and Book 3 Part 5 (LAG/LEAD).
- Estimate the number of active credit cards in a large Indian city and state your assumptions. [S2] Book 6 Part 5 (business case studies: pricing, churn, fraud, supply chain).
- Walk through the data science project on your resume, including what you would change. [S1] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).
- How would you evaluate the quality of an LLM assistant's answers in production? [S8] Book 2 Part 9 (LLM evaluation: RAGAS, LLM-as-judge, hallucination, benchmarks).
- Design a real-time card-fraud scoring system. [illustrative] Book 1 Part 11 (ML system design) and Book 6 Part 9 (domain sets: fintech).

**What they score:**
- Project depth and the ability to explain past work clearly: guides and candidates describe an experience-driven process [S1][S3].
- Domain knowledge of credit and card business, especially for manager-level interviews [S1][S2].
- SQL, Python and core ML fundamentals [S15][S2].
- Behavioural and motivation questions such as "why Amex" appear in guide summaries [S5][S14].
- A formal rubric: not found in sources.

**Level notes:**
- Job titles seen in India: Analyst, Data Science; Data Scientist; Manager, Data Science; Director, Data Science; AI Engineer II / III; Senior AI Engineer I; Senior Engineer II [S12][S13].
- Junior posts list 0 to 30 months of relevant analytics or big-data experience for Analyst, Data Science; one AI Engineer III post asks for 3-5+ years [S12][S4]. Expectations per level in interviews: not found in sources.

**Preparation plan (2 weeks):**
- Days 1-2: SQL joins, CTEs, windows. Book 3 Parts 2-5.
- Days 3-4: pandas and sklearn live coding. Book 1 Part 12 (NumPy/pandas/sklearn live-coding) and Book 1 Part 2 (regression, regularization, feature engineering).
- Days 5-6: classification metrics, imbalance, tree models. Book 1 Parts 3-4.
- Days 7-8: statistics refresh and anomaly detection. Book 1 Parts 1, 5 and 13.
- Days 9-10: credit and fraud case practice with guesstimates. Book 6 Parts 3, 5 and 9 [G].
- Days 11-12: for AI Engineer roles, RAG, agents and evaluation. Book 2 Parts 6, 8 and 9.
- Days 13-14: tell-your-project stories, two mocks, read the role's own job description for the team. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Not being able to explain your own project in depth, when the process is described as project-driven [S1][S3].
- Ignoring the card and credit business, then freezing on domain questions [S1][S2].
- Treating a single Glassdoor round order as the standard process [G].
- Quoting accuracy only for an imbalanced fraud problem [S15] (case study is on precision/recall).

**Recent changes and AI-era notes:**
- Recent job posts (2025-2026 listing dates on aggregators) show GenAI and agentic AI engineering roles in Gurugram, Bengaluru and Chennai, naming RAG pipelines, copilots and Google Cloud Platform [S13]. This is hiring demand, not an interview-format change.
- No source on AI-tool policy in interviews, remote versus onsite shift, or any change in the American Express process: not found.
- HireVue-style one-way video screens are described for student programs by a guide; scope for experienced data roles is unknown [S16].
- Older: campus aptitude plus technical plus HR rounds, 2018 reports [S9].

**Sources:**
- S1: https://www.interviewquery.com/guides/american-express-data-scientist . Supports: 4-6 round DS description, senior-manager round on credit market, ensembles, ETL; project-depth emphasis. Seen 2026-10-31. Snippet only.
- S2: https://www.glassdoor.co.in/Interview/American-Express-Interview-E35-RVW102573068.htm . Supports: Gurgaon Glassdoor reports (Nov 2023 candidate: SQL, algorithms, outliers, missing data, credit-score factors, CV-based second round and case; 1-4 week timelines; Delhi card-user estimate; Amex vs Visa and Mastercard). The page-to-detail match is from a search summary covering several Gurgaon reports (RVW102573068, RVW103116987, RVW82764632 and others), approximate. Anecdotal. Seen 2026-10-31. Snippet only.
- S3: https://dataford.io/interview-guides/american-express/data-scientist/experiences . Supports: data scientist experiences listing (aggregator; Data Scientist Manager XGBoost and credit card business question). Seen 2026-10-31. Snippet only.
- S4: https://www.interviewquery.com/interview-guides/american-express-machine-learning-engineer . Supports: ML engineer final loop of four to five interviews of about 45-60 minutes, ML tied to business goals. Seen 2026-10-31. Snippet only.
- S5: https://www.interviewquery.com/guides/american-express-data-analyst . Supports: 2-4 rounds (HR, technical, manager, panel/director), SQL and behavioural emphasis (data analyst role, may not apply to DS). Seen 2026-10-31. Snippet only.
- S6: https://www.glassdoor.sg/Interview/American-Express-Interview-E35-RVW100554102.htm . Supports: three-round report (HR phone, team member video, hiring manager video, about 2 months; another about 3 weeks), anecdotal; the match of the detail to this page is from a search summary. Seen 2026-10-31. Snippet only.
- S7: https://builtin.com/articles/AMEX-data-scientist-interview . Supports: existence of an AMEX data scientist interview article (only title seen; no detail used). Seen 2026-10-31. Snippet only.
- S8: https://dataford.io/interview-guides/american-express/genai-engineer . Supports: GenAI Engineer prep guide with LLM-evaluation sample question (third party). Seen 2026-10-31. Snippet only.
- S9: https://www.geeksforgeeks.org/?p=221902 . Supports: on-campus internship and full-time offer write-up (older, campus; anecdotal). Seen 2026-10-31. Snippet only.
- S10: https://freshershunt.in/american-express-hiring-freshers-analyst-data-science-bengaluru/ . Supports: Analyst, Data Science, Bengaluru fresher posting (aggregator; aptitude, technical, HR structure from an employer listing summary). Seen 2026-10-31. Snippet only.
- S11: https://hackerearth.com/jobs/american-express/analyst-assistant-manager-big-data-labs-risk-information-management . Supports: existence of Analyst / Assistant Manager, Big Data Labs, Risk Information Management role. Seen 2026-10-31. Snippet only.
- S12: https://career.io/job/analyst-data-science-gurugram-american-express-1673251b1e3a0fb2950a5ebec65c482d . Supports: Analyst, Data Science, Gurugram posting (model validation, NLP); related Bengaluru/Gurugram posts say 0-30 months experience and mention Credit and Fraud Risk and Decision Science teams (from search summary). Seen 2026-10-31. Snippet only.
- S13: https://www.wearedevelopers.com/en/jobs/ext/6343797/sr-ai-engineer-i . Supports: Senior AI Engineer I, agentic AI on Google Cloud (India); a Gurugram AI Engineer II role on GenAI, agents, copilots, RAG is from the search summary of talentmate and similar boards. Seen 2026-10-31. Snippet only.
- S14: https://in.indeed.com/cmp/American-Express/faq/interviews . Supports: general interview-stage description (up to four stages) and anecdotal tips. Seen 2026-10-31. Snippet only.
- S15: https://www.glassdoor.co.in/Interview/American-Express-Interview-E35-RVW75736891.htm . Supports: Analyst Data Science candidate report (coding assessment, python/sql/pandas, guesstimates, ML/DL; 2025 case study on confusion matrix, director round); detail match from summary of several Glassdoor results. Anecdotal. Seen 2026-10-31. Snippet only.
- S16: https://blog.theinterviewguys.com/?p=19007 . Supports: HireVue one-way video screen guidance (third-party blog, student programs). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium confidence in the broad shape (screen, technical, manager, senior round); low confidence in round counts, durations and the order [S1][S6][S2].
- India: Gurgaon reports exist but are small and mixed by role; Bengaluru ML-engineer reports were not found; Chennai interview reports were not found [S2][S4].
- Verify on American Express careers (amexjobs): the team (Credit and Fraud Risk, Decision Science, Big Data Labs, AI engineering), title and level, and whether an online assessment applies.
- Several results were low-quality mirror sites and were not used. No claim here that any question will be asked.
### C6 Visa (Global payments network; India centres in Bengaluru and others)

**Entity note:** Visa Inc. is the global payments network. Official interview guidance on the careers site is global, not India-specific [S1]. India-specific evidence is a handful of Bengaluru reports, almost all for data engineer roles on Jointaro, plus Bangalore data scientist and staff machine-learning-scientist job posts [S9][S10]. Many data scientist and machine learning engineer reports in guides are from other offices (US, Singapore, Warsaw, Naples) and are not Bengaluru evidence [S3][S5][S11].

**Evidence level:** Medium for the general shape (an official page on rounds and AI-tool rules, plus consistent guides on assessment, technical and case-study content); Thin for India data science and ML specifically, where no Bengaluru data scientist report body was visible and the Blind thread appeared with its title only [S1][S2][S8].

**Roles seen in sources:** Data Scientist and Senior / Staff Data Scientist (Bengaluru post) [S9], Staff Machine Learning Scientist (Bangalore post, applied AI research) [S10], Senior Consultant AI and Data Engineer with GenAI and MLOps (post) [S10], Machine Learning Engineer and Senior ML Engineer in the Cloud AI Platform (single Blind account) [S6][S7], Machine Learning Scientist, Generative AI (an online-assessment thread) [S12], and Data Engineer in Bengaluru (anecdotal reports) [S8].

**Process overview (as reported):**
1. Recruiter scheduling and screen: scheduling runs through the recruiter and the applicant tracking system [S1]; candidates describe a call on logistics and expectations [S3].
2. Online assessment: HackerRank with one SQL and one Python question in one report [S3]; a CodeSignal general coding assessment of four questions, roughly 70 minutes, is reported by guides and Glassdoor entries (candidate-reported, location mixed) [S4][S13]; a Visa ML online assessment thread mentions ensemble learning, coding and ML concepts in about 70 minutes (anecdotal) [S12].
3. Technical interviews: for data science, SQL, Python, machine learning and statistics, typically two technical rounds in one guide [S3]; for ML engineer, ML system design is rated very high likelihood by a guide [S5].
4. Case study or business case: a 45-minute business-case round on hypothetical data is described in a Glassdoor report (location not shown); ML roles may include an ML case study [S14][S4].
5. Final or "super day": some candidates report four interviews mixing technical and behavioural content [S3]. Visa's own page says most candidates go through two to four interview rounds depending on role and level [S1].
6. Total duration: one guide says 3-5 weeks for data scientist [S3]; another says 4-6 weeks for technical candidates [S4]; Glassdoor timelines range from about two weeks to several months (anecdotal) [S3][S4]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call | Logistics, role fit | [S1][S3] |
| Online assessment | HackerRank (SQL and Python) or CodeSignal (4 questions, about 70 min) | Coding, DSA; for ML scientist, ensemble learning and ML concepts | [S3][S4][S12] anecdotal and guides |
| Technical round(s), DS | Video, typically two | SQL, Python, ML, statistics, modelling, model metrics | [S3][S2] |
| Technical round(s), MLE | Video | DSA, ML knowledge, ML system design (fraud, risk), cloud / OOP for platform roles | [S5][S6][S7] anecdotal |
| Business / ML case study | About 45 min in one report | End-to-end problem such as transaction anomalies; fraud, risk, personalisation | [S14][S4] anecdotal |
| Hiring manager / behavioural | Video or panel | Past experience, fit, "why Visa", stakeholder collaboration | [S4][S2] |

**Question types:**
- SQL joins and subqueries; Python coding [S14][S3].
- ML fundamentals: bagging vs boosting, evaluation metrics for a random forest, gradient descent, loss functions, LSTMs [S14][S2][S7].
- Statistics, A/B testing, probability and product metrics are listed as common topic areas in a guide [S2].
- Fraud and risk framing: real-time fraud detection, risk assessment, credit-based purchase model (candidate-submitted prompts on Prepfully), anomaly scores with a threshold [S7][S14].
- Nested-string decoding and a URL-shortener style design were reported on Prepfully for ML engineer (anecdotal) [S7].
- Behavioural and communication: past experience, stakeholder collaboration, presenting insights, "why Visa" [S4][S2].
- Bengaluru data engineer reports (not DS): Python, SQL, PySpark, Spark cluster sizing, a question about querying a very large table (anecdotal) [S8][S11].

**Sample questions (illustrative):**
- Compare bagging and boosting and say which you would use for a card-fraud model. [S14] Book 1 Part 4 (trees, RF, boosting, SHAP).
- Which metrics would you use to evaluate a random forest on rare-event fraud data? [S2] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding).
- Design a real-time fraud detection system for a card network: features, latency, feedback loop. [S7] Book 1 Part 11 (ML system design) and Book 4 Part 6 (serving: batch vs real-time).
- Given an anomaly score per transaction, how do you choose the threshold that flags fraud? [S14] Book 1 Part 5 (clustering, PCA/UMAP, anomaly detection) and Book 1 Part 3.
- Write SQL joining transactions to merchants and using a subquery to find merchants above the average volume. [S14] Book 3 Part 2 (joins) and Book 3 Part 3 (subqueries, CTEs).
- Decode a string like "2[a3[b]c]". [S7] Book 5 Part 4 (stack, queue, monotonic stack).
- Design an experiment to test a new personalisation feature and present the result to a non-technical stakeholder. [illustrative] Book 1 Part 10 (A/B testing, causal inference) and Book 6 Part 4 (experiment design).
- A fraud model's precision drops after a merchant-mix change; how do you investigate? [illustrative] Book 6 Part 2 (model performance degraded in production) and Book 4 Part 8 (monitoring: drift).

**What they score:**
- Technical fundamentals in SQL, Python, ML and statistics [S3][S2].
- Business framing: case rounds on fraud, risk and personalisation reward end-to-end problem solving [S14][S4].
- Communication, stakeholder collaboration, business acumen and experiment design in onsite panels (Glassdoor summary, anecdotal) [S2].
- Visa's own page describes a structured approach; formal rubric details were not found [S1].

**Level notes:**
- Titles seen: Data Scientist, Senior Data Scientist, Staff Data Scientist, Staff Machine Learning Scientist (8+ years in the post), Senior ML Engineer, Staff Data Engineer [S9][S10][S7].
- System design is described by a guide as usually reserved for more senior candidates [S4]. Other level-specific expectations: not found in sources.

**Preparation plan (2 weeks):**
- Days 1-2: SQL joins, subqueries, windows. Book 3 Parts 2-4.
- Days 3-4: Python and DSA warm-up for the timed assessment. Book 5 Parts 1, 2 and 4, and Book 1 Part 12.
- Days 5-6: Trees, boosting, metrics, imbalance. Book 1 Parts 3-4.
- Days 7-8: Anomaly detection and fraud framing. Book 1 Part 5 and Book 6 Part 9 (domain sets: fintech).
- Days 9-10: Statistics and A/B testing. Book 1 Parts 10 and 13.
- Days 11-12: ML system design and serving for ML roles. Book 1 Part 11, Book 4 Parts 6 and 8, Book 2 Part 12 for GenAI roles.
- Days 13-14: case study practice, behavioural stories, two mocks. Book 6 Parts 5, 6 and 10 [G]. Practise without any AI assistant, since the official page prohibits it [S1].

**Common mistakes:**
- Using an AI assistant, third-party tool or self-recording during any interview stage, which the official page prohibits [S1].
- Assuming Bengaluru data science loops equal the data engineer reports or the US/Singapore reports [S8][S11].
- Preparing only ML theory and skipping SQL and the timed coding assessment [S3][S4].
- Answering fraud questions with accuracy alone, without thresholds, latency or feedback loops [S7][S14].
- Treating a Glassdoor round order from another office as the standard [G].

**Recent changes and AI-era notes:**
- Visa's careers page states that interviewers may use Microsoft Copilot transcription for notes only, candidates may not use third-party tools or start their own audio, video or transcription recording, and using AI during interviews, including to provide answers, is strictly prohibited [S1]. Whether AI is allowed in the online coding assessment is not stated on the page [S1][S13].
- 2025-2026: Visa posts for GenAI, MLOps and applied AI research roles in Bangalore indicate hiring demand [S10]. No source reported a change in round structure.
- Older: Glassdoor reports from 2017-2022 and a 2022 staff data engineer report (online assessment, three technical rounds, hiring manager) may not reflect today [S8][S4].

**Sources:**
- S1: https://careers.smartrecruiters.com/Visa/interviewing . Supports: official Visa careers guidance (two to four rounds, recruiter scheduling, no third-party tools or recording, AI use during interviews prohibited, Copilot transcription for notes only). Seen 2026-10-31. Snippet only.
- S2: https://interviewquery.com/interview-guides/visa-data-scientist . Supports: four-round DS structure, topics (A/B testing, probability, product metrics, Python, SQL); the 2025 Glassdoor summary (recruiter screen, coding, ML, statistics, onsite panel; random forest metrics question) comes from the search summary. Seen 2026-10-31. Snippet only.
- S3: https://www.interviewquery.com/guides/visa-data-scientist . Supports: rounds (online assessment, recruiter, technical, behavioural/management), 3-5 weeks, super day, HackerRank SQL and Python report (via search summary of guide and Glassdoor entries, approximate). Seen 2026-10-31. Snippet only.
- S4: https://tryexponent.com/blog/visa-interview-process . Supports: 4-6 weeks, CodeSignal 70-minute four-question coding screen, system design for senior candidates, ML case study (third-party guide). Seen 2026-10-31. Snippet only.
- S5: https://interviewquery.com/interview-guides/visa-machine-learning-engineer . Supports: ML engineer topics, ML system design rated very high likelihood (third-party; the final-loop and ML case-study text is from a later search summary). Seen 2026-10-31. Snippet only.
- S6: https://www.teamblind.com/post/senior-machine-learning-engineer-visa-vjstgdgy . Supports: single secondhand Senior ML Engineer (Cloud AI Platform) account: resume review and DSA round, then OOP, system design, cloud (anecdotal). Seen 2026-10-31. Snippet only.
- S7: https://prepfully.com/interview-questions/visa/machine-learning-engineer?page=3 . Supports: candidate-submitted ML engineer prompts (credit-based purchase model, risk assessment, real-time fraud detection; the nested-string and URL-shortener prompts appear on pages 2 and 6; ML knowledge on pages 4 and 9). Anecdotal. Seen 2026-10-31. Snippet only.
- S8: https://www.teamblind.com/post/data-scientist-interview-experience-at-visa-inc-bangalore-ilkhaajc . Supports: existence of a Blind thread on a Bangalore data scientist interview; title only, no detail. Seen 2026-10-31. Snippet only.
- S9: https://www.themuse.com/jobs/visa/sr-data-scientist-cab54c . Supports: Senior / Staff Data Scientist posting (Bengaluru DS team); a Bangalore data scientist posting listing Python, SQL, PySpark, Hadoop, Hive, Tableau is from the search summary. Seen 2026-10-31. Snippet only.
- S10: https://www.themuse.com/jobs/visa/staff-machine-learning-scientist-8-years-exp . Supports: Staff Machine Learning Scientist (8+ years, applied AI) Bangalore posting; Senior Consultant AI and Data Engineer GenAI / MLOps posting at a sibling URL. Seen 2026-10-31. Snippet only.
- S11: https://www.jointaro.com/interviews/companies/visa/experiences/data-engineer-bengaluru-july-4-2025-accepted-offer-positive-0aedae19/ . Supports: Bengaluru data engineer report (Python, SQL, PySpark; anecdotal; data engineering, not data science); Warsaw and Naples Glassdoor mentions in other results are location context. Seen 2026-10-31. Snippet only.
- S12: https://www.1point3acres.com/interview/thread/1107911 . Supports: Visa ML online assessment thread (ensemble learning, coding, about 70 minutes; anecdotal); a Machine Learning Scientist Generative AI assessment thread exists at /thread/1083765. Seen 2026-10-31. Snippet only.
- S13: https://www.datainterview.com/blog/visa-software-engineer-interview . Supports: CodeSignal general coding assessment (4 questions, two attempts in one Singapore report) and AI-tool prohibition repeated by a third party; software engineer focus. Seen 2026-10-31. Snippet only.
- S14: https://www.glassdoor.com/Interview/Visa-Inc-Interview-RVW89276680.htm . Supports: Glassdoor Visa reports on case studies (fraud, risk, personalisation), 45-minute business case round, SQL joins and subqueries, bagging and boosting; page-to-detail match from a summary of several Glassdoor results (location not always shown). Anecdotal. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium confidence in the official outline (two to four rounds, AI prohibited); low confidence in exact rounds, durations and the case-study round for India data science [S1][S14].
- India: no Bengaluru data scientist or ML engineer report body found; Bengaluru data engineer reports only [S8][S11].
- Verify on Visa's careers page and with the recruiter: rounds and formats for your role and level, whether CodeSignal or HackerRank applies, and the current AI-tool rules for each stage [S1][S13].
- No claim here that any question will be asked.
