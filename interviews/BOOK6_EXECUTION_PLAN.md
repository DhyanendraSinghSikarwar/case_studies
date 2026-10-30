# BOOK6_EXECUTION_PLAN.md — How Book 6 (Scenario-Based Interview Questions, 10 parts) will be built

Follows plan.md §4 (answer template), §5 (Book 6 table), §11 (workflow) and style_guide.md. Books 1-5 are complete. Band: Rs 30-80 LPA roles; no salary figures anywhere. Output files: `Book6_Scenarios/Book6_Scenarios_PartNN.md`.

## Pipeline (same as Books 2-5)
1. **Wave A (one research agent per part):** research real scenario / case / "what would you do if" questions for the topic (public interview guides, question banks, company-type write-ups, engineering blogs; record opened vs snippet-only pages; paraphrase, never copy), freeze the list in `Book6_Scenarios/Book6_Scenarios_PartNN.md` with `<!-- ANSWER_PENDING -->`, append `B6PNN-Qn` rows to `question_index.md`, write `research_notes/Book6_PartNN_sources.md`. Wave A scripts in `scratch/B6PNN_wavea/` (copy `scratch/B5P14_wavea/build.py` pattern; stars sorted 3,2,1; easy to hard within a star).
2. **Wave B (4-5 answer agents per part, about 10-12 Qs each, own folder `scratch/B6PNN_Qxx-yy/answers.md`; progress written to disk early):** lead merges by heading with `scratch/B6PNN_merge/merge.py` (copy `scratch/B5P14_merge/merge.py`, change paths).
3. **Wave C (lead):** `python3 scratch/B6_check.py <part file>` (structure and re-run of every python block), spot-check, `review_notes/Book6_PartNN_review.md`, update plan.md tracker and this checklist, fetch then plain push (never force).

## Book 6 answer template
Per question, in order: `### Qn stars emoji scenario` / `**Asked at:**` / **Say this first (1 line):** / **Clarifying questions:** (3-6 questions to ask the interviewer, each with why it matters) / **Approach:** (numbered steps, structured like a spoken framework) / **Metrics:** (exact metric definitions, numerator/denominator, guardrails) / **Risks:** (what can mislead or go wrong) / **What the interviewer scores:** (3-5 bullets: what separates a strong answer from a weak one) / **Example:** (concrete numbers, hand-checkable, with a one-line weak answer versus strong answer contrast) / **Code:** (ONE python block that verifies the Example numbers or simulates the situation with a fixed seed; or the sentence "Not applicable: <why>" when the scenario is purely about people or judgement) / **Output (my run):** (pasted from the real run, or "not executed" when Code is not applicable) / **Follow-ups:** 1-3 with short answers / **Common mistakes:**. Spoken-interview tone, short sentences, bullets/tables.

## Execution rules
- Python 3.13 standard library plus numpy/pandas/scipy if installed (check); every block runs with `python3 -I`, self-contained, seeded randomness, asserts on the numbers quoted in the text; the pasted output is the real output.
- Numbers in Examples are invented for teaching ("illustrative numbers"), never presented as real company data. No benchmark, price or salary claims; no claims about what a named company does beyond the Asked-at line ("commonly reported in public guides").
- Paraphrase scenarios; name well-known frameworks by common names only (e.g., funnel, cohort, CUPED, SRM).
- Every statistics claim tested in the Code block where practical (e.g., the sample size, the p-value, the SRM chi-square) and labelled "my run".
- Scope: Book 1 Part 10 owns A/B and causal theory (Book 6 Part 4 stays on ambiguous situations and judgement, cross-reference earlier parts only by checked headings); Book 2 owns GenAI internals; Book 4 owns MLOps tooling; Book 3 owns SQL; Book 9 owns behavioural/soft-skill scripts (Book 6 Part 6 keeps to trade-off decisions in data-science work).
- Cross-reference other books/parts ONLY by build-verified headings.

## Part checklist (targets from plan.md)
| Part | Topic | Target | Wave A | Wave B | Wave C |
|---|---|---|---|---|---|
| 1 | Product metrics and metric drops ("DAU fell 10%") | 55 | ✅ (55 Qs) | ✅ | ✅ |
| 2 | Model performance degraded in production | 50 | ⬜ | ⬜ | ⬜ |
| 3 | Imbalanced / noisy / missing data situations | 50 | ⬜ | ⬜ | ⬜ |
| 4 | Experiment design and ambiguous A/B results | 55 | ⬜ | ⬜ | ⬜ |
| 5 | Business case studies (pricing, churn, fraud, supply chain) | 55 | ⬜ | ⬜ | ⬜ |
| 6 | Stakeholder conflicts and trade-off decisions | 45 | ⬜ | ⬜ | ⬜ |
| 7 | GenAI scenarios (hallucinations, cost, latency, eval) | 55 | ⬜ | ⬜ | ⬜ |
| 8 | MLOps incidents (pipeline failures, rollback, drift) | 45 | ⬜ | ⬜ | ⬜ |
| 9 | Domain sets: fintech, e-commerce, healthcare, ads | 50 | ⬜ | ⬜ | ⬜ |
| 10 | "Design a solution end-to-end" open scenarios | 40 | ⬜ | ⬜ | ⬜ |

## Process notes
Tell agents to stop and report (not retry) at a spend limit; commit and push WIP often (a stop hook demands it); frozen-prompt corrections are applied identically in the part file, the agent's answers.md heading, Wave A scripts and question_index.md before merge; WebFetch is unavailable (snippet-only sources, label them); lessons from Book 5: test every "why" sentence, state tie rules and conventions, fix wording that does not match observed output.

## Next step
Part 2 Wave A (model performance degraded in production, target 50): accuracy or precision falling, silent drift, label delay, training/serving skew, feedback loops, data pipeline bugs, seasonality, a metric fine offline but bad online, threshold and calibration decay, segment-level degradation, retraining decisions, rollback versus retrain, monitoring without labels, AI-era twists. Part 1 lessons: ambiguous prompt wording is answered through clarifying questions; fix prompt numbers that do not add up (Q1, Q53) identically in the part file, agent heading, qs.py, question_index.md and index_rows.txt before merge; every numeric Example backed by a code block with asserts; cross-reference Book 1 Part 10 and other parts only by checked headings.
