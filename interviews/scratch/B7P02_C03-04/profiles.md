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
