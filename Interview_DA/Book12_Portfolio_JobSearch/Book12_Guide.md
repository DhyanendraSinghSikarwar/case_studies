# Book 12: Portfolio, Resume, LinkedIn/Naukri & Job Search (HR to Data Analyst)

**Reader:** a non-technical HR professional switching to data analytics. **Target roles:** Data Analyst, Business Analyst, MIS/Reporting, BI, Product/Operations and People/HR Analytics. **Target cities:** Hyderabad and Bengaluru (also Pune, Chennai, NCR). **Pay target:** Rs 6-10 LPA (see Book 0 for what the research says about pay).

**How to read this guide.** Every number comes from the series' own research files (`research/`), with its confidence label next to it. Job-description percentages are from a pooled, non-random sample (n=186, about +/-7 points). Interview processes are anonymous and candidate-reported. Resume, LinkedIn, Naukri, outreach and certificate advice comes from blogs, vendors and platform help pages that we read only as search snippets, so it is labelled "unverified" or "snippet only, check the live page". Where no reliable data exists (ATS pass rates, callback and reply rates, certificate value in India, recruiter behaviour), the guide says "No reliable data found" and gives a decision rule you can apply yourself. Platform limits, prices and settings change: always check the live page. Routines, timelines and the 10-application rule are our own design, not research findings. Today is 2026-11-26.

**Ground rules this guide never breaks.** Use only public or synthetic data in a portfolio, never your employer's data. Never claim experience or numbers you do not have. Never hide keywords or pad a resume to fool a system. Never pay anyone for a job (see Section 4). Legal and policy points (confidentiality, notice period, platform terms) are general information, not legal advice: confirm with HR, a lawyer or the platform.

**Contents**
1. An ATS-friendly resume for a career switcher
2. Five portfolio projects
3. LinkedIn and Naukri profile optimisation
4. Referrals, cold outreach, recruiters, networking and consultancies
5. Certifications (PL-300, Google Data Analytics and others)
6. Application tracker, weekly routine and job-search hygiene
7. The 108 FAQs: how to use them (answers in `Book12_FAQs.md`)

Cross-references: "Book N Part M" points to the other books in this series (Book 0 Career switch guide and FAQs; Book 1 Excel; Book 2 SQL; Book 3 Python; Book 4 Power BI; Book 5 Stats; Book 7 Guesstimates and cases; Book 8 Scenarios; Book 9 ML and AI; Book 10 Domain; Book 11 Soft skills). "Q" numbers in this book mean the FAQs in `Book12_FAQs.md`, unless written "Book 0 Q".

---

## Section 1. An ATS-friendly resume for a career switcher

**Evidence labels used in this section.** "Blog/vendor, unverified" = advice from resume-builder, training or career blogs that we read only as search snippets (A12a sources), consistent with each other but never measured. "JD percentages" = pooled sample of 186 job descriptions, non-random, about +/-7 points (MS Addendum). Everything labelled "illustrative" is an invented example for demonstration, not a result and not a real candidate.

### 1.1 What an ATS is, and what we can honestly say about it

An **ATS (applicant tracking system)** is software an employer uses to collect applications, store resumes and let recruiters search and filter them. Think of it as the employer's shared inbox with a search box.

- Blogs agree on the same layout advice: plain single-column layout, standard headings (Skills, Projects, Experience, Education), no text inside images, a PDF or Word file with real selectable text (blog/vendor, unverified). Different systems read files differently, so no layout is guaranteed.
- **No reliable data found** on ATS pass rates, how many resumes an ATS rejects, or how Naukri and LinkedIn rank resumes. Any blog number on these is a vendor claim.
- Honest limit: a recruiter or hiring manager usually makes the decision, but no source we could read gives screening time per resume. Do not trust "recruiters look for 6 seconds" type claims.

**Decision rule:** make a resume that a machine can read and a person can understand in about half a minute (our rule, not a measured figure). Test it with the copy-paste check in 1.7.

### 1.2 Structure for a career switcher

Your job title says HR, so the first screen of the resume must carry the analytics proof. Use a hybrid layout: skills and projects first, then jobs in reverse-chronological order (latest first).

| Section | What goes in | Why |
|---|---|---|
| Header | Name, phone, email, city, LinkedIn link, GitHub or portfolio link | Recruiter can contact you and open your proof |
| Summary (3 lines) | Who you are, tools you can demo, target role | Tells the reader how to read the rest |
| Skills | Grouped list of tools you can demo | Quick keyword match for people and software |
| Projects | 2 to 3 best projects, one or two lines each, with link | Your analytics proof while your job title is HR |
| Experience | HR roles rewritten with data work (see 1.3) | Shows real working history and domain knowledge |
| Education | Degree, college, year | Standard |
| Certificates | Only completed ones, month and year | Short; see Section 5 |

- Projects above experience for the first applications is our decision rule. Blogs suggest the same (blog/vendor, unverified); no India outcome data exists.
- **Functional format** (skills only, no dates) hides your history and tends to read as evasive; hybrid works only if each skill is tied to concrete work (both are blog snippet opinion, unverified).
- Header: by default leave out photo, date of birth and marital status. The reason is simplicity, not a sourced rule. **No reliable data found** on what Indian recruiters prefer. If an employer's form asks for something, follow the form.

### 1.3 Translating HR work into analytics achievements

Bullet formula: **verb + what you analysed or built + tool + size of data + result or decision.** This formula comes from blogs (unverified) and is a template, not evidence. Book 0 Guide Section 5 has a short translation table and Book 0 Q83 and Q26 answer the same question briefly; this table goes deeper. Book 10 Part 1 defines the HR metrics.

**Honesty rules (read before copying anything):**

- Every line must be something you did. The right column shows what tool you must really have used for the line to be true.
- If you did not use SQL or Power BI at work, the bullet says Excel, and the SQL or Power BI skill lives in a project instead. Never list a tool you cannot demo.
- If you do not remember exact numbers, use scale ("monthly report for 3 business units") or "approx." and say how you estimated it. Do not guess a percentage. If asked "how did you calculate that?" you must be able to answer.

| HR task | Duty version (weak) | Analytics version (illustrative) | Tool you must really have used |
|---|---|---|---|
| Attrition report | Responsible for attrition reporting | Built a monthly attrition report for approx. [N] employees across [N] teams; found [pattern]; HR head used it to [decision] | Excel pivots |
| Headcount MIS | Prepared headcount MIS | Maintained a monthly headcount MIS covering [N] locations; reconciled it with payroll before release | Excel, lookups |
| Attendance/payroll reconciliation | Checked attendance against payroll | Matched attendance and payroll records for [N] employees; traced [N] mismatches to [cause] and fixed the source | Excel, lookups or Power Query |
| Hiring funnel tracker | Tracked recruitment status | Built a funnel tracker (applied, interviewed, offered, joined) by role; showed the largest drop-off at [stage] | Excel or Sheets |
| Engagement survey | Ran the engagement survey | Summarised scores from [N] responses by team; grouped comments into [N] themes; presented drivers to leadership | Excel, survey tool |
| Exit-interview themes | Conducted exit interviews | Coded [N] exit interviews into themes and counted reasons by department | Excel |
| Compliance tracker | Tracked compliance dates | Built a due-date tracker with alerts for [N] items; [add "no missed deadlines in [period]" only if that is true] | Excel |
| Offer-to-join tracking | Followed up with candidates | Tracked offer-to-join ratio by source; shared findings with the recruiting team | Excel |
| Training effectiveness | Organised training | Compared [score or metric] before and after training for [N] participants | Excel |
| HRIS data clean-up | Updated employee records | Cleaned duplicate and missing fields in [N] HRIS records; documented the rules used | HRIS export, Excel |
| Absenteeism | Monitored leave | Analysed leave and absence by team and weekday; flagged [pattern] to managers | Excel pivots |
| Recruitment cost | Managed hiring budget | Calculated cost per hire by channel for [period]; suggested shifting effort to [channel] | Excel |

**Worked example (illustrative, replace every bracket with your true facts):** "Built a monthly attrition report in Excel for approx. [N] employees across [N] teams; found that [pattern, for example exits cluster in the first year]; HR head used it to [decision, for example change onboarding follow-up]." If no decision followed, write the report and the finding, and stop. Do not add an outcome that did not happen.

### 1.4 Summary, skills section and keywords

| | Weak summary (illustrative) | Strong summary (illustrative) |
|---|---|---|
| Text | "Hardworking HR professional seeking a challenging role in a reputed organisation." | "HR professional with [N] years in [area] who builds attrition and hiring reports in Excel and is completing SQL and Power BI projects (links below). Targeting MIS, reporting and junior data analyst roles." |
| Why | Says nothing checkable | States background, tools you can show, and target |

- **Skills section:** grouped list (Analysis: Excel, SQL; Visualisation: Power BI; Other: communication). Skip skill bars and percentages: nobody can verify them, and this is our judgement, in line with blog opinion (unverified). Order the groups by the target job description.
- **Keyword method:** open 10 real job descriptions (JDs) for your target role and tally which tools they name. For scale, the pooled sample (n=186, non-random, about +/-7 points) names dashboards/reporting in 75%, communication 73%, Excel 60%, SQL 54%, Power BI 40%, Python 32% (MS Addendum). Your own 10 JDs matter more for your target.

| Tool or skill | Named in how many of my 10 JDs | Can I demo it? (yes/no) | On my resume? |
|---|---|---|---|
| Excel | | | |
| SQL | | | |
| Power BI | | | |

Use only keywords you can demo.

> **Ethics box.** Do not hide white-text keywords, paste the whole JD into your resume, or list tools you never used. News and vendor snippets say these tricks backfire and some systems expose hidden text (Built In, Fortune, Jobscan; snippets only). Vendor detection percentages are not used here. Our reason is integrity first: if it is not true, it does not go on the page.

### 1.5 Length, file, gaps, certificates, cover letter

- **Pages:** Monster, CBS and Dice snippets say one page for career changers and for under about 10 years of experience. A ResumeGo 2018 study (482 respondents, US, simulated resumes, author sells resume services) favoured two pages. None is India data. **Decision rule:** one page unless a second page carries relevant evidence.
- **File:** PDF with selectable text, named like `Name_DataAnalyst.pdf`. Send Word only if the employer asks (blog/vendor, unverified).
- **Gaps:** label them briefly ("career break", "caregiving", "full-time study"), keep personal detail private, and show any learning or projects done in the gap (general advice snippets, not analytics-specific; no callback figure used). Interview side: Book 0 Q84 and Book 11 Part 8.
- **Certificates:** list only what you completed, with month and year. No analytics certificate (PL-300, Google Data Analytics) was named in any JD in our samples, so its hiring value is unverified. Full treatment is Section 5.
- **Cover letter:** optional unless asked. If you write one, keep it to three short paragraphs: why this role, evidence from one project or piece of work, and your ask. **No reliable data found** on whether Indian recruiters read them. Decision rule: send one when applying by email or to a named person; skip it when a portal does not ask.

### 1.6 Interview-facing resume questions

- **"Your resume shows no analytics experience."** Frame: transferable work (reports and data you already handled), proof project (link), and target role. Say it aloud in plain words: "My title was HR, but [N] years of my work was [reporting task] in [tool]. To show the analytics side I built [project], and I am targeting [role]." Fill the brackets with true facts. See Book 11 Part 1 and Book 0 Q19.
- **"Explain this bullet."** Every line must survive three follow-ups. Exercise: under each bullet write the three questions an interviewer would ask (How did you get the data? How did you calculate it? What did the manager do with it?) and write true answers. Delete any bullet you cannot defend.

### 1.7 Checks and tools

- **Copy-paste test (our own method):** paste the resume into a plain text editor. If the order or words break, a machine may also read it badly.
- **ATS score checkers and AI resume builders** are vendor products and their claims are unverified. Use them at most to spot typos and formatting problems, never to add skills.
- **AI rewriting** is fine for wording. You must verify every number and tool afterwards, because a model can invent claims. See Book 9 Part 9 on verifying AI output.

### 1.8 Limitations (Section 1)

- All resume advice here is blog/vendor-grade and mostly US or global; nothing is measured for India. **No reliable data found** on callback rates, ATS behaviour of Indian portals or recruiter preferences.
- Search snippets only; no page was read in full. Examples are illustrative templates, not real candidates.

**Checklist**
- Resume is single column, standard headings, selectable text, one page.
- Projects with links sit above HR experience.
- Every bullet is true, names the tool you really used, and has no invented number.
- Skills list contains only tools you can demo, matched to 10 real JDs.
- Copy-paste test passed; you can answer three follow-ups per bullet.

---

## Section 2. Five portfolio projects

### 2.1 Purpose and rules

A **portfolio** is a small set of projects showing you can do the tasks in the job description. Blog opinion (snippet, unverified) is that it earns a conversation, not an offer. The one sourced anchor: a project or resume walk-through appears in about 14 of 20 company interview profiles (IP Section 4, candidate-reported, not a statistical sample). Book 0 Q14 holds the "how many" rule (2 to 3 first, our rule of thumb, no data on how many are enough); this section builds them.

> **Data rule (strict).** Use only public or synthetic (invented) data. Never use employer data, candidate or employee records, salary files or screenshots of internal dashboards, even anonymised or "just the structure". Anything with real names, phone numbers or salaries of real people is out. Never present made-up results as real. Reason: confidentiality and possible legal risk (general statement, not legal advice; confirm with HR/legal).

**Order for an HR switcher** (our decision rule, based on the role-tool table in MS Section 6; no outcome data): (1) HR attrition dashboard, (2) SQL case, (3) by target role: for MIS/reporting a sales or operations dashboard in Excel or Power BI, for BI or data analyst roles a Python EDA, then (4) the other, and (5) a guesstimate deck as a differentiator. In the MIS/people sample (32 JDs, wider error margin, about +/-17 points) Excel is 72% and Python 16%; in the Bengaluru (42 JDs) and GCC (25 JDs) samples Python is 40% and in the Hyderabad sample (47 JDs) 30% (MS Addendum per-sample column; the pooled n=186 is non-random, about +/-7 points, and each sub-sample is smaller and less certain).

### 2.2 Choosing data safely

| Source | What it is | Licence | Caution |
|---|---|---|---|
| IBM HR attrition sample | Fictional HR table, about 1,470 rows x 35 columns per snippets (IEEE DataPort, wiki, HR blog) | Loosely specified; a GitHub copy lists Open Dataset terms (snippet) | Load it and check size yourself. Patterns are designed in, so never claim real-world causes |
| data.gov.in | Indian government open data portal | GODL (Government Open Data Licence), notified 2017 per secondary snippets | Licence text not read by us. Read the licence and each dataset page |
| Kaggle datasets | Community datasets | Varies per dataset | Kaggle licence field not retrieved; read each licence before use |
| Self-made synthetic data | Table you generate with stated rules | Yours | State in the README that it is invented and how |

**Worked example, run and checked (illustrative data).** This code invents 200 employees with two stated rules (Support leaves more often; leavers go within 1 to 3 years) and counts leavers per department. Run on this seed it produced this output (the numbers belong to this invented table only and say nothing about real companies):

```python
# Make a small invented HR table so no real person's data is used.
import random
import csv

random.seed(42)  # same seed gives the same table every time

departments = ["Sales", "Support", "Tech", "Finance"]
rows = []
for employee_number in range(1, 201):
    department = random.choice(departments)
    joining_year = random.randint(2019, 2025)
    # Rule 1 (invented): Support has a higher chance of leaving
    chance_of_leaving = 0.30 if department == "Support" else 0.12
    has_left = random.random() < chance_of_leaving
    # Rule 2 (invented): leavers go after 1 to 3 years
    years_in_company = random.randint(1, 3) if has_left else random.randint(1, 6)
    rows.append([employee_number, department, joining_year, years_in_company, "Yes" if has_left else "No"])

with open("synthetic_hr.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["employee_id", "department", "joining_year", "years_in_company", "left"])
    writer.writerows(rows)

# Leavers divided by headcount, per department
for department in departments:
    group = [r for r in rows if r[1] == department]
    leavers = [r for r in group if r[4] == "Yes"]
    print(department, "headcount", len(group), "leavers", len(leavers),
          "rate", round(100 * len(leavers) / len(group), 1))
```

```text
Sales headcount 51 leavers 4 rate 7.8
Support headcount 51 leavers 22 rate 43.1
Tech headcount 58 leavers 5 rate 8.6
Finance headcount 40 leavers 6 rate 15.0
```

In plain words: the Support rate is high because we wrote that rule; a dashboard on this table can show the rule back to you, not a real cause. That is why the README must say "synthetic". Cite source, date downloaded and licence in every README.

### 2.3 The five projects

Time box (our suggestion, not sourced): finish a first version, publish it, then improve. Stop when the README is written and you can answer the five follow-ups below.

**Project 1. HR attrition dashboard**
- **Question:** which groups leave most, and when?
- **Data:** IBM sample or your synthetic table (2.2).
- **Steps:** state the formula (attrition rate = leavers / average headcount in the period; a simple version divides by headcount, say which you used); cut by tenure band, department, overtime flag if present; build a one-page dashboard in Excel or Power BI; write 3 findings. No causal claims.
- **README bullets:** question, formula, data note (synthetic or licensed), 3 findings, limits.
- **Follow-ups:** Why average headcount? What if the data is wrong? Why this chart? What would you change? Correlation or cause?
- **Pointers:** Book 10 Part 1, Book 4, Book 5 Part 7.

**Project 2. Sales dashboard**
- **Question:** which products or regions drive sales, and where is the drop?
- **Data:** a public retail or sales sample (check its licence).
- **Steps:** simple star schema (one fact table of sales plus lookup tables for product, date, region), 3 to 5 KPIs, one insight and one recommendation; Power BI Desktop or Tableau Public.
- **Follow-ups:** Why these KPIs? What is a measure? How is the model joined? Who is the audience? What is missing?
- **Pointers:** Book 4 Parts 3, 8, 9.

**Project 3. SQL case**
- **Question set:** 8 to 10 business questions on a small multi-table database (SQLite or Postgres).
- **Steps:** joins, GROUP BY, one window function, one CTE; keep a `.sql` file plus screenshots of results.
- **Follow-ups:** INNER vs LEFT join? What if keys repeat? Why a CTE? How do you check the count?
- **Pointers:** Book 2.

**Project 4. Python EDA** (EDA = exploratory data analysis: looking at data to see what is in it)
- **Steps:** one notebook; load, clean (missing values, duplicates, data types), 5 charts, 3 findings in plain words; no model needed.
- **Follow-ups:** How did you treat missing values? Why that chart? Any outliers? What would you do next?
- **Pointers:** Book 3 Parts 4 to 9.

**Project 5. Guesstimate deck**
- **Steps:** 5 to 8 slides, one sizing question, assumptions table, top-down and bottom-up estimate, sanity check. Label every base number "assumption".
- **Follow-ups:** Which assumption matters most? How would you check it? Why two methods?
- **Pointers:** Book 7.

### 2.4 Publishing

- **GitHub (a site that stores project files):** make an account and one **repository** (project folder) per project. A **README** is the front-page text file; GitHub Docs says it tells visitors what the project is for and how to use it, and it can sit in the root, `.github` or `docs` folder (official, snippet only). What the README should contain is our checklist: problem, data source and licence, tools, steps, 3 findings, screenshots, how to reproduce, limitations.

```text
hr-attrition-dashboard/
  README.md
  data/          (only data you may share; otherwise a link)
  notebooks/ or sql/
  images/        (dashboard screenshots)
```

  Commit only data you are allowed to share; for large or restricted data, link and do not copy. See Book 0 Q100 and Book 3 Part 11 (Jupyter).
- **Tableau Public:** free; save from Tableau Desktop Public Edition or web authoring. Everything, including the underlying data, becomes public (official help page, snippet only). Help pages differ on which edition can publish: check the current page.
- **Power BI:** Publish to web lets anyone on the internet view the report with no sign-in, warns against confidential data, and needs a licence and an admin-enabled tenant setting (Microsoft Learn, snippet only; wording was revised in July 2025 per community posts). **No reliable data found** on what a free personal account can do. Alternatives: PDF export, screenshots, a short screen recording, or the `.pbix` file on GitHub (check file size and data licence). Never publish HR data to the web.
- **Where to link:** resume header, LinkedIn Featured section (Section 3), pinned repositories on your GitHub profile.

### 2.5 Presenting a project in the interview

**90-second structure** (blog guidance, unverified; no timing data): business question, data, what you did (tools and one hard problem), finding, what you would do next and one limitation. STAR (situation, task, action, result) can be the backbone, though critics say it sounds too story-like. Say "I" for what you did and "we" only for real team work.

**Worked script (illustrative, for the HR attrition project; replace brackets with your true facts):**
"I wanted to know which groups leave most and when. I used a public [or synthetic] HR table of about [N] employees. In [Excel/Power BI] I defined attrition as leavers divided by average headcount, cut it by tenure and department, and found [finding]. The hard part was [real problem, e.g. inconsistent department names], which I fixed by [step]. This data is [synthetic/public], so I would not claim a real cause; with live data I would first check [next step]."

| Follow-up | Answer skeleton |
|---|---|
| Define attrition rate | Leavers in period / average headcount; state the period |
| Why this chart? | Matches the question (comparison: bars; trend: line) |
| What if the data is wrong? | Check counts against source, duplicates, blanks; say what you checked |
| Did you follow a tutorial? | Say which part did, and what you changed yourself |
| Limitations | Synthetic or small data; no causes proven |
| What would you change? | One real improvement, e.g. add exit reasons |
| How would it scale? | Automate refresh, move data to a database |
| Who is the audience? | HR head; they need [decision], not chart detail |
| What if numbers disagree with another report? | Compare definitions first, then data |
| What did you learn? | One true skill gained |

**Honest-answer rules:** say which parts followed a tutorial; never claim business impact that did not happen. Say "if this were live, the HR head could [decision]." See Book 8 Part 8, Book 11 Parts 1 and 2, and Book 0 Q28.

**Self-check:** can you re-create the key number by hand from 10 rows? Can you explain each chart's axis and filter?

### 2.6 Limitations (Section 2)

- **No reliable data found** on how much recruiters in India value GitHub or public dashboards.
- Project ideas come from vendor and training blogs (unverified).
- We did not read dataset licences directly: read them yourself.
- Tool-feature facts (Tableau Public, Power BI publish) are snippet-level: check the current page.
- Interview frequency (about 14 of 20) is candidate-reported and anecdotal.

**Checklist**
- Only public or synthetic data is used; no employer data anywhere.
- Each project has a README with question, data source and licence, steps, 3 findings, limits.
- You can re-create one key number by hand and explain every chart.
- You have a 90-second spoken version and honest answers to the follow-ups, including what followed a tutorial.
- Links sit in the resume header and, after Section 3, in LinkedIn Featured.

---

## Section 3: LinkedIn and Naukri Profile Optimisation

### 3.1 What a profile does, and what we do not know

A profile does two jobs. It lets a recruiter find you when they search by keyword, and it lets anyone you message check you out in about 30 seconds. For the role of each site in an analyst search, see Book 0 Q101. This section does not repeat it. It shows you how to build both profiles.

Here is what nobody has measured in the research behind this book:

- **No reliable data found** on how Naukri ranks profiles, on the effect of headline wording, on the effect of "Open to Work", on callback rate by profile completeness, or on the value of endorsements (B12S, "No reliable data found").
- **Source access was limited.** The Naukri and LinkedIn pages themselves were not opened. Every platform fact below comes from a search snippet of an official help or blog page, or from a vendor or blog, and is labelled that way. Naukri returned HTTP 403 and LinkedIn was not fetched in the market research (MS Section 2). Menus and limits change: **check the live page** before you rely on any of them.

Because there is no data, use a decision rule instead. Change one thing at a time, wait about 2 weeks, then read your tracker (Section 6) to see whether views, messages or calls changed. This rule is our suggestion, not a research finding.

### 3.2 Keywords from job descriptions (the core method)

A keyword is a word a recruiter types into a search box, such as "SQL" or "MIS". A job description (JD) is the posting that lists what the employer wants. The method below is our own, not sourced from any study.

1. Save 10 to 15 real JDs for one target title (for example "MIS Executive" or "Associate Analyst").
2. List every tool or skill each JD names.
3. Count how many JDs name each one.
4. Put the top terms in your headline, skills list and summary, and in project lines. Use only terms you can defend in an interview.

For orientation, this is how often skills were named in the JDs we sampled for this project.

| Skill named in JD | Share of JDs (pooled n=186) |
|---|---|
| Dashboards / reporting / MIS | 75% |
| Communication | 73% |
| Excel | 60% |
| SQL | 54% |
| Stakeholder management | 44% |
| Power BI | 40% |
| Tableau | 33% |
| Python | 32% |
| Statistics | 23% |

Label: n=186 non-random sample, about +/-7 points. Counts are keyword tallies, and the sample is skewed to sites we could reach; Naukri, Indeed, Glassdoor and foundit were blocked (MS Addendum). Treat this as a starting list, then build your own from the JDs you save.

**Role-title variants.** Search and mention more than one title: MIS executive, reporting analyst, operations analyst, associate analyst. See Book 0 Q64 for the list and the reasoning (MS Section 6). Do not repeat it here.

**Worked example: JD to keyword list to headline (illustrative).** The three snippets below are invented for demonstration. Use real JDs.

| Illustrative JD snippet | Terms named |
|---|---|
| "Prepare weekly MIS reports in Excel; build dashboards; coordinate with HR and finance" | MIS, Excel, dashboards, stakeholders |
| "Associate Analyst: SQL queries, Power BI reports, present to business teams" | SQL, Power BI, reports, presentation |
| "Reporting Analyst: Excel, data cleaning, monthly dashboards, basic SQL a plus" | Excel, data cleaning, dashboards, SQL |

Count: Excel 2, dashboards 2, SQL 2, MIS 1, Power BI 1, data cleaning 1. A headline built from the top terms, if you can truthfully back them: "HR Reporting and MIS | Excel, SQL, Power BI dashboards".

**Rule, stated plainly.** Use only keywords for skills you have actually used and can explain. Never paste hidden or white-text keywords into a profile or resume. Never copy a skill list you have not worked with. A recruiter call or interview will test it.

### 3.3 LinkedIn profile, field by field

Advice on headlines and About sections below comes from vendor and blog guides (Teal, Resume Worded and similar), which agree with each other but give no outcome data: **vendor/blog claim, unverified** (B12S).

**Headline.** Put a title first, then 2 to 3 core skills. For a switcher, state the direction honestly rather than claiming a title you have not held.

| Version | Headline (illustrative) | Why |
|---|---|---|
| Weak | HR Professional seeking opportunities | No searchable skill, says nothing |
| Better | HR Analyst | Excel, SQL, Power BI | Title plus skills, but "HR Analyst" must be true of your work |
| Best | HR Reporting and People Analytics | Excel, SQL, Power BI | True direction, skills a recruiter can search |

**About section.** Three short paragraphs: who you are, what you built, what you want. Below is an example of about 125 words for an HR-to-analytics switcher. It is **illustrative**. Replace every fact with your own, and if you do not remember exact numbers, leave the number out and describe the work.

> I have worked in HR operations for [X] years, handling [your real tasks, for example monthly headcount and attrition reports]. I enjoy the reporting side most: finding out why a number moved and explaining it to managers.
>
> Over the past months I learned Excel, SQL and Power BI and built a project on a public, synthetic HR dataset. In it I analysed attrition by department and tenure and built a dashboard (a one-page visual summary of key numbers) with [two or three findings from your own project]. The data is not from any employer.
>
> I am looking for MIS, reporting or associate analyst roles in [Hyderabad/Bengaluru], ideally where HR or people data is part of the work. Project links are in the Featured section.

**Experience entries.** Rewrite HR duties as reporting achievements without changing titles, dates or employers. The translation table is in Section 1.

**Skills.** A LinkedIn help snippet says the Skills section allows up to 100 skills (**search snippet only, unverified; check the live limit**, as third parties disagree on when it changed). Put the 3 to 5 that match your JD list at the top (our suggestion; check how the app orders skills). There is **no reliable data found** on whether endorsements affect recruiter contact.

**Featured and Projects.** Link your GitHub, Power BI Service or Tableau Public pages from Section 2. A project link lets a stranger check your work without a call.

**Low-priority hygiene** (no data, so treat as basic tidiness): a clear face photo, a custom profile URL, your location set to Hyderabad or Bengaluru, a plain banner.

**Open to Work.** LinkedIn offers visibility to all members or to recruiters only, and says it cannot guarantee that recruiters at your current company will not see it (official help snippet, undated; check live). There is no reliable data on its effect on calls.

| Setting | What it does | What it does not do |
|---|---|---|
| Open to Work, recruiters only | Signals to recruiters using LinkedIn's recruiter tools | Does not guarantee your employer's recruiters cannot see it |
| Open to Work, all members | Shows a visible badge to everyone | Gives no privacy at all |
| Off | No signal | Recruiters can still find your normal profile |

Decision rule: if you are still working in HR, choose recruiters only or off, and tell your close network directly instead of posting publicly.

**Posting.** Optional. No reliable data found on its effect. Rule: post one write-up of a project once, not daily.

### 3.4 Naukri profile, field by field

Naukri is a job portal where recruiters search resumes by keyword. Official Naukri blog advice (snippet only) says recruiters search by keywords, to complete the profile and to update it regularly.

- **Resume headline and key skills:** use your JD keyword list, truthfully.
- **Profile summary:** 3 or 4 plain lines, the same story as your LinkedIn About.
- **Employment and projects:** same titles, dates and employers as your resume.
- **Resume upload:** a parser (the software that reads your file into fields) works better with a simple layout. Avoid tables and text boxes. This is a third-party tip, **unverified**.
- **Notice period, current and expected CTC:** answer honestly and consistently. For how to handle salary and notice questions, see Book 11 Part 8.

**Completeness.** Official advice is to complete the profile (snippet only). The claim that "100% completeness gives 3x views" comes from vendor blogs and is **unverified; do not use it**.

**Freshness.** Naukri's recruiter FAQ (a 2016 page, official snippet) says resume freshness reflects when a candidate was last active, and recruiters can filter on it. The official blog snippet says to update at least once in 6 months. Tips such as "update every 2 to 3 days" or "re-upload every 7 to 10 days" are from third-party sites and **unverified**. There is no reliable data on the best frequency. Decision rule: make a genuine edit weekly while you are searching (add a skill, a project line). Do not use auto-refresh tools; whether they break the terms of service is **unverified, confirm on the Naukri page**.

**Privacy.** Official snippets describe a Block Companies setting and a "not searchable" option. Naukri says it cannot guarantee full concealment. Labels may differ in the app.

| Setting | What it does | What it does not do |
|---|---|---|
| Block Companies | Hides your profile from the companies you list | Does not guarantee full concealment |
| Not searchable | Removes you from recruiter search | You then cannot be found by anyone, including new recruiters |

**Consistency.** The same titles, dates and employers on your resume, LinkedIn and Naukri. A mismatch looks careless, and may cause problems at background verification (our reasoning, not researched; confirm with the employer's verification process).

**Naukri vs LinkedIn, in short.**

| Field | Naukri | LinkedIn |
|---|---|---|
| Headline | Resume headline, keyword-rich | Title first plus 2 to 3 skills |
| Story | Short profile summary | About, three paragraphs |
| Proof | Projects field, resume file | Featured links, posts |
| Skills | Key skills list | Skills section, top 3 to 5 matched to your JDs |
| Privacy | Block Companies, not searchable | Open to Work options |

### 3.5 How recruiters search, and how to diagnose a quiet profile

LinkedIn's marketing pages say recruiters can filter by title, location and skills, and have an "Open to work" filter (vendor-stated, B12S; plan tiers not shown). Naukri's own snippet says recruiters search by keywords. So your words and your title need to match what they type.

**Diagnosis table.** All rules here are **decision rules, not measured**.

| Symptom | Likely cause | One change to try |
|---|---|---|
| No profile views | Keywords missing or title too generic | Put your top 3 JD terms in headline and skills |
| Views but no calls | Profile fits but proof or fit is weak | Add a project link and a real result line |
| Calls for wrong roles | Title or keywords attract other work | Narrow the headline to one target title |
| Calls but "notice period too long" | Notice period or location mismatch | State notice period and location clearly |

**Job alerts and saved searches.** Set one alert per platform for your target title and city (labels may differ, check live). Keep it to 2 or 3 alerts, so you actually read them (our suggestion).

**Worked example: reading a week of tracker rows (illustrative).** Suppose your tracker shows 10 applications and 2 recruiter calls, both for roles that named Power BI, while you only listed Excel and SQL in your headline. The suggested change is to add Power BI to the headline, only if you have a Power BI project to show. Wait 2 weeks and see if the pattern holds. Two calls is a small sample, so treat it as a hint, not proof.

### Limitations

No page from LinkedIn or Naukri was opened, so every platform feature is a snippet and may be out of date. No data exists in our research on what moves calls. Everything in the diagnosis table is a rule of thumb. Check live pages for limits, labels and privacy.

### Checklist

- Save 10 to 15 JDs for one target title and list the top terms.
- Rewrite your headline using terms you can truthfully defend.
- Set LinkedIn Open to Work to recruiters only or off if you are employed.
- Update Naukri and check Block Companies, then make one real edit each week.
- Make titles, dates and employers identical on resume, LinkedIn and Naukri.

**Pointers.** Book 0 Q19, Q64, Q75, Q101; Book 10 Part 1 (HR domain vocabulary); Book 11 Part 8 (salary and notice period); Section 1 (resume), Section 2 (projects), Section 6 (tracker).

---

## Section 4: Referrals, Cold Outreach, Recruiters, Networking and Consultancies

### 4.1 What this section is, and its limits

A referral is when an employee submits or recommends your profile for a named opening. Book 0 Q74 covers the "I have no network" case; this section adds the process and message shapes.

- **No reliable data found** on referral conversion for switchers, cold-message reply rates, the best follow-up timing, or the share of analyst hires that come through referrals or consultancies.
- Trade-press items (TCS, Infosys, Home Credit referral schemes, 2025) show companies run referral programmes and often pay bonuses in stages after joining (**snippet only**). Their amounts are for tech and mid-level roles, so do not take them as expected for an analyst switcher.
- This section is process and etiquette. It is not a promise of results.

### 4.2 Whom to approach, in what order

| Tier | Who | Why start here |
|---|---|---|
| 1 | People you know: HR colleagues, recruiters you worked with, vendors, college alumni | An HR professional already has many of these contacts (see Book 0 Section 5 on HR as an advantage) |
| 2 | Second-degree contacts in analytics at target companies | A mutual contact can introduce you |
| 3 | Strangers (cold) | No reply-rate data found; expect more effort per reply, so keep messages specific |

The tier order is our rule, not a finding. Next, build a list of 20 target companies from the JDs you saved (20 is our suggestion, not a research number). Company names in the market research (MS Appendix A) are examples of who posted, and do not show who hires switchers.

| Contact type | What to ask | What not to ask |
|---|---|---|
| Former colleague in reporting | Two specific questions on the team's tools | A job in the first message |
| Recruiter you know | Whether a role fits your profile | To ignore the JD requirements |
| Alumni in analytics | 15 minutes of advice | A referral before they know your work |
| Hiring manager (cold) | One question about a posted role | Pay, perks, or "any opening" |

### 4.3 Message templates

Every template below is **illustrative**. Names are invented. Replace every fact with your own, keep each message short, and never claim work you did not do. The general shape comes from vendor and blog advice (**unverified**, no reply-rate data): name the role, give one reason you fit (a real project), make one clear ask, do not mass copy-paste, and attach nothing to a first cold message.

**1. LinkedIn connection note.** Vendor sources say 200 characters standard and 300 on older or Premium accounts, and conflict on the free-account note quota (3 versus 5 per month) (**unverified, no LinkedIn page seen; check the counter in the app**).

> Hi Anita, I moved from HR into reporting and am applying for the Associate Analyst role at [Company]. Could I ask you two quick questions? Thanks, Ravi

**2. Referral request to a known person.** Extends Book 0 Q74.

> Hi Suresh, hope you are well. I am applying for the [role name, ID if any] opening on your team. I built an attrition dashboard on a public dataset (link: [your link]). If you think I fit, would you be comfortable referring me? I can send the JD and a 3-line summary. No problem at all if not.

**3. 15-minute advice request.** Two specific questions, no job ask.

> Hi Meera, I am moving from HR to data reporting. Two questions: how does your team use SQL and Power BI day to day, and what would you build first if you were starting again? Fifteen minutes whenever suits you.

**4. Cold email to a recruiter or hiring manager.**

> Subject: Associate Analyst application, HR reporting background
> Dear Mr Rao, I saw the Associate Analyst role at [Company]. I have [X] years in HR and built a project analysing attrition with Excel, SQL and Power BI: [link]. Resume attached. I would be glad to share more. Thank you, Ravi

**5. Reply to an inbound recruiter message.** From general blog advice (**unverified**, not India-specific): reply within about a day, thank them, ask for the JD and pay band, state your notice period honestly, and offer two call slots.

> Thank you for reaching out. Could you share the JD and the pay band? My notice period is [your real notice period]. I am free [Tuesday 4 pm or Wednesday 11 am] for a call.

**6. Follow-up and thank-you.** One nudge after about 5 to 7 days, then stop (**vendor/blog advice, unverified**). After help, send thanks, and tell them the outcome later.

> Hi Suresh, a gentle follow-up on my note last week. No worries if you are busy. Thanks again for your time.

**Template rules.** Name the role. One reason you fit. One clear ask. No mass copy-paste. No attachment in the first cold message.

### 4.4 Recruiter calls and the "why switch" answer

First-call checklist, so you leave with facts: the role, the team, the tools, the pay band range, the notice period and the location. Prepare an honest answer to "Why are you moving from HR to analytics?" using the story framework in Book 0 and Book 11 Parts 1 and 2. Do not duplicate it here. For salary and notice questions, the rule is simple: be honest and consistent with your profile. See Book 11 Part 8.

### 4.5 Consultancies and staffing firms

A consultancy or staffing firm finds candidates for client companies. A vendor source says the usual model is that the employer pays (**vendor-stated, unverified**). Some place you on their payroll as a contract worker, others on the client's payroll as permanent staff (general knowledge, unverified), so ask.

| Question to ask | Why |
|---|---|
| Who is my employer on paper? | Payroll decides benefits and notice |
| Contract length and renewal? | Contract roles can end |
| Notice period and background verification? | Avoids later surprises |
| Can the role convert to permanent, and when? | Plan your next step |
| Which company is the client, and is the role on its careers page? | Checks the role is real |

**Fee red flags.** TCS and Michael Page (official snippets) warn that legitimate firms do not charge candidates for registration or placement. Rule: do not pay anyone to get an interview or a job. Charging a candidate is a warning sign. Its legal status is conflicting across sources (a 2025 bill and a Maharashtra act, per vendor and news sources), so **unverified, confirm before quoting**.

| Red flag | What to do |
|---|---|
| Registration, CV processing or "security deposit" fee | Stop; do not pay |
| Guaranteed job for money | Stop |
| No named client, no office address | Ask for both; walk away if refused |
| Pressure to pay today | Walk away |

Fee ranges quoted online are **unverified**. To verify a firm, check its website, address and company registration, and confirm the role on the hiring company's own careers page. **No reliable data found** on which firms in Hyderabad or Bengaluru place switchers at analyst roles.

### 4.6 Etiquette, volume and ethics

- **Volume:** 3 messages a week matches Book 0 Q74. That is a suggestion, not research.
- Share a short work sample (a project link) before you ask anyone to vouch for you. Do not ask someone to vouch for skills they have not seen.
- Employees may earn a referral bonus. Ask politely, and never offer money or favours.
- Never misrepresent your experience or share employer data to impress anyone.
- One follow-up, then move on. Do not spam hiring managers.
- If there is no reply, record it in your tracker (Section 6) and move on.

### 4.7 A 6-week outreach plan (illustrative)

Copy this into your tracker. Three messages a week is our suggestion.

| Week | Messages | Focus |
|---|---|---|
| 1 | 3 | Tier 1: close contacts, advice chats |
| 2 | 3 | Tier 1 follow-ups plus 1 alumni |
| 3 | 3 | Tier 2 via a mutual contact |
| 4 | 3 | Referral asks to people who know your project |
| 5 | 3 | Cold emails to up to 3 target companies |
| 6 | 3 | Follow-ups, thanks, outcome updates, review |

### Limitations

All templates and timings are suggestions from general advice, not tested on Indian analyst hiring. Character limits and fee law are conflicting or unverified. Consult the live app, and for fee law, a legal source.

### Checklist

- Write your list of 20 people and 20 target companies.
- Send 3 messages this week, starting with tier 1.
- Ask for advice first, a referral only after they know your project.
- Ask any consultancy who the employer is, and never pay a fee.
- Log every message and reply in your tracker.

**Pointers.** Book 0 Q74, Q58, Q65; Section 6; Book 11 Parts 1, 2, 8; Sections 1, 2, 3.

---

## Section 5. Certifications (PL-300, Google Data Analytics and others)

### 5.1 The honest verdict first

A certification is a course or exam certificate from a vendor such as Google (through Coursera, an online course site) or Microsoft. Many switchers ask whether they need one. Here is what the research supports:

- **No certification was named as a requirement in any job description we read.** In the first sample of 40 in-scope postings, none named a certification such as PL-300, Google Data Analytics, Tableau or CBAP (MS Section 5). In the pooled sample of 186 postings, certifications were named only as advantages in a few postings (Tableau or Power BI certificate, Google Data Analytics, Microsoft Data Analyst Associate, CBAP) (MS Addendum; n=186 non-random sample, about +/-7 points). Two postings said "certifications" without naming one.
- **Value of a certificate in India: No reliable data found.** That covers how much employers weigh them, whether they raise salary, pass rates, and outcomes for HR switchers. Claims about placement or salary uplift come from the vendors and course sellers who profit from the sale (vendor marketing, unverified).
- **Our rule:** a certificate is optional signalling. It is never a hiring filter and never ranks above a finished project.

Order of work, from plan.md: Excel, then SQL, then a portfolio, then a certificate if you still want one. For learning content see Book 1 (Excel), Book 2 (SQL) and Book 4 (Power BI), and Section 2 of this book for projects. Book 0 already answers "certificate or projects?", "do placement guarantees work?" and "are bootcamp claims true?" in Q55, Q56 and Q57. This section does not repeat them.

### 5.2 What each certificate is

Every cell below comes from a search snippet of an official or vendor page, not from a page opened in full (A12c sources). Prices change, so check the live page.

| Certificate | What it is | Facts found | Source tag |
|---|---|---|---|
| Google Data Analytics Professional Certificate (Coursera) | A beginner course series with 9 courses | About 6 months at 10 hours a week; no degree or experience required. The Google India page says many finish in 3 to 6 months. Pace is the provider's own claim. | Official vendor page, snippet only |
| Microsoft PL-300, Power BI Data Analyst Associate | A proctored (supervised) exam on Power BI, the Microsoft dashboard tool | Exam price depends on the country where you sit it. Passing score 700. Study guide heading says "skills measured as of April 20, 2026". | Official page, snippet only |
| Tableau Desktop Specialist | An entry exam for Tableau, a rival dashboard tool | Official fee shown as USD 100; no prerequisites; the credential does not expire. Exam length not verified. | Official page, snippet only |
| DP-600 (Fabric Analytics Engineer) | A Microsoft exam for building data platforms in Fabric | More advanced than PL-300, a step beyond a first analyst role. | Blog claim, unverified |
| CBAP and similar business-analysis credentials | Professional credentials for business analysts | Appeared only in a posting asking 4 to 6 years of experience (MS Section 5). Out of scope for you now. | JD sample, one posting |

Three details need care:

- **Prices: we do not quote one.** The Google India page and the US Coursera page showed different monthly figures, and third-party sites quoted other rupee amounts. For PL-300 we found no official rupee price, and third-party guesses conflict (unverified). Open Coursera or the Microsoft exam page, look at the price in rupees today, and write it in your worksheet (5.5).
- **Renewal of PL-300.** The official FAQ snippet says renewal is free through an online assessment taken before the certificate expires; if it lapses you must earn it again. Book 0 Q55 mentions a 12-month renewal. Confirm the current rule on the Microsoft page.
- **Tableau.** Tableau appeared in about 33% of the pooled postings and Power BI in about 40% (MS; n=186 non-random sample, about +/-7 points). That is no proof a Tableau certificate helps. It only says to consider Tableau if your target postings name it.

### 5.3 Decision rule when there is no data

Use your own evidence, not mine. Collect 10 job descriptions (JDs) for the roles you want, in Hyderabad or Bengaluru.

1. Count how many name a certificate.
2. If 0 to 2 do, spend your next hours on a project.
3. If your target role says Power BI is required and you already have one finished dashboard, PL-300 is a reasonable add.
4. Work out the total cost: fee, plus study hours, plus the risk of a retake.

| Situation | Do a certificate now | Later | Skip |
|---|---|---|---|
| 0 to 2 of your 10 JDs name a certificate and you have no project | | | Skip for now; build the project |
| Excel and SQL are weak | | Later | |
| One finished dashboard and 4 or more of 10 JDs ask for Power BI | Reasonable | | |
| You need a study structure and the fee is small to you | Optional | | |
| A course promises a "guaranteed certificate" or placement | | | Skip (see Book 0 Q56, Q57) |
| Target JDs ask 3+ years and name a credential | | Later | Skip for a first role |

### 5.4 Worked examples (illustrative)

**A. Two weeks: certificate or project?** (illustrative) You have 14 evenings of 1 hour. A certificate course says "about 40 hours". A dashboard project takes you perhaps 20 to 30 hours, including cleaning data and writing a short README (a page explaining what the project is). Your 10 JDs name no certificate. Decision: do the project; a recruiter can open it and see your work. If you finish early, start the certificate. Book 12 Q86 works this through.

**B. Cost arithmetic.** (illustrative; replace every number with your own)

| Item | Formula | Invented placeholder | Your number |
|---|---|---|---|
| Exam or course fee | Check live page, in rupees | Rs 10,000 (not a real price) | |
| Study hours | Hours you will really study | 40 | |
| Value of your hour | What you could earn or the sleep you give up; decide your own figure | Rs 300 | |
| Time cost | Hours x value of hour | 12,000 | |
| Base total | Fee + time cost | 22,000 | |
| Retake risk | Add one more fee if you might fail | +10,000 | |
| Worst case | Base total + retake | 32,000 | |

If you cannot name a job that needs it, the worst case should make you pause.

**C. Listing it honestly.**

- **Resume:** put it in a short "Certifications" block below Projects, with name, issuer and month and year earned. "In progress" only if you are really enrolled, with a true expected month. Never list one you have not earned. Do not hide a failed attempt behind a vague date; just leave it out until you pass.
- **LinkedIn:** use the Licenses and Certifications section, and mention the project that used the same skill in your About text (see Section 3). Check the live LinkedIn page for how it lets you enter the credential ID.
- **Interview:** if asked "why this certificate?", say what you learned and show the project (Book 11 Parts 1 and 2 cover your switch story).

### 5.5 Blank worksheet to complete

| Line | What to write |
|---|---|
| Certificate considered | |
| JDs naming it (out of 10) | |
| Live fee in rupees (date checked) | |
| Study hours you will really do | |
| Value you give one hour | |
| Total = fee + hours x value | |
| Retake fee if you fail | |
| Project you would skip to do this | |
| Decision (now / later / skip) and date to review | |

### 5.6 Honest limits and a do-not list

- A certificate shows you passed an exam or course; it does not show you can build a dashboard from messy data.
- Exam content changes. The PL-300 outline carries an April 2026 date, so older prep videos and books may be stale.
- Do not list a certificate you have not earned.
- Do not use exam dumps (leaked question banks) or pay someone to sit the exam. This is deceptive and can cost you the credential and your name with the vendor. Book 12 Q94 covers it.
- Do not buy bundles that "guarantee" a certificate or a job.
- Never use your employer's data for practice projects; use public or invented data (Book 4 for Power BI practice).

### Limitations (Section 5)

- All certificate facts are search-snippet level; no page was opened in full, and the search tool saw US results.
- Rupee prices for PL-300 and Google Data Analytics were not found reliably. Prices, exam outlines and renewal rules change.
- Employer weight in India, salary uplift, pass rates and HR-to-analyst outcomes: No reliable data found.
- The JD sample is non-random; absence of certificates in it does not prove they never matter.

### Checklist (Section 5)

- Count how many of your 10 target JDs name a certificate before spending anything.
- Finish Excel, SQL and one project before a certificate.
- Check the live price in rupees; fill the worksheet; never rely on a blog price.
- List only certificates you have earned, below your projects.
- Skip dumps, proxy testers and "guaranteed" bundles.

---

## Section 6. Application tracker, weekly routine and job-search hygiene

### 6.1 Why track

No source we found shows that tracking raises your chance of a job. We track because the Book 0 rule needs data: after 10 applications with no replies, change the resume, not the target (Book 0 FAQs, job-search answer; this is our own rule of thumb, not sourced, and 10 is illustrative). Without a record you cannot see which resume version or which board is working. Build the tracker in Excel (Book 1) or Google Sheets.

### 6.2 Tracker design

Career blogs agree on roughly 6 to 10 core columns (blog and career-centre advice, unverified; A12c sources). Use these:

| Column | What goes in | Why |
|---|---|---|
| Date applied | dd-mmm-yyyy | Starts the follow-up clock |
| Company | Name | |
| Role | Title as in the JD | |
| Source | Naukri, LinkedIn, Indeed, career page, referral, consultancy | Lets you compare sources |
| JD link | URL, or save the JD text (postings get removed) | |
| Resume version | v1, v2 and so on | Lets you compare resumes |
| Status | From the list in 6.3 | |
| Contact | Recruiter or referrer name | |
| Next action date | Date you will nudge or prepare | |
| Notes | Feedback, stage reached, reason | Feeds your rejection log |

Add a small summary sheet (a pivot table, which counts rows by a category; Book 1) and response-rate formulas: replies divided by applications, by source and by resume version.

### 6.3 Status words and next actions

| Status | Meaning | Next action |
|---|---|---|
| Saved | JD kept, not applied | Tailor 3 resume lines, apply within 2 days |
| Applied | Sent | Set a follow-up date about 1 to 2 weeks out |
| Referral asked | You asked someone to refer you (Section 4) | Thank them; wait about a week |
| Screen | First call with recruiter | Prepare your switch story (Book 11 Part 1) |
| Interview round n | Technical, case or manager round | Practise by stage (Books 2, 7, 8, 11) |
| Offer | Written offer received | Check terms; see 6.9 |
| Rejected | Said no | Fill the rejection log (6.7) |
| Ghosted | No reply after your follow-ups | Close it after the cut-off in 6.8 |
| Withdrawn | You pulled out | Note why |

Follow-up convention from career blogs: first nudge about 1 to 2 weeks after applying, then at most 2 or 3 follow-ups (convention, unverified, not data). Book 12 Q101 covers wording.

### 6.4 Worked example: a 4-week tracker and summary

All entries are illustrative placeholders, not evidence. "Reply" here means any human response, including a rejection.

| # | Week | Company (invented) | Source | Resume | Status | Reply? |
|---|---|---|---|---|---|---|
| 1 | 1 | Firm A | Naukri | v1 | Screen | Yes |
| 2 | 1 | Firm B | Naukri | v1 | Applied | No |
| 3 | 1 | Firm C | Naukri | v1 | Ghosted | No |
| 4 | 2 | Firm D | Naukri | v2 | Applied | No |
| 5 | 2 | Firm E | Naukri | v2 | Rejected | Yes |
| 6 | 2 | Firm F | LinkedIn | v2 | Screen | Yes |
| 7 | 3 | Firm G | LinkedIn | v1 | Applied | No |
| 8 | 3 | Firm H | LinkedIn | v2 | Applied | No |
| 9 | 3 | Firm I | Career page | v1 | Applied | No |
| 10 | 4 | Firm J | Career page | v2 | Rejected | Yes |
| 11 | 4 | Firm K | Referral | v2 | Interview round 1 | Yes |
| 12 | 4 | Firm L | Consultancy | v1 | Applied | No |

Summary (reply rate = replies / applications):

| Group | Applications | Replies | Reply rate |
|---|---|---|---|
| Naukri | 5 | 2 | 40% |
| LinkedIn | 3 | 1 | 33% |
| Career page | 2 | 1 | 50% |
| Referral | 1 | 1 | 100% |
| Consultancy | 1 | 0 | 0% |
| Resume v1 | 6 | 1 | 17% |
| Resume v2 | 6 | 4 | 67% |
| All | 12 | 5 | 42% |

In Excel, with Source in column D and Reply in column G, a rate is `=COUNTIFS(D:D,"Naukri",G:G,"Yes")/COUNTIF(D:D,"Naukri")`. Read the table with care: groups of 1 to 6 are far too small to rank anything. Even v1 versus v2 (1 of 6 against 4 of 6) is a hint to test, not a finding. Collect 4 to 6 weeks of rows before moving effort (Q99, Q100).

### 6.5 Weekly routine (our own design, not research)

Nothing in the research tells us how many applications make an offer: **No reliable data found** on callback rates, applications per offer, best days or times to apply, or time to hire. So the numbers below are planning variables you set. Count in roles, not hours.

| Block | Employed in HR, 1 to 2 hours a day | Between jobs, full time |
|---|---|---|
| Mon to Fri | 1 hr evening: 2 weekday evenings apply, 1 outreach (Section 4), 2 study or portfolio (Section 2) | Morning: apply and outreach. Afternoon: study or project. Evening off |
| Interview practice | 1 weekday evening in place of study when a screen is booked (Books 7, 8, 11) | 1 to 2 afternoons a week |
| Weekend | One 2 to 3 hour block: project work | One block: project; the other day off |
| Sunday review | 20 minutes: update tracker, refresh summary, set next week's targets | Same, 30 minutes |
| Applications a week | A number you choose, for example a small fixed target of well-matched roles | A higher fixed target; cap it per day |

Where to apply, by public name: Naukri, LinkedIn, Indeed, company career pages, referrals and consultancies (Section 4). Naukri and Indeed pages are vendor sources. Indeed's Hiring Lab notes its India data skews to tech, management and sales. No source ranks boards by hit rate: **No reliable data found**. Rule: track response by source for 4 to 6 weeks, then move time to what answers you.

Volume versus quality: tailor the top-fit JDs by matching 3 resume lines to each (Book 0 Q83). Do not mass-apply with an untailored resume. Never hide keywords or invent experience.

### 6.6 Silence and ghosting

Silence is normal and says little about you. Use the follow-up rule in 6.3, then close the row after a cut-off you set in advance, for example 3 weeks after your last follow-up (illustrative). No data on whether follow-ups change response: **No reliable data found**. Do not follow up daily.

### 6.7 Rejection handling and a log

Ask once, politely, for feedback; do not argue. Log the stage where you fell, then fix that stage with the right book.

| Stage lost | What it may mean | Fix with |
|---|---|---|
| Resume screen | Keywords or fit; some filters are rigid JD requirements, not a verdict on you (CompTIA blog snippet) | Section 1, Section 3 |
| Screening call | Story unclear | Book 11 Parts 1 and 2 |
| Technical round | Skill gap | Books 1, 2, 4 |
| Case or scenario | Structure | Books 7, 8 |
| HR round | Pay, notice, fit | Book 11 Part 8 |

Mini rejection log (illustrative row): Firm E, resume screen, Week 2, resume v2, feedback: none, action: add SQL project line, retry similar JDs next week.

### 6.8 Pacing

Schedule rest and cap daily applications. The advice is general career-centre advice (blog and university pages), not India data. A tired applicant sends careless applications.

### 6.9 Notice period overlap (read your own contract)

Not legal advice. Notice period rules are from memory and blogs, unverified: confirm with your own contract, HR policy or legal advice. The sources we saw say the contract sets the notice period, a buyout (paying to leave early) is the employer's choice, and some new employers reimburse a buyout (Instahyre blog, unverified). One blog says the Labour Codes leave it to the contract (unverified). Ask the new employer for a later start date, and never leave without a relieving letter. As an HR person you know your company's policy; use it.

Illustrative arithmetic (replace with your own contract terms):

| Line | Formula | Invented number |
|---|---|---|
| Monthly pay used in buyout | Check your contract (basic or gross) | Rs 50,000 |
| Daily pay | Monthly / 30 | about Rs 1,667 |
| Notice days remaining | Notice days minus days served | 60 - 20 = 40 |
| Cost of buying out remaining days | Daily pay x days | about Rs 66,700 |
| Cost of asking for a later start | Wait of 40 days | no payment; offer may lapse |

No data on notice buyout norms by company: **No reliable data found**. See Book 11 Part 8 and Book 12 Q103.

### 6.10 Scam and confidentiality hygiene

Scams: a recruiter who asks for money is a red flag. Paying a recruiter or consultancy for a job is a warning sign (legality: unverified, confirm). Verify the opening on the official careers page. Never share an OTP or install a remote-access app. Be wary of WhatsApp-only offers with no interview. Report at cybercrime.gov.in or call 1930 (company and media pages, snippet only; check the live site). No scam-rate statistic was used. See Q106.

Confidentiality: do not discuss your search at work, do not use office email or laptop, and keep your employer's data out of your portfolio and interviews. If employed, set LinkedIn "Open to work" to recruiters only or off; LinkedIn says it cannot guarantee privacy from recruiters at your current company (official help snippet; see Section 3 for current wording). Check the live setting.

### Limitations (Section 6)

- The tracker columns, routine, follow-up gaps and the "10 applications" rule are conventions or our design, not research findings.
- Reply rates, applications per offer, best timing, effect of follow-ups, board hit rates and buyout norms: No reliable data found.
- Notice, privacy and platform-term points are from memory and blogs; confirm with HR, legal advice or the platform page.
- Scam advice comes from company and media snippets; blocked sites (LinkedIn, Naukri help, Glassdoor) were not read.

### Checklist (Section 6)

- Start the tracker today with the 10 columns and the status words.
- Set a weekly number of tailored applications you can sustain, and review every Sunday.
- Compare response by source and resume only after 4 to 6 weeks; treat small groups as hints.
- Log the stage of each rejection and fix that stage with the right book.
- Read your own notice clause before you accept an offer, and never pay anyone for a job.


---

## Section 7. The 108 FAQs: how to use them

The FAQs are in `Book12_FAQs.md`, grouped by guide section, and every answer points back to the guide section or book that covers it.

| Guide section | FAQs |
|---|---|
| 1. Resume | Q1-Q24 |
| 2. Portfolio projects | Q25-Q48 |
| 3. LinkedIn and Naukri | Q49-Q66 |
| 4. Referrals and outreach | Q67-Q84 |
| 5. Certifications | Q85-Q94 |
| 6. Tracker, routine and hygiene | Q95-Q108 |

**How to use them.**
- Read the guide section first, then the FAQs for the same section, then do the checklist at the end of the guide section this week.
- Starred questions (⭐⭐⭐) first. Questions marked "Say this in the interview" are interview-facing: practise the script aloud with your own true facts in the [placeholders].
- Every example is labelled illustrative. Replace it with your own true story and numbers; never copy an example as your own history.
- Where an answer says "No reliable data found", do not look for a blog number to fill the gap. Apply the decision rule in the answer.
