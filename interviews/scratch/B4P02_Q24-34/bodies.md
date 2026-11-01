=====Q24
**Say this first (1 line):** Hadolint reads the Dockerfile (and runs ShellCheck on the RUN lines) and flags smells like `:latest`, `ADD`, unpinned installs and root. It is a cheap gate in pre-commit and CI. It reads text only, so it cannot tell you the image is good.

**Then explain:**
- Each finding has a DL number. I read it as: what breaks, how likely, how cheap the fix is.
  - `DL3007` `:latest` means the build is not repeatable and rollbacks are guesses. Pin a tag, ideally a digest.
  - `DL3064` a secret-looking name in `ENV` or `ARG`. The value stays in image metadata and `docker history`. Fixing the line is not enough: rotate the token (see Q9).
  - `DL3020` (an error) use `COPY`. `ADD` can auto-extract tars and fetch URLs, which is surprising.
  - `DL3009` / `DL3015` apt lists left behind and recommended packages pulled in: bigger image.
  - `DL3008` / `DL3013` unpinned apt and pip packages: two builds a week apart give two different images.
  - `DL3042` pip cache kept in the layer (`--no-cache-dir`).
  - `DL3002` last `USER` is root. `DL3025` shell-form `CMD` makes `sh` PID 1 (see Q11).
  - `DL3059` many consecutive `RUN`s. Style, usually the first one I relax.
- What I suppress, and how. Put the reason on its own comment line, then `# hadolint ignore=DL3008` on the line directly above the instruction. For repo-wide choices use `.hadolint.yaml` with `ignored:` and a comment per rule.
  - I accept `DL3008` (apt pins) when the base image is pinned, because Debian rotates point versions and pins then break the build.
  - I never suppress `DL3007`, `DL3020`, `DL3002` or `DL3064` without a written reason in the PR.
- Wire-up: run it on every Dockerfile change, in a pre-commit hook (fast feedback) and in CI (the one nobody can skip). Set `failure-threshold` so info-level noise prints but does not fail the build. Check current docs for hook and action versions.
- What a linter cannot tell you: image size, whether the app starts, whether the model loads, whether a pinned package has a CVE (that is a scanner, Q32), whether the layer order gives good cache hits, whether `HF_TOKEN` is a real secret. Clean lint does not mean good image.
- Edge cases I hit in my own run. (1) The first bad Dockerfile had no `USER` line at all and hadolint said nothing about root. It only warned once I wrote `USER root`. A missing `USER` is the same risk, so a human review item. (2) Hadolint picks up a `.hadolint.yaml` in the current directory by itself. My "no config" run silently used my config until I moved it. (3) If a comment sits between the `ignore` line and the instruction, the ignore does not apply. My first attempt still printed DL3008.

**Example:** line 2 of the bad file is `ENV HF_TOKEN=hf_FAKE_not_a_real_token`. Hadolint says DL3064. I would also grep `git log -p` for the real token, because an ENV in an old commit is already leaked.

**Code:**
{{CODE:dockerfile:q24/Dockerfile.bad,q24/Dockerfile.good}}
{{CODE:yaml:q24/cfg/hadolint.yaml,q24/.pre-commit-config.yaml,q24/ci_fragment.yml}}
{{CODE:bash:q24/run.sh}}

**Output (my run):** hadolint 2.15.1 (pip `hadolint-py` 2.15.1.2), Python 3.13.17, PyYAML 6.0.3. The pre-commit and CI fragments were only parsed as YAML. The pre-commit hook and the GitHub Action were not run (no pre-commit run, no Actions here). `docker buildx build --check` needs a daemon, so it was not executed.
{{OUT:q24}}

**Follow-ups:**
- *Hadolint or a scanner?* Both. Hadolint checks how you wrote the file. Trivy-style scanners check what is inside the built image.
- *Can you fail only on errors?* Yes: `failure-threshold: error`. I start at `warning` and keep info visible.
- *Is there a BuildKit built-in check?* Recent BuildKit has a build-check mode (`docker buildx build --check`, check current docs). It needs a builder, so it did not run here.

**Common mistakes:**
- Silencing a rule globally to get green CI, with no reason written down.
- Treating a clean lint as a security review.
- Putting the `ignore` comment in the wrong place, so it silently does nothing.
- Fixing `DL3064` by deleting the line but leaving the real token in git history.

=====Q25
**Say this first (1 line):** I run JupyterLab as the data scientist's own UID and GID, bind-mount the repo, keep the home directory in a named volume, publish the port on localhost only, and reach it by SSH tunnel. It is a dev tool, not a production image.

**Then explain:**
- **Ownership.** A container runs as root by default, so files it writes into a bind mount are root-owned on the host. Fix: `--user "$(id -u):$(id -g)"` (compose: `user: "${HOST_UID}:${HOST_GID}"`). Then the host user owns what the notebook writes.
  - **A UID with no passwd entry has no home.** Set `HOME` to a writable path. Jupyter needs a writable config and runtime dir. I use a named volume (`ds-home`) so kernels, settings and caches survive container restarts.
  - Edge case: a new named volume copies the permissions of the image directory it covers. Make `/home/ds` writable for any UID in the image, or the first start fails with permission denied. Check this on the real box.
- **Port.** `-p 127.0.0.1:8888:8888`, not `-p 8888:8888`. The second form listens on every interface, and a token alone on a shared network is thin. Use `ssh -L 8888:localhost:8888 user@gpu-box`. Always set a token (`JUPYTER_TOKEN`), never an empty one.
- **GPU on a shared box.** `--gpus '"device=0"'` or compose `count: 1`. Taking `all` starves colleagues. Containers can share one GPU, but nothing here limits GPU memory, so agree on who gets which index. Also raise `--shm-size` for DataLoader workers (Q19).
  - **Base image.** A team-built image on a pinned CUDA and PyTorch base with the usual libraries (pandas, sklearn, matplotlib). Notebooks then start the same way for everyone.
- **Not a production image.** It has dev tools, mutable state, unpinned `pip install` from cells, big size, and often secrets pasted in notebooks. Production gets a slim, pinned, non-root image with a health check built from the code, not from a notebook.
  - **Docker group is root.** Letting users run `docker` on a shared box is close to giving them root (Q36). If that matters, look at rootless Docker or Podman (check current docs).

**Example:** alice (UID 1001) runs the container as `1001:1001`. She saves `train.ipynb`. On the host `ls -l` shows `alice alice`. Without `--user` it would show `root root` and she could not edit it from her shell.

**Code:**
{{CODE:yaml:q25/compose.yml}}
{{CODE:bash:q25/run.sh,q25/run_all.sh}}
{{CODE:python:q25/validate.py}}

**Output (my run):** Docker Compose v5.6.1, PyYAML 6.0.3. Starting the container was not executed (no daemon, no GPU). What ran: `docker compose config` (grep'ed to the lines that matter, with `HOST_UID=1001`), the missing-token failure, a PyYAML policy check, and `bash -n` on the run script. The sandbox user is UID 0, so I set 1001 by hand to show the interpolation.
{{OUT:q25}}

**Follow-ups:**
- *Why not just `chmod 777`?* It hides the real problem and makes every file writable by everyone on a shared box. Matching UIDs is cleaner.
- *VS Code dev containers?* Same ideas (bind mount, matching UID, GPU flag). Check current docs for the exact `devcontainer.json` fields.
- *Where do big datasets go?* A read-only bind mount (`:ro`), not copied into the home volume.

**Common mistakes:**
- `-p 8888:8888` with `--NotebookApp.token=''` on a shared network.
- Running as root, then not being able to edit or delete the files from the host.
- Forgetting `HOME`, so Jupyter fails writing its runtime dir.
- Shipping the notebook image to production because "it already works".

=====Q26
**Say this first (1 line):** An image is built for one CPU architecture. An M-series Mac builds arm64 by default, the GPU server is amd64, so the binaries do not match and Linux says `exec format error`. Build for the target with `buildx --platform`, ideally one native build per architecture.

**Then explain:**
- **Two architectures.** `linux/amd64` (x86-64) and `linux/arm64` (aarch64). Same Dockerfile, different base image variant, different wheels, different machine code.
  - **Manifest list (image index).** One tag points to a list of per-platform manifests. `docker pull` picks the entry that matches your machine. If the index has only arm64, an amd64 host fails. `docker buildx imagetools inspect <tag>` shows the list.
- **Two ways to build the other arch.**
  - Emulation (QEMU): `--platform linux/amd64` on the Mac works with no extra hardware, but is much slower, and heavy `pip` compiles can be painfully slow or flaky.
  - Native: build amd64 on an amd64 CI runner and arm64 on an arm64 runner, then merge them into one manifest list. Fast and reliable. Check current docs for what runners your CI offers.
  - For compiled languages, cross-compiling with `FROM --platform=$BUILDPLATFORM` plus `TARGETARCH` avoids emulation. For Python wheels it mostly does not help.
- **Wheels.** A missing arm64 wheel means pip compiles from source, or fails. CUDA builds of some ML libraries are published for amd64 and not for arm64 (or only some versions), so check the index. A Mac cannot use an NVIDIA GPU anyway: test CPU behaviour locally, build the GPU image for amd64 in CI.
  - **Checking.** `docker image inspect --format '{{.Os}}/{{.Architecture}}'` on a local image, `imagetools inspect` on a registry tag, or read the ELF header of the binary. `--platform` on `run` forces a platform and falls back to emulation.
  - **Failure mode.** On a Mac with emulation, a "works on my laptop" amd64 build is slow but correct. An arm64 image pushed as `:latest` over an amd64 one breaks the whole fleet. Push per-arch tags or one manifest list, never overwrite blindly.

**Example:** I build on an M2 Mac with `docker build -t api .` and push. The server pulls it and prints `exec format error`. The ELF header of the entrypoint binary says arm64 and the server is x86-64. Fix: CI runs `buildx build --platform linux/amd64,linux/arm64 --push`, and the tag now points to both.

**Code:**
{{CODE:bash:q26/commands.sh,q26/run_all.sh}}
{{CODE:python:q26/arch_check.py}}

**Output (my run):** Docker CLI 29.9.2, buildx v0.38.1, Python 3.13.17, x86-64 Linux. Real multi-platform builds, QEMU, `imagetools` and registry pushes were not executed (no daemon, no registry). The last line is my attempt, which failed on the daemon connection. The manifest list is a hand-written sample with fake digests. The ELF check is a teaching tool I wrote, not a Docker feature.
{{OUT:q26}}

**Follow-ups:**
- *Why is QEMU slow?* It translates every instruction in software. Compile steps suffer most.
- *Can I just pin `--platform linux/amd64` in `FROM`?* It works but hides the problem and forces emulation on Macs. Prefer `--platform` at build time.
- *Do I need arm64 at all?* Only if you run on arm machines (some cloud instances, Macs for dev). If the fleet is amd64 only, build amd64 and test on it.

**Common mistakes:**
- Pushing an arm64 build from a Mac to a tag the servers use.
- Believing `--platform` on `docker run` is free: it silently switches to slow emulation.
- Assuming a pip wheel exists for every architecture.
- Trying to test a CUDA image on a Mac.

=====Q27
**Say this first (1 line):** On spot instances the job will be killed, so I write atomic checkpoints often, resume from the latest one at start, and catch SIGTERM to save once more before exiting inside the stop grace period.

**Then explain:**
- **Where checkpoints go.** A mounted volume or an object store, never the container's writable layer (gone with `docker rm`). If the volume is local to the node, a replacement node loses it, so for spot use object storage, or copy to it after each save.
  - **Atomic write.** Write `state.json.tmp`, flush, `fsync`, then `os.replace` onto the real name. A kill in the middle leaves the old checkpoint intact, never half a file.
  - **Resume.** At start, load the latest checkpoint if it exists. A checkpoint needs more than weights: optimizer state, step counter, scheduler, RNG state, and the data position. Otherwise the resumed run is not the same run.
- **SIGTERM.** `docker stop` sends SIGTERM, waits (default 10 s, change with `docker stop -t` or `--stop-timeout`), then SIGKILL. The handler only sets a flag. The loop saves at a safe point and exits. Doing heavy work inside a signal handler is risky.
  - It only works if Python is PID 1 or gets the signal: use exec form `CMD ["python", ...]` or `ENTRYPOINT` with `exec` (Q11), or the shell swallows it.
  - Spot reclaim gives a short notice that differs by cloud (check current docs). If a step or an upload takes longer than that, the last periodic checkpoint is what you get. So save periodically too, not only on SIGTERM.
- **Idempotent output paths.** Write to `runs/<run-id>/step-N` and a final marker, so a retried job overwrites the same files, not a second copy.
  - **Logs to stdout** with `flush=True`, so the last lines before the kill reach the log driver.
  - **Exit codes.** 0 means done. A non-zero code (143 here, 128+15) tells the restart policy or orchestrator "interrupted, retry me". Exiting 0 after a partial run would mark the job finished.
  - **Multi-GPU.** In distributed training every rank must stop at the same step, so one rank cannot save alone. Use the framework's elastic or checkpoint support. Concept only here.

**Example:** step time 0.05 s, 50 steps, save every 10. I SIGTERM it at about 1 s. It had reached step 20, saved, exited 143. Second run printed `start at step 20` and finished at 50. The step it stopped at changes a little per run.

**Code:**
{{CODE:python:q27/train.py,q27/drive.py}}
{{CODE:bash:q27/docker_run.sh,q27/run_all.sh}}

**Output (my run):** Python 3.13.17. The signal test is real: a child process killed with SIGTERM, then restarted. The step number depends on timing, so a rerun may show another number (it was 20 here). The `docker run` command was not executed (no daemon, no GPU, no volume), only syntax-checked with `bash -n`.
{{OUT:q27}}

**Follow-ups:**
- *What about SIGKILL or a power cut?* Nothing can be caught. That is why periodic atomic checkpoints are the real protection and the handler is a bonus.
- *Why exit 143, not 0?* So the scheduler knows the work is not finished.
- *Why `--init`?* It reaps zombie child processes and forwards signals if your entrypoint is a shell or spawns children.

**Common mistakes:**
- Checkpointing into the container filesystem.
- Shell-form `CMD`, so SIGTERM never reaches Python.
- Writing the checkpoint in place, so a kill corrupts it.
- Saving only weights and resuming with a fresh optimizer and a reset learning-rate schedule.
- A grace period shorter than the save time.

=====Q28
**Say this first (1 line):** For most ML services I use a multi-stage build: install into a virtualenv in a builder stage with a pinned lockfile (pip with hashes, or uv), copy only the venv to the runtime stage, and pick the torch wheel by index URL. Conda or micromamba only when I need non-Python native packages.

**Then explain:**
| Tool | Strengths | Watch out |
|---|---|---|
| pip | everywhere, wheels, `--require-hashes` | slower resolver, no lockfile by itself (pair with pip-compile or similar) |
| uv | very fast resolve and install, real lockfile (`uv.lock`) and `pip compile` with hashes | newer tool: pin its version in the image |
| conda / micromamba | non-Python libs (compilers, CUDA bits, geo stacks), solves binary compatibility | bigger envs, slower solves, licence and channel choices; micromamba is a small static binary |
- **Cache.** `pip --no-cache-dir` keeps layers small but redownloads every build. A BuildKit cache mount (`RUN --mount=type=cache,target=/root/.cache/pip`) keeps the download cache between builds on the same builder, and it is not stored in the image. On ephemeral CI runners the mount is empty each time unless you save it (Q33).
- **torch wheel flavour.** The index URL decides it. `--index-url https://download.pytorch.org/whl/cpu` gives a CPU wheel with no CUDA libraries, which is much smaller than the default Linux wheel that ships CUDA libraries (that is a size by reasoning, I did not measure). Check the PyTorch install page for the current URL scheme. Use `--index-url` for torch, not `--extra-index-url`, so another index cannot shadow it (dependency-confusion risk).
- **venv in the image.** `python -m venv /opt/venv` in the builder, then `COPY --from=builder /opt/venv /opt/venv` in the runtime stage and put it on `PATH`. The compilers, pip cache and headers stay behind. Both stages must use the same Python minor version and OS, since a venv holds absolute paths.
  - **pip as root.** Inside a throwaway builder with a venv it is fine. System-wide `pip install` as root in the final image can overwrite OS-managed Python packages. Newer Debian Pythons also refuse system pip installs (PEP 668, check your base). The final stage should not run pip at all.
  - **Lockfile and hashes.** A hashed requirements file makes pip refuse any file that does not match, so a poisoned or silently replaced wheel fails the build.
- **Size by reasoning.** Variant A (pip + venv, CPU torch) is smaller than a CUDA wheel variant by roughly the CUDA libraries it skips. The uv variant has the same final layers as A: the size difference is build time, not image size. A conda image is typically bigger unless you `conda clean` and avoid duplicate libraries.

**Example:** `requirements.in` has `packaging`. `uv pip compile --generate-hashes` wrote the pin and two hashes (shortened below). Feeding pip a requirement with a wrong hash made it stop with "THESE PACKAGES DO NOT MATCH THE HASHES".

**Code:**
{{CODE:dockerfile:q28/Dockerfile.pip,q28/Dockerfile.uv}}
{{CODE:bash:q28/run_all.sh}}

**Output (my run):** hadolint 2.15.1, uv 0.11.32, pip from Python 3.13.17. Image builds were not executed (no daemon), so neither Dockerfile was built and no sizes were measured. The `ghcr.io/astral-sh/uv:0.11.0` tag and `torch==2.5.1` in the files are examples I did not verify against the registries. Pin tags that exist when you build. The compile output hashes are shortened with `...` in the paste.
{{OUT:q28}}

**Follow-ups:**
- *uv or pip in production?* Either, with a lockfile and hashes. uv is faster in CI. Pick one and pin it.
- *Why conda at all?* A package that needs a native library the wheel does not bundle, or a stack that is not Python-first.
- *Does the cache mount change the image?* No. It is a build-time directory.

**Common mistakes:**
- `pip install` without a lockfile, so two builds differ.
- Forgetting `--no-cache-dir` and not using a cache mount either.
- The default torch wheel in a CPU-only service.
- Different Python versions in builder and runtime stage.

=====Q29
**Say this first (1 line):** I go from outside in: `docker ps -a` for state and exit code, `docker logs` for the app's last words, `docker inspect` for ExitCode, OOMKilled and Error, then a shell in the image with a different entrypoint. The exit code usually names the cause.

**Then explain:**
- **Triage order.**
  1. `docker ps -a`: restarting, exited, or never created? How many restarts?
  2. `docker logs --tail 100`: a Python traceback means the app broke. Empty logs mean the process never started.
  3. `docker inspect --format '{{json .State}}'`: `ExitCode`, `OOMKilled`, `Error`. Runtime errors (exec failures) appear in `Error`, not in logs.
  4. `docker events`: die, oom and restart in time order.
  5. `docker run --rm -it --entrypoint sh <image>`: bypass the broken entrypoint and poke around (`ls -l`, `ldd`, `env`, `python -c "import ..."`).
  6. `docker exec -it <name> sh` only works while it is up, so a restart loop needs step 5.
- **Symptom to cause.**
| Symptom | Likely cause | Check |
|---|---|---|
| `exec format error` | image arch differs from host (Q26) | `docker image inspect` arch |
| `no such file or directory` on a script that exists | CRLF line ending in the shebang, or missing interpreter | `od -c script.sh` shows `\r` |
| `permission denied`, exit 126 | missing executable bit, or a noexec mount | `ls -l`, `chmod +x` |
| exit 127 `command not found` | binary not in the image or PATH, or a missing shared lib message | `which`, `ldd` |
| `error while loading shared libraries` | runtime stage lacks a lib the wheel needs (Q3) | `ldd` on the `.so` |
| exit 137 plus `OOMKilled: true` | memory limit hit (Q19) | `docker inspect`, `dmesg` |
| exit 143 | SIGTERM, a normal stop | who stopped it? |
| exit 1 plus a traceback | app error: import, config, missing model file | `docker logs` |
| `address already in use` | host port taken by another process | `ss -ltnp`, change `-p` |
| runs, but cannot find files | wrong `WORKDIR` or a path built relative to it | `pwd`, `ls` in a shell |
- **Restart loops hide failures.** `--restart always` keeps relaunching a crash. Look at `RestartCount` and the logs of the previous run.
- **Exact exit codes for exec failures differ by Docker version** (126, 127 or 128, with the reason in `State.Error`). Read the text, not just the number.

**Example:** `api-3` is in state `created`, exit 128, error `exec /app/start.sh: no such file or directory`, and the file exists. The cause is a CRLF line ending: the kernel looks for an interpreter literally named `/bin/sh\r`. The fix is `dos2unix` or `tr -d '\r'`, plus `.gitattributes` `* text=auto eol=lf` for scripts.

**Code:**
{{CODE:bash:q29/commands.sh,q29/crlf_demo.sh,q29/run_all.sh}}
{{CODE:python:q29/triage.py}}

**Output (my run):** Python 3.13.17, the sandbox shell. Docker commands were not executed (no daemon). The inspect JSON is a hand-written sample (seven made-up containers), parsed by a script I wrote, so the diagnosis text is my own mapping, not Docker output. The CRLF, missing-x-bit and not-found cases ran for real in a plain shell. A container shows "no such file or directory" for the CRLF case, my shell words it "required file not found".
{{OUT:q29}}

**Follow-ups:**
- *Logs are empty. Now what?* The process probably never started: read `State.Error`, then override the entrypoint.
- *Container is up but unhealthy?* Look at the health status and what the check runs (Q12).
- *How do I stop CRLF coming back?* `.gitattributes` with `eol=lf`, and lint shell scripts in CI.

**Common mistakes:**
- Reading only `docker logs` and missing `State.Error`.
- Running `docker exec` on a container that keeps dying.
- Treating 137 as "a bug in my code" before checking OOMKilled.
- Editing scripts on Windows without LF settings.

=====Q30
**Say this first (1 line):** Apps should log to stdout and stderr and let Docker handle the files. The default `json-file` driver does not rotate, so set `max-size` and `max-file`, and clean images and cache on a schedule or the GPU server's disk fills up.

**Then explain:**
- **stdout and stderr.** The container runtime captures them, `docker logs` reads them, and log shippers read them from the driver. Logging to a file inside the container writes to the writable layer, grows unseen, and dies with the container.
  - **json-file default.** Docker's default driver keeps all output in one JSON file per container under `/var/lib/docker/containers/...`, with no size limit unless you set one. A chatty training loop printing every step can fill a disk.
- **Rotation.** `log-opts` `max-size` and `max-file`. The values must be strings (`"50m"`, `"3"`). The worst case per container is `max-size x max-file`. A change in `daemon.json` needs a daemon restart and only applies to containers created after it. Existing containers keep their old settings until recreated.
  - **Other drivers at a glance.** `local` (rotating by default, check docs for defaults), `journald`, `syslog`, `fluentd`, `gelf`, cloud drivers, and `none`. Some remote drivers limit what `docker logs` can show (check current docs).
- **Where the disk goes.** `docker system df` splits images, containers, local volumes and build cache and shows a RECLAIMABLE column. On a GPU box with many 8 GB images, each retrained tag adds the layers that differ (shared base layers are stored once).
- **Prune, what each deletes.**
| Command | Deletes |
|---|---|
| `docker image prune` | dangling images (untagged) only |
| `docker image prune -a` | every image not used by a container, stopped ones count as used |
| `docker container prune` | stopped containers |
| `docker builder prune` | build cache |
| `docker volume prune` | unused anonymous volumes (`-a` adds named volumes: possible data loss) |
| `docker system prune` | stopped containers, unused networks, dangling images, build cache |
| `docker system prune -a --volumes` | the above plus all unused images and unused volumes. Dangerous on a box with checkpoints in volumes |
  - **Safe habit.** Run `docker system df` first, prune images with `--filter until=...` on a schedule, keep checkpoints on a bind mount or object store, and keep `/var/lib/docker` on its own disk so a full disk does not take the OS down.
  - **Failure mode.** `prune -a` also removes the old image you wanted for a rollback. Keep the last known-good tag in use or in the registry.

**Example:** a training container prints 200 bytes per step for a month with no `max-size`. The file grows forever. With `50m x 3` the same container can never hold more than 150 MiB.

**Code:**
{{CODE:json:q30/daemon.json}}
{{CODE:bash:q30/commands.sh,q30/run_all.sh}}
{{CODE:python:q30/check_daemon.py,q30/rotation_sim.py}}

**Output (my run):** Docker CLI 29.9.2, Python 3.13.17. Nothing was pruned and `docker system df` could not connect (no daemon). The flag names come from the real `--help` output. The rotation script is my toy model of the idea (bytes kept stay under the cap), not Docker's code. `bad_daemon.json` has a trailing comma and numbers instead of strings; Python's parser stops at the comma first, so the string-type check did not get to run on that file.
{{OUT:q30}}

**Follow-ups:**
- *Can I set limits per container?* Yes: `--log-opt max-size=50m --log-opt max-file=3` on `docker run`.
- *Do logs survive `docker rm`?* No, with json-file they go with the container. Ship them to a log system if you need them.
- *Does `docker logs` work with every driver?* No, see the docs for your driver.

**Common mistakes:**
- Unbounded `json-file` on a long-running job.
- Numbers in `log-opts` instead of strings.
- Expecting a `daemon.json` change to apply to running containers.
- `docker system prune -a --volumes` on a shared box.

=====Q31
**Say this first (1 line):** In Compose I request a GPU with `deploy.resources.reservations.devices` (driver nvidia, capabilities gpu), keep a base `compose.yml`, and layer dev and prod settings with override files and profiles. It runs one VM. It is not an orchestrator.

**Then explain:**
- **GPU request.** Under the service: `deploy.resources.reservations.devices` with `driver: nvidia`, `count: 1` (or `device_ids`), `capabilities: [gpu]`. It needs the NVIDIA Container Toolkit on the host (Q6). `docker compose config` only checks the file. A missing runtime shows up at `up` time. Newer Compose also has a short `gpus:` form (check current docs).
- **Override files.** `compose.yml` plus `compose.override.yml` are merged automatically for plain `docker compose up`. That is my dev layer: bind-mount source, `build: .`, debug logs, `restart: "no"`, published port. For prod I name files explicitly: `-f compose.yml -f compose.prod.yml`. In that case the override file is not read, which my check confirms.
  - **Merge rules.** Scalars are replaced, mappings are merged, and lists such as ports and volumes are combined. So keep ports out of the base file or you cannot remove them in prod.
  - **Profiles.** `profiles: ["monitoring"]` keeps optional services (Prometheus, a notebook) off unless asked with `--profile`.
- **Restart policies.** `no`, `always`, `on-failure[:n]`, `unless-stopped`. Dev: `no`, so crashes are visible. Prod: `always` or `unless-stopped`.
  - **Limits.** `deploy.resources.limits` for CPU and memory. A model with no memory limit can take the host down.
  - **Env-specific.** Image tag from `${TAG}`, secrets by `env_file` or the platform, never baked into the file.
- **Compose vs orchestrator.** Compose gives you one host: no scheduling across machines, no self-healing if the VM dies, no rolling updates or autoscaling, GPU allocation by hand (Q41, and Kubernetes in a later part).

**Example:** the base file has the GPU reservation and a memory limit. Dev adds a code bind mount and port 8000 on all interfaces. Prod adds `restart: always`, port `127.0.0.1:8000` behind a reverse proxy, and a larger memory limit.

**Code:**
{{CODE:yaml:q31/compose.yml,q31/compose.override.yml,q31/compose.prod.yml}}
{{CODE:python:q31/check.py}}
{{CODE:bash:q31/run_all.sh}}

**Output (my run):** Docker Compose v5.6.1, PyYAML 6.0.3, Python 3.13.17. `docker compose config` worked without a daemon and normalised the GPU block. Starting the stack (`up`) was not executed (no daemon, no GPU), so the host runtime and the actual GPU grant are unverified. The memory values print in bytes (16 GiB, 24 GiB).
{{OUT:q31}}

**Follow-ups:**
- *Will `docker compose up` fail with no GPU?* Yes, at start. Config validation will not catch it.
- *`depends_on` and health?* See Q12 and Q14.
- *Can Compose scale across hosts?* Not by itself. That is where an orchestrator starts.

**Common mistakes:**
- Putting dev-only ports and bind mounts in the base file.
- `count: all` on a shared box.
- Trusting `compose config` as proof the GPU works.
- Forgetting that `-f` replaces the automatic override file.

=====Q32
**Say this first (1 line):** A scanner lists the OS and Python packages in an image and matches them to known CVEs. Most findings come from the base image, so I scan the final image, fix what has a fix and is reachable, rebuild on a schedule, and gate CI with a written policy and expiring waivers.

**Then explain:**
- **What gets scanned.** OS packages (apt) and language packages (pip). Tools I would name: Trivy, Grype, Docker Scout. Availability and flags change, so check current docs. None are installed here.
  - **SBOM.** A software bill of materials: the list of packages in the image (formats such as SPDX and CycloneDX). Store it with the image so you can answer "are we affected?" for a new CVE without rescanning everything.
- **Base image drives most findings.** A newer base tag or a slimmer base (Q4) removes many at once. A multi-stage build keeps compilers out of the final image. Findings that exist only in the builder stage are not shipped, so scan the final image.
- **Triage.** Ask four questions: is there a fix, is the package in the runtime stage, is the vulnerable code reachable in how we use it (a CVE in a library we never call), and how bad is it. A scanner flags presence, not exploitability. VEX statements can record "not affected" (concept).
  - **Rebuild on a schedule.** A CVE can appear next week against an image you built last month. A weekly rebuild and rescan picks up patched bases.
  - **Signing.** `cosign` signs an image digest, and a cluster policy can refuse unsigned images. Concept level here. Sign the digest, not the tag, since a tag can move (Q22).
- **CI gate.** Agree a policy, for example: fail on CRITICAL, fail on HIGH when a fix exists, allow with an owner, a reason and an expiry date. Expiry matters, otherwise waivers live forever.
  - **Limits.** A clean scan is not a secure model server. Scanners miss unknown flaws, secrets in layers (needs a secrets scan), and misconfig like running as root.

**Example:** in the sample report two CRITICALs and one fixable HIGH block the build. A HIGH with no fix is allowed. One HIGH is waived until 2026-12-31 with a reason. A second waiver expired in September, so that finding blocks again.

**Code:**
{{CODE:python:q32/policy_check.py}}
{{CODE:bash:q32/commands.sh,q32/run_all.sh}}

**Output (my run):** Python 3.13.17. Trivy, Grype, Syft, Cosign are not installed here and `docker scout` is not a command in this CLI, so no scanner was run and nothing was signed. The scan report is a hand-written sample shaped like Trivy's JSON, with invented CVE IDs and package names (`CVE-0000-...`), so its findings are not real. The policy script is mine. The date is passed in so the run repeats.
{{OUT:q32}}

**Follow-ups:**
- *Why not fail on every HIGH?* If nothing can fix it, the team learns to bypass the gate. Fail on what is actionable.
- *Scan at build time only?* No: also on a schedule, since new CVEs appear after the build.
- *Does signing stop vulnerabilities?* No. It proves who built the image and that it was not changed.

**Common mistakes:**
- Scanning the builder stage or an old tag instead of the image that ships.
- Waivers with no owner or expiry.
- Treating a scanner result as a risk rating without checking reachability.
- Never rebuilding, so the base stays as old as the last release.

=====Q33
**Say this first (1 line):** CI runners are fresh each run, so BuildKit has no cache. I export the cache at the end of a build with `--cache-to` and import it at the start with `--cache-from`, using the registry or the GitHub Actions cache, and order layers so the slow ones rarely change.

**Then explain:**
- **cache-from and cache-to.** `--cache-from` tells BuildKit where to look for layer results. `--cache-to` says where to save them after the build.
  - `type=registry,ref=...:buildcache` stores cache in a registry tag. Works across CI systems and machines. `mode=max` also stores intermediate layers (for example a builder stage), `mode=min` only the final image's layers.
  - `type=inline` puts cache metadata inside the pushed image. Simple, but only covers the final image's layers.
  - `type=gha` uses the GitHub Actions cache service. Needs the buildx setup step. Size limits and eviction apply (check current docs).
  - `type=local` writes a directory, which you can save with your CI's own cache.
- **Cache mounts are separate.** `RUN --mount=type=cache` content is not part of the exported layer cache. On an ephemeral runner it starts empty, unless you save and restore that directory yourself with an extra step (check current docs and community actions).
  - **Pulling the old image is not a cache.** `docker pull` gives you layers, but BuildKit decides reuse from cache keys. Without `--cache-from` pointing at cache data that holds those keys, it will rebuild. Whether a local image is seen at all depends on the builder driver, so do not rely on it.
- **Layer order for hit rate.** Base, system packages, `COPY requirements.txt`, `pip install`, then `COPY src`. Anything that changes every commit (git SHA `ARG`, `COPY . .`) goes last (Q2).
  - **Failure modes.** Pull-request builds from forks often cannot write cache. A cache that is saved only on `main` helps PRs read it. A changed base tag or lockfile busts everything after it, as it should.
  - **Cost.** The big win is skipping the dependency layer. The model download layer is the next one: do not bake it into a layer that changes with code (Q16).

**Example:** same `requirements.txt`, one-line code change. Empty cache rebuilds three layers. With the saved cache only `COPY src/` rebuilds (the toy model below). The actual minutes depend on your project, so I give no numbers.

**Code:**
{{CODE:yaml:q33/build.yml}}
{{CODE:bash:q33/commands.sh,q33/run_all.sh}}
{{CODE:python:q33/check_workflow.py,q33/cache_sim.py}}

**Output (my run):** buildx v0.38.1, Python 3.13.17, PyYAML 6.0.3. No build ran (no daemon or registry). What ran: `--help` for the cache flags, a PyYAML check of the workflow file, and my toy cache-key simulation. Action versions in the YAML (`@v3`, `@v4`, `@v6`) are what I remember, so check current docs. Pyyaml reads the key `on` as boolean `True`, which the first line of output shows. Use `wf[True]` or quote `"on"` when scripting against workflows.
{{OUT:q33}}

**Follow-ups:**
- *Registry or GHA cache?* GHA is easiest inside GitHub. Registry cache works anywhere and can be shared with laptops.
- *Why `mode=max`?* Multi-stage builds: the builder stage is not in the final image, so `min` would lose its layers.
- *Does a smaller image fix slow CI?* It helps pulls, but the cache is what saves build time.

**Common mistakes:**
- Setting `cache-to` and forgetting `cache-from`.
- Expecting `--mount=type=cache` to survive between runs.
- `COPY . .` before the install step.
- Pushing from pull requests by accident.

=====Q34
**Say this first (1 line):** Kubernetes removed the dockershim adapter (in 1.24), not Docker images. The kubelet now talks to containerd or CRI-O through the CRI, and those run any OCI image, including ones built with `docker build`. So ML teams keep building the same way.

**Then explain:**
- **What dockershim was.** A bridge inside the kubelet so it could drive Docker Engine, which did not speak the CRI. Docker itself already ran containerd underneath. Kubernetes dropped the bridge and talks to containerd directly. If you must keep Docker Engine as the runtime, an external adapter (`cri-dockerd`) exists. Check current docs for your version.
  - **Why images still run.** The image format is the OCI image spec, and Docker's older schema-2 format is also understood by CRI runtimes. A registry holds the same bytes whatever built them. My script classifies two sample manifests as an example.
- **What changes for ML teams.**
  - Build in CI with Docker, BuildKit, or Buildah, push to a registry, and deploy by digest. Nothing in the cluster needs Docker.
  - Debug on a node with `crictl` (and `ctr` for containerd), not `docker ps`. Some node-level scripts that call `docker` break.
  - GPU access in a cluster comes from the NVIDIA device plugin plus the toolkit configured for containerd. There is no `--gpus` flag in a pod spec. You request `nvidia.com/gpu` in resources (details in Part 3).
- **What does not exist in a cluster.** `docker.sock` in pods: nodes may have no Docker at all, and the socket is root-equivalent on the node (Q36). `docker compose`: it is a one-host tool. Docker-in-Docker needs privileged containers and is a security risk.
- **How to build images inside a cluster.** Daemonless or rootless builders: BuildKit (rootless mode), Buildah, Kaniko. Kaniko's upstream project status changed recently (I recall it being archived, check current status). Or build outside the cluster in CI and only deploy there.
  - **Failure mode.** A CI job that mounts the host `docker.sock` into a build pod stops working on a containerd node. Worse, it works on some nodes and not others.

**Example:** the team's `Jenkinsfile` mounts `/var/run/docker.sock` into a pod and runs `docker build`. After the cluster upgrade the nodes use containerd, the socket does not exist, and the job fails. The app images are fine. Fix: switch the build to a daemonless builder or build in CI outside the cluster.

**Code:**
{{CODE:yaml:q34/pod_bad.yaml,q34/pod_ok.yaml}}
{{CODE:python:q34/find_sock.py,q34/oci_types.py}}
{{CODE:bash:q34/commands.sh,q34/run_all.sh}}

**Output (my run):** Docker CLI 29.9.2 (client only, the daemon is not reachable), Python 3.13.17, PyYAML 6.0.3. No cluster, no `crictl`, no Kaniko or BuildKit pod was run. The pod files are small samples (the builder image name is a placeholder), and the scanner and classifier are my scripts. The `docker version` filter shows the client and the missing server.
{{OUT:q34}}

**Follow-ups:**
- *Do I need to rebuild my images after the change?* No.
- *Is Docker dead?* No, Docker is still the common developer tool and builds OCI images. It is just not the cluster runtime by default.
- *Where do I read the runtime a node uses?* `kubectl get nodes -o wide` (CONTAINER-RUNTIME column).

**Common mistakes:**
- Saying "Kubernetes dropped Docker support" and meaning images stopped working.
- Mounting `docker.sock` into pods for builds.
- Using `docker` commands for node debugging on containerd nodes.
- Looking for a `--gpus` flag in Kubernetes.
