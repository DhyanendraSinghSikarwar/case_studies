# Mid-review (after M3) - Case 06 RFM / CLV / basket / recsys

**Verdict: Ready (conditional).** M1-M3 are implemented, tested and reproducible; the silhouette KPI is met only after a documented change of feature space (risk 1).

Fresh checks: `pytest -q` first run 26 passed / 1 failed (Streamlit AppTest 90 s timeout under CPU contention; fixed, timeout now 300 s; after fixes 30 passed, ruff clean); `ruff check .` clean. Full `tasks.py all` was not run (deviation: CPU shared with three other reviews; only pytest, ruff and `evaluate` were run). Numbers below come from `outputs/summary.json` / `metrics.json`.

## Spec conformance (M1-M3)
| Module | Implemented | Tests |
|---|---|---|
| data.py | yes | test_data |
| rfm.py (quintile codes, 6 named segments) | yes (`n_products` replaces `n_categories`, documented) | test_rfm |
| cluster.py (KMeans 2..10, GMM, HDBSCAN, profile, UMAP) | yes | test_cluster |
| clv.py (BG/NBD + GG, baseline, MAE, Spearman) | yes | test_clv (incl. holdout-leakage test) |

## Acceptance / KPIs through M3
| Item | Status | Evidence |
|---|---|---|
| Silhouette >= 0.35 | PARTIAL | 0.377 at k=4 on log-RFM (3 features). Spec 6-feature space: 0.257 at k=4 (best 0.323 at k=2); RFM+tenure 0.339 at k=4. Target met by narrowing the feature space and excluding k=2 (0.456). Disclosed in README Deviations and ablation |
| CLV MAE vs holdout beats baseline | PASS (thin) | 549 vs 570 (about 4% better); Spearman 0.608 vs 0.567 |
| Time-based split, no holdout leakage into CLV | PASS | calibration <= 2011-06-30; leakage test in tests/test_clv.py |
| Top-decile CLV share | PASS | 58.9% of predicted CLV; 60.7% of actual holdout spend (oracle 72.1%) |
| Aggregate calibration | WEAK | predicted holdout spend 3.42M vs actual 4.19M (Q4 seasonality), disclosed |

## Methodology scores (1-5)
| Area | Score | Note |
|---|---|---|
| Framing & KPI clarity | 4 | KPIs explicit |
| Data quality & validation | 4 | cleaning documented in DATA.md; duplicate lines kept (deviation) |
| Leakage / split design | 4 | calibration/holdout and tuning windows separate |
| Baseline vs model | 3 | CLV edge over historical average is small; k choice guided by the target |
| Business translation | 3 | segment revenue shares good; GBP native, INR display only |
| Explainability / fairness | 3 | segment-level checks only (no demographics in data) |
| Reproducibility | 4 | seed, tasks.py, pinned deps |
| Code quality | 4 | typed, docstrings, ruff clean |
| App usability | 4 | 4 tabs, AppTest covered |

## Top fixes
1. Keep the silhouette caveat prominent (3-feature space, k>=3): done via README ablation table.
2. Streamlit AppTest timeout 90 -> 300 s (tests/test_pipeline_e2e.py): done.
3. Add a bootstrap CI on the CLV MAE gap: open.
4. Add a seasonality-aware sensitivity of holdout spend: open.
5. Decide whether the 6-feature silhouette should be the headline with RFM-only as supplementary: open, judgement call.

## Likely sponsor questions
1. Why is silhouette only met on RFM? The wider space separates less; segments drive actions and the ablation is published.
2. Why k=4, not 2? k=2 only splits active from lapsed; not actionable.
3. Is CLV better than a simple average? Modestly on MAE (549 vs 570), clearer on rank (Spearman 0.608 vs 0.567).
4. Why under-predicted totals? BG/NBD lacks seasonality and the holdout includes Q4.
5. Rule segments or clusters for campaigns? Rule segments (named, stable); clusters are a cross-check (ARI 0.318).
