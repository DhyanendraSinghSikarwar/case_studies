# Book 4 Part 2 Sources & research notes (Docker for ML)

Date: 2026-10-26. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. Six WebSearch calls plus one WebFetch attempt. WebFetch failed (getaddrinfo ENOTFOUND for docs.docker.com), so NO page was opened. All sources below are SEARCH SNIPPET ONLY (search tool summaries). No company-reported exact question was verified; 'Asked at' tags are source types, not companies.

## Pages OPENED (WebFetch)
None.

## Snippet-only sources (not opened)
| Source | URL | What the snippet said (as summarised by the search tool) | Used for |
|---|---|---|---|
| PracHub, Docker optimization, container fundamentals, and CI/CD for an ML model service | https://prachub.com/interview-questions/docker-optimization-container-fundamentals-and-ci-cd-for-an-ml-model-service | listed as an eBay applied scientist question: explain layers and build caching, then optimise a Python ML inference service image (company attribution is the site's claim, unverified) | layer caching, size reduction, weights-in-image questions |
| ResumeLens, containerizing ML models best practices | https://www.resumelens.org/blog/mlops/containerizing-ml-models-best-practices-for-docker-images | ML containers differ by large images from numerical libs, GPU isolation, determinism across hardware; cache ordering matters more with massive dependencies | ML-specific framing |
| Techoral Docker Interview Questions 2026; Cloud Soft Solutions 2026; KodeKloud; Adaface; MentorCruise; Second Talent | https://techoral.com/docker/docker-interview-questions.html and others | basics, Dockerfile practices, multi-stage builds, networking, Compose, security, CMD vs ENTRYPOINT, COPY vs ADD, scenario questions; difficulty tagged | general question coverage (editorial guides) |
| NVIDIA Container Toolkit user guide and runtime docs (versions 1.6-1.12); E2E Networks; HowToGeek; LinuxConfig | https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/ | --gpus flag; nvidia/cuda tags base/runtime/devel; NVIDIA_VISIBLE_DEVICES and NVIDIA_DRIVER_CAPABILITIES preset in NVIDIA images; container CUDA may be older than driver-supported, not newer; example docker run --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi (third-party). Snippet gave no current cuDNN tags; Wave B must hedge tags and say check Docker Hub | GPU questions |
| BuildKit syntax.md, Docker Hub docker/dockerfile, OneUptime BuildKit cache and secrets (2026-01), Opstree, a 2026 CI cache checklist | https://github.com/moby/buildkit (frontend/dockerfile/docs/syntax.md) | secret mounts keep secrets out of the image, ARG/ENV secrets show in history; pip cache mount pattern; cache mounts are not preserved by GitHub Actions cache by default; digest pinning is a trade-off; no source tied cache mounts to pip hash checking (treat as unverified) | secrets, caching, reproducibility |
| Bengaluru MLOps postings (Infosys-linked via weekday.works, Quantiphi-linked via builtinbengaluru, Skyworks, GrabJobs, transperfect) | e.g. https://builtinbengaluru.in/job/senior-mlops-engineer/3352157 | Docker and Kubernetes for model deployment, GPU/CUDA auto-scaling workloads, multi-GPU scheduling; these are postings, NOT interview reports. No Pune-specific or GCC-specific hits | India angle only |

## Not found (evidence gaps)
- No page reporting named-company Docker interview questions for Indian firms (Glassdoor, AmbitionBox, Reddit unreachable). India angle = postings plus expert design.
- No source found for: .dockerignore matching, entrypoint exec pattern, OCI layout internals, shm-size, exit 137, registry rate limits, Docker-in-K8s dockershim, base-image fleet strategy. These are expert extensions or tagged with the generic Docker guides. Wave B must verify technical claims against official docs if reachable, else hedge versions and say 'check current docs'.

## Design decisions
- 45 Qs: 17 three-star, 18 two-star, 10 one-star. Each prompt is self-contained, names a failure scenario or an artifact to produce, and says up front what cannot be executed.
- Scope: Kubernetes (Part 3), CI/CD design (Part 7), AWS ECR/IAM (Part 10) only as pointers; LLM serving internals stay in Book 2.

## What Wave B can really run (checked 2026-10-26 in this sandbox)
- Docker CLI 29.9.2 present; `docker info` shows Client plus 'failed to connect to the docker API at unix:///var/run/docker.sock' => NO daemon. `docker build/run/pull/push/images/history/scan` all NOT executable; label 'not executed' and write from docs.
- `docker buildx version` works (v0.38.1). `docker buildx build --check .` FAILS here (needs daemon). `docker buildx build --help`, `docker build --help`, `docker compose config --help` work. `docker compose version` v5.6.1 works.
- `docker compose -f file.yml config` WORKS without a daemon (validates and normalises a compose file; tested on a trivial file; GPU device reservation syntax not yet tested, Wave B should try). `docker compose up` not executable.
- hadolint: `pip install hadolint-py` WORKED via the proxy; `hadolint --version` gave 'Haskell Dockerfile Linter 2.15.1'; a test Dockerfile produced DL3007, DL3013, DL3042, DL3020. Binary is on PATH after install (reinstall if sandbox reset). Python module form does not exist; call the CLI.
- Python 3.13.17, pyyaml 6.0.3 installed; pip works (earlier parts installed pytest, uv, ruff, etc.). Not checked: dockerfile-parse, trivy, grype (likely not installable; label not executed). A hand-written Dockerfile parser or regex linter in Python is fine.
- Runnable by script: layer-cache simulation (hash of instruction plus file contents), layer-size ranking from a pasted history table, .dockerignore matcher (simplified), cgroup file reads, signal-handling tests (SIGTERM to a Python subprocess), entrypoint.sh with exec, OCI-layout toy builder (sha256, tarfile), JSON parsing of inspect/scan samples, YAML checks on compose and workflow files, torch/CUDA version printout only if torch installs (CPU-only; no GPU here, so is_available() False).
- Must be labelled 'not executed': any image build, container run, GPU access, nvidia-ctk, registry push/pull, buildx multi-platform build, image scanning against real images, prune, Docker Hub rate limits, ECR or other cloud registries.
