# Market & Skills Research 2026 (Phase 0, Subagent 0a)

Accessed: 2026-10-20. Confidence: **LOW-MEDIUM** (n = 40, not 100; sample skewed to one aggregator). Do not treat percentages as precise; at n = 40 each percentage has roughly +/- 15 points of sampling error.

## 1. Method and sample size

- **Target:** at least 100 JDs. **Achieved: 40 distinct in-scope job descriptions, read in full** (JD body text fetched per posting, then checked against a fixed skill checklist; a skill counts only if the JD text names it).
- **In-scope rule:** Data/Business/BI/MIS/Reporting/People/Operations/Product/FP&A-type analyst; Hyderabad or Bengaluru (or "remote, hiring in India" where the page says so); required experience minimum <= 2 years, or tagged Entry/Junior with no years stated. Roles needing 3+ years (about 25 more postings read) were excluded from the tally (Appendix B).
- **Where postings came from:** Built In India listing pages (builtinhyderabad.in / builtinbengaluru.in -> builtin.com job pages) = 31 of 40; jobfound.org = 2; Greenhouse (Hyreo) = 1; atypicaladvantage.in (KPMG) = 1; Cutshort page (TopGrep) = 1; plus Gartner, Unisys etc. via Built In (already counted above). See Appendix A for each row's URL.
- **Duplicates:** four near-identical Hyreo (Bengaluru) JD templates counted as **one**. Reposted listings counted once.
- **Counting rule:** "Excel" includes Excel/Advanced Excel; "Dashboards/reporting" = JD says dashboards/reports/MIS; "GenAI/AI tools" = JD names GenAI, LLM, Copilot, ChatGPT, Claude, OpenAI or "AI tools" (bare "AI" not counted). "Statistics" counted only when named as a skill/requirement, not when only in a degree list.
- **Not done:** no scraping, no login-gated sites. The tally is hand-extracted by a language model reading each page; extraction errors are possible. Dates are mostly relative ("posted 12 days ago") at the time of access.

## 2. Access limitations (exact)

| Site | Result |
|---|---|
| Naukri (naukri.com listing page) | **HTTP 403, blocked** |
| Indeed India (in.indeed.com search page) | **HTTP 403, blocked** |
| Glassdoor (listing page) | **HTTP 403, blocked** |
| foundit.in (job page) | **HTTP 403, blocked** |
| LinkedIn, AmbitionBox, Instahyre | **Not fetched.** Not retrievable via search results; login walls assumed but unverified. No data from them. |
| weekday.works job pages | Reachable, but pages hold only title/salary/location/chips, **no JD body**; used for secondary context only |
| Cutshort listing/search pages | Returned navigation only; one job page returned a list of ~31 jobs (one in-scope, TopGrep) |
| Dead/removed postings | Wipro MIS Executive, Techblocks MIS (Keka), Deloitte Power BI (filled), catalitium.com (HTTP 410), several weekday pages (410/404) |
| WebSearch | US-only search tool; returns summaries, not raw JDs. Search-engine summaries were **not** counted in the tally |

Consequence: the Naukri/Indeed/LinkedIn-heavy mass market (service-MNC and BPO-style MIS roles) is under-represented; Built In skews toward product companies, GCCs and funded startups.

## 3. Skill frequency (n = 40, in-scope JDs, full text)

Class rule: Must-have >= 50%, Common 20-50%, Good-to-have < 20%.

| Skill / tool | Count | % of 40 | Class |
|---|---|---|---|
| Communication (written/verbal) | 36 | 90.0% | **Must-have** |
| Excel (incl. advanced) | 24 | 60.0% | **Must-have** |
| SQL | 23 | 57.5% | **Must-have** |
| Dashboards / reporting / MIS | 21 | 52.5% | **Must-have** |
| Python | 14 | 35.0% | Common |
| Power BI | 13 | 32.5% | Common |
| Statistics (named) | 8 | 20.0% | Common (boundary) |
| GenAI / AI tools (Copilot, ChatGPT, Claude, LLM) | 8 | 20.0% | Common (boundary) |
| Stakeholder management | 6 | 15.0% | Good-to-have |
| Tableau | 5 | 12.5% | Good-to-have |
| Machine learning | 5 | 12.5% | Good-to-have |
| R | 4 | 10.0% | Good-to-have |
| Snowflake | 4 | 10.0% | Good-to-have |
| Alteryx | 4 | 10.0% | Good-to-have |
| Google Sheets | 4 | 10.0% | Good-to-have |
| Data cleaning (named) | 4 | 10.0% | Good-to-have |
| Any cloud (AWS/Azure/GCP; 3 distinct postings) | 3 | 7.5% | Good-to-have |
| ETL | 3 | 7.5% | Good-to-have |
| DAX | 3 | 7.5% | Good-to-have |
| VBA / macros | 2 | 5.0% | Good-to-have |
| SAP | 1 | 2.5% | Good-to-have |
| Looker | 1 | 2.5% | Good-to-have |
| A/B testing | 1 | 2.5% | Good-to-have |
| Domain knowledge (named explicitly) | 1 | 2.5% | Good-to-have |
| BigQuery, Power Query (in-scope JDs) | 0 | 0% | Not seen |

Observations (not counted, impressions only): among the ~25 postings requiring 3+ years that I read, Python, Power BI/Tableau, cloud data platforms (Snowflake, Databricks, Azure) and GenAI/ML appeared noticeably more often than in the 0-2 year set. SQL/Excel/communication stayed constant. This is consistent with Python/BI being the "mid-level separator".

Statements in plan.md Section 2 to correct: "SQL, Python, Excel, Power BI/Tableau, statistics appear in almost all DA JDs" is **not supported** for the 0-2 year band here (Python 35%, Power BI 32.5%, Tableau 12.5%, statistics 20%). "Python in a majority of postings" is also not supported at this level.

## 4. Salary bands (as stated; most JDs do not disclose)

Only 8 of 40 in-scope JDs showed any pay figure.

| Posting | Stated pay | Note |
|---|---|---|
| Hire Daily, Data Analyst, Hyderabad, 0-3 yrs | Rs 5-9 LPA | jobfound.org says "estimate" |
| OrbiTouch HR, Junior DA, Hyderabad, 0-2 yrs | Rs 4-5 LPA | up to 5 LPA, interview-dependent |
| KPMG Operations Analyst, Bengaluru, 1-2 yrs | Rs 3.5 LPA | negotiable; page says posted about a year ago |
| TopGrep Junior Power BI, Bengaluru/Hyderabad, 1-3 yrs | Rs 3.5-4.5 LPA | Cutshort, 17 Jul 2026 |
| Peakflo Data Analyst, remote India, ~1 yr | Rs 7-10 LPA (700K-1M) | Built In |
| PharmaForceIQ Data Analyst, remote India, 2-4 yrs | Rs 4.25 LPA base | Built In |
| TMI Group MIS Executive, Hyderabad, 2+ yrs | shown as "INR 160K-180K annually" | page's figure, likely about Rs 1.6-1.8 LPA; unverified |
| Weekday Revenue Analytics Analyst, remote India, 2+ yrs | Rs 15-25 LPA | outlier, remote/US-facing |

Secondary / unverified (search-result snippets, not JDs):
- foundit "Data Analyst AVP", Hyderabad, 0-3 yrs: Rs 5-12 LPA (snippet; page itself returned 403).
- ICE "Junior Data Analyst, Model Risk Management", Hyderabad: Rs 5.5-10 LPA (weekday.works/foundit card).
- EdTech Jobs "People Data Analyst", Bengaluru: Rs 6-10 LPA (snippet; experience not shown).
- Salary blogs (unverified estimates): Jobrise guides give about Rs 4-12 LPA for entry/mid Bangalore analysts and Rs 3.5-9 LPA for Hyderabad 0-2 yrs; Flexiple shows a Bengaluru platform median of Rs 7.5 LPA.

Reading: the Rs 6-10 LPA target is reachable in GCC/product/finance-analytics postings, but the in-scope pay I could verify was mostly Rs 3.5-9 LPA. Rs 6 LPA+ at 0-2 yrs is the upper half of what was observed.

## 5. Certifications

- **No named analytics certification (PL-300, Google Data Analytics, Tableau, CBAP etc.) appeared in any of the 40 in-scope JDs.** Two (Deutsche Bank Workday role, Empower) say "certifications" without naming one; JPMC FP&A lists CA/MBA/CWA (finance degrees, not analytics certs).
- Seen only in 3+ year postings: Tableau Desktop Certified Associate (Everpure BI Analyst); CBAP/CCBA/PMI-PBA/CSPO (Techdome Business Analyst, 4-6 yrs).
- PL-300 / Google DA value for Book 12 Section 5 is therefore **unverified by this sample**; treat as optional signalling, not a hiring filter.

## 6. Switcher-friendly roles (HR to analytics)

| Role type | Evidence (posting, level) | Tools asked |
|---|---|---|
| People/HR analytics | EdTech Jobs People Data Analyst, Bengaluru (Rs 6-10 LPA, snippet); Deutsche Bank Workday Prism Analytics & Reporting, Bengaluru (Entry, in-scope); Syneos HR Analytics & Visualization, Hyderabad (3+ yrs); Unisys People Analytics, Bengaluru (4-6 yrs) | Excel, Power BI/Tableau, SQL, Workday/Visier/SuccessFactors |
| HR-adjacent / change mgmt | Unisys Associate Analyst OCM, remote India, 0-2 yrs | Excel, Power BI, Copilot/ChatGPT |
| MIS / reporting | TMI MIS Executive (Hyd), Tata Play Fiber SME MIS (Blr, Entry), EXL MIS Reporting BA (Blr), Quess Asst Manager MIS | Excel (often advanced), VBA, BI tool basics |
| Operations analyst | KPMG Operations Analyst (Blr, 1-2 yrs), HPE Procurement Ops Analyst I (Blr, 0-2) | Excel, SQL (nice to have), dashboards |
| Product analyst (non-tech product) | Netcom Learning (Hyd, 1-3 yrs) | Excel, Power BI, AI tools |
| Business/pricing/research analyst | Easyship, TriNet, Gartner, Cushman & Wakefield | Excel, SQL, Tableau/Power BI |

Most switcher-accessible by tool bar: MIS, operations analyst, HR-tech reporting (Workday), research/pricing analyst: all Excel-first with SQL optional. Python-heavy product/startup analyst roles are the hardest entry point.

## 7. Secondary sources (NOT counted; published analyses, methods undisclosed)

- ownyourcareer.in/careers/data-analyst: SQL 98%, Power BI/Tableau 88%, Python 80%, statistics/A-B 74%, AI literacy 66%. No sample size or method; **my 40-JD sample does not reproduce these** (SQL 57.5%, Python 35%). Treat as unverified marketing-style figures.
- SLA Consultants training page (via etchrock.com): Excel in "over 40%" of postings, Power BI 24.7%, Tableau 28.1%, SQL "in most". Training provider, dataset unnamed.
- Jobrise 2026 city guides and Flexiple: qualitative and salary estimates only.

## 8. Implications for the books

(a) **Must-have skills vs plan.md Section 3 coverage:** every must-have is covered: Excel (Book 1), SQL (Book 2), dashboards/reporting (Books 1, 4, 8 Part 3), communication (Book 11). **No must-have skill is missing.** Notes:
- Excel is the single most frequent tool (60%) and is as important as SQL for 0-2 year roles; keep Book 1 at full 600 and do not push it behind Power BI/Python. Add Google Sheets (10%) mentions inside Book 1.
- Communication at 90% supports giving Book 11 Part 4 (explaining data) priority and a 30-day plan.
- Power BI and Python are Common (about one-third), not near-universal; keep the books but update plan.md Section 2 wording.
- Consider a short optional add-on (about 10-15 Qs, not a book): Alteryx (10%, finance/GCC), HR systems (Workday/Visier) for the people-analytics path, "Workday reporting" basics in Book 10 Part 1.

(b) **Planned parts for rare skills that could shrink (confirm with a larger sample before cutting hard):**

| Planned part | JD evidence (n=40) | Suggested change |
|---|---|---|
| Book 4 Part 10, Tableau basics & Power BI vs Tableau (50 Qs) | Tableau 12.5% | cut to about 25 |
| Book 1 Part 11, VBA & Copilot (20 Qs) | VBA 5%, GenAI 20% | keep Copilot, limit VBA to about 8 |
| Book 9 Part 11, Cloud basics (30 Qs) | Any cloud 7.5%, Snowflake 10% | cut to about 15 |
| Book 9 Part 10, LLM/RAG (40 Qs) | RAG appeared only in tags of one Hartford role; GenAI/AI tools 20% | cut to about 20; keep Part 9 (GenAI for analysts, 60) |
| Book 9 Parts 3, 6, 7, 8 (trees, overfitting, forecasting, churn projects: about 190 Qs) | ML named in 12.5% | reduce about 25-30% in total |
| Book 5 Part 8, A/B testing (50 Qs) | A/B testing 2.5% in JDs | cut to about 30, but interview-process research (Subagent 0b) may justify keeping |
| Book 4 Parts 4-5, DAX (130 Qs) | DAX 7.5%, Power BI 32.5% | keep DAX basics; trim advanced DAX (Part 5) to about 40 |
| Book 3 Part 3, NumPy (40 Qs) | not named in JDs (only OrbiTouch names NumPy/pandas) | cut to about 25 |

Not rare, do not shrink: SQL, Excel, dashboards, communication, and Python basics.

Caveat for all decisions: n = 40, Built In-heavy, JD text rather than interview content. Several shrink candidates (statistics, A/B testing, scenarios) may still be heavily asked in interviews, so reconcile with research/interview_processes.md.

## Appendix A. Sampling table (the 40 in-scope JDs)

Date column is as shown at access (2026-10-20); "rel." = relative. Skills = terms named in the JD.

| # | Company | Title | City | Exp | Date | Source URL | Skills named |
|---|---|---|---|---|---|---|---|
| 1 | Hire Daily | Data Analyst | Hyderabad | 0-3 | 14 Oct 2026 | https://jobfound.org/job/hire-daily-is-hiring-for-data-analyst-hyderabad-telangana-india-india-14-october-2026 | SQL, Python, Power BI, dashboards, communication |
| 2 | OrbiTouch HR | Junior Data Analyst | Hyderabad | 0-2 | 14 Oct 2026 | https://jobfound.org/job/orbitouch-hr-orbitouch-outsourcing-pvt-ltd-is-hiring-for-data-analyst-hyderabad-telangana-india-india-14-october-2026 | SQL, Excel, Python, R, Power BI, Tableau, statistics, Google Sheets, dashboards, cleaning, communication |
| 3 | Cityscope | Business Analyst | Hyd/Blr listing | 2+ (Junior) | rel. 8 days | https://builtin.com/job/business-analyst/11189792 | SQL, Excel, communication |
| 4 | Hyreo (4 reposts as 1) | Analyst (contract) | Bengaluru | 2+ | n/a | https://job-boards.greenhouse.io/hyreo/jobs/5339545004 | SQL, Excel, Power BI, Python, R, Tableau, statistics, Google Sheets, dashboards |
| 5 | KPMG | Operations Analyst | Bengaluru | 1-2 | rel. 1 yr | https://atypicaladvantage.in/find-a-job/operations-analyst-kpmg-bangalore-894 | Excel, dashboards, communication |
| 6 | Peakflo | Data Analyst | Remote India | ~1 | rel. 3 days | https://builtin.com/job/data-analyst-remote-india/9920702 | SQL, Python, GCP, dashboards, communication, AI tools |
| 7 | Perceptive Analytics | Data Analyst - Adv. Analytics | Hyderabad | 0-3 | rel. 2 mo | https://builtin.com/job/data-analyst-advanced-analytics/9918747 | SQL, Excel, VBA, Python, R, statistics, communication |
| 8 | QED.ai | Forward-Deployed Data Analyst | Remote | Entry | rel. 2 mo | https://builtin.com/job/forward-deployed-data-analyst/7771078 | SQL, dashboards, communication |
| 9 | Drivetrain | Business Analyst | Remote India | Entry | rel. 2 mo | https://builtin.com/job/business-analyst-customer-platform/6194771 | SQL, dashboards, communication |
| 10 | PharmaForceIQ | Data Analyst | Remote India | 2-4 | rel. 2 mo | https://builtin.com/job/data-analyst/10400120 | SQL, Excel, Python, Power BI, statistics, domain, dashboards, cleaning, communication |
| 11 | Portcast | Data Analyst | Hyd/Blr listing | 2-3+ | rel. 2 mo | https://builtin.com/job/data-analyst/10584051 | SQL, Python, dashboards, communication, AI tools, ML |
| 12 | Easyship | Pricing Analyst | Bengaluru | 2+ | rel. 1 day | https://builtin.com/job/pricing-analyst/11745584 | SQL, Excel, Google Sheets, statistics, Looker, Tableau, communication, stakeholders |
| 13 | Cushman & Wakefield | Analyst | Hyderabad | Entry | rel. 1 day | https://builtin.com/job/analyst/11743662 | Excel, communication, stakeholders |
| 14 | The Hartford | Business Data Analyst | Hyderabad | Entry | rel. 11 days | https://builtin.com/job/ind-business-data-analyst/11588847 | SQL, GenAI, communication |
| 15 | Weekday (Inc.) | Revenue Analytics Analyst | Remote India | 2+ | rel. 1 day | https://builtin.com/job/revenue-analytics-analyst/11748729 | SQL |
| 16 | Applied Materials | BI Analyst | Bengaluru | Entry | rel. 13 days | https://builtin.com/job/business-intelligence-analyst/11413189 | Excel, SAP, communication |
| 17 | Cummins | BI Analyst | India/remote | Entry | rel. 12 days | https://builtin.com/job/business-intelligence-analyst/11566812 | SQL, Python, Power BI, DAX, Snowflake, statistics, ML, OpenAI, dashboards, communication, stakeholders |
| 18 | Takeda | Analyst, Data Reporting Ops | Bengaluru | 1-3 | rel. 19 days | https://builtin.com/job/tech-operations-and-support-analyst-usbu-obu-data-reporting-ops/11457591 | SQL, Power BI, DAX, dashboards, communication, stakeholders |
| 19 | JPMorganChase | CB Risk Reporting Analyst | Bengaluru | 2-5 | rel. 22 days | https://builtin.com/job/cb-risk-reporting-analyst/10815527 | SQL, Alteryx, Python, AWS, Azure, communication |
| 20 | Deutsche Bank | Workday Prism Analytics & Reporting Consultant (HR IT) | Bengaluru | Entry | rel. 8 days | https://builtin.com/job/workday-prism-analytics-and-reporting-consultant-hr-it-associate/11541587 | ETL, dashboards, communication, AI tools, "certifications" |
| 21 | Tata Play Fiber | SME MIS & Reporting | Bengaluru | Entry | rel. 12 days | https://builtin.com/job/sme-mis-reporting/11566940 | Excel, VBA, dashboards, cleaning, communication |
| 22 | EXL | Associate BA, MIS Reporting | Bengaluru | 2-5 | rel. 2 mo | https://builtin.com/job/associate-business-analyst-reporting-mis-reporting/9923683 | Excel, dashboards, communication |
| 23 | Climate Collective Foundation | Impact Analyst | Remote India | 2-5 | rel. 1 mo | https://builtin.com/job/impact-analyst/10820820 | Excel, communication |
| 24 | ZAGENO | Business Analyst | Bengaluru | 2-5 | rel. 2 mo | https://builtin.com/job/business-analyst/10130306 | SQL, Python, R, statistics, ML, communication |
| 25 | Gartner | Specialist Analyst | Remote India | 0-2 | rel. 2 days | https://builtin.com/job/specialist-analyst-technology-market-market-sizing-revenue-analysis/10513392 | Excel, Power BI, statistics, communication |
| 26 | TopGrep Tech | Junior Power BI Developer/Analyst | Blr/Hyd | 1-3 | 17 Jul 2026 | https://cutshort.io/job/BI-Specialist-Hyderabad-Loyalty-Juggernaut-Inc-21iCwlhL (listing page) | SQL, Power BI, DAX, ETL, Python, Snowflake, Azure, AWS, communication |
| 27 | Netcom Learning | Product Analyst | Hyderabad | 1-3 | rel. 26 days | https://builtin.com/job/product-analyst/11347061 | Excel, Power BI, AI tools, communication |
| 28 | Precision Medicine Group | Product Analyst | Remote India | 1-3 | rel. 22 days | https://builtin.com/job/product-analyst/11395387 | SQL, Excel, Power BI, Python, Snowflake, ML, dashboards, communication, stakeholders |
| 29 | Rocket Learning | Product Analyst | Remote India | 2-4 | rel. 1 mo | https://builtin.com/job/product-analyst/10817316 | SQL, Tableau, Alteryx, Python, A/B testing, ETL, dashboards, communication |
| 30 | TMI Group | MIS Executive | Hyderabad | 2+ | rel. 4 days | https://builtin.com/job/mis-executive/7704029 | Excel, cleaning, communication |
| 31 | Empower | Compliance Operations Analyst | Bengaluru | 2-4 | rel. 3 days | https://builtin.com/job/compliance-operations-analyst/11630833 | Excel, Power BI, dashboards, communication, "certifications" |
| 32 | HPE | Procurement Ops Analyst I | Bengaluru | 0-2 | rel. 19 days | https://builtin.com/job/procurement-ops-analyst-i/11456726 | SQL (nice to have), communication |
| 33 | H1 | Revenue Operations Analyst | Remote India | 2-4 | rel. 11 days | https://builtin.com/job/revenue-operations-analyst/11605287 | Excel, Google Sheets, dashboards, communication, AI assistants |
| 34 | Quess Corp | Asst Manager - MIS | India | Entry | rel. 13 days | https://builtin.com/job/assistant-manager-mis/11559638 | dashboards |
| 35 | TriNet | Associate Pricing Analyst | Hyderabad | <2 | rel. 1 day | https://builtin.com/job/associate-pricing-analyst/11741885 | SQL, Excel, Tableau, communication |
| 36 | The Hackett Group | Associate Analyst - GBS | Hyderabad | Entry | rel. 2 mo | https://builtin.com/job/associate-analyst-gbs/8822584 | Excel, communication |
| 37 | Bottomline Technologies | Corp FP&A Financial Analyst | Bengaluru | 1-3 | rel. 20 days | https://builtin.com/job/corp-fp-financial-analyst/11434037 | Excel, Snowflake, Alteryx, Power BI, communication, stakeholders |
| 38 | JPMorganChase | Analyst - FP&A | Bengaluru | 1-3 | rel. 1 mo | https://builtin.com/job/analyst-financial-planning-analysis/10925519 | Excel, SQL, Python, Alteryx, ML, dashboards, communication |
| 39 | Magnit | Analyst, Financial Operations | Bengaluru | 2 | rel. 7 days | https://builtin.com/job/analyst-financial-operations/11655025 | Excel |
| 40 | Unisys | Associate Analyst OCM | Remote (Karnataka) | 0-2 | rel. 14 days | https://builtin.com/job/associate-analyst-ocm/11522487 | Excel, Power BI, dashboards, communication, Copilot/ChatGPT/GenAI |

## Appendix B. Read but excluded (experience minimum 3+ years, wrong geography, or no JD body); not in tally

Pointo DA (4+), Garden City Games DA (3+), Weekday BA Non-US Raters (3+), Anblicks DA and Audience Analytics (4+), Synchrony Data Quality (4+), Everpure BI (4+; Tableau Desktop Certified Associate), Danaher x2 (3+), ABB T&E (3+), Wati Product Analyst (3+), Squircle SCM DA (3-5), Techdome BA (4-6; CBAP/CCBA/PMI-PBA/CSPO), Unisys People Analytics (4-6), Syneos HR Analytics (3+), Flatworld Jr BA (3-5), HPE Finance Ops (4+), Blue Machines AI Analyst (3-4), Rwazi Product Analyst (3-6+), Zoom Marketing DA (3+), First Advantage Marketing DA (3+), Prudential BI Analyst and StartupBlink and Arcana and Intersoft (experience not stated, "mid"), CNX (location is Philippines), Diageo and American Express (US-based postings). Page-only, no JD body: ICE Junior DA Model Risk (Rs 5.5-10 LPA), S&P Global, Innova ESI (weekday/foundit pages).

## Appendix C. Other URLs consulted

- https://builtinhyderabad.in/jobs/data-analytics/search/data-analyst and /business-analyst, /analyst, /power-bi, /product-analyst, /mis, /hr-analytics, /associate-analyst, /business-intelligence
- https://builtinbengaluru.in/jobs/data-analytics/search/data-analyst, /business-analyst, /analyst, /bi-analyst, /reporting; /jobs/search/people-analytics, /operations-analyst, /junior-analyst, /associate-analyst, /insights-analyst, /marketing-analyst, /financial-analyst
- https://www.weekday.works/jobs/data-analyst-jobs-in-hyderabad-3, /data-analyst-jobs-in-bangalore, /data-analyst-jobs-4 (card chips only)
- https://internshala.com/jobs/data-analyst-jobs/ (reachable; mostly non-analyst or non-metro roles, not used)
- Secondary: https://www.ownyourcareer.in/careers/data-analyst ; https://jobrise.io/en/blog/data-analyst-jobs-hyderabad-guide-2026/ ; https://jobrise.io/en/blog/data-analyst-jobs-bangalore-2026/ ; https://flexiple.com/hire/data-analyst/bengaluru ; https://etchrock.com (SLA Consultants page)

---

## Addendum (2026-10-21): Pooled sample, n = 186

Pooled from this file's 40 JDs plus four extra samples: `jd_sample_hyderabad.md` (47), `jd_sample_bengaluru.md` (42), `jd_sample_mis_people.md` (32, includes 5 near-identical Honhr rows), `jd_sample_gcc_mnc.md` (25, Amazon = 12 of 25). Counts are the sub-agents' own tallies, summed; several used keyword matching (±2). Sample is NOT random: skewed to the sources that were reachable (Built In, LinkedIn public pages, Shine, TheIndiaJobs, employer career sites). Naukri/Indeed/Glassdoor/foundit were blocked. Treat % as ±7 pts.

| Skill | Count /186 | % | Class | Per-sample % (orig, Hyd, Blr, MIS, GCC) |
|---|---|---|---|---|
| Dashboards/reporting/MIS | 140 | 75% | Must | 52, 85, 81, 72, 88 |
| Communication | 135 | 73% | Must | 90, 79, 71, 44, 72 |
| Excel | 112 | 60% | Must | 60, 55, 48, 72, 76 |
| SQL | 101 | 54% | Must | 58, 51, 50, 44, 76 |
| Stakeholder mgmt | 82 | 44% | Common | 15, 64, 60, 19, 60 |
| Power BI | 75 | 40% | Common | 32, 49, 45, 38, 32 |
| Tableau | 61 | 33% | Common | 12, 40, 38, 28, 48 |
| Python | 60 | 32% | Common | 35, 30, 40, 16, 40 |
| Statistics | 43 | 23% | Common | 20, 34, 31, 6, 16 |
| ETL | 34 | 18% | Good (upper bound; Amazon wording inflates) | 8, 26, 7, 6, 56 |
| GenAI/AI tools | 26 | 14% | Good | 20, 15, 12, 9, 12 |
| VBA/macros | 24 | 13% | Good | 5, 9, 5, 19, 40 |
| ML | 19 | 10% | Good | 12, 6, 12, 3, 20 |
| Cloud | 18 | 10% | Good | 8, 6, 7, 9, 24 |
| R | 16 | 9% | Good | 10, 13, 10, 6, 0 |
| Google Sheets | 14 | 8% | Good | 10, 4, 7, 16, 0 |
| DAX | 10 | 5% | Good | 8, 9, 2, 6, 0 |
| A/B testing | 8 | 4% | Good | 2, 0, 12, 0, 8 |
| Snowflake | 7 | 4% | Good | 10, 4, 0, 0, 4 |
| Alteryx | 6 | 3% | Good | 10, 2, 0, 0, 4 |

Other findings: no analytics certification required in any sample (named only as advantages: Tableau/Power BI cert, Google DA, MS Data Analyst Associate, CBAP). Pay shown in few rows; entry MIS/BA mostly ₹3–6 LPA, Amazon/GCC/product higher but unstated. No pure people-analytics role at 0–2 yrs found (all Workday-reporting roles asked 3+ yrs). Caveats: Hyd/Blr experience labels sometimes wide ("0–4 yrs"); a few operational roles are weak fits.
