# Book 4 Part 7 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (CI/CD for ML, GitHub Actions, model registry, promotion gates, supply chain). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops. Each agent used its own temp dirs, sqlite DBs and git repos.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 15 / 15 / 10 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 40 (the script flagged Q9 only because a "**Code CD:**" bullet in its explanation matched the label search; the labels themselves are in order) |

The lead did not re-run the demos (they use per-question temp repos and databases); pasted outputs come from each agent's real runs, with `run_all.sh`/`out.txt` in each agent's `code/` folder. Q36's output came from a one-off 50-run loop in a copy outside the repo.

## What really ran (actionlint 1.7.12, check-jsonschema 0.38.2, PyYAML 6.0.3, mlflow 3.17.2 on sqlite, pytest, ruff, scikit-learn, git 2.43)
actionlint and check-jsonschema (built-in GitHub workflow schema, offline) on good and deliberately broken workflows; MLflow registry with aliases, promotion with actor and run tags, idempotent and compare-and-set promotion, rollback ledger; gate, trigger, router, bump (semver tags with `git describe` and version sort), fairness-gate and OIDC sub-claim scripts with pytest; matrix expansion; a repo linter; pandas data checks; CycloneDX JSON from a pinned requirements file with SHA-256 tamper check; Argo CD and Flux manifests parsed and a values bump with `git revert`; a stub LLM judge gate.

## Findings kept in the text (observed)
- PyYAML parses the workflow key `on` as boolean `True`.
- actionlint does not check `id-token: write`, did not flag a secret pasted into a `run:` line, flags a custom `gpu`/`train` runner label until `.github/actionlint.yaml` lists it, and needs a `.git` directory to resolve a local reusable-workflow callee. check-jsonschema passes files actionlint rejects (missing `needs`, mistyped caller inputs, unknown runner labels).
- `pull_request_target` with a fork checkout passes both linters.
- pandas 3 reads text columns as `str`, which broke an `object` dtype check.
- MLflow alias `.version` is a string; comparing with an int silently broke idempotency (fixed in two answers and described).
- A flaky threshold test failed 13 of 50 runs; a seeded-band or statistical fix 0 of 50.
- A naive read-then-write alias move is not atomic; a concurrency group is what closes the race.

## Not executed
GitHub runners, environments and approvals, OIDC token exchange, branch protection, CODEOWNERS enforcement, cache save/restore, schedule and workflow_run behaviour, Dependabot, Argo CD, Flux, Jenkins, GitLab runners, self-hosted/GPU runners, Docker build/scan/push (no daemon), Trivy, Syft, cosign, `act`, `gh release create`, authenticated MLflow server, any real LLM call. Jenkinsfile and .gitlab-ci.yml were only parsed.

## Hedged ("check current docs")
Artifact limits and retention, reusable-workflow nesting, schedule disabling on inactive repos, cache scope and size, environment plan limits, a skipped job counting as success for required checks (Q29: verify in a sandbox repo), "prevent self-review" option, pre-commit hook ids, a March 2025 supply-chain incident recalled from memory, cosign flags, CycloneDX types, example action SHAs (recalled, not checked), empty-matrix rejection. Gate thresholds and CI minute inputs are example policy values and assumptions, no prices.

## Evidence limits
No candidate-reported questions found; every WebFetch failed, so sources are snippet-only guides. Gaps listed in research_notes/Book4_Part07_sources.md: SBOM/SLSA, fairness gates, GitOps for ML, LLM CI, conflicting MLOps maturity numbering.
