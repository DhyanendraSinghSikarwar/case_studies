# Book 4 Part 1 Sources & research notes (Git, code quality, packaging, testing ML code)

Date: 2026-10-26. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. Nine WebSearch calls were made. Every WebFetch attempt failed (getaddrinfo ENOTFOUND for www.datacamp.com and eugeneyan.com), so NO page was opened. All sources below are SEARCH SNIPPET ONLY (search tool summaries). No company-reported exact question was verified; 'Asked at' tags are source types, not companies.

## Pages OPENED (WebFetch)
None (fetch failures noted above).

## Snippet-only sources (not opened)
| Source | URL | What the snippet said (as summarised by the search tool) | Used for |
|---|---|---|---|
| DataCamp, MLOps interview questions | https://www.datacamp.com/blog/mlops-interview-questions | Git for code plus DVC for data and models for reproducibility and rollback; unit tests of preprocessing and feature code with pytest or unittest, before integration and performance tests; sample question "What are the ways of packaging ML models?" (no answer in snippet) | reproducibility, test pyramid, packaging (editorial guide) |
| Devinterview-io mlops-interview-questions, wecreateproblems, DEV Community (vivekk101), goodspace, Towards AI 101 questions | https://github.com/Devinterview-io/mlops-interview-questions and others | reproducibility lists: commit hash, data version, parameters, library versions, GPU type, metrics, model artifact; Docker for environment; CI assures changes are tested | run manifest question (editorial guides) |
| Eugene Yan, How to Test Machine Learning Code and Systems | https://eugeneyan.com/writing/testing-ml | pre-train tests (no trained parameters needed, e.g. probability range, output shape) versus post-train behaviour tests; pytest examples; train/test leakage check | model testing, leakage tests (educational article, not an interview report) |
| Marvelous MLOps, How to test ML code? | https://marvelousmlops.substack.com/p/how-to-test-ml-code | pytest setup, tests/ folder, unit versus integration tests | pytest questions |
| MLOps Zoomcamp testing notes (DEV Community) | https://dev.to/abdelrahman_adnan/mlops-zoomcamp-module-6-chapter-1-testing-and-quality-assurance-1ehf | model tests (behaviour, loading, inference) and data tests (schema, missing values, outliers) | data validation question |
| Miki Tebeka, LinkedIn Learning testing Python data science code | https://github.com/LinkedInLearning/testing-python-data-science-code-2477020 | schemas, approximate comparisons, regression testing with pytest and Hypothesis | Hypothesis, approx questions |
| Breck et al., ML Test Score (Google research PDF) | https://research.google.com/pubs/archive/aad9f93b86b7addfea4c419b9100c6cdd26cacea.pdf | 28 actionable tests and a scoring rubric for production readiness (scoring detail came from a GitHub rubric repo, not the paper); excludes generic unit-test coverage | testing pyramid, regression gate |
| Google Rules of Machine Learning | https://developers.google.com/machine-learning/guides/rules-of-ml/ | training-serving skew as a pitfall; mitigation of reusing code across training and serving came from a third-party mirror, to verify in Wave B before quoting | skew question |
| PhoenixNAP and DataCamp merge vs rebase pages, leyaa.ai | https://phoenixnap.com/kb/git-rebase-vs-merge | merge preserves history; rebase rewrites and linearises; rebase private branches and merge shared ones; force-push pitfall | merge/rebase question |
| GoLinuxCloud, Naukri Code360, Vskills, wecreateproblems Git lists | https://www.golinuxcloud.com/git-interview-questions-answers-developers-linux/ and others | reset vs revert, reflog, cherry-pick, bisect, stash as typical items | Git recovery questions |
| PEP 660; Xebia pyproject guide; editables docs | https://peps.python.org/pep-0660/ | editable installs via build_wheel_for_editable; pip install -e .; src layout recommended; wheel vs sdist; config changes need reinstall (third-party opinions flagged) | packaging questions; Wave B should check packaging.python.org text if reachable |
| Bangalore job postings (Cognizant MLOps Engineer, CommBank, JPMorgan Chase Software Engineer III MLOps, Hirist) | careers.cognizant.com, builtin.com, themuse.com, hirist.tech | Git, CI/CD, Docker, Python, MLflow/Kubeflow listed as required skills. These are postings, NOT interview reports | India-angle (GCC, IT-services, bank) framing only |

## Not found (evidence gaps)
- No page reporting actual MLOps/ML-engineer interview questions on Git or packaging for a named Indian company; round-by-round experiences would be on Glassdoor, AmbitionBox, Reddit (not reachable). India relevance is therefore from job postings plus expert design.
- No source found for: dependency pinning/lockfiles, pre-commit and mypy in ML repos, git filter-repo, flaky ML tests, bootstrap regression gates, private package indexes. Those questions are expert extensions or tagged with the generic Git/packaging sources.
- Sculley et al. 'Hidden Technical Debt in ML Systems' is cited from memory as a well-known paper; not searched.

## Design decisions
- 40 Qs: 15 three-star, 16 two-star, 9 one-star. Hard questions have seeded, checkable setups; no cross-references to other Q numbers inside the part.
- Hosted-service topics (GitHub branch protection, private package indexes, Hydra) are hedged concept questions, not executable.
- LLM serving left to Book 2; DVC/MLflow to Part 4; CI pipelines to Part 7; Docker to Part 2.

## What Wave B can really run (checked 2026-10-26 in this sandbox)
Python 3.13.17; git 2.43.0; git-lfs 3.4.1 (client; no remote server); git-filter-repo 2.47.0; numpy 2.5.3; pandas 3.0.5; pyyaml 6.0.3; pydantic 2.13.5; setuptools 68.1.2 (system) plus pip install worked (proxy allows PyPI): pytest 9.1.1, pytest-cov 7.1.0, scikit-learn 1.9.1, scipy 1.18.1, hypothesis 6.170.11, ruff 0.17.2, mypy 2.4.0, coverage 7.17.0, build 1.6.1, hatchling 1.32.4, twine 7.0.0, uv 0.13.5, pre-commit 4.7.0, nbstripout 0.9.1, jupytext 1.19.6, pandera 0.35.0. These were installed with pip as root into the system Python; a fresh Wave B agent may need to re-install if the sandbox is reset (pip install pytest scikit-learn ruff mypy hypothesis coverage pytest-cov build hatchling pre-commit nbstripout jupytext pandera git-filter-repo).
Not runnable: Docker daemon (CLI client 29.9.2 present, 'failed to connect to the docker API'); GitHub/GitLab settings; hosted package indexes (twine upload not run); pre-commit hook installation needs network to clone hook repos (use local hooks or `repo: local` in demos); web pages (WebFetch DNS fails).
Notes: Wave B must run git demos in a temp repo with git config user.name/email set locally and no git commands against this repo; seeds and versions printed in outputs.
