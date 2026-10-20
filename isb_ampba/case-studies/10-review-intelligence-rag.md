# Case Study 10 — Review Intelligence: Aspect Sentiment + RAG Copilot (E-commerce GenAI / NLP)

**Reference repos:** [R16 RishabhBansal2409/Sentiment_Analysis_of_Customer_Reviews](https://github.com/RishabhBansal2409/Sentiment_Analysis_of_Customer_Reviews) (scrape + sentiment + Shiny) · [R18 RishabhBansal2409/Natural_Language_Processing__Chatbot](https://github.com/RishabhBansal2409/Natural_Language_Processing__Chatbot) (intent bot) · [R6 anmolisb/Escalant_SurveyProgramming](https://github.com/anmolisb/Escalant_SurveyProgramming) (LangGraph agents + evaluation harness, ISB AMPBA 2026S). ISB capstone theme: "Auto-classification of Products into Categories".

### 10.1 Business problem
Product & CX teams can't read 100k+ reviews. Build: (a) aspect-based sentiment (battery, delivery, quality, price, packaging…), (b) emerging-issue alerts, (c) a grounded RAG copilot answering "Why are 2-star reviews rising for SKU X?" with citations.

- **KPIs:** sentiment macro-F1 ≥ 0.80 (3-class); aspect extraction F1 ≥ 0.70 on 300 hand/LLM-labelled reviews; RAG faithfulness ≥ 0.85 & answer relevancy ≥ 0.80 (RAGAS or own LLM-judge); p95 latency < 5 s.

### 10.2 Data
- HuggingFace `McAuley-Lab/Amazon-Reviews-2023` — https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 — use categories `Electronics` or `Cell_Phones_and_Accessories`; sample 100k reviews + item metadata (`raw_review_*`, `raw_meta_*` configs, `trust_remote_code=True`). Fallback: Flipkart product reviews CSV placed in `data/raw/` by the user.
- Labels: star rating → sentiment (1–2 neg, 3 neu, 4–5 pos); aspect gold set: 300 reviews labelled via LLM then human-verified (store in `data/gold/aspects.jsonl`).

### 10.3 Modules (`PKG=revai`)
```
src/revai/
  data.py         load sample, clean, language filter, dedupe, PII scrub (emails/phones regex)
  sentiment.py    baselines TF-IDF+LogReg, VADER; transformer fine-tune (distilbert-base-uncased, 2 epochs, HF Trainer);
                  report macro-F1, confusion matrix
  aspects.py      aspect taxonomy per category (config); (a) zero-shot NLI (facebook/bart-large-mnli) or
                  (b) LLM structured extraction -> [{aspect, sentiment, span}]; evaluate on gold
  topics.py       BERTopic on negative reviews; monthly topic trends
  alerts.py       emerging issue = aspect-negative share z-score > 3 vs trailing 8 weeks per SKU
  classify.py     product auto-categorisation from title+description (embeddings + LogReg) — ISB capstone theme
  rag/
    index.py      chunk reviews (by review) + metadata (asin, rating, date); embeddings bge-small-en-v1.5; FAISS or Chroma
    retrieve.py   hybrid BM25 + dense, metadata filters (asin, date range, rating), rerank (bge-reranker-base, optional)
    graph.py      LangGraph: route(question) -> {sql_stats tool over DuckDB aggregates | rag_retrieve} -> answer with [review_id] citations
                  -> self-check node (claims supported by retrieved text?) -> final
    eval.py       50-question test set (auto-generated + curated) -> faithfulness, relevancy, citation precision
  api.py          FastAPI /ask, /aspects/{asin}, /alerts
app/streamlit_app.py  SKU dashboard (aspect sentiment bars, trend lines, alerts), review explorer, copilot chat with citations
```

### 10.4 Method
1. Sample & clean; EDA (rating distribution, length, verified purchase).
2. Sentiment baselines → transformer; error analysis on neutral class.
3. Aspect extraction + evaluation; aspect × month heatmaps.
4. BERTopic + alerting backtest (did alerts precede rating drops?).
5. RAG build + evaluation harness; compare dense vs hybrid vs hybrid+rerank.
6. Cost/latency table per LLM provider; mock mode for tests.

### 10.5 Acceptance criteria
- [ ] Transformer beats TF-IDF baseline on macro-F1.
- [ ] RAG eval table for 3 retrieval configs; every answer has ≥ 1 valid citation.
- [ ] Pipeline runs on 20k sample in < 15 min on CPU (flag `--full` for 100k / GPU).
- [ ] Memo: top 5 issues for chosen category with ₹/rating impact estimate.

### 10.6 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 10 "Review Intelligence: Aspect Sentiment + RAG Copilot" per spec. PKG=revai.
Data: HF McAuley-Lab/Amazon-Reviews-2023 (Electronics sample). LLM_PROVIDER=mock default.
Extend github.com/RishabhBansal2409/Sentiment_Analysis_of_Customer_Reviews; use LangGraph + eval-harness discipline of
github.com/anmolisb/Escalant_SurveyProgramming. Milestones: M1 data+sentiment, M2 aspects+topics+alerts,
M3 RAG index+graph, M4 RAG eval, M5 API/app/memo/CI.
[PASTE SECTION 10.1–10.5 HERE]
```
