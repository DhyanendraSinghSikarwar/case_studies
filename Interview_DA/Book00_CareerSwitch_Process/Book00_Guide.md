# Book 0: Career Switch & Interview Process Guide (HR to Data Analyst)

**Reader:** a non-technical HR professional switching to data analytics. **Target roles:** Data Analyst, Business Analyst, MIS/Reporting, BI, Product/Operations and People/HR Analytics. **Target cities:** Hyderabad and Bengaluru (also Pune, Chennai, NCR). **Target pay:** Rs 6-10 LPA (see Section 2b for what the evidence supports).

**How to read this guide.** Every number comes from the series' own research files (`research/`), with its confidence label next to it: job-description percentages are from a pooled, non-random sample (n=186, about +/-7 points; smaller sub-samples have wider error), interview processes are anonymous and candidate-reported, and pay or course figures from blogs and vendors are unverified. Where no data exists the guide says "No reliable data found" and gives a rule you can apply to your own numbers. Hours, milestones and timelines in the roadmap are study-plan targets, not research findings. The 123 FAQs live in `Book00_FAQs.md`; this guide is the context they refer to.

**Evidence labels.** "JD" means job description, the text of a job posting. "n=186 non-random sample, about +/-7 points" means we read 186 in-scope postings (Hyderabad/Bengaluru, stated minimum experience of 2 years or less, or tagged entry/junior) pooled from five samples of 40, 47, 42, 32 and 25 and counted which skills they name. The postings are not a random draw of the market, so treat every percentage as a rough size, not an exact figure. "Candidate-reported, anonymous" means the claim comes from interview write-ups by candidates we cannot verify. "Vendor/blog claim, unverified" means a training provider, salary blog or job-board snippet. Today is 2026-10-22; everything below describes what the research found in October 2026, not what will happen later.

---

**Contents**
1. Role map: DA vs BA vs MIS vs BI vs Product vs People Analyst
2. Skills demanded in 2026: must-have vs good-to-have
2b. Honest pay bands and switcher-friendly entry roles
3. Interview process by company type (with reliability caveats)
4. Round-by-round expectations
5. How your HR experience is an advantage (and where it is not)
6. Six-month learning roadmap for a non-technical beginner
7. The 123 FAQs: how to use them (FAQ answers in `Book00_FAQs.md`)
Limitations to state in the guide

---

## Section 1. Role map: Data Analyst vs Business Analyst vs MIS vs BI vs Product vs People Analyst

### 1.1 The honest starting point

Job titles in this field overlap a lot. One company's "Business Analyst" does the daily work another company calls "Data Analyst" or "MIS Executive". We found no independent source that defines these titles consistently, so the table below describes *typical* work as seen in the sampled JDs, not an official definition. The practical rule is: **read the JD, not the title.** Count which tools and tasks the JD names, and judge the role by those.

### 1.2 The role table

Tool evidence in this table comes from the JD samples (MS Section 6 and the MS Addendum). "Switcher-friendliness" is our reading of how high the tool bar is for someone starting from HR, based on which tools the JDs ask for. It is a judgement, not a measured outcome. Pay is deliberately left out here and covered once, in Section 2b, so the numbers never diverge between sections.

| Role | What you do (typical) | Main tools asked in sampled JDs | Switcher-friendliness for an HR professional |
|---|---|---|---|
| **MIS / reporting analyst** | Build and send the same reports daily, weekly and monthly. Clean data, reconcile numbers, keep trackers and dashboards updated. | Excel (often advanced), VBA/macros, basic BI tool. In the MIS/people sample alone: Excel 72%, SQL 44%, Python 16% (n=32, non-random, about +/-17 points; this is one of the five samples, not the pooled n=186). | **Highest.** Excel-first, SQL often optional. Examples seen: Tata Play Fiber SME MIS and Reporting (Bengaluru, Entry), EXL MIS Reporting BA (Bengaluru), TMI MIS Executive (Hyderabad), Quess Assistant Manager MIS. |
| **Operations analyst** | Track process metrics (turnaround time, errors, volumes), find where a process leaks, report to a manager. | Excel, dashboards, SQL "nice to have". | **High.** Examples seen: KPMG Operations Analyst (Bengaluru, 1-2 yrs), HPE Procurement Ops Analyst I (Bengaluru, 0-2 yrs; SQL listed as nice to have). |
| **Data analyst (DA)** | Pull data with SQL, clean it, analyse it, and present findings or dashboards. | SQL, Excel, a BI tool (Power BI or Tableau), sometimes Python. Python appeared in 30% (Hyderabad, n=47), 40% (Bengaluru, n=42) and 40% (GCC, n=25) of JDs; each sample is non-random and small, so read these as about +/-15 to 20 points. The first 40-JD sample gave 35% (about +/-15 points). | **Medium.** Needs SQL ready; Python often "nice to have" at entry level. |
| **BI / dashboard analyst** | Own dashboards: data model, refresh, visuals, definitions, user questions. | Power BI or Tableau, SQL, DAX (Power BI formula language) sometimes. | **Medium.** A learnable, project-friendly path; see Book 4. |
| **Business analyst (BA)** | Turn a business question into a requirement or analysis; work with stakeholders; some data work. | Excel, SQL, a BI tool; heavy on communication. Stakeholder management was named in 64% (Hyderabad, n=47), 60% (Bengaluru, n=42) and 60% (GCC, n=25) of those samples, but only 15% in the first 40-JD sample and 19% in the MIS sample; the pooled figure is 44% (n=186, non-random, about +/-7 points). The spread suggests counting rules differed between samples, so treat it as "common", not exact. | **Medium**, with a communication edge for people from HR. |
| **Product analyst** | Study how users behave in a product: funnels, retention, experiments, metric drops. | SQL, Python, dashboards, A/B testing sometimes. | **Lowest in startups** (hardest SQL, Python-heavy). One non-tech example, Netcom Learning (Hyderabad, 1-3 yrs), asked Excel, Power BI and AI tools. |
| **Business / pricing / research analyst** | Market sizing, pricing, competitor and revenue analysis. | Excel, SQL, Tableau or Power BI. | **High to medium.** Examples seen: Easyship, TriNet, Gartner, Cushman & Wakefield. |
| **People / HR analyst** | Attrition, hiring funnel, headcount, engagement and payroll reporting. | Excel, Power BI/Tableau, SQL, and HR systems (Workday, Visier, SuccessFactors) where named. | **High on domain fit, thin on openings.** See 1.4. |

Two cautions on the table:

- The examples are postings we read in October 2026. They show what exists, not what is open to you today.
- Sampling skew matters. Naukri, Indeed, Glassdoor and foundit returned errors for our tools, so the mass-market service-company and BPO-style MIS roles are probably under-represented. Built In, the main source, leans toward product companies, GCCs (global capability centres, the India offices of multinationals) and funded startups.

### 1.3 What the skill mix tells you about each role family

- **MIS / reporting:** Excel 72%, SQL 44%, Python 16% (MIS/people sample only, n=32, non-random, about +/-17 points). If you can already make clean Excel reports, you are closer to this bar than to any other role's bar. See Book 1.
- **DA / BI:** SQL plus a BI tool, with Python in roughly a third of JDs (32% pooled; 40% in the Bengaluru and GCC samples against 30% in the Hyderabad sample, small non-random samples). See Books 2, 4 and 3.
- **BA / product:** stakeholder-heavy. The work is as much explaining and prioritising as it is analysing. See Book 11 for communication and Book 7 and Book 8 for case-style thinking.

### 1.4 People/HR analytics: the honest picture

This is the path most HR professionals expect to be natural, so the limits matter.

- **No pure people-analytics role at 0-2 years was found** in our sampled JDs. The other Workday-reporting roles we found asked for 3 or more years (examples read: Syneos HR Analytics and Visualization, Hyderabad, 3+; Unisys People Analytics, Bengaluru, 4-6 yrs). Naukri, Indeed, Glassdoor and foundit were blocked, and LinkedIn was only partly readable (public pages in the Hyderabad sample), so this is a finding about the sources we could reach, not proof that no such role exists.
- **One in-scope entry example:** Deutsche Bank, Workday Prism Analytics and Reporting Consultant (HR IT), Bengaluru, tagged Entry (MS Appendix A row 20). It names ETL, dashboards and communication. **Source conflict:** MS Section 6 lists this role as in-scope Entry, while the MS Addendum says all Workday-reporting roles asked 3+ years. We could not reconcile them: "Entry" is the posting's own tag and no years were stated, so treat it as one possible entry door, not proof that fresher Workday roles are common.
- **HR-adjacent roles do exist at 0-2 years:** Unisys Associate Analyst, Organisational Change Management (remote India, 0-2 yrs), asking Excel, Power BI and AI tools like Copilot or ChatGPT.
- In the sampled postings, Workday, SuccessFactors and Visier were not named in any in-scope (0-2 yr) JD of the MIS/people sample. HR-system words that did appear were HROne/HCM (payroll platforms), "HCM systems" and "HRIS a plus".
- One job-board snippet lists a "People Data Analyst" in Bengaluru at Rs 6-10 LPA (EdTech Jobs; snippet only, experience not shown, unverified).

Plain conclusion: your HR background is a real advantage for *explaining* and *interpreting* people data (Section 5 of this guide), but it does not remove the need for Excel and SQL, and a directly matching entry role is scarce in what we could see.

### 1.5 Decision flow: "Which role should I aim at first?"

Answer these in order. This is guidance based on the tool bars above, not a prediction of outcomes.

1. **Can you build a clean pivot-table report in Excel without help, and use lookups?**
   - No: start with Excel (Book 1). Your first target is MIS/reporting or operations analyst.
   - Yes: go to 2.
2. **Can you write a SQL query with a JOIN and a GROUP BY from scratch?**
   - No: start SQL (Book 2). Target MIS/ops or research/pricing analyst while you learn.
   - Yes: go to 3.
3. **Do you have a finished dashboard in Power BI or Tableau that you can walk someone through?**
   - No: build one (Book 4 and Book 12). Target DA/BI roles after that.
   - Yes: target DA/BI or BA roles. Add Python (Book 3) before aiming at product or startup analyst roles.
4. **Do you want to stay close to HR?** Look for HR-tech or HR-operations reporting roles (Workday or HRIS reporting). Expect fewer entry openings. Use MIS or ops roles in an HR-heavy employer as the realistic bridge, and keep the HR reporting angle in your resume.
5. **Do you want a startup or product-company analyst role?** Be honest with yourself: this is the hardest entry. In the interview research, product and startup companies (Flipkart, PhonePe, Meesho) are reported, candidate-reported, to ask the hardest SQL (see Section 3).

### 1.6 Limitations (Section 1)

- Titles overlap; no independent definition source was found.
- Switcher-friendliness is our reading of the tool bar. **No reliable data found** on which role converts HR switchers best or fastest. The decision rule above uses the tools you already have.
- MIS/people sample percentages (Excel 72, SQL 44, Python 16) come from the MIS column of the MS Addendum (n=32, about +/-17 points). The people-MIS file also notes that five near-identical postings from one employer (Honhr, a bulk-posting template) inflate its tool counts; collapsing them leaves Excel and dashboards high and SQL lower.
- Pay by role is covered only in Section 2b.

---

## Section 2. Skills demanded in 2026: must-have vs good-to-have

### 2.1 The pooled table

Source: MS Addendum, n=186 in-scope JDs from five samples, **non-random, about +/-7 points**. Classes: Must-have = 50% or more of JDs; Common = 20-50%; Good-to-have = under 20%. "Named" means the JD text names the skill; it does not mean the employer tests it deeply.

| Skill | Share of 186 JDs | Class |
|---|---|---|
| Dashboards / reporting / MIS | 75% | Must-have |
| Communication | 73% | Must-have |
| Excel | 60% | Must-have |
| SQL | 54% | Must-have |
| Stakeholder management | 44% | Common |
| Power BI | 40% | Common |
| Tableau | 33% | Common |
| Python | 32% | Common |
| Statistics | 23% | Common |
| ETL (moving and transforming data) | 18% | Good-to-have (upper bound; Amazon wording inflates it) |
| GenAI / AI tools | 14% | Good-to-have |
| VBA / macros | 13% | Good-to-have |
| Machine learning | 10% | Good-to-have |
| Cloud | 10% | Good-to-have |
| R | 9% | Good-to-have |
| Google Sheets | 8% | Good-to-have |
| DAX | 5% | Good-to-have |
| A/B testing | 4% | Good-to-have |
| Snowflake | 4% | Good-to-have |
| Alteryx | 3% | Good-to-have |

### 2.2 What this table says in plain words

- **Only two tools clear the 50% line: Excel (60%) and SQL (54%).** Add "dashboards/reporting" (75%) and "communication" (73%) and you have the four must-haves. Everything else is a minority of postings.
- **Communication is a must-have in nearly three of four JDs.** Many HR professionals underrate this. It is your strongest card (see Section 5 and Book 11).
- **Power BI (40%) and Tableau (33%) together are common**, but they are not interchangeable, and many JDs name one or neither. Pick one first (Power BI is the more frequent here) and learn the ideas, which transfer.
- **Python is at 32%.** Useful, not universal, and lower in the MIS/people sample (16%, n=32, wide error).
- **The "good-to-have" tail is long and small.** Cloud (10%), DAX (5%), A/B testing (4%), Snowflake (4%) and Alteryx (3%) are each in 10% or fewer of JDs. Do not start there.

### 2.3 Correction callout: a popular belief the data does not support

> **"SQL, Python, Power BI and statistics are in almost all data analyst JDs."** This is repeated widely and **was not supported** in our sample. In the 0-2 year band, Python was in 32%, Power BI in 40%, Tableau in 33% and statistics in 23%. Excel and SQL are the only tools above half. (MS Section 3, last paragraph; plan.md Section 2.)
>
> Some career and training pages publish much higher figures (one, ownyourcareer.in, reports SQL at 98%, Python at 80%; MS Section 7). Their sample size and method are not disclosed, and our own counts do not reproduce them. Treat them as vendor/blog claims, unverified.

An observation, not a counted result: among the roughly 25 postings that required 3 or more years in the first sample (read but excluded from the tally), Python, Power BI/Tableau, cloud platforms and GenAI/ML appeared noticeably more often than in the 0-2 year set, while SQL, Excel and communication stayed constant. This is an impression from reading, not a measurement, but it fits the idea that Python and BI are what separate mid-level from entry-level roles.

### 2.4 The interview gap: why skills that JDs rarely name still get asked

JDs are one signal and interviews are another. In the interview research (candidate-reported, anonymous; about 20 company profiles, not a statistical sample; IP Section 4), the number of company profiles reporting each topic was:

| Topic in interviews | Profiles reporting it (of about 20) |
|---|---|
| SQL (joins, group by, Nth highest, window functions) | about 19 |
| Behavioural / HR round | about 15 |
| Project / resume walk-through | about 14 |
| Aptitude / online assessment | about 14 |
| Python / pandas (mostly basic) | about 10 |
| Business case / metric diagnosis | about 8 |
| Power BI / DAX | about 7 |
| Statistics / probability | about 6 |
| Guesstimates | about 6 |
| Excel | about 5 |

Reading this honestly:

- **SQL is the single most reported interview topic and also a JD must-have.** Treat it as non-negotiable (Book 2).
- **Project walk-through, aptitude and the behavioural round are near-universal** even though a JD never lists them as "skills". Prepare them (Books 8, 6 and 11).
- **Statistics (JD: 23%) and guesstimates/cases still show up in interviews** (about 6-8 profiles each), mostly at analytics firms and product companies. This is why Books 5 and 7 are kept even though the JD data alone would argue for trimming them.
- **Excel is mentioned in only about 5 interview profiles** though it is a JD must-have at 60%. Likely reason (our interpretation): interviewers often test it inside a case or take-home rather than as a standalone round, and it is rarely discussed in write-ups. Do not drop Excel because of this number.
- Python is mostly basic in the interview reports (lists, strings, duplicates, pandas), not deep.

### 2.5 Recommended learning order

Based on the two tools above 50% and the interview signal (guidance, not a measured outcome):

1. **Excel and SQL first** (Books 1 and 2). They are the only two tools above half of JDs, and SQL leads interview reports.
2. **One BI tool next,** Power BI first (Book 4), then Tableau basics if a target JD asks for it.
3. **Python after that** (Book 3), basics first.
4. **Then** statistics (Book 5), cases and scenarios (Books 7 and 8), and domain (Book 10).
5. **Aptitude (Book 6) and communication/behavioural prep (Book 11) run alongside,** not after.

If your target is MIS/reporting, Python can wait. If your target is a startup or product analyst role, SQL depth and metrics thinking come first, then Python.

### 2.6 Certificates

- **No named analytics certification appeared as a requirement in any sampled JD.** Certificates (Tableau, Power BI/Microsoft Data Analyst Associate, Google Data Analytics, CBAP) appeared only as stated advantages, and in a few roles requiring 3+ years (MS Section 5; MS Addendum "Other findings").
- Therefore a certificate is **optional signalling; its value in the Indian hiring market is unverified.** **No reliable data found** on whether certificates change interview-call rates. (B0S: searches found US-based vendor material and nothing India-specific on PL-300.)
- Decision rule: do a certificate only if it gives you a structured way to practise a tool you have already decided to learn, and only after the Excel and SQL basics. Never let a certificate stand in for a project you can explain.

### 2.7 GenAI: emerging, not a gate

- GenAI / AI tools were named in 14% of JDs (n=186, non-random, about +/-7 points). The 40-JD sub-sample, which counted AI tools such as Copilot and ChatGPT, showed 20%.
- Interview evidence is thin: **one** candidate-reported Infosys Hyderabad review (March 2026) with a GenAI/LLM test (IP Section 4). That is one report, not a pattern.
- Practical reading: being able to use AI assistants for analysis tasks is a plus; deep LLM knowledge is not a demonstrated entry requirement. See Book 9.

### 2.8 Caveats box

- Sample is non-random and skewed toward reachable sources (Built In, LinkedIn public pages, Shine, TheIndiaJobs, employer career sites).
- Naukri, Indeed, Glassdoor and foundit were blocked; AmbitionBox was not usable; LinkedIn was readable only as public pages in one sample (others got expired pages or none). The largest mass-market sources are therefore missing.
- Counts were made by reading each JD against a checklist; several samples used keyword matching (about +/-2 per count). Per-sample sizes are 40, 47, 42, 32 and 25; the GCC sample is 12 Amazon postings out of 25. Extraction errors are possible.
- Experience labels in Hyderabad/Bengaluru postings are sometimes wide ("0-4 yrs"); a few operational roles are weak fits for "data analyst".
- A skill "named" in a JD is not the same as "tested in the interview".

### 2.9 Limitations (Section 2)

JD percentages: n=186, non-random, about +/-7 points (per-sample figures are wider, about +/-15 to 20 points). Interview counts: candidate-reported, anonymous, profile counts not statistics. Certificate value, GenAI demand and the exact weight of Python at entry level are not settled by this evidence.

---

## Section 2b. Honest pay bands and switcher-friendly entry roles

### 2b.1 Read this first

- Most JDs do not state pay. Rows showing any figure: 8 of 40 (first sample, MS Section 4), 7 of 47 (Hyderabad), 7 of 42 (Bengaluru), 9 of 32 (MIS/people) and 0 of 25 (GCC), about 31 of 186 in all (some are monthly, stipend or aggregator figures). The tables below use the first sample plus the added samples; they are small and non-random.
- Pay claims from blogs and job-board snippets are **vendor/blog claim, unverified.** They are listed separately below and must not be mixed with posted figures.
- Your target is Rs 6-10 LPA. A few postings and unverified snippets show it, but it is the upper part of what we saw, not the middle.

### 2b.2 Pay stated in the sampled JDs

| Posting | Stated pay | Note |
|---|---|---|
| TopGrep Tech, Junior Power BI Developer/Analyst, Bengaluru/Hyderabad, 1-3 yrs | Rs 3.5-4.5 LPA | Cutshort listing, July 2026 |
| KPMG, Operations Analyst, Bengaluru, 1-2 yrs | Rs 3.5 LPA | Negotiable; page said posted about a year ago |
| OrbiTouch HR, Junior Data Analyst, Hyderabad, 0-2 yrs | Rs 4-5 LPA | Up to Rs 5 LPA, interview-dependent |
| PharmaForceIQ, Data Analyst, remote India, 2-4 yrs | Rs 4.25 LPA base | Built In |
| Hire Daily, Data Analyst, Hyderabad, 0-3 yrs | Rs 5-9 LPA | The aggregator page itself calls this an "estimate" |
| Peakflo, Data Analyst, remote India, about 1 yr | Rs 7-10 LPA | Built In; remote role |
| Weekday, Revenue Analytics Analyst, remote India, 2+ yrs | Rs 15-25 LPA | **Outlier**; remote, US-facing; do not use as a benchmark |
| TMI Group, MIS Executive, Hyderabad, 2+ yrs | Page showed "INR 160K-180K annually" | Likely about Rs 1.6-1.8 LPA per the page's own figure; **unverified**, possibly a data error; shown for completeness only |

The MIS/people sample adds: Honhr (one employer, five bulk-posted fresher/entry roles) showed a flat Rs 4.8 LPA on four of its rows and Rs 6.0 LPA on one (Strategy Analyst). The same file notes this is a posting template, so it should not be treated as five independent data points.

The Hyderabad and Bengaluru samples add these posted figures (jd_sample_hyderabad.md Section 6; jd_sample_bengaluru.md Section 5):

| Posting | Stated pay | Note |
|---|---|---|
| Newton School, Data Analyst, Bengaluru, fresher/0-1 yr | Rs 4-8 LPA | Wellfound |
| Codemonk, Associate Business Analyst, Bengaluru, 1-2 yrs | Rs 4-6 LPA | Wellfound |
| KPMG, Operation Analyst, Bengaluru, fresher, 6-month contract | Rs 3.65 LPA | Posted about a year ago |
| DSHINE PRO SOLUTIONS, Data Analyst, Bengaluru | Rs 3-5 LPA | Experience not shown |
| Guardian Capital, Operations Analyst, Hyderabad, 1+ yr | Rs 5-7 LPA fixed | LinkedIn |
| DeepThought CultureTech, fresher BA / analytics associate, Hyderabad | Rs 15k per month for a 6-month probation, then Rs 5-8 / 5-6 LPA | Small startup page |
| Skilltransform, Junior Data Analyst, Hyderabad, 0 yrs | Rs 1.8-3 LPA | Small provider; the file says far below MNC bands |
| Xohani Solutions, Data Analyst, Hyderabad/Bengaluru, 2-6 yrs | Rs 12-22 LPA | Above the 2-year ceiling; not a benchmark |
| Velocity, Data Analyst, Bengaluru, 2+ yrs | Rs 20-30 LPA plus equity | **Outlier**; not a benchmark |

The files also list monthly or unclear figures (for example Avyan Packaging up to Rs 40,000 per month; Swiggy via aggregator "INR 60K", period unstated; Unisys MIS Executive 18,000-24,000, period unstated); we leave those out of the LPA comparison.

### 2b.3 Reading the figures

- **JD-stated pay for 0-3 year roles mostly sits at Rs 3.5-9 LPA** (MS Section 4 "Reading"), with some lower (Rs 1.8-3 LPA at small employers) and a few higher outliers for 2+ year roles (Rs 12-30 LPA). MS Section 4 and plan.md Section 2 say Rs 6-10 LPA is reachable at GCC, product and finance-analytics employers; the evidence for that is thin (Peakflo Rs 7-10 LPA, Honhr Rs 6.0 LPA, plus the unverified snippets in 2b.4; no GCC JD showed pay). At 0-2 years, Rs 6 LPA or more is the upper half of what was observed.
- **Entry MIS and business analyst roles mostly cluster at Rs 3-6 LPA** (MS Addendum "Other findings"). Amazon, GCC and product-company postings are higher but did not state pay.
- **Do not read these as salary statistics.** Eight posted figures cannot describe a market, and several postings were old, remote, or contract roles.

### 2b.4 Unverified secondary snippets (label every time you quote them)

| Source (type) | Claim | Status |
|---|---|---|
| foundit "Data Analyst AVP", Hyderabad, 0-3 yrs (search snippet; page returned an access error) | Rs 5-12 LPA | Vendor/blog claim, unverified |
| ICE "Junior Data Analyst, Model Risk Management", Hyderabad (job-board card; no JD body read) | Rs 5.5-10 LPA | Unverified |
| EdTech Jobs "People Data Analyst", Bengaluru (snippet; experience not shown) | Rs 6-10 LPA | Unverified |
| Salary blogs (Jobrise) | about Rs 3.5-9 LPA (Hyderabad, 0-2 yrs); about Rs 4-12 LPA (Bengaluru entry/mid) | Blog estimates, unverified |
| Flexiple, Bengaluru | Platform median Rs 7.5 LPA | Unverified |
| Fresher-pay blogs (via B0S) | Rs 3.5-6 LPA indicative | Indicative, vendor-sourced; the blogs conflict with each other |
| HR-analytics pay pages from vendors (Keka, Taggd) | Conflicting entry pay claims | **Not used**; they disagree sharply |

Note that the secondary figures broadly overlap the posted ones, but "overlaps" is not "verified".

### 2b.5 The pay-cut question: no data, so use your own numbers

**No reliable data found** on the size of the pay cut (or gain) for HR professionals moving into analyst roles, on how pay varies by years of HR experience, or on how many switchers reach Rs 6-10 LPA in their first analyst job. Any article quoting a specific switcher uplift or discount is a vendor/blog claim, unverified.

What you can do instead is calculate your own position. Use the template below with your real figures. The numbers shown are **illustrative** round figures for arithmetic only; they are not evidence about the market.

| Line | Your figure | Illustrative example |
|---|---|---|
| A. Current annual fixed pay (CTC less variable, as paid) | ____ | Rs 8.0 lakh |
| B. Current annual variable/bonus you reliably get | ____ | Rs 0.5 lakh |
| C. Target first-role offer (use the posted ranges above, not the top) | ____ | Rs 5.5 lakh |
| D. Gap (A + B minus C) | ____ | Rs 3.0 lakh |
| E. Monthly take-home cut (D divided by 12, then adjust for tax) | ____ | about Rs 25,000 before tax adjustment |
| F. Savings you can afford to spend on the switch (Rs) | ____ | e.g. Rs 6.0 lakh |
| G. Months with no income if you resign before you have an offer (0 if you apply while employed; your own estimate, no research figure exists, see Section 6) | ____ | your number |
| H. Total cost of switching = D (first-year gap) + monthly current pay x G + any course fees | ____ | compute |
| I. Expected pay in year 2 if you succeed (a guess you write, not a fact) | ____ | your number |

Decision rule: **switch when F (what you can fund, in rupees) exceeds H (what the transition costs, in rupees) with a margin, and you can still pay fixed commitments.** If it does not, consider the lower-risk route first: add Excel and SQL reporting duties in your current HR job, build the projects, and apply for an internal move or a hybrid HR-analytics role. This protects income while you prove the skills.

### 2b.6 Switcher-friendly entry roles

Evidence: MS Section 6 and Appendix A (postings read October 2026). "Tools asked" are the tools named in those postings.

| Entry role type | Examples seen in sampled JDs | Tools asked | Why it suits a switcher |
|---|---|---|---|
| MIS / reporting | Tata Play Fiber SME MIS and Reporting (Bengaluru, Entry); EXL Associate BA, MIS Reporting (Bengaluru, 2-5 yrs); TMI MIS Executive (Hyderabad, 2+ yrs); Quess Assistant Manager MIS (Entry) | Excel (often advanced), VBA, dashboards, data cleaning | Excel-first; SQL optional. The lowest tool bar of the data roles. |
| Operations analyst | KPMG Operations Analyst (Bengaluru, 1-2 yrs); HPE Procurement Ops Analyst I (Bengaluru, 0-2 yrs); The Hackett Group Associate Analyst, GBS (Hyderabad, Entry) | Excel, dashboards, SQL nice to have | Process-minded; HR operations experience reads as relevant. |
| HR-tech reporting | Deutsche Bank Workday Prism Analytics and Reporting Consultant, HR IT (Bengaluru, Entry) | ETL, dashboards, communication | Direct use of HR domain; very few entry postings seen. |
| Research / pricing analyst | Easyship Pricing Analyst (Bengaluru, 2+ yrs), TriNet Associate Pricing Analyst (Hyderabad, under 2 yrs), Gartner Specialist Analyst (remote India, 0-2 yrs), Cushman & Wakefield Analyst (Hyderabad, Entry) | Excel, SQL, Tableau or Power BI | Excel-led analysis with writing and stakeholder work. |

Experience labels are as posted. The Deutsche Bank row carries the conflict described in 1.4 (Entry tag in MS Section 6 versus "Workday-reporting roles asked 3+ years" in the MS Addendum). Several of the roles above list 2 or more years, so "entry" here means the lowest bar among analyst roles, not a guarantee that a fresher is accepted.

**Hardest entry points:** Python-heavy product and startup analyst roles. These asked SQL plus Python and sometimes A/B testing (for example Rocket Learning Product Analyst, 2-4 yrs, named SQL, Tableau, Alteryx, Python, A/B testing). Interview reports for Flipkart, PhonePe and Meesho describe harder SQL (candidate-reported).

### 2b.7 What lifts pay toward Rs 6-10 LPA

This is qualitative and tied to the reading in 2b.3, not to a number:

- **Employer type.** The Rs 6-10 LPA postings we saw were at GCC, product and finance-analytics employers, not at the typical entry MIS posting.
- **SQL plus a BI tool plus proof.** The must-have list (Excel, SQL, dashboards, communication) plus a project you can walk through lines up with what those postings and the interview reports ask for (SQL in about 19 of 20 interview profiles; project walk-through in about 14).
- **Stakeholder and communication strength**, where your HR experience helps (Section 5).
- **Not shown to matter by this evidence:** a certificate. **No reliable data found.**

### 2b.8 A realistic first-role plan

- Treat Rs 3.5-6 LPA MIS, operations or BA entry as the *base case* that the evidence supports for a first analyst job, and Rs 6-10 LPA at a GCC, product or finance-analytics employer as the *stretch case* that exists but is the upper part of the range (MS Section 4 "Reading" and Addendum).
- Use the worksheet in 2b.5 with both cases before you resign or reduce notice periods.

### 2b.9 Limitations (Section 2b)

- Pay was stated in few JDs (about 31 of 186 rows; 8 of 40 in the original sample, 9 of 32 in the MIS/people sample, 0 of 25 in the GCC sample). Several are remote, old, contract, small-employer or aggregator figures.
- Secondary snippets are unverified; HR-analytics vendor pay pages conflict and were not used.
- No data found on HR-to-analyst pay change, pay by age or seniority, certificate effect, or switcher success rates. The worksheet uses your own numbers; every figure in it marked illustrative is invented for arithmetic only.

---

## Section 3. Interview process by company type (with reliability caveats)

### 3.0 Read this first: how reliable is this section?

Nobody publishes an official interview structure for data analyst roles. Everything below is what anonymous candidates said happened to them. Treat it as a map drawn from travellers' notes, not a timetable.

- **Candidate-reported, anonymous.** Reports span 2009 to 2026. Dates are given where known. (IP Section 1)
- **Blocked sources.** Glassdoor and AmbitionBox pages could not be opened by the researcher; Glassdoor content comes only from search-tool summaries of the pages. Reddit, LinkedIn and YouTube gave no evidence at all. (IP Section 1)
- **Few pages read in full.** Only about 9 pages were read directly. Everything else is a summary of a page or a third-party prep guide. (IP Section 1)
- **Anecdote rule.** A pattern backed by fewer than 3 independent sources is called an "anecdote" here. (IP Section 1)
- **Campus versus lateral.** Many reports are campus-drive reports. You are a lateral/switcher candidate, so the process you meet may differ. (IP Section 1)
- **Location.** Hyderabad and Bengaluru evidence is weak; many reports come from Chennai, Pune, Noida, Mumbai or an unstated city. (IP Section 1)

**Labels used in this guide:**

| Label | Meaning |
|---|---|
| [R] | The researcher read the page |
| [S] | Search-tool summary of a page that could not be opened; wording unverified |
| [G] | Third-party prep guide (InterviewQuery, Dataford, Hyring, FACE Prep and similar), not evidence of company policy |
| anecdote | Fewer than 3 independent sources |
| unverified | Single weak source or none |

**Do this before every interview:** ask the recruiter, in writing, "How many rounds are there, what does each one test, and how long is each?" Recruiters usually answer. That answer beats everything in this section.

### 3.1 Service MNCs (TCS, Infosys, Accenture, Deloitte USI, Cognizant, Wipro)

Reported shape: 2 to 4 rounds. Usually an online aptitude/assessment, a technical interview, sometimes a managerial/project round, then HR. (IP 2.1)

| Company | What was reported | Label |
|---|---|---|
| TCS | A guide says 3 rounds (technical, managerial, HR), driven by your resume. One Hyderabad review of an automated "bot-run" interview was for a data engineer role, not DA. | [G]; [S] |
| Infosys | Online assessment (aptitude plus basic analytics), then technical (SQL, Excel, Python, Power BI/Tableau, data interpretation, a case), then HR. A guide says 2-3 rounds. One Hyderabad review (interview March 2026) reports 4 rounds with a GenAI/LLM/RAG technical test; the role was not confirmed as DA. | [S]; [G]; anecdote (1 report) |
| Accenture India | Aptitude/cognitive test, a technical test, and an English communication assessment. A Bengaluru report describes an elimination round (verbal, logical, quant, core CS including databases, 1-2 coding problems) followed by a non-elimination English communication assessment. A January 2026 Bangalore-Rural report: aptitude, then technical on Python, SQL and basic statistics (INNER vs LEFT JOIN asked). A GfG DA post lists phone screen, technical (SQL, Excel, data scenarios), behavioural, case/technical, final, but gives no questions, location or date. | [G/S]; [S]; [R] |
| Deloitte USI (Hyderabad) | 2025-26 reviewers report 2 rounds: round 1 SQL (basics, window functions, duplicates, optimisation), round 2 Power BI (row-level security, optimisation, SUM vs SUMX) plus project workflow, with about a week's wait. A Nov 2025 analyst report: an aptitude-style first round, then a project explanation plus two medium-hard SQL questions, of which the candidate solved one. The 2021 campus process (GfG): a 75-minute AMCAT aptitude test, then one technical-cum-HR round described as easy; 36 of 103 shortlisted candidates were selected. | [S]; [S]; [R] (campus, 2021) |
| Cognizant (Hyderabad) | July 2025: two technical rounds (SQL, business analysis, stakeholder management) plus a casual HR round. A Feb 2025 report (role unstated): online communication round, MCQ plus coding with basic SQL, an in-person round focused on Java with two SQL questions, about 3 months in total. | [S]; [S] |
| Wipro | A guide says 3 rounds: online assessment (aptitude; sometimes coding), technical (SQL, analysis, Excel/Power BI, projects), HR. Candidate reports mention Power BI/DAX and SQL (joins, CTE, stored procedures) in Bangalore-Rural (2023) and joins/GROUP BY/HAVING in Noida (2025). One reviewer saw a technical round on ML and statistics (anecdote). | [G]; [S] |

**Pattern.** SQL basics, Power BI/DAX concepts, Excel, basic Python, a project walk-through, aptitude, then HR. Difficulty is mostly basic to medium; the Deloitte 2021 campus round was "easy" [R], and Accenture is rated "medium" by a Dataford aggregate (its claimed 58% offer rate comes from an unverified method, so do not rely on it) [G]. What interviewers were said to probe: resume and project depth (a 2015 Deloitte Hyderabad BI review said every point on the resume was probed [S]; the TCS guide says "resume-driven" [G]) and, at Accenture, English communication. No group discussion (GD) appears in any of these service-MNC sources. (IP 2.1)

**Timelines.** One week after round 2 (Deloitte, [S]); 1-2 weeks (TCS guide, [G]); 3 months (one Cognizant candidate, [S]). Accenture and Wipro timelines are not reliably stated. Treat all as unverified.

**GenAI.** One Infosys Hyderabad report (March 2026) is the only direct interview evidence. Call it "emerging, 1 report, not a pattern." (IP Section 4)

### 3.2 GCCs (global capability centres): Amazon, Wells Fargo, Novartis, HSBC, JPMorgan, Microsoft

| Company | What was reported | Reliability |
|---|---|---|
| Amazon (Bengaluru/Hyderabad; BA, BIE) | The most consistent GCC pattern. A LeetCode BA-II India post: 5 rounds, an SQL screen on a shared screen, then scenario and Leadership Principle (LP) rounds on Chime [S]. A GfG BIE Bangalore post (fresh graduate, early 2023): 5 rounds: online analytical/data-interpretation test, SQL plus data modelling, LP behavioural, a data-analysis/case study, a final with a senior manager [R]. A Hyderabad review rated it Easy with basic-to-medium SQL (GROUP BY, joins, window functions) and basic Python [S]. A Bengaluru 2025 review: third-highest salary per department using DENSE_RANK; rejection came after over a month with no explanation [S]. | About 4 India sources agree on "SQL early, LP-based behavioural in most later rounds" (IP 2.2). Best-supported GCC. |
| Wells Fargo (Hyderabad) | Reviews are for Senior Analytics Consultant, not plain DA. Nov 2024: first round on Teams with Tableau, SQL and logical reasoning; SQL joins, TRUNCATE vs DELETE, views vs temp tables; another reviewer reported about an hour of SQL plus SSIS/SSRS and window functions; the in-person managerial round was almost non-technical. 3 rounds (technical, managerial, HR) in about four weeks; one candidate was rejected as "not technically strong". | [S]; about 3-4 reviews |
| Novartis (Hyderabad) | Varies widely. March 2023: 6 rounds over 2 weeks including an Excel case study (pivots, rank, formulas). Sept 2025 campus: online MCQ, 4 technical rounds, HR. Another Sept 2025 report: a group discussion, project interview, HR. Roles not confirmed as DA. | [S]; anecdotes. Strong signal only for the Excel case and one GD |
| HSBC (Hyderabad) | One March 2026 report: 2 rounds, technical (SQL, Python, banking functions, resume) then HR. A Mumbai June 2026 report: 3 interview rounds plus 2 HR, a psychometric test, Python, Power BI, Looker. | [S]; thin, anecdotes |
| JPMorgan (Hyderabad) | One review calls the process long with too many rounds, with basic Python questions. A guide (not Hyderabad-specific) lists online assessment, recruiter screen, technical, superday, live coding over 4-6 weeks. | [S]; [G]. Treat all as unverified for full-time Hyderabad DA |
| Microsoft (Hyderabad/Bengaluru) | Very weak. Hyderabad DA: moderate difficulty, basic CTE SQL; another Hyderabad review (Jan 2024) lists Power BI, Fabric, Azure, DSA, Excel; a Bengaluru DA: HR screen, SQL technical, final case study; another Bengaluru report "very hard" with coding/DSA. | [S]; unverified for the India development centre |

**GCC common thread.** SQL (joins, window functions, ranking) is the one constant. Tools differ by team: Tableau at Wells Fargo, Power BI at Deloitte and Microsoft, an Excel case at Novartis. Behavioural/LP weight is high at Amazon; for Microsoft it is only guide-level evidence. Difficulty in India reports is basic to medium (Amazon Hyderabad "Easy", HSBC 2/5 on a small base) but not uniform. Timelines: Wells Fargo about 4 weeks, Novartis 2 weeks, JPMorgan guide 4-6 weeks. (IP 2.2)

### 3.3 Analytics firms (Tiger Analytics, Fractal, Mu Sigma, LatentView, Indium)

| Company | What was reported | Reliability |
|---|---|---|
| Tiger Analytics | GfG campus DA post (year unknown): 4 rounds, a roughly 90-minute proctored online assessment (about 20 aptitude/maths, 10 CS fundamentals, 2 coding), Technical 1 (coding, SQL, Bayes/conditional probability, projects), Technical 2 (probability, statistics, puzzles, project discussion), HR. The writer called stats/probability the hardest part. Funnel: 220 took the test, about 50 shortlisted, 5 selected. Summaries add SQL second-highest salary, self-join, window function and a hypothesis-test example. | [R] (campus); [S]. About 4 sources. |
| Fractal | One 2024 Bengaluru BA report: a 75-question aptitude test (quant, logical, verbal, some analytics, ending in a video introduction), a technical round built on the resume, then HR. Other reports: a technical test of 8 questions (4 SQL, 4 Python/R) and a business round with guesstimates, probability and market-entry cases, scored on structure. | [S]; about 3-4 sources. A "6-7 rounds" figure from an aggregator is unverified. |
| Mu Sigma | A FACE Prep guide: 3-4 rounds: aptitude plus psychometric, a video-synthesis observational test, a group case-study activity, a personal interview (technical, then HR). Technical content is guesstimates, case/metric design and puzzles, graded on structure and stated assumptions rather than the final number. Some 2026 cohorts reportedly add an AI-led conversational screening (AI as interviewer). Mostly campus/trainee hiring. A claim that only 15-20% clear the aptitude cutoff comes from a prep site and is unverified. | [R/G] (guide); [S] for candidate corroboration |
| LatentView | A Feb 2026 Chennai report: planned 3 rounds (technical screen, technical, client) with a project-manager round added. A guide says 4 rounds. A 2020 GfG campus post (Analytics Engineer, virtual) had 6 rounds, including a GD. **No Hyderabad or Bengaluru-specific report was found (Chennai is its base).** | [S]; [G]; [R] (2020 campus) |
| Indium Software (Hyderabad/Chennai) | The most Hyderabad-relevant of this group. July 2026: 4 rounds (2 technical, a client round, HR). Jan 2026: written test (aptitude, logical, SQL, analytical), then two technical levels. May 2026: a one-day process with a GD and 2 technical rounds covering ML basics and a market-estimation case. SQL joins, aggregates, window functions, CTEs; Tableau. | [S]; roughly 4-5 reviews. Review-to-detail mapping unverified. |

**Pattern.** An aptitude gate first, then 1-2 technical rounds (SQL, Python, probability), a case or guesstimate, a client round at Indium, then HR. The aptitude gate and the stats/probability questions are harder here than at service MNCs, while the interview rounds themselves are reported as "medium". Interviewers were said to look for structure, assumptions, project depth and "business understanding". Timelines: one Tiger candidate reported 3 weeks [S]; the rest are unverified. (IP 2.3)

### 3.4 Product companies and startups (Flipkart, PhonePe, Meesho; Swiggy and Zepto unverified)

| Company | What was reported | Reliability |
|---|---|---|
| Flipkart (Bengaluru) | A review of a 2023 interview: 4 rounds: pre-screen, guesstimates plus puzzles, case studies, a KPI round, plus hands-on SQL. A 2024 report: aptitude test with SQL, logical reasoning and statistics. Another: 2 rounds (resume-based, then business metrics). Round counts conflict (2-4). | [S]; about 4-5 reports |
| PhonePe | A BA online assessment: quant aptitude, logical reasoning, and 5 SQL questions (1 easy, 2 medium, 2 hard). Bengaluru April 2025 (role unstated): a 15-minute recruiter call, then a manager round that was "all SQL... LeetCode-hard" with 4-5 queries. April 2024: 3 rounds (SQL, puzzles/experience, case/scenario). A Hyring guide says there is no fixed path and calls itself an editorial map, not official. | [S]; [R/G]; 3 candidate reports |
| Meesho | An online SQL-coding assessment (reports vary: 10-12 SQL questions, or 4 medium-hard SQL plus 24 MCQs on SQL, aptitude and Excel), an SQL technical round, a case/product round, then HR/manager. Topics: window functions, CTEs, UNION vs UNION ALL, recursive CTE. Cases: declining completed orders, root-cause analysis. | [S]; about 4-6 sources. Strongest startup pattern. Bengaluru detail brief. |
| Swiggy | One guide says 5 rounds, another says 2-3 (conflicting). Candidate reports found were for Data Scientist 1, not DA. | [G]; [S]. **Unverified for DA.** |
| Zepto | No first-hand DA reports found. Guides say about 4 stages over 3-5 weeks with a take-home or live data exercise. | [G] only. **Unverified.** |

**Pattern.** The SQL online test replaces the aptitude test, followed by a hard SQL round, then a case/metrics round and a manager/HR round. SQL difficulty here is the highest of any type ("LeetCode-hard" at PhonePe, "moderate to tough" at Meesho). Interviewers were said to value first-principles thinking and a justified approach, not only the answer (Swiggy and PhonePe guides, [G]). GD appears only for PhonePe campus hiring, per a guide. Timelines are mostly unverified. (IP 2.4)

### 3.5 Comparison table (all cells candidate-reported and anecdotal)

| Dimension | Service MNCs | GCCs | Analytics firms | Product / startups |
|---|---|---|---|---|
| Typical rounds | 2-4 | 2-6 (Amazon 5; Wells Fargo 3; HSBC 2; Novartis 2-6) | 3-6 (Tiger 4; Mu Sigma 3-4; Indium 4; LatentView 3-6) | 2-5 (Meesho 2-3; PhonePe 2-3; Flipkart 2-4; see note below) |
| First filter | Aptitude / online test | SQL screen or analytical online test | Long aptitude plus coding/SQL test | SQL-heavy online test |
| SQL difficulty | Basic-medium | Basic-medium | Medium | Medium-hard |
| Case / guesstimate | Rare | Amazon case; Novartis Excel case | Common | Common |
| Stats / probability | Basic | Rare | Common and hard | Occasional |
| GD | None seen | Novartis (1 report) | LatentView 2020, Mu Sigma, Indium 2026 | PhonePe campus (guide) |
| Timelines reported | about 1-2 weeks to 3 months | about 2-6 weeks | about 3 weeks (1 report) | Mostly unverified |
| Evidence strength | Moderate (many thin reports) | Weak to moderate | Moderate (campus-skewed) | Moderate for Meesho/Flipkart/PhonePe; weak for Swiggy/Zepto |

(IP Section 3)

Note on conflict: the IP table gives Meesho and PhonePe as 2-3 rounds, but IP Section 2.4 describes Meesho as four steps (online test, SQL technical, case/product, HR/manager) and PhonePe as a recruiter call plus a manager round. Counting an online test as a round or not explains most of this. Use the ranges as rough only.

### 3.6 Group discussions, timelines and the typical loop

- **GD.** It is a campus/early-career screening device at mid-size analytics and BPO-adjacent firms, about 6 sources, mostly campus and mostly before 2023. Examples: Ugam 2021 (about 50% eliminated at the GD [R]), LatentView 2020 [R], Mu Sigma, Indium May 2026 (Hyderabad, [S]), Novartis Sept 2025 [S]. **No evidence of GD for lateral/switcher hires at service MNCs, GCCs or startups.** Treat the claim that some Hyderabad mid-size firms still use GDs as "few reports" (Indium 1, Novartis 1). Preparation is in Book 11 Part 7. (IP 2.5)
- **Timelines.** Roughly 1 week to 3 months at service companies; 2-6 weeks at GCCs; others mostly unverified. Ask the recruiter. (IP Section 3)
- **Typical loop.** Service MNCs and analytics firms: online test, then technical, then HR. GCCs and startups: an SQL screen takes the place of the aptitude test. (IP Section 5 item 13)

### Limitations (Section 3)

- No company confirmed any process. Reports are anonymous and unverifiable, the Glassdoor/AmbitionBox/Reddit/LinkedIn/YouTube gaps are real, and several review-to-URL mappings are unverified.
- Evidence for HSBC, JPMorgan, Microsoft, Swiggy and Zepto is thin or unverified, and LatentView has no Hyderabad/Bengaluru report.
- Salary and lateral-versus-fresher differences are not covered by these sources.
- Companies change processes. Nothing here predicts what a specific team will do next month.

---

## Section 4. Round-by-round expectations

Each block says what the round tests, where it was reported, how long (only where the research gives a figure), and which book prepares you. Evidence labels as in Section 3. Counts of "profiles" come from about 20 company profiles in IP Section 4, are not a statistical sample, and one profile can rest on one report.

### 4.1 At a glance

| Round | Reported by (company type) | Frequency signal (IP Section 4) | Prepare with |
|---|---|---|---|
| Online test: aptitude / assessment | Service MNCs, analytics firms, Accenture, Deloitte | about 14 profiles | Book 6 |
| SQL (online and live) | All four types | about 19 of 20 profiles | Book 2 |
| Excel / Power BI / Tableau task | Deloitte, Wipro, Infosys (Power BI); Novartis (Excel case); Wells Fargo, Indium (Tableau) | Power BI about 7; Excel about 5; Tableau about 4 | Books 1 and 4 |
| Case / guesstimate | Analytics firms, Flipkart, Meesho, Amazon, Novartis | cases about 8; guesstimates about 6 | Book 7 (and Book 8) |
| Stats / probability | Tiger, Fractal; occasionally Flipkart | about 6 | Book 5 |
| Take-home / live data exercise | Zepto only, per guides | [G] only, unverified | Books 1, 2, 4, 8 |
| Project walk-through | Across types | about 14 profiles | Book 8 Part 8 |
| Managerial | Wells Fargo, startups, TCS guide | not tallied | Book 11 |
| HR / behavioural | Universal last round; Amazon is LP-heavy | about 15 profiles | Book 11 |
| Group discussion | Mostly campus-era; Indium and Novartis 2025-26 | about 6, mostly campus | Book 11 Part 7 |

### 4.2 Online test (aptitude, SQL, MCQ)

- **What is tested.** Quant, logical and verbal aptitude; data interpretation; basic CS or database questions; sometimes SQL or small coding tasks. Examples: Tiger's roughly 90-minute proctored test (about 20 aptitude/maths, 10 CS, 2 coding) [R]; Fractal's 75-question test with a video introduction [S]; Deloitte campus AMCAT, 75 minutes [R]; Accenture's elimination round plus a non-elimination English communication assessment [G/S]; a Novartis online MCQ with a pie-chart interpretation question [S]; PhonePe's quant/logical test plus 5 SQL questions [S]; one Meesho variant with 4 SQL questions plus 24 MCQs on SQL, aptitude and Excel [S].
- **Who uses it.** Service MNCs and analytics firms as a first gate; GCCs and startups swap in an SQL-flavoured test.
- **Length.** Only two durations are reported: Tiger about 90 minutes and Deloitte campus AMCAT 75 minutes. Fractal (75 questions) and the Meesho variant (4 SQL plus 24 MCQs) give question counts, not time. Do not assume others.
- **Prepare.** Book 6 for aptitude and data interpretation; Book 2 for SQL questions; Book 3 for small coding items.
- **Honest note (guidance, not research).** These tests act as a filter, so a switcher with a good resume could be cut here. Practise them under time limits.

### 4.3 Live SQL

- **What is tested.** Joins, GROUP BY/HAVING, Nth-highest salary (DENSE_RANK appears in an Amazon report), window functions, CTEs, duplicates, subqueries; at startups also recursive CTEs, self-joins, cumulative sums. (IP 2.1-2.4)
- **Difficulty by type (reports).** Service MNCs and GCCs basic to medium; analytics firms medium; product/startups medium-hard, with "LeetCode-hard" at PhonePe. Individual exceptions exist: a Deloitte Nov 2025 candidate solved one of two medium-hard questions [S]. (IP Section 3)
- **Format.** Shared screen (Amazon, [S]), Teams call (Wells Fargo, [S]), or in-person.
- **Prepare.** Book 2. Aim for the tier of the company type you target, and say your reasoning aloud while you write.

### 4.4 Excel, Power BI or Tableau task

- **What is tested.** Power BI/DAX concepts: SUM vs SUMX, ALL vs ALLEXCEPT, DATEDIFF, row-level security, incremental refresh, optimisation, Power Query, data modelling [S]. Tableau: blending, LODs, filters [S]. Excel: a Novartis case using pivots, rank and formulas [S].
- **Who uses it.** Power BI at Deloitte, Wipro, Infosys, Microsoft and HSBC; Tableau at Wells Fargo, Indium, LatentView, Infosys; Excel case at Novartis. Tool choice depends on the team, so read the JD.
- **Prepare.** Books 1 and 4. Match the tool named in the JD.

### 4.5 Case study and guesstimate

- **What is tested.** Structured thinking and explicit assumptions rather than the final number (Mu Sigma guide [R/G]; Fractal summary [S]). Examples reported: petrol stations in India, coffee shops in Bangalore, a 15% footfall-drop case, market entry, profitability, sweet shops in a hometown, number of stores in New Delhi, declining completed orders on an executive dashboard, and a KPI definition round at Flipkart.
- **Who uses it.** Analytics firms, Flipkart, Meesho, Amazon (data-analysis/case round), Novartis and Indium. Rare at service MNCs.
- **Prepare.** Book 7 for structure and estimation, Book 8 for metric-change investigations and data interpretation.

### 4.6 Take-home or live data exercise

Only guides mention it, for Zepto, and no first-hand DA report was found. Treat it as **unverified**. If you are told to expect one, ask the recruiter for the time limit, data format and expected output. Practise end to end with Books 1, 2, 4 and 8.

### 4.7 Statistics and probability

- **What is tested.** Bayes and conditional probability, hypothesis-test examples, probability puzzles. Tiger's campus writer called this the hardest part; it also appears at Fractal and, in MCQ form, at Flipkart. Service-MNC reports mention only basic statistics (Accenture). (IP 2.2-2.4, Section 4)
- **Prepare.** Book 5. Analytics firms justify the effort; for most service or GCC roles, basics suffice on this evidence.

### 4.8 Project walk-through

- **What is tested.** Whether you really did what the resume says and can explain it end to end. Near-universal: about 14 profiles, including Deloitte, TCS, Wipro, Fractal, Tiger, LatentView, Mu Sigma and Flipkart. The research does not say how decisive it is for switchers; as guidance, your projects are your main proof, so prepare this round well.
- **Prepare.** Book 8 Part 8 (project deep-dive questions), Book 12 for portfolio and resume, and have one project you can explain in plain business words.

### 4.9 Managerial and HR/behavioural rounds

- **What is tested.** Managerial rounds can be almost non-technical (Wells Fargo, [S]). HR rounds cover career goals, relocation and your switch story. Amazon is the only company with consistent LP evidence: scenario and LP rounds with STAR-style answers. (IP 2.2, Section 5 item 11)
- **How to do well.** Prepare your career-switch story first (Book 11 Parts 1-2), then STAR stories (Book 11 Part 3), HR logistics (Book 11 Part 8), and the Amazon Leadership Principles bank if you apply there (Book 11 Part 11).

### 4.10 Group discussion

See Section 3.6: mostly campus, mostly before 2023, with Indium (May 2026) and Novartis (Sept 2025) as the recent reports. Ugam's candidate advice was to be fluent, not interrupt, and make a few strong points [R]. Practise lightly with Book 11 Part 7.

### 4.11 When you blank or do not know

No research source measures how interviewers react, so this is guidance, not data. A simple rule: say what you do know, state your assumption, work the problem aloud, and ask a clarifying question. Interviewers at analytics firms were reported to score structure and assumptions, not only answers (Mu Sigma, Fractal, [R/G], [S]). Practise this with Book 11 Part 9.

### 4.12 Putting it together: what to expect by target

| If you target | Likely loop (candidate-reported) | Spend your time on |
|---|---|---|
| Service MNC | Online test, technical (SQL/Power BI/Excel/projects), HR | Books 6, 2, 1, 4, then Book 11 |
| GCC | SQL screen, tool-specific round, managerial, HR (Amazon: LP rounds) | Books 2, 4, 8, 11 |
| Analytics firm | Aptitude gate, technical (SQL/Python/probability), case, HR | Books 6, 2, 5, 7, 3 |
| Product / startup | SQL test, hard SQL round, case/metrics, manager/HR | Books 2, 7, 8, 5 |

Before any of these, confirm the structure with the recruiter.

### Limitations (Section 4)

- Round contents are candidate-reported. Durations are known for only two tests (Tiger, Deloitte AMCAT); Fractal and Meesho give question counts only.
- The IP tallies have small internal inconsistencies: the SQL count "about 19 of 20" lists three exclusions (Zepto, Swiggy, Microsoft), which would give about 17; the guesstimate count of "about 6" names Fractal twice (5 distinct companies). Read all counts as rough.
- Frequency counts are tallies of company profiles, not a sample of interviews, and several rest on one report.
- No reliable data was found on how often switchers (as against freshers) are cut at each round, or on how interviewers treat HR-to-analytics candidates specifically.
- The "how to behave" advice in 4.11 and the preparation priorities in 4.12 are guidance, not research findings.

---

## Section 5. How your HR experience is an advantage (and where it is not)

Short version: HR gives you a business domain, daily contact with people data, and the communication habits that most analyst job descriptions ask for. It does not replace Excel or SQL. Treat it as the reason a hiring manager keeps your resume in the pile, and treat the technical skills as the reason you pass the test.

### 5.1 What the job postings say about communication and stakeholders

Evidence labels: JD percentages come from a pooled sample of 186 in-scope postings (non-random, about +/-7 points; MS Addendum).

| Skill named in the JD | Share of 186 JDs | What it means for you |
|---|---|---|
| Communication | 73% (labelled "must-have") | HR work is built on this: explaining policy, handling difficult conversations, writing clearly |
| Stakeholder management | 44% (labelled "common"); 60-64% in the Hyderabad, Bengaluru and GCC sub-samples (n=47, 42, 25), but only 15-19% in the first sample and the MIS/people sample | You already manage managers, employees, leadership and vendors |
| Dashboards/reporting | 75% | You already produce headcount, attrition and hiring reports, usually in Excel |
| Excel | 60% | Many HR professionals already use pivots and lookups; this is your head start if so |
| SQL | 54% | Usually NOT an HR strength (general knowledge, not checked). This is the gap to close |

Reading: employers ask for communication more often than they ask for Python (32%) or Power BI (40%). That is useful for you, but a JD line is not a hiring guarantee. Stakeholder skills help in the interview and on the job; they do not get you through an SQL test.

### 5.2 The data HR already touches

Most HR professionals work near three kinds of data, even if they never called it "data":

- **HRIS** (human resource information system, for example Workday or SuccessFactors): employee master data, joiners, leavers, grades, reporting lines.
- **Payroll and attendance:** pay components, leave, overtime, absenteeism.
- **ATS** (applicant tracking system): applicants, stages, offers, source of hire.

Why this matters: a person who understands what a "leaver" record means, why headcount differs between two reports, or why attendance data is messy, needs less explaining in a people-data role. This is domain knowledge, and Book 10 Part 1 (HR / People Analytics) is built around it.

Bridge roles seen in the research (MS Section 6): a Workday Prism Analytics and Reporting role at Deutsche Bank, Bengaluru, tagged Entry; an HR Analytics and Visualization role at Syneos, Hyderabad, asking 3+ years; a People Analytics role at Unisys, Bengaluru, asking 4-6 years; and an Associate Analyst (organisational change management) role at Unisys, remote India, asking 0-2 years, using Excel and Power BI. A "People Data Analyst" listing in Bengaluru showed Rs 6-10 LPA in a search snippet only (experience not shown; unverified secondary source).

### 5.3 Translation table: HR task to analytics phrasing

Illustrative wording, no numbers. Only claim what you actually did.

| What you did in HR | How an analytics resume or interview says it |
|---|---|
| Tracked monthly attrition in Excel | Built a recurring attrition report; analysed exits by tenure, department and manager (cohort and retention analysis) |
| Reported open positions and hiring status | Built a hiring-funnel view (applications, interviews, offers, joins) and tracked stage-to-stage conversion |
| Reconciled payroll or attendance data | Cleaned and validated data from multiple sources; found and fixed mismatches before reporting |
| Prepared a monthly HR review deck | Turned data into a stakeholder-ready summary with a recommendation |
| Ran an engagement survey | Collected survey data, summarised themes and scores, and presented drivers to leadership |
| Compared pay across grades | Segmented compensation data and flagged outliers |

Where to turn this into your story and resume: Book 11 Parts 1-2 (career-switch story, "why analytics", "why leave HR") and Book 12 Section 1 (resume). For the matching interview-answer practice on HR cases, see Book 7 Part 8 and Book 10 Part 1.

### 5.4 Honest limits

1. **No pure people-analytics role at 0-2 years that names Workday, SuccessFactors or Visier was found** (MS Addendum "Other findings"; MIS/people sample: all Workday-reporting JDs asked 3+ years). Sources conflict here: MS Section 6 lists the Deutsche Bank Workday role as Entry, while the Addendum says Workday-reporting roles asked 3+ years. Two near-misses also exist in the pooled samples: Goldman Sachs "Human Capital Management Analyst - HRIS", Hyderabad, 1-3 years (Hyderabad sample), and McDonald's "HR Analytics" supervisor, Hyderabad, experience not stated (MIS/people sample). So the evidence is a handful of postings, not a market count, and a "people analytics first" plan is a bet on a thin market. See Q34 and Q75 in Section 7.
2. **Domain does not replace SQL or Excel.** Interviews test SQL in about 19 of the 20 company profiles examined (candidate-reported, anonymous, one profile can rest on a single report; IP Section 4).
3. **HR domain helps most in HR-related analyst roles and less in a product or e-commerce analyst role.** There, you will be compared with people who know funnels and SQL. For those, you need Book 10 Parts 2 onward and strong SQL (Book 2).
4. **Domain knowledge is not a technical credential.** "I know attrition" must be followed by "and here is the query and the dashboard I built" (Book 12 Section 2).

**No reliable data found** on how much HR experience raises a switcher's chance of being hired or paid, or on how many HR professionals complete this switch. Decision rule: if two or three JDs from your target list mention HR, people, workforce or "HRIS" data, lead with the domain in your summary; if none do, lead with Excel, SQL and a project, and mention HR as supporting context.

**Limitations of this section:** JD percentages are a non-random sample (n=186, about +/-7 points). The translation table is illustrative language, not evidence of what recruiters prefer. The bridge-role list is a handful of postings read on 2026-10-20/21, not a market count.

---

## Section 6. Six-month learning roadmap for a non-technical beginner

### 6.0 Read this first: these are targets, not research findings

The week-by-week schedule, the hours per day, the monthly milestones and the "start applying" timing below are a **study-plan design** (plan.md Section 7). They are **not researched figures**. **No reliable data found** on how long this switch takes for a non-technical beginner, or on success rates for any plan. If you work full time, expect it to stretch; see Q2, Q13, Q49 and Q52. Blog timelines in the research (B0S) come from training providers and platform founders and are not used as evidence.

### 6.1 The time budget (arithmetic, not a promise)

- Plan assumption: 2-3 hours a day.
- Daily split: 40% SQL, Excel and Power BI practice; 25% Python and statistics; 20% cases, guesstimates and aptitude; 15% soft skills and portfolio.
- At 2.5 hours a day that is about 60, 38, 30 and 22 minutes for those four buckets respectively (rounded arithmetic).
- Soft-skill practice from Book 11 Part 10 runs at 15 minutes a day from Week 1.
- Total over 24 weeks: at 5 study days a week, 2-3 hours a day gives about 240-360 hours; at 7 days a week, about 336-504 hours. If you can study fewer hours, the same plan takes proportionally longer; recompute with your own weekly hours.

The split follows what the market sample suggests: Excel and SQL are the only two tools named in more than half of the JDs (60% and 54%, n=186, non-random, about +/-7 points), so they come first (MS Addendum). Python is named in 32%, and Power BI in 40%.

### 6.2 Month-by-month plan

The plan has 24 weeks. Months below are four-week blocks, so they line up with the schedule only approximately (the plan.md week ranges overlap month edges).

| Month (weeks) | Focus | Books | Milestone (target) | Self-check at month end |
|---|---|---|---|---|
| M1 (Wk 1-4) | Excel, maths basics, orientation, first SQL | Book 0; Book 1; Book 5 Parts 1-2; Book 6 Parts 1-2; Book 2 begins in Wk 4 | Build a clean HR attrition workbook with pivots, lookups and a chart | Rebuild a monthly headcount report from raw data in one sitting, without help |
| M2 (Wk 5-8) | SQL core | Book 2 Parts 1-6; Book 6 Parts 3-5 | Write SELECT, GROUP BY, JOIN, subquery and window-function queries on your own dataset | Solve a set of easy-medium SQL questions under a time limit (you choose the limit) |
| M3 (Wk 9-12) | SQL scenarios and Power BI | Book 2 Parts 7-12; Book 4 Parts 1-4; Book 4 Parts 5-12 begin in Wk 11 | One working Power BI dashboard from a clean dataset | Explain your data model and every measure on screen, out loud |
| M4 (Wk 13-16) | Dashboards finished, statistics, Python basics | Book 4 Parts 5-12; Book 5 Parts 3-12; Book 3 Parts 1-6 | Read a CSV in pandas, clean it, summarise it | Explain mean vs median, p-value and correlation vs causation in plain words |
| M5 (Wk 17-20) | Python finish, cases, scenarios, HR domain, portfolio | Book 3 Parts 7-12; Book 7; Book 8; Book 10 (HR first) | Two portfolio projects finished and written up | Do a "walk me through your project" session with a friend (Book 8 Part 8) |
| M6 (Wk 21-24) | ML and AI awareness, soft skills, mocks, applications | Book 9; Book 6 mocks; Book 11; Book 12 | Resume, LinkedIn and Naukri profile done; mock interviews done; applications going out | Full mock interview rounds across SQL, project and HR |

Note that the plan.md schedule gives Book 4 Parts 1-4 in weeks 8-10 and Parts 5-12 in weeks 11-13, and statistics Parts 3-6 also in weeks 11-13, while Parts 7-12 come in weeks 14-16. Do not read the month table as a promise that each part fits in its week. If you fall behind, drop depth in Book 9 and the advanced Power BI parts first, not SQL or Excel (JDs: ML 10%, DAX 5%, n=186).

### 6.3 Role-based branches

Choose by target role (MS Addendum per-sample columns; plan.md Section 2):

| Branch | When to choose it | Shift the plan this way |
|---|---|---|
| **MIS / reporting first** | Strong Excel already; MIS sample showed Excel 72%, SQL 44%, Python 16% | Stay longer in Book 1 (including VBA basics, Book 1 Part 11); do SQL core; do Python lightly |
| **Data analyst / BI first** | Comfortable with learning tools; want dashboards | Follow the main table; SQL and Power BI early; Python 30-40% in Hyderabad, Bengaluru and GCC samples |
| **Product / startup analyst** | Willing to take the harder entry | More SQL depth (Book 2 Parts 5, 6, 9, 10), plus metrics cases (Book 7 Parts 4-7). This was the hardest entry point for switchers in the research (MS Section 6) |
| **HR-tech / people reporting** | Want to use your domain | Excel, Power BI or Tableau, SQL, plus Book 10 Part 1 and the HR-systems section in Book 10 Part 7 |

### 6.4 When to start applying

Guidance, not data: if you target MIS or Excel-first operations roles, start applying around the end of Month 3 once your Excel is solid and your SQL basics work. For DA/BI roles, around the end of Month 4 or 5, once you have one SQL-plus-dashboard project. Applying early is also practice: you learn what companies ask. It is a judgement call and nothing in the research tests the timing.

### 6.5 Projects, practice material and certificates

- **At least two to three portfolio projects.** No reliable data found on how many projects employers expect (B0S records no project-count finding). Treat two to three as a sensible minimum chosen for this plan, not a proven threshold; Book 12 Section 2 plans five. Details are in Q14.
- **Free resources and practice datasets:** use each book's "How to Develop" part (Book 1 Part 12, Book 2 Part 12, Book 3 Part 12, Book 4 Part 12, Book 5 Part 12, Book 7 Part 9, Book 8 Part 9, Book 9 Part 12, Book 10 Part 8). This guide does not make external claims about specific courses.
- **Certificates:** no certification (PL-300, Google Data Analytics, Tableau, CBAP) was named as a requirement in any of the 186 JDs; they appeared only as "advantages" in some postings. Value in India is unverified. Do them after SQL, Excel and portfolio, if at all (Book 12 Section 5, Q17, Q55).
- **Bootcamp vs self-study:** the research has no comparison. A training blog claims costs of Rs 50,000-1.5 lakh (vendor/blog claim, unverified). That a bootcamp can give structure and a network is general knowledge, not checked. **No reliable data found** on placement rates. Decision rule: ask any bootcamp for the number placed, the number who enrolled, the salary and employer for each, and whether placement requires paying extra; if they cannot show it, treat claims as marketing (Q12, Q56, Q57).

**Limitations of this section:** plan targets, not research. The month table follows plan.md Section 7 (checked), but the plan's week ranges are not the same as four-week months. Hours are arithmetic from a stated assumption. Month boundaries are approximate. The timing for applying and the project count are guidance, with no data behind them.

---

## Section 7. The 123 FAQs: how to use them

The 123 questions are in `Book00_FAQs.md` (answers in the same file). They are ordered by how often they come up (three-star first), not by topic, so you may find it quicker to go by group. Below is a reading map. Each question appears once.

### 7.1 Groups

| Group | Questions | When to read |
|---|---|---|
| 1. Realism and timeline | Q1, Q2, Q13, Q15, Q49, Q52, Q67, Q68, Q70, Q72, Q102 | Before you commit time or money |
| 2. Role choice | Q7, Q16, Q34, Q63, Q66, Q75, Q86, Q88, Q98, Q103, Q107, Q108, Q118 | After Section 1; to choose your first target role |
| 3. Pay | Q5, Q6, Q25, Q35, Q76, Q85, Q122 | Before you set salary expectations (see Section 2b) |
| 4. Skills order | Q3, Q4, Q11, Q20, Q44-Q48, Q51, Q87, Q89-Q92, Q109, Q111 | Before you plan your learning order (Section 6) |
| 5. Learning path (bootcamp, certificates, self-study) | Q12, Q17, Q21, Q24, Q32, Q33, Q50, Q53, Q55-Q57, Q69, Q93, Q94, Q104, Q106, Q112 | When choosing courses and resources |
| 6. Resume and HR framing | Q8, Q14, Q18, Q19, Q26, Q28, Q29, Q54, Q58, Q83, Q100, Q101 | Before you write your resume and your story |
| 7. Company types, cities and job search | Q23, Q27, Q36-Q40, Q64, Q65, Q73, Q74, Q77-Q80, Q96, Q97, Q99, Q114, Q115, Q123 | When building your target list and applying (Section 3) |
| 8. Interview process and answering technical questions | Q9, Q10, Q30, Q41-Q43, Q71, Q81, Q82, Q110 | Before your first interview (Sections 3 and 4) |
| 9. HR round and offers | Q22, Q59-Q62, Q116, Q117, Q119 | Before the HR round and when negotiating |
| 10. Special situations (age, gaps, seniority, family, first job) | Q31, Q84, Q95, Q105, Q113, Q120, Q121 | If any of these describes you |

### 7.2 How to use them

1. **Read the three-star questions first (Q1 to Q30).** They cover the most common doubts.
2. **Then read your group.** Use the table above to jump to your situation.
3. **Look at the evidence line in each answer.** Every answer says what the research shows and how reliable that is, or says "No reliable data found" and gives a decision rule. The decision rules are meant to be used with your own numbers.
4. **Use the scripts, but make them yours.** Interview-facing answers (for example Q8, Q18, Q22, Q28-Q30, Q54, Q58-Q61, Q84, Q117) include a "Say this in the interview" line. Say it in your words, and only say what is true for you.
5. **Follow the pointers** in "Where this is covered" to the relevant book part or guide section.
6. **Re-check anything time-sensitive.** The market evidence was collected in October 2026 from a limited sample (see Limitations).

---

## Limitations to state in the guide

- **Job-description evidence is a non-random pooled sample.** Skill percentages come from n=186 postings, collected from the sources that could be reached (Built In, LinkedIn public pages, Shine, TheIndiaJobs, employer career sites), with an error of about +/-7 points. Some counts used keyword matching.
- **Interview evidence is candidate-reported and anonymous.** It is thin for several companies, and no Hyderabad/Bengaluru report was found for some. Always ask the recruiter for the round structure.
- **Some major sources could not be accessed:** Naukri, Indeed, Glassdoor, foundit, AmbitionBox, Reddit, Quora and LinkedIn posts were blocked, not surfaced or needed a login, so their content is not in this guide, except that some Glassdoor review details reached the research only as search-tool summaries of the page (second-hand). LinkedIn public job pages were used for part of the JD sample.
- **Pay is posted in few JDs.** Only a small number of postings showed salary, so pay ranges are indicative. Unverified secondary snippets and blog ranges are labelled as such.
- **Certificate value is unverified.** No certification was required in any sampled JD, and nothing India-specific was found on PL-300 or Google Data Analytics.
- **Switcher outcome statistics do not exist in the research set.** No reliable data was found on outcomes by age, bootcamp placement rates, HR-to-analyst conversion rates, or the size of the HR-to-analyst pay change. Where you see "No reliable data found", the guide gives a rule for you to apply with your own numbers.
- **The learning roadmap is a study-plan design.** Hours, timelines and milestones are targets, not researched figures.
- **Dated evidence.** Research was collected on 2026-10-20 and 2026-10-21; the market changes, and nothing here is a statement about what will happen next.
