# Review: Book 9 Part 4 (clustering, k-means, RFM), Wave C

Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, SQLite 3.53.1.

## Counts
- Answers checked: 66 of 66 (all numbers recomputed; all arithmetic questions Q8, Q9, Q12, Q17, Q22, Q24, Q25, Q26, Q29, Q45, Q50, Q52, Q59, Q64, Q66 redone by hand/script).
- Code blocks run: 29 Python blocks (extracted and executed) plus 1 SQL block (Q48, sqlite3); hidden-data blocks rebuilt from the stated description.
- Answers changed: 35 (Q4, Q6, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q36, Q37, Q38, Q39, Q40, Q41, Q42, Q43, Q44, Q45, Q46, Q47, Q49, Q51, Q54, Q55, Q56, Q57, Q58, Q60, Q62, Q63, Q65). Substantively wrong: 11 (Q25, Q30, Q36, Q39, Q42, Q44, Q47, Q49, Q55, Q62, Q63) plus the made-up 300-customer family (Q45, Q46, Q51, Q54, Q56, Q58, Q60, Q65).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q4 | "P3 switches to c2": P3 had no earlier cluster | "P3 joins c2" |
| Q6 | Table reproduced exactly (inertia, silhouette), but generator not stated | Added make_blobs/KMeans settings |
| Q25 | Grand mean stated as 7.2; correct is 6.8; code lacked numpy import and data | Fixed 6.8, added import and data |
| Q26 | Missing `import numpy` | Added |
| Q27, Q28, Q29, Q33, Q34, Q37, Q40, Q41, Q43 | Snippets did not run as shown (no imports or data) | Added imports and data-building lines; outputs reproduced identically |
| Q30 | Output inertia 1999.45 is impossible: standardised 500x4 data has total spread 2,000, so any 3-cluster fit is far lower | Gave generator (make_blobs seed 42), real output `[2 0 2 0 1] (3, 4) 100.26...`, explained |
| Q31 | "99.996% from monetary" lacked the pair; no data/imports | Named customers 1001 and 1003 (verified 99.9963%); added df and imports |
| Q32 | Data hidden | Found exact generator (`default_rng(42).lognormal(7,1,300).round()`, reproduces mean 1,692, max 20,209, sizes [270 27 3] / [85 158 57]); added to code |
| Q36 | Hidden data; cluster sizes and means not reproducible | Wrote generator, real output (101, 100, 97, 2; means 1,492 to 7,513), updated prose |
| Q39 | Inertia 666.4/1590/1597 impossible for 6 clear standardised blobs (total spread 720) | New reproducible blobs (std 0.6, seed 0): 38.7, 39.0, 20.2, 38.9, 20.2; best 20.2. Verified `n_init="auto"` = 1 for k-means++, 10 for random (source) |
| Q42 | Hidden data; correlations and PCA shares not reproducible | Generator added; real values 0.96, 0.09, 0.06; PCA 66/33/1% |
| Q44 | Hidden data; shares 0.46/0.29 and table not reproducible; plt.show note | Generator added; real 0.46/0.28 (74%), new table and reading |
| Q45 | Frequency-monetary correlation 0.85 and agreement 0.93 not reproducible | Added generator for shared 300-customer data; real 0.91 and 0.94 |
| Q46 | Bootstrap ARI numbers not reproducible | Recomputed: single starts all 1.0; k=3 mean 0.95 (worst 0.91); k=5 mean 0.90 (worst 0.53) |
| Q47 | Training data hidden; distances 1.75/2.12 not reproducible | Added training data; real distances 1.58 (centre 1) vs 2.08 (centre 0); labels and output match |
| Q49 | "5.0 apart raw" wrong (sqrt(1+25) = 5.1); second figure unclear | Rewritten with 5.1 and 2.2 explained |
| Q51, Q54, Q65 | Segment sizes and revenue shares not reproducible | Recomputed: 74 / 143 / 83 customers, 64% / 29% / 7% revenue; Q54 reworded to the unnamed Segment 2 (= Lapsed here) |
| Q55, Q56 | Inertia and silhouette sequences not reproducible | New generator (3 overlapping blobs): inertia 900 to 247.1, silhouette peak 0.373 at k=3; stability 0.96/0.79 (k=3) vs 0.82/0.56 (k=5); k=5 sizes 91, 53, 58, 51, 47 |
| Q57 | Numbers correct (0.25, 1.0, 3 noise points) | Added make_moons settings |
| Q58 | Sizes and agreements not reproducible | Recomputed: 143/74/83 vs 149/74/77 (0.94); with 20,000 spender 80/220/1 vs 148/76/77 (0.49) |
| Q60 | Seed pair and 99.7% not reproducible | Seeds 1 and 4: labels swapped, ARI 1.0, 100% after renaming |
| Q62 | Probability figures not reproducible | Recomputed: 81% above 0.9, 21 below 0.7, borderline customer 0.52/0.00/0.48, ARI vs k-means 0.51 |
| Q63 | Claim that mini-batch took half the time did not reproduce (full k-means about 0.3 s, mini-batch several seconds here) | Removed speed claim; kept inertia comparison (1,000,436 vs 1,000,482); speed benefit marked from memory, unverified |
| Q38 | "Asked at" overstated Tiger Analytics mapping | Reworded to sources-file wording |

## Verified correct, unchanged
Q7 (49,000.01 and scaled output), Q8, Q9 (81 days), Q10, Q11 (full table and profile), Q12 (cut points 8.2, 17.6, 36, 66), Q17, Q22 (all drop percentages), Q24, Q26, Q27, Q29 (3.125 shows as 3.12), Q37, Q40 (linkage matrix), Q41, Q43, Q45 weight arithmetic, Q48 (SQL output matches row for row on SQLite 3.53.1), Q50 (3.85, 4.9, 3.42; 47/39/14%), Q52 (6.0% vs 4.2%, z-test p = 0.025), Q59 (129.0 and 0.0), Q64, Q66 (600, 2,000, 3,000).

## Unresolved / notes
- The 300-customer examples (Q45, Q46, Q51, Q54, Q58, Q60, Q62, Q65) and the Q55/Q56 dataset now run from stated generators, but numbers depend on numpy 2.5.3 / scikit-learn 1.9.1 and the seed; the text says so.
- Q48: NTILE order among tied values is engine-dependent; the answer already warns about ties.
- Ordering/numbering: no issues. Overlap: Q6/Q22/Q55 (choosing k), Q26/Q7/Q58 (scaling), Q36/Q37 (outliers) overlap by design; Q60/Q46 share label-switching and stability themes. Also check overlap of Q61 (cluster labels as features) with Book 9 supervised-model parts.

## Left unverified (labelled in the answers)
Typical "0.5 silhouette is reasonable" rule of thumb (Q23); singleton-cluster silhouette = 0 (Q24, sklearn convention from memory); gap statistic, t-SNE/UMAP, RobustScaler, BIC for mixtures, k-modes/k-prototypes/k-medoids packages (not installed), BG/NBD, DBSCAN eps choice (Q6, Q36, Q44, Q57, Q58, Q62, Q64, Q66); DPDP Act and GDPR (Q49, Q53). Asked-at claims all follow the sources file (snippet-level, unverified); no LLM, cloud or pricing claims in this part. No em dashes in answer text; code fences balanced (110 fence lines).
