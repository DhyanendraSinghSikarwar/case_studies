# BOOK4_EXECUTION_PLAN.md — How Book 4 (MLOps / Productionization, 12 parts) will be built

Follows plan.md §4 (answer template), §5 (Book 4 table), §11 (workflow) and style_guide.md. Books 1-3 are complete (728 + 558 + 501 Qs). Band: Rs 30-80 LPA roles; no salary figures anywhere. Output files: `Book4_MLOps/Book4_MLOps_PartNN.md`.

## Pipeline (same as Books 2 and 3)
1. **Wave A (one research agent per part):** research real MLOps interview questions (guides, banks, company-type write-ups, official docs), record opened vs snippet-only pages, freeze the list in `Book4_MLOps/Book4_MLOps_PartNN.md` with ANSWER_PENDING, append `B4PNN-Qn` rows to question_index.md, write `research_notes/Book4_PartNN_sources.md`. Script `scratch/B4PNN_wavea/build.py` (copy `scratch/B3P12_wavea/build.py`; stars sorted 3,2,1).
2. **Wave B (4 answer agents per part, about 10 Qs each, own scratch folder `scratch/B4PNN_Qxx-yy/answers.md`):** lead merges by heading with `scratch/B4PNN_merge/merge.py` (copy of `scratch/B3P12_merge/merge.py`, change paths).
3. **Wave C (lead):** structure check, re-run code, spot-check, `review_notes/Book4_PartNN_review.md`, update plan.md tracker and this checklist, fetch then plain push (never force).

## Book 4 answer template
Per question, in order: `### Qn stars emoji text` / `**Asked at:**` / **Say this first (1 line):** / **Then explain:** (2-5 bullets) / **Example:** (concrete, hand-checkable) / **Code:** (config, Dockerfile, YAML, Python, shell; see execution rules) / **Output (my run):** (only for what was really run; otherwise write "not executed" and say why) / **Follow-ups:** / **Common mistakes:**. Short mandatory edge cases or failure modes inside Then explain or Common mistakes. Spoken-interview tone, plain words.

## Execution rules (environment differs from Book 3)
- Installed: Python 3.13, pyyaml, pydantic, uvicorn, git, docker CLI (check `docker info`; daemon likely unavailable). NOT installed: kubectl, helm, dvc, mlflow, airflow, prefect, fastapi, pytest, sklearn, aws CLI. Agents may `pip install` small libs (pytest, fastapi, httpx, mlflow, dvc, scikit-learn) if the network proxy allows; say which versions ran. Never claim a run that did not happen.
- Run for real: git workflows in a temp repo, Python packaging/testing/pytest code, YAML parsing and validation (pyyaml/pydantic), FastAPI via TestClient if installable, MLflow local file store, DVC local if installable, pure-Python drift/monitoring maths (PSI, KS with numpy/scipy if available), Dockerfile lint by reading only.
- Not executable here (label "not executed", write from official docs, hedge versions): Docker builds if no daemon, Kubernetes, Helm, Airflow/Kubeflow/Prefect server, Triton, cloud services (AWS/Azure/GCP), Kafka/Spark clusters. Show the config/manifest, explain, and add a validation step that CAN run (YAML parses, schema checks).
- No vendor benchmark or price numbers. Cloud service names and limits are hedged; note "check current docs".
- Scope: Book 3 owns SQL; Book 1 owns ML theory; Book 2 owns LLM serving/RAG; Book 6 owns product/business. Book 4 stays on operating and shipping models. Part 9 (feature stores, streaming) keeps to concepts plus small runnable simulations.

## Part checklist (targets from plan.md)
| Part | Topic | Target | Wave A | Wave B | Wave C |
|---|---|---|---|---|---|
| 1 | Git, code quality, packaging, testing ML code | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 2 | Docker (images, layers, multi-stage, GPU) | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 3 | Kubernetes basics for ML, Helm, autoscaling | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 4 | Data and model versioning: DVC, MLflow, W&B | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 5 | Pipelines/orchestration: Airflow, Kubeflow, Prefect | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 6 | Serving: FastAPI, batch vs real-time, Triton, BentoML | 45 | ⬜ | ⬜ | ⬜ |
| 7 | CI/CD for ML, GitHub Actions, model registry | 40 | ⬜ | ⬜ | ⬜ |
| 8 | Monitoring: drift, data quality, alerting, retraining | 45 | ⬜ | ⬜ | ⬜ |
| 9 | Feature stores, streaming (Kafka, Spark) | 35 | ⬜ | ⬜ | ⬜ |
| 10 | AWS: S3, EC2, Lambda, SageMaker, ECR/ECS, IAM | 50 | ⬜ | ⬜ | ⬜ |
| 11 | Azure ML and GCP Vertex AI (comparison) | 35 | ⬜ | ⬜ | ⬜ |
| 12 | Cost, scaling, security, MLOps system design | 45 | ⬜ | ⬜ | ⬜ |

## Process notes
Split Wave B into agents of about 10 questions; tell agents to stop and report (not retry) at a spend limit and to keep files in their own scratch folders; commit and push WIP often (a stop hook demands it); run Part N Wave A for the next part in parallel with Part N-1 Wave B when budget allows.

## Next step
Part 6 Wave A (serving: FastAPI, batch vs real-time, Triton, BentoML; target 45). Test pip install fastapi uvicorn httpx pytest bentoml onnxruntime scikit-learn; run FastAPI via TestClient and a real uvicorn on localhost with curl/httpx, load tests only as tiny labelled-machine-specific demos; Triton/GPU/Docker-based serving 'not executed' (no daemon). Part 5 lessons: Airflow 3.3.2, Prefect 3.9, kfp 2.17 install in venvs under /tmp/claude-0/b5p05; each agent needs its own AIRFLOW_HOME/PREFECT_HOME; Airflow 3 differs from older docs. Part 4 lessons: dvc, mlflow, wandb(offline) install and run in a venv (/tmp/claude-0/ven/v may exist); set MLFLOW_DISABLE_TELEMETRY=true; agents must not write outside their dirs. Part 3 lessons: kubernetes-validate --strict works offline; no helm/kubectl; Part 2 lessons: hadolint-py and docker compose config work without a daemon. Part 1 lessons: pip works through the proxy (pytest, scikit-learn, ruff, mypy, uv installed); WebFetch fails (snippet-only sources); delete __pycache__ before committing.
