# Extra JD sample: MIS / reporting / HR-analytics / operations-analyst niches (Hyderabad, Bengaluru)

Accessed: 2026-10-20. Companion to `market_skills_2026.md` (the 40 JDs there were NOT re-sampled; no row below duplicates its Appendix A). Confidence: LOW-MEDIUM. n = 32, hand-extracted by a language model from fetched page text; extraction errors are possible.

## 1. Method

- **Target:** at least 25 new in-scope JDs. **Achieved: 32 distinct JDs, each with a real URL and fetched JD text.**
- **In-scope rule (same as the main file):** analyst / MIS / reporting / HR-analytics / operations-type role; Hyderabad or Bengaluru (multi-city listings that name Bangalore are marked); required-experience minimum at most 2 years, or fresher / entry / intern / "not stated". Postings needing 3+ years were read and excluded (Section 6).
- **Checklist and counting rule:** identical to the main file. A skill counts only if the JD text names it. "Preferred / nice to have / plus" mentions are counted as named (as the main file did for HPE "SQL nice to have"). Bare "AI" is not GenAI. "English proficiency" alone is not counted as communication. "Data visualization" alone is not counted as dashboards.
- **Sources used (Built In deliberately avoided):** Internshala job pages (8 rows), Greenhouse company boards for GHX and Cohere Health (5), Lever (Dun & Bradstreet) (1), talent.com aggregator view pages carrying JD text (16), jobinsider.in write-ups of official postings (2). Listing pages were used to find postings; every row was then opened and its body read.
- **Dead or stale postings skipped:** Apollo Hospitals MIS Executive (Hyderabad; page says no longer accepting applications), flexingit "Junior MIS Executive" (Hyderabad; project posted 11/06/2025, date format ambiguous, treated as stale), flexingit steel-and-mining MIS consultant (4+ yrs, closed), Cohere "Data Analyst L1" link (returned only the board index).
- **Caveats that matter:**
  1. **Five rows (1-5) are the same employer (Honhr, a "UK-based HR consultancy and training firm" on Internshala) with 5 openings each, 1000+ applicants and a flat Rs 4.8 LPA CTC.** They are distinct roles and each was read, but they look like a bulk-posting template. They pull the Excel / Power BI / SQL / Tableau counts up. Section 5 gives the tally with those five collapsed to one.
  2. Rows 15 and 16 come from jobinsider.in summaries of official Workday postings (Workday pages render empty without JavaScript). Their pay figures are the aggregator's own estimate, not JD figures. For JLL, SQL / Python / Tableau were described as interview topics, not JD requirements, so they were not counted.
  3. Row 7: employer is inconsistent on the page (Redfoxa Careerlink in the header, Concentrix in the body).
  4. Experience "not stated" rows (14, 19, 21, 23, 27, 31 and fresher / intern rows) are included under the entry rule; some may in practice want more.
  5. Workday / SuccessFactors / Visier were **not named in any in-scope JD**. The only Workday reporting JDs found (Carrier 8+ yrs, Empower senior, Wabtec 5+, Haleon 3-5, Accenture 3-5, Velotic 3-5) are all above the 2-year ceiling.

## 2. Blocked or unusable sites (exact)

| Site | Result |
|---|---|
| Indeed India (search pages) | HTTP 403 |
| Glassdoor (India search pages) | HTTP 403 |
| foundit.in (job page) | HTTP 403 (page content not retrieved; only search-snippet summaries seen, not counted) |
| Naukri | Not re-fetched (HTTP 403 in the main file) |
| Shine.com | WebFetch refused: "unable to fetch from www.shine.com" |
| TimesJobs | WebFetch refused: "unable to fetch from www.timesjobs.com" |
| Bayt.com job page | HTTP 403 |
| in.jobsora.com job pages | Listing page loads; each job page returned a "verifying you are not a robot" bot check, no JD text |
| jobs.weekday.works job pages | Reachable but hold only title / company / location (sometimes experience chips); no JD body; not counted |
| Workday-hosted career pages (JLL, LSEG) | Returned empty content (JavaScript-rendered); used jobinsider.in summaries instead |
| freshersworld.com | Page returned navigation and filters only |
| cutshort.io | `/jobs/hr-analytics-jobs` listed 27 jobs but none was a Hyderabad/Bengaluru role at 0-2 yrs; `/jobs/mis-jobs-in-hyderabad` returned navigation only |
| jobs.empower.com, jobs.lever.co/yuno, hackajob | HTTP 404 / 404 / 410 |
| LinkedIn, Instahyre, AmbitionBox | Not attempted (login walls assumed, as in the main file) |

## 3. Sample table (32 JDs)

Exp = minimum/range stated in the JD. "NS" = not stated. Pay is as shown; "(est.)" = aggregator estimate, not the employer.

| id | company | title | city | source URL | exp required | pay if shown | skills named |
|---|---|---|---|---|---|---|---|
| 1 | Honhr | MIS Analyst (Fresher) | Bangalore (multi-city) | https://internshala.com/job/detail/fresher-mis-analyst-job-in-multiple-locations-at-honhr1790571975 | none (fresher) | Rs 4.8 LPA | Excel, Power BI, SQL (pref), Tableau (pref), Power Query, Google Data Studio (pref), dashboards/reporting, communication, stakeholder mgmt, ERP/CRM (pref) |
| 2 | Honhr | BI Analyst | Bangalore (multi-city) | https://internshala.com/job/detail/bi-analyst-job-in-multiple-locations-at-honhr1790593277 | 1 yr (freshers encouraged) | Rs 4.8 LPA | Excel, SQL, Power BI, Tableau, Looker, DAX, statistics (statistical modeling), ETL, dashboards, data modeling |
| 3 | Honhr | Business Analyst (Fresher) | Bangalore (multi-city) | https://internshala.com/job/detail/fresher-business-analyst-job-in-multiple-locations-at-honhr1790443778 | none (fresher) | Rs 4.8 LPA | Excel, SQL, Python, Power BI (pref), Tableau (pref), reports/reporting tools, stakeholder mgmt, process analysis |
| 4 | Honhr | Research Analyst (Fresher) | Bangalore (multi-city) | https://internshala.com/job/detail/fresher-research-analyst-job-in-multiple-locations-at-honhr1790572505 | none (fresher) | Rs 4.8 LPA | Excel, PowerPoint, data visualization, reporting techniques, market research |
| 5 | Honhr | Strategy Analyst | Bangalore (multi-city) | https://internshala.com/job/detail/strategy-analyst-job-in-multiple-locations-at-honhr1790593151 | 1 yr (freshers encouraged) | Rs 6.0 LPA | Excel, PowerPoint, reports/dashboards, data analysis |
| 6 | Material Depot | Data Operations Executive | Bengaluru | https://internshala.com/job/detail/data-operations-executive-job-in-bangalore-at-material-depot1790420131 | 1-2 yrs | Rs 4-6 LPA | Excel (pivot, advanced formulas), SQL, Python, Google Sheets, data cleaning |
| 7 | Redfoxa Careerlink (body says Concentrix) | Business Analyst (Fresher) | Bengaluru | https://internshala.com/job/detail/fresher-business-analyst-job-in-bangalore-at-redfoxa-careerlink-pvt-ltd1778027420 | none (fresher) | Rs 4-4.5 LPA | communication, stakeholder mgmt, requirements gathering, documentation, data analysis and reporting |
| 8 | DeepThought CultureTech | Business Analyst (Fresher) | Secunderabad, Hyderabad | https://internshala.com/job/detail/fresher-business-analyst-job-in-multiple-locations-at-deepthought-culturetech-ventures-private-limited1792029706 | none (fresher) | Rs 15k/month for 6-month probation, then Rs 5-8 LPA | business analysis only (no tools named) |
| 9 | GHX | Managed Services Analyst I | Hyderabad | https://job-boards.greenhouse.io/globalhealthcareexchangeinc/jobs/4738994005 | 1-3 yrs | NS | Excel (basic), MS Office, trackers and dashboards, communication, case-management software |
| 10 | GHX | Document Intelligence Analyst I | Hyderabad | https://job-boards.greenhouse.io/globalhealthcareexchangeinc/jobs/4734601005 | 1-3 yrs | NS | ADM platform, data verification, typing 35 WPM, domain (procurement / US healthcare supply chain, pref); no analytics tools |
| 11 | GHX | AI Knowledge Analyst I | Hyderabad | https://job-boards.greenhouse.io/globalhealthcareexchangeinc/jobs/4736567005 | 2+ yrs | NS | communication, Excel (M365), SharePoint, Confluence, ServiceNow, Salesforce Knowledge, LLM content requirements (GenAI), Lean/Six Sigma (pref); certs: Prosci / KCS / ACMP are a plus |
| 12 | Cohere Health | Sales Support Analyst | Hyderabad | https://job-boards.greenhouse.io/coherehealth/jobs/8002135003 | 2-4 yrs (page also says "entry to 5") | NS | Excel (advanced), Google Sheets, SQL (nice), Tableau/Looker/Power BI (nice), Salesforce, dashboards, CohereGPT and Claude (GenAI), HubSpot (nice) |
| 13 | Cohere Health | Payroll Specialist | Hyderabad | https://job-boards.greenhouse.io/coherehealth/jobs/7777131003 | 2-4 yrs | NS | HROne / HCM payroll platforms (HRIS), MIS reports, dashboard reporting (nice), statutory compliance (PF, ESI, TDS), SOPs |
| 14 | Dun & Bradstreet | Analyst, Data Acquisition | Hyderabad | https://jobs.lever.co/dnb/02ab0414-b41c-4109-9ba1-1eeba9958d36 | NS ("experience in related fields preferred"); master's required (MBA / CA / ACCA / MSc) | NS | statistics (plus), data manipulation, querying datasets, MS Office, communication |
| 15 | JLL (via jobinsider.in summary) | Data Analyst (Freshers) | Bengaluru | https://www.jobinsider.in/jobs/jll-data-analyst-job-bangalore-power-bi-26/ | fresher (2025/2026 batch) | Rs 3.3-4.6 LPA (est., aggregator) | Excel, Power BI, BI dashboards, daily/weekly/monthly MIS reports, communication (pref), domain (facility ops, pref) |
| 16 | LSEG (via jobinsider.in summary) | Business Graduate Associate, Data & Analytics | Bengaluru | https://www.jobinsider.in/jobs/lseg-graduate-associate-job-data-analyst-26/ | fresher (2026/2027 batch) | Rs 6-11 LPA (est., aggregator) | SQL, Python (intro), communication, domain (financial markets) |
| 17 | Ninjacart | MIS Executive | Hyderabad | https://in.talent.com/view?id=559608553690640365 | 1-3 yrs | NS | Excel (VLOOKUP, pivot, macros/VBA), reporting tools, dashboards |
| 18 | ZS Operations Center | Data Analyst | Hyderabad | https://bebee.com/in/jobs/data-analyst-zs-operations-center-hyderabad--t7xk-892114448 | 1-3 yrs | NS | Power BI, DAX, Power Query, SQL, Excel, dashboards/reporting, Databricks / Fabric / Azure (cloud), RLS |
| 19 | McDonald's (global office, India) | Supervisor, Business Process Mgmt - HR Analytics | Hyderabad | https://in.talent.com/view?id=623397540337224096 | NS (reporting / BPM / shared-services experience) | NS | Excel, HCM systems (HRIS), operational reporting, data validation, SOPs, communication |
| 20 | Acko | Associate / Sr. Associate - MIS | Bengaluru | https://in.talent.com/view?id=605402591030749500 | 1-4 yrs | NS | SQL, Excel, Tableau, BI tools, MIS reporting |
| 21 | Tata Advanced Systems | MIS Reporting Analyst | Bengaluru | https://in.talent.com/view?id=639459543752706189 | NS; Chartered Accountant qualification | NS | Excel (pivot, VLOOKUP, macros/VBA), Power BI, Tableau, SAP, communication, stakeholder mgmt, reporting |
| 22 | Bridgestone Americas | MIS Executive - Customer Experience (JD: MIS and Data Analytics Executive) | Bengaluru | https://in.talent.com/view?id=637616848439478080 | 2-3 yrs | NS | Excel (pivot, Power Query, VBA), SQL (basic), Power BI, Tableau, Zoho BI (nice), Python / R (pref), dashboards, data warehousing; certifications in analytics/BI/MIS "an advantage" (none named) |
| 23 | HP | Business & Operations Analyst | Bengaluru | https://in.talent.com/view?id=640376813485362979 | NS | NS | Excel (advanced), Power BI, SQL (good), Power Query, Power Automate, JIRA, dashboards, business reporting, stakeholder mgmt, PowerPoint, workforce/headcount analytics |
| 24 | Rippling | PEO Operations Analyst | Bengaluru | https://in.talent.com/view?id=605331895790936639 | 18+ months (US SaaS support/implementation) | NS | HRIS systems (a plus), Google Suite, MS Office, JIRA, Confluence, communication, regulatory/payroll operations |
| 25 | Unisys Global Services India (via ViHub) | MIS Executive | Bengaluru | https://in.talent.com/view?id=637619401897946006 | 2-6 yrs | 18,000-24,000 (period/currency not stated; likely Rs per month) | Excel, MS Office, database management, report generation |
| 26 | Beyond Appliances | MIS Executive - After Sales & Operations | Bengaluru | https://in.talent.com/view?id=615158921478280083 | 2-4 yrs | NS | Excel (advanced), Google Sheets, macros, Power BI, Tableau, Google Data Studio, dashboards, Salesforce, Zoho, Power Apps, ChatGPT / Zapier / Notion AI (GenAI) |
| 27 | Vee Technologies | Finance Executive - MIS, Reporting & GST | Bengaluru | https://in.talent.com/view?id=636491656796317367 | NS | NS | Excel (pivot, INDEX-MATCH, basic macros), SAP / Tally / Oracle (advantage), communication, stakeholder coordination, domain (GST) |
| 28 | Apna (client role) | MIS Executive (JD: Business Analyst, MIS) | Bengaluru | https://in.talent.com/view?id=609662993905426037 | 2-4 yrs | NS | Excel (must), SQL, ETL / data pipelines, dashboards (plus), CRM, communication |
| 29 | Altisource | Operations Analyst | Bengaluru | https://in.talent.com/view?id=534433812908607462 | 2-4 yrs (mortgage) | NS | MS Office, macros (VBA), MS SQL, inventory/exception reports, communication, domain (mortgage), SOX/audit support |
| 30 | Wayground (Quizizz) | Revenue Operations Analyst | Bengaluru | https://in.talent.com/view?id=613114248968733652 | 1-2 yrs | NS | Salesforce, dashboards/reports, SQL (pref), Excel / Google Sheets (pref), HubSpot / Outreach / ZoomInfo (pref), communication; cert: Salesforce Administrator (bonus) |
| 31 | StepChange | Product Operations Analyst | Bengaluru | https://in.talent.com/view?id=605402590972750140 | NS | NS | Power BI, Azure, AWS, Jira, Confluence, PowerPoint, Zendesk |
| 32 | hireshire | Business Analytics Intern (paid) | Hyderabad | https://in.talent.com/view?id=616128384057678042 | none (student / recent graduate) | paid, amount NS | Excel, Google Sheets, SQL, Python, R, Power BI, Tableau, Looker (adv), cloud and ML (adv), dashboards; certs named as advantages: Google Data Analytics Certificate, Microsoft Data Analyst Associate |

## 4. Tallies (n = 32)

Class rule as in the main file: Must-have >= 50%, Common 20-50%, Good-to-have < 20%.

| Skill / tool | Count | % of 32 | Class |
|---|---|---|---|
| Excel (incl. advanced) | 23 | 71.9% | Must-have |
| Dashboards / reporting / MIS | 23 | 71.9% | Must-have |
| Communication | 14 | 43.8% | Common |
| SQL | 14 | 43.8% | Common |
| Power BI | 12 | 37.5% | Common |
| Tableau | 9 | 28.1% | Common |
| Stakeholder management | 6 | 18.8% | Good-to-have |
| VBA / macros | 6 | 18.8% | Good-to-have |
| Salesforce / CRM named (rows 1, 11, 12, 26, 28, 30) | 6 | 18.8% | Good-to-have |
| Python | 5 | 15.6% | Good-to-have |
| Google Sheets | 5 | 15.6% | Good-to-have |
| Domain knowledge named (rows 10, 15, 16, 27, 29) | 5 | 15.6% | Good-to-have |
| Power Query (rows 1, 18, 22, 23) | 4 | 12.5% | Good-to-have |
| GenAI / AI tools (named LLM / Claude / ChatGPT) | 3 | 9.4% | Good-to-have |
| HRIS tools (HROne/HCM, HCM systems, "HRIS a plus"; rows 13, 19, 24) | 3 | 9.4% | Good-to-have |
| Any cloud (Azure/AWS/Databricks/Fabric/cloud; rows 18, 31, 32) | 3 | 9.4% | Good-to-have |
| Looker (rows 2, 12, 32) | 3 | 9.4% | Good-to-have |
| JIRA (rows 23, 24, 31) | 3 | 9.4% | Good-to-have |
| Statistics (named) | 2 | 6.3% | Good-to-have |
| R | 2 | 6.3% | Good-to-have |
| ETL | 2 | 6.3% | Good-to-have |
| DAX | 2 | 6.3% | Good-to-have |
| SAP | 2 | 6.3% | Good-to-have |
| Data cleaning / validation named (rows 6, 19) | 2 | 6.3% | Good-to-have |
| Machine learning | 1 | 3.1% | Good-to-have |
| Power Automate (row 23) | 1 | 3.1% | Good-to-have |
| Snowflake | 0 | 0% | Not seen |
| Alteryx | 0 | 0% | Not seen |
| A/B testing | 0 | 0% | Not seen |
| BigQuery | 0 | 0% | Not seen |
| Workday / SuccessFactors / Visier (in-scope JDs) | 0 | 0% | Not seen |

Row-id lists behind the main counts:
- Excel: 1, 2, 3, 4, 5, 6, 9, 11, 12, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 30, 32
- Dashboards/reporting: 1, 2, 3, 4, 5, 7, 9, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 28, 29, 30, 32
- Communication: 1, 7, 9, 11, 14, 15, 16, 19, 21, 24, 27, 28, 29, 30
- SQL: 1, 2, 3, 6, 12, 16, 18, 20, 22, 23, 28, 29, 30, 32
- Power BI: 1, 2, 3, 12, 15, 18, 21, 22, 23, 26, 31, 32
- Tableau: 1, 2, 3, 12, 20, 21, 22, 26, 32
- Python: 3, 6, 16, 22, 32
- Stakeholder: 1, 3, 7, 21, 23, 27
- VBA/macros: 17, 21, 22, 26, 27, 29
- Google Sheets: 6, 12, 26, 30, 32
- GenAI: 11, 12, 26

## 5. Sensitivity and reading

- **Collapsing the five Honhr rows (1-5) into one** gives n = 28. Then: Excel 19 (67.9%), Dashboards/reporting 19 (67.9%), SQL 11 (39.3%), Power BI 9 (32.1%), Tableau 6 (21.4%), Communication 13 (46.4%), Python 4 (14.3%), Looker 2. Excel and dashboards/reporting stay Must-have; SQL, Power BI, Tableau stay Common (Tableau at the boundary).
- Against the main file (n = 40: Excel 60%, SQL 57.5%, dashboards 52.5%, Python 35%, Power BI 32.5%): in the MIS / reporting / people / operations niche, **Excel and dashboards/reporting are higher (about 68-72%) and SQL is lower (39-44%)**. Python is lower (14-16%). Power BI is similar (32-38%). Tableau is higher here (21-28% vs 12.5%) but this is mostly the Honhr template and the Bengaluru MIS postings.
- **Pooling the two files (40 + 32 = 72 JDs, Honhr as 5 rows):** Excel 47 (65%), dashboards/reporting 44 (61%), SQL 37 (51%), communication 50 (69%), Power BI 25 (35%), Python 19 (26%), Tableau 14 (19%), GenAI 11 (15%), VBA 8 (11%). Pooling assumes both files used the same counting rule; the main-file communication count was 36 and its rule counts "English proficiency" less strictly, so the pooled communication figure is the least reliable.
- **No Workday / SuccessFactors / Visier in any in-scope JD.** HR-systems experience appeared only as HROne/HCM (payroll), "HCM systems" (McDonald's HR analytics) and "HRIS a plus" (Rippling). Pure people-analytics roles that name Workday were all 3+ years in this search.
- **HR-analytics JDs in scope were scarce:** only rows 13, 19, 24 are HR-system related and none is a pure people-analytics analyst role at 0-2 years. This is a finding about availability in the sources reachable, not proof that none exist (Naukri / LinkedIn / Indeed were blocked).
- **Pay:** only 9 of 32 rows show a pay figure from the posting itself (rows 1-8: Rs 3.6-8 LPA with Honhr at 4.8-6.0; row 25: 18-24k, period unstated), plus 2 aggregator estimates (rows 15, 16). Entry-level MIS / BA postings in this sample cluster at Rs 3-6 LPA.
- **Certifications:** none required in any of the 32. Named only as advantages: Google Data Analytics Certificate and Microsoft Data Analyst Associate (row 32), Prosci / KCS / ACMP (row 11), Salesforce Administrator (row 30). Chartered Accountant appears as a qualification for row 21 and as a degree option for rows 14 and 27. Row 22 says analytics / BI / MIS certifications are an advantage without naming one.
- **Source skew:** 16 of 32 rows come from talent.com (an aggregator that republishes company JDs; relative dates only, no exact posting dates), 8 from Internshala (fresher-oriented, small-company and mass-posting heavy), 5 from Greenhouse/Lever company boards, 2 from jobinsider.in, 1 from bebee.com (ZS). Large service-MNC and BPO MIS roles on Naukri/Indeed remain unsampled.

## 6. Read but excluded (not in tally)

Experience minimum 3+ years or wrong location: Carrier HR Technology Workday Reporting (Hyd, 8+), Amgen Associate Data Analytics (Hyd, 3-5), JPMorgan MIS Finance Operations Associate (Blr, 4+), Capco MIS reporting FP&A (Blr, 3-8), Cigna Operations Senior Analyst (Blr, 5-8), Diebold BI Analyst Advanced Excel MIS (Hyd, 5-7), Tanla MIS Analyst (Hyd, 3-5), Deloitte Business Process Controls Analyst (Hyd, 2-4 but audit/CA-specific; read, not counted), Cohere Compliance Analyst (Hyd, 2+, security-compliance, not an analytics role), Cohere Associate IT Operations Analyst (Hyd, 2-3, desktop support), H1 Research Analyst (Hyd, 3+), TTEC Digital Reporting Senior Analyst (Hyd, 4+), flexingit steel-and-mining MIS consultant (Hyd, 4+, closed).
Read but no usable JD body: Scouto AI HR Fresher (Blr), King Sturge/JLL MIS Executive (Blr), Merck Group Data Analyst (Blr), Gradient Data Analyst (Blr), Centotech MIS Executive (Hyd), Multiplier Mudra "MIS Executive" (Blr; body is a sales-team role with no tools), Ultratech Zonal MIS Analytics Executive (Hyd; dispatch-planning role, no skills from the checklist; experience not stated).
Skipped as non-analyst: Internshala Symmetric Technology Busops Trainee (Blr), Mannlich Operations Executive (Blr; office operations, MS-Office only).

## 7. Other URLs consulted

- https://internshala.com/fresher-jobs/data-analytics-jobs-in-bangalore/work-from-home/ ; https://internshala.com/jobs/mis-executive-jobs-in-hyderabad/ ; /jobs/hr-analytics-jobs-in-bangalore/ ; /jobs/mis-executive-jobs-in-bangalore/ ; /jobs/data-analytics-jobs-in-hyderabad/ ; /jobs/operations-analyst-jobs-in-bangalore/ ; /jobs/business-analyst-jobs-in-hyderabad/ ; /jobs/reporting-analyst-jobs-in-bangalore/
- https://in.talent.com/jobs?k=mis+executive&l=Hyderabad ; ?k=mis+analyst&l=Bengaluru ; ?k=hr+analytics&l=Hyderabad ; ?k=operations+analyst&l=Bengaluru ; ?k=hr+analytics&l=Bengaluru (no results)
- https://bebee.com/in/jobs/role/data-analyst/hyderabad ; https://in.jobsora.com/jobs-mis-analyst ; https://www.weekday.works/jobs/data-analyst-fresher-jobs-in-bangalore ; /jobs/power-bi-jobs-25 ; https://cutshort.io/jobs/hr-analytics-jobs
- https://job-boards.greenhouse.io/globalhealthcareexchangeinc ; https://job-boards.greenhouse.io/coherehealth ; https://jobs.lever.co/h1 ; /dnb ; /ttecdigital
