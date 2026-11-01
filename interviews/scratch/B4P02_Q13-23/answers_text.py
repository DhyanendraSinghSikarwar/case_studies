A[13] = f"""
**Say this first (1 line):** Data goes in as a read-only bind mount, checkpoints go in a named volume, scratch goes in tmpfs, logs go to stdout, and the container runs as a fixed non-root UID that owns the volume.

**Then explain:**
- **Where each thing lives**
  - Training data: bind mount or a data volume, mounted `readonly`. The job must never change its input.
  - Checkpoints: named volume (or object storage). They must survive `docker rm`.
  - Model-registry download cache and the Hugging Face cache: named volume, so a restart does not download again.
  - Logs: stdout and stderr, not files. The Docker log driver collects them (see Q30).
  - Scratch and temp files: `--tmpfs /tmp`. Fast, memory-backed, gone on stop.
- **Three mount types**
  - Named volume: Docker manages the path, works the same on Linux and Docker Desktop, survives `docker rm`. Best for state you own.
  - Bind mount: you choose the host path. Good for input data and local development. Host UID and permission problems show up here. On Docker Desktop (Mac, Windows) it goes through a file-sharing layer and is often slow for many small files.
  - tmpfs: lives in RAM, vanishes at stop, counts against the memory limit. Never put checkpoints there.
- **What survives `docker rm`:** named volumes and bind-mounted host files survive. The container writable layer and tmpfs do not. Anonymous volumes (a `VOLUME` line with no name) survive too, but `docker rm -v` or `--rm` removes them, which surprises people.
- **`-v` versus `--mount`:** `--mount` is explicit (`type=,src=,dst=,readonly`) and errors if a bind source does not exist. `-v host:ctr` silently creates a missing host directory, owned by root. I prefer `--mount` in scripts.
- **UID problem (the usual failure):** the container user is UID 10001, but the volume or host dir is owned by root, so the first checkpoint save gives `PermissionError`. Fixes: `chown` the path in the Dockerfile (a new named volume copies that ownership from the image), or `--user $(id -u):$(id -g)` for bind mounts, or a one-off init container that runs `chown`.
- **Failure modes:** a checkpoint written to the container layer is lost on `rm`; a volume mounted over a path hides what the image had there; a disk-full volume fails the job late.

**Example:** The job runs as UID 10001. The volume `ckpts` is created empty and owned by root. Epoch 1 ends, `torch.save` fails with permission denied, and 6 hours of training is lost. With the `chown 10001 /ckpts` line in the image, the same run saves fine. The simulation below reproduces exactly these cases with real UIDs: root-owned dir fails, chowned dir works, a read-only input dir rejects writes, and a backup tarball restores byte-for-byte.

**Code:** the Dockerfile and run commands are not executed (no daemon). The Python simulation ran.
{fence("dockerfile", rd("q13_Dockerfile"))}
{fence("bash", rd("q13_run.sh"))}
{fence("python", rd("q13_volumes.py"))}

**Output (my run):** `docker run` and `docker volume` were **not executed** (no Docker daemon in this sandbox). What did run: `hadolint` on the Dockerfile (clean), `bash -n` on the commands, `docker run --help` to confirm the flags exist, and the simulation. In step 3 the process is not root, so the read-only input dir is simulated with mode 0555. A real `:ro` mount gives `Read-only file system` (EROFS), not EACCES, even for root.
{out(("hadolint q13_Dockerfile", "(no output, exit 0)"), ("bash -n q13_run.sh", "bash syntax ok"), ("docker run --help | grep -E -- '--mount|--tmpfs|--read-only'", "q13_help.out"), ("python3 -I q13_volumes.py", "q13.out"))}

**Follow-ups:**
- *Why not just bind mount the checkpoint dir too?* You can on Linux. On Docker Desktop it is slower, and host UID clashes appear. A named volume avoids both.
- *How do you back up a volume?* Run a throwaway container that mounts the volume read-only plus a host dir, and `tar` it (commands above; the tar step is simulated in the script).
- *Can two containers share a volume?* Yes, but Docker does no locking. Two writers to one checkpoint file corrupt it.

**Common mistakes:**
- Running as root "to avoid permission errors", then shipping that.
- Writing checkpoints to a path that is not a volume.
- Mounting the whole repo over `/app` in production, which hides the code baked into the image.
- Putting caches on tmpfs: the model downloads again after every restart and RAM fills.
"""

A[14] = f"""
**Say this first (1 line):** One user-defined network, services call each other by service name, state sits in named volumes, health checks gate `depends_on`, and only the API (plus loopback-only admin ports) is published to the host.

**Then explain:**
- **Name resolution:** Compose creates a network for the project and registers each service name in its DNS. The API calls `http://mlflow:5000`, MLflow calls `postgres:5432` and `http://minio:9000`. No IPs.
- **`localhost` is the container itself.** If MLflow is told `localhost:5432` it looks inside its own container and fails. `localhost` only means "the host" when you use host networking, and not on Docker Desktop in the same way (Q15).
- **Ports:** `ports:` is for the host's benefit. Service-to-service traffic needs none. Postgres is not published at all. The MLflow UI and MinIO console are bound to `127.0.0.1` so only this machine can open them. Only the API is open on all interfaces.
- **Startup order:** `depends_on` with `condition: service_healthy` waits until the dependency's healthcheck passes. A plain `depends_on` only waits for the container to start, not for the database to accept connections.
- **Config:** one `.env` via `env_file` for local use. Caveat: `env_file` hands every variable to that service, so a real project splits files per service. Never commit real secrets.
- **Failure modes:** `$VAR` in a list-form `command` is not expanded (no shell), so I pass the Postgres URL through `environment:` where Compose interpolates it; healthcheck tools missing in an image (check `curl` or `mc` exists, else use Python); MinIO bucket must exist before MLflow logs artifacts (a one-shot init service or `mc mb`); `latest` tags in the file are for the demo only.

**Example:** `docker compose up` starts Postgres and MinIO first. When both are healthy MLflow starts. When MLflow's `/health` answers, the API starts. A bad `depends_on` typo (`mlfow`) is caught by the pyyaml check below, as the second output shows.

**Code:** `docker-compose.yml`, `.env`, and the pyyaml check. `docker compose up` is not executed.
{fence("yaml", rd("q14/docker-compose.yml"))}
{fence("dotenv", rd("q14/.env"))}
{fence("python", rd("q14_check.py"))}

**Output (my run):** `docker compose config` ran for real (it needs no daemon). Starting the stack was **not executed** (no daemon, and images such as `postgres`, `minio` and MLflow were not pulled). The two Dockerfiles in `build:` are one-line stubs only so that `config` can resolve them.
{out(("docker compose -f q14/docker-compose.yml config > q14_config.out", "(exit 0; normalised file, 4 services, 2 volumes, 1 network; env_file values expanded into each service)"), ("python3 -I q14_check.py q14/docker-compose.yml", "q14_check.out"), ("python3 -I q14_check.py q14/bad.yml   # depends_on typo", "q14_bad.out"))}

**Follow-ups:**
- *Why not `sleep 10` before MLflow?* It is a guess. A healthcheck is a fact.
- *Does `depends_on` keep working after startup?* No. If Postgres dies later, MLflow is not restarted. Use restart policies and retries in the app.
- *How would the API reach MLflow running on the host instead?* `host.docker.internal` (Docker Desktop) or `host-gateway` via `extra_hosts` on Linux (Q15).

**Common mistakes:**
- `localhost` for another service.
- Publishing Postgres to the world "for debugging".
- Using `latest` and getting a different MinIO next week.
- Putting credentials in the compose file itself.
- Forgetting named volumes, then losing the DB on `docker compose down -v`.
"""

A[15] = f"""
**Say this first (1 line):** Inside the container the server must listen on `0.0.0.0`; if it listens on `127.0.0.1`, the published port reaches the container's network interface and nothing is listening there, so `curl` hangs or resets.

**Then explain:**
- **Network modes**
  - `bridge` (default): the container gets a private IP behind NAT; you reach it with `-p`.
  - `host`: shares the host network stack. No `-p` needed (and ignored). Port clashes are possible. Behaves differently on Docker Desktop (check current docs).
  - `none`: only loopback. Good for offline batch jobs that must not call out.
- **`-p host:container`** maps a host port to a container port. `-p 127.0.0.1:8000:8000` keeps it local. `-p 8000:8000` opens all host interfaces. `EXPOSE` only documents the port and publishes nothing. `-P` publishes every `EXPOSE`d port to random host ports.
- **The classic bug:** `uvicorn app:app` defaults to `127.0.0.1`. On the laptop that is fine. In the container, traffic arrives on `eth0`, not loopback. Fix: `--host 0.0.0.0`. The socket demo below shows the same effect on one machine.
- **DNS:** on a user-defined bridge (and Compose networks) containers resolve each other by name. On the default `bridge` network they do not, only by IP (or legacy `--link`). So create a network: `docker network create ml`.
- **Reaching a service on the host:** Docker Desktop provides `host.docker.internal`. On Linux add `--add-host=host.docker.internal:host-gateway` (or use the host's bridge IP). The host service must listen on an address the container can reach, not only `127.0.0.1`.
- **Failure modes:** a port already used on the host; a firewall in front; a mismatch between `-p` container port and the app port; the app crashed (check `docker logs`).

**Example:** The app listens on `127.0.0.1:8001` inside, the Dockerfile says `EXPOSE 8000`, and the run uses `-p 8000:8000`. Two bugs (wrong bind address, wrong port), one symptom: hang. The checker below finds both in the Dockerfile, and also three compose problems.

**Code:** the checker and the bind demo ran. The docker commands are not executed.
{fence("bash", "# NOT EXECUTED (no daemon)\ndocker network create ml\ndocker run -d --name api --network ml -p 127.0.0.1:8000:8000 myorg/api:1.0   # app must bind 0.0.0.0\ndocker run --rm --network ml curlimages/curl http://api:8000/health      # DNS by name works on a user-defined network\ndocker run --rm --add-host=host.docker.internal:host-gateway myorg/api:1.0   # reach a host service on Linux")}
{fence("python", rd("q15_netcheck.py") + "\n\n# ---- second script: q15_bind_demo.py ----\n" + rd("q15_bind_demo.py"))}

**Output (my run):** Both scripts ran with `python3 -I`. The sample files `q15/Dockerfile.bad` and `q15/compose.bad.yml` are deliberately wrong. No container was started (**not executed**).
{out(("python3 -I q15_netcheck.py q15/Dockerfile.bad q15/compose.bad.yml", "q15_bad.out"), ("python3 -I q15_bind_demo.py", "q15_demo.out"), ("docker run --help | grep -E -- '-p, --publish|--add-host|--network '", "q15_help.out"))}
The checker prints 5 findings: two from the Dockerfile, and the localhost URL, the host-networking-plus-ports pair and the public Postgres port from the compose file. It is regex and pyyaml based: it does not follow `ARG` substitution, multi-stage `CMD`, or compose `extends`.

**Follow-ups:**
- *Why does `host` networking "fix" it?* The app's loopback is then the host's loopback. It works but gives up isolation.
- *Why can containers on the default bridge not use names?* Automatic DNS is only provided on user-defined networks.
- *Does `EXPOSE` matter?* Only as documentation and for `-P` and some tools.

**Common mistakes:**
- `localhost` in a database URL inside a container.
- Binding `127.0.0.1` in the app.
- Publishing every port instead of the one that users need.
- Expecting `-p` to work with `--network host`.
"""

A[16] = f"""
**Say this first (1 line):** Small model: bake it in. Medium: bake it if releases are rare, otherwise download into a cache volume with a pinned checksum. Big LLM: keep it out of the image and put it on a volume or a pre-warmed node cache, behind a readiness gate.

**Then explain:**
| | Baked in image | Mounted volume | Downloaded at start |
|---|---|---|---|
| Image size and pull time | Grows with the model, every node pulls it | Small image; weights arrive separately | Small image |
| Cold start | Pull time, then fast load | Fast if the volume is warm | Download time on every fresh node (until cached) |
| Rollback | Retag the old image, done | Need versioned dirs and a pointer | Config change to the old version; needs old file kept |
| Reproducibility | Best: the image digest pins code and model | Depends on how the volume is filled | Only if you pin a version id and checksum |
| Registry cost | Every model version stores a new big layer (sharing helps only if the model layer is unchanged) | None | None |
| Air-gapped | Works, one artifact | Works with a prefilled volume | Needs an internal mirror |
| Secrets | None at runtime; registry pull credentials only | Storage access to fill it | Needs a token at runtime for the model store |
- **Small sklearn model (MBs):** bake it. One digest equals one tested thing.
- **Medium transformer (about 2 GB):** bake if the registry is close and you ship rarely. If code ships weekly and the model monthly, put the model in its own layer (copied before the code, so the weekly rebuild reuses it) or download to a cache volume. Judgement call; say so in the interview.
- **Big LLM (about 30 GB):** do not bake. Very large layers are slow to push and pull, and some registries have size limits (check current docs). Use a shared volume, a node-local cache filled by a daemonset, or a download with caching.
- **Safe startup download:** pin an exact version and a sha256 (not `latest`), retry with backoff, write to a temp file then rename, verify the checksum before use, and only flip readiness when the model is loaded. If it fails, exit non-zero so the orchestrator restarts instead of serving garbage.
- **Failure modes:** a half-downloaded file loaded as a model; two replicas starting together and downloading the same 30 GB; the store being down during an autoscale event; a token that expired.

**Example:** The script below fakes a store with a local HTTP server. The first two requests return 503, the third works and the sha256 matches, so READY is written. The second file is corrupt, fails the checksum twice, is never renamed into place, and the process gives up with a non-zero exit.

**Code:** a Dockerfile for the download variant (linted by hadolint), the download-and-verify script, and the not-executed commands.
{fence("dockerfile", rd("q16_Dockerfile"))}
{fence("python", rd("q16_safe_download.py"))}
{fence("bash", "# NOT EXECUTED (no daemon, no registry)\n# Variant A: bake. Model copied before app code so weekly code changes reuse the big layer.\ndocker build -t myorg/api:1.14.0-m23 -f Dockerfile.baked .\n# Variant B: download at start into a cache volume\ndocker run -v models:/models -e MODEL_URL=https://store.example.com/churn/23/model.bin -e MODEL_SHA256=<sha256> myorg/api:1.14.0")}

**Output (my run):** the script ran with `python3 -I` (real local HTTP server, random weights, so the hash changes each run). `hadolint` ran on the Dockerfile. No image was built (**not executed**).
{out(("hadolint --no-color q16_Dockerfile", "(no findings, exit 0)"), ("python3 -I q16_safe_download.py", "q16.out"))}

**Follow-ups:**
- *Why checksum if the URL is HTTPS?* TLS protects transit, not a truncated file, a wrong version, or a changed object.
- *How do you pin a model with download?* Version id in config, sha256 in config, and log both at startup.
- *Why a readiness gate?* So the load balancer sends traffic only after the model is loaded (Q12).

**Common mistakes:**
- `MODEL_URL=.../latest/model.bin`.
- Loading the file while it is still being written.
- Baking a 30 GB model and then wondering why scale-out takes 20 minutes.
- Putting the model-store token in the image.
"""

A[17] = f"""
**Say this first (1 line):** `docker build .` tars the whole context directory and sends it to the builder; `.dockerignore` removes files from that tarball, so builds are faster, caches stay valid and secrets like `.env` cannot be copied in.

**Then explain:**
- **Context:** the directory you pass (the `.`). Everything in it is a candidate for `COPY`. A 20 GB `data/` makes every build start by shipping 20 GB (with BuildKit only the needed files are transferred, but you cannot rely on that; check current docs).
- **Cache:** `COPY . /app` hashes the files it copies. A changed notebook, log or `.git` file changes that hash and busts the layer (Q2). Ignoring them keeps the hash stable.
- **Security:** `.env`, keys and `.git` history do not get into the image if they never reach the context.
- **Pattern rules (Docker's, simplified):** one pattern per line; `#` comments; paths are relative to the context root; `*` matches within one directory level, so `*.ipynb` only matches in the root; `**/*.ipynb` matches at any depth; a trailing `/` is optional; the **last matching line wins**; `!pattern` re-includes something an earlier line excluded, so put exceptions after the rule they undo.
- **Without a daemon:** list the files yourself with a matcher (below). `docker build` has no real dry-run that needs no daemon here.
- **What my matcher does not cover:** exact Go `filepath.Match` rules (`[a-z]` classes, escapes), `**` in the middle in every position, `!` interaction with parent-directory pruning (Docker may skip a whole excluded directory for speed, but still honours `!` exceptions for files below it; check current docs), symlinks, and case sensitivity on Windows. The Dockerfile and `.dockerignore` are always sent to the builder; ignoring them only hides them from `COPY`.
- **Failure mode:** you ignore `models/` but the Dockerfile has `COPY models/prod.pt`. The build fails with "not found". Add an exception, or do not ignore it.

**Example:** My sample tree has `.env`, `.env.example`, `.git/HEAD`, `data/raw/big.csv`, `models/big.pt`, `models/tiny_test.pt`, a notebook, a `.pem` file, a `.pyc` file, `requirements.txt` and `src/app.py`. After the rules, four files are sent: `.env.example`, `models/tiny_test.pt` (the `!` exception), `requirements.txt`, `src/app.py`.

**Code:** the `.dockerignore` and the simplified matcher. Both ran.
{fence("gitignore", rd("q17.dockerignore"))}
{fence("python", rd("q17_ignore.py"))}

**Output (my run):** the script ran with `python3 -I` on a temporary tree of 100-byte files. The second run shows the gotcha: a bare `*.ipynb` does not match `nb/eda.ipynb`. No `docker build` was run (**not executed**, no daemon).
{out(("python3 -I q17_ignore.py <tmp-tree> q17.dockerignore", "q17.out"), ("python3 -I q17_ignore.py <tmp-tree> <file containing only '*.ipynb'>  # filtered to ipynb lines", "q17_gotcha.out"))}

**Follow-ups:**
- *Is `.gitignore` enough?* No. Docker does not read it. Keep both, and keep them similar.
- *Does `.dockerignore` shrink the image?* Only what `COPY` would have copied. Layers from `RUN` are unaffected.
- *Where do data and weights go instead?* Mounted at run time or fetched at start (Q13, Q16).

**Common mistakes:**
- `*.ipynb` instead of `**/*.ipynb`.
- An exception placed before the rule it should undo.
- Ignoring `requirements.txt` by accident with a broad pattern.
- Believing `.dockerignore` protects secrets that are passed as `ARG`.
"""

A[18] = f"""
**Say this first (1 line):** A container is an ordinary process on the host kernel, isolated by namespaces and limited by cgroups; a VM boots its own kernel on virtual hardware, so it is heavier but a stronger boundary.

**Then explain:**
- **Namespaces** give each container its own view: `pid` (process IDs, the first process is PID 1), `net` (interfaces, ports, routing), `mnt` (filesystem tree), plus `uts` (hostname), `ipc` and `user`.
- **cgroups** limit and account for resources: CPU shares or quota, memory limit, process count. `docker run --memory` and `--cpus` set them.
- **Shared kernel:** every container on a host runs on the same kernel. A kernel bug or a misconfigured privileged container affects the host. A container cannot ship its own kernel.
- **Speed and size:** a container starts in about the time it takes to start a process (no boot, no OS). A VM boots an OS. Containers are smaller because they hold only userland files.
- **GPU consequence:** the GPU driver is a kernel module on the host, so the image cannot contain it. The image carries the CUDA runtime and libraries; the host supplies the driver, and the container toolkit exposes the device files. A model needing a newer CUDA than the host driver supports fails no matter how the image is built (Q6).
- **When to use a VM or micro-VM:** running untrusted code (user-submitted notebooks, other tenants' models), hard multi-tenant isolation, different kernel requirements, or compliance rules. Sandboxed runtimes (gVisor, Kata, Firecracker-style micro-VMs; check current docs for each) sit between the two.
- **Failure modes:** `--privileged`, mounting `docker.sock`, or host PID/network namespaces remove the isolation you thought you had. Limits are not automatic: without `--memory`, one container can use the whole host RAM.

**Example:** The script below shows this process's namespace IDs, its cgroup paths and the kernel release (the same kernel a container here would use), then starts a command in a **new PID namespace** using `unshare`, where it sees itself as PID 1 while the host sees a normal PID. That is the container trick without Docker.

**Code:** run with `python3 -I`. Needs Linux; the `unshare` step needs root or user namespaces.
{fence("python", rd("q18_isolation.py"))}

**Output (my run):** real output of this sandbox. It shows cgroup v1 style paths and no `memory.max` file at the v2 location, so the limit lines say "not present here". On a cgroup v2 host those files exist (see Q19). No container ran (**not executed**, no daemon).
{out(("python3 -I q18_isolation.py", "q18.out"))}

**Follow-ups:**
- *Is a container secure by default?* Reasonably isolated for trusted code, not a security boundary for hostile code.
- *Can I run a Linux image on a Mac?* Docker Desktop runs a small Linux VM and the containers live inside it.
- *Why is a micro-VM useful?* Near-container start with a separate kernel per workload.

**Common mistakes:**
- "A container is a lightweight VM."
- Saying the image contains the NVIDIA driver.
- Forgetting resource limits.
- Running untrusted notebooks in a shared-kernel container with the Docker socket mounted.
"""

A[19] = f"""
**Say this first (1 line):** Exit 137 is 128 plus signal 9, SIGKILL, most often the kernel OOM killer after the container hit its memory limit; the "bus error, shared memory" crash is a different cause: the 64 MB default `/dev/shm`, which DataLoader workers use to pass tensors.

**Then explain:**
- **137:** `128 + 9`. Something sent SIGKILL: the OOM killer, `docker kill`, or `docker stop` after the grace period. Confirm with `docker inspect -f '{{{{.State.OOMKilled}}}} {{{{.State.ExitCode}}}}' <c>` and `dmesg | grep -i 'killed process'` on the host. Caveat: if the kernel kills a child worker, `OOMKilled` can be false while the symptom is the same.
- **Limits:** `--memory 8g` sets the cgroup limit. Without it the container can use the host's RAM. Tools that read `/proc/meminfo` (and `os.cpu_count()` for CPUs) see the **host**, not the limit, so they plan for more than they will get. Read the cgroup files instead. Setting `--memory-swap` equal to `--memory` disables extra swap.
- **Python and PyTorch under a limit:** page cache, pinned memory, many DataLoader workers (each can hold a copy of the data), and big batches all count. Python often does not return freed memory to the OS right away, so RSS looks high.
- **Shared memory:** DataLoader workers send tensors through `/dev/shm`. Docker gives it 64 MB by default. Symptoms: `RuntimeError: DataLoader worker (pid N) is killed by signal: Bus error` and a message about shared memory. Fixes: `--shm-size=2g` (size it to batch and worker count), or `--ipc=host` (shares the host IPC namespace, so weaker isolation). Last resort: `num_workers=0`.
- **Fixes for 137:** lower batch size or workers, stream data, raise the limit, or find the leak.

**Example:** 4 workers, batch 64 images of 3x224x224 floats is about 38 MB per batch in flight per worker, so a handful of prefetched batches overruns 64 MB at once. Hand-check: 64*3*224*224*4 bytes = 38,535,168 bytes. That is why the default 64 MB breaks.

**Code:**
{fence("bash", "# NOT EXECUTED (no daemon)\ndocker run --rm --gpus all --memory 16g --memory-swap 16g --shm-size 2g myorg/trainer:1.4.0\n# or: --ipc=host (less isolation)\ndocker inspect -f '{{{{.State.OOMKilled}}}} {{{{.State.ExitCode}}}}' train\ndmesg | grep -i 'killed process'")}
{fence("python", rd("q19_cgroup_mem.py"))}

**Output (my run):** the script ran with `python3 -I`. The sandbox shows cgroup v1 with no limit, and `/dev/shm` here is not Docker's 64 MB default, so this run shows the reader working, not an OOM. The exit-code lines come from a real SIGKILL of a child. `docker run` and `docker inspect` were **not executed** (no daemon); `docker run --help` confirms `--memory` and `--shm-size` exist.
{out(("python3 -I q19_cgroup_mem.py", "q19.out"))}

**Follow-ups:**
- *Is 137 always OOM?* No. Check `OOMKilled`, `dmesg`, and whether something ran `docker kill` or a stop timed out.
- *Why not always use `--ipc=host`?* It shares IPC with the host and other containers; fine on a private box, poor in multi-tenant setups.
- *Is `--memory` the same as a Kubernetes limit?* Same cgroup idea, set through the pod spec (later part).

**Common mistakes:**
- Raising `num_workers` to speed up and then hitting 137.
- Sizing from `free -m` inside the container.
- Not setting any limit on a shared GPU box.
- Ignoring that page cache and pinned memory count.
"""

A[20] = f"""
**Say this first (1 line):** Use `COPY` not `ADD`, chain `apt-get update && install --no-install-recommends && rm -rf /var/lib/apt/lists/*` in ONE `RUN`, use `WORKDIR` not `cd`, and remember a later `RUN rm` cannot shrink an earlier layer.

**Then explain:**
- **COPY vs ADD:** `COPY` copies files. `ADD` also auto-extracts a local tar archive and can fetch a URL. That magic is surprising, so use `COPY`. For downloads, `RUN curl ... && verify checksum` (or `ADD --checksum` where your BuildKit supports it; check current docs).
- **Layers only add:** each `RUN` is a layer. Files deleted in a later layer are only hidden, the earlier layer still ships. So clean up in the same `RUN` that created the files.
- **apt:** `update` and `install` in the same `RUN` (a cached `update` layer goes stale), `--no-install-recommends` for a smaller layer, delete `/var/lib/apt/lists` in that same command. Versions pinning is possible but a trade-off (Q8).
- **WORKDIR vs cd:** `RUN cd /app` only affects that one `RUN`. `WORKDIR` persists, creates the directory and is clearer.
- **EXPOSE** is documentation, it publishes nothing (Q15). **LABEL** adds metadata (use the `org.opencontainers.image.*` keys): source, revision, version. Labels are visible in `docker inspect`, so never put secrets in them.
- **Exec form CMD** (`["python", "serve.py"]`) so signals reach the app (Q11).
- **Failure mode:** a linter cannot see that `RUN rm -rf /root/.cache` in its own layer saves nothing. Only reading the layer sizes with `docker history` shows it (not executed here).

**Example:** Before: 11 findings from 9 rule IDs. After: `slim` base, one apt `RUN`, `WORKDIR`, `COPY`, `--no-cache-dir`, JSON `CMD`. hadolint output shows the rule numbers before, and one remaining warning after, which I suppress on purpose with a comment (`DL3008`, apt version pinning) and a stated reason.

**Code:** before and after Dockerfiles, and the lint commands.
{fence("dockerfile", "# ---- Dockerfile.before ----\n" + rd("q20/Dockerfile.before") + "\n\n# ---- Dockerfile.after ----\n" + rd("q20/Dockerfile.after"))}
{fence("bash", "pip install hadolint-py     # worked here via the proxy: Haskell Dockerfile Linter 2.15.1\nhadolint --no-color Dockerfile.before\nhadolint --no-color Dockerfile.after\n# docker build / docker history on these were NOT EXECUTED (no daemon)")}

**Output (my run):** hadolint ran for real. The suppression in the "after" file is `# hadolint ignore=DL3008` with the reason in the Follow-ups below. Image building was **not executed**.
{out(("hadolint --no-color q20/Dockerfile.before", "q20_before.out"), ("", "q20_after.out"))}
Rule map: DL3020 `ADD` instead of `COPY`; DL3003 `cd` instead of `WORKDIR` (plus shellcheck SC2164); DL3009 apt lists not deleted; DL3015 missing `--no-install-recommends`; DL3008 unpinned apt packages; DL3042 pip cache not disabled; DL3025 shell-form `CMD`; DL3059 consecutive `RUN`s (info). The `RUN rm` in its own layer and the `ADD <url>` are **not** flagged.

**Follow-ups:**
- *Why suppress DL3008?* Debian security updates change versions; pinning breaks builds when old versions leave the mirror. The reason belongs in a comment next to the ignore.
- *Does `ENV` or `ARG` in the same `RUN` help size?* No; size comes from files written.
- *`ADD` of a local `.tar.gz`?* It is extracted. If you wanted the tarball itself, use `COPY`.

**Common mistakes:**
- `RUN apt-get update` on its own line.
- `rm` in a later `RUN`.
- Using `ADD` for plain files.
- Putting secrets in `LABEL`.
"""

A[21] = f"""
**Say this first (1 line):** `ARG` exists only while building and is gone at runtime (but its value can still show in `docker history`); `ENV` is baked into the image and visible to the running process; model paths and thresholds should be runtime config so one image works everywhere.

**Then explain:**
- **ARG:** set with `--build-arg NAME=value`; usable in later build instructions in its stage; not in the container's environment at run time. Never pass secrets this way, they appear in image metadata (Q9).
- **ENV:** persists into the image and the running container. A default can be overridden at run time with `docker run -e NAME=value` or `--env-file file`. `-e NAME` with no value passes the host's current value through.
- **12-factor:** config that changes between environments (model path, threshold, feature flags, URLs) belongs in environment variables at run time, not in the image. One image, many environments, no rebuild to change a threshold.
- **ARG before FROM:** allowed, but only for use in `FROM` lines (for example `FROM python:${{PY_VERSION}}-slim`). After `FROM`, that value is out of scope. To use it inside the stage, redeclare the name: `ARG PY_VERSION`. Each stage has its own scope too, so declare ARGs again in every stage that needs them.
- **Pattern for build info:** `ARG GIT_SHA` then `LABEL ...revision="${{GIT_SHA}}"` or `ENV BUILD_SHA=${{GIT_SHA}}` when the app should report its own version. Remember that this changes the layer on every commit, so place it late (Q2).
- **Failure modes:** an ARG used in a stage where it was not declared silently expands to an empty string; an `ENV` default hides a missing runtime variable; baking a threshold into `ENV` and forgetting it is overridable.

**Example:** In the sample Dockerfile below, `PY_VERSION` is declared globally and used in two `FROM` lines. Only stage 1 redeclares it, so only stage 1 can use it in `RUN`. `GIT_SHA` is build-only, but stage 1 copies its value into `ENV BUILD_SHA`, so the value does survive at runtime that way. `MODEL_PATH` and `THRESHOLD` are runtime ENV with defaults.

**Code:** the Dockerfile, the scope script, and commands that were not executed.
{fence("dockerfile", rd("q21/Dockerfile"))}
{fence("bash", "# NOT EXECUTED (no daemon)\ndocker build --build-arg GIT_SHA=$(git rev-parse --short HEAD) -t myorg/api:dev .\ndocker run --rm -e THRESHOLD=0.7 -e MODEL_PATH=/models/v2.pkl myorg/api:dev\ndocker run --rm --env-file prod.env myorg/api:dev      # file lines are KEY=VALUE, # comments allowed")}
{fence("python", rd("q21_scope.py"))}

**Output (my run):** the script and hadolint ran. Building and running the image were **not executed** (no daemon). The script is a line-based reader (handles `\\` continuations, `KEY=value` ENV only), not a full Dockerfile parser.
{out(("python3 -I q21_scope.py q21/Dockerfile", "q21.out"), ("hadolint --no-color q21/Dockerfile", "(no findings, exit 0)"))}

**Follow-ups:**
- *Why does ARG show in history?* Build args are recorded in the image's build metadata and layer commands.
- *How do I see runtime env?* `docker inspect` shows ENV and `-e` values for a container, so no secrets there either on shared hosts.
- *Where do big configs go?* A mounted file, with the path in an env var.

**Common mistakes:**
- Expecting an ARG to exist in the running container.
- Using `ARG` before `FROM` inside the stage without redeclaring.
- Baking environment-specific URLs into the image.
- Putting a changing ARG (commit hash) early in the Dockerfile and killing the cache.
"""

A[22] = f"""
**Say this first (1 line):** Tag every image with an immutable identifier (git SHA), add human tags (semantic version, model version), treat `latest` and environment names as moving pointers only, and deploy by digest so you always know what ran.

**Then explain:**
- **`latest`** is just a default tag name, not "newest". It is mutable. Rollback by "the previous latest" is impossible, because that tag now points at the new image. Two nodes can pull different images under the same tag.
- **Tags are mutable pointers; digests are immutable.** A digest (`@sha256:...`) is the hash of the manifest. Some registries can enforce tag immutability (check current docs). Deploying `repo@sha256:...` guarantees the same bytes.
- **One image, many tags:** `docker tag` adds names to the same image ID. Pushing them uploads the layers once.
- **Link to model and run:** put the model registry version and training run ID in image labels and in the tag if the model is baked in. Also record the image digest back in the model registry entry, so you can go both ways.
- **Weekly code, monthly retrain scheme (proposal):**
  - Code release tag `1.14.0` (semver, weekly).
  - `1.14.0-g9f3c2a1`, the exact commit, built once by CI. The others are retags of it.
  - `sha-<12 chars>` for any commit build.
  - `1.14.0-churn-m23` when model version 23 is baked in. If weights are mounted or downloaded (Q16), the model version goes in runtime config and the tag only tracks code.
  - `staging` and `prod` as moving pointers, set by the deploy job, never used as the only record.
- **Failure modes:** tag collisions from retagging `1.14.0` after a hotfix (cut `1.14.1` instead); invalid tag characters or over 128 chars; a retention rule that deletes the tag your rollback needs.

**Example:** Release 1.14.0 moves `latest`. The script prints the registry state: before and after, `latest` points somewhere else, while `1.13.0` still points to the previous image, so rollback by version works and by `latest` does not.

**Code:** the script ran; the `docker` commands it prints were not executed.
{fence("python", rd("q22_tags.py"))}

**Output (my run):** the script ran with `python3 -I`. `docker build`, `docker tag`, `docker push` were **not executed** (no daemon, no registry); `docker tag --help` and `docker push --help` ran and confirm `--all-tags` exists. The commit hash and registry host are made-up examples.
{out(("python3 -I q22_tags.py", "q22.out"), ("docker push --help | grep -E -- '--all-tags'", "      -a, --all-tags          Push all tags of an image to the repository"))}

**Follow-ups:**
- *How does the cluster deploy?* Reference the digest (or a tag that the deploy job records as a digest). Tools differ; check current docs.
- *Can I reuse a version tag?* Don't. If you must, you have lost auditability.
- *Date tags?* Handy for retention and humans, not for identity.

**Common mistakes:**
- Deploying `latest`.
- Not recording which model went into which image.
- Moving a release tag after a hotfix.
- Tags with `/`, spaces or a leading dash.
"""

A[23] = f"""
**Say this first (1 line):** A registry stores images by repository, tag and digest; you log in, push layers (only missing ones are uploaded), and pull from nodes. For ML teams the real concerns are rate limits, private access, cleanup and the cost of many large images.

**Then explain:**
- **Names:** `registry/repo:tag` or `@digest`. With no registry the CLI assumes Docker Hub; a single-name official image like `python` becomes `docker.io/library/python`. The script below parses these.
- **Flow:** `docker login registry` stores credentials (by default in `~/.docker/config.json`; a credential helper is safer). `docker push` uploads each layer blob that the registry does not already have, then the manifest that lists them. `docker pull` fetches the manifest, then only layers the node lacks. This is why layer order and sharing matter (Q2, Q7).
- **Auth:** prefer `--password-stdin` with a token over typing a password. In CI use short-lived tokens or workload identity where the registry supports it (check current docs; the cloud-specific IAM details come in a later part). Never bake registry credentials into images.
- **Registries (hedged):** Docker Hub; GitHub Container Registry (`ghcr.io`), tied to your GitHub org permissions; cloud registries from the big cloud providers (AWS ECR, Google Artifact Registry, Azure Container Registry), which integrate with cloud identity and live near your compute. Check current docs for features and limits.
- **Docker Hub rate limits:** anonymous and free-tier pulls are limited per time window, and the limits change (check current docs). A cluster pulling the same base image from many nodes behind one IP can hit them. Mitigations: log in with a token, mirror base images into your own registry, or run a pull-through cache (`registry-mirrors` in `daemon.json`, or a registry configured as a proxy cache).
- **Public vs private:** weights, proprietary code and data baked in images must be private. Public images leak whatever is in their layers (Q9).
- **Retention and cost:** old images pile up. Cost grows with unique layer bytes stored (shared layers are stored once) plus transfer across regions or out of the cloud. Use lifecycle or cleanup policies (the names differ by registry): keep tags in use and the last N releases, expire untagged manifests, expire PR/CI tags quickly. Do not delete the tag a rollback needs.
- **Failure modes:** rate-limited pull during an autoscale event; expired token; deleting a tag that production still references; a rebuilt base layer that makes every new image share nothing.

**Example:** With toy sizes (MB): base 2000, deps 5000, four app layers of 20, two model layers of 1500. Four images listed by tag sum to 31,080 MB if you count each separately, but the registry stores 10,080 MB because base and deps are shared. Delete the oldest tag and 20 MB comes back; change the base and 7,000 MB is added. The numbers are invented to show the effect.

**Code:** the parser and retention simulation ran. The commands are not executed.
{fence("bash", "# NOT EXECUTED (no daemon, no registry, no credentials)\necho \"$REGISTRY_TOKEN\" | docker login ghcr.io -u myuser --password-stdin\ndocker push ghcr.io/myorg/churn-api:1.14.0\ndocker pull ghcr.io/myorg/churn-api:1.14.0\n# pull-through cache / mirror: set in /etc/docker/daemon.json  {{\"registry-mirrors\": [\"https://mirror.example.com\"]}}")}
{fence("python", rd("q23_registry.py"))}

**Output (my run):** the script ran with `python3 -I`. All `docker login/push/pull` commands are **not executed** (no daemon, no registry); `docker login --help` ran to confirm `--password-stdin`. No rate-limit or cloud behaviour was tested.
{out(("python3 -I q23_registry.py", "q23.out"), ("docker login --help | grep -- '--password-stdin'", "q23_help.out"))}

**Follow-ups:**
- *Why not `docker login -p`?* The password shows in shell history and process lists.
- *Mirror or pull-through cache?* A mirror is a copy you maintain; a pull-through cache fetches on demand and keeps what it saw. Either avoids upstream limits.
- *Where do big model files go?* Often outside the registry (object storage or a volume, Q16), which also keeps image storage down.

**Common mistakes:**
- Relying on anonymous Docker Hub pulls in production.
- No cleanup policy until the bill arrives.
- Deleting by age and removing a tag in use.
- Rebuilding the base layer constantly, so nothing is shared.
"""
