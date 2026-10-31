### C1 Walmart (global retailer; India captive centre: Walmart Global Tech India)

**Entity note:** Walmart Inc. is the global retailer. Walmart Global Tech is its technology organisation, and "Walmart Global Tech India" is the India captive centre with a Bengaluru hub and a second centre reported in Chennai [S12][S13]. Many search results are Glassdoor pages for the global company or for US locations (Bentonville, Sunnyvale, Toronto). Each claim below says which one it refers to. India-specific content is thin.

**Evidence level:** Thin. There is no official Walmart process page for data science or ML roles (the careers page found is generic and says Walmart uses behavioural interviews [S11]). India reports are a handful of anecdotes, prep-site templates are generic, and several snippets conflict on round counts [S1][S4][S5][S7].

**Roles seen in sources:** Data Scientist, Senior and Staff Data Scientist (India postings, Bengaluru) [S10][S2]; Senior Data Scientist, GenAI Platform; Machine Learning Engineer [S8][S9]; Research Scientist (guide only) [S4]; AI Engineer (guide only) [S15].

**Process overview (as reported):**
1. Recruiter or HR phone screen, then an online assessment: one-hour HackerRank coding in one guide [S5]. A US Glassdoor aggregate lists a skills test, phone screen and group panel; reports also mention a SQL HackerRank test or a 24-hour take-home (US and Toronto mixed in, anecdotal) [S6].
2. Technical rounds. One India Data Scientist candidate wrote of 4 rounds (3 technical plus 1 hiring manager), and a further technical round with a Staff data scientist after HR had asked for documents (anecdotal) [S1]. A 2021 Bengaluru review said 5 rounds, 4 technical and 1 managerial (anecdotal, old) [S7].
3. A recent Glassdoor process listing (location not shown, anecdotal): resume shortlisting, HR screen, online assessment, project deep dive, multiple coding rounds at easy-medium level, ML breadth and depth, ML case study or design (tied to IN3/IN4 levels), hiring manager [S16].
4. Bengaluru ML engineer report, April 2025 (anecdotal): round 1 coding and big-data fundamentals, round 2 ML system design [S7].
5. Staff level, Bengaluru, January 2025 (anecdotal): four technical ML design rounds; a Staff candidate was asked to design a catalogue policy-violation detection system [S16].
6. Duration: about 4-8 weeks in one guide [S5]; about 17 days in India in another guide citing Glassdoor [S3]. Duration varies; treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / HR screen | Call | Fit, background | [S5][S16] |
| Online assessment | HackerRank, about 1 hour in one guide; SQL or take-home in other reports | Coding, SQL, stats | [S5][S6] anecdotal |
| Coding rounds | Live, easy-medium level | Data structures, Python | [S16][S7] anecdotal |
| Project deep dive | Interview | Your resume projects and design choices | [S16] anecdotal |
| ML breadth and depth | Interview | Fundamentals, algorithms | [S16][S1] anecdotal |
| ML case study / system design | Interview | Retail or catalogue style ML design | [S16][S7] anecdotal |
| Hiring manager | Interview | Fit, behaviour | [S1][S16][S4] |

**Question types:**
- ML engineering and fundamentals; a candidate asked whether to prioritise coding or ML algorithms for a first ML-engineering round [S1].
- Python and pandas, logistic regression, R-squared, clustering, missing data (Glassdoor aggregate, mixed locations, anecdotal) [S6].
- Resume project and design-choice questions (Data Scientist III, March 2025, anecdotal) [S16].
- ML system design for retail or catalogue problems [S16][S8].
- GenAI and deep learning questions (Bentonville Data Scientist, July 2025, US, anecdotal) [S16]; a 2026 guide says GenAI/LLM questions now appear alongside fundamentals [S10].
- Behavioural, with past examples [S11][S4].

**Sample questions (illustrative):**
- Design a system to detect catalogue-policy violations in product listings. [S16] Book 1 Part 11 (ML system design) and Book 4 Part 12 (MLOps system design).
- Walk me through a model project on your resume and why you chose that design. [S16] Book 6 Part 10 ("design a solution end-to-end" scenarios).
- Write a SQL query for top-selling items per store with a running 4-week total. [illustrative] Book 3 Part 4 (window functions: ranking, top-N) and Part 5 (running totals, moving averages).
- Explain precision versus recall and how you would pick a threshold for flagging bad listings. [illustrative] Book 1 Part 3 (classification metrics, imbalance, thresholding).
- Forecast weekly demand for a product with promotions. [illustrative] Book 1 Part 6 (time series and forecasting).
- Build a RAG assistant over product documents and say how you would evaluate it and add guardrails. [illustrative] Book 2 Part 6 (RAG basics), Part 9 (LLM evaluation) and Part 5 (alignment, safety, guardrails).
- Solve an easy-medium array or string problem in Python and state complexity. [illustrative] Book 5 Part 1 (arrays and hashing) and Part 3 (strings).
- Tell me about a time a stakeholder disagreed with your model's recommendation. [illustrative] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).

**What they score:**
- Coding ability at easy-medium level, with MLE candidates held to the same coding bar as software engineers in one guide [S8][S16].
- ML breadth and depth, and the ability to explain your own projects [S16].
- ML design for retail-style problems [S16][S8].
- Behavioural fit; Walmart's careers page says it uses behavioural interviews, so prepare specific past examples [S11].
- For senior GenAI roles, postings emphasise owning production GenAI systems and evaluation strategy including red-teaming and guardrails [S10].

**Level notes:**
- India postings seen: Data Scientist III, Senior Data Scientist, Staff Data Scientist [S10]. One Glassdoor listing ties the ML case study to IN3 and IN4 levels [S16].
- Senior: end-to-end design, development and operation of production GenAI, agentic and ML systems [S10]. Staff: technical direction for GenAI initiatives, including agents built with RAG and orchestration frameworks [S10].
- Staff candidates report several ML design rounds (anecdotal) [S16].

**Preparation plan (2 weeks):**
- Days 1-2: Python and SQL basics; window functions. Book 3 Parts 4-5; Book 5 Parts 1 and 3.
- Days 3-4: Coding at easy-medium level in a plain editor. Book 5 Parts 2, 4, 7 [G].
- Days 5-6: ML fundamentals and metrics. Book 1 Parts 2-4.
- Days 7-8: Forecasting and recommenders for retail. Book 1 Parts 6-7.
- Days 9-10: Prepare two project deep dives with design trade-offs. Book 6 Part 10.
- Days 11-12: ML system design and MLOps. Book 1 Part 11; Book 4 Parts 8 and 12.
- Days 13-14: GenAI (RAG, evaluation, agents) if the role is GenAI, plus behavioural stories. Book 2 Parts 6, 8, 9; Book 6 Part 6.

**Common mistakes:**
- Treating a single anecdote or the prep-site template as the process [S4][S1].
- Being unable to explain design choices in your own resume projects [S16].
- Skipping coding practice because the title is data scientist; reports include multiple coding rounds [S16][S7].
- Giving generic GenAI answers without evaluation or guardrails, when postings name both [S10].
- Not asking the recruiter which round formats and tools apply [G].

**Recent changes and AI-era notes:**
- 2026 guide: GenAI and LLM questions now appear in technical conversations (secondhand, India DS) [S10].
- One candidate (location not shown) reported a HackerRank assessment with a debugging task where an AI assistant was available; a guide describes Karat-run coding rounds. Both are unofficial; no company-wide AI-use policy was found [S15][S14].
- A 2026 Glassdoor report mentions a question about how the candidate uses AI day to day (single anecdote) [S15].
- April 2025: a second India centre in Chennai was reported, with focus on data engineering, AI, cloud and cybersecurity [S13]. Older: 2021 five-round Bengaluru report [S7].

**Sources:**
- S1: https://www.fishbowlapp.com/post/hi-fishes-recently-i-completed-4-3-technical-1-hiring-manager-rounds-of-interview-for-data-scientist-position-hr-asked . Supports: Walmart Global Tech India Data Scientist, 3 technical plus 1 hiring manager rounds, extra Staff-level round; separate post asked about the first ML-engineering round (anecdotal). Seen 2026-10-31. Snippet only.
- S2: https://www.fishbowlapp.com/post/hello-to-all-i-have-an-interview-lined-up-with-walmart-global-tech-for-the-position-of-staff-data-scientist-does-anyone-oh9w-5 . Supports: a Staff Data Scientist candidate thread at Walmart Global Tech (question only; no answers seen). Seen 2026-10-31. Snippet only.
- S3: https://claveprep.com/blog/walmart-global-tech-india-interview-preparation-2026 . Supports: India prep guide; about 17 days application-to-offer citing Glassdoor. Seen 2026-10-31. Snippet only.
- S4: https://interviewkickstart.com/blogs/companies/walmart-data-scientist-interview-process . Supports: paid-prep template: 3-4 onsite rounds, 1-2 coding, 1-2 domain, 1 behavioural; generic, not confirmed Walmart practice. Seen 2026-10-31. Snippet only.
- S5: https://tryexponent.com/blog/walmart-interview-process . Supports: recruiter call, one-hour HackerRank assessment, 3-5 loops, about 4-8 weeks (global company guide). Seen 2026-10-31. Snippet only.
- S6: https://static.glassdoor.ca/Interview/Walmart-Data-Scientist-Interview-Questions-EI_IE715.0,7_KO8,22.htm . Supports: Walmart (global) Data Scientist aggregate: skills test, phone screen, panel, SQL test, take-home; topics Python/pandas, regression, clustering; reports 2015 to 2026 from US, Toronto and Bengaluru (anecdotal; page-to-detail match from a summary of several Glassdoor results). Seen 2026-10-31. Snippet only.
- S7: https://www.glassdoor.com.mx/Entrevista/Walmart-Global-Tech-Entrevista-E3293060-RVW96433682.htm . Supports: Bengaluru ML engineer report April 2025 (coding and big data, then ML system design) and a 2021 five-round Bengaluru report; both from a summary of several Glassdoor results, so page-to-detail match is uncertain (anecdotal). Seen 2026-10-31. Snippet only.
- S8: https://codemia.io/guides/walmart-machine-learning-engineer . Supports: 2026 MLE guide: recruiter, phone coding, onsite coding, ML system design, ML depth; same coding bar as SWE (third party). Seen 2026-10-31. Snippet only.
- S9: https://dataford.io/interview-guides/walmart-global-tech/machine-learning-engineer . Supports: guide grouping rounds into coding, ML design, behavioural/hiring manager (third party). Seen 2026-10-31. Snippet only.
- S10: https://jobs.anitab.org/companies/walmart/jobs/92686797-ind-senior-data-scientist . Supports: India (Bengaluru) Senior Data Scientist posting: production GenAI, agentic and ML systems, evaluation, red-teaming, guardrails; related Staff and Data Scientist III listings and a 2026 guide remark on GenAI questions came from the same search summary. Seen 2026-10-31. Snippet only.
- S11: https://careers.walmart.com/how-to-prepare-for-a-walmart-interview . Supports: official generic page: Walmart uses behavioural interviews, prepare specific examples (not specific to data science). Seen 2026-10-31. Snippet only.
- S12: https://www.businessofgcc.com/gcc-data/companies/walmart-india-bangalore . Supports: Walmart Global Tech India GCC profile listing ML/AI as a hiring area (undated, third party). Seen 2026-10-31. Snippet only.
- S13: https://english.punjabkesari.com/india/2025/04/17/walmart-expands-in-india-with-new-tech-hub-in-chennai . Supports: April 2025 report of a Chennai tech hub complementing Bengaluru. Seen 2026-10-31. Snippet only.
- S14: https://interviewkickstart.com/blogs/interview-questions/walmart-interview-questions . Supports: guide describing 2-3 Karat coding rounds in an AI environment (third party). Seen 2026-10-31. Snippet only.
- S15: https://www.lockedinai.com/company-details/WMT . Supports: single anecdote on AI use in the interview, June 2026; HackerRank-with-AI-assistant and AI-usage question anecdotes came from the same search summary of Glassdoor and aggregator results. Seen 2026-10-31. Snippet only.
- S16: https://www.glassdoor.com.mx/Entrevista/Walmart-Global-Tech-Entrevista-E3293060-RVW95815953.htm . Supports: Walmart Global Tech Glassdoor reports 2025 (process list, Data Scientist III project question, Bengaluru Staff design rounds, Bentonville GenAI questions); details from a summary of several Glassdoor results, so page-to-detail match is uncertain (anecdotal). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence in round counts and order; reports differ by level, location and year [S1][S4][S7][S16].
- Several snippets mix Walmart (global, US) and Walmart Global Tech India; do not assume US reports match India [S6][S16].
- Verify with the recruiter: which rounds apply to your level, which city (Bengaluru or Chennai), whether the assessment allows AI tools, and whether a take-home applies [S15][S14].
- No claim here that any question will be asked.

### C2 Target (global retailer; India captive centre: Target in India / Target Corporation India)

**Entity note:** Target Corporation is the US retailer. "Target in India" (Target Corporation India Pvt Ltd) is its Bengaluru captive centre, with technology, merchandising, store design, marketing and finance functions [S9]. Most interview snippets are Glassdoor pages for "Target" that name Bengaluru in the review text; the company page itself is the global one, so India attribution rests on the location written in each review. Target's own interview guide is for corporate roles in general [S5].

**Evidence level:** Thin. No official process page for data science or ML roles exists in the results; evidence is a small set of Bengaluru Glassdoor reviews (2018 to 2026, mixed levels), one prep-site outline that shows only its first round, and India job postings [S1][S2][S4][S7].

**Roles seen in sources:** Data Scientist, Senior Data Scientist, Lead Data Scientist (reviews) [S1][S3]; Senior Data Scientist, Advanced Machine Learning, with a GenAI platform focus (posting) [S7]; Lead Data Scientist, Item Science (posting) [S8]; Senior Engineer AI/ML and Senior AI Engineer (postings) [S10]; AI engineer interview report, May 2025 (no detail) [S3].

**Process overview (as reported):**
1. Prep-site outline: four rounds for the data scientist process, opening with a recruiter phone screen on soft skills; the rest were not visible in the snippet [S4].
2. Bengaluru Lead Data Scientist review (anecdotal): one exploratory round, four technical rounds, then a managerial and an HR round [S1].
3. Bengaluru Data Scientist review, September 2025 (anecdotal): three rounds; round 1 in the office on DSA problem solving, rounds 2 and 4 over Zoom on machine learning and data science problem solving, each 30 minutes to 1 hour [S3].
4. Another review describes five to six rounds with data science, DSA and statistics questions [S1]. A senior review reports SQL, PySpark and Python coding and later a bar raiser round and an HR round (2025, anecdotal) [S11].
5. A December 2025 Bengaluru report describes DSA and MLOps-related rounds (anecdotal) [S2].
6. Timelines reported vary: 2 weeks and 4 weeks in two Bengaluru reviews (anecdotal) [S3][S1].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Phone | Soft skills, fit | [S4] |
| Exploratory round (lead level) | Interview | Background, experience | [S1] anecdotal |
| DSA round | In office (one report) | Data structures and algorithms | [S3] anecdotal |
| ML / data science rounds | Zoom, 30 min to 1 hour | ML fundamentals, problem solving, statistics | [S3][S1] anecdotal |
| MLOps round | Interview | MLOps-related questions | [S2] anecdotal |
| Senior coding | Interview | SQL, PySpark, Python | [S11] anecdotal |
| Bar raiser | Interview | Not described in snippet | [S11] anecdotal |
| Managerial and HR | Interview | Fit, behaviour | [S1][S11] anecdotal |

**Question types:**
- Probability, statistics and puzzles; data mining; retail case studies; ML questions (Lead and Data Scientist reviews, anecdotal) [S1][S11].
- ML topics: logistic regression, evaluation metrics, decision trees, optimisation, k-nearest neighbours, overfitting, regression and cost function (anecdotal, locations vary) [S11][S3].
- Supply chain planning approach, reported in Bengaluru reviews in 2025 and 2026 (anecdotal) [S3][S11].
- Explaining BERT and transformers (one review, possibly an analyst interview, anecdotal) [S3].
- Past-project discussion and what you would do differently; prioritising deadlines (anecdotal) [S11].
- SQL, PySpark and Python coding for senior roles [S11].

**Sample questions (illustrative):**
- How would you approach a supply chain planning problem such as store replenishment? [S3] Book 6 Part 5 (business case studies: pricing, churn, fraud, supply chain).
- How do you prevent overfitting, and how would you tell it is happening? [S11] Book 1 Part 2 (regression, regularization) and Part 4 (trees and boosting).
- Explain what a cost function is for regression and compare two loss choices. [S11] Book 1 Part 2 (linear and logistic regression, regularization).
- Explain how BERT differs from a plain transformer encoder and when you would fine-tune it. [S3] Book 1 Part 9 (NLP and CV) and Book 2 Part 4 (fine-tuning).
- Write PySpark or SQL to find the top 3 products per category by weekly sales. [illustrative] Book 3 Part 4 (window functions, top-N per group); Book 4 Part 9 (feature stores, streaming, Spark).
- Forecast promotion lift for an item and say how you would validate it. [illustrative] Book 1 Part 6 (time series) and Book 1 Part 10 (A/B testing, causal inference).
- Solve an array or graph problem and explain complexity. [illustrative] Book 5 Part 1 (arrays and hashing) and Part 9 (graphs).
- Describe a past project and what you would do differently. [S11] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).

**What they score:**
- DSA fundamentals, since reports describe a dedicated DSA round [S3][S2].
- ML and statistics depth, with an expectation of knowing your own answers "in great detail" (one reviewer, anecdotal) [S3].
- Retail-domain problem solving such as supply chain and item-level forecasting [S3][S8].
- Behavioural and managerial fit, in line with Target's official guidance to prepare examples and learn its values [S5].
- For GenAI-leaning postings: programmatic use of GenAI/LLMs, responsible-AI standards, deep learning in PyTorch or TensorFlow [S7].

**Level notes:**
- Levels seen in reviews and postings: Data Scientist, Senior, Lead; postings also show Principal Data Scientist and Senior Engineer titles [S1][S7][S10].
- A Senior AI/ML posting expects about 4 years of experience and strong Scala or Python/PySpark, with a promotion forecasting and optimisation team named [S10].
- Lead roles in Item Science list GenAI, LLMs, computer vision, classical ML, deep learning and agentic workflows [S8].

**Preparation plan (2 weeks):**
- Days 1-2: DSA warm-up in a plain editor. Book 5 Parts 1, 2, 9 [G].
- Days 3-4: SQL and PySpark-style problems. Book 3 Parts 4-5; Book 4 Part 9.
- Days 5-6: Statistics, probability and puzzles. Book 1 Parts 13-14.
- Days 7-8: ML fundamentals, regularization, trees. Book 1 Parts 2-4.
- Days 9-10: Forecasting, supply chain and retail cases. Book 1 Part 6; Book 6 Part 5.
- Days 11-12: MLOps and GenAI as the role requires. Book 4 Parts 5, 8; Book 2 Parts 4, 6, 9.
- Days 13-14: Project walk-through and behavioural stories. Book 6 Parts 6 and 10.

**Common mistakes:**
- Preparing only ML theory when reports describe a DSA round [S3][S2].
- Being vague about details of your own projects, since interviewers reportedly probe depth [S3][S11].
- Mixing up roles when reading prep guides: some Interview Query pages are for analyst or engineer roles with different round counts [S4].
- Treating one candidate's loop as the standard [G].
- Responding to unofficial postings; Target says it asks candidates to apply only through its own sites or Workday [S7].

**Recent changes and AI-era notes:**
- No source found describing AI tools allowed or banned in Target interviews, or an AI-era change to the loop. Do not assume either way [U].
- Postings in Bengaluru increasingly list GenAI, LLM, RAG and agentic experience for senior and lead roles [S7][S8].
- A July 2026 report says about 40 per cent of Target's global technology workforce is in Bengaluru [S9].
- Older: the 2018-2021 reviews and a 2021 Blind post (an interviewer preferring R) may not reflect today [S6].

**Sources:**
- S1: https://www.glassdoor.fr/Entretien/Target-Entretien-E194-RVW88532261.htm . Supports: Bengaluru Lead Data Scientist review (1 exploratory, 4 technical, managerial and HR) and a 5-6 round report; match from a summary of several Glassdoor results, so page-to-detail match is uncertain (anecdotal). Seen 2026-10-31. Snippet only.
- S2: https://static.glassdoor.co.uk/Interview/Target-Data-Scientist-Interview-Questions-EI_IE194.0,6_KO7,21.htm . Supports: Bengaluru review, Dec 2025, DSA and MLOps-related rounds (anecdotal). Seen 2026-10-31. Snippet only.
- S3: https://www.glassdoor.ie/Interview/Target-Interview-E194-RVW66404884.htm . Supports: Bengaluru Data Scientist report, Sept 2025: 3 rounds (DSA in office, two Zoom ML rounds), supply chain question, "know everything in detail" remark, AI engineer May 2025; detail from a summary of several Glassdoor results, so mapping is uncertain (anecdotal). Seen 2026-10-31. Snippet only.
- S4: https://interviewquery.com/interview-guides/target-data-scientist . Supports: four-round outline opening with a recruiter soft-skills screen; other rounds not visible (third party). Seen 2026-10-31. Snippet only.
- S5: https://corporate.target.com/careers/interview-prep-guide . Supports: official generic corporate interview guide: tips are suggestions, review the posting, learn culture and values, ask the recruiter about process or accommodations. Seen 2026-10-31. Snippet only.
- S6: https://www.teamblind.com/post/senior-data-scientist-role-at-target-india-yfnho5ec . Supports: 2021 Blind thread on a Target India senior role (interviewer preferred R; anecdotal, old). Seen 2026-10-31. Snippet only.
- S7: https://indiajobs.target.com/job/bengaluru/sr-data-scientist-advanced-machine-learning/34386/80036929168 . Supports: Bengaluru Senior Data Scientist, Advanced Machine Learning posting (GenAI platform team, Python/SQL/Hive, PyTorch or TensorFlow, responsible AI); note on applying only via official sites came from the same search summary. Seen 2026-10-31. Snippet only.
- S8: https://apna.co/job/bengaluru/lead-data-scientist-item-science-1862206888 . Supports: Target Corporation India Lead Data Scientist, Item Science listing (GenAI, LLMs, CV, agentic workflows; third-party job board). Seen 2026-10-31. Snippet only.
- S9: https://www.hrkatha.com/news/40-of-targets-global-tech-workforce-now-based-in-bengaluru/ . Supports: Target India footprint and functions, Bengaluru share of Target's tech workforce (July 2026 per search summary). Seen 2026-10-31. Snippet only.
- S10: https://indiajobs.target.com/job/bengaluru/sr-engineer-ai-ml/34386/83236151520 . Supports: Bengaluru Senior Engineer AI/ML posting (about 4 years experience, Scala or Python/PySpark, promotion forecasting team). Seen 2026-10-31. Snippet only.
- S11: https://www.glassdoor.com.br/Entrevista/Target-Entrevista-E194-RVW104316457.htm . Supports: Bengaluru senior and lead reports (SQL/PySpark/Python, bar raiser, HR; ML topics; April 2026 supply chain question; behavioural questions); details from a summary of several Glassdoor results, so mapping is uncertain (anecdotal). Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low confidence in round order and counts; the few reviews span years and levels [S1][S3][S11].
- India attribution relies on the location in review text; some snippets may include US or other-location reviews [S3].
- Verify on Target's India careers site and with your recruiter: rounds for your level, whether a DSA round is in office, and whether AI tools are permitted [S5][S7].
- No claim here that any question will be asked.
