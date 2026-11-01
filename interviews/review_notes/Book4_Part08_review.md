# Book 4 Part 8 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45 (monitoring ML in production: drift, data quality, delayed labels, alerting, retraining). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-12, Q13-23, Q24-34, Q35-45; merged by heading: 45 of 45 merged, 0 skipped, 0 pending. No spend-limit stops. Several tools needed separate environments (Evidently with pandas 2.3.3; whylogs, Great Expectations, pandera and prometheus-client each in their own venv; core maths in the shared venv).

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45; star order and counts 17 / 17 / 11 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 45 |

The lead did not re-run the scripts (they span six environments); pasted outputs come from each agent's real runs, saved next to each script as `.out`/`out/qNN.txt`. All data is seeded; outputs that carry timestamps (Q16 `_created`) differ on a re-run.

## What really ran (numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1; evidently 0.7.23 on pandas 2.3.3; whylogs 1.6.4; great-expectations 1.24.1; pandera 0.35.0; prometheus-client 0.26.0)
PSI, KS, chi-square, Jensen-Shannon and Wasserstein drift maths; bootstrap nulls; domain-classifier drift and PCA reconstruction error; CUSUM and Page-Hinkley over 200 seeds; label-free performance estimation from calibrated scores; stratified label sampling with weights; selection-bias loop with an exploration holdout; burn-rate and two-window alert calculator; fairness windows with Wilson intervals; redacting logger with keyed hash; Evidently reports and drift dicts offline; whylogs profile merge and drift scores; Great Expectations and pandera schemas on good and corrupted batches; pytest suite for monitors and a detection matrix over 200 seeds; prediction-logging and incident-timeline simulations.

## Findings kept in the text (observed)
- Accuracy did not fall under covariate shift (0.836 vs 0.793 unchanged); a feature-only monitor misses concept drift (KS D 0.015); a score-based estimate stays at 0.77 under concept drift while true accuracy is about 0.52 (and 0.687 vs 0.576 in Q24); matured-label accuracy showed the drop only 31 days after the change.
- PSI missed a tail-only shift (0.011) and false-alarms at n=100 (about 0.099); KS p-values flip with sample size at a tiny shift (0.53, 0.70, 0.008 at n = 200, 2000, 200000); PSI null p99 fell 0.12, 0.011, 0.001 for n = 200, 2000, 20000.
- A correlation flip leaves per-feature KS quiet (p about 0.5) while a domain classifier (AUC 0.893) and PCA error catch it; permutation importance alone caught a concept change in which drift tests stayed quiet.
- Selection bias: AUC on approved cases 0.774 vs true 0.735; an exploration holdout gave 0.814.
- Evidently 0.7.23 fails to import under pandas 3; whylogs 1.6.4 crashes on pandas 3 string columns with numpy 2 (np.unicode_), so Q15/Q39 cast to object or use numeric columns; pandera column checks skip nulls by default; Q45's volume monitor first missed a dropped region and a category monitor was added.
- Two-window burn-rate alerts stop once a fault is fixed; the single long window kept firing an hour longer.

## Not executed
alibi-detect (install failed), Prometheus, Alertmanager, Grafana, promtool (alert rules only parsed with PyYAML for structure; PromQL not validated), WhyLabs, Arize, Fiddler, SageMaker Model Monitor, Vertex AI Model Monitoring, Azure ML monitoring, Great Expectations Data Docs and checkpoints, any real LLM provider, the traffic filter in Q44. Incident dates, owners and rotas are simulated and invented.

## Hedged ("check current docs")
SageMaker and Vertex descriptions (snippet-only), whylogs default drift threshold, Evidently "normed" definition, DPDP Act and GDPR text (not quoted, no regulator text looked up). PSI 0.1/0.25, burn-rate 6.0, 0.8 ratio, MAD multiplier k=8, gain floor 0.005 and similar are illustrative conventions, not standards; sources conflict on PSI small-n behaviour. The Q25 "90 percent" is ambiguous, so both readings are shown.

## Evidence limits
No candidate-reported monitoring questions found; one page opened (a GitHub question list with no dedicated monitoring items); every WebFetch otherwise failed. DPDP, RBI, Azure ML monitoring, fairness monitoring and ML SLOs are expert extensions. See research_notes/Book4_Part08_sources.md.
