---
name: ampba-llm-agents
description: Patterns for LLM, RAG and LangGraph multi-agent code in the ISB AMPBA case studies (CS2 audit copilot, CS3 agentic underwriting, CS10 review RAG). Mock-first, structured outputs, evaluation harness. Use whenever writing llm.py, agents, RAG index/retrieval or LLM evaluation.
---

# LLM / Agents / RAG patterns

## 1. Provider wrapper — `src/<PKG>/llm.py` (write first)
- `LLM_PROVIDER` env in {mock, groq, openai}; default **mock**. Load `.env` with python-dotenv.
- `complete(system, user, schema: type[BaseModel] | None = None) -> str | BaseModel`.
- Structured output: ask for JSON matching `schema.model_json_schema()`, parse with pydantic; on failure retry once with the validation error appended; then raise.
- Mock: deterministic — builds a valid schema instance from inputs (e.g. extracts numbers/ids from the prompt context) so the whole pipeline and tests run offline.
- Retries: 3× exponential backoff; timeout 60s; log provider, model, tokens, latency, cost estimate to `outputs/llm_usage.csv`.
- Defaults: groq `llama-3.3-70b-versatile`, openai `gpt-4o-mini` (override via env GROQ_MODEL / OPENAI_MODEL).
- Prompts live in `prompts/*.md` (versioned), loaded by name — never inline long prompts.

## 2. LangGraph agents
- State = one pydantic model (`state.py`); each node is a pure function `node(state) -> dict` (partial update).
- One file per agent under `agents/`; each agent has a unit test with fixture state and mock LLM.
- Conditional edges for human-in-the-loop (REFER) and errors; max 1 self-correction loop per node.
- Tools: typed functions; SQL tools are read-only (reject regex `\b(insert|update|delete|drop|alter|create|attach|copy)\b`, case-insensitive), row cap 500.
- Persist a trace per run (`outputs/traces/<run_id>.json`): node, inputs summary, outputs, latency.

## 3. RAG
- Chunk by natural unit (one review / one policy clause); keep metadata ids.
- Embeddings `BAAI/bge-small-en-v1.5` (sentence-transformers, CPU OK); FAISS (or Chroma) persisted under `data/index/`.
- Retrieval: hybrid BM25 (rank_bm25) + dense, reciprocal-rank fusion; optional reranker `BAAI/bge-reranker-base`.
- Answers must cite ids like `[R123]`; post-check: every cited id is in retrieved set, else drop/regenerate.
- Grounding check node: for each claim sentence, verify support in retrieved text (LLM-judge or token overlap in mock).

## 4. Evaluation harness — `evaluation/harness.py`
- Fixed test set (`data/gold/*.jsonl`), versioned; run all configs; output `outputs/eval_<config>.json` and a comparison table.
- Metrics: task accuracy vs gold, faithfulness, answer relevancy, citation precision, hallucinated-number rate (every number in output must exist in inputs/state), latency p50/p95, cost per item.
- Run in mock mode in CI; real-provider runs are manual (`python -m evaluation.harness --provider groq`) and results committed.

## 5. Safety & privacy
- Scrub PII (emails, phones, PAN/Aadhaar-like patterns) before sending to providers.
- Never log API keys; `.env` gitignored; `.env.example` committed.
