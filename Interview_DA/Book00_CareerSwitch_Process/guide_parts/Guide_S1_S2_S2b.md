# Book 0 Guide: Sections 1, 2 and 2b

How to read the evidence labels in this guide. "JD" means job description, the text of a job posting. "n=186 non-random sample, about +/-7 points" means we read 186 in-scope postings (Hyderabad/Bengaluru, stated minimum experience of 2 years or less, or tagged entry/junior) pooled from five samples of 40, 47, 42, 32 and 25 and counted which skills they name. The postings are not a random draw of the market, so treat every percentage as a rough size, not an exact figure. "Candidate-reported, anonymous" means the claim comes from interview write-ups by candidates we cannot verify. "Vendor/blog claim, unverified" means a training provider, salary blog or job-board snippet. Today is 2026-10-22; everything below describes what the research found in October 2026, not what will happen later.

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
