# Book 1 Part 12 review (Wave C)

Scope: Q1-Q51 read for known items; every python block (54) extracted and run standalone in scratch dir.

## Fixes
- Header: added star counts (18 / 23 / 10, total 51 verified). No stale "dedupe pass" star note exists.
- Q2: example/output numbers did not match the code (12%/21%/0.40/39.49); replaced with the run values (9.5%, 17%, 0.33, median 40.83).
- Q5: snippet now contains the slow apply version, timing and equality assert (20k rows: 12.56 s vs 0.0064 s in this run). The "5M rows" claim is labelled as an extrapolation.
- Q6: unreproducible "offset 0.093" replaced by a computed mean shift (0.025), added to snippet.
- Q7: AUC numbers corrected to the run (0.877).
- Q9: snippet now includes the leaky SMOTE-before-CV variant (0.999) next to the pipeline (0.072).
- Q10: example described rows that do not exist in the data; replaced by the actual run values (Jan 26: mean 27.0, count 2; Feb 8 NaN).
- Q11: time-series numbers (0.35 / -0.31) came from another run; added standalone snippet reproducing them; text now 0.97 vs -1.76.
- Q12: AUCs corrected (0.921/0.477; 0.521/0.478).
- Q14: snippet was abbreviated; replaced by the full standalone script. Table now from this script (0.990/0.977, 0.898/0.862, 0.889/0.697, 0.885/0.547; baseline 0.891). Marked as synthetic/illustrative.
- Q16: example bounds corrected (-3.07, 3.26; raw max 21.48), demo lines added to snippet.
- Q17: timing / memory / +1e8 offset-error claims now reproduced in the snippet (0.55 s, 80 MB, rel err 3e-16 vs ~3).
- Q23: snippet made standalone (generates big.csv); numbers replaced with run values (400 MB -> 20 MB; CSV 96.5 MB, Parquet 14.5 MB; chunk float32 error ~16 of 2e8); 5 GB extrapolation labelled. polars/duckdb confirmed installed and run. Note: printing a Polars table on Windows needs PYTHONIOENCODING=utf8.
- Q29: removed an unreproduced figure (oversample LR 0.198).
- Q38: removed unreproduced "PSI 0.017".
- Q40: added missing Example; added numpy import to buggy snippet; reworded the "divide by k" bug (it is a convention choice).
- Q42: snippet gets the train-set importance line.
- Q44: runtime claim removed; 6 tests pass (pytest).
- Q47: timing text reworded to ratio from a re-run.
- Q48: timing + .explain() added to snippet (see below for numbers).
- Q49: removed unverifiable survey attribution.
- Q3: CoW statement verified (opt-in in 2.x, default in 3.0; chained assignment warns, SettingWithCopyWarning removed in 3.0). Left as is.
- Q30/Q31: numbers match the runs exactly; no change needed (the "trivial differences" item: none found).

## Code blocks
54 blocks run. Initial: 49 pass, 5 "fail" for non-bug reasons: Q14 (abbreviated -> fixed), Q23 (needed external big.csv -> fixed), Q35 first block and Q50 first block (deliberately buggy input code shown for review, not meant to run), Q37 (slow, see unresolved).
- Q48 re-run: pandas 4.69 s, Polars lazy 0.46 s, DuckDB 0.81 s, identical top totals; `.explain()` shows `PROJECT 2/4 COLUMNS` and the pushed-down selection (claim verified). Timings in text updated and flagged as noisy.
- Q42 train-set importances (0.238, 0.147, 0.184) reproduced; Q37 (HistGradientBoosting, ~8 min on this busy machine) reproduced exactly: 0.800 / 0.796 / 0.793 / 0.814 / 0.812.
- Q11, Q14, Q23 new/extended snippets run: pass. Q40 fixed tests run: "all tests pass". Q44: pytest 6 passed.

## Unresolved / caveats
- Q35 first block and Q50 first block are deliberately buggy review input (need df / imports); they are labelled as the code under review, not meant to run standalone.
- Q13/Q16/Q17/Q9 snippets were extended with print lines; values verified in scratch runs but the full edited blocks were not re-extracted and re-run as a final pass beyond those scratch versions (they are the same code).
- Q5 slow-version timing depends heavily on machine load; the 5M-row figure is an explicit extrapolation.
- Q3 CoW claim checked from knowledge (pandas 3.0 released Jan 2026), no web check.
- Q30/Q31: nothing wrong found.
