---
name: ampba-decision-memo
description: Write the CXO decision memo, model card, review-deck outline and LinkedIn post for a finished AMPBA case-study project, using only numbers from outputs/. Use after the final review or when the user asks for memo / model card / presentation / portfolio write-up.
argument-hint: "<case NN>"
---

# Decision memo, model card, deck outline

Input: case number. Work in `projects/<NN>-<slug>/`. Source every number from `outputs/summary.json`, `outputs/metrics.json` or files under `outputs/`; if a needed number is missing, add it to `analysis/run_analysis.py`, re-run, then write.

## 1. docs/DECISION_MEMO.md (max 1 page, ~400 words)
```
# <Decision title as a recommendation, e.g. "Approve cut-off 0.27 to lift portfolio profit by ₹X Cr">
**To:** <sponsor role>  **From:** <team>  **Date:**
## Recommendation (2 lines)
## Why (3 bullets, each with a number)
## Impact (table: metric | today | proposed | change)
## Sensitivity (what would change the decision; break-even values)
## Risks & mitigations (3 bullets)
## Next steps (pilot design: scope, duration, success metric, owner)
```

## 2. docs/MODEL_CARD.md
Intended use / out-of-scope use · Data (source, period, size, synthetic?) · Model(s) & features · Metrics (test, with CI where possible) · Fairness checks (groups, metric, gap) · Limitations & known failure modes · Monitoring plan (drift metric, threshold, retrain trigger) · Owners & version.

## 3. docs/REVIEW_DECK_OUTLINE.md (10 slides, ISB review format)
1 Title & team · 2 Business problem & KPI · 3 Data & quality · 4 Approach (diagram) · 5 Baseline vs model · 6 Key insight charts (figures/ paths) · 7 Business impact ₹ · 8 Sensitivity & risks · 9 Demo (app screenshots) · 10 Recommendation & next steps.
Each slide: title (a claim), 3 bullets max, figure path, speaker note.

## 4. docs/LINKEDIN_POST.md
150 words: hook with the headline result, problem, approach in one line, 3 bullet learnings, repo link placeholder, hashtags #ISB #AMPBA #Analytics. Put it in a code block for easy copy.

## 5. Finish
- README "Business impact" section updated with memo headline.
- Tick "Memo" in root README tracker. Commit "docs: memo, model card, deck outline".
