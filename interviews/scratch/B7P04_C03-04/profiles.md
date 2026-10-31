### C3 Booking.com (online travel platform; Amsterdam HQ plus other offices)

**Entity note:** Booking.com is headquartered in Amsterdam; its data science and ML postings seen are in Amsterdam, Tel Aviv and Manchester [S9][S10]. Most candidate reports below are for Amsterdam [S2][S3]; Glassdoor pages also mix in other cities and roles. Each claim names the office where the source does. No India-office reports were found.

**Evidence level:** Thin. There is an official "how we hire" page (generic timeline) and an official AI-use guide for candidates, but process detail for data science and ML roles comes from small, mixed-year anecdotal Glassdoor reports (2014 to 2026) and prep-site guides that often disagree [S1][S2][S3][S6][S7].

**Roles seen in sources:** Data Scientist (Amsterdam reports) [S1][S2]; Machine Learning Engineer (Amsterdam) [S3][S4][S8]; Machine Learning Scientist (a single report, anecdotal) [S4]; GenAI Applications roles (Machine Learning Engineer II and Senior Machine Learning Scientist, Tel Aviv postings; Senior Machine Learning Scientist on a Travel LLMs and Agentic team, Amsterdam posting), postings only with no interview detail [S9][S10].

**Process overview (as reported):**
1. Official: the recruitment process can take about 3 to 6 weeks depending on the interviews a role needs, and a pre-employment screening process exists [S6].
2. Data scientist, third-party guide: HR phone call, then an online technical test; sometimes a presentation round on a case study [S1]. One Amsterdam candidate (anecdotal): HR phone interview, a statistics and machine learning test, then a technical phone interview [S2].
3. Data scientist, anecdotal Amsterdam account: two one-hour face-to-face interviews, each with two data scientists and two business cases; a final interview with a senior data scientist and one more case [S2]. A 2025 candidate reported three rounds: technical, a role-linked business case, and company alignment (anecdotal) [S1].
4. Take-home (anecdotal, mostly older): a business case with a window of about three days, then presenting findings to the team, then a cultural fit round; follow-ups on experimentation [S2][S13]. One third-party guide calls the take-home optional [S13].
5. Machine learning engineer (anecdotal Amsterdam): an online assessment (a HackerRank coding question plus multiple-choice ML questions in a March 2024 report), an HR screen, coding rounds, and for one 2025 report a hotel-pricing design question [S3][S14]. A Glassdoor aggregate from three interviews lists LeetCode-style graphs and trees in Python, system design, then HR [S4]. A 2021 Amsterdam candidate described four rounds starting with an online ML, statistics and probability test [S4].
6. Time to hire: Glassdoor summaries of a few interviews give about 47 days for data scientists and about 30 days for ML engineers (rough, tiny samples) [S1][S4].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter or HR screen | Phone call | Fit, role match | [S1][S2][S6] |
| Online technical test | Online test | Statistics and ML basics (DS); HackerRank coding plus ML multiple choice (MLE) | [S1][S2][S3] anecdotal |
| Technical phone interview | Call | Technical depth | [S2] anecdotal |
| Business case interviews (DS) | Face to face or video, about 1 hour | Analytical reasoning on product and hotel cases, experimentation follow-ups | [S2] anecdotal |
| Take-home and presentation | Case over a few days, then team presentation | Analysis, communication | [S2][S13] anecdotal, older |
| Coding and design (MLE) | Live | Graphs and trees in Python; ML system design such as hotel pricing | [S4][S14] anecdotal |
| Company alignment or culture fit | Interview | Values and fit | [S1][S2] |

**Question types:**
- Business cases such as estimating a hotel's star rating or measuring product health [S2].
- Experimentation, including how to analyse a change in a cancellation policy and predicting days until a hotel is fully booked (candidate-reported) [S2].
- Statistics, ML and probability basics in an online test [S2][S4].
- Coding: HackerRank question, graphs and trees in Python [S3][S4].
- ML system design with a pricing flavour [S14].
- Project deep dives [S1]. Booking.com's experimentation leader said in 2018 he looks for customer impact focus and people who explain their reasoning and update when challenged (a 2018 podcast, older) [S12].

**Sample questions (illustrative):**
- Estimate a hotel's star rating from available platform data; say which features and what error you accept. [illustrative] Book 6 Part 5 (business case studies) and Book 1 Part 2 (regression, feature engineering).
- Cancellation policy changes for some properties: how do you measure the effect on bookings and on guest behaviour? [S2] Book 1 Part 10 (A/B testing, causal inference) and Book 6 Part 4 (experiment design).
- Predict how many days before a stay a property becomes fully booked. [S2] Book 1 Part 6 (time series and forecasting).
- Design a hotel pricing recommendation model: data, model, metric, serving. [S14] Book 1 Part 11 (ML system design).
- Solve a graph traversal problem in Python and state complexity. [S4] Book 5 Part 9 (graphs).
- Walk through a past project and what you would change; defend a modelling choice. [S1] Book 6 Part 6 (stakeholder conflicts and trade-offs).
- Build an agentic trip-planning assistant: retrieval, tool use, evaluation. [illustrative] Book 2 Part 8 (agents) and Book 2 Part 12 (GenAI system design).

**What they score:**
- Reasoning on business cases and how clearly you explain it [S2][S12].
- Experimentation fundamentals [S2][S12].
- Technical basics: statistics, ML, Python coding [S2][S4].
- Alignment with company values; candidates are advised to read about them (anecdotal) [S1].
- Outcomes can depend on the interviewer (one Machine Learning Scientist review, anecdotal) [S4].

**Level notes:**
- Postings show Machine Learning Engineer II and Senior Machine Learning Scientist I levels [S9][S10]; level-specific interview expectations were not found.
- One guide lists a recruiter screen, a 60-minute technical screen and a four-to-five round virtual onsite for technical roles generally, not data-science specific [S11].

**Preparation plan (2 weeks):**
- Days 1-2: Business cases and metrics. Book 6 Parts 1 and 5.
- Days 3-4: Experimentation and causal inference. Book 1 Parts 10, 13; Book 6 Part 4.
- Days 5-6: Statistics and ML basics under test conditions. Book 1 Parts 1-4 and 14.
- Days 7-8: Python coding, graphs and trees. Book 5 Parts 7 and 9; Book 1 Part 12.
- Days 9-10: Forecasting and ranking or recommenders (travel use cases). Book 1 Parts 6 and 7.
- Days 11-12: ML system design and, for GenAI roles, agents. Book 1 Part 11; Book 2 Parts 8 and 12.
- Days 13-14: Take-home practice with a short team presentation, then values stories and two mocks. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Jumping to a model before defining the business question in a case [S2][S12].
- Not preparing for experimentation follow-ups after a case [S2].
- Skipping research on how Booking.com uses ML (a 2021 candidate's advice, anecdotal) [S4].
- Using AI tools live in interviews or independent assessments, which the official guide advises against [S7].
- Treating one candidate's loop as the process [G].

**Recent changes and AI-era notes:**
- Official, recent: Booking.com publishes "How to use AI fairly and effectively in your Booking.com interviews". Using AI to practise is fine; for some technical roles it may test how you use AI in a controlled setting such as pair coding; real-time AI use in interviews, coding tasks or independent assessments is not recommended, nor is AI recording or transcription of interviews [S7]. Date of the page not shown in the snippet.
- GenAI and agentic teams are hiring (postings in Tel Aviv and Amsterdam); no interview reports for them were found [S9][S10].
- Older: take-home and presentation reports date from 2016 onwards and may no longer apply [S2][S13].

**Sources:**
- S1: https://www.interviewquery.com/interview-guides/bookingcom-data-scientist . Supports: DS stages (HR call, online test, optional presentation), 2025 three-round report, experimentation and deep dives, 47-day figure (third-party guide plus Glassdoor summary). Seen 2026-10-31. Snippet only.
- S2: https://www.glassdoor.ca/Interview/Booking-com-Interview-E256653-RVW23859925.htm . Supports: Glassdoor DS reviews (Amsterdam; two one-hour interviews with business cases; take-home with three days; cancel-policy and days-to-fully-booked prompts; anecdotal). The page-to-detail match comes from a summary of several Glassdoor results returned together. Seen 2026-10-31. Snippet only.
- S3: https://www.1point3acres.com/interview/thread/1065770 . Supports: Amsterdam MLE thread (online assessment, HR screen, coding rounds; anecdotal). Seen 2026-10-31. Snippet only.
- S4: https://static.glassdoor.nl/Interview/Booking-com-Machine-Learning-Engineer-Interview-Questions-EI_IE256653.0,11_KO12,37.htm . Supports: MLE aggregate (graphs and trees, system design, HR; about 30 days; 2021 four-round report; ML Scientist interviewer-dependence note from the search summary). Seen 2026-10-31. Snippet only.
- S5: https://www.teamblind.com/post/bookingcom-data-scientist-interview-gd2s7bvg . Supports: existence of a Blind thread on Booking.com data scientist interviews; no content seen, so nothing relies on it. Seen 2026-10-31. Snippet only.
- S6: https://careers.booking.com/how-we-hire/ . Supports: official page; about 3 to 6 weeks, pre-employment screening, interview preparation tips. Seen 2026-10-31. Snippet only.
- S7: https://careers.booking.com/candidate-ai-usage-recommendations/ . Supports: official AI-use guidance for candidates. Seen 2026-10-31. Snippet only.
- S8: https://www.interviewquery.com/interview-guides/bookingcom-machine-learning-engineer . Supports: third-party MLE guide (coding assessment, system design, culture fit, final hiring-manager or panel conversation). Seen 2026-10-31. Snippet only.
- S9: https://www.themuse.com/jobs/bookingcom/machine-learning-engineer-ii-genai-applications . Supports: GenAI Applications ML Engineer II posting (Tel Aviv per search summary). Seen 2026-10-31. Snippet only.
- S10: https://magnet.me/en/opportunity/1051919/senior-machine-learning-scientist . Supports: Senior Machine Learning Scientist posting (Amsterdam, Travel LLMs and Agentic team per search summary). Seen 2026-10-31. Snippet only.
- S11: https://www.techprep.app/blog/booking-interview-process . Supports: generic technical-role stage list (recruiter screen, 60-minute screen, virtual onsite, hiring manager); not DS-specific. Seen 2026-10-31. Snippet only.
- S12: https://www.datacamp.com/community/podcast/online-experiments-booking . Supports: 2018 podcast with Booking.com's experimentation director on hiring mindset (older). Seen 2026-10-31. Snippet only.
- S13: https://jobrise.io/en/blog/booking-com-data-scientist-resume-interview-2026/ . Supports: third-party prep guide; take-home presented to team as an optional stage, pandas and scikit-learn readiness. Seen 2026-10-31. Snippet only.
- S14: https://www.glassdoor.com.au/Interview/Booking-com-Interview-E256653-RVW65256550.htm . Supports: possibly the Feb 2025 Amsterdam hotel-pricing design report (anecdotal); page match is uncertain, from a result summary. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium confidence in the overall shape (screen, online test or take-home, case interviews, alignment); low confidence in round counts, durations and which part applies to your team [S1][S2][S4].
- India: no India-based reports found; treat as general process evidence only [S2].
- Verify on Booking.com careers: the stages for your role, whether a take-home or pair-coding exercise applies, and the current AI-use guidance [S6][S7].
- No claim here that any question will be asked.

### C4 Klarna (fintech and payments; Stockholm HQ plus other offices)

**Entity note:** Klarna is headquartered in Stockholm. Candidate reports below are mostly Stockholm, with one Berlin report and some Glassdoor pages with no city shown [S1][S8]. Each claim names the office where the source does. No India-office reports were found.

**Evidence level:** Thin. No official Klarna interview-process page appeared. Evidence is anonymous Glassdoor reports (2011 to 2026, many for other roles) and commercial prep guides that disagree on take-home length and round counts [S1][S2][S5][S6].

**Roles seen in sources:** Data Scientist [S2][S3][S5]; Machine Learning Engineer (guides only, no first-hand report found) [S4][S5]; Analytics Manager, Data Analyst and Product Analyst (adjacent roles, used for process shape only) [S1][S10]; Senior Software Engineer (Stockholm, Mar 2026 listing, no content used) [S11].

**Process overview (as reported):**
1. Early online logic or cognitive test. Stockholm anecdotes: an 18-question logic test (2018), two logic tests with strict cut-offs for a 2019 data scientist, and in a 2023 analytics-manager review a logic test, a 15-minute HR call, then the logic test again proctored [S1]. A 2026 guide gives about 15 to 30 minutes for this round [S2].
2. HR or recruiter screen [S1][S6].
3. Technical task for data science: exploratory analysis, an ML model, and deployment on a cloud provider (guide) [S3]. Anecdotes: train a credit risk model and deploy it behind an API on any cloud provider; one candidate said it took over 10 hours [S7]. Guides disagree on size: about 7 days and 10+ hours in one, a 3 to 4 hour take-home in another [S2][S5].
4. Presentation of the case and technical deep dive, plus behavioural questions (guide) [S4][S5].
5. Team and culture interviews. A Berlin report from May 2025 (anecdotal): HR, ML task, technical interview, Klarna fit interview, another technical interview, team fit [S8]. A 2019 Stockholm data scientist reported interviews with HR, a team lead and a data science lead [S1].
6. Length: reports range from two weeks to several months; a guide says up to two months; one analysis of Glassdoor data gives about 36 days [S5][S6]. Treat as rough.

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Logic or cognitive test | Online, timed | Pattern recognition, reasoning; strict cut-offs reported | [S1][S2] anecdotal |
| HR or recruiter screen | Call, about 15 to 30 minutes | Fit, motivation | [S1][S6] |
| ML case or take-home | Remote, hours to days (sources disagree) | EDA, model, cloud deployment, credit risk or similar | [S3][S7] anecdotal |
| Case presentation and technical deep dive | Interview | Explaining choices, deployment, reproducibility | [S4][S5] |
| Team and culture fit | Interviews | Fit with team; Klarna principles (bar-raiser-style round mentioned by some, mainly non-engineering) | [S6][S8] anecdotal |

**Question types:**
- Logic puzzles in an online test [S1].
- Building and deploying a credit risk model; imputing missing values (candidate-reported) [S7][S9].
- Fraud detection design and credit scoring, MLOps and fairness (guide, not confirmed) [S4].
- SQL, statistics and ML modelling categories on a question-bank site [S9].
- Behavioural and team-fit questions [S6][S8].

**Sample questions (illustrative):**
- Train a credit risk model on a messy dataset and serve it behind an API. [S7] Book 1 Part 3 (classification metrics, imbalance, calibration) and Book 4 Part 6 (serving).
- How would you impute missing values, and when is each approach risky? [S9] Book 6 Part 3 (imbalanced, noisy, missing data).
- Design a real-time fraud detection system for card and pay-later payments. [S4] Book 1 Part 11 (ML system design) and Book 6 Part 9 (domain sets, fintech).
- How would you monitor a credit scoring model after launch for drift and fairness? [S4] Book 4 Part 8 (monitoring, drift).
- Choose a decision threshold when false declines and defaults have different costs. [illustrative] Book 1 Part 3 (thresholding).
- Present your take-home to a panel and defend one modelling choice you rejected. [S5] Book 6 Part 6 (stakeholder conflicts and trade-offs).
- Write a SQL query for default rate by customer cohort. [illustrative] Book 3 Part 6 (cohorts).

**What they score:**
- Passing the logic-test cut-off first [S1].
- Hands-on ML delivery: analysis, model, deployment, shown in the take-home [S3][S7].
- Ability to explain and present your work [S4][S5].
- Team fit and values; one Stockholm reviewer said team placement may be unclear until late (anecdotal) [S6].

**Level notes:**
- Level names and expectations were not found in snippets. Guides list a five-round ML engineer process without level detail [S4].

**Preparation plan (2 weeks):**
- Days 1-2: Practise timed logic and reasoning puzzles [G].
- Days 3-4: Classification, credit risk metrics, calibration, thresholds. Book 1 Parts 3 and 4.
- Days 5-6: Messy data, imputation. Book 6 Part 3; Book 1 Part 2.
- Days 7-8: Serving and cloud deployment of a model. Book 4 Parts 6, 10 and 11.
- Days 9-10: Monitoring, drift, fairness. Book 4 Part 8; Book 6 Part 2.
- Days 11-12: Fraud and credit ML system design, SQL cohorts. Book 1 Part 11; Book 6 Part 9; Book 3 Part 6.
- Days 13-14: Build and present a mock take-home in a time box; values and team-fit stories. Book 6 Parts 6 and 10 [G].

**Common mistakes:**
- Treating the logic test as a formality when cut-offs are reported to be strict [S1].
- Underestimating the take-home: one candidate reported 10+ hours because of data exploration [S7].
- Delivering a model with no deployment or reproducibility story [S3][S4].
- Not asking the recruiter which stages remain, since Klarna reportedly does not publish one fixed process [S15].
- Relying on SEO pages with unverified claims about 2026 loops [G].

**Recent changes and AI-era notes:**
- Reported hiring context, not interview policy: in late 2024 Klarna's CEO said hiring had effectively stopped a year earlier because of AI, then in May 2025 said Klarna was hiring again for customer service [S12][S13]. A July 2026 Swedish headline reports a hiring freeze and AI investment; the article itself was not seen [S14].
- No official Klarna statement on AI use in interviews was found. Claims of "AI fluency" as a hiring signal come from low-quality aggregator pages and are unverified [U].
- Take-home reports mix 2019 to 2026; the Berlin report is May 2025 [S1][S8].

**Sources:**
- S1: https://static.glassdoor.com.au/Interview/Klarna-Analytics-Manager-Interview-Questions-EI_IE389854.0,6_KO7,24.htm . Supports: Stockholm Jul 2023 analytics-manager review (logic test, HR call, proctored retest, skills, team, culture); 2018 and 2019 Stockholm logic-test and data scientist details come from a summary of several Glassdoor results. Anecdotal. Seen 2026-10-31. Snippet only.
- S2: https://interview.norahq.com/interview-guides/klarna-data-scientist-interview-guide-2026 . Supports: third-party 2026 guide; logic test about 15 to 30 minutes, about 7-day ML case study of 10+ hours. Seen 2026-10-31. Snippet only.
- S3: https://www.interviewquery.com/interview-guides/klarna-data-scientist . Supports: third-party DS guide; technical task of EDA, ML model and cloud deployment. Seen 2026-10-31. Snippet only.
- S4: https://www.interviewquery.com/interview-guides/klarna-ml-engineer . Supports: third-party MLE guide; five rounds, fraud and credit scoring prompts, MLOps and fairness, presentation (not confirmed by first-hand MLE reports). Seen 2026-10-31. Snippet only.
- S5: https://www.cleverprep.com/companies/klarna/data-scientist . Supports: third-party guide; 3 to 4 hour take-home on ML, statistics, SQL and Python; up to two months. Seen 2026-10-31. Snippet only.
- S6: https://www.techprep.app/blog/klarna-interview-process . Supports: third-party five-stage outline, about 36 days, team-fit and bar-raiser mentions, recruiter-ask advice. Seen 2026-10-31. Snippet only.
- S7: https://static.glassdoor.com.ar/Interview/Klarna-Interview-E389854-RVW76138712.htm . Supports: anecdotal case study to build an ML model and host via API on a cloud provider; credit risk model over 10 hours; exact page-to-detail match from a result summary. Seen 2026-10-31. Snippet only.
- S8: https://www.glassdoor.co.nz/Interview/Klarna-Interview-E389854-RVW73266522.htm . Supports: possibly the May 2025 Berlin report (HR, ML task, technical, Klarna fit, technical, team fit; anecdotal); page match uncertain, from a result summary. Seen 2026-10-31. Snippet only.
- S9: https://prepfully.com/interview-questions/klarna/data-scientist?page=8 . Supports: question-bank categories (ML modelling, statistics, SQL) and imputation question; user-submitted. Seen 2026-10-31. Snippet only.
- S10: https://www.hackingthecaseinterview.com/pages/klarna-case-interview . Supports: third-party case-interview guide, mainly non-engineering roles; used only as context. Seen 2026-10-31. Snippet only.
- S11: https://static.glassdoor.com.au/Interview/Klarna-Senior-Software-Engineer-Interview-Questions-EI_IE389854.0,6_KO7,31.htm . Supports: existence of a Stockholm Mar 2026 report (software engineer; no content used). Seen 2026-10-31. Snippet only.
- S12: https://www.aol.com/klarna-ceo-says-company-stopped-205638908.html . Supports: CEO said hiring stopped about a year earlier because of AI (late 2024). Seen 2026-10-31. Snippet only.
- S13: https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/ . Supports: May 2025 reversal, hiring customer service agents again. Seen 2026-10-31. Snippet only.
- S14: https://www.realtid.se/bors-finans/bank-fintech/klarna-fryser-anstallningar-och-satsar-pa-ai/ . Supports: July 2026 headline only; article not seen. Seen 2026-10-31. Snippet only.
- S15: https://ophyai.com/blog/company-guides/klarna-interview-guide . Supports: third-party 2026 guide; Klarna reportedly has no single fixed process, ask the recruiter. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Low-to-medium confidence that a logic test, an ML case or take-home, and team and culture interviews feature for data science; low confidence in durations, take-home size and ML engineer specifics [S1][S2][S5].
- India: no India-based reports found; general process evidence only.
- Verify with the Klarna recruiter and careers page: which stages apply to your role and office, the take-home scope, and any AI-use rules.
- No claim here that any question will be asked.
