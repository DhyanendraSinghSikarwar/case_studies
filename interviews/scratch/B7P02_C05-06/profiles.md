### C5 Razorpay (Indian fintech unicorn)

**Evidence level:** Thin. No official Razorpay interview page appeared in full; the best items are a 2024-era Analytics India Magazine piece quoting a company representative (fragments only) and third-party prep sites that disagree on round counts [S1][S2][S4]. Little is specific to ML engineer or applied scientist roles.

**Roles seen in sources:** Data Scientist and ML engineer track [S1][S2]; a Lead ML Engineer posting and a Senior Manager Data Science posting [S6]; a small AI/ML team split across data scientist, ML engineer and MLOps roles, per one article [S3]; AI Builder and Full Stack Builder postings that expect AI-tool fluency [S5]. Data analyst and SDE guides also exist but are a different track [S4].

**Process overview (as reported):**
1. A company representative told Analytics India Magazine that Razorpay follows a five-step process for data science and ML hiring; the snippet did not list all five steps [S1].
2. A technical assessment or screen, then deep-dive technical rounds (Dataford describes 2 rounds, about 2-4 weeks, for data scientist; aggregator guide) [S2].
3. Candidate-style reports mention ML knowledge and system design in a later stage, with an example of a real-time ranking engine for payment gateways (one article, not a verified question) [S3].
4. A final hiring-manager round focused on cultural fit and levelling where needed [S1]. Hiring-manager rounds are also described as probing decisions made, alternatives rejected and results measured (SDE guide, not DS-specific) [S4].
5. Round counts differ by source: 2 (Dataford DS), 3 to 5, 4 to 6, and one Glassdoor post of 4 technical rounds plus HR over about three weeks (anecdotal) [S2][S4][S7]. Treat all as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Technical assessment / screen | Online or live; format not found | ML, statistics, SQL/Python as listed in guides | [S2] |
| Deep-dive technical | Interview(s); duration not found in sources | ML depth, productionizing models | [S2][S3] |
| ML system design | Interview | Design example: real-time ranking for payments | [S3] one article |
| Practical AI-tool assessment | 60 min, engineering roles | Planning and execution with autonomous AI tools | [S7] anecdotal, not DS-specific |
| Hiring manager | Interview | Decisions, results, cultural fit, levelling | [S1][S4] |

**Question types:**
- Machine learning and algorithms, statistics, SQL and Python (guide topic lists) [S2].
- Productionizing models and ML system design (ranking, payments) [S3].
- Project deep dives: choices, rejected alternatives, measured results [S4].
- Fit with Razorpay's stated hiring themes: role fit, ownership, collaboration, use of AI [S4][S5].

**Sample questions (illustrative):**
- Design a real-time ranking or routing model for choosing a payment gateway: features, latency, metric, fallback. [S3] Book 1 Part 11 (ML system design) and Book 4 Part 12.
- Build a fraud detection model with heavily imbalanced labels; pick the metric and threshold. [illustrative] Book 1 Part 3 (metrics and imbalance).
- Write SQL for success rate by payment method per day, then flag days that dropped. [illustrative] Book 3 Part 5 (window functions) and Part 8 (product metrics).
- How would you take a model from notebook to production and monitor drift? [S3] Book 1 Part 11 and Book 4 Part 12.
- Explain a past project: what alternatives did you reject and what did you measure? [S4] Book 6 Part 6 (stakeholder and project stories).
- Design an A/B test for a new checkout flow with a small base of merchants. [illustrative] Book 1 Part 10 (A/B testing) and Book 6 Part 4.
- Build a retrieval-augmented assistant for merchant support: chunking, evaluation, failure modes. [illustrative] Book 2 Part 6 (RAG basics) and Book 2 Part 9 (LLM evaluation).

**What they score:**
- Role fit, communication and collaboration, ownership, and use of AI in problem solving, as reported from the careers framing (Role Fit, Synergy, AI Edge) [S4][S5].
- Technical depth in ML and ability to ship models to production [S2][S3].
- Decision quality in past work [S4].

**Level notes:**
- ML Engineer track is reported to prefer about 2-3 years of experience (FACE Prep; Weekday listing says minimum 2 years) [S3].
- Postings exist at Lead, Senior Manager and Associate Director levels; expectations not found in snippets [S6].

**Preparation plan (2 weeks):**
- Days 1-2: SQL windows and payment-metric analysis. Book 3 Parts 5 and 8.
- Days 3-4: ML fundamentals, metrics, imbalance. Book 1 Parts 1-4.
- Days 5-6: Statistics and A/B testing. Book 1 Parts 10, 13; Book 6 Part 4.
- Days 7-8: Coding in a plain editor. Book 5 Parts 1-9 [G].
- Days 9-10: Transformers, RAG and agents if the role is GenAI. Book 2 Parts 1, 6, 9.
- Days 11-12: ML system design and production. Book 1 Part 11, Book 4 Part 12.
- Days 13-14: Project stories and two mocks. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Treating one aggregator round count as the process [S2][S4].
- Describing a project without the alternatives you rejected or the measured result [S4].
- Ignoring production and monitoring for an ML role [S3].
- Assuming AI tools are banned or allowed without asking the recruiter [G].

**Recent changes and AI-era notes:**
- Razorpay's careers framing is reported to include "AI Edge", and a 2026 guide says use of AI in problem solving is evaluated [S4][S5].
- A Glassdoor-hosted report describes a 60-minute practical assessment with autonomous AI tools for engineering roles; single anecdote, scope for DS/ML unknown [S7].
- Job listings expect AI-tool fluency (one names Claude Code or Cursor as a default environment) [S5].
- Older: the Analytics India Magazine five-step statement; date not confirmed in snippet [S1].

**Sources:**
- S1: https://analyticsindiamag.com/ai-hiring/data-science-hiring-process-at-razorpay . Supports: five-step DS/ML process per company representative, hiring-manager round on culture and levelling (fragments only). Seen 2026-10-31. Snippet only.
- S2: https://dataford.io/interview-guides/razorpay/data-scientist . Supports: DS guide, 2 rounds, about 2-4 weeks, technical assessment then deep dives (aggregator). Seen 2026-10-31. Snippet only.
- S3: https://www.interviewquery.com/interview-guides/razorpay-machine-learning-engineer . Supports: MLE guide; ML system design example, productionizing, 2-3 years preference (summary also draws on an AI/ML team article and FACE Prep). Seen 2026-10-31. Snippet only.
- S4: https://www.designgurus.io/answers/detail/what-is-the-razorpay-interview-process-like-round-by-round . Supports: general round counts, hiring-manager probing, careers-page themes (third-party; summary also uses Orbyt, Fueler). Seen 2026-10-31. Snippet only.
- S5: https://fueler.io/blog/razorpay-hiring-process-jobs-interviews-and-skills-required . Supports: 2026 guide on hiring themes and AI use; AI-fluency expectations in postings (summary also cites a Full Stack Builder listing). Seen 2026-10-31. Snippet only.
- S6: https://builtinbengaluru.in/job/lead-ml-engineer/3729874 . Supports: Lead ML Engineer posting (ranking, neural networks). Seen 2026-10-31. Snippet only.
- S7: https://fr.glassdoor.ch/Entretien/Razorpay-Entretien-E1146550-RVW93476801.htm . Supports: Glassdoor report of a 60-minute AI-tools practical assessment; the page-to-claim match is from a search summary of several Glassdoor results (anecdotal). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence in round counts and durations; sources conflict [S2][S4].
- Almost nothing is specific to applied scientist or GenAI roles; ask the recruiter for the round list [G].
- Verify on Razorpay's careers page whether AI tools are allowed in assessments and what the AI-tools practical covers [S5][S7].
- No claim here that any question will be asked.

### C6 CRED (Indian fintech unicorn)

**Evidence level:** Thin. Evidence is one Analytics India Magazine article from December 2024 (fragments), aggregator guides that disagree on round counts, and mostly SDE-focused review pages; no ML engineer specific report was found [S1][S2][S3].

**Roles seen in sources:** Data scientist and data science analyst hiring in Bengaluru, from a team of about 30 including data scientists and ML engineers [S1]; data scientist guides [S2]; AI/ML engineer and ML, NLP intern listings [S5]; product analyst and data scientist postings on Lever [S4].

**Process overview (as reported):**
1. The head of data science told Analytics India Magazine the company uses a mix of behavioural, skill-based and situational interviews; individual rounds were not visible in the snippet [S1].
2. One guide describes 3 rounds over about 3-5 weeks: screening, technical assessment, deep-dive interviews (aggregator) [S2].
3. Another source reports 5 rounds from 82 candidate reports, and a Glassdoor review for a Senior Data Scientist role says the interview was divided into 5 rounds (anecdotal) [S2][S6].
4. A general CRED guide says four to six rounds depending on role and level, often starting with an online HackerRank coding test (not ML-specific) [S3].
5. Dataford says behavioural and product-sense rounds are equally weighted and mentions a cultural alignment round [S2].
6. Duration of each round was not found in sources; one review (SDE) reports about 2 weeks end to end (anecdotal) [S6].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Screening | Format not found | Background and role fit | [S2] |
| Technical assessment | Possibly online test | Stats, SQL, Python | [S2][S3] |
| Deep-dive technical | Interview; duration not found | Modeling, metrics, experimentation | [S2] |
| Product sense / case | Interview | Root-cause analysis, e.g. engagement drop | [S2] |
| Behavioural / cultural | Interview | Trust, ownership, innovation | [S1][S2] |

**Question types:**
- Statistics, data visualization and dashboarding, Python (Interview Query top topics) [S2].
- SQL, metrics and experimentation, ML/modeling (Prepfully question bank topics) [S2].
- Product analytics cases: investigate a sudden 10% drop in engagement on the payment screen (Dataford example) [S2].
- Behavioural: how would you improve CRED if you got the job (Prepfully-listed, anecdotal) [S2].

**Sample questions (illustrative):**
- Engagement on the payment screen dropped 10% overnight; how do you find the root cause? [S2] Book 3 Part 8 (product metrics) and Book 6 Part 4.
- Build a credit-risk or repayment propensity model with limited bad-loan labels; choose metrics. [illustrative] Book 1 Part 3 (metrics) and Book 1 Part 4.
- Write SQL for month-over-month retention of members who paid a card bill. [illustrative] Book 3 Part 5 and Part 6 (cohorts).
- Design an experiment for a reward-offer change and name guardrail metrics. [illustrative] Book 1 Part 10 (A/B testing).
- How would you improve CRED if you got this job? [S2] Book 6 Part 1 (product metrics) and Book 6 Part 6 (stakeholder conflicts and trade-offs).
- Design an LLM-based support assistant for card and payments queries with an evaluation plan. [illustrative] Book 2 Part 6 (RAG basics), Book 2 Part 9 (LLM evaluation) and Book 2 Part 12.
- Explain a model you shipped and how you monitored it. [illustrative] Book 1 Part 11 and Book 4 Part 12.

**What they score:**
- Culture values named by the head of data science: trust, ownership, innovation, entrepreneurship [S1].
- Technical execution plus fit with a high-growth culture (Dataford wording) [S2].
- Product sense and behavioural signals weighted comparably to technical ones, per one guide [S2].

**Level notes:**
- Hiring across experience levels was stated in the 2024 article; level names not found [S1].
- An older AIM-linked page asked for more than three years in data science, especially NLP and deep learning; likely outdated [S4].

**Preparation plan (2 weeks):**
- Days 1-2: SQL, cohorts, retention. Book 3 Parts 4-6 and 8.
- Days 3-4: Statistics and A/B testing. Book 1 Parts 10, 13, 14; Book 6 Part 4.
- Days 5-6: ML fundamentals, metrics, boosting. Book 1 Parts 1-4.
- Days 7-8: Python coding without autocomplete. Book 5 Parts 1-9 [G].
- Days 9-10: Product cases and metric drops. Book 3 Part 8, Book 6 Part 4.
- Days 11-12: GenAI basics and ML system design if the role needs it. Book 2 Parts 1, 9, 12; Book 1 Part 11.
- Days 13-14: Ownership stories and mocks. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Relying on SDE interview reviews as if they described the data science loop [S6].
- Giving a model answer to a product case without first checking data quality and segments [G].
- Underpreparing the behavioural and product rounds [S2].
- Quoting a single round count as fact [S2][S3].

**Recent changes and AI-era notes:**
- CRED's Lever postings say it may use AI tools to support parts of hiring, such as reviewing applications, and that final decisions are made by humans [S4].
- No source described a dedicated GenAI interview track or a candidate AI-tool policy [S4].
- Older: the December 2024 article and 2020-2022 candidate reports [S1][S6].

**Sources:**
- S1: https://analyticsindiamag.com/ai-hiring/data-science-hiring-process-at-cred . Supports: team of about 30, mixed behavioural/skill/situational interviews, values (Dec 2024; fragments). Seen 2026-10-31. Snippet only.
- S2: https://dataford.io/interview-guides/cred/data-scientist . Supports: 3 vs 5 round claims, behavioural and product-sense weighting, engagement-drop case (aggregator; Interview Query and Prepfully topic lists come from the same search summary). Seen 2026-10-31. Snippet only.
- S3: https://www.designgurus.io/answers/detail/what-is-the-cred-interview-process-like-round-by-round . Supports: general 4-6 rounds, HackerRank start (third-party; summary also cites Hyring, Fueler). Seen 2026-10-31. Snippet only.
- S4: https://jobs.lever.co/cred . Supports: AI-in-hiring disclosure with human decisions; data scientist and analyst postings (summary of several Lever pages). Seen 2026-10-31. Snippet only.
- S5: https://builtinhyderabad.in/job/prefr-cred-ai-ml-engineer/9644887 . Supports: an AI/ML engineer listing associated with CRED; details not seen. Seen 2026-10-31. Snippet only.
- S6: https://www.glassdoor.ie/Interview/CRED-Interview-E3050300-RVW44639058.htm . Supports: CRED Glassdoor reviews (mostly SDE; Senior DS 5-round review, about 2 weeks; page-to-claim match from search summary; anecdotal). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence in round counts; sources give 3, 4-6 and 5 [S2][S3].
- No ML engineer, applied scientist or GenAI specific round detail was found [S3].
- Verify on CRED's careers page the rounds for your role and whether a coding test comes first [S3][S4].
- No claim here that any question will be asked.
