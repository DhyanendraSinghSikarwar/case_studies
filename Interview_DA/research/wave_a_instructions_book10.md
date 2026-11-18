# Wave A instructions — Book 10 (Domain Knowledge for Data Analysts) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 10. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9, Book 10 table), `style_guide.md` (Sections 2, 3, 7, 8, 10, 11), `research/interview_processes.md` (domain-flavoured rounds), `research/market_skills_2026.md` (domain knowledge, BFSI/e-commerce/healthcare/GCC mentions), the JD samples in `research/jd_sample_*.md` (grep your domain's words), and for format only the header of `Book08_Scenarios/Book08_Part09.md` and `research/index_rows/B8P09.md`. Do NOT copy their questions.

## Book 10 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Domain | Target |
|---|---|---|
| 1 | HR / People Analytics: headcount types, attrition, hiring funnel, engagement, DEI metrics, compensation, workforce planning, HRIS data and payroll basics, privacy of employee data. The switcher's strength: go deep | 120 |
| 2 | E-commerce & quick-commerce (orders, GMV, AOV, conversion, returns, delivery SLAs, dark stores, catalogue, marketplace, payments) | 90 |
| 3 | BFSI: banking, credit/lending, fintech/UPI, insurance, capital markets basics, risk, collections, KYC/fraud, regulation in plain words | 100 |
| 4 | Healthcare & pharma: hospital operations, claims, clinical trials, pharma sales, patient privacy, coding standards | 70 |
| 5 | Supply chain & operations: inventory, demand forecasting, logistics, warehouse, procurement, OTIF, lead time, S&OP | 70 |
| 6 | Marketing & sales analytics: funnel, campaigns, attribution, CRM, pipeline, segmentation, pricing/promotions | 80 |
| 7 | IT services / GCC reporting & MIS (utilisation, bench, billing, SLAs, project health), plus a Workday/HR-systems and Alteryx mini-section | 65 |
| 8 | How to learn a new domain fast (learning-journey interview questions and the skill-development scope) | 20 |

Boundaries (do NOT duplicate; grep `question_index.md` for these before finalising): Book 7 (Parts 4 and 8) already owns generic business-metric definitions (DAU/MAU, CAC, LTV, churn, retention, conversion, ARPU) and a first layer of HR metrics (attrition rate, time-to-hire, cost per hire, offer acceptance, funnel conversion, pay gap, compa-ratio) and HR cases; Book 8 owns scenarios (data quality, stakeholders, dashboards, metric-drop investigations); Books 1, 2, 3, 4 own tool how-to; Book 5 owns statistics; Book 6 owns aptitude. Book 10 is DOMAIN KNOWLEDGE: how the business works, its vocabulary, its data tables and sources, the metrics specific to the domain (go beyond the generic ones), typical analyses an analyst is asked, industry regulations and data-privacy awareness stated in plain words, and domain-flavoured analysis tasks and "what would you check" questions. Where a Book 7 or 8 question is close, ask the domain-specific angle (for example, how a hospital defines bed occupancy and what data feeds it) or skip it.

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred). Run at least 6 distinct searches for your domain, e.g. "<domain> data analyst interview questions 2025/2026", "<domain> analyst interview Hyderabad/Bengaluru", "<domain> KPIs metrics every analyst should know", "<domain> data analyst job description India", company-specific experiences. If WebSearch hits a rate limit, wait and retry with narrower queries; note blocked pages (Glassdoor/AmbitionBox/GfG/Reddit). Pages may not be fetchable: record snippet-only honestly.
2. Record every source in `research/Book10_PartNN_sources.md` in the format of `research/Book08_Part09_sources.md`: URL, use, type, recency, honest note whether fetched in full or snippet only. No invented sources or company claims; mark unverified; state sample size/limitations and your star reasoning.
3. If you cannot research (tools unavailable), STOP, write nothing, report why.

## Question rules
- Questions a real interviewer asks a 0-3 year data/business/MIS analyst applying to that domain. Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part or book.
- Stars ⭐⭐⭐/⭐⭐/⭐ from the research; difficulty 🟢🟡🔴. Sort: stars descending, then 🟢→🔴. Numbering Q1..Qn continuous.
- Target is a minimum; fill gaps. Mix: vocabulary and "how does this business work" (🟢), metric definition with a small inline-numbers calculation (🟡), "what data/tables would you need and what first cuts" tasks (🟡), regulation/privacy awareness in plain words (🟡), and a few domain case-style analysis questions (🔴). Include small inline data for calculation questions (as Books 7 and 8 do) so they are answerable in about 5 minutes.
- Reader is a non-technical HR career switcher: explain the domain from zero (assume no prior knowledge of banking, pharma etc.); include HR-flavoured connections where natural (for example, workforce metrics in a hospital).
- Regulated domains (BFSI, healthcare, HR data): questions may cover regulation and privacy only at awareness level in plain words; never ask for or imply legal, medical or financial advice. Real regulatory details will be labelled "from memory, unverified" at answer time.

## Files you write (only these)
1. `Book10_Domain/Book10_PartNN.md` (mkdir -p):
```
# Book 10 — Domain Knowledge | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer; inline data lines go directly under the heading line, before the marker).
2. `research/Book10_PartNN_sources.md`.
3. `research/index_rows/B10PNN.md`: rows `| B10PNNQn | 10 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B8P09.md`.
Touch no other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/A10_PartNN`. Do not commit or push.

## Final reply (short)
Files, actual count vs target, searches/fetches, blocked sources, gap-fill count, overlaps you avoided with Books 7 and 8, anything uncertain.
