# review_Book1.md — Wave C review, Book 1 (DS / ML Technical)

Scope: 14 parts, 728 questions, 554 Python blocks. Per-part detail: `review_notes/Book1_PartNN_review.md`.

## Structure checks (scripted, final run)
| Check | Result |
|---|---|
| `ANSWER_PENDING` markers | 0 |
| Numbering continuous per part | Pass (all 14) |
| Star order ⭐⭐⭐→⭐⭐→⭐ | Pass (all 14) |
| Duplicate question titles across parts | 0 |
| Required fields (Asked at, Say this first, Example, Follow-ups, Common mistakes) | Pass (23 missing Example fields found earlier, all fixed) |
| Python blocks parse (ast) | 554 / 554 |
| Header Actual / star counts | Corrected in all parts |

## Counts after cross-part dedupe (Wave A) and review
| Part | Topic | Qs | ⭐⭐⭐ / ⭐⭐ / ⭐ |
|---|---|---|---|
| 1 | ML fundamentals, from-scratch | 35 | 14 / 16 / 5 |
| 2 | Regression, regularization, features | 51 | 15 / 24 / 12 |
| 3 | Classification metrics, imbalance, calibration | 48 | 17 / 21 / 10 |
| 4 | Trees, boosting, SHAP | 53 | 15 / 27 / 11 |
| 5 | Clustering, PCA, anomaly | 46 | 12 / 23 / 11 |
| 6 | Time series | 54 | 16 / 26 / 12 |
| 7 | Recsys, ranking | 49 | 15 / 21 / 13 |
| 8 | Deep learning | 58 | 16 / 30 / 12 |
| 9 | NLP & CV | 52 | 14 / 21 / 17 |
| 10 | A/B, causal | 56 | 19 / 27 / 10 |
| 11 | ML system design | 52 | 18 / 24 / 10 |
| 12 | pandas/sklearn, AI code review | 51 | 18 / 23 / 10 |
| 13 | Statistics I | 61 | 20 / 27 / 14 |
| 14 | Statistics II | 62 | 19 / 26 / 17 |
| **Total** | | **728** | |

Every part meets or exceeds its target. Total exceeds the ~620 book target (user chose to keep all 728).
Dedupe removed 14 cross-part duplicates (e.g. missing values, leakage, scaling, multicollinearity, CUPED, k-means from scratch).

## What the review changed (summary)
- Most quoted example numbers in answers were not reproducible from the code shown (worst: Parts 3, 6, 12, 1). Code was made standalone (seeded synthetic data) and text numbers replaced with printed ones; several conclusions flipped to match reality (e.g. P3 class weights/SMOTE tie; P6 global GBM beats seasonal naive; P6 Q45 honest fix loses to seasonal naive).
- Factual errors fixed: P11 Q21 price multiplier (1.84x, not 1.6x), P11 Q38 RBI/DPDP wording, P14 Q35 VIF (≈196), P14 Q42 sample size (≈2,600), P14 Q10/Q30/Q58/Q62 statements, P13 Q41/Q53/Q58/Q60, P8 Q29/Q46/Q47/Q49, P5 Q16 silhouette, P4 Q9/Q13/Q26, P10 Q50 toy simulation now shown.
- Weak or negative results kept and stated honestly (e.g. focal loss not beating logistic loss; embeddings adding little; unconstrained RF winning on validation).
- Illustrative / hand-computed / extrapolated numbers are labelled as such. Machine-specific timings labelled.

## Known limitations (unresolved)
1. **Code not executed** (marked in text): Prophet (P6 Q22/Q43), Chronos (P6 Q49), UMAP and FAISS (P5), transformers/HF snippets (P9 Q9/Q28/Q46/Q50), GPU-only code (P8 Q40 GradScaler, Q45 DDP), intentionally buggy code-review snippets, and a few skeleton snippets (P3 Q16/Q34). P4 Q26 and a few edited blocks in P2/P12 were verified in scratch versions, not re-extracted from the final file. P6 Q13/Q29 print nothing.
2. **Citations / external facts not web-verified** (recalled from memory): e.g. Ng & Jordan, Bergstra & Bengio, Goyal 2017, Jozefowicz 2015, Wilson 2017, Hoerl–Kennard, Guo 2017, Elkan–Noto, Hu–Koren–Volinsky, TIGER, Johari et al. mSPRT, model/paper descriptions in P6, EU AI Act / RBI details (worded generically). Verified by web: Grinsztajn 2022 (title/size) and DistilBERT figures (P8).
3. **Question-source evidence is thin**: web search returned mostly prep-site snippets; no first-hand reports for most named India/Europe companies. Stars partly rely on expert judgement; "Asked at" tags are indicative, not verified quotes. Details in `research_notes/Book1_PartNN_sources.md` (their Q-numbers predate the dedupe renumbering).
4. Timings (P4 Q52, P5 Q36/Q45, P12 Q5/Q47/Q48) are machine-specific and noisy.
5. Environment: transformers, umap, hdbscan, faiss, prophet not installed; torch CPU, polars, duckdb were installed during the run.

## Plan.md
Progress Tracker §10 updated: Book 1 = 14 / 14.
