# Brief: building (or finishing) one case-study notebook

Project root (cd here for every command): `C:/Users/11624/OneDrive - Indian School of Business/Documents/personal/case_studies/ecommerce`
Python 3.12, kernel `fintech-cases` is installed. Use Bash (POSIX) tool. Tools run from the project root; paths in `nbtool.py` are relative to it.

## What exists (read before writing)
- `README.md`, `decision.md` (decision-log format), `indian_ecommerce_data_science_case_studies.md` (sourced reference; **read your case's section: "## Case Study N"** for documented facts, evidence level, sources).
- Finished models to imitate in structure, tone, depth, statistics rigour: `_build/src/cs15.src` (shortest, ~400 lines) and one or two of `cs01.src`, `cs07.src`, `cs17.src`, `cs19.src`, `cs22.src`, `cs25.src`. Matching generators: `data/generate_csNN.py`. Matching fills: `_build/fills/fill_cs15.py`, `dec_cs15.md`, `rows_cs15.md`.
- Tooling: `python _build/nbtool.py ...` (see its docstring): `src2nb`, `run`, `dump`, `fill`, `verify`.

## Pipeline for a NEW case NN (name from `_build/rate.json`, e.g. `cs03_dark_store_inventory`)
1. Write `data/generate_csNN.py` (pure numpy/pandas, `generate(seed=42)`; hidden ground-truth columns prefixed `_`; calibrated to figures the reference file documents; keep runtime under ~3 min and data small enough: gz CSVs well under ~30 MB). Save outputs to `data/csNN/` from the notebook, including `data_dictionary.csv`.
2. Write `_build/src/csNN.src` with `#%% md` / `#%% code` cells (use `@@INCLUDE <absolute path to generate script>` after a `%%writefile data/generate_csNN.py` line exactly like cs15.src). Same section layout as cs15: 0 Exec Summary (marker `«EXEC»`), 1 Problem in simple English, 2 Reference (a documented / b what we simulate / c industry use), 3 Business->Analytical->Hypotheses, 4 Data (sourcing, generator, dictionary), 5 Data quality, 6 EDA, 7 Statistics as the core (assumptions checked, effect sizes, CIs, power/sample size, multiple-testing correction, a written observation cell after every analysis), 8 short ML section, 9 ₹ business case with best/base/worst, 10 Recommendation + decision rule + KPIs, 11 Risks, 12 Appendix (formulas, glossary).
   - Observation text is NOT written before running. Put markers like `«O5»`, `«O71»` in the md cells after analyses; after execution you replace them using a fills file.
   - Standards: seed 42; pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, seaborn only (xgboost ok if needed); no hyper-parameter tuning; honest null/negative results; every chart has `set_title`, `set_xlabel`, `set_ylabel` (or is a heatmap) and the next cell is a markdown cell containing the word "Takeaway"; no stderr warnings (filterwarnings ignore); runtime of whole notebook preferably under 15 min (use subsampling where needed); ~35-40 cells; 4-7 charts.
   - Weak-evidence cases: say plainly in section 2 that public method detail is thin and the notebook is an interview-standard solution on simulated data, not a reproduction of the company's system. Never state undocumented facts as documented.
   - Use "₹", "crore", "lakh". Plain, direct English. No em-dash overuse.
3. `python _build/nbtool.py src2nb _build/src/csNN.src csNN_name.ipynb` then `python _build/nbtool.py run csNN_name.ipynb > _build/runNN.log 2>&1` (run in the background if it may exceed 2 minutes, with timeout care). Fix errors in the .src and rebuild; do not hand-edit the notebook except through fill.
4. `python _build/nbtool.py dump csNN_name.ipynb > _build/dumpNN.txt`; read the real numbers.
5. Write `_build/fills/fill_csNN.py` defining `R = {...}` with every marker -> text built ONLY from numbers actually printed (no invented numbers; if a result is null or contradicts the plan, say so). Then `python _build/nbtool.py fill csNN_name.ipynb _build/fills/fill_csNN.py`.
6. `python _build/nbtool.py verify csNN_name.ipynb` must report OK (no leftover markers).
7. Write `_build/fills/dec_csNN.md` (header `---` then `# Case Study N — Title (Company) · \`csNN_name.ipynb\``, then 6-8 `## D-N-0k:` entries in the same 8-field format as dec_cs15.md) and `_build/fills/rows_csNN.md` (matching summary-table rows). 

## DO NOT touch (shared files, edited serially by the coordinator): `README.md`, `decision.md`, `indian_ecommerce_data_science_case_studies.md`, `nbtool.py`. Do NOT run `adddec` or `mark`. Only touch files carrying your case number.

## Finishing an existing half-built case (11, 17, 19, 20, 22, 25)
`_build/src/csNN.src` and a notebook exist. Check `python _build/nbtool.py verify`. If cells error or are unexecuted: fix the .src (e.g. cs11: MLPRegressor has no tuple `loss`; cs20: unterminated string in a code cell), rebuild with src2nb, rerun. If it already executed OK: dump, write fill/dec/rows files, fill, verify. Same rules.

## Final report (keep under 150 words)
Notebook file, runtime, verify status, 3 headline results, anything you could not do or that is weak.
