# Book 4 Part 4 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (DVC, MLflow, W&B, data and model versioning, lineage). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 15 / 17 / 8 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 40 |

The lead did not re-run the DVC and MLflow demos: they build throwaway repos and servers, and the pasted outputs come from each agent's real runs (scripts and raw outputs are in each agent's `code/` folder). Outputs that contain timestamps, temp paths or hashes will differ on a re-run.

## What really ran (dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0 offline, scikit-learn 1.9.1, git-lfs 3.4.1)
DVC with a local-directory remote: add, push, delete and pull cycles, pipelines with repro and dvc.lock, params and metrics diff, experiments (-S, queue, apply, branch), directory manifests, get/import/update, gc dry runs and real gc, merge conflicts in dvc.lock. MLflow on sqlite: tracking, autolog, signatures, registry versions, aliases and rollback, legacy stages, `mlflow run`, `mlflow models predict` and `serve` on localhost, a local `mlflow server`, `mlflow migrate-filestore`, `mlflow db upgrade`. W&B offline runs and artifact manifests. Toy Python simulations (lakeFS-style branch and merge, snapshot time travel with vacuum, OpenLineage-style event, tag-policy checker).

## Findings kept in the text (observed, not assumed)
- MLflow 3.17.2: plain `./mlruns` file store raises an error unless `MLFLOW_ALLOW_FILE_STORE=true`; the default tracking URI is `sqlite:///mlflow.db`; the legacy stage API still works with a deprecation note.
- `search_model_versions` returned an empty `aliases` list for a version that holds an alias; `get_model_version` shows it.
- Signature enforcement rejects int64 into a double column; only int32 and float32 widen.
- A RandomForest failed to log with an untrusted-sklearn-types (skops) error; the lab answer uses logistic regression.
- `dvc status -c` exits 0 even when data is not pushed (CI must parse output); `dvc repro --dry` was misleading for downstream stages; `dvc params diff` lists unused keys that `dvc status` ignores.
- Git does not restore DVC-tracked data: `dvc checkout` is needed after `git checkout`.
- An undeclared dependency leaves a stale output; deleting dvc.lock does not re-run a stage if the run cache restores the output.
- `dvc gc` dry-run text says "Removed" though files stay; after `gc -w -c` on the remote an old-tag pull fails.
- Same-seed and n_jobs 1 vs 4 scores were identical; two configs over 5 seeds gave p=0.18 (Welch).

## Not executed
S3/GCS/Azure/SSH remotes, hosted W&B (sync, sweeps, hosted artifacts), Postgres and SSO for MLflow, `mlflow models build-docker` and Docker-based serving, lakeFS, Delta, Iceberg, Spark, OpenLineage servers, Hugging Face Hub calls, GPU determinism, `dvc exp push/pull`, CI platforms.

## Hedged
The snippet claim that lakeFS took over DVC in late 2025 is unverified and hedged in Q31/Q33. The vendor comparison in Q28 comes from general knowledge, no prices. The DPDP Act remark and IT-services/GCC MLflow usage in Q28 are labelled as the writer's hedged observations. OpenLineage field names are hedged.

## Evidence limits
No candidate-reported questions found; every WebFetch failed, so sources are snippet-only guides, docs snippets and job postings (the India-hiring lab uses skills lists from postings, not interview reports). See research_notes/Book4_Part04_sources.md.

## Housekeeping
An early agent run created a stray `/no/such/dir/mlflow.db` outside the repo; the safety check refused deleting it, so it was left. Harmless; remove with `rm -r /no` if wanted.
