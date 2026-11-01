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

# B7P03 C07-08 profiles

### C7 Mastercard (global payments network; India centres Pune, Gurugram, Mumbai)

**Entity note:** Everything below comes from the global company's careers pages, global prep guides and Glassdoor entries that mix locations. Only a few entries name Pune. No source tied a process to a named business unit (for example Services, AI Garage or Technology) except one Blind post about a Gen AI role [S8]. The Pune site is described in a company press release as a technology hub [S11]; Gurugram appears only as an office name in press coverage [S11]. Treat "India process" as unconfirmed [U].

**Evidence level:** Thin. The official pages say little about rounds, third-party guides disagree, no source describes a data science loop specific to Pune, Gurugram or Mumbai, and ML and GenAI reports are single anecdotes [S1][S5][S2].

**Roles seen in sources:** Data Scientist [S1][S4], Machine Learning Engineer [S3], Research Scientist (a different title) [S10], AI Engineer (software track) [S9], a Gen AI role in an AI group [S8], Data Analyst [S12].

**Process overview (as reported):**
1. Official position: formats differ by role; every interview has a behavioural component and an assessment of problem-solving; a recruiter can explain the format [S5][S7].
2. Data scientist, per one prep guide: four rounds, namely a test, a hiring manager round, a behavioural round and a team interview [S1].
3. Candidate reports vary: three rounds for an analyst, four rounds for a senior data scientist, four rounds where the first three were technical with case questions and the last had puzzles and behavioural questions (anecdotal) [S2][S4].
4. A Glassdoor entry mentions a written test with ML, deep learning and probability questions before discussion of resume projects (anecdotal; location and date not shown) [S3].
5. AI Engineer report (software track): online assessment, three interview rounds, then an HR discussion, with RAG and MCP a major theme (anecdotal) [S9].
6. Duration: guides say about 1-2 weeks [S1] or 3-5 weeks or longer [S7]; candidate reports range from 3 weeks to 2 months [S2]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Online test | Assessment before interviews | ML, deep learning, probability or aptitude, depending on role | [S3][S12] anecdotal |
| Hiring manager | Conversation | Resume depth, projects | [S1] |
| Technical or case rounds | Live interviews | DSA, loss functions, gradient descent, metrics, use cases | [S4][S2] anecdotal |
| Behavioural | Interview | Teamwork, working with others | [S1][S4] |
| Team interview | Interview | Fit with the team | [S1] |

**Question types:**
- Resume and project defence, such as a customer segmentation project [S1][S4].
- ML basics: loss functions, cross entropy, gradient descent, precision and recall versus threshold, CatBoost versus gradient boosting (anecdotal) [S4].
- Coding: an array problem of the Kadane type was reported by one Pune candidate (anecdotal) [S2]; bubble sort was reported for an analyst role [S12].
- Behavioural: what you learned from a junior colleague [S4].
- GenAI: RAG and MCP for an AI Engineer role [S9]; one Blind poster said a Gen AI interview with a senior AI leader had no model or coding questions, an undated anecdote [S8].

**Sample questions (illustrative):**
- How do precision and recall change as you move the decision threshold, and how would you choose one for card fraud alerts? [S4] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding).
- Explain cross entropy loss and what gradient descent does with it. [S4] Book 1 Part 8 (deep learning, backprop, optimizers).
- Find the maximum sum of a contiguous subarray. [S2] Book 5 Part 1 (arrays and hashing) and Part 10 (dynamic programming I).
- Walk me through a customer segmentation project you did, and how you validated the segments. [S4] Book 1 Part 5 (clustering, PCA, anomaly detection).
- Design a RAG assistant over internal policy documents and say how you would evaluate it. [illustrative] Book 2 Part 6 (RAG basics) and Part 9 (LLM evaluation).
- Tell me about something you learned from a junior colleague. [S4] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).
- Design a transaction fraud scoring system. [illustrative] Book 1 Part 11 (ML system design) and Book 6 Part 9 (domain sets: fintech).

**What they score:**
- Official line: behavioural fit and problem-solving [S5][S7].
- A prep guide says the interviews test whether you can defend every line on your resume [S1].
- Reviewer comments on a careers-page summary stress communication, teamwork and company values (secondhand, role mix unclear) [S7].

**Level notes:**
- Level names did not appear in snippets; one Glassdoor entry mentions a senior data scientist loop of 4 rounds [S2]. Postings exist for Data Scientist II, Lead Data Scientist and Manager, Data Scientist in Pune and elsewhere, but expectations were not in snippets [U].

**Preparation plan (2 weeks):**
- Days 1-2: ML basics, loss functions, gradient descent. Book 1 Parts 2 and 8.
- Days 3-4: Metrics, imbalance, thresholds. Book 1 Part 3.
- Days 5-6: Trees and boosting. Book 1 Part 4.
- Days 7-8: Arrays, strings, DP warm-ups. Book 5 Parts 1, 3, 10 [G].
- Days 9-10: Clustering, segmentation. Book 1 Part 5; rehearse two resume projects line by line.
- Days 11-12: GenAI basics if the role is AI-facing. Book 2 Parts 6, 8, 9.
- Days 13-14: Fintech scenarios and behavioural stories. Book 6 Parts 6 and 9; two mocks.

**Common mistakes:**
- Not being able to explain every line of your resume [S1].
- Assuming a GenAI loop will be all technical, or all non-technical; reports conflict [S8][S9].
- Using live AI help against the company's stated expectations [S6].
- Treating one candidate's loop as the standard [G].

**Recent changes and AI-era notes:**
- Mastercard's careers page on integrity in applications: candidates are asked to take part in good faith; AI is encouraged for preparation such as mock interviews; some roles may be invited to use AI in a technical assessment with rules given beforehand (search summary; read the page) [S6].
- Recent: a Sept 2026 anecdotal AI Engineer report with RAG and MCP focus [S9]. Older: the Pune hub opening in Oct 2024 [S11].

**Sources:**
- S1: https://www.interviewquery.com/guides/mastercard-data-scientist . Supports: 4 rounds (test, hiring manager, behavioural, team), resume defence, 1-2 weeks. Seen 2026-10-31. Snippet only.
- S2: https://www.glassdoor.co.in/Interview/Mastercard-Interview-E3677-RVW102163371.htm . Supports: Glassdoor Pune-tagged reports (Kadane-style coding, 3 weeks; others with no questions), via a search summary that did not show which entry carried which detail; also senior DS 4 rounds and 2 months from a general search. Seen 2026-10-31. Snippet only.
- S3: https://www.glassdoor.sg/Interview/Mastercard-Interview-E3677-RVW101500535.htm . Supports: possibly the entry with a test covering ML, DL and probability then resume projects; the search summary did not tie the detail to a specific entry. Seen 2026-10-31. Snippet only.
- S4: https://static.glassdoor.ie/Interview/Mastercard-Data-Scientist-Interview-Questions-EI_IE3677.0,10_KO11,25.htm . Supports: Data Scientist question themes (loss functions, gradient descent, cross entropy, threshold, segmentation, junior colleague). Seen 2026-10-31. Snippet only.
- S5: https://careers.mastercard.com/us/en/interview-tips . Supports: formats vary by role; behavioural component and problem-solving assessment in every interview. Seen 2026-10-31. Snippet only.
- S6: https://careers.mastercard.com/us/en/ai-guidelines . Supports: integrity expectations and AI usage guidance for candidates. Seen 2026-10-31. Snippet only.
- S7: https://careers.mastercard.com/us/en/mastercards-hiring-process . Supports: general hiring process page; third-party timeline estimates came from other results in the same search. Seen 2026-10-31. Snippet only.
- S8: https://www.teamblind.com/post/my-hilarious-interview-experience-at-mastercard-kp80tcdc . Supports: anecdote, Gen AI role, first round with a senior AI leader, no model or coding questions. Seen 2026-10-31. Snippet only.
- S9: https://leetcode.com/discuss/post/8539984/mastercard-ai-engineer-interview-experie-u5ak/ . Supports: AI Engineer (SWE-1) online assessment, 3 rounds, HR, RAG and MCP focus. Seen 2026-10-31. Snippet only.
- S10: https://dataford.io/interview-guides/mastercard/research-scientist . Supports: research scientist guide, about 5 rounds over 4-6 weeks; generic prep-site content. Seen 2026-10-31. Snippet only.
- S11: https://newsroom.mastercard.com/news/ap/en/newsroom/press-releases/en/2024/mastercard-opens-new-state-of-the-art-tech-hub-in-pune-india/ . Supports: Pune tech hub opened Oct 2024; Gurugram, Mumbai and other offices listed in coverage. Seen 2026-10-31. Snippet only.
- S12: https://www.ambitionbox.com/interviews/mastercard-interview-questions/analyst . Supports: Analyst role HR round and aptitude test; bubble sort anecdote. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium on the broad shape (test, manager, technical, behavioural), low on anything India-specific or role-specific [S1][S5].
- Verify with the recruiter: which business unit the role sits in, whether there is an online test, rounds and tools allowed, and the AI-use rules on the careers page [S6].

### C8 Intuit (financial software company; India centre Bangalore)

**Entity note:** Intuit is one company (products such as TurboTax, QuickBooks, Credit Karma, Mailchimp). Most sources are US or mixed-location. Bangalore-specific data science or ML reports are few; some snippets say Bengaluru, many do not state a location. Where a location is unknown it is marked [U].

**Evidence level:** Thin to Medium. Several prep guides and Blind and Glassdoor reports agree on the "craft demo" and SQL/Python screens, but no official Intuit process page appeared, location is often unstated, and Bangalore ML and GenAI reports are very thin [S1][S9][S5].

**Roles seen in sources:** Data Scientist [S1][S2], Staff Data Scientist and Staff AI Scientist (postings, including Bengaluru) [S11][S14], Machine Learning Engineer and Senior ML Engineer (1point3acres) [S5][S6], AI Engineer [S16], GenAI GenOS engineering roles (US postings) [S15].

**Process overview (as reported):**
1. Recruiter or hiring-manager screen of about 20 minutes on your resume [S8][S1].
2. SQL and Python screen; Bengaluru reports describe SQL and DSA-style coding (anecdotal) [S3]. An ML engineer phone screen included a project discussion and a LeetCode problem (location not shown) [S6].
3. Craft demo: a presentation round where you walk a panel through a past project or prepared case [S1]; one guide lists it as 60 minutes in the data scientist loop [S9]. Forum posters describe a 90-minute craft exercise and a classification-style ML exercise (anecdotal) [S9][S10]. A Bengaluru candidate reported a classification problem solved on-site in an hour, then presented in later rounds (anecdotal) [S4].
4. Virtual onsite of about five hours, per one guide, with "ask anything" style rounds, then decision [S8][S1].
5. A 2026 staff data scientist report: recruiter, technical screen, take-home case study, panel interview, with SQL and Python and a product case with A/B testing (anecdotal) [S11].
6. Duration: about 23-24 days in Glassdoor-based estimates [S8], 3-5 weeks or 4-8 weeks in other guides [S1][S9]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter / hiring manager | About 20 min call | Resume walk-through, experience | [S8][S1] |
| Technical screen | Live, SQL and Python | SQL, data manipulation, sometimes DSA | [S3][S11] anecdotal |
| Craft demo | Prepared case or exercise, about 60-90 min, then presentation | Applied ML, modelling choices, communication | [S9][S10][S1] |
| Virtual onsite | About 5 hours total, several rounds | Experimentation, metrics, ML, behavioural | [S8][S1] |
| ML engineer onsite | Technical, system design, behavioural | Coding, ML design | [S5] location unknown |

**Question types:**
- SQL queries, including a retention and discounts scenario for premium subscribers [S3].
- Experimentation and product metrics, A/B testing [S1][S11].
- Classification problem solving and communicating results [S4].
- Precision and recall formulas; designing a ranking system [S1].
- Communicating with technical and non-technical stakeholders; prioritising projects [S1][S3].
- Coding: DSA mediums reported for a staff role (anecdotal; another candidate said ML questions were light) [S11].
- Values: integrity and honest decisions [S1].

**Sample questions (illustrative):**
- Write SQL to find subscribers likely to lapse and who should receive a discount. [S3] Book 3 Part 6 (date/time, retention, cohorts) and Part 8 (funnels, conversion, product metrics).
- You have an hour to build a classifier on a tabular dataset, then present it: what do you show? [S4] Book 1 Part 3 (classification metrics, imbalance, calibration, thresholding) and Part 12 (NumPy/pandas/sklearn live coding).
- Design a ranking system for suggested expense categories. [S1] Book 1 Part 7 (recommenders, ranking, search).
- Design an A/B test for a new onboarding flow and choose the metrics. [S11] Book 1 Part 10 (A/B testing, causal inference) and Book 6 Part 4 (experiment design).
- Explain a past project to a non-technical panel in 10 minutes. [S1] Book 6 Part 6 (stakeholder conflicts and trade-offs).
- Extract fields from scanned tax documents with an LLM and say how you evaluate it. [illustrative] Book 2 Part 9 (LLM evaluation) and Part 6 (RAG basics).
- Build a mini RAG or agent on a small corpus, with AI tools allowed or not. [illustrative] Book 2 Part 12 (GenAI system design and coding).

**What they score:**
- Applied problem solving shown through a craft demo, not puzzles [S1][S9].
- Communication to mixed audiences [S1][S3].
- Integrity and company values, per one guide [S1].

**Level notes:**
- Postings use Staff Data Scientist, Staff AI Scientist and Staff Software Engineer (ML), plus Machine Learning Engineer 1 in Bengaluru; the Staff ML posting asks for 5+ years of production ML and the Staff AI Scientist US posting 8+ years (search summaries) [S14][S11].

**Preparation plan (2 weeks):**
- Days 1-3: SQL and pandas, cohorts, retention. Book 3 Parts 4-6 and 8.
- Days 4-5: Experimentation. Book 1 Part 10; Book 6 Part 4.
- Days 6-7: Classification, metrics, boosting. Book 1 Parts 3-4.
- Days 8-9: Practise a timed modelling exercise and a 10-minute talk. Book 1 Part 12 and Book 6 Part 10 (design a solution end-to-end).
- Days 10-11: Ranking and system design. Book 1 Parts 7 and 11.
- Days 12-13: GenAI evaluation and RAG if the role is AI-facing. Book 2 Parts 6, 9, 12.
- Day 14: Behavioural stories on integrity and stakeholders; mock. Book 6 Part 6 [G].

**Common mistakes:**
- Treating the craft demo as an interview rather than a prepared presentation of your reasoning [S1].
- Assuming a coding-light loop; DSA mediums were reported for a staff role [S11].
- Ignoring the recruiter's preparation call (secondhand advice) [S8].
- Treating a US report as the Bangalore process [U].

**Recent changes and AI-era notes:**
- Anecdotal 2025-2026 reports: take-home projects with AI allowed (software engineer), an AI prompting round in a phone screen, and an HR question on how you use AI tools [S12][S13]. No official policy was found [U].
- Intuit's GenOS platform and agentic AI push (Sept 2025 press release) suggests AI-platform roles exist, but says nothing about interviews [S15].
- Older: the craft demo format, discussed on Blind over several years [S9][S10].

**Sources:**
- S1: https://www.interviewquery.com/guides/intuit-data-scientist . Supports: about 4 rounds, craft demonstration, question types, values. Seen 2026-10-31. Snippet only.
- S2: https://codemia.io/guides/intuit-data-scientist . Supports: prep guide for the data scientist loop; second guide giving 3-5 weeks. Seen 2026-10-31. Snippet only.
- S3: https://static.glassdoor.at/Interview/Intuit-Interview-E2293-RVW81747241.htm . Supports: Bengaluru-tagged reports with SQL, DSA, discount query and stakeholder questions, from search summaries that did not tie each detail to one entry. Seen 2026-10-31. Snippet only.
- S4: https://static.glassdoor.com.ar/Interview/Intuit-Interview-E2293-RVW83063550.htm . Supports: classification problem solved on-site in an hour and presented later (Bengaluru candidate per search summary). Seen 2026-10-31. Snippet only.
- S5: https://www.1point3acres.com/interview/thread/1080120 . Supports: ML engineer onsite with technical, system design and behavioural rounds; location not shown. Seen 2026-10-31. Snippet only.
- S6: https://www.1point3acres.com/interview/thread/1085832 . Supports: ML engineer phone screen with project discussion and a LeetCode problem. Seen 2026-10-31. Snippet only.
- S7: https://www.interviewquery.com/interview-guides/intuit-machine-learning-engineer . Supports: ML engineer guide mentioning craft demo and ML system design. Seen 2026-10-31. Snippet only.
- S8: https://hyring.com/jobseeker-toolkit/interview-questions/company/intuit . Supports: 5 stages, virtual onsite about 5 hours, about 24 days, recruiter call; secondary prep site. Seen 2026-10-31. Snippet only.
- S9: https://www.teamblind.com/post/intuit-data-science-on-site-interview-craft-demo-znolepzo . Supports: data science onsite with craft demo and 90-minute exercise (anecdotal); a guide's 60-minute craft demo and 4-8 weeks came from the same search. Seen 2026-10-31. Snippet only.
- S10: https://www.teamblind.com/post/intuit-ds-machine-learning-craft-demo-p1n0wzqz . Supports: DS/ML craft demo thread, classification-style exercise (anecdotal). Seen 2026-10-31. Snippet only.
- S11: https://www.glassdoor.com.au/Interview/Intuit-Interview-E2293-RVW84655226.htm . Supports: 2026 staff data scientist reports: take-home case study, panel, SQL and Python, product case with A/B tests, DP medium (anecdotal). Seen 2026-10-31. Snippet only.
- S12: https://www.1point3acres.com/interview/thread/1171367 . Supports: HR call and take-home projects with AI allowed (software engineer, anecdotal). Seen 2026-10-31. Snippet only.
- S13: https://prachub.com/interview-experiences/intuit-software-engineer-interview-experience-phone-screen-with-an-ai-prompting-round-then-silence . Supports: AI prompting round in a phone screen (software engineer, anecdotal). Seen 2026-10-31. Snippet only.
- S14: https://jobs.intuit.com/job/bengaluru/staff-ai-scientist/27595/81001228272 . Supports: Staff AI Scientist posting in Bengaluru exists; Bengaluru ML postings on a job board gave requirements. Seen 2026-10-31. Snippet only.
- S15: https://www.businesswire.com/news/home/20250923904408/en/Intuit-Rapidly-Advances-GenOS-to-Accelerate-Development-of-Agentic-AI-Experiences-at-Scale/ . Supports: GenOS platform, Sept 2025. Seen 2026-10-31. Snippet only.
- S16: https://www.interviewquery.com/prep-guides/intuit-ai-engineer . Supports: AI Engineer guide exists; no detail used beyond role name. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium on the craft demo and SQL/Python screening being common in data science loops; low on Bangalore specifics and on ML and GenAI loops [S1][S9][S4].
- Verify with the recruiter: the craft demo brief and timing, whether AI tools are allowed, which business unit, and the round list for the Bangalore opening [U].

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
- Why healthcare and why Optum? [S7] Book 9 (soft skills) when available [G].

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

