### C9 Atlassian (Software company; India centre in Bengaluru)

**Entity note:** Atlassian is the global software company (Jira, Confluence, Rovo). Its India presence is the Bengaluru centre; sources that name Bengaluru are marked as such, and the rest describe the company-wide process [S3][S6].

**Evidence level:** Thin. Atlassian's own engineering interview handbook and a 2021 values-interviewing document appeared in results, so the general shape (recruiter, manager, skills, values, hiring committee) is supported [S1][S2][S4]. Data science and ML loops come only from third-party guides and a few anecdotal reports with conflicting round counts, and nothing was found on Applied Scientist or GenAI loops [S5][S7][S8].

**Roles seen in sources:** Data Scientist (including Associate and Principal, Bengaluru reports and postings) [S5][S6]; Machine Learning Engineer, including Principal and Senior MLE onsites on 1point3acres [S9][S10]; Senior Principal and Senior ML Engineer postings tied to Rovo quality and evaluation [S11]. No Applied Scientist loop found.

**Process overview (as reported):**
1. Recruiter screen [S2][S4].
2. Hiring manager conversation, reported early, before the technical rounds, though one list places it after the SQL screen [S2][S5].
3. Technical assessment. Data science: a HackerRank-style test on SQL, statistics and Python/pandas, then SQL-heavy live rounds (guide description) [S5]. ML engineer: a Karat-run technical screen is reported by one guide for most engineering roles but not all [S1][S7].
4. Skills loop. Data science: a case or experimentation round and a craft or system-design style round (guide description) [S5][S6]. ML engineer: reports of ML design, an ML deep dive or project presentation, and coding on data structures and ML-related implementation (anecdotal and guide-based) [S7][S9][S10].
5. Values interview, usually about 45 minutes of behavioural questions tied to five values, often run by an employee outside the hiring team [S2][S4][S12].
6. Hiring committee reviews written feedback and CV information, separate from the interviewers [S1].
7. Duration: guides say about 3-6 weeks end to end; one Bengaluru data scientist report says 3 months (anecdotal) [S2][S3].
Round counts differ: 3-5 in one guide, 7 in another, 3 to 7 across sources [S5][S7].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call | Background, role fit | [S2][S4] |
| Hiring manager interview | Conversation | Ambiguity handling, stakeholders, values alignment | [S2][S5] |
| Online assessment (DS) | HackerRank-style test | SQL, statistics, Python/pandas | [S5] |
| Technical screen (MLE) | Karat-run, some roles | Coding | [S1][S7] |
| SQL / coding live round (DS) | Live | SQL-based coding | [S3][S5] anecdotal |
| Case or experimentation (DS) | Interview | Experimentation case, product reasoning | [S3][S5] |
| ML design (MLE) | Onsite | ML system for an Atlassian-style product (search ranking, recommendations) | [S7] guide |
| Coding (MLE) | Onsite | Data structures, ML-related implementation | [S7][S10] anecdotal |
| Values interview | Behavioural, about 45 min | Teamwork, customer orientation, five values | [S2][S4][S12] |
| Hiring committee | Offline review | Written packet | [S1] |

**Question types:**
- SQL (joins, windows) and Python/pandas data handling [S5].
- Experimentation case: how to solve an experiment-design case (Bengaluru report, anecdotal) [S3].
- Statistics and A/B testing with pitfalls (guide advice) [S6][S5].
- ML design for a product feature, ML fundamentals, modeling and coding (guides) [S7][S8].
- Data structures such as hashing and HashMap internals (one Bengaluru report, role unspecified, anecdotal) [S3].
- Behavioural STAR stories mapped to the values [S2][S12].
- LLM evaluation, RAG design, A/B tests and LLM-as-a-judge appear in Rovo job postings as expected experience; no source confirms they are interview questions [S11].

**Sample questions (illustrative):**
- Write SQL for week-over-week retention of teams that adopted a new Jira feature. [illustrative] Book 3 Part 6 (date/time: retention, cohorts, MoM/YoY).
- An experiment on a search-ranking change shows a lift in clicks but a drop in task completion; decide what to do. [S3] Book 1 Part 10 (A/B testing, causal inference, experimentation) and Book 6 Part 4 (experiment design and ambiguous A/B results).
- Design an ML system to recommend related pages in a documentation product. [illustrative] Book 1 Part 7 (recommenders, ranking, search) and Book 1 Part 11 (ML system design).
- Explain how a HashMap works internally and when collisions hurt. [S3] Book 5 Part 1 (arrays and hashing).
- Design an offline and online evaluation plan for an LLM assistant answering questions over company documents. [illustrative] Book 2 Part 9 (LLM evaluation) and Book 2 Part 6 (RAG basics).
- Tell me about a time you changed your mind after customer feedback. [illustrative] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).
- How would you decide an ML model is good enough to launch given a guardrail metric? [illustrative] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding).

**What they score:**
- Role-specific skills: analytical depth and product reasoning for data science [S5].
- Values-driven collaboration; the values interview is a distinct, weighty stage and independent of the skills interviewers [S2][S4][S5].
- A separate hiring committee decides from written feedback, so each interviewer's notes matter [S1].
- Candidates are interviewed before being matched to a team in the centralized model, per one guide [S2].

**Level notes:**
- Levels reported by title in postings: Machine Learning Engineer I and II, Senior, Principal, Senior Principal; Associate and Principal Data Scientist [S6][S11].
- Principal-level loops reported to add ML craft, system design and a project presentation (anecdotal) [S9][S10].
- One Principal Data Scientist Bengaluru posting asks for a stated minimum of years of experience; treat as one posting [S6].
- Level-by-level interview expectations were not found.

**Preparation plan (2 weeks):**
- Days 1-2: SQL with windows and cohorts. Book 3 Parts 4-6 and 8.
- Days 3-4: Experimentation and statistics. Book 1 Parts 10, 13, 14; Book 6 Part 4.
- Days 5-6: ML fundamentals and metrics. Book 1 Parts 1-3.
- Days 7-8: Data-structure coding in a plain editor. Book 5 Parts 1, 2, 7 and Book 1 Part 12 [G].
- Days 9-10: ML system design and recommenders or search. Book 1 Parts 7 and 11.
- Days 11-12: LLM evaluation and RAG if the role is GenAI-adjacent. Book 2 Parts 6, 9, 12 [G].
- Days 13-14: Values stories (two STAR stories per value is one guide's advice) and mocks. Book 6 Part 6; Book 9 when available [S2].

**Common mistakes:**
- Treating the values interview as soft and preparing no stories [S2][S5].
- Preparing only ML theory for a loop that opens with SQL and coding screens [S5].
- Assuming one candidate's round order is standard; sources conflict [S5][S7].
- Assuming an AI-tool policy without asking the recruiter [S13].

**Recent changes and AI-era notes:**
- No official Atlassian policy on AI use in interviews was found; a third-party guide says it is unpublished and to ask the recruiter [S13].
- One Glassdoor review (Sydney, May 2026, a software engineering internship, anecdotal) describes an AI-assisted coding interview where the interviewer observed the candidate working with an agent; it is not evidence for India or data roles [S13].
- Older: the 2021 values-interviewing document and the engineering handbook describe the stable structure [S1][S4].

**Sources:**
- S1: https://www.atlassian.com/company/careers/resources/interviewing/engineering . Supports: official engineering interview handbook: coding in two parts (data structures, code design), systems design, values interview, independent hiring committee seeing feedback and CV information. Seen 2026-10-31. Snippet only.
- S2: https://www.interviewquery.com/interview-guides/atlassian . Supports: five stages (recruiter, manager, skills, values, committee), 3-6 week range, 45-minute values interview, centralized team matching, two STAR stories per value. Seen 2026-10-31. Snippet only.
- S3: https://www.glassdoor.co.nz/Interview/Atlassian-Interview-E115699-RVW89804346.htm . Supports: Bengaluru anecdotal reports (Aug 2024 hashing and HashMap topics; Oct 2025 Data Scientist, 3-month process, experimentation case, offer accepted). Search summary pooled several Glassdoor results, so attribution to this single URL is approximate. Seen 2026-10-31. Snippet only.
- S4: https://atlassianblog.wpengine.com/wp-content/uploads/2021/11/values-interviewing-atlassian.pdf . Supports: Atlassian 2021 material: values interviewers are employees recognised as values champions, not necessarily on the hiring team. Seen 2026-10-31. Snippet only.
- S5: https://www.interviewquery.com/guides/atlassian-data-scientist . Supports: DS loop of 3-5 rounds, HackerRank (SQL, stats, pandas), SQL-heavy rounds, case or craft round, values conversation; analytical depth, product reasoning, values-driven collaboration. Seen 2026-10-31. Snippet only.
- S6: https://www.cleverprep.com/companies/atlassian/data-scientist . Supports: 7-round description, A/B testing advice, values interview as critical; Bengaluru Principal Data Scientist posting context at careers-apac-atlassian.icims.com/jobs/26576/principal-data-scientist/job. Seen 2026-10-31. Snippet only.
- S7: https://www.interviewquery.com/interview-guides/atlassian-machine-learning-engineer . Supports: MLE loop (recruiter, online assessment, ML fundamentals, modeling, coding, ML system design, manager). A CleverPrep MLE page (cleverprep.com/companies/atlassian/machine-learning-engineer) was also in results for the 7-round, Karat and onsite ML design description. Seen 2026-10-31. Snippet only.
- S8: https://www.teamblind.com/post/atlassian-data-scientist-interview-xffk8uym . Supports: Blind DS interview post (anecdotal; STAR values round; one Blind post noted as 2022). Seen 2026-10-31. Snippet only.
- S9: https://www.1point3acres.com/interview/thread/1160189 . Supports: recent MLE onsite thread (coding, ML system design, values behavioural; others list six rounds or four rounds); title and summary only. Seen 2026-10-31. Snippet only.
- S10: https://www.1point3acres.com/interview/thread/1128343 . Supports: Principal MLE video interview, five rounds (HR, ML craft, system design, coding on data structures); anecdotal. Seen 2026-10-31. Snippet only.
- S11: https://www.atlassian.com/company/careers/details/27453 . Supports: Senior ML Engineer posting (Rovo Agents quality, agent evaluation, LLM-as-a-judge); Senior Principal MLE posting at jobs.accel.com/companies/atlassian/jobs/65254842-senior-principal-machine-learning-engineer (Rovo Chat, online evals, RAG). Postings, not interview content. Seen 2026-10-31. Snippet only.
- S12: https://www.levels.fyi/blog/interviewing-at-atlassian.html . Supports: general Atlassian interviewing overview, values interview as a distinct stage (title seen; detail from summary). Seen 2026-10-31. Snippet only.
- S13: https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/?format=md . Supports: AI-policy tracker context; no published Atlassian rule, ask the recruiter. Sydney May 2026 AI-assisted interview anecdote from the Glassdoor Software Engineer Internship page (static.glassdoor.ca/Interview/Atlassian-Software-Engineer-Internship-Interview-Questions-EI_IE115699.0,9_KO10,38.htm). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Confidence: medium for the five-stage shape (official handbook plus guides); low for DS and MLE round contents and order; none for Applied Scientist and GenAI loops [S1][S5][S7].
- Verify on Atlassian's careers interviewing pages and with your recruiter: the exact rounds for your role, whether a Karat or HackerRank screen applies, what the AI-tool policy is, and the Bengaluru team's loop.
- Evidence is mostly aggregator sites and anecdotes; one report is not the process [G].

### C10 Optum (UnitedHealth Group's health services and technology business)

**Entity note:** Optum is a business of UnitedHealth Group (UHG). In India, hiring is done by Optum Global Solutions (India) Private Limited, with offices reported in Bengaluru, Chennai, Gurugram, Hyderabad and Noida; postings use UHG's careers site [S1][S2]. Some prep guides (Dataford "Optum Tech", "Optum Financial") describe other Optum units and are not India-specific [S3]. A Dublin report is from Ireland, not India [S4]. Each source below is marked by entity or location where it says.

**Evidence level:** Thin. UHG's own careers blog gives a six-step generic process [S5]; data science round detail is anonymous Glassdoor reports (a few from India, some for other roles or locations) and generic aggregator guides, with conflicting round counts [S3][S4][S6][S7]. No Applied Scientist loop was found, and nothing from AmbitionBox, Reddit or Blind surfaced.

**Roles seen in sources:** Data Scientist, Associate Data Scientist, Senior Data Scientist, Principal Data Scientist (India postings) [S2][S8]; AI/ML Engineer, Senior AI/ML Engineer and Manager AI/ML Engineer with Gen AI, NLP and Python focus (India postings) [S2][S8]; Applied Scientist appears only as a Dataford guide title [S9].

**Process overview (as reported):**
1. UHG's general process: application, application review, assessment, interview, decision, onboarding. Assessments are not used for every role and the interview process varies by role [S5].
2. Third-party description of common rounds: recruiter phone screen, a pre-recorded digital video interview, then a live virtual or in-person round; technical roles add a technical or domain round [S10]. One aggregator says UHG states recorded interviews are reviewed by a team member, not AI (secondhand) [S11].
3. Data scientist, India (anecdotal): one report of two interviews, a technical one of about 50 minutes and a techno-managerial one of about 25 minutes, then HR; another describes a recruiter round plus two technical meetings [S6].
4. Hyderabad Data Scientist (2020, anecdotal): one day long, with an in-depth question on ML algorithms [S12].
5. AI/ML roles, Bengaluru (anecdotal): a Nov 2025 report of a Python/pandas coding round then a system design round on an agentic application; a Jan 2025 report of two technical rounds (case studies, ML, deep learning, Python and SQL coding) then a hiring manager round [S13].
6. Duration reports vary: about 3 weeks in one data science report; guide estimates of 4-6 weeks are generic and unverified [S4][S3].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen / HR | Call | Fit, background | [S5][S10] |
| Online or AI-based screening (some roles) | Assessment | Skills (one 2026 Hyderabad software developer report, other role) | [S14] anecdotal |
| Technical round 1 (DS) | Live, about 50 min in one report | Python, statistics, ML, projects | [S6][S7] anecdotal |
| Technical round 2 / system design (AI/ML) | Live | ML, deep learning, SQL, agentic application design | [S13] anecdotal |
| Techno-managerial / hiring manager | Live, about 25 min in one report | Project depth, fit | [S6][S13] anecdotal |
| HR | Call | Why Optum, why healthcare, strengths | [S7] anecdotal |

**Question types:**
- Python coding, including data preprocessing, missing data, label encoding (internship reports) [S4].
- Probability basics, logistic regression, ReLU, basic numpy and pandas (anecdotal) [S7].
- Resume and project deep dives, with some math [S7].
- Gen AI and LLM questions, for example Gemini versus GPT after discussing LLM experience; LLM architecture and projects in recent reports [S4][S7].
- Model selection (simple model versus neural network) and evaluation metrics for healthcare outcomes (prep guide, not confirmed in interviews) [S15].
- SQL window functions, Spark and recursive CTE (data engineering reports, other role) [S14].
- HR: "Tell me about yourself", "Why Optum?", "Why healthcare?" [S7].
- Healthcare data science themes (30-day readmission risk, claims data, label leakage, fairness, HIPAA awareness) came from CVS Health and Kaiser Permanente results, not Optum; treat only as a general healthcare pattern [G].

**Sample questions (illustrative):**
- Build a model to predict 30-day readmission when only about 10% of patients are readmitted; discuss metric and leakage. [illustrative] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding) and Book 6 Part 9 (domain sets: fintech, e-commerce, healthcare, ads).
- Logistic regression versus gradient boosting when the model must be explainable to clinicians. [S15] Book 1 Part 2 (linear/logistic regression, regularization, feature engineering) and Book 1 Part 4 (trees, boosting, SHAP).
- Write pandas code to fill missing values and encode categorical labels without leaking test data. [S4] Book 1 Part 12 (NumPy/pandas/sklearn live-coding) and Book 6 Part 3 (imbalanced, noisy, missing data situations).
- Explain probability of a positive test given a rare condition. [S7] Book 1 Part 14 (statistics II: conditional probability and Bayes).
- Design an agentic application that answers member questions over policy documents; how do you evaluate it? [S13] Book 2 Part 8 (agents) and Book 2 Part 12 (GenAI system design and coding).
- SQL: flatten an employee-manager hierarchy with a recursive CTE. [S14] Book 3 Part 9 (recursive CTEs, hierarchies, graphs).
- Walk me through the project on your CV: why this model, what failed? [S7] Book 6 Part 10 ("design a solution end-to-end" open scenarios).
- Why healthcare and why Optum? [S7] Book 6 Part 6 (stakeholder conflicts and trade-off decisions), for structuring a concise motivated answer.

**What they score:**
- Python coding fluency and ML fundamentals, with many questions drawn from your projects [S7].
- LLM and Gen AI familiarity in recent reports and in India AI/ML postings (RAG, LangChain, vector databases listed as desirable) [S13][S8].
- Hiring manager or techno-managerial fit [S6][S13].
- Motivation for healthcare, from the HR questions reported [S7].
- No official scoring rubric was found [U].

**Level notes:**
- Titles in India postings: Associate Data Scientist, Data Scientist, Senior Data Scientist, Principal Data Scientist; AI/ML Engineer, Senior, Manager [S2][S8].
- Postings state minimum experience in years (one Hyderabad Associate posting asks 1+ years; a Senior posting 6+ years; one mid-to-senior listing 5+ years); this is posting text, not an interview expectation [S2][S8].
- Interview expectations by level were not found.

**Preparation plan (2 weeks):**
- Days 1-2: Python and pandas coding, missing data, encoding. Book 1 Part 12; Book 6 Part 3.
- Days 3-4: Statistics and probability basics. Book 1 Parts 13 and 14.
- Days 5-6: Regression, trees, boosting, explainability. Book 1 Parts 2 and 4.
- Days 7-8: Metrics for imbalanced outcomes. Book 1 Part 3; Book 6 Part 9 (healthcare).
- Days 9-10: Deep learning and NLP basics. Book 1 Parts 8 and 9.
- Days 11-12: LLM, RAG and agent design, evaluation. Book 2 Parts 6, 8, 9, 12 [G].
- Days 13-14: SQL refresh (Book 3 Parts 4, 9), project walkthrough practice, HR answers; Book 6 Part 10.

**Common mistakes:**
- Not being able to explain every model and choice on your own CV, since project questions are common [S7].
- Assuming a Dublin or other-unit Optum report describes the India loop [S4].
- Skipping SQL and Python fundamentals because the role is "AI" [S13][S14].
- Vague answers to "Why healthcare?" [S7].

**Recent changes and AI-era notes:**
- Gen AI questions and agentic system design appear in 2025 reports and in 2026 postings for Hyderabad, Noida, Gurugram and Bengaluru [S13][S8].
- A 2026 Hyderabad report (software developer, other role) mentions an AI-based screening or online assessment first; scope for data roles unknown [S14].
- No UHG or Optum policy on candidates using AI during interviews was found; a May 2026 Bloomberg report about tracking employees' AI use concerns staff, not candidates [S11][S16].
- Older: Hyderabad data scientist report from 2020 and generic reports from 2015-2018 [S12].

**Sources:**
- S1: https://www.unitedhealthgroup.com/careers/in/work.html . Supports: Careers at Optum (India); office cities and entity name reading comes from the search summary. Seen 2026-10-31. Snippet only.
- S2: https://careers.unitedhealthgroup.com/job/hyderabad/associate-data-scientist/34088/97936376624 . Supports: Hyderabad Associate Data Scientist posting (entry requirements in years; Python, R, SQL); Senior DS posting at careers.unitedhealthgroup.com/job/hyderabad/senior-data-scientist/50688/96158879504. Postings, not interview content. Seen 2026-10-31. Snippet only.
- S3: https://dataford.io/interview-guides/optum-tech/data-scientist . Supports: generic about 4-6 weeks and 5 rounds estimate for Optum Tech, flagged as not verified Optum data; Optum Financial DS guide (dataford.io/interview-guides/optum-financial/data-scientist) about 3 rounds over 3-5 weeks. Different business units. Seen 2026-10-31. Snippet only.
- S4: https://www.glassdoor.ie/Interview/Optum-Interview-E2409113-RVW102817614.htm . Supports: Optum DS reports pooled in the search summary: Dublin Senior/Principal (HR, team technical, Director round); India 2 interviews plus HR; internship live coding on preprocessing and label encoding; Gemini versus GPT question; about 3 weeks. Per-URL attribution is approximate. Anecdotal. Seen 2026-10-31. Snippet only.
- S5: https://www.unitedhealthgroup.com/careers/en/job-seeker-resources/blog/2025-08-01-tips-from-recent-hires.html . Supports: official six-step process, assessments not for all roles, interview varies by role, legitimate emails from uhg.com or optum.com. Seen 2026-10-31. Snippet only.
- S6: https://www.glassdoor.co.in/Interview/Optum-Interview-E2409113-RVW102158211.htm . Supports: India Data Scientist report (technical about 50 min, techno-managerial about 25 min, HR; another: recruiter plus two technical); attribution to this URL approximate. Anecdotal. Seen 2026-10-31. Snippet only.
- S7: https://www.glassdoor.co.in/Interview/Optum-Interview-E2409113-RVW103599724.htm . Supports: DS candidate reports (Python in every round, probability, logistic regression, ReLU, numpy/pandas, project and resume questions, LLM architecture; HR questions incl. Why Optum, Why healthcare); pooled across Glassdoor results and interviewquery.com/interview-guides/optum-data-scientist. Anecdotal. Seen 2026-10-31. Snippet only.
- S8: https://careers.unitedhealthgroup.com/job/noida/data-scientist/34088/95612494384 . Supports: Noida Data Scientist posting listing Gurugram, Hyderabad, Bangalore; Gurgaon AI/ML Engineer posting (careers.unitedhealthgroup.com/job/gurgaon/ai-ml-engineer/34088/99373677376); RAG and LLM focus, 5+ years for mid-senior; Manager AI/ML posting (careers.unitedhealthgroup.com/job/21264305). Postings, not interview content. Seen 2026-10-31. Snippet only.
- S9: https://dataford.io/interview-guides/optum/applied-scientist . Supports: existence of an Applied Scientist guide page only (title seen, no loop detail). Seen 2026-10-31. Snippet only.
- S10: https://blog.theinterviewguys.com/unitedhealth-group-interview-questions/ . Supports: third-party description of recruiter screen, digital video interview, live round, added technical round; theinterviewguys is a prep blog. Seen 2026-10-31. Snippet only.
- S11: https://hyring.com/jobseeker-toolkit/interview-questions/company/optum . Supports: aggregator description of interview formats (in person, live virtual, digital recorded) and UHG statement on recorded-interview review (secondhand); no AI policy for candidates. Seen 2026-10-31. Snippet only.
- S12: https://www.glassdoor.ca/Interview/Optum-Interview-E2409113-RVW31901521.htm . Supports: Hyderabad Data Scientist report from Feb 2020 (one day, in-depth ML algorithms question, anecdotal). Seen 2026-10-31. Snippet only.
- S13: https://www.glassdoor.com.au/Interview/Optum-Interview-E2409113-RVW104137733.htm . Supports: Bengaluru AI/ML-type reports (Nov 2025 Python/pandas then agentic system design; Jan 2025 two technical rounds then hiring manager); attribution approximate; anecdotal. Seen 2026-10-31. Snippet only.
- S14: https://www.glassdoor.com.mx/Entrevista/Optum-Entrevista-E2409113-RVW89075375.htm . Supports: Apr 2026 Hyderabad software developer report (AI-based screening, 1-2 technical, HR) and data engineering topics (Spark, window SQL, recursive CTE) from pooled results; other roles, anecdotal. Seen 2026-10-31. Snippet only.
- S15: https://www.interviewquery.com/interview-guides/optum-machine-learning-engineer . Supports: prep-guide themes (model selection, metrics for healthcare outcomes, pipeline maintainability); Dataford sample question on choosing a model for a business objective. Seen 2026-10-31. Snippet only.
- S16: https://bloomberg.com/news/articles/2026-05-15/unitedhealth-tracks-workers-ai-use-in-push-to-transform-company . Supports: May 2026 report that UHG tracks some employees' AI use (employees, not candidates). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Confidence: medium for UHG's generic six-step process [S5]; low for data scientist round order and content; none for Applied Scientist [S4][S6][S9].
- Verify on careers.unitedhealthgroup.com and with your recruiter: the rounds for your requisition, whether an online or AI-based assessment applies, whether recorded video interviews are used, and any AI-tool rule for interviews.
- Evidence is anonymous reviews mixing locations, roles and Optum units; one report is not the process [G].
