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

### C3 Zomato (Indian unicorn; listed parent Eternal Limited)

**Evidence level:** Thin. No official Zomato or Eternal interview page appeared. The data-science-specific reports are a few anecdotes, mostly older (a Dec 2022 data scientist offer post, a 2023 case-study mention), and most 2025-2026 candidate posts are for SDE or analyst roles, not data science or ML. An Analytics India Magazine piece on the data science hiring process appeared, but its step list was cut off in the snippet [S3][S1][S2].

**Roles seen in sources:** Data Scientist (one Dec 2022 offer report, one 2024 AmbitionBox listing, older Glassdoor mentions) [S1][S6][S2]. A Naukri Code360 data scientist guide that covers junior to principal levels [S15]. ML / AI Engineer (a 2026 prep-site article only, no candidate report found) [S5]. An April 2025 Glassdoor report on ML and LLM topics at a Roorkee site, role not clear from the snippet (anecdotal) [S4]. No GenAI or applied scientist interview report found.

**Company note:** Zomato Limited was renamed Eternal Limited (approved March 2025). Eternal is the listed parent and runs Zomato, Blinkit, District and Hyperpure; the Zomato app and brand keep their name. Headquarters Gurugram [S7][S8]. Job and interview posts may say Zomato, Eternal or Blinkit; check which business unit the role is in [U].

**Process overview (as reported):**
1. Screen or managerial conversation. One Dec 2022 data scientist report starts with a 20-minute managerial round with a senior leader covering culture, projects and expected work (anecdotal, old) [S1].
2. Technical rounds. Reports vary: Python, SQL, and spreadsheet or BI tools in one Glassdoor account [S2]; probability and statistics, Python and SQL are the skills named in a prep guide [S15]; a generic prep page lists an online coding test and two DSA-heavy technical interviews, which is a general Zomato process, not a data science one [S10].
3. Case study round. A one-hour technical plus case study round with a principal data scientist in the Dec 2022 report [S1]. A 2023 candidate reportedly got two case problems on improving Zomato's recommendations plus a coding question (older, from a search summary) [U].
4. Case study and guesstimate round in a four-round Glassdoor account (2 technical, 1 case plus guesstimate, 1 HR); another account lists five rounds (3 technical, 2 screening and HR). Both anecdotal and role mix unclear [S2].
5. HR or culture round [S2][S10].
6. The same Dec 2022 post says candidates from top colleges may get only one round, so round count depends on the candidate path (anecdotal) [S1].
7. Duration of each round: mostly not found in sources. Total timeline not found.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Managerial / screen | About 20 min conversation (one report) | Culture, projects, expectations | [S1] anecdotal |
| Technical (DS) | Live, duration not found | SQL, Python, statistics, probability | [S2][S15] anecdotal |
| Technical + case study | About 1 hour with a principal data scientist (one report) | Applied problem solving on a Zomato-style problem | [S1] anecdotal, 2022 |
| Case + guesstimate | Live | Marketplace case, estimation, assumptions | [S2][S11] |
| HR / culture | Conversation | Fit | [S2][S10] |
| ML / LLM concepts | Live discussion (Roorkee report, April 2025) | Representation learning, Random Forest vs Transformer inputs, F1 vs accuracy, LLM basics and LLM evaluation | [S4] anecdotal |

**Question types:**
- SQL, from basic grouping and CASE to harder analytical queries; a 2025 analyst report describes a 40-minute SQL-heavy round with a puzzle and a guesstimate at the end (analyst role, anecdotal) [S2].
- Probability and statistics puzzles (conditional probability, expected value of coupon use, frequentist vs Bayesian), self-reported on a prep site, some 3-4 years old [S9].
- Case studies on recommendations or delivery-style marketplace problems [S1][U].
- Guesstimates; advice is to state assumptions and use a root-cause framework [S11].
- ML and LLM concepts: representation learning, tree models vs transformers, metrics, LLM evaluation (one anecdote) [S4].
- Coding in Python; for the ML / AI Engineer track, a prep article says the coding round tests Python and ML algorithms rather than only generic DSA [S5].

**Sample questions (illustrative):**
- A restaurant's orders fell 15% week on week in one city. How do you find the cause? [illustrative] Book 6 Part 1 (product metrics and metric drops).
- Improve the restaurant recommendation feed: pick the target, features, offline and online metrics. [S1] Book 1 Part 7 (recommender systems and ranking) and Book 6 Part 10 (end-to-end design).
- Write SQL for each city's top 3 restaurants by orders in the last 30 days, then add a week-on-week change. [illustrative] Book 3 Parts 4 and 5 (window functions).
- Two children, at least one is a boy: probability both are boys? Then: expected cost of a coupon that 30% of users redeem. [S9] Book 1 Part 1 (stats and probability basics) and Part 13 (statistics deep dive).
- Why can accuracy mislead for a rare-event classifier, and when do you prefer F1 or a precision-recall view? [S4] Book 1 Part 3 (classification metrics, class imbalance).
- How would you evaluate an LLM-based support assistant for order issues, without relying only on another LLM? [illustrative] Book 2 Part 9 (LLM evaluation) and Book 6 Part 7 (GenAI scenarios).
- Estimate how many delivery partners are needed in a city at the dinner peak. [illustrative] Book 6 Part 5 (business case studies); estimation habits from Book 6 Part 1.

**What they score:**
- Practical judgment about when and how to apply algorithms, in the Analytics India Magazine framing (snippet only) [S3].
- Clear assumptions and structured reasoning in guesstimates and root-cause cases [S11].
- SQL, Python and statistics fundamentals [S2][S15].
- Fit with a fast-moving team and ownership; the CEO has publicly framed AI use as a hiring theme for business and product leaders (undated, not specific to data science roles) [S14].
- A single anecdote does not show a formal rubric; no official scoring description found [U].

**Level notes:**
- A Naukri Code360 guide describes data scientist levels from junior to principal; level-specific expectations were not visible in the snippet [S15].
- The Dec 2022 report involved a principal data scientist as interviewer [S1].
- ML / AI Engineer: a 2026 prep article says 1-3 years of experience is preferred, with strong LLM or reinforcement learning research backgrounds considered [S5]; secondary source.

**Preparation plan (2 weeks):**
- Days 1-2: SQL windows, cohorts, funnels, retention. Book 3 Parts 4-6 and 8.
- Days 3-4: Probability and statistics. Book 1 Parts 1, 13, 14.
- Days 5-6: ML fundamentals, metrics, imbalance, boosting. Book 1 Parts 1-4.
- Days 7-8: Recommenders and ranking for a food and quick-commerce marketplace. Book 1 Part 7 and Book 6 Part 9 (domain sets, e-commerce).
- Days 9-10: Case studies and metric drops, guesstimates out loud. Book 6 Parts 1, 4, 5.
- Days 11-12: GenAI basics and evaluation if the role is ML or GenAI. Book 2 Parts 1, 6, 9; Book 6 Part 7 [G].
- Days 13-14: Python live-coding in a plain editor and two full mocks. Book 1 Part 12 and Book 6 Part 10 [G].

**Common mistakes:**
- Treating the loop as DSA only when the data-science reports describe SQL, statistics and cases [S2][S1].
- Guesstimating without stating assumptions first [S11].
- Giving a modelling answer to a case without defining the business metric [G].
- Expecting a fixed process; there is no single process for every Zomato role [S10].
- Treating one candidate's loop as the standard [G].

**Recent changes and AI-era notes:**
- Older (2022-2023): the data scientist offer report and the report of generative AI hiring intent at Zomato and Blinkit [S1][S12].
- 2025: the April 2025 Glassdoor report includes LLM basics and LLM evaluation questions (anecdotal, one report) [S4]. Zomato Limited became Eternal Limited in March 2025 [S8].
- 2026: Eternal announced an AI collaboration with OpenAI (Feb 2026) and an expanded one reported in May 2026; this is company AI strategy, not an interview-process change [S13].
- No source describes an AI-tool policy for candidates in Zomato or Eternal interviews [U].

**Sources:**
- S1: https://leetcode.com/discuss/post/3024221/zomato-data-scientist-dec22-offer . Supports: Dec 2022 data scientist offer: 20-min managerial round with a senior leader, 1-hour technical plus case study with a principal data scientist, top-college candidates may get one round (anecdotal, old); also https://leetcode.com/discuss/interview-experience/3024221/ . Seen 2026-10-31. Snippet only.
- S2: https://fr.glassdoor.ca/Entretien/Zomato-Entretien-E515676-RVW98890941.htm . Supports: Glassdoor reports in the search summary: a four-round process (2 technical, 1 case plus guesstimate, 1 HR; SQL, Python, Power BI, Google Sheets), a five-round one (3 technical, 2 screening and HR; basic SQL and Excel), and a 2025 analyst report with a SQL-heavy 40-min round; which URL holds which report was not verified (second URL https://fr.glassdoor.ca/Entretien/Zomato-Entretien-E515676-RVW97458209.htm). Anecdotal, mixed roles. Seen 2026-10-31. Snippet only.
- S3: https://analyticsindiamag.com/ai-hiring/data-science-hiring-process-at-zomato . Supports: describes the process as quite straightforward, team of 20+, emphasis on practical judgment; updated Dec 2024; step list not visible. Seen 2026-10-31. Snippet only.
- S4: https://www.glassdoor.com.ar/Entrevista/Zomato-Entrevista-E515676-RVW102050403.htm . Supports: April 2025 Roorkee-site report on representation learning, Random Forest vs Transformer inputs, F1 vs accuracy, LLM basics and evaluation (from the search summary; anecdotal, role unclear). Seen 2026-10-31. Snippet only.
- S5: https://faceprep.in/article/zomato-2026-ai-engineering-recommender-systems-for-entry-level/ . Supports: ML / AI Engineer track, 1-3 years preferred, coding round tests Python and ML algorithms, Gurugram and Bangalore (third-party prep article). Seen 2026-10-31. Snippet only.
- S6: https://www.ambitionbox.com/interviews/eternal-interview-questions/data-scientist . Supports: only one interview listed for Eternal data scientist, moderate difficulty, 2024 (thin sample). Seen 2026-10-31. Snippet only.
- S7: https://en.wikipedia.org/wiki/Eternal_Limited . Supports: Eternal Limited, formerly Zomato Limited, HQ Gurugram, four verticals (Zomato, Blinkit, Hyperpure, District). Seen 2026-10-31. Snippet only.
- S8: https://yourstory.com/2025/03/zomato-now-eternal-mca-approves-name-change . Supports: name change to Eternal approved March 2025; consumer brand names unchanged. Seen 2026-10-31. Snippet only.
- S9: https://prepfully.com/interview-questions/zomato/data-scientist?page=12 . Supports: self-reported Zomato data scientist probability and statistics questions (some 3-4 years old); site says questions are candidate-submitted. Seen 2026-10-31. Snippet only.
- S10: https://fueler.io/blog/zomato-hiring-process-how-to-get-a-job-at-zomato . Supports: no single hiring process for all roles, referrals accepted, generic Zomato process (not data science, not official); a similar generic list (online coding test, two DSA-heavy technical interviews, culture fit) appeared at https://jobrise.io/jobs/zomato/ . Seen 2026-10-31. Snippet only.
- S11: https://dataford.io/interview-guides/zomato . Supports: guesstimate and root-cause framework advice, assumption-first habit (aggregated guide, claims many candidate reports); related https://dataford.io/interview-guides/zomato/product-analyst . Seen 2026-10-31. Snippet only.
- S12: https://inc42.com/buzz/after-blinkit-zomato-starts-experimenting-generative-ai/ . Supports: Zomato reported to hire for ML, data science and NLP roles for generative AI products (older, 2023). Seen 2026-10-31. Snippet only.
- S13: https://www.restaurantindia.in/news/restaurant-india-news-eternal-expands-openai-partnership-to-boost-ai-across-zomato-and-blinkit.n15295 . Supports: Eternal expanded OpenAI collaboration (reported May 2026), earlier Feb 2026 agreement; not an interview change. Seen 2026-10-31. Snippet only.
- S14: https://www.wionews.com/india-news/ai-as-their-second-brain-zomatos-deepinder-goyal-sets-bold-new-hiring-criteria-8716903 . Supports: CEO invited business and product leaders who use AI daily; undated in snippet. Seen 2026-10-31. Snippet only.
- S15: https://www.naukri.com/code360/library/data-scientist-at-zomato . Supports: data scientist skills (R, SQL, Python, maths, probability, statistics), levels junior to principal (generic guide, updated Aug 2025). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence overall. Round names, count and durations for data science and ML roles at Zomato / Eternal are not established by any official source; most evidence is anecdotal and several years old [S1][S2].
- Do not rely on SDE reports for a data science loop; they were excluded where possible [U].
- Verify on the Eternal careers page and with the recruiter: which entity is hiring (Zomato, Blinkit, District, Hyperpure), the exact rounds, whether there is a take-home or live case, and any AI-tool rules.
- The step list of the Analytics India Magazine article was not visible; read it in full if available [S3].

### C4 PhonePe (Indian fintech unicorn)

**Evidence level:** Thin. The one data-science-specific process source is an Analytics India Magazine piece saying there are three interview rounds, with the round names cut off in the snippet [S1]. Everything else is aggregated guides, data analyst reports and software engineer reports, plus PhonePe job postings that show what the roles ask for, not how interviews run. No ML engineer or GenAI interview report was found [S2][S3][S4].

**Roles seen in sources:** Data Scientist postings at 3-5 and 6-8 years of experience [S6][S9]; Senior Decision Scientist and Manager, Trust and Safety Analytics (fraud risk) [S7][S8]; a 2026 third-party article on a fresher Data Scientist track for UPI fraud detection [S10]; Data Analyst interview reports [S3]. No applied scientist or GenAI posting found. Reports for software engineers (machine coding, system design) are the bulk of what exists and are not data science evidence [S4][S13].

**Process overview (as reported):**
1. Three rounds of interviews for data science, per the Analytics India Magazine article (Dec 2024 update); the names and content of the rounds were not visible [S1].
2. An aggregated guide describes four stages starting with an online assessment, then multiple technical rounds, at least one hiring manager discussion, and for some paths a final conversation with senior leaders for culture fit; role-agnostic [S2].
3. Data analyst reports: about four rounds, one candidate saying the first was HR; SQL, Power BI, aptitude and technical questions (analyst role, anecdotal) [S3].
4. For a data science loop, a hiring-guide site says a product, analytics or business round can cover case, metrics, SQL, product judgment or a stakeholder scenario; general guide, not PhonePe-specific [S5].
5. Software engineer loops (not data science): four to five rounds; one SDE-2 backend report lists machine coding / low-level design, DSA, high-level design and hiring manager (anecdotal) [S13][S4].
6. Timeline: a guide says 2-4 weeks from first contact to offer for engineering roles, with one candidate reporting about 3 months (SDE, anecdotal) [S4]. Data science timeline not found.
7. No single process applies to all candidates; rounds change by role, seniority and team [S5].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Online assessment or screen | Format and duration not found for DS | Aptitude, SQL or coding (analyst and generic reports) | [S2][S3] |
| Technical round(s) | Live, 1-2 rounds likely, duration not found | Algorithms, mathematics, statistics, ML foundation, Python, SQL | [S1][S6][S5] |
| Product / analytics / business round | Live discussion | Case, metrics, product judgment, stakeholder scenario | [S5] general guide |
| Hiring manager | Conversation | Projects, team fit, practical scenarios | [S2][S13] |
| Senior leader / culture | Conversation, some paths | Culture alignment | [S2] |

**Question types:**
- Algorithms, mathematics and statistics foundation; the head of data science is quoted as valuing these [S1].
- ML fundamentals and implementing algorithms at scale, Python and SQL, per the posting text [S6].
- Python, SQL, TensorFlow / PyTorch / scikit-learn familiarity and fintech or financial-services experience for senior roles [S9].
- Fraud, risk and trust-and-safety problem framing: statistical methods, predictive modelling, rules-based methods [S7][S8].
- Project deep dive; one internship report describes discussion of projects plus Python, statistics, pandas, ML and SQL scenarios (internship, thin) [U].
- For engineering-flavoured ML roles, machine coding / low-level design is reported for software engineers and may or may not apply [S4][S13].

**Sample questions (illustrative):**
- Design a model to flag fraudulent UPI transactions with very few fraud labels: features, label delay, metric, threshold. [illustrative] Book 1 Part 3 (classification metrics, imbalance, thresholding) and Book 6 Part 5 (business case studies: fraud).
- Precision fell after a rules change on a fraud model. How do you separate drift from the change? [illustrative] Book 6 Part 2 (model performance degraded) and Book 4 Part 8 (monitoring, drift).
- Write SQL for merchants whose daily transaction count dropped more than 30% against their 7-day average. [illustrative] Book 3 Part 5 (running totals, moving averages).
- Explain how you would pick a decision threshold when a false decline costs a customer and a missed fraud costs the business. [illustrative] Book 1 Part 3 (thresholding) and Book 6 Part 6 (trade-off decisions).
- Design the serving path for a real-time fraud score, including feature freshness and latency. [illustrative] Book 4 Part 9 (feature stores and streaming) and Book 1 Part 11 (ML system design).
- Walk through one project end to end: data, model choice, what failed, what you would redo. [illustrative] Book 6 Part 10 (end-to-end open scenarios).
- Implement a simple algorithm (for example logistic regression or k-means) from scratch in Python. [illustrative] Book 1 Part 1 (from-scratch code) and Part 12 (live coding).

**What they score:**
- Algorithms, mathematics and statistics foundations, technical competence, domain expertise and attitude, as the head of data science is quoted [S1].
- Implementing ML at scale in Python and SQL, from posting requirements [S6].
- Domain understanding of fintech and fraud or risk, from posting requirements [S7][S9].
- Design justification and scalability reasoning are reported for engineering rounds [S4]; whether data science rounds score this is not found [U].

**Level notes:**
- Data Scientist postings are banded by experience (3-5 years, 6-8 years) [S6][S9].
- Senior Decision Scientist and manager-level analytics titles exist in trust and safety [S7][S8].
- The 6-8 year posting is described as a more senior ML role asking for fintech experience [S9].
- Interview expectations per level not found in sources.

**Preparation plan (2 weeks):**
- Days 1-2: Statistics and probability. Book 1 Parts 1, 13, 14.
- Days 3-4: Classification metrics, imbalance, calibration, boosting. Book 1 Parts 3 and 4.
- Days 5-6: SQL windows, cohorts and funnels on transaction data. Book 3 Parts 4-6 and 8; fintech set in Book 3 Part 12.
- Days 7-8: Anomaly detection and fraud-style cases. Book 1 Part 5 and Book 6 Parts 5 and 9.
- Days 9-10: Python from-scratch ML and live coding in a plain editor. Book 1 Parts 1 and 12; Book 5 Parts 1-4 [G].
- Days 11-12: ML system design for real-time scoring. Book 1 Part 11, Book 4 Parts 6, 8, 9.
- Days 13-14: Project deep dive, hiring-manager practice and two mocks. Book 6 Parts 6 and 10 [G]; GenAI basics if the role needs it: Book 2 Parts 1, 6, 9.

**Common mistakes:**
- Preparing only machine coding because it is described for software engineers, when the data science signal is statistics and ML fundamentals [S4][S1].
- Ignoring the domain: fraud, risk and payments context is in every data science posting seen [S7][S9].
- Not being able to explain your own projects in depth [U].
- Assuming the process is fixed; it varies by role, seniority and team [S5].
- Treating one candidate's loop as the standard [G].

**Recent changes and AI-era notes:**
- Dec 2024: the Analytics India Magazine data science hiring article was last updated; it says three rounds [S1].
- Nov 2025: PhonePe announced a collaboration with OpenAI to bring ChatGPT to Indian users; this is a product partnership, not an interview change [S12].
- 2026: guides for engineering roles describe machine coding as a main filter [S4]. No source describes PhonePe's policy on candidate AI tools, or a GenAI interview round [U].
- Industry-wide, not PhonePe: one analysis reports AI and LLM questions rising in tech interviews since 2023 [S14].

**Sources:**
- S1: https://analyticsindiamag.com/data-science-hiring-process-at-phonepe/ . Supports: three interview rounds for data science (round names not visible), updated Dec 2024; head of data science values algorithms, mathematics, statistics, technical competence, domain expertise and attitude; also https://analyticsindiamag.com/ai-hiring/data-science-hiring-process-at-phonepe . Seen 2026-10-31. Snippet only.
- S2: https://dataford.io/interview-guides/phonepe . Supports: aggregated guide, four stages starting with an online assessment, technical rounds, hiring manager, senior culture conversation (role-agnostic). Seen 2026-10-31. Snippet only.
- S3: https://www.ambitionbox.com/interviews/phonepe-interview-questions/data-analyst . Supports: data analyst reports of about four rounds, SQL, Power BI, aptitude (analyst role, anecdotal). Seen 2026-10-31. Snippet only.
- S4: https://www.techprep.app/blog/phonepe-interview-process . Supports: engineering process, machine coding as primary filter, 2-4 weeks, one report of about 3 months (software engineer, not data science). Seen 2026-10-31. Snippet only.
- S5: https://hyring.com/jobseeker-toolkit/interview-questions/company/phonepe . Supports: no single process, varies by role, seniority and team; product / analytics / business round description (general guide). Seen 2026-10-31. Snippet only.
- S6: https://job-boards.greenhouse.io/phonepe/jobs/7545987003 . Supports: Data Scientist (3 to 5 years) posting, ML foundation, implementing algorithms at scale, Python and SQL. Seen 2026-10-31. Snippet only.
- S7: https://job-boards.greenhouse.io/phonepe/jobs/7450895003 . Supports: Senior Decision Scientist, T&S Analytics, fraud risk solutions with cross-functional teams. Seen 2026-10-31. Snippet only.
- S8: https://job-boards.greenhouse.io/phonepe/jobs/6523910003 . Supports: Manager, Trust and Safety Analytics, statistical methods, predictive modelling, rules-based methods. Seen 2026-10-31. Snippet only.
- S9: https://www.foundit.in/job/data-scientist-6-to-8-years-phonepe-bengaluru-bangalore-46471605 . Supports: Data Scientist (6-8 years) via Foundit, Python, SQL, TensorFlow / PyTorch / scikit-learn, fintech experience; PhonePe's own board copy https://job-boards.greenhouse.io/phonepe/jobs/6672004003 . Seen 2026-10-31. Snippet only.
- S10: https://faceprep.in/article/phonepe-ai-engineer-fresher-track-fraud-ranking-recommendations/ . Supports: April 2026 fresher Data Scientist track on UPI fraud, Bengaluru, Python and SQL focus (third-party commentary, not official). Seen 2026-10-31. Snippet only.
- S11: https://inc42.com/?p=450720 . Supports: PhonePe uses machine learning extensively for fraud detection, per its CTO (company context). Seen 2026-10-31. Snippet only.
- S12: https://www.phonepe.com/press/phonepe-announces-strategic-collaboration-with-openai-to-bring-chatgpt-to-indian-users-at-scale/ . Supports: Nov 2025 OpenAI collaboration, consumer product, not hiring. Seen 2026-10-31. Snippet only.
- S13: https://leetcode.com/discuss/post/8547106/phonepe-sde-2-backend-interview-experien-vcqt/ . Supports: SDE-2 backend report, four rounds: machine coding / LLD, DSA, HLD, hiring manager (software engineer, anecdotal). Seen 2026-10-31. Snippet only.
- S14: https://interviewquery.com/p/ai-interview-trends-tech-hiring-2025 . Supports: industry-wide rise in AI / LLM interview questions, not PhonePe-specific. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence overall. The only data-science-specific process claim is "three rounds", and its content is not visible [S1].
- Most interview detail comes from software engineer and analyst reports; treat as indicative only [S3][S4][S13].
- Verify on PhonePe's careers board and with the recruiter: round names, whether a machine-coding or take-home step applies to your role, interview length, and any AI-tool rules.
- No ML engineer, applied scientist or GenAI interview report was found; those parts of the profile are [G] or [U] extrapolation.

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

### C9 Paytm (Indian fintech; listed parent One97 Communications)

**Evidence level:** Thin. No official Paytm interview-process page appeared in any result. Evidence is two third-party guides with a 4-round, 3-5 week outline, a handful of Glassdoor reviews for non-DS roles, and job postings [S1][S2][S4]. No candidate report specific to a Paytm India data scientist or ML engineer loop was found [U].

**Roles seen in sources:** Lead Data Scientist, Noida, on Paytm's Lever page [S6]; a data scientist posting about building foundation models for risk across merchant and user journeys, date unclear [S12]; Data Scientist guides [S1][S2]; ML Engineer guide [S3]; a Senior Product Manager (AI) posting for LLM-powered products, which is a product role, not science [S9][S13]. Paytm Labs (Toronto) is a separate entity and its ML reports are only a loose signal [S5].

**Company note:** Paytm is the brand of One 97 Communications Limited, the listed parent, which listed on Indian exchanges in November 2021 [S10]. Postings and guides use "Paytm" and "One97" for the same employer.

**Process overview (as reported):**
1. Initial screening [S1].
2. Technical assessment or technical rounds: ML, Python and SQL are the most-cited areas [S1][S2][S3].
3. Project deep-dive [S1].
4. Cultural alignment or HR discussion [S1]. One Glassdoor review for a different Paytm role reports 4 rounds: two technical, one managerial, one HR (anecdotal) [S4].
5. Duration: one guide says about 3-5 weeks [S1]; a Glassdoor review says 4 weeks (anecdotal) [S4].
6. Paytm Labs Toronto ML (2019, different entity): ML phone screen, week-long take-home data and ML challenge, onsite with four people, HR (anecdotal, weak signal for India) [S5].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Initial screening | Call or short assessment | Background, role fit | [S1] |
| Technical round(s) | Live discussion and coding | ML concepts, Python, SQL | [S1][S2][S3] |
| Project deep-dive | Discussion | Your past ML work | [S1] |
| Managerial | Discussion | Fit with team, ownership | [S4] anecdotal, other role |
| HR / culture | Discussion | Values, logistics | [S1][S4] |
| Take-home (Paytm Labs only) | One-week data and ML challenge | End-to-end modelling | [S5] anecdotal |

**Question types:**
- Machine learning is the largest topic in one guide's question list [S2].
- SQL and Python/R [S2][S1].
- Production ML systems and data pipeline design [S3].
- Debugging an underperforming production model, as a sample behavioural-technical question in a guide [S1].
- Project-related and AML questions in reviews for associate roles (anecdotal) [S4].
- DSA is heavily reported for freshers and 0-2 years in a generic Noida prep blog [S11].

**Sample questions (illustrative):**
- Describe a situation where you had to debug a model that was underperforming in production. [S1] Book 4 Part 8 (monitoring) and Book 6 Part 2 (model performance degraded in production).
- Build a fraud or risk model for payment transactions with very few positive labels. Which metric do you optimise? [illustrative] Book 1 Part 1 (ML fundamentals) and Book 1 Part 3 (imbalanced data and metrics).
- Write SQL for each merchant's rolling 7-day transaction count and flag a drop of more than 30 percent. [illustrative] Book 3 Part 5 (running totals, moving averages).
- Design a pipeline that scores transactions in near real time and falls back safely if the model is slow. [S3] Book 1 Part 11 (ML system design) and Book 4 Part 12.
- Walk me through the hardest ML project on your resume, including what you would change. [S1] Book 6 Part 10 (end-to-end open scenarios).
- Design an A/B test for a new cashback offer where users interact with each other. [illustrative] Book 1 Part 10 (A/B testing) and Book 6 Part 4 (experiment design).
- Explain how you would evaluate an LLM assistant that answers payment-support queries. [illustrative] Book 2 Part 9 (RAG evaluation) and Book 2 Part 12.

**What they score:**
- No published rubric [U].
- Technical depth in ML, Python and SQL, from the topic mix in guides [S1][S2].
- Ability to explain real project work, from the deep-dive stage [S1].
- Production awareness, from the pipeline and deployment themes [S3].
- Postings for AI/ML work stress scalable ML workflows with big-data tools such as Kafka and Flink [S6].

**Level notes:**
- Lead Data Scientist is an experienced-hire title with ML and AI leadership, and big-data exposure listed [S6].
- One guide suggests successful candidates have at least 2-4 years of experience [S1].
- The foundation-models posting asks for 4+ years and deep learning framework skills [S12].
- Other level ladders were not found [U].

**Preparation plan (2 weeks):**
- Days 1-3: SQL windows, rolling metrics, funnels. Book 3 Parts 4-6 and 8.
- Days 4-6: ML fundamentals, imbalanced data, metrics, boosting. Book 1 Parts 1-4.
- Days 7-8: Statistics and A/B testing. Book 1 Parts 10, 13, 14; Book 6 Part 4.
- Days 9-10: Python and DSA at easy-to-medium level in a plain editor. Book 5 Parts 1, 7, 9 [G].
- Days 11-12: ML system design and production monitoring. Book 1 Part 11, Book 4 Part 12.
- Day 13: GenAI and RAG basics if the role mentions LLMs. Book 2 Parts 6, 9, 12 [S9].
- Day 14: Project deep-dive rehearsal and a mock. Book 6 Part 10 [G].

**Common mistakes:**
- Assuming a fixed round count; sources give about 4 rounds for DS but differ by role [S1][S8].
- Describing projects without numbers, impact or what failed, when a deep-dive is reported [S1].
- Ignoring production and pipeline questions for an ML role [S3].
- Treating Paytm Labs Toronto reports as the India process [S5].

**Recent changes and AI-era notes:**
- Paytm job posts say AI tools may support parts of hiring, such as reviewing applications or analysing resumes, and that final hiring decisions are made by humans [S7].
- Paytm has announced a drive to add about 4,000 people through March 2027, aimed at AI, product and technology, per press reports [S9].
- No rule on candidates using AI tools in interviews was found; ask your recruiter [U].
- One third-party guide labelled 2026 says the process differs by route and role [S8].

**Sources:**
- S1. https://dataford.io/interview-guides/paytm/data-scientist : DS guide, 4 rounds, 3-5 weeks, screening, technical, project deep-dive, culture; snippet-only. Seen 2026-10-31.
- S2. https://interviewquery.com/interview-guides/paytm-data-scientist : DS guide, ML largest topic, SQL and Python focus; snippet-only. Seen 2026-10-31.
- S3. https://interviewquery.com/interview-guides/paytm-machine-learning-engineer : ML engineer guide, production ML systems and pipeline design; snippet-only. Seen 2026-10-31.
- S4. https://www.glassdoor.ie/Interview/Paytm-Interview-E1159356-RVW85129251.htm : anecdotal review for another Paytm role, 4 rounds (two technical, managerial, HR), about 4 weeks (mapping among reviews uncertain); snippet-only. Seen 2026-10-31.
- S5. https://www.glassdoor.fr/Entretien/Paytm-Labs-Entretien-E1348673-RVW47687660.htm : anecdotal 2019 Paytm Labs Toronto ML review, take-home and onsite; different entity; snippet-only. Seen 2026-10-31.
- S6. https://jobs.lever.co/paytm/a79cbfd9-fcfb-4132-bef9-0d8f6e081a67 : Lead Data Scientist posting, Noida; snippet-only. Seen 2026-10-31.
- S7. https://jobs.lever.co/paytm/9d147504-dcc7-4ee9-aa6b-4a44261f09aa/apply : Paytm posting disclosing AI tools in hiring with human final decisions; snippet-only. Seen 2026-10-31.
- S8. https://hyring.com/jobseeker-toolkit/interview-questions/company/paytm : editorial third-party guide, process varies by role; snippet-only. Seen 2026-10-31.
- S9. https://yourstory.com/ai-story/paytm-hiring-spree-ai-growth-strategy/ : press report on about 4,000 hires with AI focus; snippet-only. Seen 2026-10-31.
- S10. https://en.wikipedia.org/wiki/One97_Communications : One97 Communications as Paytm's parent, listed November 2021 (the two Wikipedia pages and news gave different dates); snippet-only. Seen 2026-10-31.
- S11. https://jobrise.io/hi/blog/paytm-engineering-interview-noida/ : generic Noida prep blog, heavy DSA for freshers; snippet-only. Seen 2026-10-31.
- S12. https://www.resumonk.com/remote-jobs/data-science-senior-data-scientist-paytm-31244 : syndicated posting for foundation models for risk, 4+ years, date unclear; snippet-only. Seen 2026-10-31.
- S13. https://jobs.lever.co/paytm/b2adc37e-e6b3-4855-9c36-65acffcea663 : Senior Product Manager (AI) posting, LLM products; snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low. Verify with your recruiter: round count and format for your team, whether coding or DSA is part of a DS loop, whether there is a take-home, the location (Noida or elsewhere), and the policy on AI tools in interviews. No India DS/ML-specific candidate reports were found [U].
### C10 Myntra (Indian fashion e-commerce; Flipkart group)

**Evidence level:** Thin. No official Myntra interview page appeared. Evidence is an AmbitionBox summary, two Glassdoor snippets, a Dataford guide, and job postings; round counts conflict from 2 to about 6 and most detailed reports are dated 2020-2021 [S1][S2][S3][S4]. No source in the results confirmed the Flipkart ownership; that comes from general knowledge [G].

**Roles seen in sources:** Data Scientist and Senior Data Scientist, Bengaluru, with GenAI exposure listed [S5][S6]; Senior Software Engineer (Machine Learning Engineer) with LLM deployment [S7]; a data science intern programme [S8]. No applied scientist interview guide was found [U].

**Process overview (as reported):**
1. Round count is unclear: AmbitionBox says usually 2 rounds, technical and case study [S1]; Glassdoor snippets mention a 2021 report of about 6 rounds (anecdotal) [S2].
2. Coding test with easy arrays and sequence-sum questions plus some ML questions, reported by one candidate (anecdotal) [S1].
3. Technical interview on ML concepts and your projects: ROC-AUC, precision and recall, k-NN, loss functions (anecdotal) [S2][S3].
4. Case study, listed as a common round [S1].
5. Managerial or HR conversation [G].
6. Duration: one Bengaluru candidate (September 2025) said about four weeks (anecdotal) [S2]; another said 3 days [U].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Coding test | Online or live | Easy arrays, sequences; some ML | [S1] anecdotal |
| Technical | Interview | ML basics, metrics, project depth | [S2][S3] anecdotal |
| Case study | Discussion or take-home, format not stated | Applied problem solving | [S1] |
| Managerial / HR | Discussion | Fit, expectations | [G] |

**Question types:**
- Core ML concepts: ROC-AUC, precision and recall, k-NN, loss functions [S2][S3][S4].
- Python and standard libraries (Pandas, NumPy, scikit-learn) listed as must-have in a guide [S4].
- Project depth: "deep concepts related to the projects" in a Bengaluru report (anecdotal) [S3].
- Production deployment and ML orchestration, from postings (Airflow, Kubeflow, MLflow) [S6][S7].
- GenAI: prompt engineering, evaluation, deployment, and serving tools such as vLLM or TGI, from postings [S5][S7].
- Domain areas named in postings: recommendation, computer vision, supply chain optimisation [S9].

**Sample questions (illustrative):**
- Explain ROC-AUC and when precision-recall is the better view. [S2] Book 1 Part 3 (metrics and imbalanced data).
- Build a "similar products" recommender for a fashion catalogue and evaluate it offline. [illustrative] Book 1 Part 7 (ranking and recommendation).
- How would you detect a defect or wrong attribute in product images? [illustrative] Book 1 Part 1 (ML fundamentals) and Book 2 Part 1 (model internals).
- Compare k-NN with a gradient boosted model for size recommendation. [S3] Book 1 Parts 1-4.
- Deploy an LLM for product descriptions: serving, evaluation, cost. [S7] Book 2 Parts 6 and 12 and Book 4 Part 12.
- Design an A/B test for a new search ranking in a sale period. [illustrative] Book 1 Part 10 and Book 6 Part 4.
- Write SQL for the return rate by brand and size over rolling 30 days. [illustrative] Book 3 Part 5 (moving averages).
- Walk through a past project end to end, including what failed. [S3] Book 6 Part 10.

**What they score:**
- No published rubric [U].
- ML fundamentals and evaluation metrics, from the question mix [S2][S4].
- Production ability: deploying models, orchestration, serving [S6][S7].
- Fashion e-commerce applied sense: recommendation, vision, supply chain, from posting language [S9].
- A third-party guide says applied roles are judged on deploying and maintaining models in production [S4].

**Level notes:**
- Titles seen: Data Scientist, Senior Data Scientist, Senior Software Engineer (ML) [S5][S6][S7].
- A Senior Data Scientist posting asks for at least 2 years as an ML engineer or similar and production deployment experience [S6].
- Levels beyond this were not found [U].

**Preparation plan (2 weeks):**
- Days 1-3: ML fundamentals, metrics, boosting, k-NN. Book 1 Parts 1-4.
- Days 4-5: Recommenders and ranking. Book 1 Part 7.
- Days 6-7: Python coding at easy level plus SQL windows. Book 5 Parts 1, 7 and Book 3 Parts 4-6 [G].
- Days 8-9: A/B testing and case-study framing. Book 1 Part 10, Book 6 Parts 4-5.
- Days 10-11: Deployment, orchestration, monitoring. Book 4 Part 12 [S6].
- Days 12-13: GenAI, evaluation, serving. Book 2 Parts 6, 9, 12 [S5][S7].
- Day 14: Project narrative rehearsal and a mock. Book 6 Part 10 [G].

**Common mistakes:**
- Planning for one round structure when sources range from 2 to about 6 [S1][S2].
- Knowing metric definitions but not when each is misleading [S2].
- Relying on 2020-2021 reports as the current process [U].
- Ignoring deployment and orchestration for a senior role [S6][S7].

**Recent changes and AI-era notes:**
- Current postings ask about LLMs and GenAI: prompt engineering, evaluation, deployment, GPU serving [S5][S7].
- No Myntra statement on AI use in recruiting, and no policy on candidates using AI tools, was found [U].
- A Prepfully "test with AI interviewer" feature is a candidate prep tool, not Myntra practice [S10].
- Myntra's 2024 data-platform talk describes personalisation, search and recommendation services fed by more than 1k data pipelines [S11].

**Sources:**
- S1. https://www.ambitionbox.com/interviews/myntra-interview-questions/data-scientist : AmbitionBox DS summary, usually 2 rounds (technical, case study), a coding-test report; snippet-only. Seen 2026-10-31.
- S2. https://www.glassdoor.com.hk/Interview/Myntra-Interview-E508705-RVW54486058.htm : anecdotal review, conceptual ML questions, round count and Bengaluru September 2025 timing as described in the search summary (attribution among Glassdoor URLs uncertain); snippet-only. Seen 2026-10-31.
- S3. https://static.glassdoor.co.in/Interview/Myntra-Interview-E508705-RVW79729159.htm : anecdotal review, k-NN, AUC, precision-recall, loss function questions; snippet-only. Seen 2026-10-31.
- S4. https://dataford.io/interview-guides/myntra/data-scientist : DS guide, Python libraries, metrics, production themes; snippet-only. Seen 2026-10-31.
- S5. https://builtinbengaluru.in/job/data-scientist/3959345 : Data Scientist posting, Bengaluru, LLM and GenAI understanding; undated; snippet-only. Seen 2026-10-31.
- S6. https://builtin.com/job/senior-data-scientist/2811581 : Senior Data Scientist posting, orchestration, production, GenAI exposure; undated; snippet-only. Seen 2026-10-31.
- S7. https://nodeflair.com/jobs/myntra-senior-software-engineer-machine-learning-engineer-496462 : Senior SWE (MLE) posting, LLM, VLM deployment on GPUs, vLLM or TGI; snippet-only. Seen 2026-10-31.
- S8. https://nodeflair.com/jobs/myntra-pheonix-intern-data-science-535723 : data science intern posting with GenAI exposure; snippet-only. Seen 2026-10-31.
- S9. https://builtin.com/job/data-scientist/2530478 : Data Scientist posting, ML orchestration and GenAI; team scope (recommendation, vision, supply chain) came from a Myntra listing in the search summary, exact URL uncertain; snippet-only. Seen 2026-10-31.
- S10. https://prepfully.com/interview-questions/myntra/data-scientist?page=7 : Prepfully question bank with AI interviewer practice feature; snippet-only. Seen 2026-10-31.
- S11. https://microsites.databricks.com/sites/default/files/dais/2024/D241805L_Data + AI Summit 2024 - Myntra (1)_1717699026100001hoHv.pdf : Myntra Data + AI Summit 2024 deck, platform and 1k pipelines; snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low. Verify with your recruiter: round count and format, whether there is a coding test or case study, the Flipkart-group hiring process if your offer route goes through it [U], India location details, and the policy on AI tools. No 2025-2026 loop description for ML or applied scientist roles was found [U].

