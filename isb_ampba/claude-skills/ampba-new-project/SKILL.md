---
name: ampba-new-project
description: Scaffold a new ISB AMPBA case-study project (01-10) under projects/ from its spec in case-studies/. Use when starting a case study or when the user says "start case study N" / "new project N".
argument-hint: "<case number 01-10>"
---

# Scaffold an AMPBA case-study project

Input: case number `$ARGUMENTS` (e.g. `01`). If missing, ask which case (show the table from root README.md).

## Steps
1. Read `case-studies/<NN>-*.md` fully. Extract: PKG name, module list, app tabs, milestones, acceptance criteria, reference repos, dataset.
2. Read `templates/project-CLAUDE.md`.
3. Create `projects/<NN>-<slug>/` with exactly this tree (empty modules get docstring + `NotImplementedError` stubs with typed signatures taken from the spec):
```
CLAUDE.md                 <- copy of templates/project-CLAUDE.md + a "## This project" section: PKG, spec path, milestones
README.md                 <- sections: Problem, Data, Approach (mermaid flowchart), Results (table placeholder), Business impact,
                             Limitations, Deviations, How to run, References (alumni repos from spec with links)
SPEC.md                   <- verbatim copy of the case-study spec
requirements.txt          <- pinned, only libs this case needs (see ampba-data-sources for data libs)
Makefile + tasks.py       <- targets: setup data train evaluate app test lint all  (tasks.py = cross-platform equivalent)
Dockerfile                <- python:3.11-slim, installs requirements, CMD streamlit run app/streamlit_app.py
.gitignore                <- .venv, data/raw, data/interim, data/processed, models/, __pycache__, .env, *.duckdb, mlruns
.env.example              <- LLM_PROVIDER=mock, GROQ_API_KEY=, OPENAI_API_KEY= (only if LLM case)
.github/workflows/ci.yml  <- setup-python 3.11, pip install, ruff check, pytest -q
config/config.yaml        <- seed: 42, paths, all business assumptions & hyper-params named in the spec
src/__init__.py
src/<PKG>/__init__.py + one file per module in the spec
analysis/run_analysis.py  <- stub writing outputs/summary.json
app/streamlit_app.py      <- tabs from spec, each showing "coming in Mx"
notebooks/                <- 01_eda.ipynb placeholder (markdown cell only)
tests/conftest.py         <- fixtures: tiny synthetic dataframe matching the data schema, seed
tests/test_smoke.py       <- imports every module
docs/PROBLEM_STATEMENT.md <- objective, KPIs (from spec), constraints, success criteria, stakeholders
docs/DECISION_MEMO.md, docs/MODEL_CARD.md  <- headings only
data/{raw,interim,processed}/.gitkeep, outputs/.gitkeep, figures/.gitkeep, models/.gitkeep
```
4. `git init` inside the project folder (if git exists), first commit "scaffold: case <NN>".
5. Create venv and install: `python -m venv .venv` then install requirements. If install fails, report the package and continue.
6. Run `pytest -q` (smoke test must pass).
7. Update root README.md progress table is NOT changed yet (scaffold isn't a milestone).
8. Report: tree created, next command `/ampba-build-milestone <NN> M1`.

## Rules
- Do not implement logic yet — only structure, signatures, config, docs.
- Module names and function signatures must match the spec exactly.
