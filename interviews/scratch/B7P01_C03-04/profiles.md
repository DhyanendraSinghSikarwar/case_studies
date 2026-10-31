### C3 Amazon (Big Tech)

**Evidence level:** Medium. Amazon's own interview guide appeared as a search result [S2], but all other detail is third-party prep sites and anecdotal candidate reviews that vary by team and year. Snippets only; no page was opened.

**Roles seen in sources:** Applied Scientist (including Senior and AGI/LLM-flavoured postings) [S3][S8], Data Scientist (mostly intern reviews, some India listings) [S4][S9], GenAI Engineer and AI Engineer prep guides [S6], Research Scientist prep page on the Amazon jobs site [S1]. India reports (Bengaluru, Hyderabad) are anecdotal and few [S5][S9].

**Process overview (as reported):**
1. Recruiter screen / online application [S3]. Duration not found in sources.
2. One or two phone screens, possibly followed by role-specific assessments; screens mostly check basic qualifications [S2]. Third-party guides say about 45 minutes [S2 snippet, third-party part]; one Bengaluru anecdote describes a 60-minute screen mixing ML depth, live coding and Leadership Principles (LP) [S5] (anecdotal).
3. Timed SQL or coding test for some Data Scientist candidates in India (anecdotal) [S9].
4. Virtual or onsite "loop": third-party guides say 4 to 5 back-to-back interviews [S3]; one Applied Scientist guide says four 55-minute interviews plus a tech talk [S3]; sources conflict on size, so confirm with the recruiter [S3].
5. Bar Raiser: an interviewer from another team, focused on LPs; guides disagree on whether it is the last round and on veto power [S3] (third-party, conflicting).
6. Debrief after the final interview, judged against the LPs and role requirements; Amazon states it aims to give feedback about two business days after phone screens and about five after the loop [S2].
7. For Senior Applied Scientist, some reports mention a research or project presentation of roughly 45-60 minutes with Q&A, sometimes with an abstract sent ahead (anecdotal) [S7].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Call | Fit, role match | [S3] |
| Phone screen(s) | 45-60 min call, live coding and/or ML and LP questions | Basic qualifications | [S2][S5] |
| SQL / coding test (DS, India) | Timed online | SQL and programming basics | [S9] anecdotal |
| Loop: ML breadth | Interview with scientist | Loss functions, optimizers, regularisation, transformers | [S5] anecdotal |
| Loop: ML depth | Interview | Deep dive on your own recent project | [S5] anecdotal |
| Loop: coding | Live coding | Correctness, explanation, complexity; difficulty varies by interviewer | [S5] anecdotal |
| Loop: LP / Bar Raiser | Behavioural | Past examples against LPs | [S2][S3] |
| Research talk (Senior) | Presentation plus Q&A | Depth, communication, defending methods | [S7] anecdotal |

**Question types:**
- Behavioural questions tied to Leadership Principles, using real past examples [S2]; LP questions appear embedded in every interview in several reviews [S5] (anecdotal).
- Data Scientist reviews: SQL window functions, GROUP BY, subqueries, CTEs, Pandas manipulation, statistics (regression assumptions, Pearson vs Spearman), confusion matrix, deep learning concepts [S4] (anecdotal, intern-heavy).
- Applied Scientist: ML breadth and depth, coding, ML design [S3][S5][S8].
- LLM-era reports: LLM training techniques, LLM evaluation metrics, RAG versus fine-tuning, seq2seq, L1/L2 [S8] (anecdotal).
- Case or use-case discussion with a hiring manager appears in some reports [S10] (anecdotal).

**Sample questions (illustrative):**
1. Write a SQL query to rank each customer's orders by value and return the top 3 per customer. [illustrative] Book 3 Part 4 (window functions: ranking and top-N per group).
2. Explain the assumptions of linear regression and how you would check each. [S4] Book 1 Part 2 (linear/logistic regression), Book 1 Part 13 (statistics).
3. Walk me through a recent ML project in depth: why this model, what failed, what you would change. [S5] Book 1 Part 11 (ML system design); Book 6 Part 10 (design a solution end-to-end).
4. Compare Pearson and Spearman correlation and when each misleads. [S4] Book 1 Part 1 (stats basics), Book 1 Part 14 (statistics deep dive II).
5. When would you use RAG instead of fine-tuning, and how would you evaluate the result? [S8] Book 2 Part 6 (RAG basics), Book 2 Part 4 (fine-tuning), Book 2 Part 9 (LLM evaluation).
6. Solve an array/hash problem and state time and space complexity. [illustrative] Book 5 Part 1 (arrays and hashing).
7. Tell me about a time you disagreed with a stakeholder and what you did. [illustrative] Book 6 Part 6 (stakeholder conflicts and trade-off decisions).
8. A key metric dropped 10% week over week; how do you investigate? [illustrative] Book 6 Part 1 (product metrics and metric drops).

**What they score:**
- Leadership Principles evidence, with the panel debriefing against LPs and role requirements [S2]. Each interviewer is reported to own specific principles [S2 snippet, third-party part].
- Technical correctness with explanation and complexity (anecdotal) [S5].
- ML fundamentals and depth on own work [S5][S3].
- For Senior scientist roles, depth and communication in a talk (anecdotal) [S7].

**Level notes:** One prep guide describes Applied Scientist at L5 and Senior Applied Scientist at L6, with L6 leading projects and setting direction; the same guide's L5 title mapping looks questionable, so verify against job postings [S8] [U].

**Preparation plan (2 weeks):**
- Days 1-2: LP story bank (8 to 10 stories with measurable results, STAR format) [S2][S3]; Book 6 Part 6.
- Days 3-4: SQL timed practice: Book 3 Parts 3, 4, 5 and 12 [S4][S9].
- Days 5-6: ML and stats fundamentals: Book 1 Parts 1, 2, 3, 13 [S4][S5].
- Days 7-8: Deep learning, transformers, NLP: Book 1 Parts 8 and 9; for GenAI roles Book 2 Parts 1, 4, 6, 9 [S5][S8].
- Days 9-10: Coding practice with spoken complexity: Book 5 Parts 1, 2, 7, 9 [S5].
- Days 11-12: Prepare a deep dive on one own project; Senior roles also a 45-minute talk [S5][S7]; Book 1 Part 11.
- Days 13-14: Mixed mock loop with LP in each round [S5]; Book 6 Parts 1 and 10.

**Common mistakes:**
- Hypothetical answers to behavioural questions instead of real examples [S2 snippet, third-party part].
- Treating LPs as one round only; reports say they are embedded throughout [S5] (anecdotal).
- Not being able to go deep on your own project (ML depth) [S5] (anecdotal).
- Using AI tools during the interview (see below) [S6].

**Recent changes and AI-era notes:**
- Reported 2025: Amazon disqualifies candidates caught using unauthorized GenAI tools in interviews, and candidates acknowledge they will not use them; teleprompter-style tools are named. Reporting traces to Business Insider via secondary outlets; Amazon's own policy text was not seen [S6].
- Amazon's guide mentions 16 Leadership Principles; older guides cite 14, so check the current list [S2 snippet, third-party part].
- LLM topics (training, evaluation, RAG versus fine-tuning) appear in recent Applied Scientist reviews (anecdotal, undated) [S8].
- Older: 2021-2022 Bengaluru loops (anecdotal) [S5].

**Sources:**
- S1. https://amazon.jobs/content/en/how-we-hire/research-scientist-interview-prep : page titled "Amazon Leadership Principles" on Amazon's jobs site, appeared for the Applied Scientist query; snippet gave no content, so used only to note it exists. Seen 2026-10-31. Snippet only.
- S2. https://aboutamazon.com/news/workplace/amazon-interview-guide : Amazon's guide: LP-rooted process, debrief, feedback timing, phone screens vs loop. Seen 2026-10-31. Snippet only (also https://www.aboutamazon.com/md/news/workplace/amazon-interview-process-phone-screens-loops appeared).
- S3. https://www.cleverprep.com/companies/amazon/applied-scientist : third-party; 4 rounds, four 55-minute loop interviews plus tech talk, research presentation advice. Seen 2026-10-31. Snippet only. Also https://hyring.com/jobseeker-toolkit/interview-questions/company/amazon and https://prepfully.com/interview-guides/amazons-bar-raiser-interview for Bar Raiser descriptions (third-party).
- S4. https://www.glassdoor.co.uk/Interview/Amazon-Interview-E6036-RVW99965159.htm : Glassdoor reviews, mostly Data Scientist Intern, SQL/Python/stats/ML, LPs (anecdotal). Seen 2026-10-31. Snippet only. Also https://www.glassdoor.co.uk/Interview/Amazon-Interview-E6036-RVW103632729.htm.
- S5. https://leetcode.com/discuss/interview-experience/1585287/amazon-msft-google-apple-fb-zoom-applied-scientist-multiple-sep-21-offer-rest-reject ; https://www.teamblind.com/post/applied-scientist-interview-amazon-4udsobcp ; https://www.glassdoor.sg/Interview/Amazon-Interview-E6036-RVW79375451.htm : Bengaluru and other Applied Scientist anecdotes (screen, ML breadth/depth, coding, LPs). The search summary did not attribute each detail to a single URL, so details are attributed to this group. Seen 2026-10-31. Snippet only.
- S6. https://itpro.com/business/careers-and-training/amazon-bans-ai-tools-during-job-interviews : AI-tool ban reporting; also https://dataford.io/interview-guides/amazon/genai-engineer and https://www.interviewquery.com/prep-guides/amazon-ai-engineer as GenAI/AI Engineer prep guides (third-party). Seen 2026-10-31. Snippet only.
- S7. https://www.teamblind.com/post/amazon-science-sr-applied-scientist-interview-presentation-requirement-tgrgowoo : Blind anecdote on Senior Applied Scientist presentation (about 50 + 10 min). Seen 2026-10-31. Snippet only.
- S8. https://interviewkickstart.com/odio/amazon-applied-scientist-interview-guide : level descriptions; plus https://www.glassdoor.fr/Entretien/Amazon-Entretien-E6036-RVW100110012.htm (LLM questions, anecdotal) and https://igotanoffer.com/en/advice/amazon-applied-scientist-interview. Seen 2026-10-31. Snippet only.
- S9. https://www.ambitionbox.com/interviews/amazon-interview-questions/data-scientist : India Data Scientist anecdotes (timed SQL test, coding questions). Seen 2026-10-31. Snippet only.
- S10. https://www.interviewquery.com/guides/amazon-data-scientist?exp_page=1 : third-party description of DS loop and case prompts. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium for the existence of LP-driven loops, Bar Raiser and ML breadth/depth/coding split; low for exact round counts, durations and which levels get a talk (sources conflict) [S3].
- India-specific evidence is thin and anecdotal [S5][S9].
- Verify with your recruiter and Amazon's jobs site: loop size, Bar Raiser, presentation requirement, AI-tool policy, current LP count.

### C4 Meta (Big Tech)

**Evidence level:** Medium. Meta's own careers pages for the ML full loop appeared in results [S1][S2], but their content reached me only as short snippets. Data Scientist structure, coding and AI-era details come from prep sites, press reports and anecdotal reviews. India-specific interview evidence is thin.

**Roles seen in sources:** Data Scientist (product analytics) [S3], Machine Learning Engineer / Software Engineer, Machine Learning [S1][S4], AI/Research Scientist and GenAI-flavoured loops [S6]. India: job listings in Bangalore for Data Scientist and Senior ML Engineer, offices in Bengaluru and Hyderabad per a low-authority blog [S7].

**Process overview (as reported):**
1. Recruiter call: non-technical, role fit and motivation; one guide says 30-45 minutes [S3].
2. Data Scientist technical screen: one or two interviews of about 45 minutes (one guide says 45-60), with SQL plus a product sense case [S3].
3. Data Scientist full loop: estimates of four to five interviews covering SQL, product sense, statistics or A/B testing, analytical reasoning and behavioural; one candidate described four 45-minute virtual rounds (anecdotal) [S3].
4. ML Engineer: Meta's ML page says the full loop is up to six 45-minute conversations with engineers [S1]; third-party guides describe screening, coding, ML system design and behavioural [S4].
5. Timeline: guides say 4-6 weeks; Glassdoor candidates report about 2 to 2.5 months (anecdotal) [S3].
6. Recruiter tells you ahead of time which round is which, and which allow AI (reported for the AI-enabled pilot) [S5].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter call | Phone | Fit, motivation | [S3] |
| DS technical screen | 45-60 min, SQL + light product case | SQL, product thinking | [S3] |
| DS loop: SQL / analytical reasoning | About 45 min | Query writing, data reasoning | [S3] |
| DS loop: product sense | About 45 min | Success metrics, launch decisions, opportunity sizing | [S3] anecdotal |
| DS loop: statistics / experimentation | About 45 min | A/B test design | [S3] |
| DS loop: behavioural | About 45 min | Past behaviour, collaboration | [S3] |
| MLE: coding | LeetCode-style, several short problems | Correct, clean code, edge cases | [S4] anecdotal |
| MLE: ML system design | Open design, e.g. recommendation | Data, features, model, offline/online evaluation, trade-offs | [S4] anecdotal |
| MLE/RS: AI-enabled coding (pilot) | 60 min in CoderPad with built-in assistant | Working with AI on a larger problem | [S5] reported, limited pilot |
| Research Scientist: research fit | Present own research, open questions | Depth on own work | [S6] anecdotal |

**Question types:**
- DS: SQL, product sense (measure success of Facebook Groups, define a success metric, decide whether to launch a feature), A/B test design, opportunity sizing [S3] (anecdotal).
- MLE: LeetCode easy-to-hard coding, ML system design (recommendation and ranking recur), behavioural described as comparatively smooth [S4] (anecdotal).
- Research/GenAI: own-research defence, ML coding without PyTorch, LLM training efficiency such as gradient checkpointing, designing an LLM assistant with retrieval and safety guardrails [S6] (anecdotal).

**Sample questions (illustrative):**
1. How would you measure the success of Facebook Groups? [S3] Book 6 Part 1 (product metrics and metric drops); Book 3 Part 8 (funnels, conversion, DAU/MAU).
2. Write a query for day-7 retention by signup cohort. [illustrative] Book 3 Part 6 (date/time: retention, cohorts).
3. A new feature shows a lift on one metric and a drop on another; do you launch? [illustrative] Book 6 Part 4 (experiment design and ambiguous A/B results); Book 1 Part 10 (A/B testing).
4. Design a place-recommendation system for users. [S4] Book 1 Part 7 (recommenders, ranking); Book 1 Part 11 (ML system design).
5. Design an LLM-based conversational assistant with retrieval and safety guardrails. [S6] Book 2 Part 6 (RAG basics), Book 2 Part 5 (alignment, safety, guardrails), Book 2 Part 12 (GenAI system design).
6. Explain gradient checkpointing and when it helps training. [S6] Book 2 Part 2 (pretraining and scaling), Book 1 Part 8 (deep learning).
7. Solve a graph or array problem cleanly with edge cases handled. [S4] Book 5 Part 9 (graphs), Book 5 Part 1 (arrays and hashing).
8. Implement logistic regression training loop in NumPy without a framework. [illustrative] Book 1 Part 1 (from-scratch code), Book 1 Part 12 (live-coding).

**What they score:**
- Technical skill per round; the loop is described as assessing technical skills and giving candidates a view of the work [S2].
- For DS: product sense and metric reasoning alongside SQL and statistics [S3].
- Behavioural performance can move the level outcome: one Blind anecdote reports a candidate at IC5 on design but IC4 on behavioural [S8] (anecdotal).
- Edge cases and clean code in coding [S4] (anecdotal).

**Level notes:** Data Scientist levels appear as IC4 and IC5 and above; guides disagree on years of experience, and one Blind report says the final level is decided after the rounds [S8] (anecdotal). Engineering-track E-level names for ML roles appear in AI-coding reports (E6 and below, E7 and above) [S5]; DS equivalents not confirmed [U].

**Preparation plan (2 weeks):**
- Days 1-2: SQL timed sets: Book 3 Parts 1-5 and 8 [S3].
- Days 3-4: Product sense and metrics: Book 6 Parts 1, 4, 5 and Book 3 Part 8 [S3].
- Days 5-6: Stats and experimentation: Book 1 Parts 10, 13, 14 [S3].
- Days 7-8: ML fundamentals and recommenders: Book 1 Parts 2, 3, 4, 7 [S4].
- Days 9-10: Coding practice, short problems at speed: Book 5 Parts 1, 2, 7, 9; Book 1 Part 12 for ML coding [S4].
- Days 11-12: ML system design and, for GenAI roles, Book 1 Part 11 and Book 2 Parts 6, 9, 12 [S4][S6].
- Day 13: Practise a coding task with an AI assistant, plus writing your own tests and reviewing generated code: Book 1 Part 12 (AI-code-review rounds) [S5].
- Day 14: Behavioural stories and one full mock: Book 6 Part 6 [S3][S8].

**Common mistakes:**
- Treating the behavioural round as free, though one anecdote ties it to level outcome [S8] (anecdotal).
- Jumping to a model in ML design without covering data, features, offline and online evaluation [S4] (anecdotal).
- Using AI tools in a round where they are not allowed; Meta's full-loop guide is reported to ask candidates not to use unauthorized outside assistance [S5].
- Product answers without a clear success metric and guardrail metrics [G].

**Recent changes and AI-era notes:**
- Reported 2025: Meta confirmed building a coding interview with an AI assistant; one source says a pilot from October 2025 replaces one onsite coding round with a 60-minute CoderPad round with a built-in assistant, invite-only, and not universal [S5].
- Conflicting signal: Meta's careers guide is reported to still ask candidates not to use unauthorized AI tools; confirm in writing which round allows AI [S5].
- 2026 research scientist reports mention behavioural, ML design, AI-enabled coding and traditional coding in one loop (anecdotal) [S6].
- Older: DS loop structure from 2025 prep guides and reviews; undated for some [S3].

**Sources:**
- S1. https://www.metacareers.com/ML-prep-onsite/ : Meta ML full-loop page; snippet says up to six 45-minute conversations with engineers. Seen 2026-10-31. Snippet only.
- S2. https://www.metacareers.com/swe-prep-onsite/ : Meta SWE full-loop page; snippet describes loop as assessing technical skills and giving insight into work. Seen 2026-10-31. Snippet only.
- S3. https://www.interviewquery.com/interview-guides/facebook-data-scientist ; https://www.tryexponent.com/guides/meta-data-scientist-interview ; https://interviewkickstart.com/blogs/articles/meta-data-scientist-interview-process ; https://www.glassdoor.co.in/Interview/Meta-Interview-E40772-RVW97721021.htm : DS stages, SQL plus product sense, loop of four to five, timelines (third-party and anecdotal). Seen 2026-10-31. Snippet only.
- S4. https://www.interviewquery.com/guides/meta-ml-engineer ; https://app.igotanoffer.com/blogs/tech/facebook-machine-learning-engineer-interview ; https://dataford.io/interview-guides/meta/machine-learning-engineer/experiences : MLE rounds, coding, ML system design, behavioural (third-party, anecdotal). Seen 2026-10-31. Snippet only.
- S5. https://hellointerview.com/blog/meta-ai-enabled-coding ; https://www.techradar.com/pro/meta-is-going-to-let-candidates-use-ai-in-job-interviews ; https://www.businesstoday.in/amp/technology/news/story/meta-to-test-job-applicants-with-ai-assisted-coding-interviews-amid-ai-expansion-plans-487200-2025-07-31 ; https://www.greatfrontend.com/blog/ai-assisted-coding-interviews-for-frontend-developers : AI-enabled coding pilot, format, conflicting careers-guide note. Seen 2026-10-31. Snippet only.
- S6. https://www.glassdoor.sg/Interview/Meta-Interview-E40772-RVW92650100.htm ; https://www.1point3acres.com/interview/thread/1141203 ; https://www.interviewquery.com/guides/meta-ai-research-scientist : research/GenAI loop anecdotes. Seen 2026-10-31. Snippet only.
- S7. https://blog.kowatek.com/?p=99262 ; https://www.jointaro.com/jobs/meta/software-engineer-machine-learning-85dfab93 : India offices and Bangalore openings (low-authority). Seen 2026-10-31. Snippet only.
- S8. https://www.teamblind.com/post/ic5-behavioural-interview-expectations-at-meta-j0k1dwnv ; https://codemia.io/guides/meta-data-scientist : DS level and behavioural anecdotes; experience ranges conflict. Seen 2026-10-31. Snippet only.

**Confidence and what to verify:**
- Medium for DS (SQL plus product sense screen, product/stats/behavioural loop) and MLE (coding, ML design, behavioural); low for exact round counts per role and team [S3][S4].
- Low for the AI-enabled round: pilot, limited, sources partly conflict [S5].
- India interview evidence: none firsthand found; only locations and openings [S7]. Assume the standard process only as [U].
- Verify on Meta's careers prep page for your role and with your recruiter: loop length, which rounds permit AI, level, and whether a research presentation applies.
