# Book 1 Part 05 review (Q1-Q46)

Code blocks extracted and run standalone: 44 original blocks. 43 pass with printed numbers matching the text. Q37 "buggy snippet" is an excerpt (needs imports); now labelled as such. Q23 block needed umap and hdbscan modules (umap/hdbscan) and failed; replaced with runnable sklearn version (passes). Added blocks run: Q23 (sklearn HDBSCAN), Q24 lognormal rates, Q37 buggy-chain evidence, Q44 Deep SVDD (torch CPU). Q16 block re-run.

## Fixes
- Header: added star counts (12/23/11, recounted); removed stale dedupe remark.
- Q2: gap statistic rule corrected to Tibshirani's (next k), not "best".
- Q16: silhouette for correct moons was 0.05 only because the single DBSCAN noise point was kept as a cluster; with noise dropped it is 0.329 (claim "k-means 0.489 > DBSCAN" still holds). Code and text fixed.
- Q17: sklearn n_init default wording corrected (auto since 1.4).
- Q20: Ding-He wording made precise (relaxed indicators solved by top k-1 PCs; approximate, 2004).
- Q23: runnable sklearn HDBSCAN block added (PCA stands in for UMAP); UMAP snippet kept, marked not executed (umap-learn not installed; stale hdbscan dependency removed).
- Q24: lognormal flag rates (2.1/7.8/8.3) were unreproducible; replaced with reproduced 1.5/7.6/8.0 and added code.
- Q27: junk-cluster claim verified (7th cluster = 149 junk points); just clarified the not-executed UMAP note.
- Q30: PSI printed 0.239 (text said 0.241); fixed.
- Q37: buggy-chain numbers (0.334 vs 0.003) were not backed by code; added block.
- Q44: stale "torch unavailable" removed; Deep SVDD run (AUC 0.924 / 0.996) added; VAE left unrun.
- Q45: DBSCAN timings not reproducible on this machine (erratic); softened to indicative; J values reproduce.

## Unresolved / not verified
- Q45 timings and Q36 times are machine dependent. FAISS and UMAP not executed (not installed). Q38 LLM call not executed by design.
- Sources note not consulted (stale per brief). Ding-He and other citations checked from memory, not via web.
- Q25 text "without outliers 0.09 and 0.06" verified; Q33 nnz 47,149 and Q41 PCA min -0.33 verified.
