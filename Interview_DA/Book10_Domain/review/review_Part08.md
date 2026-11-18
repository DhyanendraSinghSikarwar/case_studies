# Review: Book 10 Part 8 (How to learn a new domain fast)

## Counts
- Answers checked: 28 (Q1-Q28).
- Answers whose numbers were recomputed by code: 8 (Q14, Q15, Q19, Q21 incl. SQL run in sqlite3, Q22, Q24, Q28; Q16 day/week arithmetic by hand).
- Answers with wrong arithmetic: 0. Answers changed: 7 (Q1, Q10, Q14, Q15, Q17, Q21, Q22), all additive or labelling fixes. No headings, numbers, stars, order or inline data changed.

## Recomputation results (all matched the written figures)
Q14 (5+3)x4 = 32 h; Q15 10+14+16+24+8 = 72, per-week 0.8/1.2/1.3/2.0/0.7 = 6.0; Q19 17 and 15 of 20, 16/20 = 80%; Q21 on a rebuilt sample: 7 rows, 6 distinct, 1 null; paid 5 rows avg 51,640, rejected 4,000, open null; Q22 5.5 + 0.5 = 6 h, x12 = 72; Q24 6/8 = 75%, 1/8 = 12.5%; Q28 avg headcount 200, 24.0%, 38/200 = 19.0%, x4 = 76%.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q1 | 40/40/20 split presented as advice without label | Labelled "my judgement, not a measured figure" |
| Q10 | "Asked at" said domain knowledge is good-to-have for "most" junior roles; sources file says about 2.5% of postings name it | Reworded to the sourced figure, small sample, may be stale |
| Q14 | 32 h over "30 days" vs 4 weeks = 28 days unexplained | Added one-line note |
| Q15 | Rounded percentages sum to 99 with no note; no pointers to Q7/Q8/Q17/Q19 | Added rounding note and cross-references |
| Q17 | Only one project flow; Section 7 mini-projects thin; no done-checklist | Added four illustrative mini-project ideas (one per domain, synthetic data only for healthcare/HR) and a done-checklist |
| Q21 | "Made-up 7-row sample" not shown, so output not reproducible; `sum(col is null)` is not portable | Added the sample rows (reproduces the pasted output exactly), a portability note and the median (2,000) |
| Q22 | Weekly plan only; no daily practice plan | Added a 30-minute daily practice block |

## Section 7 coverage (roadmap, daily plan, resources, datasets, mini-projects, self-check)
- Roadmap: Q15 (12 weeks, 72 h), Q16 (90 days), Q14 (30 days). Complete.
- Daily practice plan: Q14 daily habit, Q22 week plan, now a daily block in Q22. Complete.
- Free resources: Q7, Q18. Practice datasets: Q8 (+Q17). Mini-projects: Q17 (now with ideas). Self-check: Q19 (and Q14 week 4, Q16 day 90).
- Gap noted: none remaining within existing answers.

## Cross-references (checked every "Qn" mention)
All correct: Q1->Q5; Q2->Q13/Q14/Q17; Q7->Q8/Q14/Q18; Q12->Q5; Q13->Q14/Q27; Q14->Q5/Q8/Q19; Q16->Q7/Q8/Q17/Q19/Q24/Q27; Q22 now ->Q7/Q19. Q15 previously had none; now Q7/Q8/Q17/Q19. Q17 dataset list overlaps Q8 (report only; kept as it serves the mini-project flow).

## Domain, honesty, style checks
- Regulation mentions (DPDP, HIPAA, RBI) are awareness-level, labelled "from memory, unverified, confirm with compliance/legal" (Q20). No advice given.
- Personal-experience answers (Q2, Q6, Q13, Q26) are templates with "use only what is true". "Asked at" lines make no company claims, consistent with the sources file.
- Em dashes: none in answers (only the part-title line). Code fence balanced; no scaffolding.

## Unresolved / report only
- Part header says Target 20, Actual 28; fine (sources note explains).
- Possible overlap with Part 7/other parts on glossary and stakeholder questions was not cross-checked against other parts (outside scope).

## Left unverified
All resource and dataset names (Investopedia, Khan Academy, Coursera/edX audit, Kaggle, UCI Bank Marketing, Olist, Online Retail, Synthea, CMS DE-SynPUF, MIMIC access, DataCo, M5, IBM HR, data.gov.in), DPDP/HIPAA/RBI mentions, the quoted ~2.5% JD share (internal sample, not re-opened), and the question-bank attributions (Dataford, Modern Analyst, Bridging the Gap, MockQuestions). No web access.
