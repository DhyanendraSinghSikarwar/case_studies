# PLAN.md — Data Analyst Interview Book Series

**Target reader:** Non-technical career switcher (HR → Data Analytics)
**Target roles:** Data Analyst, Business Analyst, MIS/Reporting Analyst, BI Analyst, Product/Operations Analyst, People/HR Analytics Analyst
**Target salary:** ₹6–10 LPA
**Target cities:** Hyderabad, Bengaluru (also applies to Pune, Chennai, NCR)
**Market basis:** 2026 job postings (Naukri, LinkedIn, Indeed, Glassdoor, AmbitionBox) — to be re-verified in Phase 0

---

## 1. Goals

| Goal | Measure |
|---|---|
| Cover what is actually asked | Each skill book ≥ 600 Q&As |
| Rank by frequency | Every Q marked ⭐⭐⭐ / ⭐⭐ / ⭐, sorted most → least asked |
| Beginner-friendly | Every answer understandable by someone with no tech background |
| Interview-ready | Answers written as a strong candidate would say them, plus what the interviewer is checking |
| Skill-building | Every book includes "how to develop this skill" from zero |
| Market-aligned | Skills chosen from current job postings, not assumptions |

---

## 2. Market Snapshot (Phase 0 research, Oct 2026)

**Confidence caveat:** JD sample = 186 in-scope postings pooled from 5 samples (Built In, LinkedIn public pages, Shine, TheIndiaJobs, employer career sites; Naukri/Indeed/Glassdoor/foundit blocked), non-random, ±7 pt error. Pooled table is the Addendum in `research/market_skills_2026.md`. Interview evidence is anonymous and candidate-reported (Glassdoor/AmbitionBox/Reddit blocked; ~9 pages read directly). Sources: `research/market_skills_2026.md`, `research/interview_processes.md`. Re-run with a larger sample before any hard cut.

| Finding | Implication for books |
|---|---|
| Must-have (≥50%, n=186): dashboards/reporting 75%, communication 73%, Excel 60%, SQL 54% | Excel and SQL full size; Book 11 communication part prioritised |
| Common (20–50%): stakeholder mgmt 44%, Power BI 40%, Tableau 33%, Python 32%, statistics 23% | Python, Power BI, Tableau, Stats core; Tableau part restored to 40 |
| Good-to-have (<20%): ETL 18%, GenAI/AI tools 14%, VBA 13%, ML 10%, cloud 10%, R 9%, Sheets 8%, DAX 5%, A/B 4%, Snowflake 4%, Alteryx 3% | Shrink cloud, ML internals, advanced DAX, LLM/RAG |
| Earlier belief "SQL/Python/Power BI/stats in almost all JDs" NOT supported (Python 32%, Power BI 40%); SQL/Excel are the only tools above 50% | Python is beginner-first; do not over-weight |
| Segment differences: MIS/reporting roles → Excel 72%, SQL 44%, Python 16%; Bengaluru/Hyderabad/GCC → Python ~40%, Tableau ~40–48%, stakeholder mgmt ~60% | Book 0 role guide: pick learning order by target role |
| Interviews differ from JDs: SQL in nearly all ~20 company profiles; project walkthrough, aptitude, HR in ~14–15; Python ~10; Power BI/DAX ~7; Excel ~5; stats/guesstimate/cases ~6–8 | Keep Stats, Guesstimates, Scenarios even though JDs rarely name them |
| Service MNCs: 2–4 rounds (aptitude → technical SQL/Power BI/Python → managerial → HR); Accenture adds English communication test | Aptitude + communication-test part; Book 0 by company type |
| GCCs: Amazon = SQL screen + Leadership-Principle STAR rounds (~4 sources); others thin/unverified for DA | Amazon LP STAR bank in Book 11 |
| Analytics firms: hard online gate, SQL, Python, probability/stats ("hardest part" at Tiger), puzzles, guesstimates/cases | Probability & Bayes enlarged; guesstimates kept |
| Startups (Meesho, PhonePe, Flipkart): hardest SQL (window functions, recursive CTEs), metric-drop cases | SQL tiered by company type; recursive CTE, dedup, running totals covered |
| GenAI/LLM: 20% of JDs name AI tools; only 1 interview report of LLM/RAG test (Infosys Hyd, Mar 2026) | Practical GenAI-for-analysts enlarged; LLM/RAG and cloud shrunk, labelled "emerging" |
| Group discussion: mostly campus/pre-2023; 2026 evidence only Indium (1 report) + Novartis (1) | GD playbook shortened |
| Pay seen in JDs (8 of 40 showed pay): mostly ₹3.5–9 LPA; ₹6–10 LPA is the upper part, at GCCs/product/finance-analytics | Set salary expectations honestly in Book 0 and Book 11 Part 8 |
| No certification (PL-300, Google DA) named in any of the 40 JDs | Book 12 certs: "optional, value unverified" |
| Switcher-friendly: MIS/reporting, operations analyst (Excel-first), HR-tech reporting (Workday Prism entry role) | Book 0 role guide; Workday/Alteryx mini-section in Book 10 |

---

## 3. Book List

| # | Book | Type | Q target |
|---|---|---|---|
| 0 | Career Switch & Interview Process Guide (HR → DA) | Guide | Guide + 100 FAQs |
| 1 | Excel for Data Analysts (formulas → Power Query → dashboards) | Q&A + practical | 600 |
| 2 | SQL (easy → hard, scenario-based) | Q&A + code | 600 |
| 3 | Python & pandas for Analysts (from zero) | Q&A + code | 600 |
| 4 | Power BI (+ Tableau basics) & Data Visualization | Q&A + practical | 600 |
| 5 | Statistics & Maths for Data Analysts | Q&A + scenarios | 600 |
| 6 | Aptitude & Business Maths (online assessment) | Q&A + shortcuts | 630 |
| 7 | Guesstimates, Case Studies & Product/Business Metrics | Q&A + frameworks | 600 |
| 8 | Scenario-Based & Data Interpretation Questions | Q&A | 600 |
| 9 | Basic ML + AI Tools for Analysts (only what DA roles ask) | Q&A + code | 600 |
| 10 | Domain Knowledge (HR/People Analytics, E-com, BFSI, Healthcare, Supply Chain) | Q&A | 615 |
| 11 | Soft Skills, HR Round, GD & Career-Switch Story | Q&A + scenarios + playbooks | 630 |
| 12 | Portfolio, Resume, LinkedIn/Naukri & Job Search | Guide + 100 FAQs | Guide |

Total: ~6,675 Q&As + 2 guides. No new book added: Phase 0 found no missing must-have skill (Excel, SQL, dashboards, communication all covered). Changes are part-level rebalances (Section 6, marked **[P0]**).

---

## 4. Star & Difficulty Rules

| Mark | Meaning |
|---|---|
| ⭐⭐⭐ | Asked in most DA interviews; must know |
| ⭐⭐ | Asked often; expected from good candidates |
| ⭐ | Occasional; differentiator at 8–10 LPA or product companies |
| 🟢 / 🟡 / 🔴 | Easy / Medium / Hard |

Sort order inside every part: ⭐⭐⭐ → ⭐⭐ → ⭐; within same star, 🟢 → 🟡 → 🔴.

---

## 5. Answer Template (beginner-friendly, interview-ready)

```
### Q<n> ⭐⭐⭐ 🟢 <Question>
**Asked at:** <company types: service MNC / product / startup / GCC / consulting>
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1–2 line direct answer, plain words>
**Explain simply:**
- 2–5 points, no jargon (or jargon explained)
**Example:** <real-life / HR-background-friendly example with numbers>
**Code / Steps:** <SQL / pandas / Excel formula / DAX / click-steps where relevant>
**Likely follow-ups:** 1–3 with short answers
**Common mistakes:** <what beginners get wrong>
```

Book-specific additions:
| Book | Extra fields |
|---|---|
| 2 SQL | Table + sample data, SQL answer, **pandas equivalent**, output table, edge cases (NULLs, duplicates, ties) |
| 1 Excel | Formula, alternative formula, sample sheet layout |
| 4 Power BI | DAX, model diagram (text), click-path |
| 5 Stats | Formula in plain words, worked numeric example, Excel/Python one-liner |
| 6 Aptitude | Shortcut method + time-saving trick |
| 7 Guesstimates/Cases | Framework → clarifying questions → step-by-step numbers → sanity check |
| 8 Scenarios | Clarify → hypotheses → data needed → analysis → recommendation |
| 11 Soft skills | Weak answer vs strong answer, STAR breakdown |

---

## 6. Detailed Content Plan per Book

Each skill book ends with a **"How to Develop This Skill" part**: zero-to-job-ready roadmap, daily practice plan, free resources, practice datasets, mini-projects, self-check tests.

### Book 0 — Career Switch & Interview Process Guide
| Section | Content |
|---|---|
| 1 | DA vs BA vs MIS vs BI vs Product Analyst — what each does, pay bands |
| 2 | Skills demanded in 2026 (must-have vs good-to-have), from Phase 0 research |
| 3 | **[P0]** Interview process by company type (from `research/interview_processes.md`, with reliability caveats: candidate-reported, thin for HSBC/JPMorgan/Microsoft/Swiggy/Zepto, LatentView has no Hyd/Blr reports; advise checking with the recruiter): service MNCs (TCS, Infosys, Accenture, Deloitte, Cognizant, Wipro), GCCs (Amazon, Wells Fargo, Novartis…), product/startups (Flipkart, PhonePe, Meesho…), analytics firms (Tiger Analytics, Mu Sigma, Indium…) |
| 2b | **[P0]** Honest pay bands (JDs mostly ₹3.5–9 LPA; ₹6–10 LPA = upper end) and switcher-friendly entry roles (MIS, ops analyst, HR-tech reporting) |
| 4 | Round-by-round expectations: online test, SQL live, Excel/Power BI task, case/guesstimate, take-home, HR, GD |
| 5 | How HR experience is an advantage (people analytics, stakeholder skills, domain) |
| 6 | 6-month learning roadmap for a non-technical beginner |
| 7 | 100 FAQs on switching careers |

### Book 1 — Excel (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | Basics: cell refs, sorting, filtering, formatting, shortcuts 🟢 | 60 |
| 2 | Core functions: IF, AND/OR, COUNTIF(S), SUMIF(S), text & date functions 🟢 | 70 |
| 3 | Lookups: VLOOKUP, HLOOKUP, INDEX-MATCH, XLOOKUP 🟢🟡 | 60 |
| 4 | Pivot tables, pivot charts, slicers 🟢🟡 | 70 |
| 5 | Data cleaning: duplicates, TRIM, text-to-columns, Flash Fill 🟢 | 50 |
| 6 | Dynamic arrays: FILTER, UNIQUE, SORT, LET 🟡 | 40 |
| 7 | Power Query & Power Pivot 🟡 | 60 |
| 8 | Charts & Excel dashboards 🟡 | 50 |
| 9 | What-if, Goal Seek, conditional formatting, data validation 🟡 | 40 |
| 10 | Scenario/practical tasks (MIS reports, HR attrition sheet) 🟡🔴 | 60 |
| 11 | **[P0]** VBA basics (12; 13% of JDs) + Copilot in Excel & Google Sheets (8) ⭐ | 20 |
| 12 | How to develop Excel skills | 20 |

### Book 2 — SQL (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | SELECT, WHERE, ORDER BY, DISTINCT, LIMIT 🟢 | 50 |
| 2 | Aggregates, GROUP BY, HAVING 🟢 | 55 |
| 3 | Joins: inner, left, right, full, self, cross 🟢🟡 | 70 |
| 4 | Subqueries & CTEs 🟡 | 55 |
| 5 | Window functions: ROW_NUMBER, RANK, DENSE_RANK, top-N per group 🟡 | 65 |
| 6 | Window functions: running totals, LAG/LEAD, moving averages 🟡 | 50 |
| 7 | CASE WHEN, NULL handling, string & date functions 🟢🟡 | 50 |
| 8 | Scenario business queries: sales, HR, e-com, banking 🟡🔴 | 70 |
| 9 | Retention, cohorts, funnels, MoM growth 🔴 | 40 |
| 10 | **[P0]** Duplicates/de-duplication, nth highest (DENSE_RANK), running totals, gaps & islands, recursive CTE, query optimisation 🔴 | 40 |
| 11 | DB concepts: keys, normalization, indexes, views, stored procedures, DDL/DML 🟢🟡 | 35 |
| 12 | How to develop SQL skills (practice plan, platforms) | 20 |

### Book 3 — Python & pandas (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | Python basics: variables, types, lists, dicts, loops, functions 🟢 | 70 |
| 2 | Strings, file handling, error handling 🟢 | 45 |
| 3 | **[P0]** NumPy basics 🟢 | 25 |
| 4 | pandas: read, select, filter, sort 🟢 | 70 |
| 5 | pandas: groupby, merge, pivot, apply 🟡 | 70 |
| 6 | Data cleaning: missing values, duplicates, types, outliers 🟡 | 60 |
| 7 | Dates & time series in pandas 🟡 | 40 |
| 8 | Visualization: matplotlib, seaborn 🟢🟡 | 45 |
| 9 | EDA end-to-end tasks (live coding style) 🟡🔴 | 50 |
| 10 | **[P0]** Basic coding logic asked in DA rounds (reverse string, palindrome, counts, easy list/string/dict problems, basic CS/OOP fundamentals) 🟢🟡 | 65 |
| 11 | Jupyter, APIs, Excel automation, using AI assistants correctly 🟡 | 40 |
| 12 | How to develop Python skills | 20 |

### Book 4 — Power BI & Visualization (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | Power BI basics: components, Desktop vs Service, workflow 🟢 | 55 |
| 2 | Power Query transformations 🟢🟡 | 60 |
| 3 | Data modelling: star schema, relationships, cardinality 🟡 | 60 |
| 4 | **[P0]** DAX basics: calculated column vs measure, SUM vs SUMX, COUNT, CALCULATE 🟡 | 75 |
| 5 | **[P0]** DAX advanced: filter context, time intelligence, ALL vs ALLEXCEPT, RANKX 🔴 | 35 |
| 6 | Visuals, slicers, drill-through, bookmarks, tooltips 🟢🟡 | 55 |
| 7 | **[P0]** Service: publishing, refresh, gateways, row-level security (RLS), workspaces 🟡 | 65 |
| 8 | Dashboard design principles & storytelling 🟢🟡 | 45 |
| 9 | **[P0]** Scenario tasks: build HR/sales dashboard, fix slow report 🔴 | 70 |
| 10 | **[P0]** Tableau basics & Power BI vs Tableau (33% of JDs; ⭐⭐ not ⭐) | 40 |
| 11 | Copilot/AI features in Power BI ⭐ | 20 |
| 12 | How to develop Power BI skills | 20 |

### Book 5 — Statistics & Maths for Data Analysts (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | Maths foundations: percentages, ratios, averages, growth rates, weighted average 🟢 | 60 |
| 2 | Descriptive stats: mean/median/mode, variance, SD, percentiles, IQR 🟢 | 60 |
| 3 | Distributions: normal, binomial, Poisson, skewness, kurtosis 🟡 | 50 |
| 4 | **[P0]** Probability & Bayes (puzzles asked; analytics firms rate stats "hardest") 🟡 | 70 |
| 5 | Sampling, bias, CLT, confidence intervals 🟡 | 50 |
| 6 | Hypothesis testing: p-value, t-test, chi-square, ANOVA, errors 🟡 | 70 |
| 7 | Correlation vs causation, regression basics, R² 🟡 | 50 |
| 8 | **[P0]** A/B testing for analysts 🟡🔴 (JDs: 2.5%; kept above rare-skill size as product firms ask) | 40 |
| 9 | Outliers, Simpson's paradox, misleading stats 🟡 | 40 |
| 10 | Scenario-based stats questions (asked in Hyd/Blr loops) 🔴 | 60 |
| 11 | Stats in Excel & Python (functions, one-liners) 🟢 | 30 |
| 12 | How to develop stats/maths skills | 20 |

### Book 6 — Aptitude & Business Maths (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | Percentages, profit & loss, discounts | 70 |
| 2 | Ratio, proportion, averages, mixtures | 60 |
| 3 | Time & work, time-speed-distance | 60 |
| 4 | Simple/compound interest, business finance basics | 50 |
| 5 | Number series, number system | 50 |
| 6 | Permutation, combination, probability | 60 |
| 7 | Logical reasoning: puzzles, seating, blood relations, syllogisms | 80 |
| 8 | Data interpretation: tables, bar/pie/line charts | 80 |
| 9 | Data sufficiency | 40 |
| 10 | Speed tricks & mock test sets | 50 |
| 11 | **[P0]** English/communication assessment (Accenture-style) + embedded SQL/CS-fundamentals items seen in online tests | 30 |

### Book 7 — Guesstimates, Case Studies & Business Metrics (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | Guesstimate framework (top-down, bottom-up, sanity checks) + India population base numbers 🟢 | 30 |
| 2 | Market-size guesstimates (e.g., cars in Hyderabad, chai cups sold daily) 🟡 | 90 |
| 3 | Revenue/operations guesstimates (Swiggy orders/day, metro riders) 🟡🔴 | 70 |
| 4 | Business metrics: KPIs, DAU/MAU, CAC, LTV, churn, retention, conversion 🟢🟡 | 80 |
| 5 | Root-cause cases: "sales dropped 20%", "orders fell on Tuesdays" 🟡🔴 | 90 |
| 6 | Profitability, pricing, growth cases 🟡🔴 | 70 |
| 7 | Product analytics cases (feature launch, funnel drop) 🔴 | 70 |
| 8 | HR/People analytics cases (attrition, hiring funnel, pay equity) 🟡 | 50 |
| 9 | How to develop structured thinking | 50 |

### Book 8 — Scenario-Based & Data Interpretation (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | Data quality scenarios (missing, wrong, duplicate data) | 70 |
| 2 | Stakeholder request scenarios (vague asks, urgent reports) | 70 |
| 3 | Dashboard/report scenarios (numbers mismatch, slow refresh) | 70 |
| 4 | Metric-change investigations | 80 |
| 5 | Analysis-approach scenarios ("how would you analyse X") | 90 |
| 6 | Data interpretation from given tables/charts | 80 |
| 7 | Prioritisation & ethics scenarios | 60 |
| 8 | Project deep-dive questions ("walk me through your project") | 60 |
| 9 | How to practise scenario thinking | 20 |

### Book 9 — Basic ML + AI Tools for Analysts (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | **[P0]** What ML is; supervised vs unsupervised; when analysts use it 🟢 | 76 |
| 2 | **[P0]** Linear & logistic regression (intuition + sklearn) 🟢🟡 | 85 |
| 3 | **[P0]** Decision trees, random forest (intuition) 🟡 | 38 |
| 4 | Clustering & customer segmentation (k-means, RFM) 🟡 | 60 |
| 5 | **[P0]** Model evaluation: accuracy, precision, recall, confusion matrix, RMSE 🟡 | 80 |
| 6 | **[P0]** Overfitting, train/test split, feature engineering basics 🟡 | 38 |
| 7 | **[P0]** Forecasting basics (moving average, trend, seasonality) 🟡 | 38 |
| 8 | **[P0]** Attrition prediction & churn mini-projects (HR-friendly) 🟡🔴 | 30 |
| 9 | **[P0]** GenAI for analysts: ChatGPT/Claude/Copilot for SQL & analysis, prompt basics, verifying AI output 🟢 (20% of JDs name AI tools) | 100 |
| 10 | **[P0]** LLM/RAG basics ⭐ — "emerging, 1 interview report" | 20 |
| 11 | **[P0]** Cloud basics for analysts (AWS/Azure/GCP, Snowflake, BigQuery, Fabric) ⭐ | 15 |
| 12 | How to develop ML/AI skills | 20 |

### Book 10 — Domain Knowledge (600)
| Part | Domain | Qs |
|---|---|---|
| 1 | HR / People Analytics (attrition, headcount, hiring funnel, engagement, DEI metrics) — switcher's strength | 120 |
| 2 | E-commerce & quick-commerce | 90 |
| 3 | BFSI: banking, credit, fintech, insurance | 100 |
| 4 | Healthcare & pharma | 70 |
| 5 | Supply chain & operations | 70 |
| 6 | Marketing & sales analytics | 80 |
| 7 | **[P0]** IT services / GCC reporting & MIS, plus Workday/HR-systems and Alteryx mini-section | 65 |
| 8 | How to learn a new domain fast | 20 |

### Book 11 — Soft Skills, HR Round, GD & Career-Switch Story (600)
| Part | Topic | Qs |
|---|---|---|
| 1 | "Tell me about yourself" & career-switch story (HR → DA) | 40 |
| 2 | Why data analytics / why this company / why leave HR | 40 |
| 3 | Behavioural (STAR) questions | 90 |
| 4 | **[P0]** Communication: explaining data to non-tech people (priority: 90% of JDs) | 80 |
| 5 | **[P0]** Stakeholder management & teamwork scenarios (weak vs strong answer) | 100 |
| 6 | **[P0]** Problem-solving, ownership, learning agility (+20 each in Parts 5–6: the original Book 11 part counts summed to only 560, so this restores ≥600) | 80 |
| 7 | **[P0]** Group discussion topics & how to perform (short; mostly campus-era evidence) | 30 |
| 8 | HR round: salary negotiation, notice period, gaps, relocation | 60 |
| 9 | Interview-room situations (blanking, not knowing an answer) | 40 |
| 10 | Skill-improvement playbooks: communication, storytelling, business acumen, structured thinking, presentation, written emails, confidence (each: assessment → daily practice → 30-day plan → resources → how to show it) | 40 |
| 11 | **[P0]** Amazon Leadership Principles STAR bank (Amazon GCC rounds are mostly LP behavioural). Project end-to-end walkthrough stays in Book 8 Part 8 | 30 |

### Book 12 — Portfolio, Resume, LinkedIn/Naukri & Job Search
| Section | Content |
|---|---|
| 1 | ATS-friendly resume for career switchers; translating HR work into analytics achievements |
| 2 | 5 portfolio projects (HR attrition, sales dashboard, SQL case, Python EDA, guesstimate deck) |
| 3 | LinkedIn and Naukri profile optimisation; keywords |
| 4 | Referrals, cold outreach templates, recruiter messages |
| 5 | Certifications (PL-300, Google DA): **[P0]** none named in any of 40 JDs → optional, value unverified; do after SQL/Excel/portfolio |
| 6 | Application tracker & weekly job-search routine |
| 7 | 100 FAQs |

---

## 7. Study Schedule (24 weeks, non-technical start)

| Weeks | Focus |
|---|---|
| 1–3 | Book 0, Book 1 (Excel), Book 5 Parts 1–2 (maths basics), Book 6 Parts 1–2 |
| 4–7 | Book 2 (SQL) Parts 1–6, Book 6 Parts 3–5 |
| 8–10 | Book 2 Parts 7–12, Book 4 (Power BI) Parts 1–4 |
| 11–13 | Book 4 Parts 5–12, Book 5 Parts 3–6 |
| 14–16 | Book 3 (Python) Parts 1–6, Book 5 Parts 7–12 |
| 17–18 | Book 3 Parts 7–12, Book 7 (Guesstimates & cases) |
| 19–20 | Book 8 (Scenarios), Book 10 (Domain, HR first) |
| 21–22 | Book 9 (ML + AI tools), Book 6 mocks |
| 23–24 | Book 11 (Soft skills), Book 12 (Portfolio & job search), mock interviews |

Daily (2–3 hrs): 40% SQL/Excel/Power BI practice, 25% Python/stats, 20% cases/guesstimates/aptitude, 15% soft skills & portfolio.
Soft-skill playbooks (Book 11 Part 10): 15 min/day from Week 1.

---

## 8. Execution Workflow (How to Build the Books)

Instruction being executed:
> Research the skills and questions asked for each skill, create the books, write questions most asked → least asked. Once one topic's question list is complete, another agent answers those questions (what the interviewer expects) in detail with examples, editing the same file.

### 8.1 Order of Work
| Order | Rule |
|---|---|
| Phase 0 first | Market & skills research before any book |
| Books | 0 → 2 → 1 → 4 → 5 → 3 → 6 → 7 → 8 → 10 → 9 → 11 → 12 (priority by market demand) |
| Per part | Research → Question list (frozen) → Answers → Review |
| Gate | Answers begin only after that part's question list is frozen |

### 8.2 Phase 0 — Market & Skills Research (once, before all books)
| Step | Action |
|---|---|
| 1 | Search LinkedIn, Naukri, Indeed, Glassdoor, AmbitionBox, Foundit, Instahyre for Data Analyst / BA / MIS / BI / People Analytics roles in Hyderabad & Bengaluru, 0–3 yrs, ₹6–10 LPA |
| 2 | Sample ≥ 100 job descriptions; record skills/tools mentioned |
| 3 | Count frequency per skill → classify: Must-have (≥ 50% JDs), Common (20–50%), Good-to-have (< 20%) |
| 4 | Search interview experiences (Glassdoor, AmbitionBox, GfG, LinkedIn posts, Reddit r/developersIndia, YouTube transcripts) for DA roles at service MNCs, GCCs, analytics firms, product startups in both cities |
| 5 | Record round structure, question types, difficulty per company type |
| 6 | Check salary bands for switchers / 0–3 yrs |
| 7 | If research shows a missing must-have skill, add a new book or part; if a planned skill is rare, reduce its size |

Outputs:
- `research/market_skills_2026.md` (skill → % of JDs → must/common/good)
- `research/interview_processes.md` (company type → rounds → question types)
- Update Sections 2, 3, 6 of this plan.

### 8.3 Phase 1 — Question Research (per part)
| Step | Action |
|---|---|
| 1 | Web search: "<topic> data analyst interview questions" + Hyderabad/Bengaluru + 2025/2026 |
| 2 | Search company-specific experiences for that skill |
| 3 | Record each question: source, company type, frequency count, recency |
| 4 | Save `research/BookX_PartY_sources.md` |

### 8.4 Phase 2 — Question List (per part)
| Step | Action |
|---|---|
| 1 | Merge duplicates into one canonical question |
| 2 | Assign ⭐ by frequency, 🟢🟡🔴 by difficulty |
| 3 | Sort ⭐⭐⭐ → ⭐; within star, 🟢 → 🔴 |
| 4 | Fill gaps with important questions to meet target (≥ 600 per book) |
| 5 | Write `BookX_<Name>/BookX_PartY.md`, each question followed by `<!-- ANSWER_PENDING -->` |
| 6 | Add rows to `question_index.md` to prevent cross-part duplicates |

### 8.5 Phase 3 — Answers (separate agent, edit same file)
| Step | Action |
|---|---|
| 1 | Open frozen question file |
| 2 | Replace each `<!-- ANSWER_PENDING -->` using the Section 5 template |
| 3 | Write for a non-technical reader: plain words, explain every term, real-life example (HR examples where natural) |
| 4 | Always include "What the interviewer is checking" |
| 5 | Run/verify all SQL, pandas, Python, Excel formulas, DAX logic on sample data |
| 6 | Do not reorder or renumber questions |

### 8.6 Phase 4 — Review
| Check | Pass criteria |
|---|---|
| Completeness | No `ANSWER_PENDING` left |
| Accuracy | Formulas, numbers, code verified |
| Beginner clarity | A non-technical reader can follow every answer |
| Ordering | Stars descending, numbering continuous |
| Duplicates | None across parts |
| Count | Meets target |
Then update Progress Tracker (Section 10).

### 8.7 Multi-Agent Setup
| Wave | Agents | Job | Output |
|---|---|---|---|
| 0 — Market | 2 agents: (a) job-postings & skills, (b) interview processes | Phase 0 | `research/` files + plan update |
| A — Questions | 1 agent per part | Phases 1–2 | Question files with `ANSWER_PENDING` |
| B — Answers | 1 agent per part or Q-range (e.g., Q1–30, Q31–60) | Phase 3 | Same files, answered |
| C — Review | 1 reviewer per book | Phase 4 | Fixes + `review_BookX.md` + tracker update |

Agent rules:
- Every agent reads `plan.md` and `style_guide.md` first.
- Each agent edits only its assigned file / Q-range.
- Wave B for a part starts only after Wave A for that part is done.
- No invented sources; if a site blocks access, note it in research files.
- After each wave, report counts/issues and wait for approval.

Where to run:
| Environment | How |
|---|---|
| Claude Code / Cowork | Subagents in parallel, per part or Q-range |
| Claude.ai chat | Sequential: one part per request |

### 8.8 Folder Structure
```
interviews/data_analyst/
├── plan.md
├── style_guide.md
├── question_index.md
├── research/
│   ├── market_skills_2026.md
│   ├── interview_processes.md
│   └── BookX_PartY_sources.md
├── Book00_CareerSwitch_Process/
├── Book01_Excel/
├── Book02_SQL/
├── Book03_Python_Pandas/
├── Book04_PowerBI_Viz/
├── Book05_Stats_Maths/
├── Book06_Aptitude/
├── Book07_Guesstimates_Cases/
├── Book08_Scenarios/
├── Book09_ML_AI_Tools/
├── Book10_Domain/
├── Book11_SoftSkills/
└── Book12_Portfolio_JobSearch/
```

### 8.9 Request Commands
| Command | Result |
|---|---|
| `Phase 0` | Market & interview-process research + plan update |
| `Book X Part Y – questions` | Frozen question list |
| `Book X Part Y – answers` | Answers filled in same file |
| `Book X – review` | Review + fixes |

### 8.10 Definition of Done (per book)
- All parts: Questions ✅ / Answers ✅ / Review ✅
- ≥ 600 Q&As (skill books)
- Every answer beginner-readable with interviewer expectation + example
- All code/formulas tested
- Tracker updated

---

## 9. Rules

- Question targets are minimums; add important missing questions.
- Every question must have an answer.
- Answers sound like a confident candidate speaking, not a textbook.
- HR background is used as an asset in examples, stories and domain book.

---

## 10. Progress Tracker

| Book | Parts | Questions | Answers | Review |
|---|---|---|---|---|
| Phase 0 | — | — | — | ✅ research done (JD sample 186; pending your approval) |
| 0 | 7 sections | ✅ 123 FAQs + guide outline | ⬜ | ⬜ |
| 1 Excel | 12 | ✅ 638 (after removing 11 cross-part duplicates and adding 5 gap-fills; see research/dedupe_log_book01.md) | ✅ 638 (all 12 parts merged; formulas run in LibreOffice 24.2 where supported, 365-only functions/pivots/Power Query/VBA labelled "not run here") | ✅ Wave C done 2026-10-22 (see Book01_Excel/review_Book01.md; never run in real Excel; several Microsoft/Google facts remain unverified) |
| 2 SQL | 12 | ✅ 664 (after removing 30 cross-part duplicates; see research/dedupe_log_book02.md) | ✅ 664 (all 12 parts merged; code run on SQLite 3.45.1 / pandas 3.0.5; non-SQLite syntax labelled "not run here") | ✅ Wave C done 2026-10-21 (see Book02_SQL/review_Book02.md; dialect claims for non-SQLite engines remain unverified) |
| 3 Python | 12 | ⬜ | ⬜ | ⬜ |
| 4 Power BI | 12 | ⬜ | ⬜ | ⬜ |
| 5 Stats & Maths | 12 | ⬜ | ⬜ | ⬜ |
| 6 Aptitude | 10 | ⬜ | ⬜ | ⬜ |
| 7 Guesstimates & Cases | 9 | ⬜ | ⬜ | ⬜ |
| 8 Scenarios | 9 | ⬜ | ⬜ | ⬜ |
| 9 ML + AI | 12 | ⬜ | ⬜ | ⬜ |
| 10 Domain | 8 | ⬜ | ⬜ | ⬜ |
| 11 Soft Skills | 10 | ⬜ | ⬜ | ⬜ |
| 12 Portfolio & Job Search | 7 sections | ⬜ | ⬜ | ⬜ |
