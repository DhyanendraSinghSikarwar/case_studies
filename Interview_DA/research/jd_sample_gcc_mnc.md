# JD sample: GCC / MNC / product-company career sites (supplement to market_skills_2026.md)

Accessed: 2026-10-20 to 2026-10-21. **Sample size: 25 distinct in-scope JDs, full text read**, none overlapping the 40 JDs in `market_skills_2026.md` Appendix A. Confidence: LOW-MEDIUM (n = 25; each percentage carries roughly +/- 20 points of sampling error). Amazon is 12 of 25 postings, so this sample is Amazon-heavy; do not read it as the whole GCC market.

## 1. Method

- **Sources:** official employer ATS endpoints only: Amazon (amazon.jobs JSON search), Workday career sites (Citi, Target, Thermo Fisher, Sanofi, AstraZeneca, HPE, Cisco), JPMorganChase (Oracle HCM career site) and Lever (Paytm). Full JD body fetched per posting (description, basic and preferred qualifications). Built In India was not used.
- **Candidate pool:** about 244 Amazon India postings and about 520 Workday postings (Hyderabad/Bengaluru, 25+ tenants), plus JPMC, Greenhouse and Lever boards, filtered by analyst/MIS/BI/reporting/product-analyst-type titles.
- **Inclusion rule (stricter than the first sample):** Hyderabad or Bengaluru; analyst-type role; the JD itself states a minimum experience of at most 2 years (ranges such as 2-5 count by their lower bound). Postings with no stated years, or whose experience was only implied by seniority labels, were left out rather than guessed. Roles needing 3+ years were excluded.
- **Skill rule:** same checklist as `market_skills_2026.md`; a skill counts only if the JD text names it. Statistics counts only when named as a method (t-test, regression, statistical methods), not when "Statistics" appears only in a degree list. Cloud counts only when AWS/Azure/GCP/Google Cloud is named (Redshift alone, or Amazon's own business description, not counted). GenAI counts GenAI/LLM/Copilot/ChatGPT/"AI tools"-type terms, not bare "AI". "ETL" includes the phrase "data pipelining" (Amazon uses "knowledge of data pipelining and extraction using SQL"), so ETL is likely inflated.
- **Extraction:** skills were matched by keyword patterns over the full JD text and spot-checked on ambiguous terms (statistics, GenAI, cloud, R, ML); errors are possible. Communication is under-counted for Amazon JDs where soft skills sit in a separate paragraph not present in the fetched fields.
- **Pay:** none of the 25 JDs showed a salary figure (Indian postings on these sites do not publish pay). **Certifications:** none named in any of the 25 (generic "certifications beneficial" appears in Thermo Fisher DA; no specific certification).

## 2. Sites blocked, unusable or not fetched

| Site | Result |
|---|---|
| Wells Fargo (wellsfargojobs.com) | HTTP 403; Workday API guess returned 422 |
| TCS (tcs.com/careers) | HTTP 403 |
| Infosys (infosys.com/careers) | HTTP 403 |
| Cognizant (careers.cognizant.com) | HTTP 403 |
| Tiger Analytics (tigeranalytics.com/careers) | HTTP 403 |
| Microsoft careers search API | Returned "Please try again later"; no JDs |
| Walmart, HSBC, Accenture, Goldman Sachs career pages | Pages load but are script-rendered; no job bodies retrievable, no public JSON endpoint found |
| Wipro | Public RSS feed returned only technical/other roles and ignored the keyword filter; no analyst JD in scope |
| Deloitte (apply.deloitte.com) | Search returned US postings only; no Hyderabad/Bengaluru in-scope JD found |
| Flipkart careers | Connection failed |
| Swiggy, PhonePe, Zepto, Razorpay, CRED-type boards | Not on public Greenhouse/Lever/Ashby boards (404), or script-rendered; nothing retrieved |
| Fractal, LatentView | Career pages script-rendered or 404; no JD bodies |
| Indeed, Naukri, LinkedIn, Glassdoor | Not attempted here (blocked in the first sample) |
| Meesho, Elastic, Stripe, Zinnov, GitLab, Okta, Sigmoid, MongoDB (Lever/Greenhouse) | Fetched but the Hyderabad/Bengaluru analyst roles asked 3+ years (or no years): excluded |
| Visa Data Analyst, Citi Business Analytics Analyst | Fetched; bachelor's-degree route asks 3 or 4 years (1-2 only with Master's/PhD): excluded |
| Novartis, Mastercard, State Street, Nvidia, Adobe, Salesforce, Intel, Barclays, Micron, Autodesk, eBay | Workday/Eightfold pages read; analyst postings stated 3+ years, no years, or were non-analytics: excluded |

## 3. Sampling table


| id | company | title | city | source URL | exp required | pay if shown | skills named |
|---|---|---|---|---|---|---|---|
| G01 | Amazon | Business Analyst, Amazon Pay, Data Products | Bengaluru | https://www.amazon.jobs/en/jobs/10578343/business-analyst-amazon-pay-data-products | 1+ yrs | not shown | Excel, SQL, dashboards/reporting, cloud (AWS/Azure/GCP), ETL, SAS, SPSS |
| G02 | Amazon | Business Analyst, WHS Data | Bengaluru | https://www.amazon.jobs/en/jobs/10462523/business-analyst-whs-data | 1+ yrs | not shown | Excel, SQL, dashboards/reporting, Tableau, ETL, VBA/macros |
| G03 | Amazon | Business Analyst, Innovation lab | Bengaluru | https://www.amazon.jobs/en/jobs/10581406/business-analyst-innovation-lab | 1+ yrs | not shown | Excel, SQL, dashboards/reporting, Python, ETL, SAS, SPSS |
| G04 | Amazon | Business Analyst I, CMT | Bengaluru | https://www.amazon.jobs/en/jobs/10561075/business-analyst-i-cmt | 1+ (BQ 1+; 2+ Excel/Tableau) yrs | not shown | communication, Excel, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, ML, ETL, VBA/macros, QuickSight |
| G05 | Amazon | Business Analyst I, SPS Finance Insights & Analytics | Hyderabad | https://www.amazon.jobs/en/jobs/10478398/business-analyst-i-sps-finance-insights-analytics | 1+ yrs | not shown | communication, Excel, SQL, dashboards/reporting, stakeholder mgmt, ETL, VBA/macros |
| G06 | Amazon | Business Analyst I, TSE Analytics | Hyderabad | https://www.amazon.jobs/en/jobs/10460687/business-analyst-i-tse-analytics | 2+ yrs | not shown | communication, Excel, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, ETL, VBA/macros |
| G07 | Amazon | Business Analyst, RBS ARTS (Automation Reporting and Tech Sciences) | Bengaluru | https://www.amazon.jobs/en/jobs/10521536/business-analyst-rbs-arts-automation-reporting-and-tech-sciences | 1+ yrs | not shown | communication, Excel, SQL, dashboards/reporting, Tableau, cloud (AWS/Azure/GCP), ETL, VBA/macros, QuickSight |
| G08 | Amazon | Business Analyst I, Amazon Pay | Bengaluru | https://www.amazon.jobs/en/jobs/10566492/business-analyst-i-amazon-pay | 1+ yrs | not shown | Excel, SQL, Tableau, ML, ETL, VBA/macros |
| G09 | Amazon | Business Analyst Support, GSF Last Mile | Bengaluru | https://www.amazon.jobs/en/jobs/10581089/business-analyst-support-gsf-last-mile | 1+ yrs | not shown | communication, Excel, SQL, Python, stakeholder mgmt, ETL, VBA/macros, SAS, QuickSight, SPSS |
| G10 | Amazon | Business Intelligence Engineer I, Global Reporting & Standards (GRS) | Hyderabad | https://www.amazon.jobs/en/jobs/10577005/business-intelligence-engineer-i-global-reporting-standards-grs | 2+ yrs | not shown | communication, Excel, dashboards/reporting, Python, Power BI, statistics, Tableau, cloud (AWS/Azure/GCP), ETL, QuickSight |
| G11 | Amazon | Business Intel Engineer I, FinOps | Bengaluru | https://www.amazon.jobs/en/jobs/10557558/business-intel-engineer-i-finops | 2+ yrs | not shown | communication, Excel, SQL, dashboards/reporting, Python, Power BI, statistics, stakeholder mgmt, Tableau, cloud (AWS/Azure/GCP), ETL, QuickSight |
| G12 | Amazon | Financial Analyst, DEX Finance | Bengaluru | https://www.amazon.jobs/en/jobs/10581214/financial-analyst-dex-finance | 1+ yrs | not shown | Excel, SQL, dashboards/reporting, VBA/macros |
| G13 | Citi | Data Analyst - SAS and SQL | Bengaluru | https://citi.wd5.myworkdayjobs.com/2/job/Bangaluru-Karnataka-India/Data-Analyst---SAS-and-SQL_26997928 | 2-5 yrs | not shown | SQL, dashboards/reporting, Python, ML, SAS, data cleaning/quality, SPSS |
| G14 | Target | Data Analyst | Bengaluru | https://target.wd5.myworkdayjobs.com/targetcareers/job/BangaloreIndia/Data-Analyst_R0000431066 | 2-6 overall, 1-3 relevant yrs | not shown | communication, SQL, dashboards/reporting, Python, statistics, GenAI/AI tools, stakeholder mgmt, Tableau, cloud (AWS/Azure/GCP), ETL, Looker, A/B testing, BigQuery, Databricks/Spark |
| G15 | Target | Pricing Analyst-4 | Bengaluru | https://target.wd5.myworkdayjobs.com/targetcareers/job/BangaloreIndia/Pricing-Analyst-4_R0000475691 | 2-4 yrs | not shown | communication, Excel, SQL, dashboards/reporting, statistics, stakeholder mgmt |
| G16 | Thermo Fisher Scientific | Marketing Analyst II | Bengaluru | https://thermofisher.wd5.myworkdayjobs.com/ThermoFisherCareers/job/Bangalore-India/Marketing-Analyst-II_R-01347293-1 | 2-3 yrs | not shown | SQL, dashboards/reporting, Python, Power BI, ETL, data cleaning/quality, Databricks/Spark |
| G17 | Thermo Fisher Scientific | Data Analyst – Analytics Engineering & AI | Bengaluru | https://thermofisher.wd5.myworkdayjobs.com/ThermoFisherCareers/job/Bangalore-India/Data-Analyst---Analytics-Engineering---AI_R-01369315-1 | 2-5 yrs | not shown | communication, SQL, dashboards/reporting, Python, Power BI, GenAI/AI tools, stakeholder mgmt, Tableau, ML, Snowflake, cloud (AWS/Azure/GCP), ETL, SAP, A/B testing |
| G18 | Sanofi | R&D Scientific Competitive Intelligence Analyst | Hyderabad | https://sanofi.wd3.myworkdayjobs.com/SanofiCareers/job/Hyderabad/R-D-Scientific-Competitive-Intelligence-Analyst_R2874499-1 | >=1 yrs | not shown | communication, Excel, dashboards/reporting, GenAI/AI tools, stakeholder mgmt, Tableau |
| G19 | Sanofi | Analyst Customer Facing Effectiveness | Hyderabad | https://sanofi.wd3.myworkdayjobs.com/SanofiCareers/job/Hyderabad/Analyst-Customer-Facing-Effectiveness_R2870406 | 2+ yrs | not shown | communication, Excel, SQL, dashboards/reporting, Power BI, stakeholder mgmt, Tableau, Alteryx, SAS, Qlik |
| G20 | JPMorganChase | Analyst - Financial Analysis | Bengaluru | https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/210788199 | 2-4 yrs | not shown | communication, Excel, SQL, dashboards/reporting, Python, Power BI, stakeholder mgmt, Tableau, Databricks/Spark |
| G21 | Cisco | Finance Analyst- CA, FP&A -1-2yrs exp | Bengaluru | https://cisco.wd5.myworkdayjobs.com/Cisco_Careers/job/Bangalore-India/Finance-Analyst--CA--FP-A--1-2yrs-exp_2025427 | 1-2 (per title) yrs | not shown | communication, Excel, dashboards/reporting, stakeholder mgmt, VBA/macros |
| G22 | AstraZeneca | Associate – Social Media Listening | Bengaluru | https://astrazeneca.wd3.myworkdayjobs.com/Careers/job/India---Bangalore/Associate---Social-Media-Listening_R-262147 | 2-4 yrs | not shown | communication, Excel, dashboards/reporting, data cleaning/quality |
| G23 | HPE | Sales Support Analyst | Bengaluru | https://hpe.wd5.myworkdayjobs.com/ACJobSite/job/Bengaluru-Karntaka-India/Sales-Support-Analyst_1210153-2 | 2-4 yrs | not shown | communication, dashboards/reporting, stakeholder mgmt, SAP |
| G24 | HPE | Legal (as spelled: "Legel") Operations Operations Analyst | Bengaluru | https://hpe.wd5.myworkdayjobs.com/ACJobSite/job/Bengaluru-Karntaka-India/Legel-Operations-Analyst_1215545 | 2-4 yrs | not shown | communication, Excel, dashboards/reporting, stakeholder mgmt, VBA/macros, SAP |
| G25 | Paytm | Risk Analyst / Exp - 1 to 3 Yrs | Bengaluru | https://jobs.lever.co/paytm/beb24813-6250-46c4-b8af-63aae1f2bbe6 | 1-3 yrs | not shown | communication, SQL, Python, stakeholder mgmt, ML |

Notes on experience cells: Target Data Analyst states "Overall 2-6 years exp and relevant 1-3 years"; Cisco Finance Analyst states 1-2 years only in the job title; Sanofi CI Analyst states ">=1 year" in CI/patent analytics; Amazon Business Analyst I CMT lists 1+ years of analytical/finance experience but 2+ years of Excel/Tableau.

## 4. Skill tallies (n = 25)

| Skill | Count | % of 25 | Class (>=50% must-have, 20-50% common, <20% good-to-have) |
|---|---|---|---|
| dashboards/reporting | 22 | 88% | Must-have |
| Excel | 19 | 76% | Must-have |
| SQL | 19 | 76% | Must-have |
| communication | 18 | 72% | Must-have |
| stakeholder mgmt | 15 | 60% | Must-have |
| ETL | 14 | 56% | Must-have |
| Tableau | 12 | 48% | Common |
| VBA/macros | 10 | 40% | Common |
| Python | 10 | 40% | Common |
| Power BI | 8 | 32% | Common |
| cloud (AWS/Azure/GCP) | 6 | 24% | Common |
| SAS | 5 | 20% | Common |
| ML | 5 | 20% | Common |
| QuickSight | 5 | 20% | Common |
| SPSS | 4 | 16% | Good-to-have |
| statistics | 4 | 16% | Good-to-have |
| data cleaning/quality | 3 | 12% | Good-to-have |
| GenAI/AI tools | 3 | 12% | Good-to-have |
| Databricks/Spark | 3 | 12% | Good-to-have |
| SAP | 3 | 12% | Good-to-have |
| A/B testing | 2 | 8% | Good-to-have |
| Looker | 1 | 4% | Good-to-have |
| BigQuery | 1 | 4% | Good-to-have |
| Snowflake | 1 | 4% | Good-to-have |
| Alteryx | 1 | 4% | Good-to-have |
| Qlik | 1 | 4% | Good-to-have |

Named in 0 of 25: DAX, R, Google Sheets. Other items on the checklist (Looker, BigQuery, Snowflake, Alteryx, A/B testing, SAP) each appear in 1-3 JDs, see table.

Company mix: Amazon 12, Target 2, Thermo Fisher Scientific 2, Sanofi 2, HPE 2, Citi 1, JPMorganChase 1, Cisco 1, AstraZeneca 1, Paytm 1.

## 5. Reading against the first sample (n = 40)

- Dashboards/reporting, Excel and SQL are again the top three (88%, 76%, 76% here vs 52%, 60%, 57.5% before): GCC/MNC postings name them more often than the Built In-heavy first sample.
- Python 40% (first sample 35%), Power BI 32% (32.5%), Tableau 48% (12.5%; Amazon, Sanofi, Target, Thermo Fisher JDs list it often), statistics 16% (20%), GenAI/AI tools 12% (20%), ML 20% (12.5%).
- VBA/macros 40% (first sample 5%) is driven mostly by Amazon Business Analyst JDs ("Excel VBA macros") and is the clearest difference: for Amazon-type GCC analyst roles keep VBA more than the first sample suggested.
- Cloud 24%, ETL 56% (inflated by the "data pipelining" phrase), QuickSight 20% (Amazon only).
- No pay and no named certification appeared; salary and certification conclusions still rest on the first sample.
- Amazon provides 12 of 25 rows and shares a template (SQL, Excel, Tableau/QuickSight, VBA). Excluding Amazon (n = 13): dashboards/reporting 12, communication 11, stakeholder management 10, SQL 8, Excel 7, Python 6, Tableau 5, Power BI 4, GenAI 3, ML 3, statistics 2, VBA/macros 2. Treat these tallies as a GCC/MNC supplement, not a replacement for the first sample.
