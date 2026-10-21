# Bengaluru JD Sample (extra sampling), 2026-10-21

Accessed 2026-10-20/21. **Achieved sample: 42 distinct JDs** (target was 30+). Confidence: LOW-MEDIUM; at n=42 each percentage carries roughly +/- 15 points of sampling error. These are NEW postings; none of the 40 in `market_skills_2026.md` Appendix A are repeated.

## 1. Method

- **Scope:** Bengaluru/Bangalore Data Analyst, Business Analyst, BI, MIS/reporting, product analyst, operations analyst roles with minimum experience <= 2 years (or fresher/junior/intern). Roles whose posted range starts at 2 ("2+", "2 to 3") are included, consistent with the first sample. Finance/accounting/tax/audit/IT-support analyst roles were excluded by title.
- **Gathering:** Job pages were fetched in full (HTTP GET, tags stripped) and a fixed regex checklist (same skill list as the first file) was applied to the JD body, then spot-checked in context for ambiguous hits (R, SAP, certification, ML, domain, cloud). A skill counts only if the JD body (or the posting title, e.g. "Power BI Analyst") names it. Sidebar "skills for this role" tags on aggregator pages were NOT counted. "Dashboards / reporting / MIS" = JD says dashboards, reporting, reports or MIS.
- **Sources used (no Built In):** TheIndiaJobs (17 rows, Bengaluru listing pages), Shine (14 rows), Wellfound (5 rows), Greenhouse public job-board API (Razorpay, 2 rows), Lever public API (Paytm, 1 row), Saarthi (Indium, 1), atypicaladvantage.in (KPMG, 1), Semesteria (Swiggy listing, 1).
- **Experience column:** where an aggregator shows only its own range label (TheIndiaJobs "Fresher", Shine "0 to 4 Yrs"), that label is quoted as "site label". These labels are often defaults or wide ranges and can disagree with JD text; where the JD body states years, it is shown as "JD text". Treat TheIndiaJobs "Fresher" rows as "entry/junior, years not stated or unreliable".
- **Freshness:** TheIndiaJobs shows "4+ weeks ago" on every page (true age unknown). Shine rows were 1 hour to about 1 month old at access. Swiggy (Semesteria) said 8 months old and KPMG said about 1 year old; both kept because the JD text was readable and no closed notice was shown, but may be stale.
- **Dedup:** Velocity has two Wellfound postings (4215166, 4629922) with near-identical JDs, counted once. DSHINE PRO SOLUTIONS has three Shine postings with the same template, counted once. Two Udaan "MIS Executive" pages exist; only the one with a real JD (0-2 yrs business finance) is counted.
- **Limits:** extraction is regex-assisted and by a language model; errors are possible. Pay was shown in few postings.

## 2. Sites blocked or unusable

| Site | Result |
|---|---|
| Naukri (listing page) | HTTP 200 but only a ~35 KB JS shell with no job rows; no JDs obtained |
| Indeed India, Glassdoor India, Instahyre, Adzuna India, Jooble India, foundit.in | HTTP 403 |
| Shine (via the WebFetch tool) | tool refused the domain; plain HTTP fetch worked and was used |
| TimesJobs | tool refused the domain; plain HTTP page returned only a ~14 KB shell, not used |
| LinkedIn job pages (links from devjobsscanner) | all tested pages (GreedyGame, Mopid, Maersk, Amazon, Mindsnack) redirected to an "expired JD" page; no JD text |
| Cutshort listing, hirist.tech, iimjobs listing | navigation only / no job links; no JDs obtained |
| Internshala (Bengaluru data-analyst search) | reachable but returned zero analyst roles |
| weekday.works job pages | HTTP 410 for all tested (Skill Secure, SAZ, Litspark, Ticknetwork, Incanus) |
| apna.co, freshersworld | 404 / redirect, not used |
| Dead or filled postings seen and skipped | Deloitte Power BI Consultant (filled), Flexingit energy-client BA (closed), Qureos MIS Analyst (expired), Even Healthcare Product Analyst (closed), Apna Mart BA (closed), Apna Product Analyst (closed, 3+ yrs), eClerx foundit page (403), Tekkitake and Marutee monster.co.th mirrors ("no longer accepting") |
| Workday / SmartRecruiters tenant guesses | no usable Bengaluru entry-level analyst postings (Bosch, Experian, Freshworks, Sutherland lists were senior, other-city or non-analyst) |

## 3. Sample table

| id | company | title | city | source URL | exp required | pay if shown | skills named | source / note |
|---|---|---|---|---|---|---|---|---|
| B1 | Indium Software | Data Analyst | Bengaluru | https://joinsaarthi.com/jobs/indium-software/data-analyst-bengaluru/fe11447a-cd6a-4763-9d4f-5c8ffacdb79d | 0-3 yrs | not shown | Power BI, Python, SQL, Tableau, communication, dashboards/reporting, stakeholder | Saarthi (page shows no posting date) |
| B2 | Newton School | Data Analyst | Bengaluru | https://wellfound.com/jobs/4751311-data-analyst | Fresher / 0-1 yr | Rs 4-8 LPA | ETL, Excel, Google Sheets, Looker, Power BI, Python, SQL, Tableau, cloud, communication, dashboards/reporting, stakeholder, statistics | Wellfound |
| B3 | Velocity | Data Analyst | Bengaluru | https://wellfound.com/jobs/4215166-data-analyst | 2+ yrs | Rs 20-30 LPA + equity (a sister posting 4629922 shows Rs 18-25 LPA; counted once) | Excel, Metabase, Power BI, Python, R, SQL, Tableau, communication, dashboards/reporting, stakeholder, statistics | Wellfound |
| B4 | Codemonk | Associate Business Analyst | Bengaluru | https://wellfound.com/jobs/4791901-associate-business-analyst | 1-2 yrs | Rs 4-6 LPA | Excel, GenAI/AI tools, Jira, communication, stakeholder | Wellfound |
| B5 | Finifi | Product Analyst Intern | Bengaluru | https://wellfound.com/jobs/4824038-product-analyst-intern | none (intern/entry) | Rs 20,000/month stipend (3 months, PPO possible) | Excel | Wellfound |
| B6 | Bureau | Product Analyst Intern | Bengaluru | https://wellfound.com/jobs/4823693-product-analyst-intern | none stated (final-year/recent grad) | not shown | SQL, dashboards/reporting | Wellfound |
| B7 | KPMG | Operation Analyst | Bangalore | https://atypicaladvantage.in/find-a-job/operation-analyst-kpmg-bangalore-880 | Fresher (BCom only), 6-month contract | Rs 3.65 LPA | Excel, communication, dashboards/reporting, stakeholder | atypicaladvantage.in (posted ~1 yr ago per page) |
| B8 | Swiggy (via aggregator) | Business Analyst | Bengaluru | https://app.semesteria.com/jobs/business-analyst-bengaluru-swiggy-1f1cc66d-4169-46c8-8dca-1d6f1a9ef35b | 1-2 yrs | 'INR 60K' (aggregator figure, period unstated) | Excel, Power BI, Python, SQL, communication, dashboards/reporting, stakeholder | Semesteria aggregator (posted 8 months ago per page; may be stale) |
| B9 | Razorpay | Data Analyst, Business Finance | Bengaluru | https://job-boards.greenhouse.io/razorpaysoftwareprivatelimited/jobs/4744129005 | 0-2 yrs | not shown | GenAI/AI tools, Power BI, Python, SQL, Tableau, dashboards/reporting | Greenhouse (Razorpay board) |
| B10 | Razorpay | Junior Analyst, Risk Management | Bengaluru | https://job-boards.greenhouse.io/razorpaysoftwareprivatelimited/jobs/4740722005 | 'Junior' (no years in JD text I extracted) | not shown | communication, dashboards/reporting, stakeholder | Greenhouse (Razorpay board) |
| B11 | Paytm | Risk Analyst | Bangalore, Karnataka | https://jobs.lever.co/paytm/beb24813-6250-46c4-b8af-63aae1f2bbe6 | 1-3 yrs (title: Exp - 1 to 3 Yrs) | not shown | ML, Python, SQL, communication, stakeholder | Lever (Paytm board) |
| B12 | Belhem India Pvt. Ltd | Mis, Data Analyst - Non It | Bengaluru | https://jobs.theindiajobs.com/c/Belhem-India-Pvt-Ltd/jobs/mis-data-analyst-non-it-rgr8brskt9 | site label 'Fresher' | not disclosed | Excel, MIS, dashboards/reporting, stakeholder | TheIndiaJobs (all pages show '4+ weeks ago') |
| B13 | Blackrock | Data Management Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Blackrock/jobs/data-management-analyst-8mhhz9kyeu | site label 'Minimum 1 Year' | not disclosed | Excel, dashboards/reporting, domain, stakeholder, statistics | TheIndiaJobs (all pages show '4+ weeks ago') |
| B14 | Camsdata Technologies India Pvt. Ltd. | Data Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Camsdata-Technologies-India-Pvt-Ltd/jobs/data-analyst-98vgp7tyw8 | site label 'Minimum 2 Years' | not disclosed | BigQuery, ETL, Excel, Looker Studio, MIS, Metabase, Python, SQL, Tableau, cloud, communication, dashboards/reporting | TheIndiaJobs (all pages show '4+ weeks ago') |
| B15 | Falconx | Revenue Operations Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Falconx/jobs/Revenue-Operations-Analyst-qtn80swjBu | site label '1 to 3 Year' | not disclosed | Excel, Google Sheets, communication, dashboards/reporting, stakeholder | TheIndiaJobs (all pages show '4+ weeks ago') |
| B16 | Flipkart | Associate Business Analyst - Analytics | Bengaluru | https://jobs.theindiajobs.com/c/Flipkart/jobs/associate-business-analyst-analytics-bnghgfgrbf | site label '2 to 3 Years' | not disclosed | Excel, ML, Power BI, Python, R, SQL, Spark, Tableau, communication, stakeholder, statistics | TheIndiaJobs (all pages show '4+ weeks ago') |
| B17 | Innovatia | Reporting And Analytics Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Innovatia/jobs/reporting-and-analytics-analyst-3fn8t3pj0h | site label 'Fresher' | not disclosed | communication, dashboards/reporting, stakeholder | TheIndiaJobs (all pages show '4+ weeks ago') |
| B18 | Jindal Aluminium | Business Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Jindal-Aluminium/jobs/business-analyst-k0vx6cyekk | site label 'Fresher' | not disclosed | communication, dashboards/reporting | TheIndiaJobs (all pages show '4+ weeks ago') |
| B19 | Licious | Product Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Licious/jobs/product-analyst-qrs3nb4m0m | site label '1 to 3 Year' | not disclosed | A/B testing, Metabase, Power BI, Python, SQL, Tableau, communication, dashboards/reporting, stakeholder | TheIndiaJobs (all pages show '4+ weeks ago') |
| B20 | Limechat | Product Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Limechat/jobs/product-analyst-awgqnhp08b | site label 'Fresher' | not disclosed | A/B testing, GenAI/AI tools, Looker, ML, Metabase, Power BI, Python, R, SQL, dashboards/reporting | TheIndiaJobs (all pages show '4+ weeks ago') |
| B21 | Qualcomm India Private Limited | Business Operations Analyst, Associate | Bengaluru | https://jobs.theindiajobs.com/c/Qualcomm-India-Private-Limited/jobs/business-operations-analyst-associate-hxqek6uz8y | site label '2 to 4 Years' | not disclosed | Excel, Jira, Power BI, SAP, Tableau, communication, dashboards/reporting | TheIndiaJobs (all pages show '4+ weeks ago') |
| B22 | Tya Business Solutions Pvt. Ltd. | Mis Executive | Bengaluru | https://jobs.theindiajobs.com/c/Tya-Business-Solutions-Pvt-Ltd/jobs/mis-executive-bj0yyt4xtv | site label 'Fresher' | not disclosed | Excel, MIS, communication, dashboards/reporting | TheIndiaJobs (all pages show '4+ weeks ago') |
| B23 | Udaan | Mis Executive | Bengaluru | https://jobs.theindiajobs.com/c/Udaan/jobs/mis-executive-wcuyne6y5h | site label 'Fresher' | not disclosed | Excel, MIS, SQL, dashboards/reporting | TheIndiaJobs (all pages show '4+ weeks ago') |
| B24 | Mckinsey & Company | Data Science Analyst, Capabilities & Insights Analytics - Periscope | Bengaluru | https://jobs.theindiajobs.com/c/Mckinsey-Company/jobs/data-science-analyst-capabilities-insights-analytics-periscope-mfrsuyzpbh | site label 'Minimum 2 Years' | not disclosed | Excel, Python, R, SQL, VBA, data cleaning, statistics | TheIndiaJobs (all pages show '4+ weeks ago') |
| B25 | Reuters News Agency | Operations Analyst | Bengaluru | https://jobs.theindiajobs.com/c/Reuters-News-Agency/jobs/operations-analyst-rujvshh4q2 | site label '1 to 3 Year' | not disclosed | communication, dashboards/reporting, stakeholder | TheIndiaJobs (all pages show '4+ weeks ago') |
| B26 | Thermo Fisher Scientific | Data Analyst I | Bengaluru | https://jobs.theindiajobs.com/c/Thermo-Fisher-Scientific/jobs/data-analyst-i-yvuughc3af | site label 'Fresher' | not disclosed | Python, communication, dashboards/reporting | TheIndiaJobs (all pages show '4+ weeks ago') |
| B27 | Affine Analytics Pvt Ltd | Data Analyst - Power Bi (sen01033) | Bengaluru | https://jobs.theindiajobs.com/c/Affine-Analytics-Pvt-Ltd/jobs/data-analyst-power-bi-sen01033-tncr6h1xpy | site label '2 to 5 Years' | not disclosed | ML, Power BI, domain, statistics | TheIndiaJobs (all pages show '4+ weeks ago') |
| B28 | Kwalee | Business Intelligence (bi) Analyst - Looker | Bengaluru | https://jobs.theindiajobs.com/c/Kwalee/jobs/business-intelligence-bi-analyst-looker-6va4brptve | site label 'Fresher' | not disclosed | Looker, Power BI, Python, SQL, Tableau, communication, dashboards/reporting, stakeholder | TheIndiaJobs (all pages show '4+ weeks ago') |
| B29 | Fresenius Medical Care | Analyst Data Analytics | Bangalore | https://www.shine.com/jobs/analyst-data-analytics/fresenius-medical-care/19497900 | Shine label 0 to 4 Yrs | not disclosed | dashboards/reporting, statistics | Shine (posted 1 month ago) |
| B30 | Recognized | Business Analyst - Healthcare - Hiring Immediately (Bengaluru) | Bangalore | https://www.shine.com/jobs/business-analyst-healthcare-hiring-immediately-bengaluru/recognized/19502568 | Shine label 0 to 4 Yrs; JD text: 0-2 years | not disclosed | communication, dashboards/reporting | Shine (posted 1 month ago) |
| B31 | Quess IT Solutions | Business Analyst Retail Analytics F2F interview on 14 oct | Bangalore | https://www.shine.com/jobs/business-analyst-retail-analytics-f2f-interview-on-oct/quess-it-solutions/19863011 | Shine label 0 to 4 Yrs | not disclosed | A/B testing, Power BI, Python, SQL, Tableau, cloud, stakeholder, statistics | Shine (posted 6 hours ago) |
| B32 | PHONEPE LIMITED | Business Operations Analyst, Payments Business | Bangalore | https://www.shine.com/jobs/business-operations-analyst-payments-business/phonepe-limited/19565100 | Shine label 1 to 5 Yrs; JD text: 1-2 years | not disclosed | Excel, SQL, communication, dashboards/reporting, stakeholder | Shine (posted 4 weeks ago) |
| B33 | Cisco | Customer Intelligence and Adoption Analyst, Product Adoption Analyst | Bangalore | https://www.shine.com/jobs/customer-intelligence-and-adoption-analyst-product-adoption-analyst/cisco/19576976 | Shine label 1 to 5 Yrs; JD text: 1-4 years | not disclosed | A/B testing, Excel, GenAI/AI tools, Looker, Mixpanel/Amplitude, Power BI, Python, SQL, Tableau, communication, dashboards/reporting, stakeholder, statistics | Shine (posted 3 weeks ago) |
| B34 | AgenticOrbitX | Data Analyst, Python, SQL, DAV & Analytics Tools Development | Bangalore | https://www.shine.com/jobs/data-analyst-python-sql-dav-analytics-tools-development/agenticorbitx/19580502 | Shine label 0 to 4 Yrs | not disclosed | ETL, Looker, Power BI, Python, SQL, Tableau, communication, dashboards/reporting, stakeholder, statistics | Shine (posted 3 weeks ago) |
| B35 | DSHINE PRO SOLUTIONS | Data Analyst | Bangalore | https://www.shine.com/jobs/data-analyst/dshine-pro-solutions/19783296 | Shine label 0 to 1 Yr | 3.0 - 5 Lakh/Yr | MIS, communication, dashboards/reporting, stakeholder | Shine (posted 1 week ago) |
| B36 | Important Group | Ecommerce operations executive ( MIS ) (Bengaluru) | Bangalore | https://www.shine.com/jobs/ecommerce-operations-executive-mis-bengaluru/important-group/19862181 | Shine label 1 to 5 Yrs; JD text: 1 - 2 years | not disclosed | MIS, communication, dashboards/reporting | Shine (posted 20 hours ago) |
| B37 | Techynt Solutions LLP | Junior Data Analyst | Bangalore | https://www.shine.com/jobs/junior-data-analyst/techynt-solutions-llp/19686128 | Shine label 1 to 5 Yrs | not disclosed | Excel, ML, Power BI, Python, SQL, Tableau, communication, dashboards/reporting, data cleaning, stakeholder, statistics | Shine (posted 2 weeks ago) |
| B38 | StatusNeo | Junior Power BI Analyst (Bengaluru) | Bangalore | https://www.shine.com/jobs/junior-power-bi-analyst-bengaluru/statusneo/19593940 | Shine label 0 to 4 Yrs; JD text: 0-1 Year | not disclosed | DAX, Excel, Looker, Looker Studio, Power BI, Power Query, SQL, Tableau, communication, dashboards/reporting, statistics | Shine (posted 3 weeks ago) |
| B39 | Jobaaj - Hiring for Our Leading Clients | Junior Product Analyst | Bangalore | https://www.shine.com/jobs/junior-product-analyst/jobaaj-hiring-for-our-leading-clients/19509913 | Shine label 0 to 4 Yrs; JD text: 0-1 year | not disclosed | A/B testing, Mixpanel/Amplitude, Power BI, SQL, Tableau, communication, dashboards/reporting, stakeholder, statistics | Shine (posted 1 month ago) |
| B40 | Dev Mantra Financial Services | MIS and Automation | Bangalore | https://www.shine.com/jobs/mis-and-automation/dev-mantra-financial-services/19488527 | Shine label 0 to 4 Yrs | not disclosed | Excel, Google Sheets, MIS, Power BI, Power Query, Tableau, VBA, communication, dashboards/reporting, stakeholder | Shine (posted 1 month ago) |
| B41 | OneOrigin | Product and Process Intelligence Analyst | Bangalore | https://www.shine.com/jobs/product-and-process-intelligence-analyst/oneorigin/19733305 | Shine label 1 to 5 Yrs; JD text: 1 year | not disclosed | GenAI/AI tools | Shine (posted 1 week ago) |
| B42 | TP | WFM- MIS Reporting // Bangalore | Bangalore | https://www.shine.com/jobs/wfm-mis-reporting-bangalore/tp/19630195 | Shine label 0 to 4 Yrs | not disclosed | MIS, Power BI, communication, dashboards/reporting, stakeholder | Shine (posted 3 weeks ago) |

## 4. Skill tallies (n = 42)

Class rule as before: Must-have >= 50%, Common 20-50%, Good-to-have < 20%.

| Skill / tool | Count | % of 42 | Class |
|---|---|---|---|
| Communication | 30 | 71.4% | Must-have |
| Excel | 20 | 47.6% | Common |
| SQL | 21 | 50.0% | Must-have |
| Dashboards / reporting / MIS | 34 | 81.0% | Must-have |
| Python | 17 | 40.5% | Common |
| Power BI | 19 | 45.2% | Common |
| Statistics (named) | 13 | 31.0% | Common |
| GenAI / AI tools | 5 | 11.9% | Good-to-have |
| Stakeholder management | 25 | 59.5% | Must-have |
| Tableau | 16 | 38.1% | Common |
| Machine learning | 5 | 11.9% | Good-to-have |
| R | 4 | 9.5% | Good-to-have |
| Snowflake | 0 | 0.0% | Not seen |
| Alteryx | 0 | 0.0% | Not seen |
| Google Sheets | 3 | 7.1% | Good-to-have |
| Any cloud (AWS/Azure/GCP) | 3 | 7.1% | Good-to-have |
| ETL | 3 | 7.1% | Good-to-have |
| DAX | 1 | 2.4% | Good-to-have |
| VBA / macros | 2 | 4.8% | Good-to-have |
| SAP | 1 | 2.4% | Good-to-have |
| Looker | 6 | 14.3% | Good-to-have |
| A/B testing | 5 | 11.9% | Good-to-have |
| BigQuery | 1 | 2.4% | Good-to-have |
| Domain knowledge (named) | 2 | 4.8% | Good-to-have |
| Data cleaning (named) | 2 | 4.8% | Good-to-have |
| Power Query | 2 | 4.8% | Good-to-have |
| Looker Studio / Data Studio | 2 | 4.8% | Good-to-have |
| Metabase | 4 | 9.5% | Good-to-have |
| Jira | 2 | 4.8% | Good-to-have |
| Mixpanel / Amplitude | 2 | 4.8% | Good-to-have |
| Spark | 1 | 2.4% | Good-to-have |
| Databricks | 0 | 0.0% | Not seen |
| MIS named explicitly | 8 | 19.0% | Good-to-have |

## 5. Pay and certifications

- Pay shown in 7 of 42 rows (units as stated by the source):
  - Newton School / Data Analyst: Rs 4-8 LPA
  - Velocity / Data Analyst: Rs 20-30 LPA + equity (a sister posting 4629922 shows Rs 18-25 LPA; counted once)
  - Codemonk / Associate Business Analyst: Rs 4-6 LPA
  - Finifi / Product Analyst Intern: Rs 20,000/month stipend (3 months, PPO possible)
  - KPMG / Operation Analyst: Rs 3.65 LPA
  - Swiggy (via aggregator) / Business Analyst: 'INR 60K' (aggregator figure, period unstated)
  - DSHINE PRO SOLUTIONS / Data Analyst: 3.0 - 5 Lakh/Yr
- Named analytics certification: **none** in any of the JDs. Only: Salesforce Admin Certified (preferred) in Qualcomm Business Operations Analyst (a CRM cert, 2-4 yrs), and CA/CFA/MBA-type finance qualifications in Dev Mantra MIS and Automation. Cisco says certifications generically. PL-300 / Google DA / Tableau certs are not named anywhere.

## 6. Use with the first sample

This file does not merge the two samples. Compare Section 4 with Section 3 of `market_skills_2026.md` (Excel, SQL, Python, Power BI, Tableau, statistics, GenAI) to see whether the first sample's Built In skew mattered.
