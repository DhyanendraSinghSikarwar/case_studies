# Wave A instructions — Book 12 (Portfolio, Resume, LinkedIn/Naukri & Job Search): guide outline + frozen FAQ list

Book 12 = a GUIDE (6 content sections + a FAQ section) plus about 100 FAQs, same shape as Book 0 (see `Book00_CareerSwitch_Process/Book00_Guide_Outline.md`, `Book00_FAQs.md` for format only; do not copy their questions). Reader: a non-technical HR professional switching to data analytics in Hyderabad/Bengaluru, targeting Rs 6-10 LPA. Today is 2026-11-26.

Read first: `plan.md` (Sections 1-6, 9; Book 12 table), `style_guide.md` (Sections 1, 8), `research/market_skills_2026.md` (MS), `research/interview_processes.md` (IP), `research/Book00_sources.md`, and `Book00_CareerSwitch_Process/Book00_FAQs.md` (grep "Book 12" to see what Book 0 already points here; do not duplicate Book 0 questions, point to them).

## Section map (stay inside YOUR sections; other agents own the rest)
| Sec | Topic | FAQ target |
|---|---|---|
| 1 | ATS-friendly resume for career switchers; translating HR work into analytics achievements; summary, bullets, skills section, formats, gaps, one page vs two, cover letter | 24 |
| 2 | 5 portfolio projects (HR attrition, sales dashboard, SQL case, Python EDA, guesstimate deck): choosing data (public/synthetic only, no employer data), GitHub/Power BI/Tableau Public publishing, README, how to present in interview | 24 |
| 3 | LinkedIn and Naukri profile optimisation; keywords from JDs; headline, About, skills, open-to-work, profile-visibility, search behaviour | 18 |
| 4 | Referrals, cold outreach templates, recruiter messages, networking, follow-ups, consultancies/staffing firms | 18 |
| 5 | Certifications (PL-300, Google Data Analytics, others): MS says none is named in any JD sample, so value is unverified; cost/time only from official pages | 10 |
| 6 | Application tracker and weekly job-search routine; also job-search hygiene (where to apply, volume, response tracking, rejection handling, notice period overlap) | 14 |
Agent split: A12a = Sections 1 and 2; A12b = Sections 3 and 4; A12c = Sections 5 and 6.

## Evidence rules (strict, same as Book 0)
- A number, percentage, price, platform feature or company claim may appear in the outline or a question ONLY if it is in the research files, or in an official page you read via search snippet and cite as "snippet only". Everything from blogs/vendors/forums is "unverified". Where nothing reliable exists (ATS pass rates, callback rates, certificate value in India, recruiter behaviour), the outline says "No reliable data found" and plans a decision rule instead. No invented statistics, quotes, success stories.
- Never plan advice that needs the reader to use employer data or confidential material, to fabricate experience, or to game systems deceptively (for example hidden keyword text). Say so in the outline.

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred; WebFetch is unavailable). At least 8 distinct searches for your two sections, e.g. "ATS friendly resume data analyst fresher India career change", "resume bullets data analyst career switch HR", "data analyst portfolio projects for freshers India", "Naukri profile optimization data analyst", "LinkedIn cold message referral template data analyst", "PL-300 exam cost duration", "Google Data Analytics certificate duration", plus 2025/2026 variants. LinkedIn/Naukri/Glassdoor/Reddit may be blocked; record that.
2. Record every source in `research/Book12_<id>_sources.md`: URL, what it was used for, type (official/vendor/blog/forum), recency, honest note that it was search-snippet only. State limits. Give star-assignment reasoning.
3. If you cannot research, STOP, write nothing, and report why.

## Files you write (only these; mkdir -p)
1. `Book12_Portfolio_JobSearch/wave_a/Outline_<id>.md`: for each of your sections: what the guide section will contain (bullets, tables to include, worked examples to build, what evidence supports each point with a source pointer, "No reliable data found" items, honest limitations, cross-book pointers by number: Book 1 Excel, 2 SQL, 3 Python, 4 Power BI, 5 Stats, 6 Aptitude, 7 Guesstimates/Cases, 8 Scenarios (Part 8 project walk-through), 9 ML/AI, 10 Domain, 11 Soft skills, 0 Career switch guide). About 40-70 lines per section.
2. `Book12_Portfolio_JobSearch/wave_a/FAQ_<id>.md`: the FROZEN FAQ questions for your sections, grouped under `## Section N` headings, each:
```
### Q<n> ⭐⭐⭐ 🟢 <canonical question, as a candidate would ask it>
<!-- ANSWER_PENDING -->
```
Number Q1.. continuously inside your file (the lead renumbers globally later); order inside each section: ⭐⭐⭐ then ⭐⭐ then ⭐, 🟢 then 🟡 then 🔴. File header: `# Book 12 FAQs (<id>): Sections ..`, target, actual, scope. Stars: judgement unless a source gives frequency; say so in the sources file. Include practical "how do I..." and "should I..." questions and a few interview-facing ones (for example "Walk me through your portfolio project", "Why does your resume show no analytics experience?"). Questions may include a short inline example where the answer needs data (for example a resume bullet to rewrite); keep them self-contained.
3. `research/Book12_<id>_sources.md`.
Do not touch any other file. Scratch: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/A12_<id>` (yours only). No git commits.

## Final reply (short)
Files, FAQ count vs target, number of searches, which sources were blocked, anything uncertain.
