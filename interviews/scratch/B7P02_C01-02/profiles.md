### C1 Flipkart (Indian product company)

**Evidence level:** Thin. There is one detailed first-hand loop (a Data Scientist 2 post on LeetCode) and one generic third-party guide, plus scattered Glassdoor reports that are mostly for software roles. No official Flipkart process page appeared in any result, and no 2025-2026 first-hand report for ML engineer, applied scientist or GenAI roles could be read [S1][S2][S3].

**Roles seen in sources:** Data Scientist, including a Data Scientist 2 loop [S1][S2]; Machine Learning Engineer, as a generic guide only [S3]; AI Engineer, as a March 2026 candidate thread whose content was not visible in the snippet [S4]; Research Scientist guide exists but was not read [S5]. Job listings mention Senior and Staff AI Engineer and LLM work in NLP and multi-modal settings [S6][S7].

**Process overview (as reported):**
1. Screening call. In the Data Scientist 2 report, a 30-minute screen with a research director covering past work and behavioural questions (anecdotal) [S2]. Other reports mention HR phone screens or a SQL test first (anecdotal, mixed roles) [S8].
2. Math-modelling depth round, about 1 hour, with a principal data scientist or director (anecdotal, one report) [S2].
3. Data-science depth round, about 1 hour, on end-to-end ML system design from an abstract problem (anecdotal, one report) [S2].
4. Coding round, about 2 hours, built around a modelling problem rather than a plain algorithms puzzle (anecdotal, one report) [S2]. A generic guide instead lists ML breadth, ML system design, ML coding and a hiring manager round, about 4 rounds, with a take-home sometimes used [S1].
5. Duration: 2-4 weeks in one guide, 3 weeks in one Glassdoor review, about a month in another candidate account [S1][S8]. Rough.
6. Round counts differ by source (4 to 6 reported for various roles) and by level and campus versus lateral hiring [S9].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Screening | 30 min call, research director | Past work, behavioural | [S2] anecdotal |
| Math-modelling depth | 1 hr interview | Mathematical modelling, optimisation thinking | [S2] anecdotal |
| DS depth / ML system design | 1 hr interview | End-to-end ML pipeline from an abstract problem | [S2] anecdotal; [S1] generic |
| Coding | 2 hr interview, shared with a senior data scientist | Building a model for a pricing problem | [S2] anecdotal |
| ML breadth (generic guide) | Interview | Algorithms and the underlying maths | [S1] |
| Hiring manager | Interview | Projects, behaviour, fit | [S1][S8] |
| Case round (some roles) | Case discussion | Business problem structuring | [S9], applies mainly to analytics and DS-type roles per that source |

**Question types:**
- ML system design framed as a product problem, for example detecting mislabeled or mismapped products from sellers [S1].
- Modelling under a business objective, for example setting discounts across brands given competitors to maximise revenue [S2] (anecdotal).
- Explaining the maths behind a model, not only naming it [S1].
- Practical modelling exercise on a dataset [S1].
- SQL test for some roles [S8].
- Machine coding (low-level design) appears in software-role reports; no direct confirmation for ML roles [S10].
- Behavioural and project deep-dives with hiring managers [S1][S8].

**Sample questions (illustrative):**
- Set discounts for several shoe brands given competitor prices, and build a model that maximises revenue. [S2] Book 6 Part 5 (business case studies, pricing) and Book 1 Part 11 (ML system design, pricing).
- A seller lists a product under the wrong category. Design an ML approach to detect mislabeled or mismapped listings. [S1] Book 1 Part 9 (NLP and CV, embeddings) and Book 1 Part 3 (imbalance, thresholding).
- Derive the loss for logistic regression and say what regularization does to the solution. [illustrative] Book 1 Part 2 (regression, regularization).
- Here is a dataset and 90 minutes: build, validate and explain a baseline model. [S1] Book 1 Part 12 (live-coding with pandas and sklearn).
- Find the top 3 products by revenue in each category last month. [illustrative] Book 3 Part 4 (window functions, top-N per group).
- Design a RAG shopping assistant over a product catalogue and say how you would evaluate it. [illustrative] Book 2 Parts 6 and 9 (RAG basics, LLM evaluation) and Part 12.
- Design a food-ordering system with clean classes and extensible code (reported for a software role). [S10] Book 5 Part 14 (design problems).
- Walk me through your most complex project and the trade-offs you made. [illustrative] Book 6 Part 6 (trade-off decisions).

**What they score:**
- Depth in ML and mathematics, with reasoning explained, per the generic guide [S1].
- Ability to turn an abstract business problem into an end-to-end pipeline [S2] (anecdotal).
- Hands-on modelling and coding in a long working session [S2] (anecdotal).
- Fit and ownership judged by a hiring manager [S1][S8].
- No official Flipkart rubric was found; do not assume one [U].

**Level notes:**
- The detailed report was for a Data Scientist 2 position described by the candidate as grade 9 [S2]. Other level names were not found in snippets.
- Senior and Staff AI Engineer listings exist; expectations were not visible in snippets [S6].
- Higher-level loops often add design depth and a hiring-manager conversation [G].

**Preparation plan (2 weeks):**
- Days 1-2: Statistics and ML fundamentals with the maths explained out loud. Book 1 Parts 1-2 and 13.
- Days 3-4: Metrics, imbalance, trees and boosting. Book 1 Parts 3-4.
- Days 5-6: Pricing, optimisation and e-commerce business cases; forecasting. Book 6 Part 5; Book 1 Part 6.
- Days 7-8: Recommenders, ranking, search; NLP for catalogue problems. Book 1 Parts 7 and 9.
- Days 9-10: ML system design, end-to-end from an abstract prompt. Book 1 Part 11; Book 4 Part 12.
- Days 11-12: Timed modelling and SQL practice; basic DSA as a hedge. Book 1 Part 12; Book 3 Parts 4-6; Book 5 Parts 1-2 [G].
- Day 13: GenAI and RAG basics if the role is AI or GenAI. Book 2 Parts 6, 9 and 12.
- Day 14: Project stories and a mock with a hiring-manager style conversation. Book 6 Part 6.

**Common mistakes:**
- Naming a model without explaining the maths behind it [S1].
- Treating the coding round as pure LeetCode when the one detailed report was a modelling problem [S2].
- Jumping to a model without stating the business objective and constraints in a design round [G].
- Assuming a software-role report (machine coding, DSA) describes the data science loop [S10].
- Treating one candidate's loop as the standard [G].

**Recent changes and AI-era notes:**
- No official Flipkart policy on AI tools in interviews appeared in results; ask your recruiter [U].
- Recent: an AI Engineer interview thread dated March 2026 exists, content not visible [S4]. A FACE Prep article says prompt, retrieval and safety questions appear mainly for GenAI-flagged roles; this is a general guide, not Flipkart-confirmed [S11].
- Company direction: Flipkart describes a GenAI-powered assistant [S12], and a talk by a Flipkart principal data scientist describes using several smaller open-source models for its use cases [S13]. Useful background, not interview content.
- Older: Glassdoor and similar reports from 2021-2023 are mostly software roles [S8][S10].

**Sources:**
- S1: https://www.interviewquery.com/guides/flipkart-data-scientist . Supports: DS loop of about 4 rounds (ML breadth, ML system design, ML coding, hiring manager), take-home sometimes, mislabeled-product design scenario, 2-4 weeks. Third-party guide. Seen 2026-10-31. Snippet only.
- S2: https://leetcode.com/discuss/post/6740402/flipkart-data-scientist-2-interview-by-a-is2i/ . Supports: Data Scientist 2 loop (30 min screen, 1 hr math modelling, 1 hr DS depth, 2 hr coding with a discount-pricing problem); one candidate, anecdotal. Seen 2026-10-31. Snippet only.
- S3: https://www.interviewquery.com/interview-guides/flipkart-machine-learning-engineer . Supports: generic MLE guide (Python, SQL, algorithms, structured process); no concrete rounds. Seen 2026-10-31. Snippet only.
- S4: https://leetcode.com/discuss/post/7687848/flipkart-ai-engineer-interview-status-pr-pl45/ . Supports: existence of a March 2026 AI Engineer interview thread; contents not visible. Seen 2026-10-31. Snippet only.
- S5: https://www.interviewquery.com/interview-guides/flipkart-research-scientist . Supports: a Flipkart research scientist guide exists; not read further. Seen 2026-10-31. Snippet only.
- S6: https://nodeflair.com/jobs/flipkart-senior-ai-engineer-538540 . Supports: Senior AI Engineer listing (and a Staff AI Engineer listing on the same site). Seen 2026-10-31. Snippet only.
- S7: https://jobs.weekday.works/data-scientist-at-flipkart-internet-pvt-ltd-wkdyeo276y . Supports: Data Scientist listing mentioning LLM-based solutions, NLP and multi-modal work. Seen 2026-10-31. Snippet only.
- S8: https://clear.glassdoor.nl/Interview/Flipkart-Interview-E300494-RVW10756044.htm . Supports: Glassdoor reports of a SQL test then three rounds, HR phone screens, hiring manager rounds, about 3 weeks; the exact page-to-detail match is from a search summary of several Glassdoor results, anecdotal, mixed roles and years. Seen 2026-10-31. Snippet only.
- S9: https://www.hackingthecaseinterview.com/pages/flipkart-case-interview . Supports: case rounds mainly for analyst, DS, PM and category roles; 4-6 rounds depending on role and route. Third-party. Seen 2026-10-31. Snippet only.
- S10: https://www.jointaro.com/interviews/companies/flipkart/work-experiences/software-engineer-ii-sde2-bengaluru-june-27-2025-4-71b229f5/ . Supports: SDE-2 machine coding and low-level design reports (June 2025, software role, anecdotal); the food-ordering example comes from a search summary of such reports. Seen 2026-10-31. Snippet only.
- S11: https://faceprep.in/article/flipkart-ai-roles-for-freshers-2026-the-tech-flipkart-com-pathway/ . Supports: prompt/retrieval/safety questions mainly for GenAI-flagged roles; Flipkart listed among AI/ML hirers. Third-party. Seen 2026-10-31. Snippet only.
- S12: https://stories.flipkart.com/gen-ai-indian-ecommerce-mayur-datar . Supports: Flipkart Q&A on GenAI in e-commerce including a GenAI chat assistant. Company page. Seen 2026-10-31. Snippet only.
- S13: https://seedtoscale.com/accelaisummit/gen-ai-at-flipkart . Supports: talk by a Flipkart principal data scientist on GenAI; the smaller open-source models point is from the search summary. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence overall. The only detailed loop is one Data Scientist 2 anecdote; round counts, durations and the 2-hour coding format may not apply to your role or team [S2].
- ML engineer, applied scientist and GenAI loops: essentially no first-hand detail found [S3][S4].
- Verify with your recruiter or the Flipkart careers page: rounds for your role and level, whether a take-home or case round applies, and any AI-tool rule [S1][S9].
- No claim here that any question will be asked.

### C2 Swiggy (Indian unicorn)

**Evidence level:** Thin. Several candidate reports and third-party guides exist for data science, but they disagree on the number of rounds (2, 3 or 4), no official Swiggy process page appeared, and ML engineer, applied scientist and GenAI loops have almost no first-hand detail [S1][S2][S3][S4].

**Roles seen in sources:** Data Scientist, including Data Scientist 1 and Associate Data Scientist reports [S2][S5]; Machine Learning Engineer as a generic guide only [S6]; Data Engineer guide [S7]. No applied scientist or GenAI interview report found.

**Process overview (as reported):**
1. Resume shortlisting, then a technical screen covering SQL, Python, DSA, ML fundamentals and precision and recall (guide) [S3].
2. Round count varies: a guide says about 2 rounds (resume deep-dive, then ML coding and SQL) [S1]; another source says 3 to 4 [S3]; a Glassdoor report lists three rounds (data science, engineering/coding, product) followed by a hiring manager round (anecdotal, date unclear) [S4].
3. A Data Scientist 1 report: a coding interview of about 1 hour on Python, basic Pandas and SQL, with every round described as a knockout (anecdotal) [S2].
4. A more recent Glassdoor-style report (August 2025): data structures and SQL, then data science with ML and DL, then an HR round (anecdotal, page match approximate) [S8].
5. ML engineer guide: SQL test, a data science round on ML concepts, and possibly a business case study [S6].
6. Duration estimates range from 1-2 weeks to about 3-5 weeks across sources [S3]. Rough.
7. Interviews lean on the resume: interviewers dig into why and how of each project decision [S3].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Resume shortlist and screen | Screen | SQL, Python, DSA, ML basics, precision/recall | [S3] guide |
| Coding / SQL | About 1 hr live | Python, Pandas groupby, SQL subqueries, ranking, one easy DSA question | [S2][S9] anecdotal |
| Data science / ML | Interview | ML and DL concepts, resume-based depth | [S4][S8] anecdotal |
| Product / case | Interview | Product ideas, product analytics, case study on Swiggy | [S4][S5] anecdotal |
| Hiring manager or HR | Interview | Fit, projects | [S4][S8] anecdotal |

**Question types:**
- SQL: subqueries, ranking, GROUP BY and HAVING [S2][S9].
- Python and Pandas: functions, decorators, groupby, practical data manipulation [S2][S1].
- One easy-to-medium DSA question in some reports; one Naukri candidate says DSA is a must even for data roles, while another reviewer says the focus was practical data manipulation (conflicting, anecdotal) [S2][S5][S9].
- ML and statistics fundamentals: precision, recall, F1, ROC-AUC, regularization, bias-variance, probability [S2].
- Deep learning basics in one report (anecdotal) [S2].
- Case study based on Swiggy's business: clarify the objective, define metrics, state data constraints [S3][S5].
- Resume deep-dive [S1][S3].

**Sample questions (illustrative):**
- Rank orders by value within each restaurant and keep the top 3, then filter restaurants with a minimum order count. [S9] Book 3 Part 4 (ranking, top-N per group) and Part 1 (GROUP BY/HAVING).
- Using Pandas, compute average delivery time per city and flag cities above the overall mean. [S2] Book 1 Part 12 (pandas live coding) and Book 3 Part 3.
- Given stock prices by day, find the maximum profit from one buy and one sell. [S2] Book 5 Part 1 (arrays) and Part 8 (greedy).
- Explain precision, recall and ROC-AUC, and pick a metric for a fraud-style imbalanced problem. [S2] Book 1 Part 3 (classification metrics, imbalance).
- Design a model to predict delivery time for a food order and say how you would monitor it. [illustrative] Book 1 Part 11 (ML system design, ETA) and Book 4 Part 8 (monitoring).
- Orders per day dropped 8% in one city. Walk through how you would investigate. [illustrative] Book 6 Part 1 (metric drops) and Book 3 Part 8 (product metrics).
- Walk through your last project: why this model, what alternatives, what failed. [S3] Book 6 Part 6 (trade-off decisions).
- Design a text-to-SQL assistant for internal analysts and say how you would evaluate it. [illustrative] Book 2 Parts 9 and 12 (evaluation, GenAI design).

**What they score:**
- Practical coding in Python, Pandas and SQL more than exotic algorithms, per several reports (anecdotal) [S1][S9].
- ML fundamentals explained clearly, plus ownership of resume projects [S3].
- Product and business reasoning on case problems [S3][S4].
- No official rubric found; do not assume one [U].

**Level notes:**
- Level names seen: Data Scientist 1, Associate Data Scientist; a source mentions a DSA round for Data Scientist II roles [S2][S5][S3].
- Detailed level expectations not found in snippets [U].

**Preparation plan (2 weeks):**
- Days 1-2: SQL: aggregation, joins, subqueries, ranking. Book 3 Parts 1-4.
- Days 3-4: Pandas and Python fluency. Book 1 Part 12; Book 3 Parts 5-6.
- Days 5-6: ML fundamentals, metrics, imbalance, boosting. Book 1 Parts 1-4 and 13.
- Days 7-8: Deep learning basics, NLP, recommenders and ranking (food discovery). Book 1 Parts 7-9.
- Days 9-10: Easy-to-medium DSA as a hedge: arrays, hashing, greedy. Book 5 Parts 1, 2 and 8 [G].
- Days 11-12: Product and case practice: metrics, pricing, delivery time. Book 6 Parts 1 and 5; Book 1 Part 11.
- Day 13: GenAI basics and a look at Swiggy's published LLM work if the role touches GenAI. Book 2 Parts 6, 9 and 12 [S10][S11].
- Day 14: Resume walk-through and a mock. Book 6 Part 6.

**Common mistakes:**
- Skipping DSA entirely because the role is data science, when some reports include a question [S2][S5].
- Weak resume projects: interviewers drill into why and how of decisions [S3].
- Starting a case with a solution instead of objective, metrics and data constraints [S3].
- Memorising metrics without being able to choose between them [S2].
- Treating one candidate's loop as the standard [G].

**Recent changes and AI-era notes:**
- No official Swiggy AI-tool policy for interviews appeared; ask your recruiter [U].
- Recent: a December 2025 Associate Data Scientist report lists SQL, Python, ML and Swiggy-based case studies (anecdotal) [S5]. An August 2025 report lists DSA and SQL, then ML and DL (anecdotal) [S8].
- Company context: Swiggy's Hermes started as a GenAI text-to-SQL assistant in Slack, and Swiggy has described GenAI work on search, customer service and partner tools, via ZenML summaries [S10][S11]. Background, not interview content; no GenAI-specific interview report found.
- Older: the three-round-plus-hiring-manager Glassdoor description has no clear date [S4].

**Sources:**
- S1: https://www.interviewquery.com/guides/swiggy-data-scientist . Supports: guide saying about 2 rounds (resume deep-dive, ML coding/SQL), clustering and NumPy/Pandas coding, practical bar. Third-party. Seen 2026-10-31. Snippet only.
- S2: https://leetcode.com/discuss/interview-experience/6740564 . Supports: Data Scientist 1 report (about 1 hr coding on Python, Pandas, SQL; knockout rounds; stock buy-sell question; metrics and probability questions); one candidate, anecdotal. Seen 2026-10-31. Snippet only.
- S3: https://dataford.io/interview-guides/swiggy/data-scientist . Supports: resume shortlist, technical screen topics, 3-4 rounds, resume drill-down, case-study advice, timeline range. Third-party. Seen 2026-10-31. Snippet only.
- S4: https://www.glassdoor.com.hk/Interview/Swiggy-Interview-E952680-RVW25694400.htm . Supports: three rounds (data science, engineering, product) plus hiring manager; anecdotal, undated. Seen 2026-10-31. Snippet only.
- S5: https://www.naukri.com/code360/interview-experiences/swiggy-private-limited/swiggy-interview-experience-off-campus-dec-2025 . Supports: Dec 2025 Associate Data Scientist topics (SQL, Python, ML, Swiggy case studies), DSA advice; anecdotal. Seen 2026-10-31. Snippet only.
- S6: https://www.interviewquery.com/interview-guides/swiggy-machine-learning-engineer . Supports: ML engineer guide (SQL test, DS round, possible business case); third-party. Seen 2026-10-31. Snippet only.
- S7: https://www.interviewquery.com/prep-guides/swiggy-data-engineer . Supports: data engineer loop of 3-4 rounds; not used for DS claims. Seen 2026-10-31. Snippet only.
- S8: https://www.glassdoor.it/Colloquio/Swiggy-Colloquio-E952680-RVW100811838.htm . Supports: August 2025-style report (DSA and SQL, then DS/ML/DL, then HR); the page-to-detail match is from a search summary of several Glassdoor results, anecdotal. Seen 2026-10-31. Snippet only.
- S9: https://leetcode.com/discuss/post/6740564/swiggy-data-scientist-1-interview-by-kus-uba1/ . Supports: same Data Scientist 1 post (SQL subqueries; another Bangalore report of two easy coding questions and ranking/HAVING SQL comes from the search summary); anecdotal. Seen 2026-10-31. Snippet only.
- S10: https://www.zenml.io/llmops-database/evolution-of-hermes-v3-building-a-conversational-ai-data-analyst . Supports: Hermes text-to-SQL assistant background. Summary of a Swiggy write-up. Seen 2026-10-31. Snippet only.
- S11: https://www.zenml.io/llmops-database/neural-search-and-conversational-ai-for-food-delivery-and-restaurant-discovery . Supports: Swiggy GenAI work on search, support and partner tools (Aug 2023 post summary). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence overall: round counts conflict (2, 3, 4) and most detail is anonymous [S1][S3][S4].
- Applied scientist, ML engineer and GenAI loops: no first-hand detail found [S6].
- Verify with your recruiter or careers.swiggy.com: rounds for your role and level, whether DSA is included, and any AI-tool rule.
- No claim here that any question will be asked.
