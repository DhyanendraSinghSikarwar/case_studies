# PLAN.md — Data Science / ML Interview Book Series

Target: ₹30–80 LPA roles (India MNCs, product companies, GCCs) + Europe, USA, Canada, SEA.
Updated for the post-GenAI hiring pattern (2025–2026).

---

## 1. Goals

| Goal | Measure |
|---|---|
| Cover what is actually asked | Each book ≥ 500 Qs (Books 7–9 are guides, not Q-counts) |
| Rank by frequency | Every Q marked ⭐⭐⭐ / ⭐⭐ / ⭐ |
| Interview-ready answers | Concise answer + code where relevant + follow-ups |
| Current | Reflect AI-era changes (LLM rounds, code review, AI-tool use) |
| Usable for revision | Fixed template, consistent numbering, one topic per part |

---

## 2. Book List & Output Files

| # | Book | Folder / file prefix | Parts | Q target |
|---|---|---|---|---|
| 1 | DS / ML Engineer Technical | `01_DS_ML_PartNN.md` | 14 | 620 (incl. +100 statistics) |
| 2 | GenAI / LLM / RAG / Agentic AI + Deployment | `02_GenAI_PartNN.md` | 12 | 520–600 |
| 3 | SQL (scenario-based) + pandas equivalents | `03_SQL_PartNN.md` | 12 | 500–600 |
| 4 | MLOps / Docker / DVC / CI-CD / AWS & cloud | `04_MLOps_PartNN.md` | 12 | 500–600 |
| 5 | DSA in Python (product companies) | `05_DSA_PartNN.md` | 14 | 600 (incl. +100) |
| 6 | Scenario-based interview questions | `06_Scenarios_PartNN.md` | 10 | 500–600 |
| 7 | Company-wise interview processes | `07_Companies_PartNN.md` | 4 | ~40 companies |
| 8 | Region-wise processes vs India | `08_Regions_PartNN.md` | 3 | ~12 countries/regions |
| 9 | Soft skills, scenarios & skill-improvement playbooks | `09_SoftSkills_PartNN.md` | 5 | 210+ Qs/scenarios + 12 playbooks |

Total: ~86 part-files, ~3,900–4,300 Q&As plus guides.

**Rules:**
- Q targets are **minimums**. Any book/part may grow (up to ~600 per book, more for Books 1 & 5) if important questions remain.
- Answers are written **as you would say them in the interview**: plain language, short, structured, no jargon without explanation.
- Answer shape: 1-line direct answer → 2–5 supporting points → example/code → likely follow-up.
- Every question **must** include a full answer (plus code where practical). No question-only lists.

**Save location (local):**
```
C:\Users\11624\OneDrive - Indian School of Business\Documents\personal\bus_2_ml_case_study\interviews
```

---

## 3. Star Rating Criteria

| Rating | Rule used |
|---|---|
| ⭐⭐⭐ | Appears in most loops at this level; skipping it is risky |
| ⭐⭐ | Appears regularly; expected for strong candidates |
| ⭐ | Senior/niche/differentiator; asked at specific companies or roles |

Ordering inside each part: ⭐⭐⭐ → ⭐⭐ → ⭐.
Difficulty tag (where relevant, Books 3 & 5): 🟢 Easy / 🟡 Medium / 🔴 Hard.

---

## 4. Standard Answer Template (all Q&A books)

```
### Q<n> ⭐⭐⭐ 🟡 <Question>
**Asked at:** <company types, e.g., product / fintech / GCC>
**Say this first (1 line):** direct answer in plain words
**Then explain:**
- 2–5 key points (bullets/table), simple language
**Example:** real-world or numeric example
**Code:** (if practical)
**Follow-ups:** 1–3 likely follow-up questions with short answers
**Common mistakes:** what candidates get wrong
```

Book-specific additions:
| Book | Extra fields |
|---|---|
| 3 SQL | Schema + sample data, SQL answer, **pandas answer**, edge cases (NULLs, ties, duplicates) |
| 5 DSA | Pattern name, brute force → optimal, time/space complexity, dry run |
| 6 Scenarios | Clarifying questions → approach → metrics → risks → what interviewer scores |
| 2 & 4 | Architecture diagram (Mermaid) where useful, cost/latency trade-offs |

---

## 5. Detailed Content Plan per Book

### Book 1 — DS / ML Technical (14 parts)
| Part | Topic | Qs |
|---|---|---|
| 1 | Stats, probability, ML fundamentals, from-scratch code | 30 ✅ |
| 2 | Linear/logistic regression, regularization, feature engineering | 45 |
| 3 | Classification metrics, imbalance, calibration, thresholding | 45 |
| 4 | Trees, RF, boosting (XGBoost, LightGBM, CatBoost), SHAP | 45 |
| 5 | Clustering, PCA/UMAP, anomaly detection | 40 |
| 6 | Time series & forecasting (ARIMA, Prophet, GBM, DL) | 45 |
| 7 | Recommenders, ranking, search, learning-to-rank | 40 |
| 8 | Deep learning (backprop, optimizers, PyTorch from scratch) | 50 |
| 9 | NLP & CV (classical → transformers, embeddings) | 45 |
| 10 | A/B testing, causal inference, experimentation | 50 |
| 11 | ML system design (fraud, feed, ETA, pricing, churn) | 40 |
| 12 | NumPy/pandas/sklearn live-coding & AI-code-review rounds | 45 |
| 13 | **Statistics deep dive I**: distributions, sampling, estimators, CLT/LLN, CIs, hypothesis tests (t, z, χ², ANOVA, Mann–Whitney), power & sample size — with scipy/NumPy code | 50 |
| 14 | **Statistics deep dive II**: probability puzzles (dice, cards, coins, birthday, expected value), conditional probability & Bayes, Markov chains, regression diagnostics, Bayesian stats, sequential testing, CUPED, variance reduction, simulation-based answers | 50 |

### Book 2 — GenAI / LLM / RAG / Agentic AI (12 parts)
| Part | Topic | Qs |
|---|---|---|
| 1 | Transformer internals: attention, positional encoding, KV cache | 45 |
| 2 | Tokenization, pretraining, scaling laws, decoding strategies | 40 |
| 3 | Prompt engineering, structured outputs, function calling | 40 |
| 4 | Fine-tuning: SFT, LoRA/QLoRA, PEFT, distillation | 45 |
| 5 | Alignment: RLHF, DPO, safety, guardrails | 35 |
| 6 | RAG basics: chunking, embeddings, vector DBs, retrieval | 50 |
| 7 | Advanced RAG: hybrid search, reranking, GraphRAG, query rewriting | 45 |
| 8 | Agents: ReAct, tool use, planning, memory, MCP, multi-agent | 50 |
| 9 | LLM evaluation: RAGAS, LLM-as-judge, hallucination, benchmarks | 45 |
| 10 | Deployment: vLLM, TGI, quantization, batching, latency/cost | 45 |
| 11 | LLMOps: monitoring, tracing, prompt versioning, security (prompt injection) | 40 |
| 12 | GenAI system design + coding (build mini-RAG/agent from scratch) | 40 |

### Book 3 — SQL + pandas (12 parts, Easy → Hard)
| Part | Topic | Qs |
|---|---|---|
| 1 | SELECT, filtering, aggregation, GROUP BY/HAVING 🟢 | 45 |
| 2 | Joins (all types, self, anti/semi joins) 🟢🟡 | 45 |
| 3 | Subqueries, CTEs 🟡 | 40 |
| 4 | Window functions: ranking, top-N per group 🟡 | 50 |
| 5 | Window functions: running totals, LAG/LEAD, moving avg 🟡 | 45 |
| 6 | Date/time: retention, cohorts, MoM/YoY 🟡🔴 | 45 |
| 7 | Gaps & islands, streaks, sessionization 🔴 | 40 |
| 8 | Funnels, conversion, DAU/MAU, product metrics 🟡🔴 | 45 |
| 9 | Recursive CTEs, hierarchies, graphs 🔴 | 30 |
| 10 | Pivot/unpivot, string ops, NULL traps 🟡 | 40 |
| 11 | Query optimization, indexes, execution plans, partitioning 🔴 | 35 |
| 12 | Company-style mixed mock sets (FAANG, fintech, e-com) 🔴 | 40 |
Every SQL answer paired with equivalent **pandas** code.

### Book 4 — MLOps / Productionization (12 parts)
| Part | Topic | Qs |
|---|---|---|
| 1 | Git, code quality, packaging, testing ML code | 40 |
| 2 | Docker (images, layers, multi-stage, GPU) | 45 |
| 3 | Kubernetes basics for ML, Helm, autoscaling | 40 |
| 4 | Data & model versioning: DVC, MLflow, W&B | 40 |
| 5 | Pipelines/orchestration: Airflow, Kubeflow, Prefect | 40 |
| 6 | Serving: FastAPI, batch vs real-time, Triton, BentoML | 45 |
| 7 | CI/CD for ML, GitHub Actions, model registry | 40 |
| 8 | Monitoring: drift, data quality, alerting, retraining | 45 |
| 9 | Feature stores, streaming (Kafka, Spark) | 35 |
| 10 | AWS: S3, EC2, Lambda, SageMaker, ECR/ECS, IAM | 50 |
| 11 | Azure ML & GCP Vertex AI (comparison) | 35 |
| 12 | Cost, scaling, security, MLOps system design | 45 |

### Book 5 — DSA in Python (14 parts)
| Part | Pattern | Qs |
|---|---|---|
| 1 | Arrays & hashing | 50 |
| 2 | Two pointers & sliding window | 45 |
| 3 | Strings | 40 |
| 4 | Stack, queue, monotonic stack | 40 |
| 5 | Binary search (incl. on answer) | 40 |
| 6 | Linked lists | 35 |
| 7 | Trees & BST | 50 |
| 8 | Heaps, intervals, greedy | 45 |
| 9 | Graphs (BFS/DFS, topo sort, Dijkstra, union-find) | 45 |
| 10 | Dynamic programming I (1D, knapsack) | 40 |
| 11 | Dynamic programming II (2D, strings, intervals) | 35 |
| 12 | Backtracking, tries, bit manipulation, DS-flavoured DSA | 35 |
| 13 | **Extra I**: prefix sums, matrices/2D grids, math & number theory, randomized algorithms, sorting internals (quick/merge/counting sort from scratch) | 50 |
| 14 | **Extra II**: design problems (LRU/LFU cache, rate limiter, iterator, hit counter), advanced graphs (MST, bipartite, SCC), segment/Fenwick trees, mixed company mock sets | 50 |

### Book 6 — Scenario-Based (10 parts)
| Part | Topic | Qs |
|---|---|---|
| 1 | Product metrics & metric drops ("DAU fell 10%") | 55 |
| 2 | Model performance degraded in production | 50 |
| 3 | Imbalanced / noisy / missing data situations | 50 |
| 4 | Experiment design & ambiguous A/B results | 55 |
| 5 | Business case studies (pricing, churn, fraud, supply chain) | 55 |
| 6 | Stakeholder conflicts & trade-off decisions | 45 |
| 7 | GenAI scenarios (hallucinations, cost, latency, eval) | 55 |
| 8 | MLOps incidents (pipeline failures, rollback, drift) | 45 |
| 9 | Domain sets: fintech, e-commerce, healthcare, ads | 50 |
| 10 | "Design a solution end-to-end" open scenarios | 40 |

### Book 7 — Company Interview Processes (4 parts, researched live)
| Part | Coverage |
|---|---|
| 1 | Big Tech: Google, Microsoft, Amazon, Meta, Apple, Netflix, Uber, LinkedIn, Adobe, Salesforce |
| 2 | Indian product/unicorns: Flipkart, Swiggy, Zomato, PhonePe, Razorpay, CRED, Meesho, Ola, Paytm, Myntra |
| 3 | GCCs/MNCs in India: Walmart, Target, JPMorgan, Goldman Sachs, American Express, Visa, Mastercard, Intuit, Atlassian, Optum |
| 4 | Europe/global: Spotify, Zalando, Booking.com, Klarna, SAP, Delivery Hero, Revolut, Wise, Grab, Shopee |
Per company: rounds, duration, question types, sample questions, what they score, level/salary band, preparation tips.

### Book 8 — Region-wise Processes (3 parts, researched live)
| Part | Coverage |
|---|---|
| 1 | Europe: Sweden, Germany, Netherlands, Ireland, UK, Switzerland |
| 2 | North America: USA, Canada |
| 3 | SEA/Middle East: Singapore, Malaysia, Indonesia, UAE + India comparison & relocation guide |
Per region: rounds, take-home vs live coding, culture fit style, visa/work-permit route, salary norms, CV format, how Indians differ, how to use Books 1–6 for that market.

### Book 9 — Soft Skills (5 parts)
| Part | Coverage |
|---|---|
| 1 | What companies expect by level (SDE-DS II → Staff); STAR/CARL framework; 50 behavioural Qs with sample answers |
| 2 | Communication: explaining models to non-tech, storytelling with data, stakeholder management; 50 Qs |
| 3 | Leadership principles (Amazon LPs, Google "Googleyness"), negotiation, salary talks, HR round; 50 Qs + scripts |
| 4 | Soft-skill scenarios: 60+ workplace/interview situations with weak vs strong responses and what the interviewer scores |
| 5 | Skill-improvement playbooks: how to improve each skill, step by step |

**Part 4 — Scenario coverage (each with: situation → weak answer → strong answer → why it works):**
| Category | Example scenarios |
|---|---|
| Stakeholder conflict | PM wants a launch date your model can't meet; business rejects your findings |
| Ambiguity | Vague problem statement; no labelled data; shifting requirements |
| Failure & ownership | Model failed in production; you shipped a bug; missed deadline |
| Influence without authority | Convincing engineering to adopt your pipeline; pushing back on a senior |
| Team dynamics | Underperforming teammate; credit taken by others; cross-timezone friction |
| Ethics & judgement | Biased model; data privacy concern; pressure to inflate metrics |
| Communication | Explaining a drop in accuracy to a CXO; presenting uncertainty |
| Interview-room situations | Blanking on a question; disagreeing with interviewer; "any questions for us?" |
| Remote / global teams | Working with EU/US managers; async communication; cultural directness |

**Part 5 — Skill-improvement playbooks (each skill: what "good" looks like → self-assessment → daily/weekly practice → 30-day plan → resources → how to show it in interviews):**
| Skill | Practice examples |
|---|---|
| Structured communication | Pyramid principle, 1-minute summaries, record & review |
| Data storytelling | Rewrite one analysis per week as a 5-slide narrative |
| Stakeholder management | Stakeholder mapping, expectation-setting templates |
| Business acumen | Read earnings calls, map metrics to P&L, case drills |
| Influencing & negotiation | Pre-wiring decisions, BATNA practice, salary scripts |
| Presentation & public speaking | Meetups, internal demos, filler-word reduction drills |
| Written communication | Design docs, PR descriptions, executive emails |
| Ownership & prioritisation | Impact/effort matrix, weekly written updates |
| Handling feedback | Feedback logs, follow-up loops |
| Cross-cultural communication | EU/US directness norms, meeting etiquette, async writing |
| Mentoring & leadership | Pairing, code-review coaching, leading small initiatives |
| Composure under pressure | Mock interviews, think-aloud practice, recovery phrases |

---

## 6. How Content Is Created (method)

| Step | Action |
|---|---|
| 1 | Pick book + part from the tables above |
| 2 | List questions from known interview pools (Glassdoor, LeetCode Discuss, Blind, AmbitionBox, GfG experiences, public company guides) |
| 3 | Rank by frequency → assign stars; order ⭐⭐⭐ first |
| 4 | Write answers using the template; add tested Python/SQL/pandas code |
| 5 | Add AI-era twist where applicable (code review of LLM output, GenAI follow-ups) |
| 6 | For Books 7–8: run web searches per company/region and cite sources |
| 7 | Save as `.md`, update status table in this plan |

---

## 7. AI-Era Changes Applied Across Books

| Change | Where reflected |
|---|---|
| AI-generated code review / debugging rounds | Books 1, 3, 5 (final parts) |
| GenAI questions inside classical DS loops | Book 1 Part 9, Book 6 Part 7 |
| More system design at ₹40 LPA+ | Book 1 Part 11, Book 2 Part 12, Book 4 Part 12 |
| Take-home with LLM allowed, deep follow-up on choices | Books 6, 7 |
| Evaluation & cost-awareness emphasis | Book 2 Parts 9–10 |
| AI-assisted cheating checks → live explanation focus | Book 9 |

---

## 8. Suggested Study Schedule (12 weeks)

| Week | Focus |
|---|---|
| 1–2 | Book 1 Parts 1–4 + 13 (statistics I), Book 3 Parts 1–3, Book 5 Parts 1–2 |
| 3–4 | Book 1 Parts 5–8 + 14 (statistics II), Book 3 Parts 4–6, Book 5 Parts 3–5 |
| 5–6 | Book 2 Parts 1–6, Book 3 Parts 7–9, Book 5 Parts 6–8 |
| 7–8 | Book 2 Parts 7–12, Book 4 Parts 1–6, Book 5 Parts 9–10 |
| 9–10 | Book 4 Parts 7–12, Book 1 Parts 9–12, Book 5 Parts 11–14 |
| 11 | Book 6 (all), Book 3 Parts 10–12 |
| 12 | Books 7, 8, 9 (incl. soft-skill scenarios & playbooks — start playbooks from Week 1, 15 min/day) + mocks |

Daily split: 40% coding (DSA/SQL), 35% ML/GenAI theory + design, 25% scenarios/behavioural.

---

## 9. Request Workflow

| You say | I deliver |
|---|---|
| `Book 1 Part 2` | That part as one `.md` file |
| `Book 7 Part 1` | Researched part with sources |
| `revise Book X Part Y` | Updated version of that file |

---

## 10. Progress Tracker

| Book | Parts done |
|---|---|
| 1 | 14 / 14 (Questions ✅ Answers ✅ Review ✅; 728 Qs, see review_Book1.md) |
| 2 | 10 / 12 (Part 1: 47 Qs; Part 2: 44 Qs; Part 3: 44 Qs; Part 4: 47 Qs; Part 5: 41 Qs; Part 6: 53 Qs; Part 7: 50 Qs; Part 8: 52 Qs; Part 9: 46 Qs; Part 10: 49 Qs; Questions ✅ Answers ✅ Review ✅; see review_notes/Book2_PartNN_review.md) |
| 3 | 0 / 12 |
| 4 | 0 / 12 |
| 5 | 0 / 14 |
| 6 | 0 / 10 |
| 7 | 0 / 4 |
| 8 | 0 / 3 |
| 9 | 0 / 5 |

---

## 11. Execution Workflow (how each book is produced)

### 11.1 Two-phase process per part
| Phase | Output | Rule |
|---|---|---|
| Phase 1: Research & question list | `BB_Name_PartNN.md` with questions only, ordered ⭐⭐⭐ → ⭐ | Every question comes from research, not memory alone |
| Phase 2: Answers | Same file, edited in place: answer written directly under each question | Interview-style answer per Section 4 template |

### 11.2 Phase 1 — Research steps
| Step | Action |
|---|---|
| 1 | Search the web for the part's topic: "<topic> interview questions data scientist 2025/2026", Glassdoor/AmbitionBox experiences, LeetCode Discuss, Blind, GfG interview experiences, company engineering blogs |
| 2 | Collect candidate questions into a raw list; merge duplicates/rewordings |
| 3 | Assign frequency: count how many independent sources/experiences mention it → ⭐⭐⭐ (many), ⭐⭐ (several), ⭐ (few/senior) |
| 4 | Add AI-era questions (LLM code review, GenAI follow-ups) where relevant |
| 5 | Sort ⭐⭐⭐ → ⭐⭐ → ⭐; number Q1…Qn; add `Asked at` tag |
| 6 | Save file with questions + empty `**Answer:**` placeholders |
| 7 | Gap check against the plan's topic list; add missing important questions |

### 11.3 Phase 2 — Answer steps
| Step | Action |
|---|---|
| 1 | Open the Phase 1 file; answer questions in order |
| 2 | Replace each placeholder with: 1-line spoken answer → 2–5 points → example → code (if practical) → follow-ups → common mistakes |
| 3 | Run/verify every code snippet (Python, SQL via SQLite/DuckDB, pandas) before inserting |
| 4 | Keep language simple; explain any jargon in one line |
| 5 | Self-review: correctness, no duplicates, star order intact |
| 6 | Update Progress Tracker (Section 10) |

### 11.4 Multi-agent setup (for tools that support sub-agents, e.g., Claude Code / Cowork)
| Agent set | Role | Parallelism |
|---|---|---|
| Research agents (Set A) | One agent per part: web research → Phase 1 question file | Run all parts of a book in parallel |
| Reviewer agent | Deduplicate across parts, check star ordering, fill gaps | After Set A finishes |
| Answer agents (Set B) | One agent per part: edit Phase 1 file in place, write answers | Run in parallel after review |
| Code-verifier agent | Execute all code blocks, fix failures | After Set B |
| Final editor | Consistency of tone/format, update tracker | Last |

**Sample orchestration prompt (copy into an agent-capable tool):**
```
Read plan.md. For Book <N>, spawn one research sub-agent per part listed in Section 5.
Each sub-agent: follow Section 11.2, write /interviews/<NN>_<Name>_PartXX.md with questions only (ordered ⭐⭐⭐→⭐, with empty Answer placeholders).
When all finish, run a reviewer sub-agent to dedupe across parts and fill gaps.
Then spawn one answer sub-agent per part: follow Section 11.3, edit each file in place, writing interview-style answers directly under each question.
Then run a code-verifier sub-agent to execute and fix all code blocks.
Finally update the Progress Tracker in plan.md.
```

### 11.5 In this chat (claude.ai)
- No parallel sub-agents here: parts are produced one at a time, same two phases.
- One request = one part (research → questions → answers in the same file).
- Request format:
```
Book <N> Part <M>
```

### 11.6 Order of production
Book 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9; within each book, Part 1 → last part.

---

## 11. Execution Workflow (How to Build Each Book)

Instruction being executed:
> Write the content of these books according to this plan, most frequently asked → least frequently asked for each topic. Start from Book 1. Research the internet for each topic, write the question list in an `.md` file, then answer every question (as expected by the interviewer) directly below it.

### 11.1 Order of Work
| Order | Rule |
|---|---|
| Books | 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 |
| Parts | Part 1 → last part within each book |
| Phases per part | Research → Question list → Answers → Review → Done |
| Gate | A part's answers start **only after** its question list is complete and frozen |

### 11.2 Phase 1 — Research (per part)
| Step | Action |
|---|---|
| 1 | Run web searches for the part topic + "interview questions" + role (data scientist / ML engineer) + year (2025, 2026) |
| 2 | Search company-specific sources: Glassdoor, AmbitionBox, LeetCode Discuss, Blind, GeeksforGeeks interview experiences, Medium/LinkedIn interview write-ups, company career pages |
| 3 | Search India-specific (Flipkart, Swiggy, PhonePe, GCCs) and Europe-specific (Spotify, Zalando, Booking, Klarna) experiences |
| 4 | Record each question with: source, company, frequency signal (how many sources mention it), recency |
| 5 | Note AI-era changes (new question types, dropped question types) |

Output: `research_notes/BookX_PartY_sources.md` (question → sources → frequency count).

### 11.3 Phase 2 — Question List (per part)
| Step | Action |
|---|---|
| 1 | Merge duplicates and near-duplicates into one canonical question |
| 2 | Assign stars by frequency: ⭐⭐⭐ (≥ many sources / most loops), ⭐⭐ (regular), ⭐ (niche/senior) |
| 3 | Add difficulty 🟢🟡🔴 where relevant (SQL, DSA, stats) |
| 4 | Sort: ⭐⭐⭐ → ⭐⭐ → ⭐; within same star, easy → hard |
| 5 | Check count vs target in Section 5; add important missing questions (cap ~600/book) |
| 6 | Write file `BookX_<Name>_PartY.md` with numbered questions and empty answer slots |

Question-list file format:
```
### Q12 ⭐⭐⭐ 🟡 <Question text>
**Asked at:** <companies / company types>
<!-- ANSWER_PENDING -->
```

### 11.4 Phase 3 — Answers (edit the same file)
| Step | Action |
|---|---|
| 1 | Open the frozen question-list file |
| 2 | Replace each `<!-- ANSWER_PENDING -->` with the full answer using the Section 4 template |
| 3 | Write as spoken in the interview: 1-line direct answer → simple points → example → code → follow-ups → common mistakes |
| 4 | Run all code (Python/SQL/pandas) in a sandbox before inserting |
| 5 | Never reorder or renumber questions during this phase |

### 11.5 Phase 4 — Review
| Check | Pass criteria |
|---|---|
| Completeness | Zero `ANSWER_PENDING` markers left |
| Accuracy | Formulas, complexities, and facts verified; code runs |
| Clarity | Each answer understandable without extra reading |
| Ordering | Stars descending; numbering continuous |
| Duplicates | No repeated questions across parts of the same book |
| Sources | Books 7–8 include citations |

Then update the Progress Tracker (Section 10).

### 11.6 Multi-Agent Setup (parallel work)
| Wave | Agents | Job | Input → Output |
|---|---|---|---|
| A — Research | 1 agent per part (e.g., 14 agents for Book 1) | Phase 1 + Phase 2 | Topic → question-list file with `ANSWER_PENDING` |
| B — Answer | 1 agent per part (can split a part into Q-ranges, e.g., Q1–25, Q26–50) | Phase 3 | Question-list file → same file, answered |
| C — Review | 1 reviewer agent per book | Phase 4 + cross-part duplicate check | All parts → fixes + tracker update |

Rules for agents:
- Wave B starts on a part only when Wave A for that part is done.
- Each agent edits **only its assigned file / Q-range** (avoids overwrite conflicts).
- Shared file `style_guide.md` = Section 3 (stars) + Section 4 (template) + answer-style rules; every agent reads it first.
- Shared file `question_index.md` = all canonical questions per book; Wave A agents check it to avoid cross-part duplicates.

Where to run agents:
| Environment | How |
|---|---|
| Claude Code / Cowork | Use subagents; one subagent per part or Q-range, running in parallel |
| Claude.ai chat | No parallel agents; run waves sequentially, one part per request (e.g., `Book 1 Part 2 – questions`, then `Book 1 Part 2 – answers`) |

### 11.7 Folder Structure
```
interviews/
├── plan.md
├── style_guide.md
├── question_index.md
├── research_notes/
│   └── Book1_Part02_sources.md
├── Book1_DS_ML/
│   ├── Book1_DS_ML_Part01.md
│   └── ...
├── Book2_GenAI/
├── Book3_SQL/
├── Book4_MLOps/
├── Book5_DSA/
├── Book6_Scenarios/
├── Book7_Companies/
├── Book8_Regions/
└── Book9_SoftSkills/
```

### 11.8 Request Commands (chat mode)
| Command | Result |
|---|---|
| `Book X Part Y – questions` | Research + frozen question list with `ANSWER_PENDING` |
| `Book X Part Y – answers` | Same file with all answers filled |
| `Book X Part Y – review` | Review report + corrected file |
| `Book X – review` | Cross-part duplicate/consistency check |

### 11.9 Definition of Done (per book)
- All parts have status: Questions ✅ / Answers ✅ / Review ✅
- Question count meets Section 5 target
- Zero pending markers; all code tested
- Progress Tracker updated
