# Book 4 Part 8 Sources & research notes (Monitoring ML: drift, data quality, alerting, retraining)

Date: 2026-10-26. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. About 14 WebSearch calls and 6 WebFetch attempts. WebFetch OPENED one page (github.com/Devinterview-io/mlops-interview-questions); it failed with getaddrinfo ENOTFOUND for evidentlyai.com, docs.cloud.google.com, sre.google and datacamp.com. Everything else is SEARCH SNIPPET ONLY (search-tool summaries). No company-reported exact question was found; 'Asked at' tags name source types.

## Pages OPENED
| Page | What it showed |
|---|---|
| https://github.com/Devinterview-io/mlops-interview-questions | No dedicated monitoring or drift question; monitoring appears as bullets in Q1 (monitoring and governance), Q2 (lifecycle, retrain when performance slips), Q4 (registry, rollback), Q6 (CI/CD with monitor stage), Q7 (data quality tests, lineage), Q12 (inference monitoring with Grafana and Prometheus, drift detection) |

## Snippet-only sources (not opened)
| Source | URL | What the snippet said | Used for |
|---|---|---|---|
| DataCamp, Interview Guys, Towards AI 101, Medium skphd, hyring, wecreateproblems, K21Academy 47-question PDF, dev.to vivekk101 | https://www.datacamp.com/blog/mlops-interview-questions ; https://pub.towardsai.net/101-ml-llm-agentic-aiops-interview-questions-31a346ac84d3 ; https://k21academy.com/wp-content/uploads/2026/02/47MLOpsInterviewQuestions_ed4.pdf | data vs concept drift definitions; detect with KS or PSI against a baseline, watch prediction distribution; Evidently and Great Expectations; scaled response, retrain with validation gate; rollback after bad retrain; Prometheus/Grafana dashboards | Q1, Q2, tools, retraining, scenario Qs |
| Glassdoor EPAM interview page | https://www.glassdoor.co.uk/Interview/EPAM-Systems-Interview-E15544-RVW104237011.htm | scenario: production differs from training (feature, preprocessing, version mismatch); end-to-end design with monitoring; single candidate review, unverified | training-serving skew, design Qs |
| Evidently blog (large datasets), Arize monitors docs, ICLR 2026 virtual page 'When drift detectors cry wolf', wikidocs | https://evidentlyai.com/blog/data-drift-detection-large-datasets ; https://www.iclr.cc/virtual/2026/10016892 | KS too sensitive at large n; report D with p and set minimum D; Arize says PSI less sample-sensitive; the ICLR submission says PSI unstable below ~200 samples and Bonferroni cuts false positives but also power; sources conflict | PSI, KS, multiple testing, threshold calibration |
| NannyML blog, arXiv 2509.14294 multivocal review, arXiv 2403.16795 interview study | https://www.nannyml.com/blog/machine-learning-monitoring-workflow ; https://arxiv.org/pdf/2403.16795 | delayed or absent labels; CBPE and DLE; alert fatigue from false positives leading to silenced alerts | delayed labels, estimation, alerting |
| Vertex AI Model Monitoring docs | https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview | skew needs training data; drift watches input over time; requests logged to BigQuery; attribution skew with Explainable AI | managed monitors |
| SageMaker Model Monitor FAQ and API reference | https://docs.aws.eu/sagemaker/latest/dg/model-monitor-faqs.html | four dimensions (data quality, model quality, bias drift, feature attribution drift); baseline from training data proposes constraints; DriftCheckBaselines Bias/Explainability/ModelDataQuality/ModelQuality | managed monitors |
| Google SRE Workbook 'Alerting on SLOs', Datadog burn rate | https://sre.google/workbook/alerting-on-slos/ | alert on error-budget burn; multiwindow multi-burn-rate; two-window design avoids paging after recovery | SLO Q, alerting Q |
| pandera discussion #598, endjin comparison | https://github.com/unionai-oss/pandera/discussions/598 | pandera light in-code dataframe validation; GE broader with Data Docs; common combo; freshness check at 2x cadence from a generic conventions page | data quality Qs |
| apxml.com retraining triggers, DataRobot docs, pertamapartners glossary | https://apxml.com/courses/monitoring-managing-ml-models-production/chapter-4-automated-retraining-updates/retraining-triggers | scheduled vs triggered vs hybrid; event triggers risk feedback loops if miscalibrated; champion logs challenger predictions in shadow; numeric windows are vendor suggestions (not used) | retraining, champion-challenger |
| apxml ML audit trails, gravitee, scalevise, regolo | https://apxml.com/courses/monitoring-managing-ml-models-production/chapter-6-ml-governance-compliance/ml-audit-trails | minimise payload logging, metadata first, hash or mask PII, retention figures are vendor suggestions; nothing on India DPDP | privacy Q |
| arXiv 2608.02786, arXiv 2606.14589, tianpan.co, jacar.es, towardsdatascience upstream post | https://arxiv.org/pdf/2608.02786 | silent failures need distributional monitoring; trigger/amplifier/concealer split; anecdotal vendor schema change (40 percent figure not used) | incident Q |

## Not found (evidence gaps)
- No named-company monitoring interview questions for India or global firms. India angle = role types, DPDP and RBI-regulated lender scenarios, hedged; no regulation text looked up or quoted.
- Nothing official on: label shift in Vertex or SageMaker; SLOs defined for ML models (mapping is an expert extension); fairness monitoring in production; Azure ML monitoring; Arize, Fiddler, WhyLabs product behaviour.

## What was RUN in this sandbox (venvs under /tmp/claude-0/b8p08, Python 3.13.17)
| Item | Result |
|---|---|
| numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1 | installed; drift maths ran: PSI, ks_2samp, chisquare, jensenshannon, wasserstein_distance. At a 0.02-sigma shift: n=200 KS p=0.53; n=2000 p=0.70; n=200000 p=0.008 (D about 0.017 throughout); PSI 0.07, 0.006, 0.002 |
| Simulated calibrated-score estimate | expected accuracy from scores 0.749 vs true 0.753 (no labels used) |
| evidently 0.7.23 | pip install OK; import FAILS with pandas 3.1.0 (infer_dtype_from_object); with pandas 2.3.3 DataDriftPreset report ran offline, wrote a 3.7 MB HTML and dict results (Wasserstein normed on numeric, Jensen-Shannon distance on categorical, thresholds 0.1) |
| whylogs 1.6.4 | OK offline; drift scores need whylogs[viz] (IPython); profile logged for 2000 rows, KS drift score on shifted data = DRIFT (D 0.1975); view.write works with a deprecation warning |
| great-expectations 1.24.1 | OK offline: ephemeral context, pandas dataframe asset, ExpectColumnValuesToNotBeNull and ExpectColumnValuesToBeBetween validated and returned unexpected values/indices (progress bars flood stderr) |
| pandera 0.35.0 | needs pandera[pandas]; lazy validation returned a failure_cases table |
| prometheus-client 0.26.0 | Gauge, Histogram in CollectorRegistry; generate_latest printed exposition text |
| alibi-detect 0.13.0 | NOT usable: full pip install failed building scikit-image; --no-deps install imports fail (typing_extensions, pydantic, toml missing) and it pins numpy<2 and pandas<3. Not executed |
| promtool, prometheus, alertmanager, grafana-server | not installed (`which` empty); not executed. Arize, Fiddler, WhyLabs, SageMaker, Vertex, Azure ML: not executed |

## Design decisions
- 45 Qs: 17 three-star, 17 two-star, 11 one-star. Core drift and tests 7, data quality 3, labels and performance 6, alerting and ops 8, retraining and rollout 4, tools and cloud 4, privacy and fairness 3, incident and governance 4, advanced 10.
- Overlaps: Part 6 serving metrics/probes/shadow mechanics, Part 7 gates, Part 5 scheduling, Part 9 streaming/feature stores, Book 1 theory and Book 2 LLM monitoring are referenced as boundaries only.
- Wave B notes: use pandas<3 in an Evidently-only venv; GE and whylogs emit noisy progress output, redirect stderr; hedge all version-specific API claims; do not quote PSI 0.1/0.25 as standards.
