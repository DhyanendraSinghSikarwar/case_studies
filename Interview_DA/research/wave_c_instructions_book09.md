# Wave C instructions — Book 9 (Basic ML + AI Tools for Analysts) review (plan.md Section 8.6, 8.10)

You review ONE part file of Book 9 and fix it in place. Read first: `plan.md` (Sections 4, 5, 8.6, 8.10), `style_guide.md` (Sections 10, 11), `research/wave_b_instructions_book09.md`. Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, sqlite3; matplotlib/seaborn (Agg) if installed. No web access, no live LLM calls.

## Scope and edit rules
- Edit ONLY your assigned `Book09_ML_AI_Tools/Book09_PartNN.md` (targeted Edit calls, never rewrite the whole file) and write ONE report `Book09_ML_AI_Tools/review/review_PartNN.md` (mkdir -p). Never change question headings, numbers, stars or order, nor a question's inline data/code. Do not git commit.
- Scratch folder (yours only): `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C09_PartNN`. Run `python3 script.py`.

## Checks (every answer in the part)
1. **Run every code block (mandatory):** extract each Python/SQL block (rebuild data from the answer's sample data or described generator; where the answer hides data-building code, regenerate data that matches the stated description) and run it on the installed versions; compare with the pasted Output and with numbers in the prose. Fix wrong code, outputs and numbers. Snippets must run as shown (imports included). Where output depends on a seed or hidden data, it must say so.
2. **Recompute every figure:** metrics (precision/recall/F1/accuracy/RMSE/MAE/MAPE), confusion-matrix and cost-benefit arithmetic, odds ratios, Gini/entropy, k-means steps, RFM scores, forecasts and seasonal indices, token and credit arithmetic, break-even values, intervals and tests. Hand-checked or "verified by script" claims were not always true; do not trust them.
3. **Correctness of ML concepts and API claims:** definitions, assumptions, leakage, imbalance, overfitting, interpretation of coefficients, probability vs odds, forecast evaluation, sklearn/statsmodels names, defaults and removed arguments (verify on 1.9.1/0.15.0; anything about other versions or uninstalled libraries (imblearn, Prophet, kmodes, SHAP, XGBoost) must be labelled "from memory, unverified").
4. **Honesty:** GenAI, cloud, tool, pricing, legal and privacy facts (Copilot, ChatGPT, Claude, Snowflake, BigQuery, Fabric, DPDP Act, GDPR, four-fifths rule) stated as principle only and labelled "from memory, unverified, confirm with official documentation/IT/legal"; never a claim that an LLM or cloud service was run; example numbers labelled illustrative; personal-experience and learning-journey answers are templates ("say it only if true"). "Asked at" may only claim what `research/Book09_PartNN_sources.md` or `research/interview_processes.md` supports; otherwise "commonly asked (no company-specific report found)"; prep-site claims stay marked unverified.
5. **Beginner clarity:** a non-technical HR reader must follow every step; every term explained at first use; sounds like a confident analyst. Fix jargon without padding.
6. **Interview-ready code (style_guide Sections 10, 11):** descriptive names, comments on non-obvious steps, no test scaffolding or debug prints, plain-words line after output.
7. **Template completeness:** header lines (Asked at, interviewer check, Say this), Explain simply, Code/Output where relevant, What it means, Likely follow-ups, Common mistakes. Add anything missing.
8. **Ordering/numbering:** report only. **Duplicates/overlap** with other parts or books: report only.
9. **Style/markdown:** no em dashes in answer text (part-title line may keep one); balanced code fences; blank line after tables.

## Report (`review/review_PartNN.md`, <= 60 lines)
Counts (answers checked, code blocks run, answers wrong or changed), table of every fix (Q, what was wrong, how fixed), unresolved items, claims left unverified. Final reply (short): report path, numbers, anything unverifiable.
