# Book 4 Part 2 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45 (Docker for ML). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-12, Q13-23, Q24-34, Q35-45; merged by heading: 45 of 45 merged, 0 skipped, 0 pending. No spend-limit stops.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45; star order and counts 17 / 18 / 10 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 45 |
| Python blocks re-run standalone | 41 blocks: 20 run clean; 21 are tools that take file arguments (sys.argv) or need a Dockerfile, compose file or checkpoint path beside them, or a missing package, so they do not run alone. The real runs are in each agent's `code/` folder and the pasted outputs come from those runs |

## What really ran
No Docker daemon exists here (`docker info` fails), so no image was built or run. Ran for real: hadolint 2.15.1 (via hadolint-py) on before/after Dockerfiles, `docker compose config` on compose files (including a GPU device reservation and a deliberately broken one), docker CLI `--help` checks for 18 commands, Python simulations (layer cache keys, .dockerignore matcher, OCI layout with sha256 digests, secret scanner, compose policy validators), real SIGTERM tests in PID namespaces via `unshare` (exec vs shell form), `uv pip compile --generate-hashes` and pip hash-mismatch rejection, a fork copy-on-write PSS measurement.

## Findings kept in the text
- Shell-form launchers and entrypoints without `exec` never receive SIGTERM; exec form and `exec` in the entrypoint do.
- hadolint is silent with no USER line and warns on `USER root`; an `ignore` comment does not apply if another comment sits between it and the instruction; hadolint reads `.hadolint.yaml` from the current directory.
- PyYAML parses the workflow key `on` as `True`.
- pip `--require-hashes` rejects a tampered lockfile.
- The sandbox uses cgroup v1 with no limit, so no OOM was reproduced; the answer says so.

## Not executed (stated in each answer)
Every docker build, run, push, history, commit, stop, prune, `--secret`, `--init`, buildx multi-platform, `compose up`, GPU and nvidia-ctk step; torch/CUDA checks (torch could not be installed through the proxy); Trivy, Grype, cosign, tini; registry and cloud-registry behaviour. Samples such as `docker inspect` JSON, scan reports with invented CVE IDs, manifest digests and image sizes are hand-written and labelled as such.

## Hedged ("check current docs")
GitHub Action versions, base image tags, torch and CUDA versions, the hadolint pre-commit rev, Kaniko status, Swarm status, vLLM image name and health path, MLflow env var names, Docker Hub rate limits.

## Evidence limits
No candidate-reported questions found; every WebFetch failed, so sources are snippet-only editorial guides and job postings (one PracHub snippet attributes a layer-caching question to a company, recorded as unverified). See research_notes/Book4_Part02_sources.md.
