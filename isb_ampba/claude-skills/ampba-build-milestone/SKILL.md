---
name: ampba-build-milestone
description: Implement one milestone (M1-M5) of an ISB AMPBA case-study project end-to-end with tests, metrics and README updates. Use when the user says "build M2 for case 05", "next milestone", or continues a case study.
argument-hint: "<case NN> <M1|M2|M3|M4|M5>"
---

# Build one milestone

Input: `$ARGUMENTS` = case number and milestone. If milestone missing, read the project README "Milestone log" and pick the next unfinished one.

## Before coding
1. `cd projects/<NN>-<slug>/`. Read `CLAUDE.md`, `SPEC.md`, `README.md` (Milestone log), `config/config.yaml`.
2. List the modules, method steps, tests and acceptance criteria belonging to this milestone (from SPEC "Milestones"). Show the list to the user as a short checklist, then proceed.

## Build loop (repeat per module)
1. Implement module in `src/<PKG>/` — typed, docstrings, logging, config-driven (no magic numbers).
2. Write tests in `tests/test_<module>.py` using offline fixtures (no network, LLM mock). Minimum per module: happy path, edge case, one invariant (e.g. monotonicity, identity, no-leakage).
3. Run `pytest -q tests/test_<module>.py`; fix until green.
4. Wire into `train.py` / `analysis/run_analysis.py` so outputs land in `outputs/` and `figures/`.

## Milestone close-out
1. Run full pipeline: `python tasks.py all` (or `make all`). Must finish < 15 min; add `--sample` flag if not.
2. Run `ruff check . --fix` and `pytest -q`; all green.
3. Update notebooks only by calling src functions (thin notebooks).
4. Update project README: Results table (baseline vs model; numbers read from outputs/*.json), figures, "Milestone log" entry (date, what was built, metrics, open issues), Deviations if any.
5. Tick the milestone in root `../../README.md` progress table.
6. `git add -A && git commit -m "M<x>: <summary>"`.
7. Report to user: built items, test count, key metrics vs spec targets (table: metric | target | achieved | pass?), next step. After M3 recommend `/ampba-review <NN> mid`; after M5 `/ampba-review <NN> final`.

## Guardrails
- Leakage: time-based/group splits as spec says; add `test_no_leakage` style tests.
- Always keep a naive baseline in the results.
- Data downloads go through `src/<PKG>/data.py` with caching to `data/raw/` (see skill `ampba-data-sources`).
- Never invent metric values. If a target is missed, say so and propose 2-3 concrete fixes.
- LLM work: follow skill `ampba-llm-agents`.
