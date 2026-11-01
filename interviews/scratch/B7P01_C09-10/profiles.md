### C9 Adobe (Big Tech)

**Evidence level:** Thin. Adobe's own page was only partly captured; everything about rounds comes from third-party prep sites and anonymous candidate reports that disagree on details [S1][S2].

**Roles seen in sources:** Data Scientist (India and US reports) [S3][S4]; Machine Learning Engineer [S5][S9]; Applied Scientist / ML Scientist / Firefly generative-AI roles appear mainly as job postings, with no published loop [S6][S10]. India postings for ML Engineer and Senior ML Engineer (Firefly) exist in Bangalore and Noida [S9][S10].

**Process overview (as reported):**
1. Recruiter call, described as about 30 minutes: background and motivation [S2] (third-party guide).
2. Hiring manager screen, in some guides before a technical online assessment [S2].
3. Technical online assessment for engineering roles, covering coding and problem solving [S2].
4. Technical interviews, then a final manager, director or behavioural round [S3][S4]. Guides count 4 to 6 rounds in total, varying by role, level and location [S2].
5. For Data Scientist, one guide lists: online assessment, technical interview, manager round, director behavioural round [S3]. Another describes a final round with a take-home presentation to a panel and a case study [S4].
- Duration of individual rounds: not found in sources, except a 75-minute virtual technical interview in software-engineer reports [S8] (anecdotal, not DS/ML). End-to-end time estimates range from 10-15 days (one anecdote) to 2-6 weeks [S2][S3].
- The process varies by team, for example Sensei, Experience Manager or Creative Cloud [S2].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Phone, about 30 min | Background, motivation | [S2] |
| Online assessment | Online, coding-style | Coding and problem solving (engineering); DS guide lists an OA | [S2][S3] |
| Technical interview | Interview with a data scientist or engineer | SQL, ML questions, coding such as k-nearest neighbours or a basic random forest from scratch (anecdotal) | [S3][S5] |
| ML / system design | Design discussion | Design a production fraud-detection system (one DS report); end-to-end ML design (guide) | [S4][S5] |
| Manager / director round | Behavioural, possibly project presentation | Behavioural and business-impact discussion | [S3] |
| Case study / presentation | Panel presentation, per one guide | Analytical case; guide calls it the most critical part | [S4] |

**Question types:**
- SQL, described as consistently and heavily weighted in DS reports [S4].
- Probability and statistics; web analytics and Adobe Analytics questions in one India-based report (anecdotal) [S4].
- ML fundamentals plus coding from scratch (k-nearest neighbours, matrix multiplication, a PyTorch classifier, basic random forest), anecdotal [S5].
- ML system design, for example fraud detection with data pipelines and A/B testing (one Bengaluru report, anecdotal) [S4].
- For Firefly-type roles, a third-party guide lists coding, ML and generative-AI depth, and system design on diffusion and LLM features [S6]; a Blind post on a software-engineer Firefly loop reports 2 coding, 1 system design, 1 behavioural/GenAI round (anecdotal, not an ML role) [S7].

**Sample questions (illustrative):**
- Write a SQL query for week-over-week retention of users of a creative app. [illustrative] (Book 3 Part 6 date/time retention and cohorts)
- Implement k-nearest neighbours from scratch in NumPy and discuss complexity. [S5] (Book 1 Part 8 deep learning/from scratch and Book 1 Part 12 live-coding)
- Design a production fraud-detection system: data, features, model, monitoring. [S4] (Book 1 Part 11 ML system design)
- Our A/B test on a new export button shows a small lift; do you ship? [illustrative] (Book 1 Part 10 A/B testing; Book 6 Part 4 experiment design)
- Explain how you would add a text-to-image feature check for quality drift in a diffusion model. [illustrative] (Book 2 Part 9 LLM evaluation; Book 6 Part 7 GenAI scenarios)
- Walk through a project where your analysis changed a business decision. [illustrative] (Book 6 Part 6 stakeholder trade-offs)
- Compute the median session length from a skewed events table using window functions. [illustrative] (Book 3 Part 4 window functions)

**What they score:** The sources do not publish a rubric. Guides say the process is built around company values such as honesty and creativity, from a low-authority source [S2]. Reports emphasise SQL, ML fundamentals, case-study reasoning and business impact [S3][S4]. Treat as unverified beyond that [U].

**Level notes:** An ML Scientist posting lists level P40 with P30 and P50 as additional levels [S10]. India reports mention MTS-1 and MTS-2 titles for software roles; MTS-2 candidates are reportedly asked to present a business-impact project [S4] (anecdotal). Expectations by level are otherwise not found in sources.

**Preparation plan (2 weeks):**
- Days 1-3: SQL, cohorts, retention, window functions (Book 3 Parts 4, 5, 6, 8).
- Days 4-6: ML fundamentals and from-scratch coding (Book 1 Parts 8 and 12; Book 5 Part 1 arrays and hashing for the coding screen) [G].
- Days 7-9: Statistics, A/B testing, probability (Book 1 Parts 10, 13, 14).
- Days 10-11: ML system design and generative-AI design (Book 1 Part 11; Book 2 Parts 12 and 9).
- Days 12-13: Case study and project presentation practice (Book 6 Parts 4, 5, 10).
- Day 14: Mock loop and behavioural stories [G].

**Common mistakes:**
- Treating one candidate's round list as the process; reports disagree and teams differ [S2].
- Neglecting SQL because the role says ML; reports call SQL a heavy theme [S4].
- Presenting model accuracy without business impact for the case or manager rounds [S3][S4].
- Preparing only DSA for a Firefly-type role when guides list ML and generative-AI depth [S6] (unverified, third-party).

**Recent changes and AI-era notes:**
- A third-party guide says AI tools are generally not allowed in live Adobe software-engineering interviews unless the interviewer invites them or an accommodation is approved, and that Adobe asks candidates not to use AI recording or scribing tools [S11]. This is not an Adobe statement and concerns engineering interviews; confirm with the recruiter.
- A 2026-dated guide describes an AI-engineer loop with coding, ML depth and ML system design rounds [S6] (third-party).
- Report dates span 2015 to 2026; older reports (such as take-home analysis on an open dataset) may be out of date [S4].

**Sources:**
- S1. https://www.adobe.com/careers/interviewing-at-adobe : Adobe careers page; snippet-only, partly captured; supports that recruiters follow up after interviews. Seen 2026-10-31.
- S2. https://designgurus.io/answers/detail/how-many-rounds-of-interview-are-there-in-adobe : third-party answer; 4 to 6 rounds, team variation, recruiter call and manager screen as described in the search summary (several guides summarised together, per-URL attribution not visible); snippet-only. Seen 2026-10-31.
- S3. https://www.interviewquery.com/guides/adobe-data-scientist : DS loop as OA, technical, manager, director; SQL heavy; snippet-only. Seen 2026-10-31.
- S4. https://dataford.io/interview-guides/adobe/data-scientist/experiences : DS candidate reports (final round presentation, case study, fraud-detection design, India-based reports); the search summary also drew on Glassdoor India reviews, e.g. https://www.glassdoor.co.in/Interview/Adobe-Interview-E1090-RVW28151557.htm; per-claim mapping uncertain; snippet-only. Seen 2026-10-31.
- S5. https://interviewquery.com/interview-guides/adobe-machine-learning-engineer : ML engineer guide, ML design round, candidate coding reports; snippet-only. Seen 2026-10-31.
- S6. https://codemia.io/guides/adobe-ai-engineer : 2026 third-party guide for AI engineer loop (Firefly-era); snippet-only. Seen 2026-10-31.
- S7. https://www.teamblind.com/post/swe-interview-at-adobe-firefly-uyv1jj1q : anecdotal SWE Firefly loop; snippet-only. Seen 2026-10-31.
- S8. https://www.designgurus.io/answers/detail/what-is-the-adobe-interview-process-like-round-by-round : third-party; used for the 75-minute virtual technical interview report as summarised for software engineers; per-URL attribution uncertain; snippet-only. Seen 2026-10-31.
- S9. https://careers.adobe.com/us/en/job/R151663/Machine-Learning-Engineer : Adobe job posting for ML Engineer; supports roles existing; snippet-only. Seen 2026-10-31.
- S10. https://jobs.anitab.org/companies/adobe-software-2/jobs/49581714-machine-learning-scientist : job board posting, level P40; snippet-only. Seen 2026-10-31.
- S11. https://www.datainterview.com/blog/adobe-software-engineer-interview : third-party guide on AI-tool policy for live interviews; snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low to medium. Rounds, counts and timelines are third-party and anecdotal; the Adobe page gave little. Verify on adobe.com/careers and with your recruiter: the number of rounds for your team, whether a take-home or presentation is used, whether AI tools are allowed, and the India office loop (no Bangalore or Noida DS/ML-specific loop was found beyond a few reports) [U].

### C10 Salesforce (Big Tech)

**Evidence level:** Thin. No Salesforce-published process was found; sources are third-party guides and a small number of anonymous candidate reports that conflict on round counts [S1][S2].

**Roles seen in sources:** Data Scientist [S1]; Research Scientist / applied scientist (AI research) [S3][S4]; Machine Learning Engineer, including Hyderabad and Bangalore postings and Agentforce platform ML roles [S5][S6][S7]; India software engineer (MTS/SMTS) reports used as a proxy only, none ML-specific [S8].

**Process overview (as reported):**
1. Recruiter screen, consistently the first step, short call on resume and background [S1].
2. Technical phone screen or online coding assessment; for ML Engineer a guide describes a coding and problem-solving assessment (Python, ML frameworks) followed by an introductory interview [S5].
3. Technical rounds covering SQL, ML, statistics (Data Scientist) [S1]; ML theory and generative AI "under the hood" (ML Engineer, per a guide built from candidate reports) [S6].
4. Final or onsite rounds with behavioural questions often interspersed through each interview [S2]; for research roles, reviews describe a research screen then an onsite of 4 interviews [S4] (anecdotal).
- Round count: guides say 4, 6 or 7 rounds for Data Scientist [S1]; the process is described as decentralised, varying by team [S2].
- Duration of each round: not found in sources. End to end, 2 to 6 weeks by guides [S1][S2]; one 2023 applied scientist reviewer reported 2 months (anecdotal) [S3].

**Round by round:**

| Round | Format | What is tested | Evidence |
|---|---|---|---|
| Recruiter screen | Short phone call | Resume, qualifications, background | [S1] |
| Technical screen / assessment | Phone or online | SQL (DS); Python and ML coding (MLE) | [S1][S5] |
| Technical rounds | Interviews | ML, statistics, probability, DSA; ML theory and GenAI for MLE | [S1][S6] |
| Research / applied science onsite | 4 interviews per one review | ML basics, simple coding, system design, discussion of own research | [S4] |
| Final / behavioural | Interspersed or separate | Values and culture fit, past experience | [S1][S2] |

**Question types:**
- A guide's tally of reported DS question categories: data structures and algorithms, SQL, machine learning, probability, statistics (counts from the guide, not verified) [S1].
- Case-style business reasoning for Data Scientist in one guide's 4-round version [S1].
- Research roles: project deep-dives, ML and deep-learning fundamentals, easy-to-medium coding, implementing sparse self-attention (one anecdotal report) [S3][S4].
- India engineering reports (not ML): three medium coding problems in an hour, low-level design, system design [S8] (anecdotal).

**Sample questions (illustrative):**
- Write a SQL query for the top 3 accounts by monthly usage with a ranking window function. [illustrative] (Book 3 Part 4 window functions)
- Explain how you would predict opportunity win probability and validate it. [illustrative] (Book 1 Part 11 ML system design; Book 6 Part 5 business cases)
- Implement sparse self-attention and explain its trade-offs. [S3] (Book 2 Part 1 transformer internals)
- Describe a complex mathematical problem you solved, the methods used and the impact. [S3] (Book 6 Part 6 stakeholder trade-offs; Book 1 Part 13 statistics)
- Your RAG agent for customer support hallucinates account details; how do you evaluate and reduce it? [illustrative] (Book 2 Parts 6, 9 and 8; Book 6 Part 7 GenAI scenarios)
- Solve a medium graph or matrix BFS problem and state complexity. [S8] (Book 5 Part 9 graphs)
- Explain precision versus recall for lead scoring when positives are rare. [illustrative] (Book 6 Part 3 imbalanced data)

**What they score:** No published rubric. Sources point to technical depth (SQL, ML, coding), communication in ambiguous problems [S1] and culture and values fit [S1][S2]; for research roles, depth on your own work [S3].

**Level notes:** India engineering postings use MTS, SMTS and LMTS titles, and a Lead ML Engineer title appears [S7][S8]; Salesforce data-science level expectations were not found in sources [U]. Senior roles may add a panel interview [S2].

**Preparation plan (2 weeks):**
- Days 1-3: SQL and metrics (Book 3 Parts 3, 4, 6, 8).
- Days 4-6: ML fundamentals, statistics, probability (Book 1 Parts 3-5, 13, 14).
- Days 7-8: Coding practice at easy-to-medium level (Book 5 Parts 1, 7, 9) [G].
- Days 9-11: GenAI and agents, RAG evaluation (Book 2 Parts 6-9, 12) since Agentforce roles list LLM experience [S7].
- Days 12-13: Business case and behavioural stories (Book 6 Parts 5, 6, 10).
- Day 14: Project deep-dive rehearsal and mock [G].

**Common mistakes:**
- Assuming one round count; sources range from 4 to 7 [S1].
- Giving only technical answers when behavioural questions are woven into every round [S2].
- Skipping coding prep for DS roles, where DSA was the most-reported category in one guide [S1].
- Weak project narratives for research or applied roles [S3][S4].

**Recent changes and AI-era notes:**
- Salesforce postings say AI tools help recruiters assess resumes, and that humans make selection and hiring decisions [S9].
- No policy on candidates using AI tools in interviews was found; check with your recruiter [U].
- Current ML postings (for example November 2025) reference LLMs, prompt engineering and the Agentforce platform [S7]. Older candidate reports (2019 to 2023) predate this [S3][S8].

**Sources:**
- S1. https://www.interviewquery.com/interview-guides/salesforce-data-scientist : DS guide; round counts 4/6/7, question categories, 2-4 week timing; snippet-only. Seen 2026-10-31.
- S2. https://tryexponent.com/blog/salesforce-interview-process : third-party guide; search summary combined several guides (decentralised process, 3-6 weeks, behavioural interspersed, panel for senior roles); per-URL attribution uncertain; snippet-only. Seen 2026-10-31.
- S3. https://www.interviewquery.com/interview-guides/salesforce-research-scientist : research scientist guide and Glassdoor-based reports (2019, 2023, 2024 anecdotes); snippet-only. Seen 2026-10-31.
- S4. https://www.glassdoor.com.hk/Interview/Salesforce-Interview-E11159-RVW25902909.htm : anecdotal Glassdoor review, research screen plus 4-interview onsite (mapping among listed reviews uncertain); snippet-only. Seen 2026-10-31.
- S5. https://interviewquery.com/interview-guides/salesforce-machine-learning-engineer : ML engineer stages; snippet-only. Seen 2026-10-31.
- S6. https://dataford.io/interview-guides/salesforce/machine-learning-engineer : ML theory and generative AI emphasis, built from candidate reports; snippet-only. Seen 2026-10-31.
- S7. https://www.themuse.com/jobs/salesforce/machine-learning-engineer-hyderabad-bangalore : ML Engineer posting, Hyderabad and Bangalore, posted November 2025; snippet-only. Seen 2026-10-31.
- S8. https://leetcode.com/discuss/interview-experience/4205025/ : anecdotal SMTS Bengaluru October 2023 software-engineer report (one hour, three medium problems); snippet-only. Seen 2026-10-31.
- S9. https://builtin.com/job/lead-forward-deployed-engineer-agentforce/6225088 : Salesforce posting language on AI tools used by recruiters and human decisions (statement appeared across postings in results); snippet-only. Seen 2026-10-31.

**Confidence and what to verify:** Low. Verify with your recruiter: your team's round count and format, whether there is a take-home or live ML exercise, behavioural expectations, India (Hyderabad, Bangalore) loop details, and the policy on AI tools. No India DS/ML-specific interview rounds were found [U].
