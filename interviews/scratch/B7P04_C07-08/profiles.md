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
