# CLAUDE.md — AMPBA project conventions

## Stack
- Python 3.11; pandas, numpy, scikit-learn, xgboost, lightgbm, shap, statsmodels,
  scipy, pulp (HiGHS), matplotlib, plotly, streamlit, fastapi, pydantic, pytest, ruff.
- LLM work: langchain-core / langgraph; provider via env var LLM_PROVIDER in {groq, openai, mock}.
  Default = mock (deterministic, offline) so everything runs without API keys.
- Data access: ucimlrepo, yfinance, datasets (HuggingFace). Cache raw downloads in data/raw/.

## Repo layout (mandatory)
.
├── CLAUDE.md
├── README.md                # problem, data, method, results table, how to run, limits
├── Makefile                 # setup, data, train, evaluate, app, test, all
├── requirements.txt         # pinned versions
├── Dockerfile
├── .github/workflows/ci.yml # ruff + pytest on push
├── config/config.yaml       # all paths, seeds, hyper-params, business assumptions
├── data/{raw,interim,processed}/   (gitignored except small samples)
├── notebooks/               # 01_eda, 02_features, 03_models (thin; call src/)
├── src/<package>/           # all logic; notebooks import from here
├── analysis/run_analysis.py # regenerates every figure + outputs/summary.json
├── outputs/                 # csv, summary.json, metrics.json
├── figures/                 # png charts referenced by README/memo
├── models/                  # serialized models (joblib)
├── app/                     # streamlit_app.py (and api.py if FastAPI)
├── tests/                   # pytest; unit + one end-to-end smoke test
└── docs/                    # PROBLEM_STATEMENT.md, DECISION_MEMO.md, MODEL_CARD.md

## Rules
1. Seed everything (config.seed = 42). Results must be reproducible.
2. No logic in notebooks; notebooks only call src functions.
3. Every function: type hints + docstring. Use logging, not print.
4. Validate data with explicit asserts/pandera schema in src/<pkg>/validate.py.
5. Time-based or group-based splits where leakage is possible; never random-split time series.
6. Always report a naive baseline next to the model.
7. Translate model metrics into a business metric (₹ / % / hours saved) in DECISION_MEMO.md.
8. Business assumptions live in config.yaml and are swept in a sensitivity analysis.
9. `make all` must run end-to-end on a laptop in < 15 minutes (use sampling flags if needed).
10. Tests: >= 10 unit tests; tests must run offline (use fixtures/ synthetic data, LLM mock).
11. Write MODEL_CARD.md: intended use, data, metrics, fairness check, limitations.
12. After each milestone: run `make test`, update README results table, commit.

## Windows / OneDrive notes
- This workspace lives on Windows (OneDrive). `make` may be missing: always also create `tasks.py`
  with the same targets (`python tasks.py setup|data|train|evaluate|app|test|lint|all`).
- Use a local venv: `python -m venv .venv` then `.venv\Scripts\activate` (PowerShell) or `source .venv/Scripts/activate` (Git Bash).
- Never write large data/models into OneDrive-synced git history: keep `data/raw`, `data/processed`, `models/`, `.venv/` in .gitignore.
- Use pathlib for all paths; no hard-coded `/` or `\` separators.
