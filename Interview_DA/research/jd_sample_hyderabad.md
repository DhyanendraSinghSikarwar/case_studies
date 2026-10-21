# Hyderabad JD Sample (Extra Sampling, 2026-10-20/21)

Accessed: 2026-10-20 and 2026-10-21. **Sample size: 47 distinct in-scope JDs, all with a real URL and the JD body text read.** Confidence: LOW-MEDIUM (each percentage carries roughly +/- 14 points of sampling error at n = 47). None of the 40 JDs in `research/market_skills_2026.md` Appendix A are repeated here (checked by company + title; the Cushman & Wakefield Analyst, The Hartford, TriNet Associate Pricing Analyst and Hire Daily postings were skipped as already sampled).

## 1. Method

- **Scope:** Hyderabad (or Hyderabad/Bengaluru or multi-city listings that include Hyderabad) Data/Business/BI/MIS/reporting/people-analytics/operations/product-type analyst roles whose stated minimum experience is <= 2 years (or explicit fresher/junior/intern/entry with no years). Roles with "Senior/Lead/Manager" in the title were filtered out before reading.
- **Sources used (Built In India avoided):** LinkedIn public job pages (23), Shine.com JSON-LD job pages (18), Amgen Workday careers site (2), Wellfound (2), Internshala (2). The count per source is in the table.
- **How JDs were fetched:** public pages fetched over plain HTTP with a script (curl); LinkedIn "jobs in Hyderabad" listing pages for 20+ keyword slugs gave the posting URLs, each posting page then gave the full JD text; Shine search pages gave posting URLs and each posting page carries the full JD in structured data. Workday posting JSON was used for Amgen. Wellfound and Internshala pages were read through WebFetch.
- **Skill counting rule:** same checklist and rules as `market_skills_2026.md` section 1 (a skill counts only if the JD text names it; "Excel" includes advanced Excel/pivots/VLOOKUP; "Dashboards/reporting" = dashboards, reports, reporting or MIS named; "GenAI/AI tools" = GenAI, LLM, Copilot, ChatGPT, Claude, OpenAI or "AI tools"; bare "AI" not counted; "Statistics" only when named as a skill, includes regression/hypothesis/probability). Skill detection for the LinkedIn, Shine and Workday rows was done by keyword matching over the full JD text with word-boundary patterns (not by hand), followed by spot checks; the four Wellfound/Internshala rows were extracted by hand. Keyword matching can over-count where a word appears in a non-skill sense (for example "reports" or "communication" in a general sentence) and can miss synonyms, so treat counts as +/- 2.
- **Experience column** is what the JD or its structured field says. Where Shine gives only a structured "months of experience" field it is marked as such. Two intern rows and two entry rows have no years by design.
- **Scope judgement calls (flag for the reader):** a few rows are analyst-titled but operational (HCA TA Operations, Blackbaud RevOps, Nextpower Sales Ops, BASF People Operations, Guardian Operations Analyst, Zeta FP&A Associate). They are kept because they are the ops/people/finance-analyst end of the brief and the earlier sample did the same. Revalsys (BA and Project Coordinator) and DeepThought Business Analyst are the weakest data fits; DeepThought BA names no tools at all.
- **Not done:** no login-gated pages, no scraping of paywalled content; no counts from search-engine summaries. Postings can be taken down at any time; Shine pages show a validity date a few weeks out, LinkedIn pages carry relative ages that were not recorded.
- **Also scanned, nothing usable:** about 130 Greenhouse/Lever/Ashby company boards (API) and about 90 Workday tenants for Hyderabad analyst titles. They produced only senior, engineering, fraud-investigation or long-experience roles apart from the two Amgen rows used here (Tide Hyderabad contract fraud analysts were not used: not data/BI roles).

## 2. Sites that blocked or did not help

| Site | Result |
|---|---|
| Indeed India (in.indeed.com) | HTTP 403 |
| Glassdoor India | HTTP 403 |
| Jooble India | HTTP 403 |
| SimplyHired India | Cloudflare challenge page ("Just a moment") |
| Naukri | Redirects (HTTP 301) with no content; not retrievable |
| foundit.in | Search page returns 200 but it is script-rendered; no JD bodies obtained (earlier file also recorded 403 on job pages) |
| LinkedIn guest search API | HTTP 429 (rate limited) on the API; the public "jobs in Hyderabad" listing pages and individual job pages did load |
| WebFetch tool on shine.com and timesjobs.com | Refused by the tool ("unable to fetch"); Shine worked over plain HTTP, TimesJobs was not retried |
| Cutshort job listing page | Navigation only, no postings |
| Hirist, Apna, Talent.com, FreshersWorld | Listing pages returned HTML or redirects but were not mined (time); no rows from them |
| Wellfound role pages | Worked but expose few Hyderabad analyst jobs (2 usable) |
| Internshala (Hyderabad analyst filters) | Worked but nearly all results are sales/customer roles; 2 usable |

## 3. Sampling table

| id | company | title | city | source URL | exp required | pay if shown | skills named |
|---|---|---|---|---|---|---|---|
| H1 | Trimont | Analyst, Data & Insight | Hyderabad | https://in.linkedin.com/jobs/view/analyst-data-insight-at-trimont-4468388899 | 0-1 yr | - | communication, SQL, dashboards/reporting, Python, Power BI, statistics, GenAI/AI tools, DAX, VBA/macros |
| H2 | Capgemini | FBS Strategy Integration & Reporting Analyst | Hyderabad | https://in.linkedin.com/jobs/view/fbs-strategy-integration-reporting-analyst-at-capgemini-4408177102 | 1-3 yrs (Python/PBI/SQL entry level) | - | SQL, dashboards/reporting, Python, Power BI |
| H3 | Amazon | Risk Analyst, Buyer Risk Prevention | Hyderabad | https://in.linkedin.com/jobs/view/risk-analyst-buyer-risk-prevention-payment-risk-mining-at-amazon-4455913460 | 1+ yr | - | communication, SQL, dashboards/reporting, Python, statistics, stakeholder mgmt, ML, R, ETL |
| H4 | GlobalData Plc | Analyst | Hyderabad | https://in.linkedin.com/jobs/view/analyst-at-globaldata-plc-4475233429 | 1-2 yrs | - | communication, Excel, SQL, dashboards/reporting, Python, statistics, ML, R, data cleaning |
| H5 | Deloitte | Associate (Salesforce Analyst), Client Experience Center | Hyderabad | https://in.linkedin.com/jobs/view/associate-salesforce-analyst-client-experience-center-hyderabad-hyderabad-at-deloitte-4475967692 | 1-3 yrs | - | communication, Excel, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, Salesforce |
| H6 | Amazon | Business Analyst I, SPS Finance Insights & Analytics | Hyderabad | https://in.linkedin.com/jobs/view/business-analyst-i-sps-finance-insights-analytics-at-amazon-4455903731 | 1+ yr (2+ Excel VBA) | - | communication, Excel, SQL, dashboards/reporting, stakeholder mgmt, ETL, VBA/macros |
| H7 | Amgen | Associate Field Reporting | Hyderabad | https://in.linkedin.com/jobs/view/associate-field-reporting-at-amgen-4470905634 | 1-3 yrs | - | communication, SQL, dashboards/reporting, statistics, stakeholder mgmt, Tableau, cloud, data cleaning, Jira |
| H8 | PwC USI (Growth & Purpose) | Associate, Analytics and Insights | Hyderabad | https://in.linkedin.com/jobs/view/growth-purpose-usi-digital-associate-analytics-and-insights-clients-strategy-growth-hyderabad-at-deloitte-4451412244 | 1-3 yrs | - | communication, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, DAX, Power Query |
| H9 | Marcus Evans Group | Learning & Quality Analyst | Hyderabad | https://in.linkedin.com/jobs/view/learning-quality-analyst-at-marcus-evans-group-4469126623 | 1-3 yrs | - | communication, Excel, dashboards/reporting, Power BI, stakeholder mgmt |
| H10 | Unisys | Eng Data Analyst | Hyderabad | https://in.linkedin.com/jobs/view/eng-data-analys-at-unisys-4480115801 | 2-4 yrs | - | dashboards/reporting |
| H11 | HCA Healthcare India | Analyst I - TA Operations & Tech | Hyderabad | https://in.linkedin.com/jobs/view/analyst-i-ta-operations-tech%E2%80%8B-at-hca-healthcare-india-4477409059 | 2+ yrs | - | communication, Excel, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, data cleaning |
| H12 | Sanofi | Analyst Customer Facing Effectiveness | Hyderabad | https://in.linkedin.com/jobs/view/analyst-customer-facing-effectiveness-at-sanofi-4476785651 | 2+ yrs | - | communication, Excel, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, Alteryx, Qlik, SAS |
| H13 | TriNet | Data Analyst | Hyderabad | https://in.linkedin.com/jobs/view/data-analyst-at-trinet-4472764684 | 2+ yrs | - | communication, Excel, dashboards/reporting, Power BI, statistics, GenAI/AI tools, Tableau, ETL |
| H14 | Amazon | Business Analyst, NCC-Remedy | Hyderabad | https://in.linkedin.com/jobs/view/business-analyst-ncc-remedy-at-amazon-4478560826 | 1+ yr (2+ Excel/Tableau) | - | communication, Excel, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, ETL, VBA/macros |
| H15 | Amazon | Business Analyst I, TSE Analytics | Hyderabad | https://in.linkedin.com/jobs/view/business-analyst-i-tse-analytics-at-amazon-4455796496 | 2+ yrs | - | communication, Excel, SQL, dashboards/reporting, Power BI, statistics, stakeholder mgmt, Tableau, ETL, VBA/macros |
| H16 | Guardian Capital | Operations Analyst | Hyderabad | https://in.linkedin.com/jobs/view/operations-analyst-at-guardian-capital-4478847474 | 1+ yr | Rs 5-7 LPA fixed | communication, Excel, dashboards/reporting |
| H17 | Blackbaud India | Revenue Operations Analyst | Hyderabad | https://in.linkedin.com/jobs/view/revenue-operations-analyst-at-blackbaud-india-4472556592 | 2+ yrs | - | Excel, stakeholder mgmt, Salesforce |
| H18 | Amgen | Associate Field effectiveness | Hyderabad | https://in.linkedin.com/jobs/view/associate-field-effectiveness-at-amgen-4469804003 | 1-3 yrs | - | communication, SQL, dashboards/reporting, stakeholder mgmt, Jira |
| H19 | Nextpower | Sales Operations Analyst | Hyderabad | https://in.linkedin.com/jobs/view/sales-operations-analyst-at-nextpower-4414723144 | 2+ yrs | - | communication, Excel, Power BI, stakeholder mgmt, Tableau, Google Sheets, data cleaning, Salesforce |
| H20 | Blackbaud India | Business Analyst, Associate | Hyderabad | https://in.linkedin.com/jobs/view/business-analyst-associate-at-blackbaud-india-4466568598 | 1+ yr | - | dashboards/reporting, stakeholder mgmt |
| H21 | 73 Strings | Customer Success Analyst | Hyderabad | https://in.linkedin.com/jobs/view/customer-success-analyst-at-73-strings-4479351787 | 0-2 yrs | - | communication, Excel, Power BI, GenAI/AI tools, stakeholder mgmt, Tableau, data cleaning |
| H22 | Goldman Sachs | Human Capital Management Analyst - HRIS | Hyderabad | https://in.linkedin.com/jobs/view/human-capital-management-hyderabad-analyst-hris-at-goldman-sachs-4472165449 | 1-3 yrs | - | communication, Excel, dashboards/reporting, statistics |
| H23 | Zeta Global | FP&A Associate Analyst | Hyderabad | https://in.linkedin.com/jobs/view/fp-a-associate-analyst-at-zeta-global-4462957064 | Freshers welcome (no years stated) | - | communication, Excel, dashboards/reporting, stakeholder mgmt |
| H24 | Amgen | Associate Value & Access Insights | Hyderabad | https://amgen.wd1.myworkdayjobs.com/Careers/job/India---Hyderabad/Associate-Value---Access-Insights_R-250162 | 1-3 yrs | - | communication, dashboards/reporting, Python, statistics, ML, R, cloud, ETL |
| H25 | Amgen | Associate Commercial Insights and Analytics | Hyderabad | https://amgen.wd1.myworkdayjobs.com/Careers/job/India---Hyderabad/Associate---Commercial-Insights-and-Analytics_R-231328 | 2-4 yrs | - | communication, Excel, SQL, dashboards/reporting, Python, GenAI/AI tools, stakeholder mgmt |
| H26 | Nova Technologies | Data Analyst Fresher | Hyderabad | https://www.shine.com/jobs/data-analyst-fresher-data-analytics-hyderabad/nova-technologies/19579455 | 0-1 yr | - | communication, Excel, SQL, dashboards/reporting, Python, Power BI, statistics, Tableau, Power Query, data cleaning |
| H27 | StatusNeo | Junior Power BI Analyst | Hyderabad | https://www.shine.com/jobs/junior-power-bi-analyst-hyderabad/statusneo/19593946 | 0-1 yr | - | communication, Excel, SQL, dashboards/reporting, Power BI, statistics, Tableau, DAX, Looker, Power Query |
| H28 | KTech Products | Junior Business Analyst | Hyderabad | https://www.shine.com/jobs/junior-business-analyst/ktech-products/19507631 | 1+ yr | - | communication, Excel, SQL, dashboards/reporting, stakeholder mgmt |
| H29 | Bristol Myers Squibb India | Business Intelligence Visualization and Reporting Analyst | Hyderabad | https://www.shine.com/jobs/business-intelligence-visualization-and-reporting-analyst/bristol-myers-squibb-india-pvt-ltd/19635015 | 1-2 yrs | - | communication, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, ETL, data cleaning |
| H30 | Bristol Myers Squibb India | International Markets Analytics Analyst | Hyderabad | https://www.shine.com/jobs/international-markets-analytics-analyst/bristol-myers-squibb-india-private-limited/19626716 | 1-3 yrs | - | communication, dashboards/reporting, Python, statistics, stakeholder mgmt, R, ETL, SAS, Google Analytics |
| H31 | Loyalty Juggernaut | Business Intelligence Analyst | Hyderabad | https://www.shine.com/jobs/business-intelligence-analyst/loyalty-juggernaut/19778237 | 0-1 yr | - | communication, SQL, dashboards/reporting, Python, Power BI, statistics, stakeholder mgmt, Tableau, R, Snowflake, cloud, ETL, Looker, BigQuery, data cleaning |
| H32 | MyCareernet (client) | Business Intelligence Analyst | Hyderabad | https://www.shine.com/jobs/business-intelligence-analyst/mycareernet/19635448 | min 1 yr | - | communication, Excel, dashboards/reporting, stakeholder mgmt, Tableau, ETL, data cleaning |
| H33 | Milestone Online Technology | Business Analyst - Excel & SQL | Hyderabad | https://www.shine.com/jobs/business-analyst-excel-sql/milestone-online-technology/19541834 | 0-1 yr | - | communication, Excel, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, Jira |
| H34 | Goodyear | Associate Data Analyst | Hyderabad | https://www.shine.com/jobs/associate-data-analyst/the-goodyear-tire-rubber-company/19496059 | 1-3 yrs | - | communication, SQL, dashboards/reporting, Python, Power BI, statistics, stakeholder mgmt, Tableau, data cleaning |
| H35 | EBG Group | MIS Data Analyst & Automation Specialist | Hyderabad | https://www.shine.com/jobs/mis-data-analyst-automation-specialist-hyderabad/ebg-group/19564280 | 2-3+ yrs | - | Excel, SQL, dashboards/reporting, Python, Power BI, statistics, Google Sheets, ETL, DAX, Looker, BigQuery, Power Query, data cleaning |
| H36 | Skilltransform | Junior Data Analyst | Hyderabad | https://www.shine.com/jobs/junior-data-analyst/skilltransform/19845799 | 0 yrs (freshers) | Rs 1.8-3 LPA | Excel, SQL, Python |
| H37 | Intercontinental Exchange (ICE) | Junior Data Analyst, Model Risk Management | Hyderabad | https://www.shine.com/jobs/junior-data-analyst-model-risk-management/intercontinental-exchange-holdings-inc/19592555 | Junior; no years stated | - | communication, dashboards/reporting, Python, statistics, Tableau |
| H38 | Capgemini | Financial Data Analyst Intern | Hyderabad | https://www.shine.com/jobs/financial-data-analyst-intern/capgemini/19559872 | No experience required (intern) | - | communication, Excel, SQL, dashboards/reporting, Power BI, statistics, stakeholder mgmt |
| H39 | Novartis India | Data Analyst Intern | Hyderabad | https://www.shine.com/jobs/data-analyst-intern/novartis-india/19486548 | Entry level (intern) | - | dashboards/reporting, Power BI, GenAI/AI tools |
| H40 | Avyan Packaging LLP | MIS Analyst | Hyderabad | https://www.shine.com/jobs/mis-analyst/avyan-packaging-llp/19576339 | 2+ yrs | up to Rs 40,000/month (range start truncated in text) | (none of the checklist named) |
| H41 | Flutter Entertainment India | SRPM Analyst | Hyderabad | https://www.shine.com/jobs/srpm-analyst/flutter-entertainment-india/19595589 | 2+ yrs | - | communication, Excel, dashboards/reporting, stakeholder mgmt |
| H42 | BASF (via Accenture) | People Operations Analyst | Hyderabad | https://www.shine.com/jobs/people-operations-analyst-5pm-2am-shift/basf-accenture/19626022 | 1-4 yrs | - | communication, Excel, dashboards/reporting, stakeholder mgmt, SAP, data cleaning |
| H43 | Brainworks Business Solutions | Data Analyst (US healthcare) | Hyderabad (multi-city listing) | https://www.shine.com/jobs/data-analyst/brainworks-business-solutions-private-limited/19849658 | 2 yrs (Shine structured field only) | - | communication, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Snowflake, ETL, data cleaning |
| H44 | Revalsys Technologies | Business Analyst and Project Coordinator | Hyderabad | https://wellfound.com/jobs/4666082-business-analyst-and-project-coordinator | 2+ yrs | Rs 10k-90k (as listed) | communication, SQL, stakeholder mgmt, GenAI/AI tools, Jira |
| H45 | Xohani Solutions | Data Analyst (SQL, Power BI/Tableau, Python) | Hyderabad / Bengaluru | https://wellfound.com/jobs/4629982-technology-transformation-ead-engineering-data-analyst | 2-6 yrs | Rs 12-22 LPA | communication, SQL, dashboards/reporting, Python, Power BI, Tableau, Looker, R, stakeholder mgmt, Salesforce |
| H46 | DeepThought CultureTech | Data Analytics Associate (Fresher) | Secunderabad, Hyderabad | https://internshala.com/job/detail/fresher-data-analytics-associate-job-in-multiple-locations-at-deepthought-culturetech-ventures-private-limited1792029290 | 0 yrs | Rs 15k/month probation, then Rs 5-6 LPA | dashboards/reporting, GenAI/AI tools |
| H47 | DeepThought CultureTech | Business Analyst (Fresher) | Secunderabad, Hyderabad | https://internshala.com/job/detail/fresher-business-analyst-job-in-multiple-locations-at-deepthought-culturetech-ventures-private-limited1792029706 | 0 yrs | Rs 15k/month probation, then Rs 5-8 LPA | (none of the checklist named) |

Rows by source: LinkedIn 23, Shine 18, Workday (Amgen careers) 2, Wellfound 2, Internshala 2.

Duplicates: Capgemini FBS Strategy Integration & Reporting Analyst appears on both LinkedIn and Shine; counted once (LinkedIn URL). Blackbaud Business Analyst, Associate likewise counted once. Sanofi Analyst Customer Facing Effectiveness appears on LinkedIn and Workday; counted once.

## 4. Skill tallies (n = 47)

Class rule as before: Must-have >= 50%, Common 20-50%, Good-to-have < 20%.

| Skill | Count | % | Class |
|---|---|---|---|
| communication | 37 | 78.7% | Must-have |
| Excel | 26 | 55.3% | Must-have |
| SQL | 24 | 51.1% | Must-have |
| dashboards/reporting | 40 | 85.1% | Must-have |
| Python | 14 | 29.8% | Common |
| Power BI | 23 | 48.9% | Common |
| statistics | 16 | 34.0% | Common |
| GenAI/AI tools | 7 | 14.9% | Good-to-have |
| stakeholder mgmt | 30 | 63.8% | Must-have |
| Tableau | 19 | 40.4% | Common |
| ML | 3 | 6.4% | Good-to-have |
| R | 6 | 12.8% | Good-to-have |
| Snowflake | 2 | 4.3% | Good-to-have |
| Alteryx | 1 | 2.1% | Good-to-have |
| Google Sheets | 2 | 4.3% | Good-to-have |
| cloud | 3 | 6.4% | Good-to-have |
| ETL | 12 | 25.5% | Common |
| DAX | 4 | 8.5% | Good-to-have |
| VBA/macros | 4 | 8.5% | Good-to-have |
| SAP | 1 | 2.1% | Good-to-have |
| Looker | 4 | 8.5% | Good-to-have |
| A/B testing | 0 | 0.0% | Not seen |
| BigQuery | 2 | 4.3% | Good-to-have |
| domain knowledge | 0 | 0.0% | Not seen |
| data cleaning | 13 | 27.7% | Common |
| Power Query | 4 | 8.5% | Good-to-have |
| Salesforce | 4 | 8.5% | Good-to-have |
| Jira | 4 | 8.5% | Good-to-have |
| Qlik | 1 | 2.1% | Good-to-have |
| SAS | 2 | 4.3% | Good-to-have |
| Spark/Hadoop | 0 | 0.0% | Not seen |
| Google Analytics | 1 | 2.1% | Good-to-have |

Note: "domain knowledge" and "data cleaning" are keyword-matched ("domain knowledge/expertise", "data cleaning/quality/validation"), so they are looser than the other rows.

## 5. Named certifications

- PwC USI Associate, Analytics and Insights: Tableau / Power BI certification preferred.
- MyCareernet BI Analyst (Tableau role): Tableau Desktop Specialist certification preferred.
- Milestone Online BA - Excel & SQL: CBAP, CCBA, PMI-PBA or Agile BA certifications mentioned.
- KTech Products Junior BA: professional BA certifications mentioned.
- Bristol Myers Squibb International Markets Analytics Analyst: analytics/BI certification or training mentioned.
- Guardian Capital Operations Analyst: NISM Mutual Fund Distributor certification preferred.
- Internshala pages for DeepThought list "related certification courses" (SAS, SQL, Power BI etc.) as platform upsell, not JD requirements; not counted.

## 6. Pay shown

7 of 47 rows show pay: Guardian Capital (Operations Analyst): Rs 5-7 LPA fixed; Skilltransform (Junior Data Analyst): Rs 1.8-3 LPA; Avyan Packaging LLP (MIS Analyst): up to Rs 40,000/month (range start truncated in text); Revalsys Technologies (Business Analyst and Project Coordinator): Rs 10k-90k (as listed); Xohani Solutions (Data Analyst (SQL, Power BI/Tableau, Python)): Rs 12-22 LPA; DeepThought CultureTech (Data Analytics Associate (Fresher)): Rs 15k/month probation, then Rs 5-6 LPA; DeepThought CultureTech (Business Analyst (Fresher)): Rs 15k/month probation, then Rs 5-8 LPA. Pay figures from small staffing/startup pages (Avyan, Revalsys, DeepThought probation, Skilltransform) are far below MNC bands and should not be read as the market rate.
