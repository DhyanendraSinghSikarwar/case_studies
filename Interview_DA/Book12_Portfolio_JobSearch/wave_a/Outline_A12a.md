# Book 12 Guide Outline (A12a): Sections 1 and 2

Abbreviations: MS = research/market_skills_2026.md; IP = research/interview_processes.md; B12S = research/Book12_A12a_sources.md (all web items are search-snippet only, vendor/blog unless marked official). Rule: a number appears only if it is in MS/IP or marked "snippet only" or "unverified". Reader: non-technical HR professional, Hyderabad/Bengaluru, Rs 6-10 LPA target. Cross-book: Book 0 guide Section 5 (HR as advantage, translation table), Book 0 Q14, Q19, Q26, Q28, Q53, Q55, Q83, Q84, Q100 already answer neighbouring questions; this guide points to them.

## Section 1 - ATS-friendly resume for career switchers

### 1.1 What an ATS is and what we can honestly say about it
- ATS = applicant tracking system: software where employers store applications and search them. Explain in plain words.
- Evidence: blogs agree on plain single-column layout, standard headings, no text in images, PDF or Word text (B12S, vendor, unverified). Parsing behaviour differs by system.
- **No reliable data found** on ATS pass rates, rejection-by-ATS rates, or how Indian portals (Naukri, LinkedIn) rank resumes. The guide says so and gives a decision rule instead: make the resume readable by both a machine and a person in 30 seconds; test it with the copy-paste check (1.7).
- Honest limit: a human recruiter or hiring manager usually decides; no source we could read gives screening time per resume. Do not quote "6 seconds" style claims.

### 1.2 Structure for a career switcher
- Table: section / what goes in / why. Order: header (name, phone, email, city, LinkedIn, GitHub/portfolio link) -> 3-line summary -> skills -> projects -> experience -> education -> certificates (short).
- Rule of thumb: projects above experience for the first applications because the HR job title does not signal analytics; hybrid format (skills + projects first, then reverse-chronological jobs). Source: blogs only (B12S), unverified; our own decision rule.
- Header: no photo, no date of birth, no marital status as the default; reason is simplicity, not a sourced rule. **No reliable data found** on what Indian recruiters prefer; plan states it as our recommendation and tells the reader to follow the employer's form if it asks.
- Reverse-chronological vs hybrid vs functional: functional (skills only, no dates) hides history and reads as evasive; hybrid works if each skill is tied to concrete work (B12S, snippet).

### 1.3 Translating HR work into analytics achievements (worked examples)
- Bullet formula: verb + what you analysed/built + tool + size of data + result or decision. Source: blog formula (B12S), used as a template, not as evidence.
- Build a before/after table of 12 HR tasks (attrition report, headcount MIS, attendance/payroll reconciliation, hiring-funnel tracker, engagement survey, exit-interview themes, compliance tracker, offer-to-join tracking, training effectiveness, HRIS data clean-up, absenteeism, recruitment cost). Each: duty version, analytics version, which tool the reader must really have used.
- Honesty rules: never invent numbers; use "approx." with the real method; if the reader did not use SQL/Power BI at work, the bullet says Excel and the project holds the SQL/Power BI. Never claim a tool you cannot demo.
- Worked example with placeholders the reader fills (clearly labelled illustrative, not a sourced result): "Built a monthly attrition report in Excel for ~[N] employees across [N] teams; found [pattern]; HR head used it to [decision]".
- Pointer: Book 0 Q83 (translation), Q26 (title still HR); Book 10 Part 1 for HR metric definitions.

### 1.4 Summary, skills section, keywords
- Summary: 3 lines = who you are (HR professional with N years in [area]) + tools you can show (Excel, SQL, Power BI) + the target role. Two templates, one weak/one strong, in a table.
- Skills section: grouped list (Analysis: Excel, SQL; Visualisation: Power BI; Other), no bars or percentages (cannot be verified, blogs call them weak; opinion). Order by the target JD.
- Keyword method: open 10 real JDs for the target role, count tools named (ties to MS: Excel 60%, SQL 54%, dashboards/reporting 75%, communication 73%, Power BI 40%, Python 32%, n=186, +/-7 pts). Use only keywords the reader can demo. Show a small tally table template.
- **Ethics box:** no hidden white text, no pasting the JD into the resume, no listing tools never used. Sources: Built In, Fortune snippets say it backfires and some systems expose hidden text; detection percentages (10% vs 1%) are vendor claims and are not used. The guide's reason is integrity first.

### 1.5 Length, formats, gaps, certificates, cover letter
- One vs two pages: Monster/CBS snippets say one page for under about 10 years or career changers; ResumeGo 2018 (482 respondents, US, simulated, author sells resumes) favoured two pages. Decision rule: one page unless a second page carries relevant evidence; no India data found.
- File: PDF with selectable text, name_role.pdf; Word only if the employer asks. Blogs only.
- Gaps: label briefly (e.g. career break, caregiving, study), keep personal detail private, show any learning/projects done in the gap (snippet sources, general not analytics-specific). Interview side: Book 0 Q84, Book 11 Part 8.
- Certificates: short block; PL-300/Google DA not named in any JD in MS (unverified value); full treatment is Section 5 (A12c). Here: list only what was completed, with month/year.
- Cover letter: optional unless asked; 3 short paragraphs (why this role, evidence from one project/work, ask). No data on whether Indian recruiters read them: **No reliable data found**; decision rule: send one when applying directly by email or to a named person, skip when a portal does not ask.

### 1.6 Interview-facing resume questions
- "Your resume shows no analytics experience": answer frame (transferable work + proof project + target role), cross-link Book 11 Part 1 and Book 0 Q19.
- "Explain this bullet": every line must survive 3 follow-ups; exercise: reader writes the follow-ups to each bullet.

### 1.7 Checks and tools
- Copy-paste test: paste resume into a plain text editor; order and words must survive. Our own method.
- ATS score checkers and AI builders: vendor products, claims unverified; use at most for spotting typos/formatting; never to add skills.
- AI rewriting: allowed for wording; reader verifies every number/tool; model may invent claims (point to Book 9 Part 9 on verifying AI output).

### 1.8 Honest limitations of Section 1
- All resume advice here is blog/vendor-grade and US/global; no Indian ATS or recruiter-behaviour data. Callback rates: **No reliable data found**. Examples are illustrative templates, not real candidates.

## Section 2 - Five portfolio projects

### 2.1 Purpose and rules
- Portfolio = proof you can do the tasks in the JD; gets a conversation, not an offer (blog opinion, snippet). Evidence: project/resume walk-through appears in about 14 of 20 interview profiles (IP Section 4, candidate-reported). Book 0 Q14 holds the "how many" rule; this section builds them.
- **Data rule box (strict):** public or synthetic data only. Never employer data, candidate/employee records, salary files, screenshots of internal dashboards, even anonymised or "just the structure". Never fabricated results presented as real. Anything with names, phone numbers, salaries of real people is out. Say why: confidentiality and legal risk (general statement, not legal advice).
- Order for an HR switcher: (1) HR attrition dashboard, (2) SQL case, (3) sales dashboard or Python EDA by target role (MIS/reporting -> sales/ops dashboard in Excel/Power BI; BI/DA -> Python EDA); guesstimate deck as a differentiator. Decision rule from MS role-tool table (Section 6 of MS); no outcome data.

### 2.2 Choosing data safely
- Table: source / what it is / licence / caution. Include: IBM HR attrition sample (fictional, about 1,470 rows x 35 columns per snippets; licence loosely specified; verify by loading it; patterns are designed, so do not claim real-world causes), data.gov.in (GODL licence notified 2017 per secondary snippets; read the licence and each dataset page), Kaggle datasets (read each licence), self-generated synthetic data (disclose in README).
- Worked example to build and run (Wave B): generate a small synthetic HR table in Python/Excel and state the generating rules.
- Cite source, date downloaded and licence in every README.

### 2.3 The five projects (one sub-section each; each has question, data, steps, outputs, README bullets, 5 likely interview follow-ups)
1. HR attrition: question "Which groups leave most and when?"; KPIs: attrition rate definition (leavers / average headcount, state the formula), by tenure band, department, overtime flag; Excel or Power BI dashboard; no causal claims. Pointers: Book 10 Part 1, Book 4, Book 5 Part 7 (correlation vs causation).
2. Sales dashboard: public retail/sales sample; star schema basics, 3-5 KPIs, one insight and one recommendation; Power BI Desktop or Tableau Public. Pointers: Book 4 Parts 3, 8, 9.
3. SQL case: 8-10 business questions on a small multi-table database (SQLite/Postgres); joins, GROUP BY, window function, CTE; .sql file plus query-result screenshots. Pointers: Book 2.
4. Python EDA: one notebook; load, clean (missing, duplicates, types), 5 charts, 3 findings in words; no model required. Pointers: Book 3 Parts 4-9.
5. Guesstimate deck: 5-8 slides, one sizing question (assumptions table, top-down and bottom-up, sanity check); all base numbers labelled assumptions. Pointers: Book 7.
- Time box per project (our suggestion, not sourced): finish a first version, publish, then improve; stop when README and 3 follow-ups are covered.

### 2.4 Publishing
- GitHub: create account, repo per project, README at root (GitHub Docs snippet: README tells visitors what the project is for and how to use it; found in .github, root or docs). Contents checklist (our rule): problem, data source + licence, tools, steps, 3 findings, screenshots, how to reproduce, limitations. Folder layout template. Commit only data you are allowed to share; large/licence-restricted data: link, do not copy. Pointer: Book 0 Q100; Book 3 Part 11 (Jupyter).
- Tableau Public: free; Desktop Public Edition or web authoring; everything including underlying data becomes public (official help page, snippet only; edition wording differs across help pages: tell reader to check the current page).
- Power BI: publish-to-web makes the report viewable by anyone with no sign-in, warns against confidential data, needs a licence and an admin-enabled tenant setting (Microsoft Learn, snippet only; wording revised Jul 2025 per community posts). Work/school-account limits: **No reliable data found** on what a free personal account can do; plan shows alternatives: PDF export, screenshots, short screen recording, .pbix on GitHub (check size and data licence). Never publish to web with HR data.
- Where to link: resume header, LinkedIn Featured (Section 3 by A12b), GitHub profile pin.

### 2.5 Presenting a project in the interview
- 90-second structure: business question -> data -> what you did (tools, one hard problem) -> finding -> what you would do next / limitation. Sources: blog guidance (short context, tools in Action, concrete result; STAR as backbone but critics say too story-like; "I" vs "we"). No timing data used.
- Worked example script (illustrative) for the HR attrition project, plus 10 follow-up questions with answer skeletons: define attrition rate, why that chart, what if data is wrong, did you follow a tutorial, limitations, what would you change, how to scale, who is the audience. Pointers: Book 8 Part 8 (project deep-dive), Book 11 Parts 1-2, Book 0 Q28.
- Honest-answer rules: say which parts followed a tutorial; never claim business impact that did not happen ("if this were live, the HR head could...").
- Self-check list: can you re-create the key number by hand from 10 rows? can you explain every chart's axis and filter?

### 2.6 Honest limitations of Section 2
- No data found on how much recruiters in India value GitHub or public dashboards; **No reliable data found**. Project ideas come from vendor blogs. Dataset licences were not read directly: answers must tell the reader to read them. Tool-feature facts (Tableau Public, Power BI publish) are snippet-level and must be marked "check the current page".
