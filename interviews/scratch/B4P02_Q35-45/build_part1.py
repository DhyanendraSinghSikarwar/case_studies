# answer texts for Q35-Q40 (markers @@F:lang:files@@ and @@R:dir|cmd||cmd@@ are expanded by build.py)
A = {}

A[35] = r'''**Say this first (1 line):** I add a `test` stage to the same Dockerfile, run pytest there, and build the `final` stage from the shared `base`, so tests run in the same environment that ships but pytest never reaches production.

**Then explain:**
- **Stage layout:** `base` (OS libs, pinned requirements, app code) -> `test` (base + pytest + tests) and `final` (base only). Build the test stage with `docker build --target test .`.
- **Same image, same libraries:** "passes on my laptop, fails in the image" is nearly always a missing system library (libgomp, libgl, libsndfile on a slim image) or an unpinned dependency that drifted. The test stage catches it before deploy.
- **Mount vs COPY:** mount the repo (`-v ./src:/app/src`) for fast local loops. Use COPY in CI, because a mount tests your laptop files, not what you ship.
- **Test deps stay out:** `requirements-test.txt` is installed only in the `test` stage. `final` never inherits from `test`.
- **Failure mode:** BuildKit builds only the stages the target needs. `docker build .` (final) never runs the tests. CI must build `--target test` explicitly, or the tests are silently skipped.
- **Failure mode:** `RUN pytest` fails the build but a cached layer skips a re-run. Using `CMD ["pytest"]` and `compose run` always executes.
- **Throwaway dependencies:** a compose file starts a Postgres with `tmpfs` data and a healthcheck, so every run starts clean.

**Example:** Laptop has `libgomp` from conda, the slim image does not. A test that imports a native wheel fails in the image with `libgomp.so.1: cannot open shared object file`. Fix: `apt-get install -y --no-install-recommends libgomp1` in `base`. The `final` image gets the same fix because it shares `base`. Check by hand: `final` has no `pytest` line in its lineage (the script below proves that).

**Code:** one block per language. The pytest file and the stage checker ran locally; the Docker commands did not.
@@F:dockerfile:q35/Dockerfile@@

@@F:yaml:q35/compose.test.yml@@

@@F:python:q35/src/mlsvc/__init__.py,q35/tests/test_model.py,q35/check_stages.py@@

@@F:bash:q35/commands.sh@@

**Output (my run):** Python 3.13.17, numpy 2.5.3, pytest 9.1.1 (venv), hadolint 2.15.1, docker compose v5.6.1. The image build, `compose up` and the Postgres container are **not executed** (no Docker daemon in this sandbox). What did run: pytest against the source tree, the stage checker, hadolint, and `docker compose config` (schema validation).
@@R:q35|python3 -I check_stages.py Dockerfile||PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PATH=/tmp/claude-0/v35/bin:$PATH python -m pytest -q -p no:cacheprovider||hadolint Dockerfile; echo "hadolint exit=$?"||docker compose -f compose.test.yml config --quiet; echo "compose config exit=$?"@@

**Follow-ups:**
- *Run tests at build time or run time?* Both are valid. Build time (`RUN pytest`) gives a hard gate in CI. Run time (`compose run tests`) is better when tests need a database or a GPU, since `RUN` cannot reach other containers.
- *GPU tests?* Unit tests run on CPU in this stage. GPU tests need a GPU runner with the NVIDIA runtime. Keep them in a separate marker (`-m gpu`).
- *Why not just test in CI without Docker?* Then CI tests a different OS layer from what ships.

**Common mistakes:**
- Installing pytest in the final image "just in case".
- Building only the final target in CI, so tests never run.
- Mounting the source in CI and calling it "tested in the image".
- Unpinned `requirements.txt`, so the image tests different versions each week.
- `COPY . .` before installing dependencies, which busts the cache on every code change.
'''

A[36] = r'''**Say this first (1 line):** The `docker` command is only a client; it talks over a socket to `dockerd`, which uses containerd and runc to run containers, and anyone who can use that socket is effectively root on the host.

**Then explain:**
- **The chain:** `docker` CLI -> REST API on `/var/run/docker.sock` -> `dockerd` (builds, networks, volumes) -> `containerd` (image and container lifecycle) -> `runc` (creates the Linux namespaces and cgroups and starts the process).
- **Standards:** OCI *image spec* (how an image is stored) and OCI *runtime spec* (how a container is started). That is why images built by one tool run on another.
- **Why the socket is root-equivalent:** the daemon runs as root. Whoever can talk to it can run `docker run -v /:/host --privileged ...` and edit any file. Mounting `docker.sock` into a container hands that power to the container. Being in the `docker` group counts as root.
- **Podman** has no daemon: each command is a normal process, and it supports rootless mode by default. **Rootless Docker** runs `dockerd` itself as a normal user (user namespaces), so a break-out lands as that user, with limits on ports, some storage drivers and networking.
- **HPC and shared GPU servers** often use Apptainer or Singularity: no root daemon, runs as your own user, reads a single image file, and works with schedulers like Slurm. A shared-cluster admin will not hand out docker-group membership.
- **In this sandbox:** only the client exists. The honest report is "the daemon is not running", not an invented server section.

**Example:** Interviewer: "A CI job mounts `/var/run/docker.sock` to build images. Risk?" Answer: the job (or a malicious PR running in it) can start a privileged container on the host and read secrets from other jobs. Alternatives: rootless BuildKit, Kaniko or Buildah (hedge: check current project status), or a dedicated disposable build VM.

**Code:** a small check of the socket and who could use it (Python). The two Docker commands are in the output section.
@@F:python:q36/sock_check.py@@

**Output (my run):** docker CLI 29.9.2. `docker version` and `docker info` printed the Client sections and then a connection error for the Server section, so there is **no daemon, no containerd and no runc information** to read here. Nothing about the server side was executed.
@@R:q36|docker version||docker info||python3 -I sock_check.py@@
Reading it: the `Plugins` list (buildx, compose) is client-side. `Server:` is empty because the dial to `/var/run/docker.sock` failed. On a working host, `docker info` would add storage driver, cgroup driver, runtimes and root dir (check on your machine; not shown here).

**Follow-ups:**
- *Is `docker` group membership safe?* No, treat it as root. Prefer rootless Docker or Podman where users are untrusted.
- *Where does containerd fit in Kubernetes?* The kubelet talks to containerd or CRI-O directly through CRI, without dockerd (Q34).
- *Why not Docker on an HPC login node?* Needs a root daemon, and the scheduler wants to control CPU, GPU and user identity. Apptainer images run as the calling user.

**Common mistakes:**
- Saying "Docker is a VM". A container is a process with namespaces and cgroups, sharing the host kernel.
- Mounting `docker.sock` into containers "for convenience".
- Thinking `docker run --user 1000` protects against a socket mounted inside the container.
- Assuming rootless means "no limits": rootless has real differences (ports below 1024, some networking and storage options; check current docs).
'''

A[37] = r'''**Say this first (1 line):** An image is just files addressed by their sha256 hash: layer tars, one config JSON and one manifest that lists them by digest, so change one byte and the digest changes.

**Then explain:**
- **Content-addressable storage:** the name of a blob is the hash of its bytes. Same bytes = same name = stored once. That is why two images with the same base share it, and why a registry can skip uploading a layer it already has.
- **Layer:** a tar of filesystem changes. Two hashes exist: the **blob digest** (of the compressed tar, what the registry stores) and the **diff_id** (of the uncompressed tar, listed in the config).
- **Config JSON:** env, cmd, entrypoint, architecture, `rootfs.diff_ids` and `history`. The image ID is the hash of this config.
- **Manifest:** points to the config digest and the ordered layer digests. The digest you pin (`image@sha256:...`) is the manifest's hash. A multi-arch tag points to an index of manifests.
- **Build history** (`docker history`) comes from the config `history` array: one entry per instruction with `created_by`; `ENV` and `CMD` entries are marked as empty layers (no tar).
- **`docker save`** writes a tarball with these blobs plus a `manifest.json` (newer versions may write an OCI layout; check your version).
- **Failure mode:** tar and gzip embed timestamps and owners, so "the same files" give different hashes unless you fix them. That is why reproducible builds normalise time. The script fixes mtime and gzip time.
- **Caveat:** this is a **teaching model**, not a real docker image. It has no real rootfs and no platform data; do not `docker load` it.

**Example:** Two images share the first two layers (OS, numpy) and differ only in `main.py`. In the run below, layers 1 and 2 have identical digests; layer 3 differs, so the manifest digest differs too. Flipping one byte in a blob makes verification fail.

**Code:** `python3 -I`; only stdlib.
@@F:python:q37/oci_toy.py@@

**Output (my run):** Python 3.13.17. Real run of the script above.
@@R:q37|python3 -I oci_toy.py@@

**Follow-ups:**
- *Tag vs digest?* A tag is a movable label; a digest is immutable content. Pin by digest in production, keep a human tag for reading.
- *Why does adding a layer at the end not re-upload earlier ones?* Their digests are unchanged and the registry already has them.
- *Does deleting a file in a later layer shrink the image?* No. The earlier layer still holds the bytes; the later one adds a "whiteout" marker.

**Common mistakes:**
- Mixing up diff_id (uncompressed) with the layer blob digest (compressed).
- Believing a tag name identifies content.
- Putting a secret in an early layer and deleting it later; it stays in that layer.
- Expecting identical hashes from rebuilds without fixing timestamps and file order.
'''

A[38] = r'''**Say this first (1 line):** The entrypoint script does the setup (defaults, wait, one-time download) and finishes with `exec "$@"`, so the real server replaces the shell, becomes PID 1 and receives SIGTERM from `docker stop`.

**Then explain:**
- **Defaults from env:** `: "${VAR:=default}"` sets a default only when the variable is unset or empty. Lets the same image run in dev and prod.
- **`set -euo pipefail`:** `-e` stop on error, `-u` unset variable is an error (catches typos), `-o pipefail` a failure in the middle of a pipe is not hidden. Without it, a failed model download is ignored and the server starts without weights.
- **Wait with a timeout:** loop until the port opens, then give up with a non-zero exit so the orchestrator can restart. Never wait forever. (In Compose, `depends_on: condition: service_healthy` is often cleaner.)
- **Why `exec` matters:** without it the shell stays as PID 1 and the server is a child. `docker stop` sends SIGTERM to PID 1 only. The shell dies (or ignores it), the server never gets a clean-shutdown signal, and after the grace period Docker sends SIGKILL, dropping in-flight requests.
- **Pitfalls:** CRLF line endings (a Windows checkout) break the shebang with `bash\r: No such file`; a missing executable bit gives `Permission denied` (`COPY --chmod=755` or `chmod +x`). Add `*.sh text eol=lf` in `.gitattributes`.
- **Exec form:** use `ENTRYPOINT ["/entrypoint.sh"]` and `CMD ["server..."]` as JSON arrays. Shell form wraps it in `sh -c` and hides signals again.
- **When Python is better:** when setup has real logic (retries with backoff, checksums of weights, parsing JSON config). Then write `entrypoint.py` and finish with `os.execvp(...)`. Keep bash for glue.
- **Edge case:** if `exec` is missing, a PID 1 process with no signal handler also ignores SIGTERM by default in a container. Hand it to an `init` (`--init`, tini) if you cannot control the server.

**Example:** Run order in the script: wait for DB at port 5999 (up after 1.5 s) -> model file missing, "download" -> `exec python server.py`. Hand check: the entrypoint pid in the log equals the server pid. In the no-exec variant the server pid differs and the server never prints the SIGTERM line.

**Code:** bash and Python; both ran locally with a fake dependency (a Python process that opens a TCP port after a delay).
@@F:bash:q38/entrypoint.sh,q38/crlf_demo.sh@@

@@F:python:q38/server.py,q38/fake_dep.py,q38/drive.py@@

**Output (my run):** bash and Python 3.13.17. The driver starts the fake dependency, runs the script, then sends SIGTERM to the process it started. Not a container: signals are real, PID 1 is not. In a real container the script runs as PID 1, which is **not executed** here.
@@R:q38|python3 -I drive.py||bash crlf_demo.sh@@
Reading it: with `exec`, `[entrypoint] pid=` and `[server] pid=` are the same number, and the server prints its SIGTERM line. Without `exec` the server is a child (`ppid` is the shell), gets no signal and has to be killed by hand. (Output order may interleave since the driver prints while the child runs; `q38_server_marker` is just an extra argument so the driver can find and clean up stray servers.)

**Follow-ups:**
- *`CMD` vs `ENTRYPOINT`?* ENTRYPOINT is the fixed program; CMD is the default arguments that `docker run image args` can replace. The script gets CMD as `"$@"`.
- *Why not `sleep 10` instead of waiting?* Too short breaks, too long wastes time. Poll with a deadline.
- *Model download on every start?* Put weights on a volume, check before download (the script is idempotent), or bake them in (Q43).

**Common mistakes:**
- Forgetting `exec`, then wondering why stop takes 10 seconds.
- Shell-form `CMD python server.py`, which runs under `sh -c`.
- Waiting for a dependency forever.
- Windows CRLF in the script, or no `chmod +x`.
- Using `"$*"` instead of `"$@"`, which merges arguments into one string.
'''

A[39] = r'''**Say this first (1 line):** I do not reach for Docker by default; a venv with a lockfile is enough to reproduce Python packages, and Docker earns its place when OS libraries, one artifact from dev to prod, or isolation matter.

**Then explain:**
| Tool | Pins | Weak at |
|---|---|---|
| venv + lockfile (uv, pip-tools) | Python packages and versions, with hashes | OS libs, CUDA, Python itself on other OSes |
| conda | Python, compiled libs, some CUDA runtime packages | Slow solves, large envs, still host driver and kernel |
| Nix / devbox (hedge: steep learning curve; check current docs) | Nearly everything, down to OS-level libs, reproducibly | Team adoption and GPU driver on non-NixOS hosts |
| Docker | Userland: OS libs, Python, packages, the app | Host kernel, GPU driver, data, randomness |

- **What Docker adds:** same OS libraries, same artifact in dev, CI and prod, process isolation, and a deployable unit every orchestrator understands.
- **What it does not fix:** the **GPU driver** lives on the host (the container brings CUDA userland only); **data versions** (need DVC, lakeFS or similar); **non-determinism** (seeds, GPU kernels, thread counts); the **kernel** is shared with the host (a container is not a VM).
- **Cost:** image size, build time, GPU setup (NVIDIA container toolkit), debugging friction on laptops.
- **Decision rule, 3-person team:** venv + lockfile (or conda if you need compiled CUDA libs) for dev. Add **one** Dockerfile the day you deploy to a server or a cluster, or when "works on my machine" costs a day more than once.
- **Decision rule, 30-person platform team:** Docker images are the contract: a shared base, per-project images built in CI, pinned by digest. Devs may still use venvs locally. Add dev containers if laptops differ a lot.
- **Failure mode:** an image full of `pip install` with no lockfile is not reproducible; Docker without pinning only freezes the date you built it.

**Example:** 3 people, one scikit-learn model, run on a laptop and one VM: lockfile + `python -m venv`, cron job. Team of 30, GPU models on a cluster, several services: images in CI, matrix of CUDA versions, registry. Hand check with the script: it prints what the lockfile pins and what the machine decides.

**Code:** run locally (Python). The decision function is a toy that encodes the rule above, not a product.
@@F:python:q39/env_report.py@@

**Output (my run):** Python 3.13.17. No GPU, no nvidia-smi here.
@@R:q39|python3 -I env_report.py@@

**Follow-ups:**
- *Is a conda env a good Docker replacement?* For Python and compiled libs yes; for OS packages, services and deployment no.
- *Dev containers?* Good for onboarding when laptops differ. A cost: slower file mounts on some OSes.
- *Does Docker give reproducible training?* Not alone. You still need data version, seeds and the same hardware.

**Common mistakes:**
- "We use Docker, so it is reproducible" with unpinned installs and `:latest` bases.
- Thinking the container includes the GPU driver.
- Not pinning Python itself.
- Dockerising everything for a solo notebook project.
'''

A[40] = r'''**Say this first (1 line):** One container should run one main process; gunicorn with a few workers is fine, but cron and nginx belong in their own containers, and scaling is usually more replicas, not more workers.

**Then explain:**
- **Why one main process:** the container lives and dies with PID 1. If nginx crashes inside a container where gunicorn is PID 1, nothing restarts it and the health check may still pass. Logs, restarts, resource limits and updates are all per container.
- **If you must run several processes:** use a small init or supervisor (tini, s6-overlay, supervisord), make sure signals are forwarded and that one crash kills the container so the orchestrator restarts it. Treat it as a last resort.
- **Workers vs replicas:** workers (processes) inside a container share its CPU and memory limit and its restart. Replicas are separate containers: they spread across machines, scale and roll independently. For ML, start with 1-2 workers and scale replicas.
- **Memory duplication:** each worker that loads its own model holds a full copy. 8 workers x a big model = 8x RAM or VRAM (often fatal on a GPU). Loading before the fork (`--preload` in gunicorn) lets workers share pages **copy-on-write**.
- **COW caveat:** Python touches refcounts on every object, so reading a big list of Python objects still copies pages. A big numpy buffer or memory-mapped file stays shared. GPU memory is not shared across processes the same way (CUDA contexts and fork do not mix; check your framework docs).
- **CPU limits vs worker counts:** the host has 64 cores but the container limit is 2. Using `cpu_count()` on the host gives too many workers that fight over the quota (throttling, latency spikes). Size workers from the cgroup limit.
- **Sidecar vs inside:** log shipper, proxy, metrics agent as separate containers in the same Pod or Compose project, sharing a network or volume. Cleaner updates and separate resource limits.
- **Edge case:** a cron job in the web container runs once per replica, so with 3 replicas it runs 3 times. Run it as one scheduled job.

**Example:** Host has 8 cores, container limit 2 CPUs, model 800 MB, memory limit 4 GB. Workers by CPU = 2. By memory with no sharing: (4096-800)/800+1 = 5. Take the smaller: **2**. If 90% of the model is shared, memory allows 42, so CPU is the limit; use more replicas for more throughput.

**Code:** Python for the measurement and sizing, YAML for the split layout. All of it ran locally.
@@F:python:q40/fork_memory.py,q40/workers.py@@

@@F:yaml:q40/compose.yml@@

**Output (my run):** Python 3.13.17, numpy 2.5.3, Linux, 4 workers. PSS (proportional set size) splits each shared page between the processes that share it, so the total is the real memory cost. The sizes are from this sandbox and only show the pattern. Starting the services is **not executed** (no daemon); `docker compose config` validates the YAML.
@@R:q40|python3 -I fork_memory.py||python3 -I workers.py||docker compose -f compose.yml config --services@@
Reading it: the array model with fork-after-load costs about one copy (total close to the parent's 215 MB). The same fork with a pass over millions of Python objects costs about 3.7x the parent (509 vs 139 MB) because refcount writes break copy-on-write. The "4 separate loads" line is the cost without preload. Detected limit 4.0 is the host CPU count here because this sandbox has no cgroup `cpu.max` file; inside a limited container the script would read the quota.

**Follow-ups:**
- *Why `--preload` can hurt?* Anything created before the fork (threads, DB connections, CUDA contexts) is shared in a broken way. Open them after fork, in each worker.
- *One worker and many replicas?* Simple and isolates a crash, but uses more total memory. Pick based on model size.
- *Sidecar for GPU model + preprocessing?* Only if they scale together and share a pod; otherwise separate services.

**Common mistakes:**
- `workers = 2 * cpu_count() + 1` using host cores in a limited container.
- Running cron inside every replica.
- Assuming fork-after-load always saves memory.
- Putting supervisord around everything instead of splitting containers.
'''
