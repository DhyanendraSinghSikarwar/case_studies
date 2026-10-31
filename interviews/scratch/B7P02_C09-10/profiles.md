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
- Describe a situation where you had to debug a model that was underperforming in production. [S1] Book 4 Part 12 (production ML monitoring) and Book 6 Part 5 (business case reasoning).
- Build a fraud or risk model for payment transactions with very few positive labels. Which metric do you optimise? [illustrative] Book 1 Part 1 (ML fundamentals) and Book 1 Part 3 (imbalanced data and metrics).
- Write SQL for each merchant's rolling 7-day transaction count and flag a drop of more than 30 percent. [illustrative] Book 3 Part 5 (running totals, moving averages).
- Design a pipeline that scores transactions in near real time and falls back safely if the model is slow. [S3] Book 1 Part 11 (ML system design) and Book 4 Part 12.
- Walk me through the hardest ML project on your resume, including what you would change. [S1] Book 6 Part 10 (project narratives).
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
