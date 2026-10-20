---
name: ampba-review
description: Run an ISB-style mid-review or final review of an AMPBA case-study project against its spec and acceptance criteria; produces a review report and fix list. Use when the user says "review case N", "mid review", "final review", or after M3/M5.
argument-hint: "<case NN> <mid|final>"
---

# AMPBA project review (mirrors ISB's two formal capstone reviews)

Input: `$ARGUMENTS` = case number + `mid` (after M3) or `final` (after M5).

## Steps
1. `cd projects/<NN>-<slug>/`; read SPEC.md, README.md, outputs/*.json.
2. Fresh-run checks (do not trust old outputs):
   - `pytest -q` → record pass/fail counts.
   - `ruff check .` → issues count.
   - `python tasks.py all` (final review only; mid: data+train) → time taken, errors.
3. Spec conformance: for every module in SPEC, check it exists, is implemented (no NotImplementedError), has tests.
4. Acceptance criteria: evaluate each checkbox with evidence (file path / metric value). Status: PASS / FAIL / PARTIAL.
5. Methodology audit (score each 1-5 with one-line justification):
   - Problem framing & KPI clarity
   - Data quality & validation
   - Leakage control & split design
   - Baseline vs model comparison
   - Business translation (₹ impact) & sensitivity analysis
   - Explainability / fairness (where relevant)
   - Reproducibility (seed, one-command run, pinned deps)
   - Code quality (types, docstrings, tests, thin notebooks)
   - App / deployment usability
6. Number audit: every number in README and docs/DECISION_MEMO.md must match outputs JSON; list mismatches.
7. Write `docs/REVIEW_<mid|final>.md`:
   - Summary verdict (Ready / Needs work), score table, acceptance checklist with evidence, top 5 fixes (prioritised, each with file + concrete change), risks for sponsor Q&A (5 likely questions with suggested answers).
8. Tick "Mid-review" or "Final review" in root README only if verdict = Ready.
9. Report the verdict table and top fixes to the user; offer to apply fixes.
