A = {}

A[41] = r'''**Say this first (1 line):** Compose is enough for one machine, such as a GPU VM, a demo or a small internal tool; once I need several machines, rolling updates, autoscaling or GPU scheduling across nodes, I move to an orchestrator.

**Then explain:**
- **Compose is good at:** describing a few services, volumes and networks in one file, one command to start (`docker compose up`), same file in dev and on the VM, `restart: unless-stopped` for simple recovery.
- **What it lacks:** self-healing across nodes (if the VM dies, everything is down), zero-downtime rolling updates and rollbacks, autoscaling on load, scheduling GPUs across machines, secrets and config management at scale, proper multi-node networking.
- **Swarm:** Docker's built-in clustering (`docker swarm init`, stacks). It adds multi-node, replicas and rolling updates with a small learning curve, but its community and ecosystem are much smaller than Kubernetes, and Docker has moved focus elsewhere. Hedge: check current Docker docs for its support status before choosing it for new work.
- **Rule for moving up:** move when you need **any two** of: more than one machine, uptime promises with rolling updates, autoscaling, many teams sharing GPUs, or audit and policy needs. Not before: an orchestrator is a team's worth of work.
- **Failure mode:** `restart: unless-stopped` hides crash loops. Without healthchecks and alerts, a model that crashes on load keeps restarting quietly.
- **Failure mode:** the Compose `deploy:` section is partly ignored outside Swarm/Kubernetes. GPU `reservations.devices` is honoured by Compose on a host with the NVIDIA runtime; `replicas` and `update_config` are not full rolling updates (check current docs).

**Example:** An internal summariser demo: one GPU VM, API + Redis, 20 users. Compose. Later, 3 models, 2 GPU nodes, a team that needs a deploy without downtime: orchestrator.

**Code:** a Compose file with a GPU reservation, and a deliberately broken one.
@@F:yaml:q41/compose.yml,q41/bad.yml@@

@@F:bash:q41/check.sh@@

**Output (my run):** docker compose v5.6.1. `config` validates and normalises without a daemon. Starting the stack and the GPU reservation actually working is **not executed** (no daemon, no GPU).
@@R:q41|docker compose -f compose.yml config||docker compose -f bad.yml config; echo "exit=$?"@@
Reading it: the GPU reservation block is accepted by the schema, and the typo `restrat` is rejected with a clear error. That checks syntax, not that a GPU exists.

**Follow-ups:**
- *Compose in production?* Fine for small internal tools with backups and monitoring; not for anything needing high availability.
- *Is Swarm dead?* Do not say that. Say its status needs checking in current docs and that most teams choose Kubernetes for new clusters.
- *Managed container services?* A cloud container service (check current docs) is a middle step: no cluster to run, but vendor-specific.

**Common mistakes:**
- Treating `restart: always` as high availability.
- Using Compose `deploy.replicas` and expecting zero-downtime updates.
- Moving to Kubernetes for a demo.
- Never validating the file (`docker compose config` in CI is free).
'''

A[42] = r'''**Say this first (1 line):** Both are right: `nvidia-smi` shows the newest CUDA the **driver** supports, `nvcc` shows the **toolkit** installed, and what matters is the CUDA runtime your framework or image actually uses, which must be no newer than the driver supports.

**Then explain:**
- **nvidia-smi** talks to the driver (on the host). Its "CUDA Version: 12.x" is the highest CUDA the driver can serve. It does not say what is installed.
- **nvcc --version** is the compiler from the CUDA toolkit installed in that environment, here 11.8. Only needed when you compile CUDA code (custom ops, some extensions).
- **Rule:** driver max CUDA >= runtime CUDA used by the code. Driver 12.x with toolkit 11.8 is a normal, working pair. The reverse (an image CUDA newer than the driver supports) fails (minor-version compatibility and forward-compat packages exist; check NVIDIA docs).
- **PyTorch wheels bundle their own CUDA runtime libraries** (hence `torch.version.cuda`). They do not need `nvcc` or a system toolkit; they need only the driver. A container may have no `nvcc` at all and still run torch on the GPU.
- **Inside the container, check:** `torch.version.cuda`, `torch.cuda.is_available()`, and `nvidia-smi` (it appears only when the container is started with the NVIDIA runtime, `--gpus`).
- **Checklist:** (1) host driver version and its max CUDA; (2) image CUDA tag (runtime vs devel); (3) framework wheel built for which CUDA; (4) cuDNN/NCCL versions; (5) GPU compute capability supported by that wheel; (6) the container started with GPU access. Tags and versions change, check Docker Hub and vendor docs.
- **Failure mode:** `is_available()` False inside the container usually means no `--gpus`/runtime, driver too old for the image, or a CPU-only wheel installed. It is not fixed by installing more toolkit.

**Example:** `nvidia-smi`: driver 550.54, CUDA 12.4. `nvcc`: 11.8. Image uses CUDA 11.8 libs. 12.4 >= 11.8, so it runs. Another host with driver max CUDA 11.8 pulling a 12.4 image: fails. The script encodes exactly this comparison.

**Code:** Python, run locally on a CPU-only machine. The two sample strings are pasted text, not from this machine.
@@F:python:q42/cuda_report.py@@

**Output (my run):** Python 3.13.17, CPU-only sandbox. `torch` is **not installed** here (my pip install from the PyTorch CPU index failed through the proxy), so `torch.version.cuda` and `is_available()` were **not executed**.
@@R:q42|python3 -I cuda_report.py@@
Interpreting honestly: on this machine the first block says only "no NVIDIA driver, no toolkit, no torch". It proves nothing about GPUs. The rest is the comparison logic on sample text. On a real GPU box I would also run `python -c "import torch; print(torch.version.cuda, torch.cuda.is_available())"` inside the container (not executed).

**Follow-ups:**
- *Do I need nvcc in the image?* Only to compile CUDA code. Use a `-runtime` base for serving; `-devel` for building extensions.
- *Mismatch between wheel CUDA and image CUDA?* The wheel's bundled runtime is what torch uses. The system CUDA matters for other libs and builds.
- *GPU architecture?* A new GPU may need a newer wheel/toolkit than an old one; check the framework's supported architectures.

**Common mistakes:**
- "nvidia-smi says 12.4 so I have CUDA 12.4 installed".
- Installing CUDA toolkit on the host to fix a container problem.
- Forgetting `--gpus all` (or the compose reservation) and blaming the image.
- Installing the CPU wheel by accident (`+cpu` suffix).
'''

A[43] = r'''**Say this first (1 line):** I keep the image small and pinned, put weights in a volume, pass the Hugging Face token at runtime, give the container enough shared memory, and use a healthcheck with a long start period because loading the model takes minutes.

**Then explain:**
- **GPU image:** start from the server's official image (a vLLM-style or Ollama-style image) or a CUDA runtime base; pin the exact tag or digest (check the project's current tags; never `:latest`). Run with the NVIDIA runtime / Compose GPU reservation.
- **Weights in a volume, not in the image:** weights are often many GB. In the image, every rebuild or pull moves them again, and the image becomes huge. Mount a named volume at `HF_HOME` so the download happens once and survives restarts. Bake weights in only for air-gapped or very fast cold-start needs, and then version the image by model.
- **Image size vs weight size:** the image (libs, CUDA) is usually small compared with the weights. Tune the layers you rebuild often, and keep the weights out of them.
- **Gated model token:** pass `HF_TOKEN` at runtime from the environment or a secret store. Never `ENV HF_TOKEN=...` or `ARG` (visible in `docker history` and the registry).
- **shm / ipc:** frameworks use shared memory between processes; Docker's default `/dev/shm` is small. Set `ipc: host` or `shm_size` (check your server's docs for the recommendation).
- **Healthcheck:** the port opens before the model is ready. Use a readiness endpoint and `start_period` of several minutes, so the orchestrator does not kill it mid-download. During start_period failed checks do not count.
- **Pinning:** server image tag, model id and revision, and Python deps if you build your own layer. A floating tag changes behaviour overnight.
- **Failure modes:** volume mounted read-only (cannot download); disk too small for weights; token missing gives a 401 at startup; two containers sharing one cache volume writing at once.

**Example:** A 15 GB model, 3 GB image. First start: downloads 15 GB into `hf_cache` (minutes). Restart: reads from the volume, only load time. Rebuild the image for a security patch: 3 GB pull, not 18.

**Code:** a Compose file (YAML) plus a validator (Python) that checks the policies above. `${VAR:?msg}` makes Compose refuse to start if the tag or model is not set.
@@F:yaml:q43/compose.yml@@

@@F:python:q43/validate.py@@

**Output (my run):** docker compose v5.6.1, Python 3.13.17. Starting this service, pulling the image, GPU access, the download and the healthcheck are **not executed** (no daemon, no GPU, no network to pull). The validator ran against the real normalised config, with fake values for the three variables, then against a deliberately bad copy (`:latest` and a literal token).
@@R:q43|python3 -I validate.py compose.yml; echo "exit=$?"||sed 's/vllm-openai:${VLLM_TAG:?set VLLM_TAG to a pinned release tag}/vllm-openai:latest/; s/HF_TOKEN:  .*/HF_TOKEN: hf_realtoken123/' compose.yml > /tmp/claude-0/bad43.yml; python3 -I validate.py /tmp/claude-0/bad43.yml; echo "exit=$?"||VLLM_TAG= docker compose -f compose.yml config --quiet; echo "exit=$?"@@
Reading it: the good file passes all seven checks; the bad copy fails the pin and the token check. The last command shows Compose refusing an unset tag. The image name `vllm/vllm-openai` and the `/health` path are my assumptions from the project docs I know; check the current docs before using them.

**Follow-ups:**
- *Why not copy the token into a secret file?* You can: Compose `secrets` or an orchestrator secret is better than env on shared hosts, because env shows in `docker inspect`. Check whether your server supports a token file.
- *Multiple GPUs?* `count: all` or device ids, plus tensor-parallel flags of the server (Book 2).
- *Cold start too slow?* Pre-pull the image, pre-warm the volume, or bake weights into a per-model image.

**Common mistakes:**
- Baking weights and the token into the image.
- A healthcheck that passes as soon as the port opens.
- Default 64 MB-class shared memory leading to cryptic worker crashes (check current default).
- Floating `latest` tag in production.
- No disk quota for the cache volume.
'''

A[44] = r'''**Say this first (1 line):** I group the CLI by what it does: run and inspect containers, look at logs and resources, move images around, build, and clean up; most of them need a daemon, so here I can only prove the flags exist from `--help`.

**Then explain:** in the order I would say it in a session.
| Step | Command | Meaning |
|---|---|---|
| start | `docker run -d -p 8000:80 -v data:/data --rm --name web img` | `-d` background, `-p host:container` publish a port, `-v` mount a volume, `--rm` delete on exit, `--name` give it a name. `-it` (= `-i -t`) is an interactive terminal. |
| look | `docker ps -a` | running and stopped containers |
| logs | `docker logs -f --tail 50 web` | follow output |
| shell | `docker exec -it web sh` | run a command in a running container |
| stop | `docker stop web` vs `docker kill web` | stop sends SIGTERM, waits (default 10 s), then SIGKILL; kill sends SIGKILL (or `-s`) immediately |
| inspect | `docker inspect --format '{{.State.Status}}' web` | read config and state as JSON or a template |
| files | `docker cp web:/app/out.csv .` | copy between container and host |
| usage | `docker stats --no-stream` | CPU, memory per container |
| build | `docker build -t img:1 -f Dockerfile --target final .` | build; `docker history img` shows layers |
| ship | `docker tag img:1 reg/img:1` then `docker push reg/img:1` | name and upload |
| offline | `docker save -o img.tar img:1` / `docker load -i img.tar` | move an image as a file |
| clean | `docker rm web`, `docker rmi img:1`, `docker system prune -a --volumes` | remove container, image, or everything unused (careful: `--volumes` deletes data) |

- **Order of a session:** build -> run -> ps -> logs -> exec -> inspect/stats -> stop -> rm -> tag/push -> prune.
- **Without a daemon:** `docker --help`, any `docker <cmd> --help`, `docker compose config` work. `build`, `run`, `ps`, `exec`, `logs`, `push`, `history`, `save`, `load`, `stats`, `system prune` need a daemon: **not executed**.
- **Failure mode:** `docker system prune -a --volumes` removes unused volumes, including a model-cache volume. Name volumes you care about and mount them to a running container, or do not prune with `--volumes`.
- **Failure mode:** `docker stop` that takes 10 seconds means the app ignored SIGTERM (Q38).

**Example:** "Container exits immediately." `docker ps -a` shows `Exited (1)`; `docker logs web` shows the traceback; `docker inspect --format '{{.State.ExitCode}}' web` gives the code; `docker run --rm -it --entrypoint sh img` to look inside.

**Code:** Python checks, by running `--help`, that every command and flag above exists in this CLI. Real run; no daemon needed. Then the commands that fail without one.
@@F:python:q44/drill_check.py@@

**Output (my run):** docker CLI 29.9.2. The check ran `docker <command> --help` for 18 commands. The error at the end is `docker ps` showing the daemon is missing; every real build, run, logs, exec, push and prune call is **not executed**.
@@R:q44|python3 -I drill_check.py||docker ps; echo "exit=$?"||docker build --help | sed -n 1,6p@@
Reading it: `ALL OK` means the flags exist in this client version, nothing more. `docker build --help` shows `docker build` is an alias of `docker buildx build` in this version, so BuildKit options apply.

**Follow-ups:**
- *`docker stop` vs `kill`?* Stop asks politely, then forces. Kill is immediate.
- *`rm` vs `rmi`?* `rm` deletes containers, `rmi` deletes images.
- *`exec` vs `run`?* `exec` enters an existing container; `run` creates a new one.

**Common mistakes:**
- `docker rmi` of an image that a stopped container still uses (need `rm` first or `-f`).
- Forgetting `--rm` and piling up stopped containers.
- `-p 80:8000` the wrong way round (it is host:container).
- Running `prune -a --volumes` on a shared box.
'''

A[45] = r'''**Say this first (1 line):** I would use one platform-owned base image per supported CUDA and Python combination, with thin per-project images on top, rebuilt monthly through CI, promoted only after tests pass, so teams control their libraries but not their OS and CUDA layer.

**Then explain:**
- **Fat single image vs per-project:** one fat image with everything is simple, but big, slow to pull, and one team's upgrade breaks everyone. Per-project images from a shared base keep the heavy common layers (CUDA, Python, core libs) shared and cached, and let each team pin its own libraries. A small number of bases (for example one per CUDA line) is the usual balance.
- **Base image (platform team):** CUDA runtime, Python, OS security patches, pinned common libraries via a constraints file, non-root user, labels, a smoke test. Versioned by month (`2026.10`), never overwritten. Per-project layers: their requirements lockfile and code.
- **Monthly rebuild:** rebuild the base on a schedule (OS patches), run tests, publish the new tag, open update PRs to projects. Projects pin the tag (and digest) so nothing changes under them.
- **Upgrade path for driver or CUDA:** check the fleet's driver supports the new CUDA first (matrix). Publish the new base next to the old one (status `current` / `previous` / `deprecated`), migrate project by project, remove the old base after a stated date.
- **CI:** build base, run smoke test (imports, framework version, CUDA check on a GPU runner), build a canary project on top, then promote the tag. Projects' CI builds, tests (Q35), scans and pushes.
- **Registry layout:** `platform/ml-base:<month>` (immutable tags), `team/project:<git-sha>` plus a release tag; keep digests in lock files. Check the registry's retention and immutability settings (cloud specifics: Part 10).
- **Protect from a bad base:** immutable tags, projects pin by tag or digest, canary projects built against the candidate first, a `previous` base kept available, rollback = change one line. Updates arrive as PRs, never as a silent change.
- **Failure modes:** `:latest` base in a project; a base built on a CUDA the fleet drivers cannot run; an unpinned base apt update changing libs between builds; no owner for the base.

**Example:** Base `2026.10` (CUDA 12.4, Python 3.12). The `fraud` project is on it, the `vision` project is on the 12.6 base but the fleet driver tops out at CUDA 12.4, and `legacy` is on a deprecated base. The check script flags the last two; `fraud` is ok.

**Code:** the folder layout (text), a base Dockerfile (hadolint ran on it), the matrix file (YAML) and the check script (Python).
@@F:text:q45/layout.txt@@

@@F:dockerfile:q45/base/Dockerfile,q45/demo/projects/fraud/Dockerfile@@

@@F:yaml:q45/matrix.yaml@@

@@F:python:q45/check_matrix.py@@

**Output (my run):** Python 3.13.17, pyyaml, hadolint 2.15.1. Building the base, pushing it, and GPU smoke tests are **not executed** (no daemon, no GPU, no registry). The matrix values and tags are examples; check current CUDA tags and driver compatibility in NVIDIA docs.
@@R:q45|python3 -I check_matrix.py matrix.yaml demo/projects; echo "exit=$?"||hadolint --ignore DL3008 base/Dockerfile; echo "hadolint exit=$?"||hadolint demo/projects/fraud/Dockerfile; echo "hadolint exit=$?"@@
Reading it: the script exits 1 when any project is on a deprecated base or a CUDA the fleet cannot run, so CI can block it. The two hadolint runs show a real warning (DL3042, pip cache) in the project Dockerfile that I left in on purpose; the base passes with apt pinning (DL3008) ignored by choice.

**Follow-ups:**
- *Pin by tag or digest?* Digest for reproducibility, tag for readability; keep both, let a bot update the digest.
- *What about a team that needs a different CUDA?* Offer a second base from the matrix; do not let teams build their own OS layer.
- *Who owns it?* A named platform owner with an on-call rota; a base without an owner rots.

**Common mistakes:**
- One mega image that every team must upgrade together.
- Overwriting a tag (`2026.10` rebuilt silently).
- Letting projects use `:latest`.
- Upgrading CUDA without checking the driver in the fleet.
- No rollback plan or canary.
'''
