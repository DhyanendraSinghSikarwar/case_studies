### C5 Apple (Big Tech)

**Evidence level:** Medium. Many candidate write-ups and prep-site summaries exist, but all are snippet-only, anecdotal or commercial, they disagree on round counts, and Apple's own pages were not found. [S1][S6]

**Roles seen in sources:** Machine Learning Engineer [S1][S2], Data Scientist [S4], Applied Scientist (one forum thread) [S9], AI/Research Scientist [S10], general Apple loop guides [S6]. India-specific: only a handful of Bengaluru and Hyderabad mentions, with almost no process detail [S5][S11].

**Process overview (as reported):**
1. Recruiter or screening call; one guide calls it an informal chat of about 30 minutes about interest and team fit [S6]. Some ML guides add a hiring-manager call before the technical screen (four-round version: screen, manager call, technical screen, remote onsite) [S1].
2. One or more technical or role-specific phone/video screens [S6][S4].
3. Onsite or virtual loop. Counts differ by source: 4 to 6 back-to-back interviews in one guide, "up to 10" in another [S6]; 4 to 7 rounds for ML engineer [S1]; 3 to 5 loop rounds for data scientist [S4]. Anecdotal: a six-round ML onsite thread [S2].
4. Team match and final decision [S6]. Overall duration is quoted from one to three weeks [S1] to about 4 weeks for data scientist [S4] to 4 to 6 weeks for general loops [S6]; treat as rough, anecdotal ranges.
5. Apple's process is decentralised and varies by team, per guides [S6]. Each team runs its own hiring [G].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call, about 30 min per one guide | Interest, team fit | [S6] |
| Hiring manager call (ML engineer, some reports) | Call | Background and fit | [S1] |
| Technical screen | Phone/video | Coding; for data scientist SQL, Python, statistics | [S6][S4] |
| Loop: algorithm coding | Live coding | LeetCode-style problems (anecdotal) | [S3][S9] |
| Loop: ML coding / theory | Live | ML coding problem, ML/NLP questions (anecdotal) | [S3][S2] |
| Loop: ML system design | Discussion | Design of an ML product; some loops add a general system design round | [S3][S9] |
| Loop: project deep dive / behavioral | Discussion | Past projects, behavioral questions | [S3][S1] |
| Research talk (research roles) | 45-minute presentation to team (anecdotal) | Research depth | [S3][S10] |
| Data scientist loop | Virtual onsite | SQL, statistics, metric design, A/B test, project walkthrough, case studies on Apple app lines | [S4] |

Round durations other than those named above: duration not found in sources.

**Question types:**
- Coding (LeetCode-style) and ML coding [S3][S9]
- ML/NLP fundamentals and ML system design [S3][S9][S1]
- Project deep dives [S1][S4]
- For data scientist: SQL, statistics, A/B testing, metric design, anomaly detection, regression critique, time series, telemetry data [S4]
- Behavioral [S3][S6]

**Sample questions (illustrative):**
- Walk me through an ML project you shipped: data, model choice, offline and online metrics, what you would change. [illustrative] Book 1 Part 3 classification metrics; Book 1 Part 11 ML system design.
- Write a function on a graph or binary tree (medium difficulty). [S5] Book 5 Part 7 trees and BST; Book 5 Part 9 graphs. (Source: an intern-level Glassdoor report, anecdotal.)
- How would you conduct an A/B test? [S4] Book 1 Part 10 A/B testing; Book 6 Part 4 experiment design.
- Design an ML-powered feature for an app (data, features, model, serving, monitoring). [illustrative] Book 1 Part 11 ML system design; Book 4 Part 8 monitoring ML in production.
- Given a table of usage events, write SQL for a retention or per-user metric. [illustrative] Book 3 Part 6 retention and cohorts; Book 3 Part 8 product metrics.
- Implement a simple ML algorithm (for example logistic regression) in NumPy. [illustrative] Book 1 Part 2 regression; Book 1 Part 12 NumPy/pandas live-coding.
- A metric on a telemetry dashboard moves; how do you investigate? [illustrative] Book 6 Part 1 product metrics and metric drops.

**What they score:**
- Coding correctness and communication [S3][S6]; ML depth and project ownership [S1][S4]; for data science, SQL, statistics and metric judgement [S4]. Specific scoring rubrics: not found in sources; the above is inferred from round content. [U]

**Level notes:**
- Level names and expectations: not found in sources for this snippet set. [U] Check the job posting for the title and years-of-experience line.

**Preparation plan (2 weeks):**
- Days 1-3: coding fluency, arrays/hashing, trees, graphs (Book 5 Parts 1, 7, 9) and NumPy/pandas live coding (Book 1 Part 12). [G]
- Days 4-6: ML fundamentals, metrics, tree models, NLP basics (Book 1 Parts 1-4, 9). [G]
- Days 7-8: SQL and statistics for data-scientist roles (Book 3 Parts 4-6, 8; Book 1 Parts 13-14). [S4]
- Days 9-10: A/B testing and metric scenarios (Book 1 Part 10; Book 6 Parts 1, 4). [S4]
- Days 11-12: ML system design (Book 1 Part 11; Book 4 Part 6 serving). [S3][S9]
- Day 13: prepare two project deep dives, and a research talk if the role is research. [S1][S10]
- Day 14: mock loop, plus ask the recruiter about the exact format. [S6]

**Common mistakes:**
- Treating one candidate's round list as the process; reports vary by team [S1][S6].
- Weak project stories: project deep dives recur [S1][S4].
- Skipping SQL/statistics basics for data-scientist roles [S4].
- Assuming AI tools are allowed in live rounds (see below) [S7].

**Recent changes and AI-era notes:**
- A 2026 policy tracker lists Apple as prohibiting AI tools in interviews [S7]; this is a third-party aggregator (recent, unconfirmed by Apple).
- One 1point3acres thread title says Apple added an AI-assisted coding round for software engineer full-time interviews; the date and details could not be confirmed and it is about software engineers, not ML roles [S8][U].
- Sources do not say whether ML roles differ [U]. Ask the recruiter what applies.

**Sources:**
- S1: https://www.interviewquery.com/interview-guides/Apple-Machine-Learning-Engineer ; ML engineer guide; supports 4-round and 4-7 round descriptions and 1 to 3 week timeline; seen 2026-10-31; snippet only (prep site, partly paywalled).
- S2: https://www.1point3acres.com/interview/thread/1172960 ; title "Apple Machine Learning Onsite Interview Experience: Six Rounds Overview"; supports a six-round ML onsite report (anecdotal); seen 2026-10-31; snippet only (title and listing).
- S3: https://www.glassdoor.co.uk/Interview/Apple-Interview-E1138-RVW83470630.htm ; one of the Glassdoor reviews returned for ML engineer; the search summary reported a 6-round loop (algorithm coding, ML coding, system design, behavioral) and a 45-minute research presentation loop, without naming which review held which detail, so attribution is approximate; anecdotal; seen 2026-10-31; snippet only.
- S4: https://www.interviewquery.com/guides/apple-data-scientist?exp_page=1 ; data scientist guide; supports 3-6 rounds, about 4 weeks, SQL/Python/statistics, metric design, A/B test question; seen 2026-10-31; snippet only. Bengaluru (1-hour coding, manager, behavioral) and Cork (8 rounds) candidate reports came from the Glassdoor results of the same search, not attributable to one URL (anecdotal).
- S5: https://www.glassdoor.co.in/Interview/Apple-Interview-E1138-RVW73678830.htm ; one of the Glassdoor results of the India-focused search; the summary mentioned a Bengaluru referral process of about six weeks, a Hyderabad February 2023 neutral review and an ML intern report (HR screen, 2-3 tech rounds, graph/tree problems); attribution approximate; anecdotal; seen 2026-10-31; snippet only.
- S6: https://igotanoffer.com/en/advice/apple-interview-process ; general Apple loop guide among results; supports stages, decentralisation, 30-min recruiter chat, 4-6 or up to 10 loop interviews, timelines (the summary pooled several guides in the result set, so figures are approximate); seen 2026-10-31; snippet only.
- S7: https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/ ; supports Apple listed as AI-prohibited; seen 2026-10-31; snippet only.
- S8: https://www.1point3acres.com/interview/thread/1174445 ; title "Apple Adds AI-Assisted Coding Round for Software Engineer Fulltime Interviews"; seen 2026-10-31; snippet only; unconfirmed.
- S9: https://www.levels.fyi/community/thread/OuE1gQ/what-to-expect-for-apple-applied-scientist-interview ; supports applied scientist: phone screen then onsite, LC-style and ML design questions, team-dependent (anecdotal); seen 2026-10-31; snippet only.
- S10: https://www.interviewquery.com/guides/apple-ai-research-scientist ; supports research scientist loop with research talk and 5-6 researcher interviews; seen 2026-10-31; snippet only.
- S11: https://www.teamblind.com/post/apple-applied-machine-learning-team-mqyjagy3 ; Blind thread about the applied ML team (Hyderabad per the summary); snippet showed no answers; seen 2026-10-31; snippet only.

**Confidence and what to verify:**
- Confidence: medium on the general shape (recruiter, technical screens, loop with coding, ML, design and behavioral), low on exact round counts and durations. [S1][S6]
- India: very thin; no India-specific round structure found [S5][S11]. Verify with the recruiter.
- Verify on Apple's careers page and with the recruiter: loop length, whether coding is on a shared editor, the AI-tool policy, and team-specific rounds. All sources are snippet only; no page was opened.

### C6 Netflix (Big Tech)

**Evidence level:** Thin to Medium (rated Thin). Candidate reports are few, long-loop anecdotes differ widely, prep sites contradict each other, and the official page found covers culture, not interview steps. [S7][S2][S3]

**Roles seen in sources:** Data Scientist [S1][S2][S3], Machine Learning Engineer [S4][S5], ML Infra software engineer [S6], Research Scientist [S11], AI Engineer guides [S4]. India-based Netflix hiring: nothing found.

**Process overview (as reported):**
1. Recruiter chat, then hiring manager phone screen, then technical phone screen (Senior Data Scientist, Member UI team, 2021 review; anecdotal and dated) [S10].
2. Prep-site data scientist rounds: recruiter screen, technical phone screen, SQL, statistics and experimentation, machine learning, product case study, culture fit, about 4-6 weeks [S1] (commercial guide; another guide says these are question categories, not separate rounds [S1]).
3. Prep-site ML engineer loop: six rounds (recruiter screen, technical phone screen, ML depth, coding, ML system design, culture) [S4].
4. Anecdotal long loops: a 12-round data scientist process over about two months [S2] and an 11-round loop of about two and a half months with a hiring-manager swap (October 2025) [S3]. Single anecdotes, not the standard process.
5. General Netflix guides mention roughly 8 interviews over two stages and a unanimous team decision; not role-specific and unverified [S8][U].
6. Reapply wait of 6-12 months is quoted by one general guide [S8][U].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter chat | Call | Fit and logistics | [S10][S4] |
| Hiring manager screen | Phone | Background, team fit | [S10] |
| Technical phone screen | Phone | Product analytics/experimentation (DS); in one ML anecdote a behavioral interview plus an ML system design interview | [S10][S5] |
| SQL / data manipulation | Live | SQL | [S1] |
| Statistics and experimentation | Discussion | A/B testing, causal inference | [S1] |
| ML and modeling / ML depth | Discussion | ML fundamentals, past ML project | [S1][S4][S5] |
| ML system design | Discussion | Recommendation system design (prep site); anomaly detection design (anecdote) | [S4][S6] |
| Coding | Live | Coding, short warm-up in one anecdote | [S4][S6] |
| Product case / culture | Discussion | Product reasoning, culture fit | [S1][S4] |

Round durations: duration not found in sources.

**Question types:**
- Experimentation and causal inference, product metrics, behavioral [S1]
- Past ML project, loss-function choice, computer vision experience (anecdotal) [S5]
- Recommendation system design [S4]
- ML infra loop: coding, data science collaboration, system design (anecdotal) [S6]

**Sample questions (illustrative):**
- Tell me about a machine learning project you worked on. [S5] Book 1 Part 3 classification metrics; Book 1 Part 11 ML system design.
- How would you choose a loss function for this problem? [S5] Book 1 Part 2 regression and regularization; Book 1 Part 8 deep learning.
- Design a recommendation system from data collection to serving. [S4] Book 1 Part 7 recommender systems; Book 1 Part 11 ML system design.
- Design an anomaly detection system for a streaming metric. [S6] Book 1 Part 5 anomaly detection; Book 4 Part 8 monitoring ML in production.
- A new feature shows a lift in one metric and a drop in another; how do you decide whether to ship? [illustrative] Book 6 Part 4 ambiguous A/B results; Book 1 Part 10 A/B testing.
- Write SQL for weekly retention of members by signup cohort. [illustrative] Book 3 Part 6 retention and cohorts.
- Describe a time you gave a colleague direct feedback or disagreed with a decision. [illustrative] Book 6 Part 6 stakeholder conflicts and trade-offs.

**What they score:**
- Prep sites list strong ML fundamentals, a record of shipping impactful ML, collaboration [S4]; for data science, technical depth, statistical rigour, with a strategic roadmap discussion at senior level [S1]. The careers site frames culture around context over control, with managers coaching actively [S7]. Culture fit weight is the opinion of prep writers, unverified [S8][U].

**Level notes:**
- Mid-level data science focuses on coding fluency, statistical rigour and project ownership; senior adds roadmap and strategic impact [S1]. Research scientist IC4-IC5 focuses on technical depth and system design [S11]. Role posting titles seen use L4/L5 style names (data scientist L4, L5 postings) [S1][U].

**Preparation plan (2 weeks):**
- Days 1-3: experimentation and causal inference (Book 1 Part 10; Book 6 Part 4). [S1]
- Days 4-5: SQL and product metrics (Book 3 Parts 4-6, 8). [S1]
- Days 6-8: ML fundamentals and recommenders (Book 1 Parts 2-4, 7). [S4]
- Days 9-10: ML system design (Book 1 Part 11; Book 4 Part 8). [S4][S6]
- Day 11: coding refresh (Book 5 Parts 1, 7, 9; Book 1 Part 12). [S4][S6]
- Day 12: read the careers culture page and prepare examples of candid feedback and ownership (Book 6 Part 6). [S7]
- Days 13-14: mock loop; ask the recruiter about the format, as it varies by team and year. [S8]

**Common mistakes:**
- Preparing a fixed round list; reports range from 6 to 12 rounds [S4][S2][S3].
- Ignoring the culture material when it is part of the discussion [S7].
- Shallow experimentation answers for data-scientist roles, where it is central [S1].

**Recent changes and AI-era notes:**
- A Greek news site reports Netflix lets candidates use AI tools when writing code while still assessing code quality, system design and testing; not confirmed from a primary source [S9][U].
- A mirror page says interviews now discuss how candidates think about and use AI [U]; weakly sourced.
- A 2026 tracker lists AI policies by company; the snippet did not give a Netflix-specific line [S9].
- The October 2025 long-loop anecdote is the most recent candidate evidence [S3].
- India: no Netflix India hiring information found in sources.

**Sources:**
- S1: https://www.interviewquery.com/interview-guides/netflix-data-scientist ; data scientist guide; supports round list, 4-6 weeks, mid versus senior focus, experimentation emphasis; seen 2026-10-31; snippet only (commercial).
- S2: https://www.1point3acres.com/interview/thread/1123435 ; title "Two-Month Journey Through 12 Rounds of Netflix Data Science Interviews"; supports a 12-round anecdote only; seen 2026-10-31; snippet only (title and listing).
- S3: https://prachub.com/interview-experiences/netflix-data-scientist-interview-experience-11-rounds-10-people-and-a-hiring-manager-swapped-mid-loop ; supports an 11-round, long, hiring-manager-swap anecdote (October 2025 per the summary); seen 2026-10-31; snippet only.
- S4: https://www.cleverprep.com/companies/netflix/machine-learning-engineer ; supports six-round ML engineer prep-site list, recommender design prompt, hiring criteria; seen 2026-10-31; snippet only (commercial).
- S5: https://www.teamblind.com/post/ml-engineering-interview-at-netflix-rponqss8 ; Blind thread; the search summary cited a candidate report of a behavioral plus ML system design screen and questions on past ML project and loss functions; attribution to this URL approximate; anecdotal; seen 2026-10-31; snippet only.
- S6: https://www.1point3acres.com/interview/thread/1170648 ; ML infra software engineer onsite (coding, data science collaboration, system design); anecdotal; seen 2026-10-31; snippet only. The anomaly-detection design and short coding warm-up anecdote came from another result in the same search, not attributable to one URL.
- S7: https://jobs.netflix.com/culture ; official culture page; supports context-not-control and active coaching wording only; seen 2026-10-31; snippet only.
- S8: https://igotanoffer.com/en/advice/netflix-interview-process ; general Netflix process guide among results; the summary pooled several guides (about 8 interviews, unanimous decision, reapply 6-12 months, culture emphasis), so attribution is approximate; seen 2026-10-31; snippet only.
- S9: https://www.secnews.gr/en/722863/netflix-ai-fluency-dexiotita-ergazomenoi/ ; Greek news item on Netflix AI use in coding; unconfirmed; and https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/ for the general tracker; seen 2026-10-31; snippet only.
- S10: https://www.glassdoor.co.uk/Interview/Netflix-Interview-E11891-RVW44407200.htm ; 2021 Senior Data Scientist, Member UI review; supports recruiter, hiring manager, technical phone screen; anecdotal and dated; seen 2026-10-31; snippet only.
- S11: https://www.interviewquery.com/interview-guides/netflix-research-scientist ; supports IC4-IC5 focus; seen 2026-10-31; snippet only.

**Confidence and what to verify:**
- Confidence: low on round structure, medium on question themes (experimentation, ML design, recommenders). [S1][S4]
- Process varies by team and year; aggregators say live recruiter instructions decide it [S8].
- India: nothing found. Check the Netflix careers page for current India listings.
- Verify with the recruiter: number of rounds, AI-tool policy, coding format. All sources are snippet only; no page was opened.
