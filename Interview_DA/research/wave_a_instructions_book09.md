# Wave A instructions — Book 9 (Basic ML + AI Tools for Analysts) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 9. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9, Book 9 table), `style_guide.md` (Sections 2, 3, 7, 8, 10, 11), `research/interview_processes.md` (ML/stats/AI rounds at Tiger Analytics, Fractal, Mu Sigma, LatentView, Indium, Flipkart, Meesho, Swiggy and others), `research/market_skills_2026.md` (AI tools named in about 20% of the JD sample; ML much rarer for 0-3 year analyst roles), and for format only the header of `Book08_Scenarios/Book08_Part09.md` and `research/index_rows/B8P09.md` (do not copy questions).

## Book 9 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | What ML is; supervised vs unsupervised; when analysts use it 🟢 | 76 |
| 2 | Linear and logistic regression (intuition + sklearn) 🟢🟡 | 85 |
| 3 | Decision trees, random forest (intuition) 🟡 | 38 |
| 4 | Clustering and customer segmentation (k-means, RFM) 🟡 | 60 |
| 5 | Model evaluation: accuracy, precision, recall, confusion matrix, RMSE 🟡 | 80 |
| 6 | Overfitting, train/test split, feature engineering basics 🟡 | 38 |
| 7 | Forecasting basics (moving average, trend, seasonality) 🟡 | 38 |
| 8 | Attrition prediction and churn mini-projects (HR-friendly) 🟡🔴 | 30 |
| 9 | GenAI for analysts: ChatGPT/Claude/Copilot for SQL and analysis, prompt basics, verifying AI output 🟢 | 100 |
| 10 | LLM/RAG basics (emerging; only one interview report, so stars at the low end) | 20 |
| 11 | Cloud basics for analysts (AWS/Azure/GCP, Snowflake, BigQuery, Fabric); low frequency, stars at the low end | 15 |
| 12 | How to develop ML/AI skills (learning-journey interview questions plus skill-development scope, like other books' final parts) | 20 |

Boundaries (do not duplicate): Book 5 owns statistics theory, hypothesis testing, A/B testing, correlation/regression interpretation basics and R-squared (Part 2 here is the ML angle: fitting with sklearn, coefficients as an analyst explains them, predicting, classification with logistic regression, the model-vs-explanation distinction; do not repeat Book 5 Part 7 question wording). Book 3 owns pandas/NumPy/plotting mechanics (here pandas appears only as data preparation for a model). Book 2/4 own SQL and Power BI (Part 9 here covers using AI tools to help with them; the SQL/DAX mechanics themselves are theirs). Book 7 owns business cases and metrics definitions (Part 8 here is a model-building mini-project, not a metric-drop case). Book 10 owns domain content. Part 12 is the skill-development part.

## Question format
Interviewer-style questions for a 0-3 year analyst (not an ML engineer): concept ("explain overfitting to a manager"), difference ("precision vs recall"), practical calculation with inline data (confusion matrix numbers, RMSE/MAE from a small table, k-means one step, a decision-tree split, a moving average, RFM scoring), code-reading or "what would you do" prompts, and (Parts 8, 9) mini-project and AI-workflow scenarios. Where a question has data, put it inline under the heading so a single figure can be derived; never state real-world statistics as facts. Include sklearn/statsmodels questions that are answerable with short interview code (Parts 1, 2, 3, 4, 5, 6, 8). HR flavour (attrition, hiring funnel, payroll, attendance, engagement) where natural, plus sales, e-commerce and finance.
Aim for roughly 25-40% of Parts 2, 3, 4, 5, 6, 7, 8 as questions with inline data or a short code task.

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred; WebFetch is unavailable). Run at least 6 distinct searches for your topic, e.g. "<topic> interview questions data analyst", "<topic> machine learning basics interview questions fresher analyst India", company-specific experiences (Tiger Analytics, Fractal, Mu Sigma, Flipkart...), "<topic> 2025 2026". Glassdoor/AmbitionBox/Reddit/LinkedIn may be blocked; record that.
2. Record every source in `research/Book09_PartNN_sources.md` in the format of `research/Book08_Part09_sources.md`: URL, what it was used for, type, recency, honest note that it was only a search snippet. No invented sources or company claims; mark unverified items. State sample size and limitations. Give your star-assignment reasoning (stars judgement unless a source gives frequency).
3. If you cannot research (tools unavailable), STOP, write nothing, and report why.

## Question rules
- Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part.
- Stars: ⭐⭐⭐ appears in most DA interviews that touch ML/AI, ⭐⭐ often, ⭐ occasional/differentiator/emerging; difficulty 🟢🟡🔴. Sort: ⭐⭐⭐ then ⭐⭐ then ⭐; inside the same star 🟢 then 🟡 then 🔴. Numbering Q1..Qn continuous.
- Target is a minimum; add important missing question types (common misconceptions, "explain to a non-technical manager", leakage, class imbalance, data privacy in AI use).

## Files you write (only these)
1. `Book09_ML_AI_Tools/Book09_PartNN.md` (mkdir -p):
```
# Book 9 — Basic ML + AI Tools for Analysts | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
(inline data lines, if any)
<!-- ANSWER_PENDING -->
```
(no footer).
2. `research/Book09_PartNN_sources.md`.
3. `research/index_rows/B9PNN.md`: rows `| B9PNNQn | 9 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B8P09.md`.
Do not touch any other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/A9_PartNN` (yours only). Do not commit or push.

## Final reply (short)
Files, actual count vs target, number of searches, which sources were blocked, how many questions are gap-fills, anything uncertain.
