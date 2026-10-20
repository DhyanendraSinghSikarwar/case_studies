# 00 — Common Setup (do this once, reuse for all 10 projects)

Every project plan (`projects/NN-slug/PLAN.md`) assumes you have done this page. It is written for a data scientist working by hand on Windows 11 + PowerShell. Nothing here needs an AI tool.

---

## 1. Tools to install (one time)

| Tool | Version | Check |
|---|---|---|
| Python | **3.11.x** (recommended; some packages — `implicit`, `lifetimes`, `hmmlearn`, `pyod` — publish wheels for 3.11 first) | `py -3.11 --version` |
| Git | 2.40+ | `git --version` |
| VS Code + Python + Jupyter extensions | latest | — |
| (optional) Docker Desktop | latest | `docker --version` |
| (optional) GitHub CLI | latest | `gh --version` |

If you only have Python 3.12 (`python --version`), install 3.11 from python.org side-by-side; the `py -3.11` launcher picks it.

### Git identity (do this before your first commit)
Use the GitHub no-reply address, never your ISB or personal e-mail:

```powershell
git config --global user.name  "<your-github-username>"
git config --global user.email "<id>+<your-github-username>@users.noreply.github.com"
```
(GitHub → Settings → Emails shows your exact no-reply address.)

---

## 2. Where to keep things (OneDrive caveat)

The workspace is inside OneDrive. OneDrive syncing a virtualenv or a multi-GB dataset will be slow and can corrupt files. Rule:

- **Code, docs, small outputs** → inside `projects/NN-slug/` (synced, fine).
- **Virtualenv** → outside OneDrive: `C:\venvs\ampba-NN`.
- **Raw data > 100 MB** → either keep in `data/raw/` and right-click the `data` folder → *Free up space / Always keep on this device* is NOT needed, but add it to `.gitignore`; or point `data_dir` in `config.yaml` to `C:\ampba_data\NN\`. Plans tell you which projects have big data (08, 09, 10).

---

## 3. Create a project skeleton (replace `NN-slug` and `PKG`)

```powershell
cd "C:\Users\11624\OneDrive - Indian School of Business\Documents\personal\isb_ampba\projects\NN-slug"

# virtualenv outside OneDrive
py -3.11 -m venv C:\venvs\ampba-NN
C:\venvs\ampba-NN\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel

# folders
$pkg = "PKG"
mkdir config, data\raw, data\interim, data\processed, notebooks, "src\$pkg", analysis, outputs, figures, models, app, tests, docs, .github\workflows
New-Item "src\$pkg\__init__.py", tests\__init__.py -ItemType File
git init
```

If PowerShell blocks `Activate.ps1`: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### `.gitignore`
```gitignore
.venv/
__pycache__/
.ipynb_checkpoints/
data/raw/
data/interim/
data/processed/
models/*.joblib
*.parquet
*.duckdb
.env
outputs/llm_usage.csv
```
Keep `outputs/summary.json`, `outputs/metrics.json` and `figures/*.png` **in** git — the README links to them.

### Install the package in editable mode (so notebooks can `import PKG`)
`pyproject.toml`:
```toml
[project]
name = "PKG"
version = "0.1.0"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
```
```powershell
pip install -e .
```

### Pin dependencies
After the project's packages are installed and working:
```powershell
pip freeze > requirements.txt
```
(Each plan gives a starter `requirements.in` list — install those first, then freeze.)

---

## 4. Config, seed, logging — copy this skeleton into every project

`config/config.yaml`
```yaml
seed: 42
paths:
  raw: data/raw
  interim: data/interim
  processed: data/processed
  outputs: outputs
  figures: figures
  models: models
# project-specific keys are added by each plan (business assumptions live here)
```

`src/PKG/config.py`
```python
from pathlib import Path
import logging
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path = ROOT / "config" / "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return logging.getLogger(name)
```
Seed once at the top of every entry point: `np.random.seed(cfg["seed"]); random.seed(cfg["seed"])`, and pass `random_state=cfg["seed"]` to every sklearn/xgboost/lightgbm call. Use `rng = np.random.default_rng(cfg["seed"])` for any simulation.

---

## 5. `make` is not available on Windows — use `tasks.py`

`tasks.py` at project root:
```python
"""Usage: python tasks.py <setup|data|train|evaluate|app|test|lint|all>"""
import subprocess, sys

PKG = "PKG"  # change per project
TASKS = {
    "setup":    ["pip install -r requirements.txt", "pip install -e ."],
    "data":     [f"python -m src.{PKG}.data"],
    "train":    [f"python -m src.{PKG}.train"],
    "evaluate": ["python analysis/run_analysis.py"],
    "app":      ["streamlit run app/streamlit_app.py"],
    "test":     ["pytest -q"],
    "lint":     ["ruff check ."],
}
TASKS["all"] = TASKS["data"] + TASKS["train"] + TASKS["evaluate"] + TASKS["test"]

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    for cmd in TASKS[name]:
        print(">>", cmd)
        if subprocess.call(cmd, shell=True) != 0:
            sys.exit(1)
```
(If you have Git Bash and `make`, an equivalent `Makefile` also works.)

---

## 6. Working rules that make the project defensible in a review

1. **Notebooks explore, `src/` computes.** Prototype in a notebook, then move the function to `src/PKG/*.py` and import it back. Keep notebooks thin.
2. **Split before you look.** Decide the train/valid/test (or time) split first, save it, and never fit anything (scalers, encoders, WOE bins, imputers, clustering) on valid/test.
3. **Always report a naive baseline** next to your model (majority class, seasonal naive, popularity, random).
4. **Every number you quote comes from a file** (`outputs/metrics.json`, `outputs/summary.json`) written by code, not typed by hand. In `analysis/run_analysis.py`:
   ```python
   import json
   summary = {"auc_test": float(auc), "ks_test": float(ks)}
   json.dump(summary, open("outputs/summary.json", "w"), indent=2)
   ```
5. **Business assumptions go in `config.yaml`** and are swept in a sensitivity table — never hard-coded in a function.
6. **State limitations** (synthetic data, survivorship bias, causal claims) in the README.
7. **Tests:** ≥ 10 `pytest` tests, run offline, using a tiny fixture (`tests/fixtures/`) — not the full dataset. Include at least one leakage / look-ahead test, one invariant test (identity, monotonicity, sum-to-one), one end-to-end smoke test.
8. **Commit after every milestone** with a message like `M2: WOE scorecard, test AUC 0.77` (see §10).

---

## 7. Tests + lint

```powershell
pip install pytest ruff
pytest -q
ruff check .
```
Minimal smoke-test pattern (`tests/test_smoke.py`):
```python
from PKG.config import load_config

def test_config_loads():
    assert load_config()["seed"] == 42
```

### CI (`.github/workflows/ci.yml`)
```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt && pip install -e . pytest ruff
      - run: ruff check .
      - run: pytest -q
```

---

## 8. Streamlit app + Docker (every project ends with an app)

```powershell
pip install streamlit
streamlit run app/streamlit_app.py
```
Rules for the app: read **precomputed artifacts** from `outputs/` and `models/` (do not retrain inside the app); wrap loaders in `@st.cache_data` / `@st.cache_resource`; every page shows the data source and a limitations caption.

`Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install -e .
EXPOSE 8501
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0"]
```
Deploy free: **Streamlit Community Cloud** (https://share.streamlit.io, connect the GitHub repo) or **Hugging Face Spaces** (Streamlit SDK). Commit the small precomputed artifacts the app needs.

---

## 9. Deliverables every project must end with

| File | Content |
|---|---|
| `README.md` | Problem → data → approach (mermaid diagram) → results table (baseline vs model) → business impact → limitations → how to run |
| `docs/PROBLEM_STATEMENT.md` | Objective, KPI, constraints, success criteria (write this on day 1) |
| `docs/DECISION_MEMO.md` | 1 page for a CXO: recommendation, ₹ impact, risks, next steps |
| `docs/MODEL_CARD.md` | Intended use, data, metrics, fairness/robustness check, limitations |
| `outputs/summary.json`, `metrics.json` | Machine-written numbers |
| `figures/*.png` | Charts referenced by README/memo |
| Review decks (optional) | Mid-review (after M3) and Final (after M5), ~10 slides each |

### `DECISION_MEMO.md` skeleton
```markdown
# Decision memo — <project>
**Decision requested:** <one sentence>
**Recommendation:** <what to do, with the key number>
**Impact:** <₹ / % / hours, with the assumption it depends on>
**Evidence:** <3 bullets, each with a number from outputs/summary.json>
**Risks & limitations:** <3 bullets>
**Next steps:** <pilot design, monitoring, owner>
```

### `MODEL_CARD.md` skeleton
Intended use · Out-of-scope use · Training data (source, dates, rows) · Metrics (valid/test, baseline) · Fairness / segment checks · Known failure modes · Monitoring plan · Version/seed.

---

## 10. Milestone rhythm (≈ 10 h/week; see each plan for the day-by-day)

| Stage | What | Gate |
|---|---|---|
| M1 | Data load, validation, EDA, problem statement | Data quality report done |
| M2 | Baseline + first real model | Baseline number recorded |
| M3 | Challenger / main method | **Mid-review** (deck P1–P4) |
| M4 | Business layer (economics, optimisation, policy) | Memo numbers frozen |
| M5 | App, tests, CI, memo, model card | **Final review**; README results table filled |

Commit pattern:
```powershell
git add -A
git commit -m "M2: <what you built>, <key metric>"
git remote add origin https://github.com/<you>/ampba-NN-slug.git   # first time only
git push -u origin main
```
Before any push, run `git log --format="%an <%ae>" -5` and confirm the no-reply address.

---

## 11. Common Windows problems

| Symptom | Fix |
|---|---|
| `pip` wheel build fails (C++ compiler error) | Use Python 3.11; else install "Microsoft C++ Build Tools"; or `pip install <pkg> --only-binary :all:` |
| `Activate.ps1` blocked | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Long-path errors in OneDrive | Enable long paths (`reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f`, admin) or work from `C:\dev\ampba\` |
| OneDrive "file in use"/slow | Pause sync while running heavy jobs; keep venv + big data outside OneDrive |
| `ModuleNotFoundError: PKG` in notebook | `pip install -e .` in the active venv; select that venv as the Jupyter kernel (`pip install ipykernel; python -m ipykernel install --user --name ampba-NN`) |
| Kaggle data needs login | Create a free Kaggle account → Account → "Create New API Token" → put `kaggle.json` in `%USERPROFILE%\.kaggle\`; `pip install kaggle` |
| Download blocked by a site (403) | Add a browser header: `requests.get(url, headers={"User-Agent": "Mozilla/5.0"})` |
