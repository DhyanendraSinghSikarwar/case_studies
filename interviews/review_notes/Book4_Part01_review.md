# Book 4 Part 1 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (git, code quality, packaging, testing ML code). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 15 / 16 / 9 | pass |
| All 7 template labels present, in order, in every answer; code fences balanced | pass for all 40 |
| Python blocks re-run standalone with `python3 -I` | 27 blocks: 13 run clean; 14 are fragments of multi-file demos (modules, tests, a CLI needing --config, an env var) that need sibling files, so they do not run alone. Their real runs are in each agent's `code/` folder and the pasted outputs come from those runs |

## What really ran (Python 3.13, git 2.43, pytest 9.1, scikit-learn 1.9, ruff, mypy, uv, pre-commit, hatchling/build, git-filter-repo, nbstripout, jupytext, hypothesis, pandera)
Temp-repo git workflows (reset/revert, reflog, bisect, cherry-pick -x, stash and worktree, filter-repo on a 20 MB file, submodule pin), packaging (wheel and sdist built, installed in a clean venv, extras, editable install), pytest suites for model code with an injected leak, Hypothesis finds, coverage and diff-cover, pre-commit with local hooks, a seeded flaky-threshold study (200 runs), a paired-bootstrap regression gate, a CODEOWNERS matcher, an AST smell detector.

## Findings kept in the text
- pandas 3 reports text columns as `str`, not `object`, so exact dtype-string checks break.
- 100% line coverage still passes with a bug present; branch coverage reports 86%.
- An unseeded 0.90 AUC threshold failed 5.5% of runs; a fixed seed made it fail every time; a 3-SE threshold failed 0.5%.
- scikit-learn 1.6.1 pickle loaded in 1.9.1 gives InconsistentVersionWarning.
- Thresholds such as 0.90 AUC and 0.85 accuracy are demo choices tied to seeded data, not recommendations.

## Not executed or hedged
GitHub/GitLab settings (branch protection, CODEOWNERS enforcement), hosted CI, pip-compile, ONNX, skops, Hydra, mutation testing, secret scanners (detect-secrets, gitleaks), twine upload, git-lfs server, reflog expiry defaults (check current docs), hosted-index pip forms. The Sculley et al. paper was cited from memory; the Google Rules of ML skew point came from a third-party mirror and is hedged.

## Evidence limits
No candidate-reported questions; every web fetch failed, so sources are snippet-only guides and job postings used only to frame the India angle (see research_notes/Book4_Part01_sources.md).
