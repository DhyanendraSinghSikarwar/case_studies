# Review: Book 9 Part 5 (Model evaluation), Wave C

File reviewed and edited in place: `Book09_ML_AI_Tools/Book09_Part05.md` (87 answers, Q1 to Q87).
Environment: Python 3.13, scikit-learn 1.9.1, statsmodels 0.15.0, numpy, pandas. Scratch scripts: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/C09_Part05/`.

## Counts
- Answers checked: 87 of 87.
- Code blocks run: all 38 Python blocks in the part (Q62 via an equivalent script with a stated generator, since its data was not given).
- Hand arithmetic recomputed in a script: about 60 figures (Q2 to Q9, Q11, Q13 to Q20, Q22, Q25, Q28 to Q35, Q39 to Q48, Q53, Q55, Q57 to Q59, Q64, Q65, Q70, Q79, Q80, Q86).
- Answers with a wrong or irreproducible figure that was changed: 9 (Q23, Q24, Q27, Q36, Q38, Q54, Q62, Q63, Q66). Plus 6 small clarity or reference edits (Q50, Q52, Q58, Q61, Q62 wording, Q80).
- All other code blocks matched their pasted Output exactly; no code was wrong.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q23 | Table (190/61/28, 216/303/2) came from hidden "seed 42" data that could not be reproduced | Replaced with a fully described generator (default_rng(42), leave chance 0.2, normal scores 0.75 vs 0.25, spread 0.2) and rerun numbers: 0.5 gives TP 186, FP 78, FN 32; 0.3 gives 213, 310, 5; text now says 27 more leavers, 232 extra false alarms |
| Q24 | Used the old Q23 numbers (accuracy 0.91, 87 and 76 per 100, top 250 gives 190) | Recomputed from the new table: accuracy 0.89, baseline 0.78, 85 and 70 per 100, 250 calls give about 175 |
| Q27 | Seed table (accuracy 0.84 to 0.81, recall 0.29 to 0.22, 600 rows) not reproducible | Rebuilt on the Q52 dataset, seeds 0 to 4: accuracy 0.92, 0.92, 0.90, 0.88, 0.90; recall 0.66, 0.64, 0.57, 0.43, 0.73; baseline sentence changed from 17% to 15% (0.85) |
| Q36 | "seed 1" ambiguous | Names numpy default_rng(1); 0.498 reproduced |
| Q38 | Tree train 1.00 / test 0.65 not reproducible | Generator stated; reproduced values are 1.00 train and 0.75 test, text changed to 0.75 |
| Q50, Q52 | Hidden data; only "seed 42" stated | Found the generator that reproduces both outputs exactly (make_classification n=1000, 20 features, 2 informative, 2 redundant, weights 0.85, flip_y 0.01) and added it to "Sample data"; explained `stratify=y` |
| Q54 | Seed 3 recall written 0.44; actual 0.4348 | Changed to 0.43; source data named (Q52 data) |
| Q58 | Simulation seed not tied to a generator | Named default_rng(42), 20% and 20%; 0.202 / 0.204 reproduced |
| Q61 | Report had no source matrix | Added the confusion matrix [[44,4,2],[8,18,4],[2,5,13]]; classification_report reproduces the pasted table exactly |
| Q62, Q63 | In-sample 17.8 vs out-of-sample 38.9 not reproducible; OLS not explained | Generator described (default_rng(42), 60 rows, 15 features, 3 real, noise 20, 42/18 split); rerun gives 14.2 vs 34.8; OLS defined at first use; Q63 updated |
| Q66 | Leakage illustration (0.75/0.72 to 0.96/1.00) not reproducible and clashed with Q84 | Now cites the reproducible Q84 numbers: recall 0.68 to 0.90, precision 0.31 to 0.92 |
| Q80 | Cross-reference "accuracy alone (Q69, Q72)" pointed at kappa and MCC | Changed to Q6, Q14 |

## Checked and correct (no change)
Q1 to Q22, Q25, Q26 (single-class ravel gives one value, confirmed), Q28 to Q35, Q37, Q39 to Q49, Q51 (root_mean_squared_error exists; `squared=False` raises TypeError on 1.9.1), Q53 (sklearn MAPE is a fraction, 0.1125), Q55 (SD 10,000, R-squared about -15), Q56, Q57, Q59 (Wilson 64% to 95%, exact 62% to 97%), Q60, Q64 (quantile GradientBoostingRegressor runs), Q65, Q67 to Q77, Q79, Q81 to Q86 (Q71, Q74, Q75, Q77, Q81, Q82, Q84 outputs reproduce exactly).
Template check: all 87 have Asked at, interviewer check, Say this, Explain simply, Likely follow-ups, Common mistakes; every answer with code has Output and What it means (Q62's code is in the question, no output needed). Code fences balanced; no blank-line problems after tables; no em dashes in answer text (only the part-title line).

## Unresolved / report only
- Ordering: stars descend and numbering is continuous (checked). Within star groups, difficulty order is mostly respected; Q15 and Q16 are 🟡 inside a 🟢/🟡 mix that is fine.
- Overlap: Q22 and Q80 reuse a "150 flagged, 60 caught" shape; Q49 and Q14 and Q6 all teach the accuracy paradox; Q43 and Q20 overlap on outliers; Q57 with Q58 on baselines. Q84 vs Q66 both cover leakage (cross-referenced). Q47 and Q65 share one matrix. Leakage mechanics are also expected in Part 6 (per the sources file).
- Q83 style "from memory" topics (uplift) remain labelled.

## Claims left unverified (kept labelled in the text)
- All "Asked at" claims beyond "commonly asked": Tiger Analytics (Q2, Q4, Q7, Q8, Q28, Q56, Q81) and Flipkart (Q36, Q71, Q74, Q79) rest on snippet-level anonymous reports in `research/Book09_Part05_sources.md`; none opened in full.
- F-beta (Q11, Q17), `CalibratedClassifierCV` (Q74), labels with strings (Q21), SHAP and uplift (Q83, Q87), kappa rule-of-thumb bands (Q69).
- Privacy, DPDP Act, GDPR and public-AI-tool statements (Q77, Q78) are principle only and marked "from memory, unverified, confirm with IT or legal". No LLM was run.
