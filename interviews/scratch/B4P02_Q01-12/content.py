# ---------------- Q1
answers.append(render(1, "q01",
say="An image is a read-only stack of layers plus metadata; a container is that image plus one thin writable layer and a running process, and when the container is removed the writable layer goes with it.",
explain="""
- **Image = recipe result.** Ordered, read-only layers (each is a tar of file changes, named by a content hash) plus config (CMD, ENV, user). Layers are shared: ten containers of one image store the image layers once.
- **Container = image + writable layer.** A write goes to a private copy-on-write layer on top. `docker diff` shows it: `A` added, `C` changed, `D` deleted.
- **What survives what.** `docker restart` or `stop` then `start`: the writable layer survives. `docker rm`, `docker run` again, `compose down` then `up`, a new node or a redeploy: new container, new writable layer, your change is gone. So 'gone after restart' usually means a new container was created.
- **`docker commit`** freezes the writable layer into a new image. It works, but there is no Dockerfile record, nobody can review or rebuild it, and it can capture junk and secrets. Use it only to debug. Real fix: change the code or the Dockerfile and rebuild.
- **Where runtime files should go.** Models, outputs and caches that must outlive the container go to a volume or bind mount, or to object storage and a model registry. Anything else written at runtime is throw-away by design.
- **Failure modes:** writing a big model into the writable layer is slow (copy-on-write) and is lost on `rm`; two replicas never see each other's writes; disk fills up on the node because nobody cleans stopped containers.
""",
example="""The image has `/app/model.pkl` = v1. Container c1 overwrites it with v2 and writes `/tmp/pred.log`. Container c2 from the same image still reads v1. `docker rm c1`, run again: v1. The toy script below mimics this with layers as dictionaries so you can check each line by hand.""",
code=[("python", ["layers_sim.py"]), ("bash", ["commands.sh"])],
cmds=["python3 -I layers_sim.py", "docker --version", "docker info 2>&1 | tail -2 | cut -c1-110"],
notrun="Real container commands (`docker run`, `diff`, `history`, `rm`, `commit`) are **not executed**: this sandbox has the Docker CLI but no daemon (`docker info` below shows it). What did run: the Python layer simulation, and a syntax check of the shell script (`bash -n`, silent = OK).",
followups="""
- *Why are layers shared?* They are addressed by content hash, so identical layers are stored and pulled once.
- *Is a volume part of the image?* No. A volume is storage outside the layer stack, mounted into the container path.
- *Does `docker stop` lose data?* No. The writable layer is removed only by `docker rm` (or `--rm` on exit).
""",
mistakes="""
- Saying 'the container lost the model on restart' when it was really recreated.
- Using `docker commit` as a deployment method.
- Storing models or user uploads in the writable layer.
- Thinking `RUN rm` in a later layer shrinks the image (the earlier layer still holds the bytes).
"""))

# ---------------- Q2
answers.append(render(2, "q02",
say="Docker reuses a layer only if the parent layer and the instruction (and for COPY, the file contents) are identical, so put what changes rarely first, copy only requirements.txt before pip install, and copy your code last.",
explain="""
- **How a hit is decided.** Same parent layer, same instruction text. For `COPY` and `ADD` the build also compares a checksum of the copied files (contents, not timestamps). For `RUN` it compares only the command string, not what the command would fetch today.
- **A miss breaks the chain.** Once one layer is rebuilt, every layer after it is rebuilt. That is why `COPY . /app` first is expensive: any file change (a notebook, a log, `.git`) busts pip install and the model download.
- **Fix:** `COPY requirements.txt` then `pip install`, then the heavy model step, then `COPY serve.py`. A code edit now rebuilds only the last COPY. Better still, do not bake a 500 MB model in the image; pull it at start or mount it (see Q7). Add a `.dockerignore`.
- **What still busts the cache:** a changed `requirements.txt`; an `ARG` such as `GIT_SHA` or `BUILD_DATE` that is *used* early (miss at first use, then everything after); `RUN date` or anything non-deterministic; changing the base tag or digest.
- **Stale-cache trap:** `RUN apt-get update` on its own line is cached for ever, so a later `apt-get install` uses an old package index and can 404. Keep `apt-get update && apt-get install ...` in one `RUN`. Same trap for `RUN git clone` or `curl` with no version: cached, so you never see the new data.
- **CI:** a fresh runner has an empty cache. Use a registry or CI cache export (`--cache-from` / `--cache-to`; check current docs for your CI).
""",
example="""Bad file, change one line of `serve.py`: COPY . /app is a miss, so pip install (about 10 minutes) and the model download rebuild too. Good file: six layers cached, two rebuild (the COPY and the CMD line). Edit `requirements.txt` in the good file: pip and everything after it rebuilds, which is correct.""",
code=[("dockerfile", ["Dockerfile.bad", "Dockerfile.good"]), ("python", ["cache_sim.py"])],
cmds=["python3 -I cache_sim.py", HC.format(f="Dockerfile.bad"), HC.format(f="Dockerfile.good")],
notrun="`docker build` is **not executed** (no daemon), so no real timings or layer IDs are claimed. What ran: the cache simulation (a model of the rule, not Docker's real code) and hadolint 2.15.1 on both Dockerfiles. Hadolint only flags style on the bad file (DL3059); it cannot see the cache problem.",
followups="""
- *BuildKit cache mounts?* `RUN --mount=type=cache,target=/root/.cache/pip` keeps the pip download cache between builds on one builder; it does not travel to a fresh CI runner by default.
- *Does touching a file bust COPY?* Contents decide, not mtime, so `touch` alone does not.
- *Why not copy requirements and the model in one go?* Different change rates; keep them in different layers.
""",
mistakes="""
- `COPY . .` before dependency install.
- Running `apt-get update` and `install` in different RUN lines.
- Putting `ARG BUILD_DATE` or the git hash at the top.
- Believing the cache is global; it is per builder and per machine unless exported.
"""))

# ---------------- Q3
answers.append(render(3, "q03",
say="Use one stage with compilers to build a virtualenv or wheels, then start a fresh slim stage and COPY --from only the virtualenv and the app, so build tools never reach the final image.",
explain="""
- **What is left behind:** compilers, headers, apt lists, pip caches, source tarballs. Only the files you copy cross the stage boundary. Each `FROM` starts a clean filesystem.
- **`COPY --from=builder /opt/venv /opt/venv`** copies files from the named stage (or an image, or a stage number). The venv must sit at the **same path** in the runtime stage, because venv scripts hold absolute paths.
- **`--target`:** `docker build --target test .` builds up to the `test` stage and stops. CI runs tests on that stage; production builds the last stage. BuildKit skips stages the target does not need.
- **Failure mode, missing shared library:** a wheel built or linked against `libgomp1` (OpenMP) imports fine in the builder but fails in a runtime that lacks it: `ImportError: libgomp.so.1: cannot open shared object file`. Fix: install the *runtime* package (not the `-dev` one) in the final stage. Find missing libs with `ldd` on the `.so` files in site-packages.
- **Other traps:** different Python minor version or OS release between stages (compiled extensions break); copying the venv but forgetting `ENV PATH`; running tests in the final stage so test tools ship.
""",
example="""In the file below, `build-essential` exists only in `builder`. The stage check script prints it as left behind, and `libgomp1` as kept because the runtime needs it. A wheel with a C extension that needs OpenMP imports fine in `builder` but not in `runtime` if you drop that one line.""",
code=[("dockerfile", ["Dockerfile"]), ("python", ["stage_check.py"])],
cmds=["python3 -I stage_check.py Dockerfile", HC.format(f="Dockerfile")],
notrun="`docker build`, `--target` and the import failure are **not executed** (no daemon). What ran: a small stage parser (checks every `COPY --from` points at a real stage and lists what apt installs per stage) and hadolint 2.15.1 (clean; two DL3008 apt-pin warnings are silenced with comments because pinning Debian package versions breaks when the mirror moves).",
followups="""
- *Why not just `pip install` then `apt-get purge` in one stage?* Possible in one RUN, but it is easy to leave residue; multi-stage is simpler to reason about.
- *Wheels instead of a venv?* `pip wheel -w /wheels` in the builder, then `pip install --no-index --find-links=/wheels` in the runtime. Same idea.
- *Does multi-stage make builds faster?* Not by itself; it makes the final image smaller. Cache rules from Q2 still apply.
""",
mistakes="""
- Venv in a different path in the final stage.
- Different base tags in the two stages.
- Installing `-dev` packages in the runtime stage.
- Putting pytest in the stage you ship.
"""))

# ---------------- Q4
answers.append(render(4, "q04",
say="My default is python:3.x-slim on a pinned Debian release for both a scikit-learn API and a PyTorch service; alpine is a trap for numeric Python, and distroless is for later hardening when you have a debug plan.",
explain="""
- **glibc versus musl.** Debian and Ubuntu use glibc. Alpine uses musl. Most prebuilt binary wheels (numpy, scipy, many ML libs) are tagged `manylinux` (glibc). pip on alpine looks for `musllinux` wheels; if none exist it compiles from source: slow builds, needs compilers, sometimes fails. Some libs also behave differently on musl.
- **slim** is Debian without compilers and many extra libs. Small and fine when wheels exist. If a package must compile, use a builder stage (Q3). You may need `libgomp1` for OpenMP.
- **full python image** includes compilers and tools: big; fine for a builder stage, not for runtime.
- **distroless** has no shell and no package manager: smaller attack surface, harder to debug. Debug with a debug variant, an ephemeral debug container, or `docker cp`. Worth it once the service is stable and you have a scanning and debug story. Python distroless needs care with the venv and the interpreter path.
- **ubuntu:** familiar and good when you need system packages or CUDA (Q5). Heavier than slim.
- **Tag choice:** pin minor version and OS release, such as `python:3.11-slim-bookworm`. Avoid `latest` and bare `3`, which change under you. For strict reproducibility add the digest (Q8). Check current docs for supported Python versions and OS releases.
- **My defaults:** sklearn API: `python:3.11-slim-bookworm`, install pinned wheels, run as non-root. PyTorch service: same base, with the right torch wheel (CPU-only index for CPU serving; for GPU see Q5).
""",
example="""The script below asks pip's own tag logic which platform tags this box accepts (glibc, so `manylinux`) and what an alpine box (`musllinux_1_2`) would accept. A wheel named `...manylinux2014_x86_64.whl` is accepted by the first and rejected by the second. So pip on alpine falls back to the source package.""",
code=[("python", ["wheel_tags.py"]), ("dockerfile", ["Dockerfile.sklearn", "Dockerfile.torch"])],
cmds=["python3 -I wheel_tags.py", HC.format(f="Dockerfile.sklearn"), HC.format(f="Dockerfile.torch")],
notrun="Image builds and size comparisons are **not executed** (no daemon) and no sizes are claimed. What ran: the wheel-tag check (uses the `packaging` library on this glibc host; the alpine side is emulated by asking for `musllinux` tags explicitly, not a real alpine run) and hadolint on both Dockerfiles. The torch version in the Dockerfile is an example; check current PyTorch docs.",
followups="""
- *Is alpine ever right?* For small Go or static binaries, or a tiny non-numeric Python service. Not for numpy, scipy, torch.
- *Why pin the OS release?* A new Debian release changes glibc and system libs under a floating `slim` tag.
- *Scratch image for Python?* No. Python needs an interpreter and libs; scratch is for static binaries.
""",
mistakes="""
- Picking alpine for size, then waiting for numpy to compile.
- Using `python:3` or `latest` in production.
- Shipping the full compiler image as the runtime.
- Moving to distroless with no way to debug.
"""))

# ---------------- Q5
answers.append(render(5, "q05",
say="nvidia/cuda has three flavours (base, runtime, devel); for a PyTorch pip wheel you usually do not need any of them, because the wheel brings its own CUDA libraries and a python-slim image plus the host driver is enough.",
explain="""
- **Flavours.** `base`: minimal CUDA runtime pieces. `runtime`: base plus the CUDA libraries (and cuDNN in the `cudnn-runtime` tags). `devel`: runtime plus compilers and headers (nvcc). Need `devel` only to compile CUDA code: custom ops, flash-attention style builds. Check Docker Hub for the tags that exist today.
- **Pip wheel carries CUDA.** The Linux PyTorch wheels ship the CUDA user-space libraries they need (check the current PyTorch install page for the index URL and CUDA tag). So the image only needs Python, the wheel, and a host with an NVIDIA driver and the NVIDIA Container Toolkit. The driver is never in the image (Q6).
- **Picking:** (1) python-slim plus the right wheel index: simplest, you control Python, usually the choice for pure inference. (2) `pytorch/pytorch` images: convenient, bundles tested versions, but bigger and you inherit its Python and OS. (3) `nvidia/cuda` runtime plus pip: when you need system CUDA libs, TensorRT, or NVIDIA's exact userland. Use a multi-stage with `devel` as builder and `runtime` as final if you must compile.
- **Size.** Roughly: slim plus CUDA wheel is large because the wheel itself is large (GBs); `devel` is the biggest; CPU-only wheel is much smaller. Measure with `docker images` or `docker history` on your build (not done here).
- **Failure modes:** `devel` in production (big, more CVEs); wheel built for a CUDA newer than the host driver supports; forgetting `--gpus` at run time; CPU wheel installed so `is_available()` is False.
- **Cannot test without a GPU:** `torch.cuda.is_available()`, a real forward pass on GPU, nvidia-smi inside the container, memory limits, NCCL. You can still lint, build and import-test on CPU.
""",
example="""Inference API, single model, pure PyTorch: Option A below (python-slim plus requirements with torch). Needs a custom CUDA extension compiled at build: multi-stage with `nvidia/cuda:...-devel` as builder and `...-runtime` as final. The tiny check script flags a devel image in the last stage.""",
code=[("dockerfile", ["Dockerfile", "Dockerfile.nvidia-runtime"]), ("python", ["flavour_check.py", "gpu_smoke.py"])],
cmds=["python3 -I flavour_check.py Dockerfile", "python3 -I flavour_check.py Dockerfile.nvidia-runtime", HC.format(f="Dockerfile"), HC.format(f="Dockerfile.nvidia-runtime"), "python3 -I -c 'import torch' 2>&1 | tail -1"],
notrun="Builds, `docker run --gpus`, `gpu_smoke.py` and anything touching CUDA are **not executed**: no daemon, no GPU, and torch is not installed here (last command shows it). What ran: the flavour lint and hadolint 2.15.1 (Option B gets DL3008, an apt pin warning, left visible on purpose). The `nvidia/cuda` tag is an example; check Docker Hub.",
followups="""
- *Why not always devel?* Size and attack surface; you do not need nvcc to run inference.
- *Do I need cuDNN in the image?* The PyTorch wheel includes what it needs; only the `nvidia/cuda` route needs a `cudnn` tag.
- *Can the image run on any GPU host?* Only if the host driver supports the CUDA version inside (Q6).
""",
mistakes="""
- Using `devel` as the final image.
- Installing the CPU wheel by mistake and blaming Docker.
- Putting the NVIDIA driver in the image.
- Assuming a CUDA image runs on CPU-only laptops for tests without a CPU fallback path.
"""))

# ---------------- Q6
answers.append(render(6, "q06",
say="The container never has its own GPU driver: the host driver and libcuda are injected into the container at start by the NVIDIA Container Toolkit's runtime hook when you pass --gpus, while the CUDA runtime and cuDNN come from the image.",
explain="""
- **Toolkit.** The NVIDIA Container Toolkit (host package) provides the runtime hook and `nvidia-ctk`. `nvidia-ctk runtime configure --runtime=docker` registers the runtime in `/etc/docker/daemon.json`; restart Docker after.
- **`--gpus all`** (or `--gpus 1`, or `device=0`) tells Docker to use that runtime for this container: it mounts the GPU device nodes and the host driver libraries (libcuda, nvidia-smi) in.
- **Who owns what.** Host: kernel driver, libcuda. Image: CUDA runtime, cuDNN, your framework. Rule of thumb: the CUDA version in the container may be *older* than what the driver supports, but not newer. (CUDA also has minor-version and forward-compat rules; check current NVIDIA docs for the exact compatibility table.)
- **Env vars.** `NVIDIA_VISIBLE_DEVICES` picks GPUs (`all`, `0,1`, `none`). `NVIDIA_DRIVER_CAPABILITIES` picks features (`compute,utility` for CUDA and nvidia-smi; `video` for NVENC). NVIDIA's own images preset them; a plain python-slim image does not, so set them or pass `--gpus`.
- **Debug 1: `could not select device driver "" with capabilities: [[gpu]]`.** Docker does not know the nvidia runtime. Toolkit missing, or not configured, or Docker not restarted. Check `docker info | grep -i runtimes`.
- **Debug 2: `nvidia-smi` works on the host, `torch.cuda.is_available()` is False in the container.** In order: container started without `--gpus`; a CPU-only torch wheel; the wheel's CUDA newer than the driver supports; driver capabilities missing; or running under a runtime that hides GPUs (check `NVIDIA_VISIBLE_DEVICES=void`). Run `nvidia-smi` *inside* the container first: if it fails, it is a runtime problem; if it works, it is a Python wheel problem.
""",
example="""Four cases in the helper script: (A) runtime not registered, (B) CPU wheel, (C) wheel needs CUDA 12.4 but the driver only supports 11.8, (D) image CUDA 11.8 on a driver that supports up to 12.6, which is fine. The compose GPU reservation is validated with `docker compose config` below.""",
code=[("bash", ["setup_and_debug.sh"]), ("yaml", ["compose.yaml"]), ("python", ["cuda_compat.py"])],
cmds=["python3 -I cuda_compat.py", "docker compose -f compose.yaml config | sed -n '1,14p'"],
notrun="**Not executed:** `nvidia-ctk`, `docker run --gpus`, `nvidia-smi` and any container start (no daemon, no GPU, no driver). What ran: the diagnosis helper (my simplified rules, not an NVIDIA tool) and `docker compose config`, which only validates and normalises the GPU `deploy.resources.reservations.devices` block; it does not prove a GPU will be allocated. `bash -n` on the shell script was silent (OK).",
followups="""
- *How does Kubernetes do this?* The NVIDIA device plugin and a `nvidia.com/gpu` resource; see the Kubernetes part.
- *MIG or sharing a GPU?* Possible with NVIDIA tooling; details depend on hardware, check current docs.
- *Can two containers share one GPU?* Yes by default with `--gpus`, with no memory isolation; one can OOM the other.
""",
mistakes="""
- Installing the driver inside the image.
- Forgetting to restart Docker after `nvidia-ctk runtime configure`.
- Saying 'container CUDA must equal host CUDA'. Host shows the *driver's* max CUDA version in nvidia-smi, not an installed toolkit.
- Debugging Python first when `nvidia-smi` inside the container already fails.
"""))

# ---------------- Q7
answers.append(render(7, "q07",
say="First measure which layers are big with docker history, then cut in this order: do not bake models or data in, CPU-only torch if no GPU, slim base and multi-stage, .dockerignore, pip --no-cache-dir; each step trades some risk.",
explain="""
- **1. Measure.** Rank layers by size (script below on a pasted `docker history` table). Fix the biggest first.
- **2. Take the model and data out.** Biggest win usually. Mount a volume or pull the model at start from a registry or object store. Saves the model size on every pull. Risk: start-up needs the model source and a download or cache; version the model separately and log which version is loaded.
- **3. CPU-only torch wheel** when serving on CPU. Saves the CUDA libraries (GBs). Risk: the same image will not use a GPU later; keep a GPU tag as a separate build.
- **4. Slim base plus multi-stage** (Q3, Q4). Drops compilers and build files. Risk: a missing runtime lib at import time.
- **5. One `RUN` that installs and cleans** (`apt-get install --no-install-recommends ... && rm -rf /var/lib/apt/lists/*`), `pip --no-cache-dir`, or a cache mount. A later `rm` in a new layer does not shrink anything. Risk: slower rebuilds if you drop caches without a cache mount.
- **6. `.dockerignore`** for `.git`, data, checkpoints, notebooks. Saves context upload time and layer size. Risk: ignoring a file you need; build fails loudly, which is good.
- **7. Remove dev dependencies** (pytest, jupyter) from the runtime requirements. Risk: need a separate dev requirements file.
- **Also:** pull time is about the sum of *new* layers on that node, so stable base layers and a thin app layer make rollouts fast. Registry layer compression and lazy pulling exist; check your registry docs.
""",
example="""Sample history table below totals 9.84 GB: pip layer 4.10 GB (41.7%), `COPY . /app` 3.20 GB (32.5%), model download 1.80 GB (18.3%), apt 0.61 GB. Stopping the baked model and adding a `.dockerignore` already removes about 5 GB of the 9.84 GB, before touching pip. (The table is made-up sample data for the script, not a real image.)""",
code=[("python", ["rank_layers.py"]), ("dockerfile", ["Dockerfile.slim"]), ("text", [".dockerignore"])],
cmds=["cat history.txt", "python3 -I rank_layers.py history.txt", HC.format(f="Dockerfile.slim")],
notrun="Building images, real `docker history` and measuring actual savings are **not executed** (no daemon); the layer table is a hand-written sample and no real size claims are made. What ran: the ranking script on that sample and hadolint on the slim Dockerfile.",
followups="""
- *Why not just compress or squash?* Squash hides the sharing of layers and hurts pull caching; fix the content instead.
- *Where does the model live then?* A volume, an init step, or object storage; version it and pin the version in config.
- *Distroless or alpine for size?* Last resorts here; the CUDA and torch libs dominate size.
""",
mistakes="""
- Deleting files in a later layer and expecting a smaller image.
- Optimising the base image while a 2 GB checkpoint sits in `COPY . .`.
- Dropping to CPU wheels without testing latency.
- No `.dockerignore`, so `.git` and data are in the build context.
"""))

# ---------------- Q8
answers.append(render(8, "q08",
say="FROM python:3.11 is a moving tag, so pin the base by digest, install from a hashed lockfile, and record image digest, git commit and data version with each model; that gives a repeatable build, not automatically repeatable model behaviour.",
explain="""
- **Why a tag drifts.** `python:3.11` is re-pushed with new patch versions and OS updates. Same Dockerfile, different image next month. Pin with tag plus digest: `python:3.11-slim-bookworm@sha256:...` (the tag is for humans, the digest is what is used). Cost: you must bump it on purpose; a bot can open the PRs.
- **pip drifts.** `pip install requests` takes whatever is newest, plus unpinned transitive dependencies. Use a lockfile from `uv pip compile --generate-hashes` or `pip-compile --generate-hashes`, install with `--require-hashes`. Hashes also catch a swapped package.
- **apt pins** (`pkg=1.2.3-1`) work only while that version is still in the mirror; old versions disappear, builds then fail. Better: pin the base image digest (system packages inside are frozen) and keep apt installs minimal. Debian snapshot archives exist for strict cases; check current docs.
- **Timestamps.** Layer metadata and file mtimes include build time, so the image digest changes every build. For byte-identical images use `SOURCE_DATE_EPOCH` and BuildKit's reproducible options (check current docs; support depends on version and exporter). Many teams stop at 'same content, different digest' and compare by contents.
- **Lineage record.** Store with each model: image digest (not tag), git commit, data version (a DVC rev or snapshot id), training config, seed. The script below writes it as JSON.
- **Honest difference:** a *reproducible build* gives the same environment. *Repeatable behaviour* also needs the same data, seeds, hardware and non-deterministic ops (GPU kernels, threading). Pinned image does not make training bit-identical.
""",
example="""Real run below: `uv pip compile --generate-hashes` produced a `requirements.txt` with 180 hash lines for `requests` and its four dependencies. `pip install --require-hashes --dry-run` accepts it. When I replaced every hash of `certifi` with zeros, pip refused: `THESE PACKAGES DO NOT MATCH THE HASHES`. The CI check fails `Dockerfile.unpinned` (rc 1) and passes the pinned one.""",
code=[("dockerfile", ["Dockerfile", "Dockerfile.unpinned"]), ("python", ["check_from.py", "record_run.py"]), ("bash", ["hash_demo.sh"])],
cmds=["python3 -I check_from.py Dockerfile; echo \"exit=$?\"", "python3 -I check_from.py Dockerfile.unpinned; echo \"exit=$?\"", "python3 -I record_run.py", "head -6 requirements.txt; grep -c -- '--hash' requirements.txt", "cat hash_out.txt", HC.format(f="Dockerfile.unpinned")],
notrun="The Docker build, the digest lookup and `SOURCE_DATE_EPOCH` byte-identical builds are **not executed** (no daemon). The digest in the Dockerfile is a placeholder of zeros, not a real image. What ran: `uv` 0.11.32 to generate the hashed lockfile from PyPI at the time of the run (versions in it are whatever PyPI served then), `pip --require-hashes --dry-run` with a good and a tampered file (`hash_out.txt` is the saved output of `hash_demo.sh`), the FROM-pin CI gate, and hadolint (flags the unpinned pip and pip cache on the bad file).",
followups="""
- *Does pinning by digest block security patches?* Yes until you bump it; schedule regular bumps and scans.
- *Tag or digest in a deployment manifest?* Digest, so every node runs the same bytes.
- *How do you rebuild a model from 6 months ago?* Image digest from the lineage record, git commit, data version; if the registry pruned the image, rebuild from the pinned Dockerfile and lockfile.
""",
mistakes="""
- Pinning direct dependencies but not transitive ones.
- Pinning the tag only (`python:3.11.9`): tags can still move.
- Claiming 'Docker makes ML reproducible' with unseeded training and unversioned data.
- Using `latest` for the *model* image too.
"""))

# ---------------- Q9
answers.append(render(9, "q09",
say="ARG and ENV values are stored in the image metadata and in the layers that used them, so anyone with the image can read them from docker history; use RUN --mount=type=secret for build-time secrets and pass runtime secrets at run time, never in the image.",
explain="""
- **Why ARG leaks.** `docker history` and `docker inspect` show the build steps and ENV values. A build `ARG` used in a `RUN` is recorded in that step's command text and can end up in the layer or in provenance data. An `ENV` is stored in the image config permanently and every container sees it.
- **Why a later `RUN rm` fails.** Layers are append-only. The file or token was written in an earlier layer; the `rm` layer only hides it. Anyone can read the earlier layer from the image tarball.
- **Build-time fix.** BuildKit secret mounts: `RUN --mount=type=secret,id=pip_token ...` makes the secret available as a file (default `/run/secrets/<id>`) for that one `RUN` only. It is not written into a layer. Supply it with `docker build --secret id=pip_token,env=PIP_TOKEN` or `src=file`. Needs BuildKit, the default in current Docker; check current docs.
- **Runtime secrets.** Pass at run time: environment variables from `--env-file` or the orchestrator, mounted secret files, or fetched from a secret manager (cloud IAM-based) at start. Env vars can still leak via `docker inspect` or crash dumps, so files or a manager are safer. Never bake keys into the image or the repo.
- **`.dockerignore` must list `.env`**, keys and credentials: `COPY . .` would otherwise copy them into a layer.
- **Failure modes:** a secret echoed in build logs; a token in a `pip.conf` copied into the image; secrets in the build context sent to a remote builder; rotating a leaked secret is the only real fix once an image is pushed.
""",
example="""`Dockerfile.leaky` has `ARG PIP_TOKEN`, `ENV API_KEY=sk-live-123456` and a `RUN rm`. The scanner finds four problems; the fixed file finds none, and hadolint (DL3064) agrees on the leaky one. The `sk-live` value is a made-up string.""",
code=[("dockerfile", ["Dockerfile.leaky", "Dockerfile.fixed"]), ("python", ["scan_secrets.py"]), ("bash", ["build_and_run.sh"])],
cmds=["python3 -I scan_secrets.py Dockerfile.leaky; echo \"exit=$?\"", "python3 -I scan_secrets.py Dockerfile.fixed; echo \"exit=$?\"", HC.format(f="Dockerfile.leaky"), HC.format(f="Dockerfile.fixed")],
notrun="`docker build --secret`, `docker history` and `docker run --env-file` are **not executed** (no daemon), so I did not show a real leak in a real history. What ran: the Dockerfile scanner (a simple name and pattern check; it will miss secrets with innocent names) and hadolint 2.15.1 on both files; `bash -n` on the shell script was silent.",
followups="""
- *Is `ENV` set only for the build safe?* `ARG` is not stored as a runtime env, but it still appears in history; use secret mounts.
- *SSH key for a private git dependency?* `RUN --mount=type=ssh` with `docker build --ssh default`.
- *Already pushed a leaked image?* Rotate the secret first, then delete the image; deleting alone is not enough.
""",
mistakes="""
- `ARG TOKEN` then `RUN rm`.
- `ENV` for API keys.
- Forgetting `.env` in `.dockerignore`.
- Printing the token in a build log, or `pip install -v` with credentials in the URL.
"""))

# ---------------- Q10
answers.append(render(10, "q10",
say="Run as a non-root user on a minimal pinned image, drop all capabilities, block privilege escalation, make the filesystem read-only with a tmpfs for scratch, keep secrets and the Docker socket out, and scan the image in CI.",
explain="""
- **Non-root `USER` (fixed UID, e.g. 10001).** If the app is exploited, the attacker is not root in the container. Fixed UID lets volume permissions and Kubernetes policies match.
- **Minimal pinned base, no secrets in layers** (Q4, Q8, Q9). Fewer packages mean fewer CVEs; pinning stops surprise changes.
- **`--read-only` with `--tmpfs /tmp`.** Attackers cannot drop files or modify code on the root filesystem. Scratch goes to memory-backed tmpfs.
- **`--cap-drop ALL`**, add back only what you need (a model API needs none, binding port 8000 needs none). **`--security-opt no-new-privileges`** stops setuid tricks gaining rights.
- **Never `--privileged`** (nearly full host access) and never mount `/var/run/docker.sock` (whoever has it controls the host Docker).
- **Image scan in CI** (Trivy, Grype or your registry's scanner; check current docs) fails the build on high severity findings. Scanning finds known CVEs only.
- **What breaks under read-only for ML apps:** libraries that write caches on first use: matplotlib config dir, Hugging Face / transformers cache, torch hub, `~/.cache`, pip, joblib temp, `__pycache__`, and `/tmp`. Symptom: `OSError: [Errno 30] Read-only file system`. Fix: point cache env vars at a tmpfs path (`MPLCONFIGDIR`, `HF_HOME`, `XDG_CACHE_HOME`), set `PYTHONDONTWRITEBYTECODE=1`, and mount the model directory read-only from a volume. Size the tmpfs: it counts against memory.
- **Failure modes:** a non-root user cannot bind port 80 (use 8000+); volume owned by root so the app cannot read it; `cap-drop ALL` breaks something needing `NET_BIND_SERVICE`.
""",
example="""The compose file sets every control. The audit script reads it back and prints PASS or FAIL per control. I made a bad copy (`read_only: false`, `privileged: true`) and it reports two failures. `docker compose config` normalised the file (it drops `privileged: false` because that is the default).""",
code=[("dockerfile", ["Dockerfile"]), ("yaml", ["compose.yaml"]), ("python", ["audit_compose.py"]), ("bash", ["run_hardened.sh"])],
cmds=["python3 -I audit_compose.py compose.yaml; echo \"exit=$?\"", "sed 's/read_only: true/read_only: false/; s/privileged: false/privileged: true/' compose.yaml > /tmp/c_bad.yaml; python3 -I audit_compose.py /tmp/c_bad.yaml | grep -E 'FAIL|failures'", "docker compose -f compose.yaml config | sed -n '1,20p'", HC.format(f="Dockerfile")],
notrun="`docker run` with these flags, the read-only failure itself, and an image scan are **not executed** (no daemon; Trivy and Grype not installed here). What ran: the compose audit (checks only that the settings are present in the file), `docker compose config` (validates and normalises the YAML) and hadolint 2.15.1 (clean).",
followups="""
- *Read-only root but the model needs to download?* Pre-load the model into a mounted volume, or point the cache at tmpfs and accept re-download on restart.
- *What does `no-new-privileges` stop?* A process gaining more privilege through setuid binaries or file capabilities.
- *Rootless Docker or user namespaces?* Extra layers; check current docs.
""",
mistakes="""
- Running as root 'because it works'.
- Mounting `docker.sock` for convenience.
- `--read-only` with no tmpfs, then the app crashes on first request.
- Treating a clean scan as proof of safety.
"""))

# ---------------- Q11
answers.append(render(11, "q11",
say="ENTRYPOINT is the fixed command and CMD is its default arguments; use exec form (JSON array) so your Python process is PID 1 and gets SIGTERM, because shell form makes sh PID 1 and it does not pass the signal on.",
explain="""
- **How they combine.** Final command is ENTRYPOINT plus CMD. `docker run image ARGS` replaces CMD only. `docker run --entrypoint X image` replaces ENTRYPOINT (and CMD is then X's arguments, unless you also pass args). If ENTRYPOINT is absent, CMD is the whole command.
- **Exec form** `CMD ["uvicorn", "app:app"]`: runs the program directly, no shell, no variable expansion. **Shell form** `CMD uvicorn app:app`: runs `/bin/sh -c "..."`; sh becomes PID 1 and your server is its child.
- **Signals.** `docker stop` sends SIGTERM to PID 1, waits (default 10 s, `-t` to change), then SIGKILL. PID 1 is special on Linux: a signal with no handler is ignored (no default kill). So sh as PID 1 does not forward SIGTERM and does not die: your app never hears it, then gets killed hard.
- **Effect on ML.** Hard kill means in-flight predictions are dropped (clients see resets), and a training run does not save its checkpoint or flush metrics. Fix: exec form, `exec` in entrypoint scripts, a SIGTERM handler that stops accepting work, drains and saves, and a stop timeout longer than your drain time (`docker stop -t`, `stop_grace_period`, or Kubernetes `terminationGracePeriodSeconds`).
- **tini or `--init`.** A tiny init as PID 1 forwards signals and reaps zombie children. Needed when your app spawns subprocesses (gunicorn workers, dataloader workers that become orphans), or runs a shell script that cannot `exec`. `docker run --init` injects one; or install tini in the image.
- **Uvicorn/gunicorn:** both handle SIGTERM for graceful shutdown when they are PID 1 or are reached by the signal; the failure is almost always shell form or an entrypoint script without `exec`.
""",
example="""The test below uses `unshare --pid --fork` (works here as root) so each launcher really is PID 1 of its own PID namespace, then sends SIGTERM from outside, as `docker stop` does. Exec form and an entrypoint that ends in `exec` handled it. `sh -c 'python3 server.py; true'` and an entrypoint without `exec` never delivered it. A Python app with no handler also ignored it, because PID 1 has no default kill action.""",
code=[("dockerfile", ["Dockerfile", "Dockerfile.entry-note"]) if False else ("dockerfile", ["Dockerfile"]), ("python", ["server.py", "signal_test.py"]), ("bash", ["entrypoint.sh", "entrypoint_noexec.sh", "entrypoint_generic.sh", "docker_cmds.sh"])],
cmds=["python3 -I signal_test.py", HC.format(f="Dockerfile")],
notrun="Real `docker run` and `docker stop` are **not executed** (no daemon). What ran: the signal test with real Linux PID namespaces (`unshare`), which reproduces the PID 1 behaviour but is not Docker itself, so the grace period was shortened to 1.5 s; and hadolint 2.15.1 on the Dockerfile. `tini` is not installed here, so `--init` was not tested. Note: a plain `sh -c 'python3 server.py'` with one command may be optimised by some shells into an exec; I did not rely on that and tested the `; true` form that cannot be.",
followups="""
- *Where do I trap SIGTERM in FastAPI?* Uvicorn handles it and runs shutdown events; add cleanup in the lifespan handler.
- *Why exec in the entrypoint?* `exec` replaces the shell with your process, so it becomes PID 1.
- *STOPSIGNAL?* Dockerfile instruction to change the stop signal (e.g. SIGINT); default is SIGTERM.
""",
mistakes="""
- Shell-form CMD with a pipe or `&&` chain.
- Entrypoint script that starts the server without `exec`.
- Default 10 s stop timeout with a 60 s checkpoint save.
- Handling SIGTERM in code but forgetting that the signal never arrives.
"""))

# ---------------- Q12
answers.append(render(12, "q12",
say="Liveness says the process is alive; readiness says the model is loaded and can predict; a Docker HEALTHCHECK should test readiness with a start period longer than model load, and Compose can then wait for it with depends_on condition: service_healthy.",
explain="""
- **HEALTHCHECK options.** `--interval` how often to run; `--timeout` when one check counts as failed; `--start-period` grace time at start where failures do not count toward retries; `--retries` consecutive failures before the status becomes `unhealthy`. States: `starting`, `healthy`, `unhealthy`.
- **Liveness versus readiness.** Liveness: should this process be restarted? Readiness: should it get traffic? A model server loading for 90 s is alive but not ready. Docker has one HEALTHCHECK, so choose readiness for it, or run both endpoints and let the orchestrator use each.
- **Good readiness endpoint:** returns 503 until the model object exists, then 200 after a tiny real predict. Do not make it call a slow or expensive path, and do not depend on downstream services, or one outage marks every replica unhealthy.
- **No curl in slim.** Use a tiny `healthcheck.py` with `urllib` (stdlib), or install curl on purpose. Use exec-form `CMD [...]` in HEALTHCHECK.
- **Compose.** `depends_on: model: condition: service_healthy` makes the gateway wait until the model service reports healthy. The model service must define a healthcheck, or Compose errors. It only orders start-up; it does not restart or reroute later.
- **Kubernetes.** Docker HEALTHCHECK is ignored there; use `livenessProbe`, `readinessProbe` and `startupProbe` instead (Kubernetes part). Docker's `unhealthy` status does not restart a container by itself outside Swarm.
- **Failure modes:** `start-period` shorter than load time (container flagged unhealthy while loading); `timeout` too short under load; health check that loads the model again; health passing but predictions broken (add a canary predict).
""",
example="""The stub server loads its 'model' for 3 s. Polling every 0.5 s shows `/live` returns 0 from the start while `/ready` returns 1 (fail) until about 3.5 s, then 0. In the real 90 s case set `start_period` above 90 s (the Dockerfile uses 120 s). The validator rejects a compose file where `gateway` waits on a service with no healthcheck.""",
code=[("dockerfile", ["Dockerfile"]), ("yaml", ["compose.yaml"]), ("python", ["health_server.py", "healthcheck.py", "timeline_test.py", "validate_compose.py"])],
cmds=["python3 -I timeline_test.py", "python3 -I validate_compose.py compose.yaml; echo \"exit=$?\"", "python3 -c \"import yaml;d=yaml.safe_load(open('compose.yaml'));del d['services']['model']['healthcheck'];yaml.safe_dump(d,open('/tmp/c12_bad.yaml','w'))\"; python3 -I validate_compose.py /tmp/c12_bad.yaml; echo \"exit=$?\"", "docker compose -f compose.yaml config | sed -n '/healthcheck/,/start_period/p;/depends_on/,/required/p'", HC.format(f="Dockerfile")],
notrun="A real container, the `HEALTHCHECK` status transitions and `docker compose up` ordering are **not executed** (no daemon). What ran: the stdlib health server and `healthcheck.py` in a timed loop (a Python simulation of the readiness idea, not Docker's scheduler), the compose validator (my script) on a good and a bad file, `docker compose config` (which normalised `start_period: 120s` to `2m0s`) and hadolint 2.15.1 (clean). The image's `src.api` module is not provided; the stub server stands in for it.",
followups="""
- *Why not curl?* Slim images do not ship it; Python stdlib is already there. Alpine/busybox may have wget but see Q4.
- *Health check hits the model on every interval?* Keep it cheap: check the object and one tiny input, or a cached 'last ok' flag.
- *Does Compose restart unhealthy containers?* Not by itself; use `restart` policies with care, or an orchestrator.
""",
mistakes="""
- No start-period, so a slow model load looks like a crash loop.
- A readiness check that only returns 200 from `/`.
- `depends_on` without `condition`, which only waits for the container to *start*.
- Health checks that call the database or other services.
"""))
