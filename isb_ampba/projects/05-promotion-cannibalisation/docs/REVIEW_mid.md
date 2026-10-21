# Review (mid) - Case Study 05 Promotion Cannibalisation Engine

Reviewer: Claude (ampba-review skill). Contract: `SPEC.md`, `case-studies/05-promotion-cannibalisation.md`.

## Verdict
**Ready (mid-review).** M1-M3 (data, families, baskets, demand, engine, sweep) exist, are tested and meet their acceptance criteria.

## Fresh-run checks
- `python -m pytest -q`: 52 tests: the full run showed 51 passed and 1 failure (a bug in the new test_baskets.py, fixed); after the fix test_baskets passes (3) and the remaining 49 non-app tests plus the Streamlit AppTest passed in the full run
- `python -m ruff check .`: All checks passed.
- `python tasks.py evaluate`: succeeded, 388.8 s (CPU contended; 66.5 s earlier on an idle machine).
- `data`/`train` stages not re-run (see deviation).

## Deviation of this review run
- CPU constraint (three other projects reviewed concurrently): the full `python tasks.py all` was NOT run. Run instead: `python -m pytest -q`, `python -m ruff check .`, `python tasks.py evaluate` (388.8 s under load; the data/train stages were not re-run, so the engine table, families and elasticities come from the earlier build).
- No git commands for changes; root README tracker not ticked.

## Spec conformance
| SPEC module | Status | Note |
|---|---|---|
| data.py | Implemented, tested | `tests/test_data.py` |
| catalog.py (TF-IDF + agglomerative, co-purchase check, overrides) | Implemented, tested | `tests/test_catalog.py` |
| baskets.py (FP-Growth, halo) | Implemented, tested | `tests/test_baskets.py` added in this review (was untested directly) |
| demand.py (a) log-log elasticity | Implemented, tested | month effects per SKU, pooled SKU+week FE as cross-check (README deviation 3) |
| demand.py (b) MNL / nested logit | MNL base + nested logit (added in this review) | lambda = 1 reproduces MNL exactly; reported as a sensitivity only |
| engine.py | Implemented, tested | |
| sweep.py | Implemented, tested | normalised parametric engine, not the per-family MNL (deviation 6) |
| optimise.py | Implemented, tested | pulp/HiGHS, 8-week calendar |
| viz.py | Implemented | smoke-tested via e2e |
| analysis/run_analysis.py, app | Implemented | AppTest in `test_e2e.py` |

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Engine identity (1e-6) | PASS | `tests/test_engine.py::test_engine_identity` (300 random MNL cases), `test_engine_identity_nested_logit` (100 cases), `test_context_reference_promo`. |
| Sweep >= 1,000 draws, reproducible with seed | PASS | summary.json sweep.n_draws = 2,000; reproducible_with_seed = True; `tests/test_sweep.py`, `test_e2e.py::test_pipeline_is_reproducible`. |
| Memo reports reference family net, % profitable both views, break-even multiplier | PASS | `docs/DECISION_MEMO.md`: family net £779; 60.5% promoted-only vs 38.7% family; multiplier 1.22. |
| KPI: % promos correctly classified vs simulation truth | PASS (caveat) | dashboard 75.0% vs family rule 91.8% / 82.5% / 72.9% at 10/25/50% noise. Truth comes from the same parametric engine: a self-consistency test, not external validation. |

## Methodology audit (1-5)
| Dimension | Score | Justification |
|---|---|---|
| Problem framing & KPI clarity | 5 | Four-term family-net identity; KPIs (classification vs simulation truth, net per promo, break-even) implemented and reported. |
| Data quality & validation | 4 | Documented cleaning + identifiability report (`docs/data_quality.md`); validation by asserts/tests, no pandera schema. |
| Leakage control & split design | 4 | `as_of` cut-off for baseline/elasticity/seasonal index with explicit no-leakage tests; no out-of-time check of predicted vs realised uplift (no promo flags in data). |
| Baseline vs model comparison | 4 | Dashboard (promoted-only) view and top-revenue plan are baselines everywhere; "truth" is simulated, not observed. |
| Business translation & sensitivity | 5 | GBP and INR family net, budget sensitivity, margin x outside-share grid, tornado, nested-logit lambda sensitivity; margin honestly flagged as assumed. |
| Explainability / fairness | 4 | Waterfall by term, break-even elasticity, elasticity-source flag; fairness not applicable (invoice-level data), stated. |
| Reproducibility | 4 | Seed 42, `tasks.py`, pinned requirements, sweep reproducibility asserted; full `all` not re-run in this review. |
| Code quality | 4 | Typed, docstrings, ruff clean, 52 tests, thin notebooks with no stored outputs. |
| App / deployment usability | 4 | 4-tab Streamlit app covered by AppTest, Dockerfile, CI; app needs `outputs/engine_inputs.parquet` (parquet gitignored, so a fresh clone must run `tasks.py all` first). |

## Number audit
Programmatic audit of every number in README, DECISION_MEMO, MODEL_CARD and data_quality against `summary.json`, `metrics.json` and the sensitivity CSVs: 0 unexplained mismatches in generated blocks (README results block, memo, model card, data_quality). Residual tokens are not outputs: dates/DOI/spec constants and the external reference-repo claim (86%/11%) and '90' in 'p10-p90'; handwritten README/limitations contain no result numbers beyond these. Also in the memo: 1579, 2913, 14, 21.4%, 107 of 331 all match summary.json
Generated blocks are written by `src/promo/report.py` from `summary.json`. After the `evaluate` re-run every pre-existing key in `summary.json` was identical to the earlier run (only `nested_logit_sensitivity` and runtime are new/changed).

## Nested-logit gap (closed in this review)
SPEC 5.3 asks for "MNL/nested-logit"; the build had MNL only. Added `demand.nested_shares_after_discount` (family nest + singleton outside nest, calibrated to baseline shares and own elasticity; lambda = 1 is exactly MNL) and plumbed `nest_lambda` through `score_promo`, `break_even_elasticity`, `EngineContext`, config, app slider and the reference sensitivity. Base case stays MNL (lambda is not identifiable from this data).

| lambda | Reference family net | Cannibalised | SKUs profitable (family) |
|---|---|---|---|
| 1 | £779 | £1,436 | 10 |
| 0.7 | £363 | £1,773 | 10 |
| 0.5 | £-4 | £2,026 | 8 |

## Fixes applied
1. Nested-logit implementation + 5 tests (`tests/test_demand.py`, `tests/test_engine.py`), config `demand.nest_lambda`, app slider.
2. `tests/test_baskets.py` (3 tests) for FP-Growth rules and halo.
3. README (module table, limitations, deviation 4), DECISION_MEMO, MODEL_CARD regenerated from `summary.json` through `report.py`.
4. Programmatic number audit: no unexplained mismatch.

## Top fixes still open (prioritised)
1. Run one clean `python tasks.py all` on an idle machine and record the time (needed for a 'Ready' final verdict).
2. Use lambda inside `sweep.py` / `optimise.py` so the headline sweep is not MNL-only (today only the reference promo reports it).
3. Replace the circular KPI truth with an out-of-sample check (back-test predicted uplift on inferred price-drop weeks of identifiable SKUs; `pipeline.py`).
4. Make the app runnable from a fresh clone (parquet is gitignored): ship a small sample or build on first run (`.gitignore`, `app/streamlit_app.py`).
5. Add a pandera/explicit schema module for cleaned data (`validate.py` per project conventions).

## Likely sponsor questions
1. *Why is the family total (£779) above the promoted-only total (£133) if cannibalisation hurts?* Halo (£2,082) outweighs cannibalisation (£1,436) in the base case; the point is 3 of 24 SKUs are traps and 3 are hidden winners. Halo is an association scaled by `halo_factor` (assumption).
2. *Is elasticity causal?* No: prices are not randomised and there are no promo flags; 1,579 shrunk association estimates, sweep spans -1 to -6. Recommend controlled promos.
3. *What if siblings are closer substitutes than MNL says?* Nested logit lambda 0.5 gives reference family net £-4 vs £779 under MNL: the sign is fragile, hence the break-even-multiplier < 1 gate.
4. *Where does margin come from?* Assumed 40% (no costs in data); the margin x outside-share grid shows the total changes sign.
5. *How credible is the 91.8% classification accuracy?* Measured against simulated truth from the same parametric engine with noisy parameters; it shows the family rule beats the dashboard rule (75.0%), not accuracy on real promos.
