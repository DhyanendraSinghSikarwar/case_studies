### Q35 ⭐⭐ 🟡 Running ML tests inside containers. Explain a test stage in a multi-stage Dockerfile (--target test), running pytest in the same image that ships, a compose file with a test service and throwaway dependencies, why 'passes on my laptop, fails in the image' usually means a missing system library or unpinned dependency, mounting the repo for fast local iteration versus COPY for CI fidelity, and keeping test dependencies out of the final image. Show the Dockerfile and a pytest file that runs locally without a daemon.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** I add a `test` stage to the same Dockerfile, run pytest there, and build the `final` stage from the shared `base`, so tests run in the same environment that ships but pytest never reaches production.

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
```dockerfile
# ===== Dockerfile =====
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/

FROM base AS test
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt
COPY tests/ ./tests/
ENV PYTHONPATH=/app/src
CMD ["pytest", "-q"]

FROM base AS final
ENV PYTHONPATH=/app/src
USER 10001
CMD ["python", "-m", "mlsvc"]
```

```yaml
# ===== compose.test.yml =====
services:
  tests:
    build:
      context: .
      target: test
    environment:
      DATABASE_URL: postgresql://app:app@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    # local iteration only: uncomment to mount the repo instead of the copied code
    # volumes:
    #   - ./src:/app/src:ro
    #   - ./tests:/app/tests:ro
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    tmpfs:
      - /var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 2s
      retries: 15
```

```python
# ===== src/mlsvc/__init__.py =====
import numpy as np

def softmax(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - x.max())          # subtract max: avoids overflow
    return e / e.sum()

def predict(features, weights):
    return int(np.argmax(softmax(np.asarray(weights) @ np.asarray(features))))

# ===== tests/test_model.py =====
import numpy as np
import pytest
from mlsvc import predict, softmax

def test_softmax_sums_to_one():
    assert softmax([1, 2, 3]).sum() == pytest.approx(1.0)

def test_softmax_no_overflow():
    assert np.isfinite(softmax([1000, 1001])).all()

def test_predict_picks_larger_logit():
    assert predict([1.0, 2.0], [[1, 0], [0, 1]]) == 1

# ===== check_stages.py =====
"""Q35: tiny Dockerfile stage parser. Fails if the final stage can see test dependencies.
Run: python3 -I check_stages.py Dockerfile"""
import re, sys

def stages(text):
    out, cur = {}, None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"FROM\s+(\S+)(?:\s+AS\s+(\S+))?$", line, re.I)
        if m:
            cur = m.group(2) or m.group(1)
            out[cur] = {"from": m.group(1), "lines": []}
        elif cur:
            out[cur]["lines"].append(line)
    return out

def lineage(st, name):
    chain = [name]
    while st[chain[-1]]["from"] in st:
        chain.append(st[chain[-1]]["from"])
    return chain

st = stages(open(sys.argv[1]).read())
print("stages:", list(st))
for name in st:
    print(f"  {name}: lineage {' -> '.join(lineage(st, name))}")
final = list(st)[-1]
chain = lineage(st, final)
bad = [l for n in chain for l in st[n]["lines"] if "requirements-test" in l or "tests/" in l or "pytest" in l]
print("final stage:", final, "| test-related lines in its lineage:", bad)
sys.exit(1 if bad else 0)
```

```bash
# ===== commands.sh =====
# NOT executed here (needs a Docker daemon)
docker build --target test -t ml-svc:test .                 # builds base + test stage
docker run --rm ml-svc:test                                 # runs pytest in the image
docker run --rm -v "$PWD/src:/app/src:ro" -v "$PWD/tests:/app/tests:ro" ml-svc:test   # fast local loop
docker compose -f compose.test.yml up --build --exit-code-from tests --abort-on-container-exit
docker build --target final -t ml-svc:1.0 .                 # no pytest in this image
```

**Output (my run):** Python 3.13.17, numpy 2.5.3, pytest 9.1.1 (venv), hadolint 2.15.1, docker compose v5.6.1. The image build, `compose up` and the Postgres container are **not executed** (no Docker daemon in this sandbox). What did run: pytest against the source tree, the stage checker, hadolint, and `docker compose config` (schema validation).
```text
$ python3 -I check_stages.py Dockerfile
stages: ['base', 'test', 'final']
  base: lineage base
  test: lineage test -> base
  final: lineage final -> base
final stage: final | test-related lines in its lineage: []

$ PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PATH=/tmp/v35/bin:$PATH python -m pytest -q -p no:cacheprovider
...                                                                      [100%]
3 passed in 0.05s

$ hadolint Dockerfile; echo "hadolint exit=$?"
hadolint exit=0

$ docker compose -f compose.test.yml config --quiet; echo "compose config exit=$?"
compose config exit=0
```


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

### Q36 ⭐ 🟢 Docker architecture in one minute: client, daemon (dockerd), containerd, runc, OCI image and runtime specs, the docker.sock socket and why access to it is root-equivalent. Run docker version and docker info here and read what they say (the daemon is unavailable in this sandbox; report that honestly). Contrast with Podman (daemonless) and rootless Docker, and why shared HPC or GPU servers often use Apptainer or Singularity.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** The `docker` command is only a client; it talks over a socket to `dockerd`, which uses containerd and runc to run containers, and anyone who can use that socket is effectively root on the host.

**Then explain:**
- **The chain:** `docker` CLI -> REST API on `/var/run/docker.sock` -> `dockerd` (builds, networks, volumes) -> `containerd` (image and container lifecycle) -> `runc` (creates the Linux namespaces and cgroups and starts the process).
- **Standards:** OCI *image spec* (how an image is stored) and OCI *runtime spec* (how a container is started). That is why images built by one tool run on another.
- **Why the socket is root-equivalent:** the daemon runs as root. Whoever can talk to it can run `docker run -v /:/host --privileged ...` and edit any file. Mounting `docker.sock` into a container hands that power to the container. Being in the `docker` group counts as root.
- **Podman** has no daemon: each command is a normal process, and it supports rootless mode by default. **Rootless Docker** runs `dockerd` itself as a normal user (user namespaces), so a break-out lands as that user, with limits on ports, some storage drivers and networking.
- **HPC and shared GPU servers** often use Apptainer or Singularity: no root daemon, runs as your own user, reads a single image file, and works with schedulers like Slurm. A shared-cluster admin will not hand out docker-group membership.
- **In this sandbox:** only the client exists. The honest report is "the daemon is not running", not an invented server section.

**Example:** Interviewer: "A CI job mounts `/var/run/docker.sock` to build images. Risk?" Answer: the job (or a malicious PR running in it) can start a privileged container on the host and read secrets from other jobs. Alternatives: rootless BuildKit, Kaniko or Buildah (hedge: check current project status), or a dedicated disposable build VM.

**Code:** a small check of the socket and who could use it (Python). The two Docker commands are in the output section.
```python
# ===== sock_check.py =====
"""Q36: is the docker socket here, who owns it, and could I use it? Run: python3 -I sock_check.py"""
import grp, os, stat

SOCK = "/var/run/docker.sock"
try:
    st = os.stat(SOCK)
except FileNotFoundError:
    print(f"{SOCK}: not found -> no local dockerd; the docker CLI has nothing to talk to")
else:
    print("is socket:", stat.S_ISSOCK(st.st_mode), "| mode:", oct(st.st_mode & 0o777),
          "| group:", grp.getgrgid(st.st_gid).gr_name)
    print("my uid:", os.getuid(), "| my groups:", [grp.getgrgid(g).gr_name for g in os.getgroups()])
print("DOCKER_HOST env:", os.environ.get("DOCKER_HOST", "(not set)"))
print("rule of thumb: anyone who can write to that socket can start a container with -v /:/host = root on the host")
```

**Output (my run):** docker CLI 29.9.2. `docker version` and `docker info` printed the Client sections and then a connection error for the Server section, so there is **no daemon, no containerd and no runc information** to read here. Nothing about the server side was executed.
```text
$ docker version
Client: Docker Engine - Community
 Version:           29.9.2
 API version:       1.56
 Go version:        go1.26.10
 Git commit:        a82e528
 Built:             Tue Oct 20 18:44:40 2026
 OS/Arch:           linux/amd64
 Context:           default
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory

$ docker info
Client: Docker Engine - Community
 Version:    29.9.2
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.38.1
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v5.6.1
    Path:     /usr/libexec/docker/cli-plugins/docker-compose

Server:
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory

$ python3 -I sock_check.py
/var/run/docker.sock: not found -> no local dockerd; the docker CLI has nothing to talk to
DOCKER_HOST env: (not set)
rule of thumb: anyone who can write to that socket can start a container with -v /:/host = root on the host
```

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

### Q37 ⭐ 🟡 Inside an image: manifest, config, layers, digests. Explain content-addressable storage, how a layer tar and a config JSON hash into a sha256 digest, why identical layers are shared and cached, what docker save produces, and how the build history is stored in the config. Write a Python script that builds a tiny OCI-style image layout by hand (a layer tar, a config JSON, a manifest), computes digests, and verifies them; state clearly that this is a teaching model and not a real docker image.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** An image is just files addressed by their sha256 hash: layer tars, one config JSON and one manifest that lists them by digest, so change one byte and the digest changes.

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
```python
# ===== oci_toy.py =====
"""Q37: TEACHING MODEL of an OCI-style image layout. Not a real docker image.
Run: python3 -I oci_toy.py"""
import gzip, hashlib, io, json, os, tarfile, tempfile

def sha(b): return "sha256:" + hashlib.sha256(b).hexdigest()

def make_layer(files):
    """A layer = tar of files. Fixed mtime/owner so the same files give the same bytes."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as t:
        for name, data in sorted(files.items()):
            ti = tarfile.TarInfo(name); ti.size = len(data); ti.mtime = 0
            ti.uid = ti.gid = 0; ti.uname = ti.gname = ""
            t.addfile(ti, io.BytesIO(data))
    return buf.getvalue()

def gz(b):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", mtime=0) as g: g.write(b)
    return out.getvalue()

def write_blob(root, data):
    d = sha(data); path = os.path.join(root, "blobs", "sha256", d.split(":")[1])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(data); return d, len(data)

def build(root, layer_files_list, cmd):
    layers, diff_ids, history = [], [], []
    for files, created_by in layer_files_list:
        raw = make_layer(files); packed = gz(raw)
        d, n = write_blob(root, packed)
        layers.append({"mediaType": "application/vnd.oci.image.layer.v1.tar+gzip", "digest": d, "size": n})
        diff_ids.append(sha(raw))                      # diff_id = hash of UNcompressed tar
        history.append({"created_by": created_by})
    config = {"architecture": "amd64", "os": "linux", "config": {"Cmd": cmd},
              "rootfs": {"type": "layers", "diff_ids": diff_ids}, "history": history}
    cd, cn = write_blob(root, json.dumps(config, sort_keys=True).encode())
    manifest = {"schemaVersion": 2, "mediaType": "application/vnd.oci.image.manifest.v1+json",
                "config": {"mediaType": "application/vnd.oci.image.config.v1+json", "digest": cd, "size": cn},
                "layers": layers}
    md, mn = write_blob(root, json.dumps(manifest, sort_keys=True).encode())
    json.dump({"schemaVersion": 2, "manifests": [{"mediaType": manifest["mediaType"], "digest": md, "size": mn}]},
              open(os.path.join(root, "index.json"), "w"))
    json.dump({"imageLayoutVersion": "1.0.0"}, open(os.path.join(root, "oci-layout"), "w"))
    return md

def verify(root):
    ok = True
    for fn in os.listdir(os.path.join(root, "blobs", "sha256")):
        data = open(os.path.join(root, "blobs", "sha256", fn), "rb").read()
        good = hashlib.sha256(data).hexdigest() == fn
        ok &= good
    idx = json.load(open(os.path.join(root, "index.json")))
    mdig = idx["manifests"][0]["digest"].split(":")[1]
    man = json.load(open(os.path.join(root, "blobs", "sha256", mdig)))
    cfg = json.load(open(os.path.join(root, "blobs", "sha256", man["config"]["digest"].split(":")[1])))
    for layer, diff in zip(man["layers"], cfg["rootfs"]["diff_ids"]):
        try:
            raw = gzip.decompress(open(os.path.join(root, "blobs", "sha256", layer["digest"].split(":")[1]), "rb").read())
            ok &= sha(raw) == diff
        except (OSError, EOFError):                    # corrupt gzip counts as a failed check
            ok = False
    return ok, man, cfg

base = ({"etc/os-release": b"toy-linux 1\n", "usr/lib/libc.so": b"libc"}, "FROM toy-linux")
deps = ({"app/site-packages/numpy.py": b"# numpy"}, "RUN pip install numpy")
v1 = ({"app/main.py": b"print('v1')\n"}, "COPY main.py /app")
v2 = ({"app/main.py": b"print('v2')\n"}, "COPY main.py /app")

tmp = tempfile.mkdtemp()
a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
ma = build(a, [base, deps, v1], ["python", "/app/main.py"])
mb = build(b, [base, deps, v2], ["python", "/app/main.py"])
ok, man, cfg = verify(a)
print("image A verifies:", ok, "| image B verifies:", verify(b)[1] is not None and verify(b)[0])
print("manifest digests differ:", ma != mb)
la = [l["digest"][7:19] for l in man["layers"]]
lb = [l["digest"][7:19] for l in json.load(open(os.path.join(b, "blobs/sha256", mb[7:])))["layers"]]
print("layers A:", la); print("layers B:", lb)
print("shared layers:", [x for x in la if x in lb])
print("history from config:", [h["created_by"] for h in cfg["history"]])
# tamper test
blob = os.path.join(a, "blobs", "sha256", man["layers"][0]["digest"][7:])
open(blob, "ab").write(b"x")
print("after flipping one byte in a layer blob, verifies:", verify(a)[0])
```

**Output (my run):** Python 3.13.17. Real run of the script above.
```text
$ python3 -I oci_toy.py
image A verifies: True | image B verifies: True
manifest digests differ: True
layers A: ['7cdac34538fa', '3e8c8d7cda41', '937a779e03f6']
layers B: ['7cdac34538fa', '3e8c8d7cda41', 'bd21a27ba4d9']
shared layers: ['7cdac34538fa', '3e8c8d7cda41']
history from config: ['FROM toy-linux', 'RUN pip install numpy', 'COPY main.py /app']
after flipping one byte in a layer blob, verifies: False
```


**Follow-ups:**
- *Tag vs digest?* A tag is a movable label; a digest is immutable content. Pin by digest in production, keep a human tag for reading.
- *Why does adding a layer at the end not re-upload earlier ones?* Their digests are unchanged and the registry already has them.
- *Does deleting a file in a later layer shrink the image?* No. The earlier layer still holds the bytes; the later one adds a "whiteout" marker.

**Common mistakes:**
- Mixing up diff_id (uncompressed) with the layer blob digest (compressed).
- Believing a tag name identifies content.
- Putting a secret in an early layer and deleting it later; it stays in that layer.
- Expecting identical hashes from rebuilds without fixing timestamps and file order.

### Q38 ⭐ 🟡 Entrypoint script patterns for ML containers. Write entrypoint.sh that sets defaults from env vars, waits for a dependency with a timeout, runs a migration or model-download step, then ends with exec '$@' so the server becomes PID 1 and receives signals. Explain set -euo pipefail, why exec matters, CRLF and executable-bit pitfalls, and when a Python entrypoint is better. Run the script locally with a fake dependency and show the output.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** The entrypoint script does the setup (defaults, wait, one-time download) and finishes with `exec "$@"`, so the real server replaces the shell, becomes PID 1 and receives SIGTERM from `docker stop`.

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
```bash
# ===== entrypoint.sh =====
#!/usr/bin/env bash
set -euo pipefail

# 1. defaults from env
: "${MODEL_DIR:=/tmp/models}"
: "${DEP_HOST:=127.0.0.1}"
: "${DEP_PORT:=5999}"
: "${DEP_TIMEOUT:=10}"

# 2. wait for a dependency, with a timeout (bash /dev/tcp, no extra tools needed)
echo "[entrypoint] pid=$$ waiting for ${DEP_HOST}:${DEP_PORT} (max ${DEP_TIMEOUT}s)"
deadline=$(( $(date +%s) + DEP_TIMEOUT ))
until (exec 3<>"/dev/tcp/${DEP_HOST}/${DEP_PORT}") 2>/dev/null; do
  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "[entrypoint] dependency not reachable, giving up" >&2
    exit 1
  fi
  sleep 0.5
done
echo "[entrypoint] dependency is up"

# 3. one-time setup: model download stand-in (idempotent: skip if already there)
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_DIR/model.bin" ]; then
  echo "[entrypoint] fetching model into $MODEL_DIR"
  printf 'fake-weights' > "$MODEL_DIR/model.bin"
else
  echo "[entrypoint] model already present, skipping download"
fi

# 4. hand over: exec replaces the shell, the server becomes PID 1 in a container
echo "[entrypoint] exec: $*"
exec "$@"

# ===== crlf_demo.sh =====
#!/usr/bin/env bash
# Q38 pitfalls: CRLF line endings and a missing executable bit
d=$(mktemp -d); cd "$d"
printf '#!/usr/bin/env bash\r\necho hello\r\n' > crlf.sh; chmod +x crlf.sh
echo "== CRLF script"; ./crlf.sh; echo "exit=$?"
printf '#!/usr/bin/env bash\necho hello\n' > noexec.sh
echo "== no executable bit"; ./noexec.sh; echo "exit=$?"
echo "== fix: strip CR (sed -i 's/\r$//') and chmod +x"
sed -i 's/\r$//' crlf.sh; ./crlf.sh; echo "exit=$?"
rm -rf "$d"
```

```python
# ===== server.py =====
import os, signal, sys, time
def bye(signum, frame):
    print(f"[server] pid={os.getpid()} got SIGTERM, shutting down cleanly", flush=True)
    sys.exit(0)
signal.signal(signal.SIGTERM, bye)
print(f"[server] pid={os.getpid()} ppid={os.getppid()} started", flush=True)
while True:
    time.sleep(0.2)

# ===== fake_dep.py =====
"""Fake dependency: opens a TCP port after a delay."""
import socket, sys, time
time.sleep(float(sys.argv[2]))
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", int(sys.argv[1]))); s.listen()
time.sleep(30)

# ===== drive.py =====
"""Q38 driver. Run: python3 -I drive.py   (needs bash). Runs entrypoint.sh against a fake dependency."""
import os, shutil, signal, subprocess, sys, tempfile, time

here = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
env = dict(os.environ, MODEL_DIR=os.path.join(tmp, "models"), DEP_PORT="5999", DEP_TIMEOUT="10")

def run(script, label, dep_delay="1.5", port="5999"):
    print(f"--- {label}")
    dep = subprocess.Popen([sys.executable, os.path.join(here, "fake_dep.py"), port, dep_delay])
    e = dict(env, DEP_PORT=port)
    p = subprocess.Popen([os.path.join(here, script), sys.executable, os.path.join(here, "server.py"), "q38_server_marker"],
                         env=e, stdout=subprocess.PIPE, text=True)
    time.sleep(3.5)
    print(f"[driver] sending SIGTERM to entrypoint pid {p.pid}", flush=True)
    p.send_signal(signal.SIGTERM)
    try:
        out, _ = p.communicate(timeout=5)
        print(out.rstrip())
        print("[driver] container-like process exited with", p.returncode)
    except subprocess.TimeoutExpired:
        p.kill()
        subprocess.run(["pkill", "-9", "-f", "q38_server_marker"])   # orphan keeps the pipe open
        out, _ = p.communicate(); print(out.rstrip())
        print("[driver] no clean shutdown within 5s: server never saw SIGTERM; killed it by hand")
    dep.kill()

run("entrypoint.sh", "WITH exec", port="5999")
run("entrypoint_noexec.sh", "WITHOUT exec (server is a child of bash)", port="5998")
# timeout path
print("--- dependency never comes up (timeout 2s)")
r = subprocess.run([os.path.join(here, "entrypoint.sh"), "true"], env=dict(env, DEP_PORT="5997", DEP_TIMEOUT="2"),
                   capture_output=True, text=True)
print(r.stdout.rstrip()); print(r.stderr.rstrip()); print("exit code:", r.returncode)
# cleanup stray servers from the no-exec case
subprocess.run(["pkill", "-9", "-f", "q38_server_marker"])
shutil.rmtree(tmp)
```

**Output (my run):** bash and Python 3.13.17. The driver starts the fake dependency, runs the script, then sends SIGTERM to the process it started. Not a container: signals are real, PID 1 is not. In a real container the script runs as PID 1, which is **not executed** here.
```text
$ python3 -I drive.py
--- WITH exec
[driver] sending SIGTERM to entrypoint pid 20527
[entrypoint] pid=20527 waiting for 127.0.0.1:5999 (max 10s)
[entrypoint] dependency is up
[entrypoint] fetching model into /tmp/tmp5jw0clkr/models
[entrypoint] exec: /usr/bin/python3 <code>/q38/server.py q38_server_marker
[server] pid=20527 ppid=20525 started
[server] pid=20527 got SIGTERM, shutting down cleanly
[driver] container-like process exited with 0
--- WITHOUT exec (server is a child of bash)
[driver] sending SIGTERM to entrypoint pid 20544
[entrypoint] pid=20544 waiting for 127.0.0.1:5998 (max 10s)
[entrypoint] dependency is up
[entrypoint] model already present, skipping download
[entrypoint] exec: /usr/bin/python3 <code>/q38/server.py q38_server_marker
[server] pid=20557 ppid=20544 started
[driver] no clean shutdown within 5s: server never saw SIGTERM; killed it by hand
--- dependency never comes up (timeout 2s)
[entrypoint] pid=20559 waiting for 127.0.0.1:5997 (max 2s)
[entrypoint] dependency not reachable, giving up
exit code: 1

$ bash crlf_demo.sh
== CRLF script
exit=127
== no executable bit
exit=126
== fix: strip CR (sed -i 's/\r$//') and chmod +x
hello
exit=0
/usr/bin/env: ‘bash\r’: No such file or directory
/usr/bin/env: use -[v]S to pass options in shebang lines
crlf_demo.sh: line 7: ./noexec.sh: Permission denied
```

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

### Q39 ⭐ 🟢 Do we need Docker at all? Compare a venv with a lockfile, conda environments, Nix or devbox (hedge), and Docker for reproducing an ML environment and deploying a model. Cover what Docker adds (OS libraries, same artifact from dev to prod, isolation) and what it does not fix (GPU driver on host, data versions, non-determinism, kernel). Give a decision rule for a 3-person team and for a 30-person platform team.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** I do not reach for Docker by default; a venv with a lockfile is enough to reproduce Python packages, and Docker earns its place when OS libraries, one artifact from dev to prod, or isolation matter.

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
```python
# ===== env_report.py =====
"""Q39: what a venv+lockfile pins, and what only the host decides. Run: python3 -I env_report.py"""
import os, platform, shutil, sys
from importlib import metadata

print("== pinned by a lockfile (python packages)")
for p in ("numpy", "pyyaml"):
    try: print(f"  {p}=={metadata.version(p)}")
    except metadata.PackageNotFoundError: print(f"  {p}: not installed")

print("== NOT pinned by a lockfile (comes from the machine)")
print("  libc:", " ".join(platform.libc_ver()))
print("  kernel:", platform.release(), "(a container shares the HOST kernel)")
print("  cpu count:", os.cpu_count(), "| arch:", platform.machine())
print("  nvidia-smi on PATH:", bool(shutil.which("nvidia-smi")), "(GPU driver is a host thing, never inside the image)")
print("  nvcc on PATH:", bool(shutil.which("nvcc")))

def choose(team_size, needs_gpu_libs, deploys_to_cluster, mixed_os_laptops):
    """Decision rule used in the answer. Returns a short recommendation."""
    if deploys_to_cluster or (needs_gpu_libs and team_size > 10):
        return "Docker image for deploy and CI; devs may still use venv/conda locally"
    if mixed_os_laptops and needs_gpu_libs:
        return "conda (or Docker dev container) so CUDA libs match; lock it"
    return "venv + lockfile (uv/pip-tools), add Docker only when you deploy"

print("== decision rule examples")
for args in [(3, False, False, False), (3, True, True, False), (3, True, False, True), (30, True, True, True)]:
    print(f"  team={args[0]:>2} gpu_libs={args[1]!s:<5} cluster={args[2]!s:<5} mixed_os={args[3]!s:<5} -> {choose(*args)}")
```

**Output (my run):** Python 3.13.17. No GPU, no nvidia-smi here.
```text
$ python3 -I env_report.py
== pinned by a lockfile (python packages)
  numpy==2.5.3
  pyyaml==6.0.1
== NOT pinned by a lockfile (comes from the machine)
  libc: glibc 2.39
  kernel: 6.18.44-fc-v153 (a container shares the HOST kernel)
  cpu count: 4 | arch: x86_64
  nvidia-smi on PATH: False (GPU driver is a host thing, never inside the image)
  nvcc on PATH: False
== decision rule examples
  team= 3 gpu_libs=False cluster=False mixed_os=False -> venv + lockfile (uv/pip-tools), add Docker only when you deploy
  team= 3 gpu_libs=True  cluster=True  mixed_os=False -> Docker image for deploy and CI; devs may still use venv/conda locally
  team= 3 gpu_libs=True  cluster=False mixed_os=True  -> conda (or Docker dev container) so CUDA libs match; lock it
  team=30 gpu_libs=True  cluster=True  mixed_os=True  -> Docker image for deploy and CI; devs may still use venv/conda locally
```


**Follow-ups:**
- *Is a conda env a good Docker replacement?* For Python and compiled libs yes; for OS packages, services and deployment no.
- *Dev containers?* Good for onboarding when laptops differ. A cost: slower file mounts on some OSes.
- *Does Docker give reproducible training?* Not alone. You still need data version, seeds and the same hardware.

**Common mistakes:**
- "We use Docker, so it is reproducible" with unpinned installs and `:latest` bases.
- Thinking the container includes the GPU driver.
- Not pinning Python itself.
- Dockerising everything for a solo notebook project.

### Q40 ⭐ 🟡 One process per container and server workers. A team runs gunicorn with 8 workers inside one container and also cron and nginx in it. Explain the one-main-process guideline, supervising multiple processes, workers per container versus replicas, memory duplication when each worker loads the model (and fork-after-load copy-on-write caveats), CPU limits versus worker counts, and when a sidecar is cleaner. Serving frameworks themselves are a later part; stay on the container angle.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** One container should run one main process; gunicorn with a few workers is fine, but cron and nginx belong in their own containers, and scaling is usually more replicas, not more workers.

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
```python
# ===== fork_memory.py =====
"""Q40: memory cost of N workers that each hold a 'model'. Linux only.
Measures PSS (proportional set size: shared pages are split between the processes sharing them).
Run: python3 -I fork_memory.py"""
import os, sys, time
import numpy as np

N_WORKERS = 4
MB = 1024 * 1024

def pss_mb(pid="self"):
    with open(f"/proc/{pid}/smaps_rollup") as f:
        for line in f:
            if line.startswith("Pss:"):
                return int(line.split()[1]) / 1024

def make_array_model():          # one big numpy buffer, like weights; read-only after load
    return np.ones(25_000_000, dtype=np.float64)          # ~190 MB

def make_object_model():         # millions of small Python objects, like a big dict/list of floats
    return [float(i) + 0.5 for i in range(3_000_000)]     # every object has a refcount

def run(label, loader, touch):
    """Parent loads, then forks N workers. Each worker 'serves' (touch) and reports its own PSS."""
    model = loader()
    parent_before = pss_mb()
    r, w = os.pipe()
    pids = []
    for _ in range(N_WORKERS):
        pid = os.fork()
        if pid == 0:
            touch(model)                                   # simulate a request using the model
            os.write(w, f"{pss_mb():.0f}\n".encode())
            time.sleep(1.0)                                # stay alive while the parent measures
            os._exit(0)
        pids.append(pid)
    time.sleep(0.7)
    os.close(w)
    kids = [float(x) for x in os.read(r, 4096).decode().split()]
    total = pss_mb() + sum(kids)
    for pid in pids: os.waitpid(pid, 0)
    print(f"{label:<52} parent {parent_before:6.0f} MB | worker PSS {kids} | total {total:6.0f} MB")

arr_touch = lambda m: m[:1000].sum()                               # reads a few bytes of the buffer
def obj_touch(m):
    s = 0.0
    for x in m: s += x                                             # iterating bumps refcounts on every object
run("array model, fork after load, light use", make_array_model, arr_touch)
run("object model, fork after load, full pass (COW breaks)", make_object_model, obj_touch)
one = make_array_model(); print(f"one process holding the array model: {pss_mb():.0f} MB (so {N_WORKERS} separate loads would be ~{N_WORKERS*pss_mb():.0f} MB)")

# ===== workers.py =====
"""Q40: pick a worker count from the CONTAINER CPU limit, not the host core count.
Run: python3 -I workers.py"""
import math, os

def cpu_limit():
    """cgroup v2 cpu.max looks like 'max 100000' (no limit) or '200000 100000' (= 2 CPUs)."""
    try:
        quota, period = open("/sys/fs/cgroup/cpu.max").read().split()
        if quota != "max":
            return int(quota) / int(period)
    except (FileNotFoundError, ValueError):
        pass
    return float(len(os.sched_getaffinity(0)))            # fallback: CPUs this process may use

def workers(cpus, model_mb, mem_limit_mb, shared_fraction=0.0):
    by_cpu = max(1, math.floor(cpus))
    # memory per extra worker: private part of the model plus ~ nothing for shared pages
    per_worker = model_mb * (1 - shared_fraction)
    by_mem = max(1, int((mem_limit_mb - model_mb) // max(per_worker, 1)) + 1)
    return min(by_cpu, by_mem), by_cpu, by_mem

print("detected CPU limit:", cpu_limit())
for cpus, model, mem, shared in [(2, 800, 4096, 0.0), (8, 800, 4096, 0.0), (8, 800, 4096, 0.9)]:
    w, c, m = workers(cpus, model, mem, shared)
    print(f"cpus={cpus} model={model}MB mem_limit={mem}MB shared={shared:.0%} -> by_cpu={c} by_mem={m} -> use {w}")
```

```yaml
# ===== compose.yml =====
services:
  api:                       # ONE main process: gunicorn with few workers, or 1 worker + more replicas
    image: registry.example.com/ml/api:1.4.2
    command: ["gunicorn", "app:app", "--workers", "2", "--bind", "0.0.0.0:8000", "--preload"]
    cpus: 2
    mem_limit: 4g
    expose: ["8000"]
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/healthz')"]
      start_period: 60s
  proxy:                     # nginx is its own container, not a process inside the API container
    image: nginx:1.27-alpine
    ports: ["8080:80"]
    depends_on:
      api:
        condition: service_healthy
  nightly:                   # cron job = its own container, run on a schedule from outside
    image: registry.example.com/ml/api:1.4.2
    command: ["python", "-m", "jobs.nightly"]
    profiles: ["jobs"]
```

**Output (my run):** Python 3.13.17, numpy 2.5.3, Linux, 4 workers. PSS (proportional set size) splits each shared page between the processes that share it, so the total is the real memory cost. The sizes are from this sandbox and only show the pattern. Starting the services is **not executed** (no daemon); `docker compose config` validates the YAML.
```text
$ python3 -I fork_memory.py
array model, fork after load, light use              parent    213 MB | worker PSS [51.0, 43.0, 42.0, 42.0] | total    226 MB
object model, fork after load, full pass (COW breaks) parent    137 MB | worker PSS [100.0, 100.0, 100.0, 100.0] | total    507 MB
one process holding the array model: 214 MB (so 4 separate loads would be ~857 MB)

$ python3 -I workers.py
detected CPU limit: 4.0
cpus=2 model=800MB mem_limit=4096MB shared=0% -> by_cpu=2 by_mem=5 -> use 2
cpus=8 model=800MB mem_limit=4096MB shared=0% -> by_cpu=8 by_mem=5 -> use 5
cpus=8 model=800MB mem_limit=4096MB shared=90% -> by_cpu=8 by_mem=42 -> use 8

$ docker compose -f compose.yml config --services
api
proxy
```

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

### Q41 ⭐ 🟢 Compose versus Swarm versus an orchestrator. When is docker compose enough for ML (one GPU VM, a demo, a small internal tool), what does it lack (self-healing across nodes, rolling updates, autoscaling, scheduling GPUs across machines), and what is the status of Swarm (hedge; check current docs). Give a rule for when to move up, without going into Kubernetes details.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Compose is enough for one machine, such as a GPU VM, a demo or a small internal tool; once I need several machines, rolling updates, autoscaling or GPU scheduling across nodes, I move to an orchestrator.

**Then explain:**
- **Compose is good at:** describing a few services, volumes and networks in one file, one command to start (`docker compose up`), same file in dev and on the VM, `restart: unless-stopped` for simple recovery.
- **What it lacks:** self-healing across nodes (if the VM dies, everything is down), zero-downtime rolling updates and rollbacks, autoscaling on load, scheduling GPUs across machines, secrets and config management at scale, proper multi-node networking.
- **Swarm:** Docker's built-in clustering (`docker swarm init`, stacks). It adds multi-node, replicas and rolling updates with a small learning curve, but its community and ecosystem are much smaller than Kubernetes, and Docker has moved focus elsewhere. Hedge: check current Docker docs for its support status before choosing it for new work.
- **Rule for moving up:** move when you need **any two** of: more than one machine, uptime promises with rolling updates, autoscaling, many teams sharing GPUs, or audit and policy needs. Not before: an orchestrator is a team's worth of work.
- **Failure mode:** `restart: unless-stopped` hides crash loops. Without healthchecks and alerts, a model that crashes on load keeps restarting quietly.
- **Failure mode:** the Compose `deploy:` section is partly ignored outside Swarm/Kubernetes. GPU `reservations.devices` is honoured by Compose on a host with the NVIDIA runtime; `replicas` and `update_config` are not full rolling updates (check current docs).

**Example:** An internal summariser demo: one GPU VM, API + Redis, 20 users. Compose. Later, 3 models, 2 GPU nodes, a team that needs a deploy without downtime: orchestrator.

**Code:** a Compose file with a GPU reservation, and a deliberately broken one.
```yaml
# ===== compose.yml =====
services:
  model:
    image: registry.example.com/ml/model:2.0.1
    restart: unless-stopped            # restarts on THIS machine only
    ports: ["8000:8000"]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  redis:
    image: redis:7-alpine
    restart: unless-stopped

# ===== bad.yml =====
services:
  model:
    image: registry.example.com/ml/model:2.0.1
    restrat: unless-stopped
```

```bash
# ===== check.sh =====
#!/usr/bin/env bash
# Q41: validate a compose file without a daemon
docker compose -f compose.yml config
echo "--- typo file"
docker compose -f bad.yml config; echo "exit=$?"
```

**Output (my run):** docker compose v5.6.1. `config` validates and normalises without a daemon. Starting the stack and the GPU reservation actually working is **not executed** (no daemon, no GPU).
```text
$ docker compose -f compose.yml config
name: q41
services:
  model:
    deploy:
      resources:
        reservations:
          devices:
            - capabilities:
                - gpu
              driver: nvidia
              count: 1
    restart: unless-stopped
    image: registry.example.com/ml/model:2.0.1
    networks:
      default: null
    ports:
      - mode: ingress
        target: 8000
        published: "8000"
        protocol: tcp
  redis:
    restart: unless-stopped
    image: redis:7-alpine
    networks:
      default: null
networks:
  default:
    name: q41_default

$ docker compose -f bad.yml config; echo "exit=$?"
exit=1
validating <code>/q41/bad.yml: services.model.restrat false schema
```

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

### Q42 ⭐ 🟡 'nvidia-smi says CUDA 12.x but nvcc --version says 11.8, which one is right?' Explain that nvidia-smi shows the maximum CUDA version the driver supports while nvcc shows the installed toolkit, why the toolkit inside the image is what compiled code needs, how the PyTorch wheel bundles its own runtime, and how to check torch.version.cuda and torch.cuda.is_available() inside the container. Give a compatibility checklist (driver, container CUDA, framework wheel, cuDNN, GPU architecture) and a Python script that prints versions, run locally on a CPU-only machine with the output interpreted honestly.
**Asked at:** NVIDIA Container Toolkit user guide and runtime docs (docs.nvidia.com, several versions), E2E Networks GPU-in-Docker guide, HowToGeek and LinuxConfig tutorials (search snippets only, not opened); vendor docs and tutorials, not interview reports; GPU and deep-learning MLOps roles (Bengaluru postings mention GPU/CUDA workloads on Kubernetes)
**Say this first (1 line):** Both are right: `nvidia-smi` shows the newest CUDA the **driver** supports, `nvcc` shows the **toolkit** installed, and what matters is the CUDA runtime your framework or image actually uses, which must be no newer than the driver supports.

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
```python
# ===== cuda_report.py =====
"""Q42: print every version that matters; interpret what is missing. Run: python3 -I cuda_report.py"""
import re, shutil, subprocess

def sh(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout
    except Exception as e:
        return ""

def parse_smi(text):
    m = re.search(r"Driver Version:\s*([\d.]+).*?CUDA Version:\s*([\d.]+)", text)
    return m.groups() if m else None

def parse_nvcc(text):
    m = re.search(r"release\s+([\d.]+)", text)
    return m.group(1) if m else None

def ver(s): return tuple(int(x) for x in s.split("."))

def verdict(driver_max_cuda, runtime_cuda):
    """A CUDA runtime in the image works if the driver's max supported CUDA is >= it
    (simple rule; minor-version compatibility and forward-compat packages exist, check NVIDIA docs)."""
    return "ok" if ver(driver_max_cuda) >= ver(runtime_cuda) else "driver too old for this image"

print("== this machine")
smi = shutil.which("nvidia-smi")
print("nvidia-smi:", parse_smi(sh([smi])) if smi else "not found (no NVIDIA driver here)")
nvcc = shutil.which("nvcc")
print("nvcc:", parse_nvcc(sh([nvcc, "--version"])) if nvcc else "not found (no CUDA toolkit here)")
try:
    import torch
    print("torch:", torch.__version__, "| torch.version.cuda:", torch.version.cuda,
          "| is_available:", torch.cuda.is_available())
except ImportError:
    print("torch: not installed in this sandbox (so no torch.version.cuda to read)")

print("== the question from the interview, with pasted sample text (not from this machine)")
sample_smi = "| NVIDIA-SMI 550.54   Driver Version: 550.54   CUDA Version: 12.4 |"
sample_nvcc = "Cuda compilation tools, release 11.8, V11.8.89"
d, c = parse_smi(sample_smi); t = parse_nvcc(sample_nvcc)
print(f"nvidia-smi says CUDA {c} (driver {d}); nvcc says {t}")
print(f"driver supports up to {c}; toolkit {t} is what compiled code used -> {verdict(c, t)}")
print("== image/driver checks")
for drv_max, img in [("12.4", "11.8"), ("12.4", "12.4"), ("11.8", "12.4")]:
    print(f"driver max CUDA {drv_max}, image CUDA {img}: {verdict(drv_max, img)}")
```

**Output (my run):** Python 3.13.17, CPU-only sandbox. `torch` is **not installed** here (my pip install from the PyTorch CPU index failed through the proxy), so `torch.version.cuda` and `is_available()` were **not executed**.
```text
$ python3 -I cuda_report.py
== this machine
nvidia-smi: not found (no NVIDIA driver here)
nvcc: not found (no CUDA toolkit here)
torch: not installed in this sandbox (so no torch.version.cuda to read)
== the question from the interview, with pasted sample text (not from this machine)
nvidia-smi says CUDA 12.4 (driver 550.54); nvcc says 11.8
driver supports up to 12.4; toolkit 11.8 is what compiled code used -> ok
== image/driver checks
driver max CUDA 12.4, image CUDA 11.8: ok
driver max CUDA 12.4, image CUDA 12.4: ok
driver max CUDA 11.8, image CUDA 12.4: driver too old for this image
```

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

### Q43 ⭐ 🔴 Containerising an LLM or embedding server (container angle only; serving internals belong to Book 2). Cover a GPU image for a vLLM-style or Ollama-style server, where the Hugging Face cache and model weights live (volume), the gated-model token as a runtime secret, shm and ipc settings, healthcheck with a long warm-up, image size versus weight size, and pinning versions. Show a compose file; validate it by script; actually starting it is not executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** I keep the image small and pinned, put weights in a volume, pass the Hugging Face token at runtime, give the container enough shared memory, and use a healthcheck with a long start period because loading the model takes minutes.

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
```yaml
# ===== compose.yml =====
services:
  llm:
    image: vllm/vllm-openai:${VLLM_TAG:?set VLLM_TAG to a pinned release tag}   # never :latest
    command: ["--model", "${MODEL_ID:?set MODEL_ID}", "--max-model-len", "8192"]
    ipc: host                          # or shm_size: "16gb"; some runtimes need large shared memory
    environment:
      HF_TOKEN:                        # no value here: taken from the shell at runtime
      HF_HOME: /models/hf
    volumes:
      - hf_cache:/models/hf            # weights live in a volume, not in the image
    ports: ["127.0.0.1:8000:8000"]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 5
      start_period: 600s               # weights download + load can take minutes
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
volumes:
  hf_cache:
```

```python
# ===== validate.py =====
"""Q43: policy checks on a compose file. Uses `docker compose config --format json` (no daemon needed).
Run: python3 -I validate.py compose.yml"""
import json, os, re, subprocess, sys
import yaml

def seconds(d):
    """'10m0s' -> 600. Compose prints durations in Go style."""
    return sum(float(n) * {'h': 3600, 'm': 60, 's': 1}[u] for n, u in re.findall(r'([\d.]+)([hms])', d))

env = dict(os.environ, VLLM_TAG="v0.0.0-example", MODEL_ID="org/model", HF_TOKEN="hf_FAKE_for_demo")
cfg = json.loads(subprocess.run(["docker", "compose", "-f", sys.argv[1], "config", "--format", "json"],
                                capture_output=True, text=True, env=env, check=True).stdout)
svc = cfg["services"]["llm"]
checks = {}
checks["image pinned (not latest, has tag)"] = ":" in svc["image"] and not svc["image"].endswith(":latest")
checks["GPU reserved"] = any("gpu" in d["capabilities"] for d in svc["deploy"]["resources"]["reservations"]["devices"])
checks["shm: ipc host or shm_size"] = svc.get("ipc") == "host" or "shm_size" in svc
checks["weights on a named volume"] = any(v["type"] == "volume" for v in svc["volumes"])
raw = yaml.safe_load(open(sys.argv[1]))["services"]["llm"]["environment"]
checks["HF_TOKEN has no value in the file (pass-through)"] = "HF_TOKEN" in raw and raw["HF_TOKEN"] is None
checks["healthcheck start_period >= 300s"] = seconds(svc["healthcheck"]["start_period"]) >= 300
checks["port bound to 127.0.0.1"] = svc["ports"][0].get("host_ip") == "127.0.0.1"
for k, v in checks.items(): print(("PASS" if v else "FAIL"), k)
sys.exit(0 if all(checks.values()) else 1)
```

**Output (my run):** docker compose v5.6.1, Python 3.13.17. Starting this service, pulling the image, GPU access, the download and the healthcheck are **not executed** (no daemon, no GPU, no network to pull). The validator ran against the real normalised config, with fake values for the three variables, then against a deliberately bad copy (`:latest` and a literal token).
```text
$ python3 -I validate.py compose.yml; echo "exit=$?"
PASS image pinned (not latest, has tag)
PASS GPU reserved
PASS shm: ipc host or shm_size
PASS weights on a named volume
PASS HF_TOKEN has no value in the file (pass-through)
PASS healthcheck start_period >= 300s
PASS port bound to 127.0.0.1
exit=0

$ sed 's/vllm-openai:${VLLM_TAG:?set VLLM_TAG to a pinned release tag}/vllm-openai:latest/; s/HF_TOKEN:  .*/HF_TOKEN: hf_realtoken123/' compose.yml > /tmp/bad43.yml; python3 -I validate.py /tmp/bad43.yml; echo "exit=$?"
FAIL image pinned (not latest, has tag)
PASS GPU reserved
PASS shm: ipc host or shm_size
PASS weights on a named volume
FAIL HF_TOKEN has no value in the file (pass-through)
PASS healthcheck start_period >= 300s
PASS port bound to 127.0.0.1
exit=1

$ VLLM_TAG= docker compose -f compose.yml config --quiet; echo "exit=$?"
exit=1
error while interpolating services.llm.command.[]: required variable MODEL_ID is missing a value: set MODEL_ID
error while interpolating services.llm.image: required variable VLLM_TAG is missing a value: set VLLM_TAG to a pinned release tag
```

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

### Q44 ⭐ 🟢 Rapid-fire Docker CLI drill for an interview. In one throwaway session explain and order: run -d -p -v --rm -it --name, exec, logs -f, ps -a, stop versus kill, rm and rmi, inspect with --format, cp, stats, tag, push, build -t -f --target, history, save and load, system prune. Say which of them can be shown without a daemon here (docker --help, docker build --help, docker compose config) and run those; mark the rest not executed.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** I group the CLI by what it does: run and inspect containers, look at logs and resources, move images around, build, and clean up; most of them need a daemon, so here I can only prove the flags exist from `--help`.

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
```python
# ===== drill_check.py =====
"""Q44: confirm every command and flag in the drill exists, using only --help (no daemon).
Run: python3 -I drill_check.py"""
import re, subprocess

DRILL = [  # (subcommand words, flags that must appear in its --help)
    (["run"], ["-d", "-p", "-v", "--rm", "-i", "-t", "--name", "--gpus", "-e"]),
    (["exec"], ["-i", "-t"]), (["logs"], ["-f", "--tail"]), (["ps"], ["-a"]),
    (["stop"], ["-t"]), (["kill"], ["-s"]), (["rm"], ["-f", "-v"]), (["rmi"], ["-f"]),
    (["inspect"], ["--format"]), (["cp"], []), (["stats"], ["--no-stream"]),
    (["tag"], []), (["push"], []), (["build"], ["-t", "-f", "--target", "--build-arg"]),
    (["history"], ["--no-trunc"]), (["save"], ["-o"]), (["load"], ["-i"]),
    (["system", "prune"], ["-a", "--volumes"]),
]
ok_all = True
for words, flags in DRILL:
    text = subprocess.run(["docker", *words, "--help"], capture_output=True, text=True).stdout
    missing = [f for f in flags if not re.search(r"(^|[\s,])" + re.escape(f) + r"([\s,=\[]|$)", text, re.M)]
    ok_all &= not missing and bool(text)
    print(f"docker {' '.join(words):<13} help ok={bool(text)!s:<5} flags {flags} missing={missing}")
print("ALL OK" if ok_all else "SOMETHING MISSING")
```

**Output (my run):** docker CLI 29.9.2. The check ran `docker <command> --help` for 18 commands. The error at the end is `docker ps` showing the daemon is missing; every real build, run, logs, exec, push and prune call is **not executed**.
```text
$ python3 -I drill_check.py
docker run           help ok=True  flags ['-d', '-p', '-v', '--rm', '-i', '-t', '--name', '--gpus', '-e'] missing=[]
docker exec          help ok=True  flags ['-i', '-t'] missing=[]
docker logs          help ok=True  flags ['-f', '--tail'] missing=[]
docker ps            help ok=True  flags ['-a'] missing=[]
docker stop          help ok=True  flags ['-t'] missing=[]
docker kill          help ok=True  flags ['-s'] missing=[]
docker rm            help ok=True  flags ['-f', '-v'] missing=[]
docker rmi           help ok=True  flags ['-f'] missing=[]
docker inspect       help ok=True  flags ['--format'] missing=[]
docker cp            help ok=True  flags [] missing=[]
docker stats         help ok=True  flags ['--no-stream'] missing=[]
docker tag           help ok=True  flags [] missing=[]
docker push          help ok=True  flags [] missing=[]
docker build         help ok=True  flags ['-t', '-f', '--target', '--build-arg'] missing=[]
docker history       help ok=True  flags ['--no-trunc'] missing=[]
docker save          help ok=True  flags ['-o'] missing=[]
docker load          help ok=True  flags ['-i'] missing=[]
docker system prune  help ok=True  flags ['-a', '--volumes'] missing=[]
ALL OK

$ docker ps; echo "exit=$?"
exit=1
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory

$ docker build --help | sed -n 1,6p
Usage:  docker buildx build [OPTIONS] PATH | URL | -

Start a build

Aliases:
  docker build, docker builder build, docker image build, docker buildx b
```

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

### Q45 ⭐ 🔴 Design a container strategy for a team of 10 ML engineers: one fat base image or per-project images? Cover a shared base image maintained by the platform team (CUDA, Python, common libraries), per-project layers, a monthly rebuild cadence, version pinning, an upgrade path when the driver or CUDA changes, build and test in CI, a registry layout, and how teams are protected from a bad base update. Give the folder layout and a small compatibility matrix check script.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** I would use one platform-owned base image per supported CUDA and Python combination, with thin per-project images on top, rebuilt monthly through CI, promoted only after tests pass, so teams control their libraries but not their OS and CUDA layer.

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
```text
# ===== layout.txt =====
platform-images/                  # owned by the platform team
  base/
    Dockerfile                    # CUDA runtime + python + pinned common libs
    constraints.txt               # pinned versions shared by everyone
    tests/smoke_test.py           # imports, torch.cuda check on a GPU runner
  matrix.yaml                     # allowed bases, CUDA/python/torch combos, status
  scripts/check_matrix.py
  .github/workflows/base.yml      # monthly rebuild + test + promote
projects/                         # one repo or folder per team
  fraud/Dockerfile                # FROM .../ml-base:2026.10 (pinned tag, digest in lock)
  fraud/requirements.in + requirements.lock
```

```dockerfile
# ===== base/Dockerfile =====
# syntax=docker/dockerfile:1
# Platform base image. Tag below is an EXAMPLE: check Docker Hub for current nvidia/cuda tags.
ARG CUDA_TAG=12.4.1-runtime-ubuntu22.04
FROM nvidia/cuda:${CUDA_TAG}
ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-pip \
 && rm -rf /var/lib/apt/lists/*
COPY constraints.txt /etc/ml-constraints.txt
ENV PIP_CONSTRAINT=/etc/ml-constraints.txt
LABEL org.example.base.version="2026.10"

# ===== demo/projects/fraud/Dockerfile =====
FROM registry.example.com/platform/ml-base:2026.10
RUN pip install torch==2.9.0
```

```yaml
# ===== matrix.yaml =====
# Compatibility matrix: owned by the platform team. Versions are EXAMPLES, check vendor docs.
fleet_driver_min_cuda: "12.4"        # newest CUDA the oldest driver in the fleet supports
bases:
  "2026.10": {cuda: "12.4", python: "3.12", torch_cuda: "12.4", status: current}
  "2026.09": {cuda: "12.4", python: "3.12", torch_cuda: "12.4", status: previous}
  "2026.04": {cuda: "11.8", python: "3.10", torch_cuda: "11.8", status: deprecated}
  "2026.07": {cuda: "12.6", python: "3.12", torch_cuda: "12.6", status: current}
```

```python
# ===== check_matrix.py =====
"""Q45: check every project's Dockerfile against the platform compatibility matrix.
Run: python3 -I check_matrix.py matrix.yaml demo/projects"""
import glob, os, re, sys
import yaml

def v(s): return tuple(int(x) for x in s.split("."))

def check(matrix, projects_dir):
    fleet = matrix["fleet_driver_min_cuda"]
    problems, rows = [], []
    for path in sorted(glob.glob(os.path.join(projects_dir, "*", "Dockerfile"))):
        proj = os.path.basename(os.path.dirname(path))
        m = re.search(r"^FROM\s+\S*ml-base:(\S+)", open(path).read(), re.M)
        if not m:
            problems.append((proj, "does not start from the platform base image")); continue
        tag = m.group(1); b = matrix["bases"].get(tag)
        if b is None:
            problems.append((proj, f"base tag {tag} not in matrix")); continue
        notes = []
        if b["status"] == "deprecated": notes.append("deprecated base")
        if v(b["cuda"]) > v(fleet): notes.append(f"CUDA {b['cuda']} newer than fleet driver supports ({fleet})")
        if b["cuda"] != b["torch_cuda"]: notes.append("torch wheel CUDA differs from base CUDA")
        rows.append((proj, tag, b["cuda"], b["status"], "; ".join(notes) or "ok"))
        if notes: problems.append((proj, "; ".join(notes)))
    return rows, problems

if __name__ == "__main__":
    matrix = yaml.safe_load(open(sys.argv[1]))
    rows, problems = check(matrix, sys.argv[2])
    print(f"{'project':<8} {'base':<8} {'cuda':<5} {'status':<11} result")
    for r in rows: print(f"{r[0]:<8} {r[1]:<8} {r[2]:<5} {r[3]:<11} {r[4]}")
    for p, why in problems: print("PROBLEM:", p, "->", why)
    sys.exit(1 if problems else 0)
```

**Output (my run):** Python 3.13.17, pyyaml, hadolint 2.15.1. Building the base, pushing it, and GPU smoke tests are **not executed** (no daemon, no GPU, no registry). The matrix values and tags are examples; check current CUDA tags and driver compatibility in NVIDIA docs.
```text
$ python3 -I check_matrix.py matrix.yaml demo/projects; echo "exit=$?"
project  base     cuda  status      result
fraud    2026.10  12.4  current     ok
legacy   2026.04  11.8  deprecated  deprecated base
vision   2026.07  12.6  current     CUDA 12.6 newer than fleet driver supports (12.4)
PROBLEM: legacy -> deprecated base
PROBLEM: vision -> CUDA 12.6 newer than fleet driver supports (12.4)
exit=1

$ hadolint --ignore DL3008 base/Dockerfile; echo "hadolint exit=$?"
hadolint exit=0

$ hadolint demo/projects/fraud/Dockerfile; echo "hadolint exit=$?"
demo/projects/fraud/Dockerfile:2 DL3042 warning: Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`
hadolint exit=1
```

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
