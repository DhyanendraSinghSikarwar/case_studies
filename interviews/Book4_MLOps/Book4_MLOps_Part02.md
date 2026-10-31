# Book 4 — Part 2: Docker for ML (images, layers, multi-stage builds, GPU, Compose and security)

**Topic:** containerising ML work: images and layers, build caching, multi-stage builds, base-image and CUDA choices, the NVIDIA Container Toolkit, size reduction, reproducibility, secrets and security, healthchecks, volumes, networking, Compose, registries and debugging
**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 17, ⭐⭐ 18, ⭐ 10)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git, packaging and testing; Part 3 owns Kubernetes and Helm (only pointers here); Part 7 owns CI/CD design (only cache and lint fragments here); Part 10 owns AWS (ECR and IAM details); Book 2 owns LLM serving internals; Book 3 owns SQL; Book 6 owns product and business.

Evidence limits: the free pages found could not be opened (WebFetch failed with getaddrinfo ENOTFOUND), so every source is a search snippet only (see research_notes/Book4_Part02_sources.md). No page was found that reports exact Docker questions asked by a named company; one PracHub snippet labels a layer-caching question as an eBay applied scientist question, which is unverified. 'Asked at' tags therefore name source types (guides, docs, job postings), not verified company reports. Execution limit: the Docker CLI is installed but there is no Docker daemon in this sandbox (docker info fails), so no image was built or run; Wave B may run hadolint, docker compose config, buildx and --help output, and Python scripts, and must label everything else 'not executed'.

---

### Q1 ⭐⭐⭐ 🟢 Image, container and layer, explained for an ML engineer. A teammate says 'my model changed inside the container but it is gone after restart'. Explain what an image is, what a container adds on top (writable layer), how image layers are shared and read-only, what docker commit does and why you should not use it, and where files written at runtime go. Show the commands you would use to prove it (docker run, docker diff, docker history, docker rm), and mark clearly which were not executed here.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** An image is a read-only stack of layers plus metadata; a container is that image plus one thin writable layer and a running process, and when the container is removed the writable layer goes with it.

**Then explain:**
- **Image = recipe result.** Ordered, read-only layers (each is a tar of file changes, named by a content hash) plus config (CMD, ENV, user). Layers are shared: ten containers of one image store the image layers once.
- **Container = image + writable layer.** A write goes to a private copy-on-write layer on top. `docker diff` shows it: `A` added, `C` changed, `D` deleted.
- **What survives what.** `docker restart` or `stop` then `start`: the writable layer survives. `docker rm`, `docker run` again, `compose down` then `up`, a new node or a redeploy: new container, new writable layer, your change is gone. So 'gone after restart' usually means a new container was created.
- **`docker commit`** freezes the writable layer into a new image. It works, but there is no Dockerfile record, nobody can review or rebuild it, and it can capture junk and secrets. Use it only to debug. Real fix: change the code or the Dockerfile and rebuild.
- **Where runtime files should go.** Models, outputs and caches that must outlive the container go to a volume or bind mount, or to object storage and a model registry. Anything else written at runtime is throw-away by design.
- **Failure modes:** writing a big model into the writable layer is slow (copy-on-write) and is lost on `rm`; two replicas never see each other's writes; disk fills up on the node because nobody cleans stopped containers.

**Example:** The image has `/app/model.pkl` = v1. Container c1 overwrites it with v2 and writes `/tmp/pred.log`. Container c2 from the same image still reads v1. `docker rm c1`, run again: v1. The toy script below mimics this with layers as dictionaries so you can check each line by hand.

**Code:**
```python
# ---- layers_sim.py ----
"""Toy model of image layers + container writable layer (union view)."""
import hashlib, json

def digest(files):
    return "sha256:" + hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()[:12]

# image = ordered, read-only layers; each layer is {path: content or None (None = whiteout/delete)}
image = [
    {"/app/model.pkl": "v1", "/app/serve.py": "code-v1"},   # layer 1
    {"/app/config.yaml": "threshold=0.5"},                  # layer 2
]
image_ids = [digest(l) for l in image]

def view(layers):
    fs = {}
    for layer in layers:                 # upper layers win
        for p, c in layer.items():
            if c is None: fs.pop(p, None)
            else: fs[p] = c
    return fs

class Container:
    def __init__(self, image):
        self.image = image               # shared, never modified
        self.upper = {}                  # private writable layer
    def write(self, path, content): self.upper[path] = content
    def delete(self, path): self.upper[path] = None
    def fs(self): return view(self.image + [self.upper])
    def diff(self):                      # what `docker diff` reports: A / C / D
        base = view(self.image); out = []
        for p, c in sorted(self.upper.items()):
            if c is None: out.append(f"D {p}")
            elif p in base: out.append(f"C {p}")
            else: out.append(f"A {p}")
        return out

c1, c2 = Container(image), Container(image)
c1.write("/app/model.pkl", "v2-retrained")      # change model inside container 1
c1.write("/tmp/pred.log", "42 rows")
c1.delete("/app/config.yaml")
print("c1 sees model:", c1.fs()["/app/model.pkl"])
print("c2 sees model:", c2.fs()["/app/model.pkl"], "(same image, own writable layer)")
print("docker diff c1:", c1.diff())
print("image layer ids unchanged:", image_ids == [digest(l) for l in image])

# docker rm c1 -> writable layer is thrown away; docker run again -> fresh container
c1 = Container(image)
print("after rm + run again, model:", c1.fs()["/app/model.pkl"])

# docker commit: freezes the upper layer into a NEW layer (new image); no recipe, not reviewable
c3 = Container(image); c3.write("/app/model.pkl", "v2-retrained")
new_image = image + [c3.upper]
print("commit -> layers:", len(image), "->", len(new_image), "| new top layer:", c3.upper)
```

```bash
# ---- commands.sh ----
# NOT EXECUTED here (no Docker daemon). Run on a machine with Docker.
docker run -d --name m1 myorg/model:1.0 sleep 3600
docker exec m1 sh -c 'echo v2 > /app/model.pkl; echo hi > /tmp/x'
docker diff m1            # C /app/model.pkl ; A /tmp/x   (changes in the writable layer)
docker history myorg/model:1.0   # read-only layers, newest first
docker restart m1         # writable layer SURVIVES restart
docker rm -f m1           # writable layer is deleted here
docker run --rm myorg/model:1.0 cat /app/model.pkl   # original again
docker run -v model_vol:/models myorg/model:1.0      # data that must outlive the container
docker commit m1 myorg/model:hotfix   # works, but avoid it
```

**Output (my run):**
Real container commands (`docker run`, `diff`, `history`, `rm`, `commit`) are **not executed**: this sandbox has the Docker CLI but no daemon (`docker info` below shows it). What did run: the Python layer simulation, and a syntax check of the shell script (`bash -n`, silent = OK).

```text
$ python3 -I layers_sim.py
c1 sees model: v2-retrained
c2 sees model: v1 (same image, own writable layer)
docker diff c1: ['D /app/config.yaml', 'C /app/model.pkl', 'A /tmp/pred.log']
image layer ids unchanged: True
after rm + run again, model: v1
commit -> layers: 2 -> 3 | new top layer: {'/app/model.pkl': 'v2-retrained'}

$ docker --version
Docker version 29.9.2, build a82e528

$ docker info 2>&1 | tail -2 | cut -c1-110
Server:
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the da
```

**Follow-ups:**
- *Why are layers shared?* They are addressed by content hash, so identical layers are stored and pulled once.
- *Is a volume part of the image?* No. A volume is storage outside the layer stack, mounted into the container path.
- *Does `docker stop` lose data?* No. The writable layer is removed only by `docker rm` (or `--rm` on exit).

**Common mistakes:**
- Saying 'the container lost the model on restart' when it was really recreated.
- Using `docker commit` as a deployment method.
- Storing models or user uploads in the writable layer.
- Thinking `RUN rm` in a later layer shrinks the image (the earlier layer still holds the bytes).

### Q2 ⭐⭐⭐ 🟡 Layer caching on an ML inference service (an eBay-style question). A Dockerfile does COPY . /app first, then pip install -r requirements.txt, then downloads a 500 MB model, and every one-line code change triggers a 12 minute rebuild. Explain how the build cache decides to reuse a layer, rewrite the Dockerfile so a code change rebuilds in seconds, and say what still busts the cache (a changed requirements.txt, a timestamp or git-hash ARG placed early, apt-get update on its own line). Include a small Python script that simulates cache keys by hashing instruction plus file contents so you can show which layers rebuild.
**Asked at:** PracHub write-up 'Docker optimization, container fundamentals, and CI/CD for an ML model service' (listed on the site as an eBay applied scientist question; search snippet only, not opened, not independently verified) and a ResumeLens article on containerizing ML models; editorial, not a verified candidate report; ML engineer and MLOps rounds at product companies
**Say this first (1 line):** Docker reuses a layer only if the parent layer and the instruction (and for COPY, the file contents) are identical, so put what changes rarely first, copy only requirements.txt before pip install, and copy your code last.

**Then explain:**
- **How a hit is decided.** Same parent layer, same instruction text. For `COPY` and `ADD` the build also compares a checksum of the copied files (contents, not timestamps). For `RUN` it compares only the command string, not what the command would fetch today.
- **A miss breaks the chain.** Once one layer is rebuilt, every layer after it is rebuilt. That is why `COPY . /app` first is expensive: any file change (a notebook, a log, `.git`) busts pip install and the model download.
- **Fix:** `COPY requirements.txt` then `pip install`, then the heavy model step, then `COPY serve.py`. A code edit now rebuilds only the last COPY. Better still, do not bake a 500 MB model in the image; pull it at start or mount it (see Q7). Add a `.dockerignore`.
- **What still busts the cache:** a changed `requirements.txt`; an `ARG` such as `GIT_SHA` or `BUILD_DATE` that is *used* early (miss at first use, then everything after); `RUN date` or anything non-deterministic; changing the base tag or digest.
- **Stale-cache trap:** `RUN apt-get update` on its own line is cached for ever, so a later `apt-get install` uses an old package index and can 404. Keep `apt-get update && apt-get install ...` in one `RUN`. Same trap for `RUN git clone` or `curl` with no version: cached, so you never see the new data.
- **CI:** a fresh runner has an empty cache. Use a registry or CI cache export (`--cache-from` / `--cache-to`; check current docs for your CI).

**Example:** Bad file, change one line of `serve.py`: COPY . /app is a miss, so pip install (about 10 minutes) and the model download rebuild too. Good file: six layers cached, two rebuild (the COPY and the CMD line). Edit `requirements.txt` in the good file: pip and everything after it rebuilds, which is correct.

**Code:**
```dockerfile
# ---- Dockerfile.bad ----
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "print('download 500 MB model here')"
CMD ["python", "serve.py"]

# ---- Dockerfile.good ----
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY download_model.py .
RUN python download_model.py
COPY serve.py .
CMD ["python", "serve.py"]
```

```python
# ---- cache_sim.py ----
"""Simulate the build cache: key = hash(parent key + instruction text + hash of copied files)."""
import hashlib, re

def h(*parts):
    m = hashlib.sha256()
    for p in parts: m.update(p.encode()); m.update(b"\0")
    return m.hexdigest()[:8]

def build(dockerfile, files, cache):
    parent, report = "", []
    for line in dockerfile.strip().splitlines():
        line = line.strip()
        if not line: continue
        content = ""
        m = re.match(r"COPY\s+(.+)\s+\S+$", line)
        if m:                              # COPY: key includes the content of copied files
            srcs = m.group(1).split()
            names = sorted(files) if srcs == ["."] else srcs
            content = "".join(f"{n}={files[n]}" for n in names)
        key = h(parent, line, content)
        hit = key in cache
        cache.add(key)
        report.append(("CACHED" if hit else "REBUILD", line))
        parent = key                       # a miss changes every later key
    return report

def show(title, rep):
    print(title)
    for s, l in rep: print(f"  {s:8} {l}")

BAD = open("Dockerfile.bad").read()
GOOD = open("Dockerfile.good").read()
files = {"requirements.txt": "torch==2.3.0", "serve.py": "v1", "download_model.py": "dl-v1"}

for name, df in [("BAD", BAD), ("GOOD", GOOD)]:
    cache = set()
    print(f"=== {name} ===")
    build(df, files, cache)                               # first build
    files["serve.py"] = "v2"                              # one-line code change
    show("after editing serve.py:", build(df, files, cache))
    files["requirements.txt"] = "torch==2.4.0"            # dependency change
    show("after editing requirements.txt:", build(df, files, cache))
    files.update({"serve.py": "v1", "requirements.txt": "torch==2.3.0"})

# an ARG changes the key only of instructions that USE it (cache miss on first use, then everything after)
ARGDF = """FROM python:3.11-slim
ARG GIT_SHA
RUN echo $GIT_SHA > /app/version
COPY requirements.txt .
RUN pip install -r requirements.txt"""
cache = set()
def build_arg(sha):
    parent, rep = "", []
    for line in ARGDF.splitlines():
        extra = f"GIT_SHA={sha}" if "$GIT_SHA" in line else ""
        content = files["requirements.txt"] if line.startswith("COPY") else ""
        key = h(parent, line, extra, content); hit = key in cache; cache.add(key)
        rep.append(("CACHED" if hit else "REBUILD", line)); parent = key
    return rep
build_arg("abc123")
show("ARG GIT_SHA used early, new commit:", build_arg("def456"))
```

**Output (my run):**
`docker build` is **not executed** (no daemon), so no real timings or layer IDs are claimed. What ran: the cache simulation (a model of the rule, not Docker's real code) and hadolint 2.15.1 on both Dockerfiles. Hadolint only flags style on the bad file (DL3059); it cannot see the cache problem.

```text
$ python3 -I cache_sim.py
=== BAD ===
after editing serve.py:
  CACHED   FROM python:3.11-slim
  CACHED   WORKDIR /app
  REBUILD  COPY . /app
  REBUILD  RUN pip install --no-cache-dir -r requirements.txt
  REBUILD  RUN python -c "print('download 500 MB model here')"
  REBUILD  CMD ["python", "serve.py"]
after editing requirements.txt:
  CACHED   FROM python:3.11-slim
  CACHED   WORKDIR /app
  REBUILD  COPY . /app
  REBUILD  RUN pip install --no-cache-dir -r requirements.txt
  REBUILD  RUN python -c "print('download 500 MB model here')"
  REBUILD  CMD ["python", "serve.py"]
=== GOOD ===
after editing serve.py:
  CACHED   FROM python:3.11-slim
  CACHED   WORKDIR /app
  CACHED   COPY requirements.txt .
  CACHED   RUN pip install --no-cache-dir -r requirements.txt
  CACHED   COPY download_model.py .
  CACHED   RUN python download_model.py
  REBUILD  COPY serve.py .
  REBUILD  CMD ["python", "serve.py"]
after editing requirements.txt:
  CACHED   FROM python:3.11-slim
  CACHED   WORKDIR /app
  REBUILD  COPY requirements.txt .
  REBUILD  RUN pip install --no-cache-dir -r requirements.txt
  REBUILD  COPY download_model.py .
  REBUILD  RUN python download_model.py
  REBUILD  COPY serve.py .
  REBUILD  CMD ["python", "serve.py"]
ARG GIT_SHA used early, new commit:
  CACHED   FROM python:3.11-slim
  CACHED   ARG GIT_SHA
  REBUILD  RUN echo $GIT_SHA > /app/version
  REBUILD  COPY requirements.txt .
  REBUILD  RUN pip install -r requirements.txt

$ hadolint Dockerfile.bad; echo "hadolint exit code: $?"
Dockerfile.bad:5 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
hadolint exit code: 1

$ hadolint Dockerfile.good; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *BuildKit cache mounts?* `RUN --mount=type=cache,target=/root/.cache/pip` keeps the pip download cache between builds on one builder; it does not travel to a fresh CI runner by default.
- *Does touching a file bust COPY?* Contents decide, not mtime, so `touch` alone does not.
- *Why not copy requirements and the model in one go?* Different change rates; keep them in different layers.

**Common mistakes:**
- `COPY . .` before dependency install.
- Running `apt-get update` and `install` in different RUN lines.
- Putting `ARG BUILD_DATE` or the git hash at the top.
- Believing the cache is global; it is per builder and per machine unless exported.

### Q3 ⭐⭐⭐ 🟡 Multi-stage builds for an ML service. Write a Dockerfile with a builder stage (compilers, build headers, wheels built or a virtualenv created) and a final runtime stage that copies only the virtualenv and the app. Explain what is left behind, how COPY --from works, how to target one stage with --target for tests, and what breaks if the runtime stage lacks a shared library the wheels need. Lint the Dockerfile with hadolint if it can be installed.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Use one stage with compilers to build a virtualenv or wheels, then start a fresh slim stage and COPY --from only the virtualenv and the app, so build tools never reach the final image.

**Then explain:**
- **What is left behind:** compilers, headers, apt lists, pip caches, source tarballs. Only the files you copy cross the stage boundary. Each `FROM` starts a clean filesystem.
- **`COPY --from=builder /opt/venv /opt/venv`** copies files from the named stage (or an image, or a stage number). The venv must sit at the **same path** in the runtime stage, because venv scripts hold absolute paths.
- **`--target`:** `docker build --target test .` builds up to the `test` stage and stops. CI runs tests on that stage; production builds the last stage. BuildKit skips stages the target does not need.
- **Failure mode, missing shared library:** a wheel built or linked against `libgomp1` (OpenMP) imports fine in the builder but fails in a runtime that lacks it: `ImportError: libgomp.so.1: cannot open shared object file`. Fix: install the *runtime* package (not the `-dev` one) in the final stage. Find missing libs with `ldd` on the `.so` files in site-packages.
- **Other traps:** different Python minor version or OS release between stages (compiled extensions break); copying the venv but forgetting `ENV PATH`; running tests in the final stage so test tools ship.

**Example:** In the file below, `build-essential` exists only in `builder`. The stage check script prints it as left behind, and `libgomp1` as kept because the runtime needs it. A wheel with a C extension that needs OpenMP imports fine in `builder` but not in `runtime` if you drop that one line.

**Code:**
```dockerfile
# ---- Dockerfile ----
# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm AS builder
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libgomp1 \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM builder AS test
COPY tests/ /app/tests/
COPY src/ /app/src/
RUN pip install --no-cache-dir pytest==8.3.3 && python -m pytest -q tests

FROM python:3.11-slim-bookworm AS runtime
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --create-home app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY --chown=app:app src/ /app/src/
USER 10001
CMD ["python", "-m", "src.serve"]
```

```python
# ---- stage_check.py ----
"""Parse a multi-stage Dockerfile: stages, COPY --from targets, apt packages per stage."""
import re, sys
text = open(sys.argv[1]).read().replace("\\\n", " ")
stages, cur = {}, None
for line in text.splitlines():
    line = line.strip()
    m = re.match(r"FROM\s+(\S+)(?:\s+AS\s+(\S+))?", line, re.I)
    if m:
        cur = m.group(2) or str(len(stages)); stages[cur] = {"base": m.group(1), "apt": [], "from": []}
        continue
    if cur is None: continue
    m = re.search(r"COPY\s+--from=(\S+)", line)
    if m: stages[cur]["from"].append(m.group(1))
    m = re.search(r"apt-get install\s+(.*?)(?:&&|$)", line)
    if m: stages[cur]["apt"] += [w for w in m.group(1).split() if not w.startswith("-")]
for name, s in stages.items():
    print(f"stage {name:8} base={s['base']:26} apt={s['apt']} copy_from={s['from']}")
ok = True
for name, s in stages.items():
    for src in s["from"]:
        if src not in stages: print("ERROR: unknown stage", src); ok = False
final = list(stages)[-1]
left = set(stages["builder"]["apt"]) - set(stages[final]["apt"])
print("final stage:", final)
print("left behind (apt in builder, not in final):", sorted(left))
print("runtime libs kept:", sorted(set(stages["builder"]["apt"]) & set(stages[final]["apt"])))
print("COPY --from references valid:", ok)
```

**Output (my run):**
`docker build`, `--target` and the import failure are **not executed** (no daemon). What ran: a small stage parser (checks every `COPY --from` points at a real stage and lists what apt installs per stage) and hadolint 2.15.1 (clean; two DL3008 apt-pin warnings are silenced with comments because pinning Debian package versions breaks when the mirror moves).

```text
$ python3 -I stage_check.py Dockerfile
stage builder  base=python:3.11-slim-bookworm  apt=['build-essential', 'libgomp1'] copy_from=[]
stage test     base=builder                    apt=[] copy_from=[]
stage runtime  base=python:3.11-slim-bookworm  apt=['libgomp1'] copy_from=['builder']
final stage: runtime
left behind (apt in builder, not in final): ['build-essential']
runtime libs kept: ['libgomp1']
COPY --from references valid: True

$ hadolint Dockerfile; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *Why not just `pip install` then `apt-get purge` in one stage?* Possible in one RUN, but it is easy to leave residue; multi-stage is simpler to reason about.
- *Wheels instead of a venv?* `pip wheel -w /wheels` in the builder, then `pip install --no-index --find-links=/wheels` in the runtime. Same idea.
- *Does multi-stage make builds faster?* Not by itself; it makes the final image smaller. Cache rules from Q2 still apply.

**Common mistakes:**
- Venv in a different path in the final stage.
- Different base tags in the two stages.
- Installing `-dev` packages in the runtime stage.
- Putting pytest in the stage you ship.

### Q4 ⭐⭐⭐ 🟡 Choosing a base image for a Python ML service: python:3.x, python:3.x-slim, alpine, distroless and ubuntu. Explain glibc versus musl and why numpy, scipy, torch and many manylinux wheels are painful or slow on alpine, what slim leaves out (compilers, some libs), when distroless is worth it and how you debug it, and how you pick a tag (pin the minor version and OS release). Give your default choice for a scikit-learn model API and for a PyTorch service and the reasons.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** My default is python:3.x-slim on a pinned Debian release for both a scikit-learn API and a PyTorch service; alpine is a trap for numeric Python, and distroless is for later hardening when you have a debug plan.

**Then explain:**
- **glibc versus musl.** Debian and Ubuntu use glibc. Alpine uses musl. Most prebuilt binary wheels (numpy, scipy, many ML libs) are tagged `manylinux` (glibc). pip on alpine looks for `musllinux` wheels; if none exist it compiles from source: slow builds, needs compilers, sometimes fails. Some libs also behave differently on musl.
- **slim** is Debian without compilers and many extra libs. Small and fine when wheels exist. If a package must compile, use a builder stage (Q3). You may need `libgomp1` for OpenMP.
- **full python image** includes compilers and tools: big; fine for a builder stage, not for runtime.
- **distroless** has no shell and no package manager: smaller attack surface, harder to debug. Debug with a debug variant, an ephemeral debug container, or `docker cp`. Worth it once the service is stable and you have a scanning and debug story. Python distroless needs care with the venv and the interpreter path.
- **ubuntu:** familiar and good when you need system packages or CUDA (Q5). Heavier than slim.
- **Tag choice:** pin minor version and OS release, such as `python:3.11-slim-bookworm`. Avoid `latest` and bare `3`, which change under you. For strict reproducibility add the digest (Q8). Check current docs for supported Python versions and OS releases.
- **My defaults:** sklearn API: `python:3.11-slim-bookworm`, install pinned wheels, run as non-root. PyTorch service: same base, with the right torch wheel (CPU-only index for CPU serving; for GPU see Q5).

**Example:** The script below asks pip's own tag logic which platform tags this box accepts (glibc, so `manylinux`) and what an alpine box (`musllinux_1_2`) would accept. A wheel named `...manylinux2014_x86_64.whl` is accepted by the first and rejected by the second. So pip on alpine falls back to the source package.

**Code:**
```python
# ---- wheel_tags.py ----
"""Which wheel tags would pip accept on this machine? glibc -> manylinux, musl -> musllinux."""
import platform
from packaging import tags
libc = platform.libc_ver()
print("libc:", libc)
accepted = [str(t) for t in tags.sys_tags() if t.interpreter == "cp313" and t.abi == "cp313"]
plats = sorted({a.split("-")[-1] for a in accepted})
print("cp313 platform tags accepted here (first 6):", plats[:6])
many = [p for p in plats if p.startswith("manylinux")]
musl = [p for p in plats if p.startswith("musllinux")]
print("manylinux tags:", len(many) > 0, "| musllinux tags:", len(musl) > 0)

# what an alpine (musl) box would accept, built explicitly
alp = [str(t) for t in tags.cpython_tags(python_version=(3, 11), platforms=["musllinux_1_2_x86_64"])]
print("alpine example:", alp[0], "-> a wheel tagged manylinux2014_x86_64 would NOT match")
fake = "examplepkg-1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
from packaging.utils import parse_wheel_filename
_, _, _, wtags = parse_wheel_filename(fake)
print("manylinux wheel (examplepkg) installable on alpine:", any(t in set(tags.cpython_tags(python_version=(3, 11), platforms=["musllinux_1_2_x86_64"])) for t in wtags))
mly = set(tags.cpython_tags(python_version=(3, 11), platforms=["manylinux_2_28_x86_64", "manylinux_2_17_x86_64", "manylinux2014_x86_64"]))
print("same wheel installable on a glibc distro (emulated tags):", any(t in mly for t in wtags))
```

```dockerfile
# ---- Dockerfile.sklearn ----
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY model.joblib .
RUN useradd --uid 10001 app
USER 10001
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

# ---- Dockerfile.torch ----
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
# CPU-only wheel index; for GPU use the CUDA wheel index that matches your driver (check current PyTorch docs)
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.3.1 \
    && pip install --no-cache-dir -r requirements.txt
COPY src/ src/
RUN useradd --uid 10001 app
USER 10001
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Output (my run):**
Image builds and size comparisons are **not executed** (no daemon) and no sizes are claimed. What ran: the wheel-tag check (uses the `packaging` library on this glibc host; the alpine side is emulated by asking for `musllinux` tags explicitly, not a real alpine run) and hadolint on both Dockerfiles. The torch version in the Dockerfile is an example; check current PyTorch docs.

```text
$ python3 -I wheel_tags.py
libc: ('glibc', '2.39')
cp313 platform tags accepted here (first 6): ['linux_x86_64', 'manylinux1_x86_64', 'manylinux2010_x86_64', 'manylinux2014_x86_64', 'manylinux_2_10_x86_64', 'manylinux_2_11_x86_64']
manylinux tags: True | musllinux tags: False
alpine example: cp311-cp311-musllinux_1_2_x86_64 -> a wheel tagged manylinux2014_x86_64 would NOT match
manylinux wheel (examplepkg) installable on alpine: False
same wheel installable on a glibc distro (emulated tags): True

$ hadolint Dockerfile.sklearn; echo "hadolint exit code: $?"
hadolint exit code: 0

$ hadolint Dockerfile.torch; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *Is alpine ever right?* For small Go or static binaries, or a tiny non-numeric Python service. Not for numpy, scipy, torch.
- *Why pin the OS release?* A new Debian release changes glibc and system libs under a floating `slim` tag.
- *Scratch image for Python?* No. Python needs an interpreter and libs; scratch is for static binaries.

**Common mistakes:**
- Picking alpine for size, then waiting for numpy to compile.
- Using `python:3` or `latest` in production.
- Shipping the full compiler image as the runtime.
- Moving to distroless with no way to debug.

### Q5 ⭐⭐⭐ 🟡 CUDA images for deep learning. Explain the nvidia/cuda tag flavours (base, runtime, devel) and when you need each, why a PyTorch pip wheel already ships its own CUDA libraries so you often do not need a devel image, how to pick between nvidia/cuda, pytorch/pytorch and a plain python-slim image with the right wheel index, and how image size changes between them. Show a Dockerfile for a GPU inference service and say what cannot be tested without a GPU.
**Asked at:** NVIDIA Container Toolkit user guide and runtime docs (docs.nvidia.com, several versions), E2E Networks GPU-in-Docker guide, HowToGeek and LinuxConfig tutorials (search snippets only, not opened); vendor docs and tutorials, not interview reports; GPU and deep-learning MLOps roles (Bengaluru postings mention GPU/CUDA workloads on Kubernetes)
**Say this first (1 line):** nvidia/cuda has three flavours (base, runtime, devel); for a PyTorch pip wheel you usually do not need any of them, because the wheel brings its own CUDA libraries and a python-slim image plus the host driver is enough.

**Then explain:**
- **Flavours.** `base`: minimal CUDA runtime pieces. `runtime`: base plus the CUDA libraries (and cuDNN in the `cudnn-runtime` tags). `devel`: runtime plus compilers and headers (nvcc). Need `devel` only to compile CUDA code: custom ops, flash-attention style builds. Check Docker Hub for the tags that exist today.
- **Pip wheel carries CUDA.** The Linux PyTorch wheels ship the CUDA user-space libraries they need (check the current PyTorch install page for the index URL and CUDA tag). So the image only needs Python, the wheel, and a host with an NVIDIA driver and the NVIDIA Container Toolkit. The driver is never in the image (Q6).
- **Picking:** (1) python-slim plus the right wheel index: simplest, you control Python, usually the choice for pure inference. (2) `pytorch/pytorch` images: convenient, bundles tested versions, but bigger and you inherit its Python and OS. (3) `nvidia/cuda` runtime plus pip: when you need system CUDA libs, TensorRT, or NVIDIA's exact userland. Use a multi-stage with `devel` as builder and `runtime` as final if you must compile.
- **Size.** Roughly: slim plus CUDA wheel is large because the wheel itself is large (GBs); `devel` is the biggest; CPU-only wheel is much smaller. Measure with `docker images` or `docker history` on your build (not done here).
- **Failure modes:** `devel` in production (big, more CVEs); wheel built for a CUDA newer than the host driver supports; forgetting `--gpus` at run time; CPU wheel installed so `is_available()` is False.
- **Cannot test without a GPU:** `torch.cuda.is_available()`, a real forward pass on GPU, nvidia-smi inside the container, memory limits, NCCL. You can still lint, build and import-test on CPU.

**Example:** Inference API, single model, pure PyTorch: Option A below (python-slim plus requirements with torch). Needs a custom CUDA extension compiled at build: multi-stage with `nvidia/cuda:...-devel` as builder and `...-runtime` as final. The tiny check script flags a devel image in the last stage.

**Code:**
```dockerfile
# ---- Dockerfile ----
# Option A: plain python-slim + PyTorch pip wheel (wheel bundles its CUDA user-space libs).
# Host still needs the NVIDIA driver and the NVIDIA Container Toolkit.
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    NVIDIA_VISIBLE_DEVICES=all NVIDIA_DRIVER_CAPABILITIES=compute,utility
WORKDIR /app
COPY requirements.txt .
# The default PyPI torch wheel for Linux is CUDA-enabled; to pin a CUDA flavour use the matching
# --index-url from the PyTorch install page (check current docs for the exact cuXXX tag).
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
RUN useradd --uid 10001 app
USER 10001
EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

# ---- Dockerfile.nvidia-runtime ----
# Option B: NVIDIA runtime image when you need system CUDA libs (e.g. TensorRT, custom ops).
# Tag is an example; check Docker Hub for current nvidia/cuda tags.
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY src/ src/
RUN useradd --uid 10001 app
USER 10001
CMD ["python3", "-m", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# ---- flavour_check.py ----
"""Tiny lint: flag devel images in the last stage and unpinned/latest nvidia tags."""
import re, sys
froms = re.findall(r"^FROM\s+(\S+)", open(sys.argv[1]).read(), re.M)
final = froms[-1]
print("final image:", final)
if "nvidia/cuda" in final:
    flavour = next((f for f in ("devel", "runtime", "base") if f in final), "unknown")
    print("flavour:", flavour)
    if flavour == "devel": print("WARN: devel in the final stage (compilers, headers, big)")
    if final.endswith(":latest") or ":" not in final: print("WARN: unpinned tag")
else:
    print("not an nvidia/cuda image; CUDA libs must come from the wheel")

# ---- gpu_smoke.py ----
"""Run INSIDE the container on a GPU host. Not executable in this sandbox (no GPU, no torch)."""
import torch
print("torch", torch.__version__, "built for CUDA", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device:", torch.cuda.get_device_name(0))
    x = torch.randn(1024, 1024, device="cuda")
    print("matmul ok:", (x @ x).shape)
```

**Output (my run):**
Builds, `docker run --gpus`, `gpu_smoke.py` and anything touching CUDA are **not executed**: no daemon, no GPU, and torch is not installed here (last command shows it). What ran: the flavour lint and hadolint 2.15.1 (Option B gets DL3008, an apt pin warning, left visible on purpose). The `nvidia/cuda` tag is an example; check Docker Hub.

```text
$ python3 -I flavour_check.py Dockerfile
final image: python:3.11-slim-bookworm
not an nvidia/cuda image; CUDA libs must come from the wheel

$ python3 -I flavour_check.py Dockerfile.nvidia-runtime
final image: nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
flavour: runtime

$ hadolint Dockerfile; echo "hadolint exit code: $?"
hadolint exit code: 0

$ hadolint Dockerfile.nvidia-runtime; echo "hadolint exit code: $?"
Dockerfile.nvidia-runtime:5 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
hadolint exit code: 1

$ python3 -I -c 'import torch' 2>&1 | tail -1
ModuleNotFoundError: No module named 'torch'
```

**Follow-ups:**
- *Why not always devel?* Size and attack surface; you do not need nvcc to run inference.
- *Do I need cuDNN in the image?* The PyTorch wheel includes what it needs; only the `nvidia/cuda` route needs a `cudnn` tag.
- *Can the image run on any GPU host?* Only if the host driver supports the CUDA version inside (Q6).

**Common mistakes:**
- Using `devel` as the final image.
- Installing the CPU wheel by mistake and blaming Docker.
- Putting the NVIDIA driver in the image.
- Assuming a CUDA image runs on CPU-only laptops for tests without a CPU fallback path.

### Q6 ⭐⭐⭐ 🔴 How does a container use the host GPU? Explain what the NVIDIA Container Toolkit installs and configures (runtime hook, nvidia-ctk, daemon.json), what docker run --gpus all does, which pieces come from the host (driver, libcuda) and which from the image (CUDA runtime, cuDNN), the rule that the container CUDA version may be older than the driver supports but not newer, and the NVIDIA_VISIBLE_DEVICES and NVIDIA_DRIVER_CAPABILITIES variables. Then debug: 'docker: could not select device driver with capabilities gpu', and nvidia-smi works on host but torch.cuda.is_available() is False in the container. Commands that need a GPU or daemon must be labelled not executed.
**Asked at:** NVIDIA Container Toolkit user guide and runtime docs (docs.nvidia.com, several versions), E2E Networks GPU-in-Docker guide, HowToGeek and LinuxConfig tutorials (search snippets only, not opened); vendor docs and tutorials, not interview reports; GPU and deep-learning MLOps roles (Bengaluru postings mention GPU/CUDA workloads on Kubernetes)
**Say this first (1 line):** The container never has its own GPU driver: the host driver and libcuda are injected into the container at start by the NVIDIA Container Toolkit's runtime hook when you pass --gpus, while the CUDA runtime and cuDNN come from the image.

**Then explain:**
- **Toolkit.** The NVIDIA Container Toolkit (host package) provides the runtime hook and `nvidia-ctk`. `nvidia-ctk runtime configure --runtime=docker` registers the runtime in `/etc/docker/daemon.json`; restart Docker after.
- **`--gpus all`** (or `--gpus 1`, or `device=0`) tells Docker to use that runtime for this container: it mounts the GPU device nodes and the host driver libraries (libcuda, nvidia-smi) in.
- **Who owns what.** Host: kernel driver, libcuda. Image: CUDA runtime, cuDNN, your framework. Rule of thumb: the CUDA version in the container may be *older* than what the driver supports, but not newer. (CUDA also has minor-version and forward-compat rules; check current NVIDIA docs for the exact compatibility table.)
- **Env vars.** `NVIDIA_VISIBLE_DEVICES` picks GPUs (`all`, `0,1`, `none`). `NVIDIA_DRIVER_CAPABILITIES` picks features (`compute,utility` for CUDA and nvidia-smi; `video` for NVENC). NVIDIA's own images preset them; a plain python-slim image does not, so set them or pass `--gpus`.
- **Debug 1: `could not select device driver "" with capabilities: [[gpu]]`.** Docker does not know the nvidia runtime. Toolkit missing, or not configured, or Docker not restarted. Check `docker info | grep -i runtimes`.
- **Debug 2: `nvidia-smi` works on the host, `torch.cuda.is_available()` is False in the container.** In order: container started without `--gpus`; a CPU-only torch wheel; the wheel's CUDA newer than the driver supports; driver capabilities missing; or running under a runtime that hides GPUs (check `NVIDIA_VISIBLE_DEVICES=void`). Run `nvidia-smi` *inside* the container first: if it fails, it is a runtime problem; if it works, it is a Python wheel problem.

**Example:** Four cases in the helper script: (A) runtime not registered, (B) CPU wheel, (C) wheel needs CUDA 12.4 but the driver only supports 11.8, (D) image CUDA 11.8 on a driver that supports up to 12.6, which is fine. The compose GPU reservation is validated with `docker compose config` below.

**Code:**
```bash
# ---- setup_and_debug.sh ----
# NOT EXECUTED here: needs a GPU host with Docker. Order of checks when a GPU container fails.
nvidia-smi                                   # 1. host driver works?
nvidia-ctk --version                         # 2. toolkit installed?
sudo nvidia-ctk runtime configure --runtime=docker   # writes the runtime into /etc/docker/daemon.json
sudo systemctl restart docker                # 3. daemon must restart to pick it up
docker info | grep -i runtimes               # 4. nvidia listed?
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi   # 5. smoke test (tag is an example)
docker run --rm --gpus all myorg/model-gpu:1.0 python -c "import torch;print(torch.cuda.is_available())"
docker exec c env | grep NVIDIA              # 6. NVIDIA_VISIBLE_DEVICES / DRIVER_CAPABILITIES set?
```

```yaml
# ---- compose.yaml ----
services:
  model:
    image: myorg/model-gpu:1.0
    ports: ["8000:8000"]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

```python
# ---- cuda_compat.py ----
"""Decision helper for the two classic GPU-in-container failures. Pure logic, runnable anywhere."""
def diagnose(host_driver_ok, toolkit_installed, daemon_has_nvidia_runtime,
             image_cuda, max_cuda_supported_by_driver, torch_built_for_cuda, torch_is_cpu_wheel):
    out = []
    if not host_driver_ok: out.append("Fix host: nvidia-smi fails; install the driver first.")
    if not toolkit_installed: out.append("Install NVIDIA Container Toolkit on the host.")
    elif not daemon_has_nvidia_runtime:
        out.append("could not select device driver 'gpu': run nvidia-ctk runtime configure, restart docker.")
    if torch_is_cpu_wheel: out.append("torch is a CPU wheel: is_available() is False even with a working GPU.")
    if torch_built_for_cuda and torch_built_for_cuda > max_cuda_supported_by_driver:
        out.append(f"Wheel needs CUDA {torch_built_for_cuda} but driver supports up to {max_cuda_supported_by_driver}: upgrade driver or use older wheel.")
    if image_cuda and image_cuda > max_cuda_supported_by_driver:
        out.append(f"Image CUDA {image_cuda} newer than driver ({max_cuda_supported_by_driver}): too new; use older image.")
    return out or ["No issue found by these rules; check NVIDIA_DRIVER_CAPABILITIES and run with --gpus."]

cases = {
 "A could-not-select-device-driver": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=False, image_cuda=12.4, max_cuda_supported_by_driver=12.6, torch_built_for_cuda=12.4, torch_is_cpu_wheel=False),
 "B smi ok, torch False (cpu wheel)": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=True, image_cuda=None, max_cuda_supported_by_driver=12.6, torch_built_for_cuda=None, torch_is_cpu_wheel=True),
 "C wheel newer than driver": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=True, image_cuda=None, max_cuda_supported_by_driver=11.8, torch_built_for_cuda=12.4, torch_is_cpu_wheel=False),
 "D image older than driver (fine)": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=True, image_cuda=11.8, max_cuda_supported_by_driver=12.6, torch_built_for_cuda=11.8, torch_is_cpu_wheel=False),
}
for name, kw in cases.items():
    print(name); [print("  -", m) for m in diagnose(**kw)]
```

**Output (my run):**
**Not executed:** `nvidia-ctk`, `docker run --gpus`, `nvidia-smi` and any container start (no daemon, no GPU, no driver). What ran: the diagnosis helper (my simplified rules, not an NVIDIA tool) and `docker compose config`, which only validates and normalises the GPU `deploy.resources.reservations.devices` block; it does not prove a GPU will be allocated. `bash -n` on the shell script was silent (OK).

```text
$ python3 -I cuda_compat.py
A could-not-select-device-driver
  - could not select device driver 'gpu': run nvidia-ctk runtime configure, restart docker.
B smi ok, torch False (cpu wheel)
  - torch is a CPU wheel: is_available() is False even with a working GPU.
C wheel newer than driver
  - Wheel needs CUDA 12.4 but driver supports up to 11.8: upgrade driver or use older wheel.
D image older than driver (fine)
  - No issue found by these rules; check NVIDIA_DRIVER_CAPABILITIES and run with --gpus.

$ docker compose -f compose.yaml config | sed -n '1,14p'
name: q06
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
    image: myorg/model-gpu:1.0
    networks:
      default: null
```

**Follow-ups:**
- *How does Kubernetes do this?* The NVIDIA device plugin and a `nvidia.com/gpu` resource; see the Kubernetes part.
- *MIG or sharing a GPU?* Possible with NVIDIA tooling; details depend on hardware, check current docs.
- *Can two containers share one GPU?* Yes by default with `--gpus`, with no memory isolation; one can OOM the other.

**Common mistakes:**
- Installing the driver inside the image.
- Forgetting to restart Docker after `nvidia-ctk runtime configure`.
- Saying 'container CUDA must equal host CUDA'. Host shows the *driver's* max CUDA version in nvidia-smi, not an installed toolkit.
- Debugging Python first when `nvidia-smi` inside the container already fails.

### Q7 ⭐⭐⭐ 🟡 Our model image is 9 GB and takes 15 minutes to pull on every node. Give a prioritised plan to shrink it: slim or runtime base, multi-stage, CPU-only torch wheel when no GPU is needed, pip --no-cache-dir or a cache mount, removing build tools and apt lists in the same RUN, .dockerignore, not baking training data or checkpoints, and splitting a big model into a mounted volume. For each step say what it saves and what risk it adds. Include a Python script that reads a docker history style table and ranks layers by size.
**Asked at:** PracHub write-up 'Docker optimization, container fundamentals, and CI/CD for an ML model service' (listed on the site as an eBay applied scientist question; search snippet only, not opened, not independently verified) and a ResumeLens article on containerizing ML models; editorial, not a verified candidate report; ML engineer and MLOps rounds at product companies
**Say this first (1 line):** First measure which layers are big with docker history, then cut in this order: do not bake models or data in, CPU-only torch if no GPU, slim base and multi-stage, .dockerignore, pip --no-cache-dir; each step trades some risk.

**Then explain:**
- **1. Measure.** Rank layers by size (script below on a pasted `docker history` table). Fix the biggest first.
- **2. Take the model and data out.** Biggest win usually. Mount a volume or pull the model at start from a registry or object store. Saves the model size on every pull. Risk: start-up needs the model source and a download or cache; version the model separately and log which version is loaded.
- **3. CPU-only torch wheel** when serving on CPU. Saves the CUDA libraries (GBs). Risk: the same image will not use a GPU later; keep a GPU tag as a separate build.
- **4. Slim base plus multi-stage** (Q3, Q4). Drops compilers and build files. Risk: a missing runtime lib at import time.
- **5. One `RUN` that installs and cleans** (`apt-get install --no-install-recommends ... && rm -rf /var/lib/apt/lists/*`), `pip --no-cache-dir`, or a cache mount. A later `rm` in a new layer does not shrink anything. Risk: slower rebuilds if you drop caches without a cache mount.
- **6. `.dockerignore`** for `.git`, data, checkpoints, notebooks. Saves context upload time and layer size. Risk: ignoring a file you need; build fails loudly, which is good.
- **7. Remove dev dependencies** (pytest, jupyter) from the runtime requirements. Risk: need a separate dev requirements file.
- **Also:** pull time is about the sum of *new* layers on that node, so stable base layers and a thin app layer make rollouts fast. Registry layer compression and lazy pulling exist; check your registry docs.

**Example:** Sample history table below totals 9.84 GB: pip layer 4.10 GB (41.7%), `COPY . /app` 3.20 GB (32.5%), model download 1.80 GB (18.3%), apt 0.61 GB. Stopping the baked model and adding a `.dockerignore` already removes about 5 GB of the 9.84 GB, before touching pip. (The table is made-up sample data for the script, not a real image.)

**Code:**
```python
# ---- rank_layers.py ----
"""Rank layers of a `docker history` style table by size and suggest what to look at."""
import re, sys
UNITS = {"B": 1, "kB": 1e3, "KB": 1e3, "MB": 1e6, "GB": 1e9}
def parse_size(s):
    m = re.fullmatch(r"([\d.]+)\s*([kKMG]?B)", s)
    return float(m.group(1)) * UNITS[m.group(2)] if m else None

rows = []
for line in open(sys.argv[1]).read().splitlines()[1:]:
    size = None
    parts = re.split(r"\s{2,}", line.strip())
    for p in parts[::-1]:
        if parse_size(p) is not None: size = parse_size(p); break
    if size is None: continue
    created_by = parts[2] if len(parts) > 2 else line
    rows.append((size, created_by))
total = sum(s for s, _ in rows)
print(f"total = {total/1e9:.2f} GB over {len(rows)} sized layers")
for i, (s, c) in enumerate(sorted(rows, reverse=True)[:4], 1):
    print(f"{i}. {s/1e9:5.2f} GB  {100*s/total:4.1f}%  {c[:55]}")
hints = []
for s, c in rows:
    if "COPY . " in c and s > 1e8: hints.append("COPY . is large: add .dockerignore, copy only src")
    if "pip install" in c and s > 1e9: hints.append("pip layer large: CPU-only torch? --no-cache-dir? dev deps?")
    if "get_model" in c or "download" in c: hints.append("model baked in: mount or pull at start")
    if "apt-get" in c and s > 2e8: hints.append("apt layer big: --no-install-recommends, drop build tools")
print("hints:"); [print(" -", h) for h in dict.fromkeys(hints)]
```

```dockerfile
# ---- Dockerfile.slim ----
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-serve.txt .
# CPU-only torch from the CPU wheel index; no pip cache kept in the layer
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.3.1 \
    && pip install --no-cache-dir -r requirements-serve.txt
COPY src/ src/
# model is NOT baked in; mounted at /models or pulled on start
ENV MODEL_PATH=/models/model.pt
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```gitignore
# ---- .dockerignore ----
.git
data/
checkpoints/
*.ckpt
*.pt
notebooks/
__pycache__/
.env
```

**Output (my run):**
Building images, real `docker history` and measuring actual savings are **not executed** (no daemon); the layer table is a hand-written sample and no real size claims are made. What ran: the ranking script on that sample and hadolint on the slim Dockerfile.

```text
$ cat history.txt
IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
a1b2c3d4e5f6   2 hours ago    CMD ["python" "serve.py"]                       0B
<missing>      2 hours ago    COPY . /app # buildkit                          3.2GB
<missing>      2 hours ago    RUN /bin/sh -c python get_model.py # buildkit   1.8GB
<missing>      3 hours ago    RUN /bin/sh -c pip install -r requirements.txt  4.1GB
<missing>      3 hours ago    RUN /bin/sh -c apt-get update && apt-get inst   612MB
<missing>      3 hours ago    WORKDIR /app                                    0B
<missing>      2 weeks ago    /bin/sh -c #(nop)  CMD ["python3"]              0B
<missing>      2 weeks ago    RUN /bin/sh -c set -eux; apt-get update; apt   48.5MB
<missing>      2 weeks ago    /bin/sh -c #(nop) ADD file:abc in /             74.8MB

$ python3 -I rank_layers.py history.txt
total = 9.84 GB over 9 sized layers
1.  4.10 GB  41.7%  RUN /bin/sh -c pip install -r requirements.txt
2.  3.20 GB  32.5%  COPY . /app # buildkit
3.  1.80 GB  18.3%  RUN /bin/sh -c python get_model.py # buildkit
4.  0.61 GB   6.2%  RUN /bin/sh -c apt-get update && apt-get inst
hints:
 - COPY . is large: add .dockerignore, copy only src
 - model baked in: mount or pull at start
 - pip layer large: CPU-only torch? --no-cache-dir? dev deps?
 - apt layer big: --no-install-recommends, drop build tools

$ hadolint Dockerfile.slim; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *Why not just compress or squash?* Squash hides the sharing of layers and hurts pull caching; fix the content instead.
- *Where does the model live then?* A volume, an init step, or object storage; version it and pin the version in config.
- *Distroless or alpine for size?* Last resorts here; the CUDA and torch libs dominate size.

**Common mistakes:**
- Deleting files in a later layer and expecting a smaller image.
- Optimising the base image while a 2 GB checkpoint sits in `COPY . .`.
- Dropping to CPU wheels without testing latency.
- No `.dockerignore`, so `.git` and data are in the build context.

### Q8 ⭐⭐⭐ 🔴 Reproducible Docker builds for ML. Explain why FROM python:3.11 is not reproducible, how to pin a base image by digest (tag plus sha256), why pip install without a lockfile or hashes drifts, how apt-get install pins work and their limits, why timestamps and SOURCE_DATE_EPOCH matter for byte-identical images, and how you would record the image digest, git commit and data version of every trained model. State honestly the difference between reproducible build and repeatable behaviour. Show a Dockerfile, a requirements file with hashes (pip-compile or uv, whichever installs) and a CI check that fails on an unpinned FROM.
**Asked at:** Docker BuildKit references (BuildKit syntax.md, Docker Hub dockerfile frontend page, OneUptime and Opstree BuildKit articles, a 2026 CI cache-invalidation checklist; search snippets only, not opened); documentation and blogs, not interview reports; MLOps and platform engineer rounds
**Say this first (1 line):** FROM python:3.11 is a moving tag, so pin the base by digest, install from a hashed lockfile, and record image digest, git commit and data version with each model; that gives a repeatable build, not automatically repeatable model behaviour.

**Then explain:**
- **Why a tag drifts.** `python:3.11` is re-pushed with new patch versions and OS updates. Same Dockerfile, different image next month. Pin with tag plus digest: `python:3.11-slim-bookworm@sha256:...` (the tag is for humans, the digest is what is used). Cost: you must bump it on purpose; a bot can open the PRs.
- **pip drifts.** `pip install requests` takes whatever is newest, plus unpinned transitive dependencies. Use a lockfile from `uv pip compile --generate-hashes` or `pip-compile --generate-hashes`, install with `--require-hashes`. Hashes also catch a swapped package.
- **apt pins** (`pkg=1.2.3-1`) work only while that version is still in the mirror; old versions disappear, builds then fail. Better: pin the base image digest (system packages inside are frozen) and keep apt installs minimal. Debian snapshot archives exist for strict cases; check current docs.
- **Timestamps.** Layer metadata and file mtimes include build time, so the image digest changes every build. For byte-identical images use `SOURCE_DATE_EPOCH` and BuildKit's reproducible options (check current docs; support depends on version and exporter). Many teams stop at 'same content, different digest' and compare by contents.
- **Lineage record.** Store with each model: image digest (not tag), git commit, data version (a DVC rev or snapshot id), training config, seed. The script below writes it as JSON.
- **Honest difference:** a *reproducible build* gives the same environment. *Repeatable behaviour* also needs the same data, seeds, hardware and non-deterministic ops (GPU kernels, threading). Pinned image does not make training bit-identical.

**Example:** Real run below: `uv pip compile --generate-hashes` produced a `requirements.txt` with 180 hash lines for `requests` and its four dependencies. `pip install --require-hashes --dry-run` accepts it. When I replaced every hash of `certifi` with zeros, pip refused: `THESE PACKAGES DO NOT MATCH THE HASHES`. The CI check fails `Dockerfile.unpinned` (rc 1) and passes the pinned one.

**Code:**
```dockerfile
# ---- Dockerfile ----
# The digest below is a PLACEHOLDER for illustration; get the real one from your registry
# (e.g. `docker buildx imagetools inspect python:3.11-slim-bookworm`) and let a bot bump it.
FROM python:3.11-slim-bookworm@sha256:0000000000000000000000000000000000000000000000000000000000000000
ARG SOURCE_DATE_EPOCH
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt
COPY src/ src/
CMD ["python", "-m", "src.serve"]

# ---- Dockerfile.unpinned ----
FROM python:3.11
RUN pip install requests
```

```python
# ---- check_from.py ----
"""CI gate: fail if any FROM is not pinned by digest (stage aliases and scratch are allowed)."""
import re, sys
bad = 0
for path in sys.argv[1:]:
    text = open(path).read()
    stages = set(re.findall(r"^FROM\s+\S+\s+AS\s+(\S+)", text, re.M | re.I))
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r"FROM\s+(?:--\S+\s+)?(\S+)", line, re.I)
        if not m: continue
        ref = m.group(1)
        if ref == "scratch" or ref in stages: continue
        if not re.search(r"@sha256:[0-9a-f]{64}$", ref):
            print(f"{path}:{n}: FROM {ref} is not pinned by digest"); bad += 1
print("FAIL" if bad else "OK", f"({bad} unpinned)")
sys.exit(1 if bad else 0)

# ---- record_run.py ----
"""Write the lineage record stored next to every trained model (values passed in by CI)."""
import json, sys, hashlib, datetime
def record(image_digest, git_commit, data_version, model_path_bytes):
    return {"image_digest": image_digest, "git_commit": git_commit, "data_version": data_version,
            "model_sha256": hashlib.sha256(model_path_bytes).hexdigest()[:16],
            "note": "repeatable behaviour needs seeds + data version too, not only the image"}
print(json.dumps(record("sha256:" + "ab" * 32, "9f2c1e7", "dvc:rev-2026-10", b"weights"), indent=2))
```

```bash
# ---- hash_demo.sh ----
# run in a temp dir; needs network to PyPI. Tampers every hash of certifi, pip must refuse.
python3 -m venv v
python3 - <<'PY'
s = open("requirements.txt").read()
s = s.replace("a9895e6e2758b371e0545e321a3a8fd1fcfd9829ada8824a936dfb16aaaf36cd", "0"*64)
s = s.replace("e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1", "1"*64)
open("tampered.txt", "w").write(s)
PY
v/bin/pip install --require-hashes --no-deps --dry-run -r requirements.txt | tail -1
v/bin/pip install --require-hashes --no-deps --dry-run -r tampered.txt 2>&1 | grep -E "ERROR|Expected|Got"
```

**Output (my run):**
The Docker build, the digest lookup and `SOURCE_DATE_EPOCH` byte-identical builds are **not executed** (no daemon). The digest in the Dockerfile is a placeholder of zeros, not a real image. What ran: `uv` 0.11.32 to generate the hashed lockfile from PyPI at the time of the run (versions in it are whatever PyPI served then), `pip --require-hashes --dry-run` with a good and a tampered file (`hash_out.txt` is the saved output of `hash_demo.sh`), the FROM-pin CI gate, and hadolint (flags the unpinned pip and pip cache on the bad file).

```text
$ python3 -I check_from.py Dockerfile; echo "exit=$?"
OK (0 unpinned)
exit=0

$ python3 -I check_from.py Dockerfile.unpinned; echo "exit=$?"
Dockerfile.unpinned:1: FROM python:3.11 is not pinned by digest
FAIL (1 unpinned)
exit=1

$ python3 -I record_run.py
{
  "image_digest": "sha256:abababababababababababababababababababababababababababababababab",
  "git_commit": "9f2c1e7",
  "data_version": "dvc:rev-2026-10",
  "model_sha256": "9a129038d9a00aed",
  "note": "repeatable behaviour needs seeds + data version too, not only the image"
}

$ head -6 requirements.txt; grep -c -- '--hash' requirements.txt
# This file was autogenerated by uv via the following command:
#    uv pip compile requirements.in --generate-hashes --python-version 3.11 -o requirements.txt
certifi==2026.10.23 \
    --hash=sha256:a9895e6e2758b371e0545e321a3a8fd1fcfd9829ada8824a936dfb16aaaf36cd \
    --hash=sha256:e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1
    # via requests
180

$ cat hash_out.txt
Would install certifi-2026.10.23 charset-normalizer-3.5.2 idna-3.20 requests-2.34.2 urllib3-2.8.0
ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes
        Expected sha256 0000000000000000000000000000000000000000000000000000000000000000
        Expected     or 1111111111111111111111111111111111111111111111111111111111111111
             Got        e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1

$ hadolint Dockerfile.unpinned; echo "hadolint exit code: $?"
Dockerfile.unpinned:2 DL3013 warning: Pin versions in pip. Instead of `pip install <package>` use `pip install <package>==<version>` or `pip install --requirement <requirements file>`
Dockerfile.unpinned:2 DL3042 warning: Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`
hadolint exit code: 1
```

**Follow-ups:**
- *Does pinning by digest block security patches?* Yes until you bump it; schedule regular bumps and scans.
- *Tag or digest in a deployment manifest?* Digest, so every node runs the same bytes.
- *How do you rebuild a model from 6 months ago?* Image digest from the lineage record, git commit, data version; if the registry pruned the image, rebuild from the pinned Dockerfile and lockfile.

**Common mistakes:**
- Pinning direct dependencies but not transitive ones.
- Pinning the tag only (`python:3.11.9`): tags can still move.
- Claiming 'Docker makes ML reproducible' with unseeded training and unversioned data.
- Using `latest` for the *model* image too.

### Q9 ⭐⭐⭐ 🟡 Secrets in Docker builds and runtime. A Dockerfile has ARG PIP_TOKEN and uses it to install from a private index, and the token shows in docker history. Explain why ARG and ENV leak into image metadata and layers, how RUN --mount=type=secret keeps a secret out of the final image, why a later RUN rm does not help, how runtime secrets should be passed (env at run time, mounted files, a secret manager), and why .env must be in .dockerignore. Show the fixed Dockerfile and a script that scans a Dockerfile for suspicious ARG or ENV names.
**Asked at:** Docker BuildKit references (BuildKit syntax.md, Docker Hub dockerfile frontend page, OneUptime and Opstree BuildKit articles, a 2026 CI cache-invalidation checklist; search snippets only, not opened); documentation and blogs, not interview reports; MLOps and platform engineer rounds
**Say this first (1 line):** ARG and ENV values are stored in the image metadata and in the layers that used them, so anyone with the image can read them from docker history; use RUN --mount=type=secret for build-time secrets and pass runtime secrets at run time, never in the image.

**Then explain:**
- **Why ARG leaks.** `docker history` and `docker inspect` show the build steps and ENV values. A build `ARG` used in a `RUN` is recorded in that step's command text and can end up in the layer or in provenance data. An `ENV` is stored in the image config permanently and every container sees it.
- **Why a later `RUN rm` fails.** Layers are append-only. The file or token was written in an earlier layer; the `rm` layer only hides it. Anyone can read the earlier layer from the image tarball.
- **Build-time fix.** BuildKit secret mounts: `RUN --mount=type=secret,id=pip_token ...` makes the secret available as a file (default `/run/secrets/<id>`) for that one `RUN` only. It is not written into a layer. Supply it with `docker build --secret id=pip_token,env=PIP_TOKEN` or `src=file`. Needs BuildKit, the default in current Docker; check current docs.
- **Runtime secrets.** Pass at run time: environment variables from `--env-file` or the orchestrator, mounted secret files, or fetched from a secret manager (cloud IAM-based) at start. Env vars can still leak via `docker inspect` or crash dumps, so files or a manager are safer. Never bake keys into the image or the repo.
- **`.dockerignore` must list `.env`**, keys and credentials: `COPY . .` would otherwise copy them into a layer.
- **Failure modes:** a secret echoed in build logs; a token in a `pip.conf` copied into the image; secrets in the build context sent to a remote builder; rotating a leaked secret is the only real fix once an image is pushed.

**Example:** `Dockerfile.leaky` has `ARG PIP_TOKEN`, `ENV API_KEY=sk-live-123456` and a `RUN rm`. The scanner finds four problems; the fixed file finds none, and hadolint (DL3064) agrees on the leaky one. The `sk-live` value is a made-up string.

**Code:**
```dockerfile
# ---- Dockerfile.leaky ----
FROM python:3.11-slim-bookworm
ARG PIP_TOKEN
ENV API_KEY=sk-live-123456
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://user:${PIP_TOKEN}@pypi.example.com/simple -r requirements.txt
RUN rm -f ~/.netrc
COPY src/ src/
CMD ["python", "-m", "src.serve"]

# ---- Dockerfile.fixed ----
# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .
# secret exists only for this RUN, mounted at /run/secrets/pip_token, never stored in a layer
RUN --mount=type=secret,id=pip_token \
    PIP_EXTRA_INDEX_URL="https://user:$(cat /run/secrets/pip_token)@pypi.example.com/simple" \
    pip install --no-cache-dir -r requirements.txt
COPY src/ src/
CMD ["python", "-m", "src.serve"]
```

```python
# ---- scan_secrets.py ----
"""Scan a Dockerfile for ARG/ENV names that look like secrets, and secret-looking literal values."""
import re, sys
SUSPECT = re.compile(r"(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY|CREDENTIAL|AWS_SECRET)", re.I)
VALUE = re.compile(r"(sk-[A-Za-z0-9-]{6,}|AKIA[0-9A-Z]{8,}|ghp_[A-Za-z0-9]{10,})")
found = 0
for path in sys.argv[1:]:
    for n, line in enumerate(open(path), 1):
        s = line.strip()
        if re.match(r"(ARG|ENV)\s", s, re.I):
            name = re.split(r"[\s=]", s.split(None, 1)[1])[0]
            if SUSPECT.search(name):
                print(f"{path}:{n}: suspicious {s.split()[0]} name '{name}' (visible in docker history / inspect)"); found += 1
        if VALUE.search(s):
            print(f"{path}:{n}: secret-looking literal value"); found += 1
        if re.search(r"\brm\b.*(netrc|token|\.env|credentials)", s, re.I):
            print(f"{path}:{n}: rm of a secret does not remove it from the earlier layer"); found += 1
print(f"{found} finding(s)")
sys.exit(1 if found else 0)
```

```bash
# ---- build_and_run.sh ----
# NOT EXECUTED here (no daemon).
docker build --secret id=pip_token,env=PIP_TOKEN -t myorg/model:1.0 .     # from an env var
docker build --secret id=pip_token,src=$HOME/.pip_token -t myorg/model:1.0 .   # or from a file
docker history --no-trunc myorg/model:1.0 | grep -i token                 # should print nothing
docker run --rm --env-file runtime.env myorg/model:1.0                   # runtime secret, not baked in
```

**Output (my run):**
`docker build --secret`, `docker history` and `docker run --env-file` are **not executed** (no daemon), so I did not show a real leak in a real history. What ran: the Dockerfile scanner (a simple name and pattern check; it will miss secrets with innocent names) and hadolint 2.15.1 on both files; `bash -n` on the shell script was silent.

```text
$ python3 -I scan_secrets.py Dockerfile.leaky; echo "exit=$?"
Dockerfile.leaky:2: suspicious ARG name 'PIP_TOKEN' (visible in docker history / inspect)
Dockerfile.leaky:3: suspicious ENV name 'API_KEY' (visible in docker history / inspect)
Dockerfile.leaky:3: secret-looking literal value
Dockerfile.leaky:7: rm of a secret does not remove it from the earlier layer
4 finding(s)
exit=1

$ python3 -I scan_secrets.py Dockerfile.fixed; echo "exit=$?"
0 finding(s)
exit=0

$ hadolint Dockerfile.leaky; echo "hadolint exit code: $?"
Dockerfile.leaky:2 DL3064 warning: Potentially sensitive data should not be used in the `ARG` or `ENV` commands
Dockerfile.leaky:3 DL3064 warning: Potentially sensitive data should not be used in the `ARG` or `ENV` commands
Dockerfile.leaky:7 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
hadolint exit code: 1

$ hadolint Dockerfile.fixed; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *Is `ENV` set only for the build safe?* `ARG` is not stored as a runtime env, but it still appears in history; use secret mounts.
- *SSH key for a private git dependency?* `RUN --mount=type=ssh` with `docker build --ssh default`.
- *Already pushed a leaked image?* Rotate the secret first, then delete the image; deleting alone is not enough.

**Common mistakes:**
- `ARG TOKEN` then `RUN rm`.
- `ENV` for API keys.
- Forgetting `.env` in `.dockerignore`.
- Printing the token in a build log, or `pip install -v` with credentials in the URL.

### Q10 ⭐⭐⭐ 🟡 Hardening a model-serving container. List what you change in a Dockerfile and run command to make a container safer: a non-root USER with a fixed UID, minimal base, no secrets in layers, --read-only with tmpfs for scratch, --cap-drop ALL, --security-opt no-new-privileges, pinned base, image scan in CI, no docker.sock mount, and not running with --privileged. Explain what each protects against, one thing that breaks under a read-only filesystem for an ML app (model cache, /tmp, matplotlib or HF cache dirs), and how you fix it.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Run as a non-root user on a minimal pinned image, drop all capabilities, block privilege escalation, make the filesystem read-only with a tmpfs for scratch, keep secrets and the Docker socket out, and scan the image in CI.

**Then explain:**
- **Non-root `USER` (fixed UID, e.g. 10001).** If the app is exploited, the attacker is not root in the container. Fixed UID lets volume permissions and Kubernetes policies match.
- **Minimal pinned base, no secrets in layers** (Q4, Q8, Q9). Fewer packages mean fewer CVEs; pinning stops surprise changes.
- **`--read-only` with `--tmpfs /tmp`.** Attackers cannot drop files or modify code on the root filesystem. Scratch goes to memory-backed tmpfs.
- **`--cap-drop ALL`**, add back only what you need (a model API needs none, binding port 8000 needs none). **`--security-opt no-new-privileges`** stops setuid tricks gaining rights.
- **Never `--privileged`** (nearly full host access) and never mount `/var/run/docker.sock` (whoever has it controls the host Docker).
- **Image scan in CI** (Trivy, Grype or your registry's scanner; check current docs) fails the build on high severity findings. Scanning finds known CVEs only.
- **What breaks under read-only for ML apps:** libraries that write caches on first use: matplotlib config dir, Hugging Face / transformers cache, torch hub, `~/.cache`, pip, joblib temp, `__pycache__`, and `/tmp`. Symptom: `OSError: [Errno 30] Read-only file system`. Fix: point cache env vars at a tmpfs path (`MPLCONFIGDIR`, `HF_HOME`, `XDG_CACHE_HOME`), set `PYTHONDONTWRITEBYTECODE=1`, and mount the model directory read-only from a volume. Size the tmpfs: it counts against memory.
- **Failure modes:** a non-root user cannot bind port 80 (use 8000+); volume owned by root so the app cannot read it; `cap-drop ALL` breaks something needing `NET_BIND_SERVICE`.

**Example:** The compose file sets every control. The audit script reads it back and prints PASS or FAIL per control. I made a bad copy (`read_only: false`, `privileged: true`) and it reports two failures. `docker compose config` normalised the file (it drops `privileged: false` because that is the default).

**Code:**
```dockerfile
# ---- Dockerfile ----
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    HOME=/home/app XDG_CACHE_HOME=/tmp/cache MPLCONFIGDIR=/tmp/mpl \
    HF_HOME=/tmp/hf TRANSFORMERS_CACHE=/tmp/hf
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid 10001 --create-home app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=10001:10001 src/ src/
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# ---- compose.yaml ----
services:
  model:
    image: myorg/model:1.0
    user: "10001:10001"
    read_only: true
    tmpfs:
      - /tmp:size=256m,mode=1777
    cap_drop: [ALL]
    security_opt:
      - no-new-privileges:true
    privileged: false
    ports: ["8000:8000"]
    volumes:
      - model_vol:/models:ro
volumes:
  model_vol: {}
```

```python
# ---- audit_compose.py ----
"""Audit a compose file for hardening settings."""
import sys, yaml
doc = yaml.safe_load(open(sys.argv[1]))
bad = 0
for name, s in doc["services"].items():
    checks = {
      "non-root user": str(s.get("user", "0")).split(":")[0] not in ("0", "root"),
      "read_only rootfs": s.get("read_only") is True,
      "tmpfs scratch": bool(s.get("tmpfs")),
      "cap_drop ALL": "ALL" in (s.get("cap_drop") or []),
      "no-new-privileges": any(str(o).startswith("no-new-privileges") for o in s.get("security_opt", [])),
      "not privileged": not s.get("privileged", False),
      "no docker.sock": not any("docker.sock" in str(v) for v in s.get("volumes", [])),
    }
    for k, ok in checks.items():
        print(f"{name}: {'PASS' if ok else 'FAIL'} {k}"); bad += (not ok)
print("failures:", bad)
sys.exit(1 if bad else 0)
```

```bash
# ---- run_hardened.sh ----
# NOT EXECUTED here (no daemon). Equivalent docker run:
docker run -d --name model --user 10001:10001 --read-only --tmpfs /tmp:rw,size=256m \
  --cap-drop ALL --security-opt no-new-privileges:true \
  -v model_vol:/models:ro -p 8000:8000 myorg/model:1.0
# CI (names are examples; check current docs for your scanner):  trivy image --exit-code 1 --severity HIGH,CRITICAL myorg/model:1.0
# NEVER:  -v /var/run/docker.sock:/var/run/docker.sock   --privileged
```

**Output (my run):**
`docker run` with these flags, the read-only failure itself, and an image scan are **not executed** (no daemon; Trivy and Grype not installed here). What ran: the compose audit (checks only that the settings are present in the file), `docker compose config` (validates and normalises the YAML) and hadolint 2.15.1 (clean).

```text
$ python3 -I audit_compose.py compose.yaml; echo "exit=$?"
model: PASS non-root user
model: PASS read_only rootfs
model: PASS tmpfs scratch
model: PASS cap_drop ALL
model: PASS no-new-privileges
model: PASS not privileged
model: PASS no docker.sock
failures: 0
exit=0

$ sed 's/read_only: true/read_only: false/; s/privileged: false/privileged: true/' compose.yaml > /tmp/c_bad.yaml; python3 -I audit_compose.py /tmp/c_bad.yaml | grep -E 'FAIL|failures'
model: FAIL read_only rootfs
model: FAIL not privileged
failures: 2

$ docker compose -f compose.yaml config | sed -n '1,20p'
name: q10
services:
  model:
    cap_drop:
      - ALL
    image: myorg/model:1.0
    networks:
      default: null
    read_only: true
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=256m,mode=1777
    user: 10001:10001
    volumes:
      - type: volume
        source: model_vol
        target: /models
        read_only: true
        volume: {}

$ hadolint Dockerfile; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *Read-only root but the model needs to download?* Pre-load the model into a mounted volume, or point the cache at tmpfs and accept re-download on restart.
- *What does `no-new-privileges` stop?* A process gaining more privilege through setuid binaries or file capabilities.
- *Rootless Docker or user namespaces?* Extra layers; check current docs.

**Common mistakes:**
- Running as root 'because it works'.
- Mounting `docker.sock` for convenience.
- `--read-only` with no tmpfs, then the app crashes on first request.
- Treating a clean scan as proof of safety.

### Q11 ⭐⭐⭐ 🟡 CMD versus ENTRYPOINT, exec form versus shell form, and PID 1. Explain how they combine, how runtime arguments override CMD and --entrypoint overrides ENTRYPOINT, why the shell form makes sh PID 1 so SIGTERM never reaches uvicorn or gunicorn, how docker stop works (SIGTERM then SIGKILL after a grace period) and how that affects in-flight predictions and checkpoint saving, and when you need tini or --init. Show a Dockerfile and a small Python signal handler test you can run locally without a daemon.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** ENTRYPOINT is the fixed command and CMD is its default arguments; use exec form (JSON array) so your Python process is PID 1 and gets SIGTERM, because shell form makes sh PID 1 and it does not pass the signal on.

**Then explain:**
- **How they combine.** Final command is ENTRYPOINT plus CMD. `docker run image ARGS` replaces CMD only. `docker run --entrypoint X image` replaces ENTRYPOINT (and CMD is then X's arguments, unless you also pass args). If ENTRYPOINT is absent, CMD is the whole command.
- **Exec form** `CMD ["uvicorn", "app:app"]`: runs the program directly, no shell, no variable expansion. **Shell form** `CMD uvicorn app:app`: runs `/bin/sh -c "..."`; sh becomes PID 1 and your server is its child.
- **Signals.** `docker stop` sends SIGTERM to PID 1, waits (default 10 s, `-t` to change), then SIGKILL. PID 1 is special on Linux: a signal with no handler is ignored (no default kill). So sh as PID 1 does not forward SIGTERM and does not die: your app never hears it, then gets killed hard.
- **Effect on ML.** Hard kill means in-flight predictions are dropped (clients see resets), and a training run does not save its checkpoint or flush metrics. Fix: exec form, `exec` in entrypoint scripts, a SIGTERM handler that stops accepting work, drains and saves, and a stop timeout longer than your drain time (`docker stop -t`, `stop_grace_period`, or Kubernetes `terminationGracePeriodSeconds`).
- **tini or `--init`.** A tiny init as PID 1 forwards signals and reaps zombie children. Needed when your app spawns subprocesses (gunicorn workers, dataloader workers that become orphans), or runs a shell script that cannot `exec`. `docker run --init` injects one; or install tini in the image.
- **Uvicorn/gunicorn:** both handle SIGTERM for graceful shutdown when they are PID 1 or are reached by the signal; the failure is almost always shell form or an entrypoint script without `exec`.

**Example:** The test below uses `unshare --pid --fork` (works here as root) so each launcher really is PID 1 of its own PID namespace, then sends SIGTERM from outside, as `docker stop` does. Exec form and an entrypoint that ends in `exec` handled it. `sh -c 'python3 server.py; true'` and an entrypoint without `exec` never delivered it. A Python app with no handler also ignored it, because PID 1 has no default kill action.

**Code:**
```dockerfile
# ---- Dockerfile ----
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY entrypoint_generic.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
# exec form for both. ENTRYPOINT = the fixed part, CMD = default args that `docker run image ARGS` replaces
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
STOPSIGNAL SIGTERM
```

```python
# ---- server.py ----
import signal, sys, time, os
def on_term(signum, frame):
    print(f"[pid {os.getpid()}] got SIGTERM, finishing in-flight work, saving checkpoint", flush=True)
    sys.exit(0)
signal.signal(signal.SIGTERM, on_term)
print(f"[pid {os.getpid()}] server ready", flush=True)
while True: time.sleep(0.1)

# ---- signal_test.py ----
"""Launch each style as PID 1 of a new PID namespace (unshare --pid --fork), send SIGTERM from outside
like `docker stop` does, wait a short grace period, then SIGKILL. Needs root + unshare (works in this sandbox)."""
import subprocess, signal, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
GRACE = 1.5
def run(name, argv):
    p = subprocess.Popen(["unshare", "--pid", "--fork", "--mount-proc"] + argv, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, cwd=HERE, start_new_session=True)
    time.sleep(1.0)
    # unshare --fork makes the command PID 1 in the namespace; signal the namespace's init (child of unshare)
    kids = subprocess.run(["pgrep", "-P", str(p.pid)], capture_output=True, text=True).stdout.split()
    init = int(kids[0]); os.kill(init, signal.SIGTERM)
    deadline = time.time() + GRACE
    while time.time() < deadline and p.poll() is None: time.sleep(0.05)
    if p.poll() is None:
        os.kill(init, signal.SIGKILL); verdict = f"still alive after {GRACE}s grace -> SIGKILL (like docker stop after timeout)"
    else: verdict = f"stopped by SIGTERM, rc={p.returncode}"
    out, _ = p.communicate()
    got = "got SIGTERM" in out
    print(f"--- {name}\n    {verdict}\n    app handler ran: {got}")
run("exec form: CMD [python3, server.py]", ["python3", "server.py"])
run("shell form: sh -c 'python3 server.py; true'", ["sh", "-c", "python3 server.py; true"])
run("entrypoint script WITHOUT exec", ["./entrypoint_noexec.sh", "server.py"])
run("entrypoint script WITH exec", ["./entrypoint.sh", "server.py"])
run("exec form but app has NO SIGTERM handler (PID 1 gets no default action)", ["python3", "server_nohandler.py"])
```

```bash
# ---- entrypoint.sh ----
#!/bin/sh
set -e
echo "entrypoint: warming up"
exec python3 "$@"

# ---- entrypoint_noexec.sh ----
#!/bin/sh
echo "entrypoint: warming up"
python3 "$@"

# ---- entrypoint_generic.sh ----
#!/bin/sh
set -e
echo "entrypoint: starting"
exec "$@"

# ---- docker_cmds.sh ----
# NOT EXECUTED here (no daemon)
docker run myorg/model:1.0                         # entrypoint.sh uvicorn src.api:app ...
docker run myorg/model:1.0 python -m src.train     # CMD replaced, ENTRYPOINT kept
docker run --entrypoint sh -it myorg/model:1.0     # ENTRYPOINT replaced (CMD becomes args to sh)
docker run --init myorg/model:1.0                  # tini as PID 1: forwards signals, reaps zombies
docker stop -t 30 model                            # SIGTERM, wait 30 s, then SIGKILL
```

**Output (my run):**
Real `docker run` and `docker stop` are **not executed** (no daemon). What ran: the signal test with real Linux PID namespaces (`unshare`), which reproduces the PID 1 behaviour but is not Docker itself, so the grace period was shortened to 1.5 s; and hadolint 2.15.1 on the Dockerfile. `tini` is not installed here, so `--init` was not tested. Note: a plain `sh -c 'python3 server.py'` with one command may be optimised by some shells into an exec; I did not rely on that and tested the `; true` form that cannot be.

```text
$ python3 -I signal_test.py
--- exec form: CMD [python3, server.py]
    stopped by SIGTERM, rc=0
    app handler ran: True
--- shell form: sh -c 'python3 server.py; true'
    still alive after 1.5s grace -> SIGKILL (like docker stop after timeout)
    app handler ran: False
--- entrypoint script WITHOUT exec
    still alive after 1.5s grace -> SIGKILL (like docker stop after timeout)
    app handler ran: False
--- entrypoint script WITH exec
    stopped by SIGTERM, rc=0
    app handler ran: True
--- exec form but app has NO SIGTERM handler (PID 1 gets no default action)
    still alive after 1.5s grace -> SIGKILL (like docker stop after timeout)
    app handler ran: False

$ hadolint Dockerfile; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *Where do I trap SIGTERM in FastAPI?* Uvicorn handles it and runs shutdown events; add cleanup in the lifespan handler.
- *Why exec in the entrypoint?* `exec` replaces the shell with your process, so it becomes PID 1.
- *STOPSIGNAL?* Dockerfile instruction to change the stop signal (e.g. SIGINT); default is SIGTERM.

**Common mistakes:**
- Shell-form CMD with a pipe or `&&` chain.
- Entrypoint script that starts the server without `exec`.
- Default 10 s stop timeout with a 60 s checkpoint save.
- Handling SIGTERM in code but forgetting that the signal never arrives.

### Q12 ⭐⭐⭐ 🟡 HEALTHCHECK for a model server. A container is 'running' but the model is still loading for 90 seconds and requests fail. Explain the Dockerfile HEALTHCHECK options (interval, timeout, start-period, retries), the difference between liveness (process alive) and readiness (model loaded and able to predict), a health endpoint that checks the model object, why curl may be missing in a slim image (use python or a tiny script), and how Compose depends_on with condition: service_healthy uses it. Say what Kubernetes probes replace (only a pointer; Kubernetes is a later part). Validate the compose file by script.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Liveness says the process is alive; readiness says the model is loaded and can predict; a Docker HEALTHCHECK should test readiness with a start period longer than model load, and Compose can then wait for it with depends_on condition: service_healthy.

**Then explain:**
- **HEALTHCHECK options.** `--interval` how often to run; `--timeout` when one check counts as failed; `--start-period` grace time at start where failures do not count toward retries; `--retries` consecutive failures before the status becomes `unhealthy`. States: `starting`, `healthy`, `unhealthy`.
- **Liveness versus readiness.** Liveness: should this process be restarted? Readiness: should it get traffic? A model server loading for 90 s is alive but not ready. Docker has one HEALTHCHECK, so choose readiness for it, or run both endpoints and let the orchestrator use each.
- **Good readiness endpoint:** returns 503 until the model object exists, then 200 after a tiny real predict. Do not make it call a slow or expensive path, and do not depend on downstream services, or one outage marks every replica unhealthy.
- **No curl in slim.** Use a tiny `healthcheck.py` with `urllib` (stdlib), or install curl on purpose. Use exec-form `CMD [...]` in HEALTHCHECK.
- **Compose.** `depends_on: model: condition: service_healthy` makes the gateway wait until the model service reports healthy. The model service must define a healthcheck, or Compose errors. It only orders start-up; it does not restart or reroute later.
- **Kubernetes.** Docker HEALTHCHECK is ignored there; use `livenessProbe`, `readinessProbe` and `startupProbe` instead (Kubernetes part). Docker's `unhealthy` status does not restart a container by itself outside Swarm.
- **Failure modes:** `start-period` shorter than load time (container flagged unhealthy while loading); `timeout` too short under load; health check that loads the model again; health passing but predictions broken (add a canary predict).

**Example:** The stub server loads its 'model' for 3 s. Polling every 0.5 s shows `/live` returns 0 from the start while `/ready` returns 1 (fail) until about 3.5 s, then 0. In the real 90 s case set `start_period` above 90 s (the Dockerfile uses 120 s). The validator rejects a compose file where `gateway` waits on a service with no healthcheck.

**Code:**
```dockerfile
# ---- Dockerfile ----
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY healthcheck.py .
RUN useradd --uid 10001 app
USER 10001
EXPOSE 8000
# start-period: failures during the first 120 s do not count toward retries (model loads ~90 s)
HEALTHCHECK --interval=15s --timeout=3s --start-period=120s --retries=3 \
  CMD ["python", "/app/healthcheck.py", "http://127.0.0.1:8000/ready"]
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# ---- compose.yaml ----
services:
  model:
    build: .
    ports: ["8000:8000"]
    healthcheck:
      test: ["CMD", "python", "/app/healthcheck.py", "http://127.0.0.1:8000/ready"]
      interval: 15s
      timeout: 3s
      start_period: 120s
      retries: 3
  gateway:
    image: myorg/gateway:1.0
    depends_on:
      model:
        condition: service_healthy
```

```python
# ---- health_server.py ----
"""Stdlib model server stub: /live = process alive, /ready = model loaded. Load time is configurable."""
import json, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class State: model = None
def load_model(seconds):
    time.sleep(seconds)               # stands in for reading weights
    State.model = lambda x: x * 2     # "model object"

class H(BaseHTTPRequestHandler):
    def _send(self, code, body):
        b = json.dumps(body).encode(); self.send_response(code)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path == "/live": return self._send(200, {"alive": True})
        if self.path == "/ready":
            if State.model is None: return self._send(503, {"ready": False, "reason": "model loading"})
            try: ok = State.model(1) == 2        # real predict on a tiny input, not just 'is not None'
            except Exception as e: return self._send(503, {"ready": False, "reason": str(e)})
            return self._send(200 if ok else 503, {"ready": ok})
        self._send(404, {})
    def log_message(self, *a): pass

def serve(port, load_seconds):
    threading.Thread(target=load_model, args=(load_seconds,), daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", port), H); srv.serve_forever()

if __name__ == "__main__": serve(int(sys.argv[1]), float(sys.argv[2]))

# ---- healthcheck.py ----
"""Used by HEALTHCHECK: exit 0 if /ready returns 200, else 1. No curl needed."""
import sys, urllib.request
url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/ready"
try:
    sys.exit(0 if urllib.request.urlopen(url, timeout=2).status == 200 else 1)
except Exception:
    sys.exit(1)

# ---- timeline_test.py ----
"""Start the stub with a 3 s 'model load' and run healthcheck.py every 0.5 s: shows start-period idea."""
import subprocess, sys, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
srv = subprocess.Popen([sys.executable, "-I", os.path.join(HERE, "health_server.py"), "8765", "3"])
t0 = time.time(); first_ok = None
try:
    while time.time() - t0 < 5:
        live = subprocess.run([sys.executable, "-I", os.path.join(HERE, "healthcheck.py"), "http://127.0.0.1:8765/live"]).returncode
        ready = subprocess.run([sys.executable, "-I", os.path.join(HERE, "healthcheck.py"), "http://127.0.0.1:8765/ready"]).returncode
        t = time.time() - t0
        print(f"t={t:3.1f}s live_rc={live} ready_rc={ready}")
        if ready == 0 and first_ok is None: first_ok = t
        time.sleep(0.5)
finally:
    srv.terminate(); srv.wait()
print("ready first seen at about", round(first_ok, 1), "s (load takes 3 s)")

# ---- validate_compose.py ----
"""Validate: every depends_on with service_healthy points to a service that defines a healthcheck."""
import sys, yaml
doc = yaml.safe_load(open(sys.argv[1])); svcs = doc["services"]; errors = []
for name, s in svcs.items():
    deps = s.get("depends_on", {})
    if isinstance(deps, list): deps = {d: {"condition": "service_started"} for d in deps}
    for dep, cfg in deps.items():
        if dep not in svcs: errors.append(f"{name}: depends_on unknown service {dep}"); continue
        if cfg.get("condition") == "service_healthy" and "healthcheck" not in svcs[dep]:
            errors.append(f"{name}: waits for {dep} to be healthy but {dep} has no healthcheck")
    hc = s.get("healthcheck")
    if hc:
        if "curl" in str(hc.get("test")): errors.append(f"{name}: healthcheck uses curl; slim images often lack it")
        for k in ("interval", "timeout", "start_period", "retries"):
            if k not in hc: errors.append(f"{name}: healthcheck missing {k}")
print("OK" if not errors else "\n".join(errors)); sys.exit(1 if errors else 0)
```

**Output (my run):**
A real container, the `HEALTHCHECK` status transitions and `docker compose up` ordering are **not executed** (no daemon). What ran: the stdlib health server and `healthcheck.py` in a timed loop (a Python simulation of the readiness idea, not Docker's scheduler), the compose validator (my script) on a good and a bad file, `docker compose config` (which normalised `start_period: 120s` to `2m0s`) and hadolint 2.15.1 (clean). The image's `src.api` module is not provided; the stub server stands in for it.

```text
$ python3 -I timeline_test.py
t=0.2s live_rc=0 ready_rc=1
t=0.9s live_rc=0 ready_rc=1
t=1.5s live_rc=0 ready_rc=1
t=2.2s live_rc=0 ready_rc=1
t=2.9s live_rc=0 ready_rc=1
t=3.6s live_rc=0 ready_rc=0
t=4.3s live_rc=0 ready_rc=0
t=4.9s live_rc=0 ready_rc=0
ready first seen at about 3.6 s (load takes 3 s)

$ python3 -I validate_compose.py compose.yaml; echo "exit=$?"
OK
exit=0

$ python3 -c "import yaml;d=yaml.safe_load(open('compose.yaml'));del d['services']['model']['healthcheck'];yaml.safe_dump(d,open('/tmp/c12_bad.yaml','w'))"; python3 -I validate_compose.py /tmp/c12_bad.yaml; echo "exit=$?"
gateway: waits for model to be healthy but model has no healthcheck
exit=1

$ docker compose -f compose.yaml config | sed -n '/healthcheck/,/start_period/p;/depends_on/,/required/p'
    depends_on:
      model:
        condition: service_healthy
        required: true
    healthcheck:
      test:
        - CMD
        - python
        - /app/healthcheck.py
        - http://127.0.0.1:8000/ready
      timeout: 3s
      interval: 15s
      retries: 3
      start_period: 2m0s

$ hadolint Dockerfile; echo "hadolint exit code: $?"
hadolint exit code: 0
```

**Follow-ups:**
- *Why not curl?* Slim images do not ship it; Python stdlib is already there. Alpine/busybox may have wget but see Q4.
- *Health check hits the model on every interval?* Keep it cheap: check the object and one tiny input, or a cached 'last ok' flag.
- *Does Compose restart unhealthy containers?* Not by itself; use `restart` policies with care, or an orchestrator.

**Common mistakes:**
- No start-period, so a slow model load looks like a crash loop.
- A readiness check that only returns 200 from `/`.
- `depends_on` without `condition`, which only waits for the container to *start*.
- Health checks that call the database or other services.

### Q13 ⭐⭐⭐ 🟡 Volumes, bind mounts and tmpfs for ML containers. Where do you put training data, checkpoints, the model registry download cache and logs, and why? Compare named volumes, bind mounts (host path, UID and permission issues, slow on Docker Desktop) and tmpfs, what survives docker rm, the -v versus --mount syntax, how to back up a volume, and the read-only mount for input data. Show a run command that trains with data mounted read-only, checkpoints in a named volume, and a non-root user that can write there.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```dockerfile
FROM python:3.12-slim-bookworm
RUN useradd --uid 10001 --create-home app \
 && mkdir -p /ckpts /data \
 && chown 10001:10001 /ckpts          # a NEW named volume mounted at /ckpts copies this ownership
WORKDIR /app
COPY --chown=10001:10001 train.py .
USER 10001
CMD ["python", "train.py", "--data", "/data", "--out", "/ckpts"]
```
```bash
# NOT EXECUTED here (no Docker daemon). Run on a Docker host.
docker volume create ckpts
docker run --rm --name train \
  --user 10001:10001 \
  --mount type=bind,src=/srv/data/churn,dst=/data,readonly \
  --mount type=volume,src=ckpts,dst=/ckpts \
  --mount type=volume,src=hfcache,dst=/home/app/.cache \
  --tmpfs /tmp:rw,size=512m \
  myorg/trainer:1.4.0

# same thing with the short -v syntax (a missing host path is silently created as root-owned)
docker run --rm -v /srv/data/churn:/data:ro -v ckpts:/ckpts myorg/trainer:1.4.0

# back up the named volume to a tarball in the current directory, then restore it
docker run --rm -v ckpts:/src:ro -v "$PWD":/backup alpine tar czf /backup/ckpts.tgz -C /src .
docker run --rm -v ckpts:/dst -v "$PWD":/backup:ro alpine tar xzf /backup/ckpts.tgz -C /dst
```
```python
# Q13: simulate a named volume: UID permissions, read-only input, tar backup/restore. No Docker needed.
import os, subprocess, tarfile, tempfile, shlex, filecmp
base = tempfile.mkdtemp(prefix="q13_")
data = os.path.join(base, "data"); vol = os.path.join(base, "vol_ckpt")
os.chmod(base, 0o755); os.makedirs(data); os.makedirs(vol)
open(os.path.join(data, "train.csv"), "w").write("x,y\n1,2\n")
os.chmod(data, 0o555); os.chmod(os.path.join(data, "train.csv"), 0o444)   # stand-in for :ro

def try_write(path, uid):
    code = f"import os; os.setgid({uid}); os.setuid({uid}); open({path!r}+'/ckpt_1.pt','w').write('w')"
    r = subprocess.run(["python3", "-I", "-c", code], capture_output=True, text=True)
    return "OK" if r.returncode == 0 else r.stderr.strip().splitlines()[-1]

print("1) vol owned by root, process runs as uid 10001:", try_write(vol, 10001))
os.chown(vol, 10001, 10001)                      # what you do once (image build or init step)
print("2) vol chown 10001, process uid 10001        :", try_write(vol, 10001))
print("3) input dir (read-only), process uid 10001  :", try_write(data, 10001))

arch = os.path.join(base, "backup.tgz")           # volume backup = tar of its contents
with tarfile.open(arch, "w:gz") as t: t.add(vol, arcname=".")
restore = os.path.join(base, "restored"); os.makedirs(restore)
with tarfile.open(arch) as t: t.extractall(restore, filter="data")
print("4) backup files:", sorted(os.listdir(vol)), "restored:", sorted(os.listdir(restore)),
      "same:", filecmp.cmp(os.path.join(vol, "ckpt_1.pt"), os.path.join(restore, "ckpt_1.pt"), shallow=False))

cmd = """docker run --rm --name train --user 10001:10001 --read-only
  --mount type=bind,src=/srv/data/churn,dst=/data,readonly
  --mount type=volume,src=ckpts,dst=/ckpts
  --mount type=volume,src=hfcache,dst=/home/app/.cache
  --tmpfs /tmp:rw,size=512m
  myorg/trainer:1.4.0 python train.py --data /data --out /ckpts"""
a = shlex.split(cmd)
ok = {"read-only input": "readonly" in cmd, "named volume": "type=volume,src=ckpts" in cmd,
      "non-root": a[a.index("--user")+1].split(":")[0] != "0"}
print("5) run-command checks:", ok)
```

**Output (my run):** `docker run` and `docker volume` were **not executed** (no Docker daemon in this sandbox). What did run: `hadolint` on the Dockerfile (clean), `bash -n` on the commands, `docker run --help` to confirm the flags exist, and the simulation. In step 3 the process is not root, so the read-only input dir is simulated with mode 0555. A real `:ro` mount gives `Read-only file system` (EROFS), not EACCES, even for root.
```text
$ hadolint q13_Dockerfile
(no output, exit 0)
$ bash -n q13_run.sh
bash syntax ok
$ docker run --help | grep -E -- '--mount|--tmpfs|--read-only'
      --mount mount                      Attach a filesystem mount to the
      --read-only                        Mount the container's root
      --tmpfs list                       Mount a tmpfs directory
$ python3 -I q13_volumes.py
1) vol owned by root, process runs as uid 10001: PermissionError: [Errno 13] Permission denied: '/tmp/q13_zviyss1_/vol_ckpt/ckpt_1.pt'
2) vol chown 10001, process uid 10001        : OK
3) input dir (read-only), process uid 10001  : PermissionError: [Errno 13] Permission denied: '/tmp/q13_zviyss1_/data/ckpt_1.pt'
4) backup files: ['ckpt_1.pt'] restored: ['ckpt_1.pt'] same: True
5) run-command checks: {'read-only input': True, 'named volume': True, 'non-root': True}
```

**Follow-ups:**
- *Why not just bind mount the checkpoint dir too?* You can on Linux. On Docker Desktop it is slower, and host UID clashes appear. A named volume avoids both.
- *How do you back up a volume?* Run a throwaway container that mounts the volume read-only plus a host dir, and `tar` it (commands above; the tar step is simulated in the script).
- *Can two containers share a volume?* Yes, but Docker does no locking. Two writers to one checkpoint file corrupt it.

**Common mistakes:**
- Running as root "to avoid permission errors", then shipping that.
- Writing checkpoints to a path that is not a volume.
- Mounting the whole repo over `/app` in production, which hides the code baked into the image.
- Putting caches on tmpfs: the model downloads again after every restart and RAM fills.

### Q14 ⭐⭐⭐ 🟡 A docker-compose.yml for a local ML stack: an inference API, an MLflow tracking server, Postgres for its backend store and MinIO for artifacts. Write the file with named volumes, a user-defined network, environment via an env_file, healthchecks and depends_on conditions, and ports published only where needed. Explain how services find each other by name, why localhost inside a container is not the host, and validate the file with docker compose config (works without a daemon) plus a pyyaml check that every depends_on target exists.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```yaml
name: mlstack
services:
  postgres:
    image: postgres:16-bookworm        # pin minor/digest in real use; check current tags
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks: [mlnet]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 3s
      retries: 10
  minio:
    image: minio/minio:latest          # pin a dated release tag in real use
    command: server /data --console-address ":9001"
    env_file: .env
    volumes:
      - miniodata:/data
    networks: [mlnet]
    ports:
      - "127.0.0.1:9001:9001"          # console for humans, bound to loopback only
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]   # assumes curl in the image; check
      interval: 5s
      timeout: 3s
      retries: 10
  mlflow:
    build: ./mlflow                    # small image: mlflow + psycopg2 + boto3
    env_file: .env
    environment:
      MLFLOW_S3_ENDPOINT_URL: http://minio:9000   # service name, not localhost
      MLFLOW_BACKEND_STORE_URI: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      MLFLOW_ARTIFACTS_DESTINATION: s3://mlflow-artifacts   # env names: check current MLflow docs
    command: ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]   # no shell, so no $VAR here
    networks: [mlnet]
    ports:
      - "127.0.0.1:5000:5000"
    depends_on:
      postgres: {condition: service_healthy}
      minio: {condition: service_healthy}
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request as u; u.urlopen('http://localhost:5000/health')"]
      interval: 10s
      timeout: 3s
      start_period: 20s
      retries: 6
  api:
    build: ./api
    env_file: .env
    environment:
      MLFLOW_TRACKING_URI: http://mlflow:5000
    networks: [mlnet]
    ports:
      - "8000:8000"                    # the only service users call
    depends_on:
      mlflow: {condition: service_healthy}
networks:
  mlnet:
    driver: bridge
volumes:
  pgdata:
  miniodata:
```
```dotenv
POSTGRES_USER=mlflow
POSTGRES_PASSWORD=change-me-local-only
POSTGRES_DB=mlflow
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=change-me-local-only
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=change-me-local-only
```
```python
# Q14: pyyaml checks on the compose file: depends_on targets exist, ports, networks, volumes, env_file.
import sys, yaml, os
d = yaml.safe_load(open(sys.argv[1])); base = os.path.dirname(sys.argv[1])
svcs = d["services"]; errs = []
for n, s in svcs.items():
    deps = s.get("depends_on", {}); deps = deps if isinstance(deps, list) else list(deps)
    for t in deps:
        if t not in svcs: errs.append(f"{n}: depends_on unknown service {t}")
    for t, c in (s.get("depends_on", {}) if isinstance(s.get("depends_on"), dict) else {}).items():
        if c.get("condition") == "service_healthy" and "healthcheck" not in svcs.get(t, {}):
            errs.append(f"{n}: waits for {t} healthy but {t} has no healthcheck")
    for net in s.get("networks", []):
        if net not in d.get("networks", {}): errs.append(f"{n}: undefined network {net}")
    for v in s.get("volumes", []):
        src = v.split(":")[0]
        if not src.startswith((".", "/")) and src not in d.get("volumes", {}): errs.append(f"{n}: undefined volume {src}")
    ef = s.get("env_file");
    if ef and not os.path.exists(os.path.join(base, ef)): errs.append(f"{n}: env_file {ef} missing")
    pubs = [p for p in s.get("ports", [])]
    print(f"{n:9} published: {pubs or 'none'}")
print("ERRORS:" if errs else "all checks passed", *errs, sep="\n" if errs else " ")
```

**Output (my run):** `docker compose config` ran for real (it needs no daemon). Starting the stack was **not executed** (no daemon, and images such as `postgres`, `minio` and MLflow were not pulled). The two Dockerfiles in `build:` are one-line stubs only so that `config` can resolve them.
```text
$ docker compose -f q14/docker-compose.yml config > q14_config.out
(exit 0; normalised file, 4 services, 2 volumes, 1 network; env_file values expanded into each service)
$ python3 -I q14_check.py q14/docker-compose.yml
postgres  published: none
minio     published: ['127.0.0.1:9001:9001']
mlflow    published: ['127.0.0.1:5000:5000']
api       published: ['8000:8000']
all checks passed
$ python3 -I q14_check.py q14/bad.yml   # depends_on typo
postgres  published: none
minio     published: ['127.0.0.1:9001:9001']
mlflow    published: ['127.0.0.1:5000:5000']
api       published: ['8000:8000']
ERRORS:
api: depends_on unknown service mlfow
api: waits for mlfow healthy but mlfow has no healthcheck
```

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

### Q15 ⭐⭐⭐ 🟡 Docker networking for a model API. The uvicorn app works with python app.py on the laptop but curl localhost:8000 hangs after docker run -p 8000:8000. Explain bridge, host and none networks, port publishing (-p host:container), why binding to 127.0.0.1 inside the container is the usual bug and 0.0.0.0 the fix, user-defined bridge DNS versus the default bridge, how a container reaches a database on the host (host.docker.internal on Docker Desktop, host-gateway on Linux), and how EXPOSE differs from -p. Show a Python check that parses a Dockerfile and compose file for the common mistakes.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```bash
# NOT EXECUTED (no daemon)
docker network create ml
docker run -d --name api --network ml -p 127.0.0.1:8000:8000 myorg/api:1.0   # app must bind 0.0.0.0
docker run --rm --network ml curlimages/curl http://api:8000/health      # DNS by name works on a user-defined network
docker run --rm --add-host=host.docker.internal:host-gateway myorg/api:1.0   # reach a host service on Linux
```
```python
# Q15: lint a Dockerfile and a compose file for common networking mistakes (regex/pyyaml; not a full parser).
import re, sys, yaml

def check_dockerfile(path):
    out, text = [], open(path).read()
    exposed = {int(p) for m in re.finditer(r"^EXPOSE\s+(.+)$", text, re.M) for p in re.findall(r"\d+", m.group(1))}
    cmd = re.search(r"^(?:CMD|ENTRYPOINT)\s+(.+)$", text, re.M)
    line = cmd.group(1) if cmd else ""
    host = re.search(r"--host[ =\"',]+([0-9.a-z]+)", line)
    port = re.search(r"--port[ =\"',]+(\d+)", line)
    if host and host.group(1) in ("127.0.0.1", "localhost"):
        out.append(f"{path}: server binds {host.group(1)} inside the container; -p will not reach it, use 0.0.0.0")
    if not host and "uvicorn" in line:
        out.append(f"{path}: uvicorn without --host defaults to 127.0.0.1; add --host 0.0.0.0")
    if port and exposed and int(port.group(1)) not in exposed:
        out.append(f"{path}: app listens on {port.group(1)} but EXPOSE says {sorted(exposed)} (EXPOSE is only documentation)")
    return out

def check_compose(path):
    out, d = [], yaml.safe_load(open(path))
    for n, s in d["services"].items():
        for k, v in (s.get("environment") or {}).items():
            if re.search(r"(localhost|127\.0\.0\.1)", str(v)):
                out.append(f"{path}: {n}.{k} points at localhost; inside a container that is the container itself, use the service name")
        if s.get("network_mode") == "host" and s.get("ports"):
            out.append(f"{path}: {n} uses network_mode: host AND ports; ports are ignored with host networking")
        for p in s.get("ports", []):
            if str(p).count(":") == 1 and re.search(r"postgres|mysql|redis|mongo", str(s.get("image", ""))):
                out.append(f"{path}: {n} publishes {p} on all host interfaces; use 127.0.0.1:{p} or drop it")
    return out

findings = check_dockerfile(sys.argv[1]) + check_compose(sys.argv[2])
print("\n".join(findings) or "no findings"); print(f"{len(findings)} finding(s)")

# ---- second script: q15_bind_demo.py ----
# Q15: why 127.0.0.1 inside the container is the bug. Same idea on one machine: connect via the non-loopback address.
import socket, threading
def serve(bind):
    s = socket.socket(); s.bind((bind, 0)); s.listen(1); return s
u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); u.connect(("10.255.255.255", 1))  # no packet sent; picks the outbound interface
non_loop = u.getsockname()[0]; u.close()
for bind in ("127.0.0.1", "0.0.0.0"):
    s = serve(bind); port = s.getsockname()[1]
    # docker-proxy / NAT delivers traffic to the container's eth0 address, not its loopback
    c = socket.socket(); c.settimeout(1)
    try: c.connect((non_loop, port)); r = "connected"
    except OSError as e: r = f"failed ({type(e).__name__})"
    print(f"server bound to {bind:9} -> client via {non_loop}: {r}")
    c.close(); s.close()
```

**Output (my run):** Both scripts ran with `python3 -I`. The sample files `q15/Dockerfile.bad` and `q15/compose.bad.yml` are deliberately wrong. No container was started (**not executed**).
```text
$ python3 -I q15_netcheck.py q15/Dockerfile.bad q15/compose.bad.yml
q15/Dockerfile.bad: server binds 127.0.0.1 inside the container; -p will not reach it, use 0.0.0.0
q15/Dockerfile.bad: app listens on 8001 but EXPOSE says [8000] (EXPOSE is only documentation)
q15/compose.bad.yml: api.DB_URL points at localhost; inside a container that is the container itself, use the service name
q15/compose.bad.yml: api uses network_mode: host AND ports; ports are ignored with host networking
q15/compose.bad.yml: db publishes 5432:5432 on all host interfaces; use 127.0.0.1:5432:5432 or drop it
5 finding(s)
$ python3 -I q15_bind_demo.py
server bound to 127.0.0.1 -> client via 192.0.2.2: failed (ConnectionRefusedError)
server bound to 0.0.0.0   -> client via 192.0.2.2: connected
$ docker run --help | grep -E -- '-p, --publish|--add-host|--network '
      --add-host list                    Add a custom host-to-IP mapping
      --network network                  Connect a container to a network
  -p, --publish list                     Publish a container's port(s) to
```
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

### Q16 ⭐⭐⭐ 🔴 Where do model weights live: baked into the image, mounted as a volume, or downloaded at start? Compare the three for a 2 GB model and for a 30 GB model on image size, pull time, cold start, rollbacks, registry cost, reproducibility (image digest pins the model), air-gapped clusters, and secrets for the model store. Say which you choose for a small sklearn model, a medium transformer and a big LLM, and how a startup download should be made safe (checksum, retries, a readiness gate).
**Asked at:** PracHub write-up 'Docker optimization, container fundamentals, and CI/CD for an ML model service' (listed on the site as an eBay applied scientist question; search snippet only, not opened, not independently verified) and a ResumeLens article on containerizing ML models; editorial, not a verified candidate report; ML engineer and MLOps rounds at product companies
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
```dockerfile
# Variant B: download at start (small image). Weights fetched by entrypoint into a volume.
FROM python:3.12-slim-bookworm
RUN useradd --uid 10001 --create-home app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=10001:10001 app/ ./app/
ENV MODEL_DIR=/models MODEL_URL="" MODEL_SHA256=""
VOLUME ["/models"]
USER 10001
HEALTHCHECK --start-period=300s CMD ["python", "-c", "import urllib.request as u; u.urlopen('http://localhost:8000/ready')"]
ENTRYPOINT ["python", "-m", "app.fetch_then_serve"]
```
```python
# Q16: safe startup download: retries with backoff, sha256 check, atomic rename, readiness gate. Local HTTP server stands in for the model store.
import hashlib, http.server, os, tempfile, threading, time, urllib.request, urllib.error

MODEL = os.urandom(200_000)                       # stand-in "weights"
GOOD = hashlib.sha256(MODEL).hexdigest()
calls = {"n": 0}

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        calls["n"] += 1
        if self.path == "/flaky.bin" and calls["n"] <= 2:      # first two tries fail
            self.send_error(503); return
        body = MODEL[:1000] + b"X" if self.path == "/corrupt.bin" else MODEL
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_port}"

def fetch(url, dest, sha256, tries=4, delay=0.05):
    for i in range(1, tries + 1):
        tmp = dest + ".part"
        try:
            with urllib.request.urlopen(url, timeout=5) as r, open(tmp, "wb") as f: f.write(r.read())
            h = hashlib.sha256(open(tmp, "rb").read()).hexdigest()
            if h != sha256: raise ValueError(f"checksum mismatch {h[:8]} != {sha256[:8]}")
            os.replace(tmp, dest)                  # atomic: readers never see half a file
            return i
        except (urllib.error.URLError, ValueError) as e:
            print(f"  attempt {i}: {e}")
            if os.path.exists(tmp): os.remove(tmp)
            time.sleep(delay * 2 ** i)             # exponential backoff
    raise SystemExit("giving up: container exits non-zero, orchestrator restarts it, NOT ready")

d = tempfile.mkdtemp(); ready = os.path.join(d, "READY")
print("flaky store, good checksum:")
n = fetch(base + "/flaky.bin", os.path.join(d, "model.bin"), GOOD); print(f"  ok after {n} attempt(s)")
open(ready, "w").write(GOOD)                       # readiness gate: /ready handler would check this file or the loaded model
print("ready file present:", os.path.exists(ready), "| leftover .part files:", [f for f in os.listdir(d) if f.endswith('.part')])
print("corrupt file:")
try: fetch(base + "/corrupt.bin", os.path.join(d, "bad.bin"), GOOD, tries=2)
except SystemExit as e: print(" ", e)
print("bad.bin exists:", os.path.exists(os.path.join(d, "bad.bin")))
```
```bash
# NOT EXECUTED (no daemon, no registry)
# Variant A: bake. Model copied before app code so weekly code changes reuse the big layer.
docker build -t myorg/api:1.14.0-m23 -f Dockerfile.baked .
# Variant B: download at start into a cache volume
docker run -v models:/models -e MODEL_URL=https://store.example.com/churn/23/model.bin -e MODEL_SHA256=<sha256> myorg/api:1.14.0
```

**Output (my run):** the script ran with `python3 -I` (real local HTTP server, random weights, so the hash changes each run). `hadolint` ran on the Dockerfile. No image was built (**not executed**).
```text
$ hadolint --no-color q16_Dockerfile
(no findings, exit 0)
$ python3 -I q16_safe_download.py
flaky store, good checksum:
  attempt 1: HTTP Error 503: Service Unavailable
  attempt 2: HTTP Error 503: Service Unavailable
  ok after 3 attempt(s)
ready file present: True | leftover .part files: []
corrupt file:
  attempt 1: checksum mismatch 52948119 != bc53979a
  attempt 2: checksum mismatch 52948119 != bc53979a
  giving up: container exits non-zero, orchestrator restarts it, NOT ready
bad.bin exists: False
```

**Follow-ups:**
- *Why checksum if the URL is HTTPS?* TLS protects transit, not a truncated file, a wrong version, or a changed object.
- *How do you pin a model with download?* Version id in config, sha256 in config, and log both at startup.
- *Why a readiness gate?* So the load balancer sends traffic only after the model is loaded (Q12).

**Common mistakes:**
- `MODEL_URL=.../latest/model.bin`.
- Loading the file while it is still being written.
- Baking a 30 GB model and then wondering why scale-out takes 20 minutes.
- Putting the model-store token in the image.

### Q17 ⭐⭐⭐ 🟢 .dockerignore and the build context. docker build sends the whole directory to the daemon; a repo with data/ (20 GB), .git, models/ and notebooks makes every build slow, and COPY . leaks .env into the image. Explain the build context, what .dockerignore does and its pattern rules (including ! exceptions), why it also helps the cache, and how to check what would be sent without a daemon. Write a .dockerignore for an ML repo and a Python script that lists which files it would exclude (use a simplified matcher and say what it does not cover).
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```gitignore
# VCS and editor
.git
.gitignore
.idea
.vscode
# secrets and local config
.env
.env.*
!.env.example
**/*.pem
# big or generated ML artefacts
data/
models/
checkpoints/
mlruns/
wandb/
**/*.ckpt
**/*.pt
!models/tiny_test.pt
# python junk
**/__pycache__
**/*.pyc
.venv/
.pytest_cache/
# notebooks and docs
**/*.ipynb
docs/
# Dockerfile and .dockerignore are still sent to the builder even if listed; COPY just cannot see them
Dockerfile*
docker-compose*.yml
```
```python
# Q17: simplified .dockerignore matcher. Last matching rule wins; '!' re-includes. Prints what would be sent.
import os, re, sys

def to_regex(pat):
    pat = pat.rstrip("/")
    out, i = "", 0
    while i < len(pat):
        c = pat[i]
        if pat[i:i+3] == "**/": out += "(?:.*/)?"; i += 3
        elif pat[i:i+2] == "**": out += ".*"; i += 2
        elif c == "*": out += "[^/]*"; i += 1
        elif c == "?": out += "[^/]"; i += 1
        else: out += re.escape(c); i += 1
    return re.compile("^" + out + "(?:/.*)?$")      # a match on a directory covers everything under it

def load(path):
    rules = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"): continue
        neg = line.startswith("!"); rules.append((neg, line.lstrip("!"), to_regex(line.lstrip("!").lstrip("/"))))
    return rules

def ignored(rel, rules):
    res, why = False, None
    for neg, raw, rx in rules:
        if rx.match(rel): res, why = (not neg), raw
    return res, why

if __name__ == "__main__":
    root, ig = sys.argv[1], sys.argv[2]
    rules = load(ig); sent, skipped = [], []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), root); size = os.path.getsize(os.path.join(dp, f))
            ign, why = ignored(rel, rules)
            (skipped if ign else sent).append((rel, size, why))
    print("SENT to daemon:");   [print(f"  {r}  ({s} B)") for r, s, _ in sorted(sent)]
    print("EXCLUDED:");         [print(f"  {r}  <- {w}") for r, s, w in sorted(skipped)]
    print(f"context: {sum(s for _,s,_ in sent)} B sent, {sum(s for _,s,_ in skipped)} B kept out")
```

**Output (my run):** the script ran with `python3 -I` on a temporary tree of 100-byte files. The second run shows the gotcha: a bare `*.ipynb` does not match `nb/eda.ipynb`. No `docker build` was run (**not executed**, no daemon).
```text
$ python3 -I q17_ignore.py <tmp-tree> q17.dockerignore
SENT to daemon:
  .env.example  (100 B)
  models/tiny_test.pt  (100 B)
  requirements.txt  (100 B)
  src/app.py  (100 B)
EXCLUDED:
  .env  <- .env
  .git/HEAD  <- .git
  Dockerfile  <- Dockerfile*
  data/raw/big.csv  <- data/
  models/big.pt  <- **/*.pt
  nb/eda.ipynb  <- **/*.ipynb
  notes.pem  <- **/*.pem
  src/__pycache__/app.cpython-312.pyc  <- **/*.pyc
context: 400 B sent, 800 B kept out
$ python3 -I q17_ignore.py <tmp-tree> <file containing only '*.ipynb'>  # filtered to ipynb lines
--- with only '*.ipynb':
  nb/eda.ipynb  (100 B)
```

**Follow-ups:**
- *Is `.gitignore` enough?* No. Docker does not read it. Keep both, and keep them similar.
- *Does `.dockerignore` shrink the image?* Only what `COPY` would have copied. Layers from `RUN` are unaffected.
- *Where do data and weights go instead?* Mounted at run time or fetched at start (Q13, Q16).

**Common mistakes:**
- `*.ipynb` instead of `**/*.ipynb`.
- An exception placed before the rule it should undo.
- Ignoring `requirements.txt` by accident with a broad pattern.
- Believing `.dockerignore` protects secrets that are passed as `ARG`.

### Q18 ⭐⭐ 🟢 Container versus virtual machine, for an ML engineer. Explain namespaces (pid, net, mnt), cgroups (cpu, memory), a shared host kernel, startup time and isolation trade-offs, why a container cannot ship its own kernel or GPU driver, and what that means for a model that needs a specific CUDA driver. Say when a VM or a micro-VM is the better boundary (untrusted code, multi-tenant notebooks).
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```python
# Q18: look at the kernel features containers are built from: namespaces, cgroups, shared kernel. Read-only; no Docker.
import os, platform, subprocess
print("kernel (shared with every container on this host):", platform.release())
print("namespaces of this process:")
for ns in sorted(os.listdir("/proc/self/ns")):
    print(f"  {ns:18} {os.readlink('/proc/self/ns/' + ns)}")
print("cgroup membership:", open("/proc/self/cgroup").read().strip() or "(none)")
for f in ("memory.max", "cpu.max", "pids.max"):
    p = "/sys/fs/cgroup/" + f
    print(f"  {f:11}", open(p).read().strip() if os.path.exists(p) else "not present here")
# a new PID namespace: the child sees itself as PID 1 (needs root or user namespaces)
r = subprocess.run(["unshare", "--pid", "--fork", "--mount-proc", "python3", "-I", "-c", "import os; print('in new pid ns, my pid =', os.getpid())"],
                   capture_output=True, text=True)
print((r.stdout or r.stderr).strip())
print("host pid of this script:", os.getpid())
```

**Output (my run):** real output of this sandbox. It shows cgroup v1 style paths and no `memory.max` file at the v2 location, so the limit lines say "not present here". On a cgroup v2 host those files exist (see Q19). No container ran (**not executed**, no daemon).
```text
$ python3 -I q18_isolation.py
kernel (shared with every container on this host): 6.18.44-fc-v153
namespaces of this process:
  cgroup             cgroup:[4026531835]
  ipc                ipc:[4026531839]
  mnt                mnt:[4026531832]
  net                net:[4026531833]
  pid                pid:[4026531836]
  pid_for_children   pid:[4026531836]
  time               time:[4026531834]
  time_for_children  time:[4026531834]
  user               user:[4026531837]
  uts                uts:[4026531838]
cgroup membership: 9:name=systemd:/
8:pids:/
7:blkio:/
6:freezer:/
5:devices:/
4:memory:/process_api/01a1784e-af58-7445-8b1b-fa61a2ed0e82/claude-code-bash
3:cpuset:/
2:cpuacct:/
1:cpu:/
0::/
  memory.max  not present here
  cpu.max     not present here
  pids.max    not present here
in new pid ns, my pid = 1
host pid of this script: 13078
```

**Follow-ups:**
- *Is a container secure by default?* Reasonably isolated for trusted code, not a security boundary for hostile code.
- *Can I run a Linux image on a Mac?* Docker Desktop runs a small Linux VM and the containers live inside it.
- *Why is a micro-VM useful?* Near-container start with a separate kernel per workload.

**Common mistakes:**
- "A container is a lightweight VM."
- Saying the image contains the NVIDIA driver.
- Forgetting resource limits.
- Running untrusted notebooks in a shared-kernel container with the Docker socket mounted.

### Q19 ⭐⭐ 🟡 Container killed with exit code 137 or a DataLoader crash 'bus error, shared memory'. Explain what exit 137 means (SIGKILL, often the OOM killer), the difference between --memory limits and host memory, how Python and PyTorch memory behave under a cgroup limit, why DataLoader workers need /dev/shm (default 64 MB in Docker; fix with --shm-size or --ipc=host), and how to confirm OOM (docker inspect OOMKilled, dmesg). Show the run flags and a Python script that reads cgroup memory limits from /sys/fs/cgroup if present.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Exit 137 is 128 plus signal 9, SIGKILL, most often the kernel OOM killer after the container hit its memory limit; the "bus error, shared memory" crash is a different cause: the 64 MB default `/dev/shm`, which DataLoader workers use to pass tensors.

**Then explain:**
- **137:** `128 + 9`. Something sent SIGKILL: the OOM killer, `docker kill`, or `docker stop` after the grace period. Confirm with `docker inspect -f '{{.State.OOMKilled}} {{.State.ExitCode}}' <c>` and `dmesg | grep -i 'killed process'` on the host. Caveat: if the kernel kills a child worker, `OOMKilled` can be false while the symptom is the same.
- **Limits:** `--memory 8g` sets the cgroup limit. Without it the container can use the host's RAM. Tools that read `/proc/meminfo` (and `os.cpu_count()` for CPUs) see the **host**, not the limit, so they plan for more than they will get. Read the cgroup files instead. Setting `--memory-swap` equal to `--memory` disables extra swap.
- **Python and PyTorch under a limit:** page cache, pinned memory, many DataLoader workers (each can hold a copy of the data), and big batches all count. Python often does not return freed memory to the OS right away, so RSS looks high.
- **Shared memory:** DataLoader workers send tensors through `/dev/shm`. Docker gives it 64 MB by default. Symptoms: `RuntimeError: DataLoader worker (pid N) is killed by signal: Bus error` and a message about shared memory. Fixes: `--shm-size=2g` (size it to batch and worker count), or `--ipc=host` (shares the host IPC namespace, so weaker isolation). Last resort: `num_workers=0`.
- **Fixes for 137:** lower batch size or workers, stream data, raise the limit, or find the leak.

**Example:** 4 workers, batch 64 images of 3x224x224 floats is about 38 MB per batch in flight per worker, so a handful of prefetched batches overruns 64 MB at once. Hand-check: 64*3*224*224*4 bytes = 38,535,168 bytes. That is why the default 64 MB breaks.

**Code:**
```bash
# NOT EXECUTED (no daemon)
docker run --rm --gpus all --memory 16g --memory-swap 16g --shm-size 2g myorg/trainer:1.4.0
# or: --ipc=host (less isolation)
docker inspect -f '{{{{.State.OOMKilled}}}} {{{{.State.ExitCode}}}}' train
dmesg | grep -i 'killed process'
```
```python
# Q19: read cgroup memory limit/usage (v2 or v1), /dev/shm size, and show why a SIGKILL exit looks like 137.
import os, subprocess, signal, sys

def rd(p):
    try: return open(p).read().strip()
    except OSError: return None

def mem():
    v2 = rd("/sys/fs/cgroup/memory.max")
    if v2 is not None:
        return "cgroup v2", v2, rd("/sys/fs/cgroup/memory.current"), (rd("/sys/fs/cgroup/memory.events") or "").replace("\n", "; ")
    v1 = rd("/sys/fs/cgroup/memory/memory.limit_in_bytes")
    if v1 is not None:
        return "cgroup v1", v1, rd("/sys/fs/cgroup/memory/memory.usage_in_bytes"), None
    return None

m = mem()
if not m: print("no cgroup memory files visible")
else:
    ver, lim, cur, ev = m
    unlimited = lim == "max" or (lim.isdigit() and int(lim) > 1 << 60)
    print(f"{ver}: limit={'UNLIMITED' if unlimited else str(int(lim)//2**20) + ' MiB'}, current={int(cur)//2**20 if cur else '?'} MiB, events={ev}")
st = os.statvfs("/dev/shm"); print(f"/dev/shm size: {st.f_blocks * st.f_frsize // 2**20} MiB (Docker default for a container is 64 MiB)")
print("host-visible RAM from /proc/meminfo (what many libs wrongly trust):", int(open('/proc/meminfo').readline().split()[1])//1024, "MiB")

# exit 137 = 128 + 9: the process was killed by SIGKILL (the OOM killer sends it, so does docker kill)
p = subprocess.Popen([sys.executable, "-I", "-c", "import time; time.sleep(30)"]); p.send_signal(signal.SIGKILL); p.wait()
print("python returncode:", p.returncode, "-> shell/docker would report", 128 + abs(p.returncode))
```

**Output (my run):** the script ran with `python3 -I`. The sandbox shows cgroup v1 with no limit, and `/dev/shm` here is not Docker's 64 MB default, so this run shows the reader working, not an OOM. The exit-code lines come from a real SIGKILL of a child. `docker run` and `docker inspect` were **not executed** (no daemon); `docker run --help` confirms `--memory` and `--shm-size` exist.
```text
$ python3 -I q19_cgroup_mem.py
cgroup v1: limit=UNLIMITED, current=2388 MiB, events=None
/dev/shm size: 16091 MiB (Docker default for a container is 64 MiB)
host-visible RAM from /proc/meminfo (what many libs wrongly trust): 16091 MiB
python returncode: -9 -> shell/docker would report 137
```

**Follow-ups:**
- *Is 137 always OOM?* No. Check `OOMKilled`, `dmesg`, and whether something ran `docker kill` or a stop timed out.
- *Why not always use `--ipc=host`?* It shares IPC with the host and other containers; fine on a private box, poor in multi-tenant setups.
- *Is `--memory` the same as a Kubernetes limit?* Same cgroup idea, set through the pod spec (later part).

**Common mistakes:**
- Raising `num_workers` to speed up and then hitting 137.
- Sizing from `free -m` inside the container.
- Not setting any limit on a shared GPU box.
- Ignoring that page cache and pinned memory count.

### Q20 ⭐⭐ 🟢 Dockerfile instruction details interviewers ask. COPY versus ADD (tar auto-extract, URLs), RUN with && chaining and why a later RUN rm does not shrink an image, apt-get update plus install in one RUN with --no-install-recommends and cleaning /var/lib/apt/lists, WORKDIR versus cd, EXPOSE as documentation only, and LABEL for metadata. Give a before and after Dockerfile and the hadolint rules (DL numbers) that catch each mistake, run if hadolint is installable.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```dockerfile
# ---- Dockerfile.before ----
FROM python:3.12
ADD https://example.com/model.tar.gz /models/
ADD requirements.txt /app/requirements.txt
RUN cd /app
RUN apt-get update
RUN apt-get install -y build-essential libgomp1
RUN pip install -r /app/requirements.txt
COPY . /app
RUN rm -rf /root/.cache
EXPOSE 8000
CMD python /app/serve.py

# ---- Dockerfile.after ----
FROM python:3.12-slim-bookworm
LABEL org.opencontainers.image.title="churn-api" \
      org.opencontainers.image.source="https://example.com/repo"
# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "serve.py"]
```
```bash
pip install hadolint-py     # worked here via the proxy: Haskell Dockerfile Linter 2.15.1
hadolint --no-color Dockerfile.before
hadolint --no-color Dockerfile.after
# docker build / docker history on these were NOT EXECUTED (no daemon)
```

**Output (my run):** hadolint ran for real. The suppression in the "after" file is `# hadolint ignore=DL3008` with the reason in the Follow-ups below. Image building was **not executed**.
```text
$ hadolint --no-color q20/Dockerfile.before
q20/Dockerfile.before:3 DL3020 error: Use COPY instead of ADD for files and folders
q20/Dockerfile.before:4 DL3003 warning: Use WORKDIR to switch to a directory
q20/Dockerfile.before:4 SC2164 warning: Use 'cd ... || exit' or 'cd ... || return' in case cd fails.
q20/Dockerfile.before:5 DL3009 info: Delete the apt lists (/var/lib/apt/lists) after installing something
q20/Dockerfile.before:5 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
q20/Dockerfile.before:6 DL3015 info: Avoid additional packages by specifying `--no-install-recommends`
q20/Dockerfile.before:6 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
q20/Dockerfile.before:6 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
q20/Dockerfile.before:7 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
q20/Dockerfile.before:7 DL3042 warning: Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`
q20/Dockerfile.before:11 DL3025 warning: Use arguments JSON notation for CMD and ENTRYPOINT arguments

# after (with the ignore comment):
(no findings, exit 0)
# after, ignore comment removed:
/tmp/Dockerfile.noignore:4 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
```
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

### Q21 ⭐⭐ 🟢 ARG versus ENV, build time versus run time configuration. Explain scope and visibility of each (ARG gone at runtime but visible in history, ENV persists), how --build-arg and docker run -e or --env-file work, why model paths and thresholds should be runtime config (12-factor), why FROM can use ARG before the first stage, and the ARG-before-FROM scope gotcha in multi-stage builds. Show a small Dockerfile and a script that lists which variables are build-only.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** `ARG` exists only while building and is gone at runtime (but its value can still show in `docker history`); `ENV` is baked into the image and visible to the running process; model paths and thresholds should be runtime config so one image works everywhere.

**Then explain:**
- **ARG:** set with `--build-arg NAME=value`; usable in later build instructions in its stage; not in the container's environment at run time. Never pass secrets this way, they appear in image metadata (Q9).
- **ENV:** persists into the image and the running container. A default can be overridden at run time with `docker run -e NAME=value` or `--env-file file`. `-e NAME` with no value passes the host's current value through.
- **12-factor:** config that changes between environments (model path, threshold, feature flags, URLs) belongs in environment variables at run time, not in the image. One image, many environments, no rebuild to change a threshold.
- **ARG before FROM:** allowed, but only for use in `FROM` lines (for example `FROM python:${PY_VERSION}-slim`). After `FROM`, that value is out of scope. To use it inside the stage, redeclare the name: `ARG PY_VERSION`. Each stage has its own scope too, so declare ARGs again in every stage that needs them.
- **Pattern for build info:** `ARG GIT_SHA` then `LABEL ...revision="${GIT_SHA}"` or `ENV BUILD_SHA=${GIT_SHA}` when the app should report its own version. Remember that this changes the layer on every commit, so place it late (Q2).
- **Failure modes:** an ARG used in a stage where it was not declared silently expands to an empty string; an `ENV` default hides a missing runtime variable; baking a threshold into `ENV` and forgetting it is overridable.

**Example:** In the sample Dockerfile below, `PY_VERSION` is declared globally and used in two `FROM` lines. Only stage 1 redeclares it, so only stage 1 can use it in `RUN`. `GIT_SHA` is build-only, but stage 1 copies its value into `ENV BUILD_SHA`, so the value does survive at runtime that way. `MODEL_PATH` and `THRESHOLD` are runtime ENV with defaults.

**Code:** the Dockerfile, the scope script, and commands that were not executed.
```dockerfile
ARG PY_VERSION=3.12
FROM python:${PY_VERSION}-slim AS builder
ARG PIP_INDEX_URL=https://pypi.org/simple
ARG GIT_SHA=unknown
RUN echo "index is $PIP_INDEX_URL, sha is $GIT_SHA"

FROM python:${PY_VERSION}-slim
ARG GIT_SHA
ENV MODEL_PATH=/models/churn.pkl \
    THRESHOLD=0.5 \
    BUILD_SHA=${GIT_SHA}
LABEL org.opencontainers.image.revision="${GIT_SHA}"
ARG PY_VERSION
RUN echo "python is ${PY_VERSION}"
CMD ["python", "-c", "import os; print(os.environ['MODEL_PATH'], os.environ['THRESHOLD'])"]
```
```bash
# NOT EXECUTED (no daemon)
docker build --build-arg GIT_SHA=$(git rev-parse --short HEAD) -t myorg/api:dev .
docker run --rm -e THRESHOLD=0.7 -e MODEL_PATH=/models/v2.pkl myorg/api:dev
docker run --rm --env-file prod.env myorg/api:dev      # file lines are KEY=VALUE, # comments allowed
```
```python
# Q21: list ARG/ENV scope per stage: which ARGs are build-only, which become runtime ENV, and the ARG-before-FROM gotcha.
import re, sys
text = open(sys.argv[1]).read().replace("\\\n", " ")
global_args, stage, stages = {}, None, []
for ln in text.splitlines():
    ln = ln.strip()
    m = re.match(r"(ARG|ENV|FROM)\s+(.*)", ln, re.I)
    if not m: 
        if stage is not None and re.match(r"RUN|CMD|LABEL", ln): stage["uses"] |= set(re.findall(r"\$\{?(\w+)", ln))
        continue
    k, rest = m.group(1).upper(), m.group(2)
    if k == "ARG" and stage is None:
        n = rest.split("=")[0]; global_args[n] = rest.split("=", 1)[1] if "=" in rest else None
    elif k == "FROM":
        stage = {"from": rest, "args": {}, "env": {}, "uses": set()}; stages.append(stage)
    elif k == "ARG":
        n = rest.split("=")[0]; stage["args"][n] = rest.split("=", 1)[1] if "=" in rest else None
    elif k == "ENV":
        for n, v in re.findall(r"(\w+)=(\S+)", rest): stage["env"][n] = v; stage["uses"] |= set(re.findall(r"\$\{?(\w+)", v))
print("global ARGs (before first FROM):", list(global_args), "-> usable ONLY in FROM lines unless redeclared")
for i, s in enumerate(stages):
    print(f"\nstage {i}: FROM {s['from']}")
    for n in s["args"]:
        in_env = n in s["env"] or any(f"${{{n}}}" in v or f"${n}" in v for v in s["env"].values())
        redeclared = n in global_args
        status = "build-only (gone at runtime)"
        extra = " (redeclared: value inherited from global default)" if redeclared and s["args"][n] is None else ""
        print(f"  ARG {n:14} {status}{extra}; value baked into an ENV: {in_env}")
    for n, v in s["env"].items(): print(f"  ENV {n:14} runtime (visible in docker inspect/ps env): {v}")
    for u in sorted(s["uses"]):
        if u not in s["args"] and u not in s["env"]: print(f"  WARNING: ${u} used but not declared in this stage (empty at build time)")
```

**Output (my run):** the script and hadolint ran. Building and running the image were **not executed** (no daemon). The script is a line-based reader (handles `\` continuations, `KEY=value` ENV only), not a full Dockerfile parser.
```text
$ python3 -I q21_scope.py q21/Dockerfile
global ARGs (before first FROM): ['PY_VERSION'] -> usable ONLY in FROM lines unless redeclared

stage 0: FROM python:${PY_VERSION}-slim AS builder
  ARG PIP_INDEX_URL  build-only (gone at runtime); value baked into an ENV: False
  ARG GIT_SHA        build-only (gone at runtime); value baked into an ENV: False

stage 1: FROM python:${PY_VERSION}-slim
  ARG GIT_SHA        build-only (gone at runtime); value baked into an ENV: True
  ARG PY_VERSION     build-only (gone at runtime) (redeclared: value inherited from global default); value baked into an ENV: False
  ENV MODEL_PATH     runtime (visible in docker inspect/ps env): /models/churn.pkl
  ENV THRESHOLD      runtime (visible in docker inspect/ps env): 0.5
  ENV BUILD_SHA      runtime (visible in docker inspect/ps env): ${GIT_SHA}
$ hadolint --no-color q21/Dockerfile
(no findings, exit 0)
```

**Follow-ups:**
- *Why does ARG show in history?* Build args are recorded in the image's build metadata and layer commands.
- *How do I see runtime env?* `docker inspect` shows ENV and `-e` values for a container, so no secrets there either on shared hosts.
- *Where do big configs go?* A mounted file, with the path in an env var.

**Common mistakes:**
- Expecting an ARG to exist in the running container.
- Using `ARG` before `FROM` inside the stage without redeclaring.
- Baking environment-specific URLs into the image.
- Putting a changing ARG (commit hash) early in the Dockerfile and killing the cache.

### Q22 ⭐⭐ 🟡 Tagging and versioning images for ML. Compare latest, semantic version, git SHA and model-version tags, why latest is a trap for rollbacks, why tags are mutable and digests immutable, how to tag one image several ways, and how to tie an image to a model registry version and a training run. Propose a tag scheme for a team that ships a model API weekly and retrains monthly, and show the docker tag and push commands (not executed, no registry here).
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```python
# Q22: build a tag set for one image, validate tag syntax, print the (not executed) docker commands, and show why 'latest' breaks rollback.
import re, datetime as dt
TAG_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$")     # Docker tag grammar (check current docs)

def tags(app_ver, git_sha, model_name, model_ver, run_id, built, channel=None):
    t = [f"{app_ver}",                                   # human release, moves nothing once pushed
         f"{app_ver}-g{git_sha[:7]}",                    # exact code
         f"sha-{git_sha[:12]}",                          # CI convenience, unique per commit
         f"{app_ver}-{model_name}-m{model_ver}",         # which registry model version is inside / configured
         f"{built:%Y%m%d}-m{model_ver}"]                 # date for humans and retention rules
    if channel: t.append(channel)                        # moving pointer: staging / prod. NEVER the only tag
    return t

built = dt.date(2026, 10, 26)
ts = tags("1.14.0", "9f3c2a1b7d4e5f60", "churn", 23, "run-8841", built, channel="staging")
for t in ts: print(f"{t:32} valid={bool(TAG_RE.match(t))}")
bad = ["churn:v1", "my tag", "-lead", "x" * 129]
print("invalid examples:", [(b[:12], bool(TAG_RE.match(b))) for b in bad])

img, reg = "churn-api", "registry.example.com/ml"
print("\n# NOT EXECUTED (no registry, no daemon):")
print(f"docker build -t {reg}/{img}:{ts[1]} --label org.opencontainers.image.revision=9f3c2a1b7d4e5f60 --label ml.model.version=23 --label ml.run.id=run-8841 .")
for t in ts[:1] + ts[2:]: print(f"docker tag {reg}/{img}:{ts[1]} {reg}/{img}:{t}")
print(f"docker push --all-tags {reg}/{img}")

# latest vs immutable-by-convention: a registry as a dict tag -> digest
reg_state = {"latest": "sha256:aaa1", "1.13.0": "sha256:aaa1"}
reg_state["latest"] = "sha256:bbb2"; reg_state["1.14.0"] = "sha256:bbb2"       # a release moves latest
print("\nafter release 1.14.0, 'latest' ->", reg_state["latest"], "| what was running before? unknown unless you recorded the digest")
print("rollback by tag 1.13.0 ->", reg_state["1.13.0"], "(still there)")
```

**Output (my run):** the script ran with `python3 -I`. `docker build`, `docker tag`, `docker push` were **not executed** (no daemon, no registry); `docker tag --help` and `docker push --help` ran and confirm `--all-tags` exists. The commit hash and registry host are made-up examples.
```text
$ python3 -I q22_tags.py
1.14.0                           valid=True
1.14.0-g9f3c2a1                  valid=True
sha-9f3c2a1b7d4e                 valid=True
1.14.0-churn-m23                 valid=True
20261026-m23                     valid=True
staging                          valid=True
invalid examples: [('churn:v1', False), ('my tag', False), ('-lead', False), ('xxxxxxxxxxxx', False)]

# NOT EXECUTED (no registry, no daemon):
docker build -t registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 --label org.opencontainers.image.revision=9f3c2a1b7d4e5f60 --label ml.model.version=23 --label ml.run.id=run-8841 .
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:1.14.0
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:sha-9f3c2a1b7d4e
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:1.14.0-churn-m23
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:20261026-m23
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:staging
docker push --all-tags registry.example.com/ml/churn-api

after release 1.14.0, 'latest' -> sha256:bbb2 | what was running before? unknown unless you recorded the digest
rollback by tag 1.13.0 -> sha256:aaa1 (still there)
$ docker push --help | grep -E -- '--all-tags'
      -a, --all-tags          Push all tags of an image to the repository
```

**Follow-ups:**
- *How does the cluster deploy?* Reference the digest (or a tag that the deploy job records as a digest). Tools differ; check current docs.
- *Can I reuse a version tag?* Don't. If you must, you have lost auditability.
- *Date tags?* Handy for retention and humans, not for identity.

**Common mistakes:**
- Deploying `latest`.
- Not recording which model went into which image.
- Moving a release tag after a hotfix.
- Tags with `/`, spaces or a leading dash.

### Q23 ⭐⭐ 🟡 Container registries for ML teams: Docker Hub, GitHub Container Registry, and cloud registries (ECR, Artifact Registry, ACR; hedge names and check current docs). Explain push and pull flow, authentication (docker login, short-lived tokens), Docker Hub pull rate limits and mirrors or pull-through caches, private versus public images, image retention and cleanup policies, and cost of storing many 8 GB images. Cloud-specific ECR and IAM details belong to a later part; stay on registry concepts. Mark all commands not executed.
**Asked at:** Bengaluru MLOps job postings that list Docker, Kubernetes and GPU/CUDA workloads (Infosys-linked, Quantiphi-linked, Skyworks, GrabJobs listings; snippets only) plus editorial Docker interview guides (snippets only); postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
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
```bash
# NOT EXECUTED (no daemon, no registry, no credentials)
echo "$REGISTRY_TOKEN" | docker login ghcr.io -u myuser --password-stdin
docker push ghcr.io/myorg/churn-api:1.14.0
docker pull ghcr.io/myorg/churn-api:1.14.0
# pull-through cache / mirror: set in /etc/docker/daemon.json  {{"registry-mirrors": ["https://mirror.example.com"]}}
```
```python
# Q23: (1) parse image references the way the docker CLI normalises them, (2) simulate a retention policy and layer-shared storage.
import re

def parse(ref):
    digest = None
    if "@" in ref: ref, digest = ref.split("@", 1)
    first, _, rest = ref.partition("/")
    if rest and ("." in first or ":" in first or first == "localhost"): reg, path = first, rest
    else: reg, path = "docker.io", ref                      # default registry (Docker Hub)
    if reg == "docker.io" and "/" not in path: path = "library/" + path   # official images
    tag = None
    if ":" in path.rsplit("/", 1)[-1]: path, tag = path.rsplit(":", 1)
    if tag is None and digest is None: tag = "latest"
    return reg, path, tag, digest

for r in ["python:3.12-slim", "myorg/trainer:1.4.0", "ghcr.io/myorg/api:sha-9f3c2a1",
          "123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/api:1.0", "localhost:5000/ml/api",
          "python@sha256:" + "ab" * 32]:
    reg, path, tag, dg = parse(r); print(f"{r[:30]:30} -> registry={reg:34} repo={path:16} tag={tag} digest={'yes' if dg else '-'}")

# Retention: keep tags in use + newest N release tags; untagged manifests expire. Sizes are layer MB (toy numbers).
layers = {"base": 2000, "deps": 5000, "app1": 20, "app2": 20, "app3": 20, "app4": 20, "model_v1": 1500, "model_v2": 1500}
images = {  # tag -> layers, newest last
    "1.10.0": ["base", "deps", "app1"], "1.11.0": ["base", "deps", "app2"],
    "1.12.0": ["base", "deps", "app3", "model_v1"], "1.13.0": ["base", "deps", "app4", "model_v2"]}
def stored(tags): return sum(layers[l] for l in {l for t in tags for l in images[t]})
naive = sum(layers[l] for t in images for l in images[t])
print(f"\nsum of image sizes (no sharing): {naive} MB | stored with layer sharing: {stored(images)} MB")
in_use = {"1.12.0", "1.13.0"}; keep_new = 3
keep = in_use | set(list(images)[-keep_new:])
print("keep:", sorted(keep), "| delete:", sorted(set(images) - keep), "| stored after cleanup:", stored(keep), "MB")
print("lesson: a changed base or deps layer breaks sharing, so every rebuild then costs the full", layers["base"] + layers["deps"], "MB again")
```

**Output (my run):** the script ran with `python3 -I`. All `docker login/push/pull` commands are **not executed** (no daemon, no registry); `docker login --help` ran to confirm `--password-stdin`. No rate-limit or cloud behaviour was tested.
```text
$ python3 -I q23_registry.py
python:3.12-slim               -> registry=docker.io                          repo=library/python   tag=3.12-slim digest=-
myorg/trainer:1.4.0            -> registry=docker.io                          repo=myorg/trainer    tag=1.4.0 digest=-
ghcr.io/myorg/api:sha-9f3c2a1  -> registry=ghcr.io                            repo=myorg/api        tag=sha-9f3c2a1 digest=-
123456789012.dkr.ecr.us-east-1 -> registry=123456789012.dkr.ecr.us-east-1.amazonaws.com repo=ml/api           tag=1.0 digest=-
localhost:5000/ml/api          -> registry=localhost:5000                     repo=ml/api           tag=latest digest=-
python@sha256:abababababababab -> registry=docker.io                          repo=library/python   tag=None digest=yes

sum of image sizes (no sharing): 31080 MB | stored with layer sharing: 10080 MB
keep: ['1.11.0', '1.12.0', '1.13.0'] | delete: ['1.10.0'] | stored after cleanup: 10060 MB
lesson: a changed base or deps layer breaks sharing, so every rebuild then costs the full 7000 MB again
$ docker login --help | grep -- '--password-stdin'
      --password-stdin    Take the Password or Personal Access Token
```

**Follow-ups:**
- *Why not `docker login -p`?* The password shows in shell history and process lists.
- *Mirror or pull-through cache?* A mirror is a copy you maintain; a pull-through cache fetches on demand and keeps what it saw. Either avoids upstream limits.
- *Where do big model files go?* Often outside the registry (object storage or a volume, Q16), which also keeps image storage down.

**Common mistakes:**
- Relying on anonymous Docker Hub pulls in production.
- No cleanup policy until the bill arrives.
- Deleting by age and removing a tag in use.
- Rebuilding the base layer constantly, so nothing is shared.

### Q24 ⭐⭐ 🟢 Dockerfile linting and review checklist. Run hadolint (via pip install hadolint-py if it works) on a deliberately bad ML Dockerfile with FROM :latest, ADD, unpinned pip install, apt-get without cleanup, root user and secrets in ENV. Explain what each finding means, which you would suppress and how (a # hadolint ignore comment with a reason), how to wire it into pre-commit or CI, and what a linter cannot tell you (image size, runtime behaviour, correctness of the app).
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```dockerfile
# --- file: Dockerfile.bad ---
FROM python:latest
ENV HF_TOKEN=hf_FAKE_not_a_real_token
ADD . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y curl build-essential
RUN pip install torch scikit-learn fastapi
USER root
CMD python serve.py

# --- file: Dockerfile.good ---
FROM python:3.11.9-slim-bookworm
# Reason: Debian rotates point versions of apt packages; we pin the base image instead.
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
RUN useradd --uid 10001 --no-create-home app
USER 10001
CMD ["python", "-m", "src.serve"]
```
```yaml
# --- file: hadolint.yaml ---
# repo-level policy. Say WHY each rule is relaxed.
failure-threshold: warning     # info-level findings are printed but do not fail the build
ignored:
  - DL3059                     # consecutive RUN is fine in our long ML installs; readability over layer count

# --- file: .pre-commit-config.yaml ---
repos:
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0          # check current docs for the latest tag
    hooks:
      - id: hadolint-docker   # runs the linter in a container; use id: hadolint if the binary is installed

# --- file: ci_fragment.yml ---
jobs:
  lint-dockerfile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hadolint/hadolint-action@v3.1.0   # check current docs for versions
        with:
          dockerfile: Dockerfile
          failure-threshold: warning
```
```bash
set -u
cd "$(dirname "$0")"
pip install -q hadolint-py >/dev/null 2>&1
hadolint --version
echo "--- bad Dockerfile"
hadolint --no-color Dockerfile.bad; echo "exit=$?"
echo "--- good Dockerfile (no config)"
hadolint --no-color Dockerfile.good; echo "exit=$?"
echo "--- bad Dockerfile with repo config (DL3059 ignored, so fewer lines)"
hadolint --no-color --config cfg/hadolint.yaml Dockerfile.bad | sed "s/\x1b\[[0-9;]*m//g"; 
echo "--- good Dockerfile with repo config"
hadolint --no-color --config cfg/hadolint.yaml Dockerfile.good; echo "exit=$?"
echo "--- yaml parse of pre-commit and CI fragments"
python3 -I -c "
import yaml
for f in ['.pre-commit-config.yaml','ci_fragment.yml','cfg/hadolint.yaml']:
    d=yaml.safe_load(open(f)); print(f,'parses, top keys:',list(d))
"
```

**Output (my run):** hadolint 2.15.1 (pip `hadolint-py` 2.15.1.2), Python 3.13.17, PyYAML 6.0.3. The pre-commit and CI fragments were only parsed as YAML. The pre-commit hook and the GitHub Action were not run (no pre-commit run, no Actions here). `docker buildx build --check` needs a daemon, so it was not executed.
```text
Haskell Dockerfile Linter 2.15.1
--- bad Dockerfile
Dockerfile.bad:1 DL3007 warning: Using latest is prone to errors if the image will ever update. Pin the version explicitly to a release tag
Dockerfile.bad:2 DL3064 warning: Potentially sensitive data should not be used in the `ARG` or `ENV` commands
Dockerfile.bad:3 DL3020 error: Use COPY instead of ADD for files and folders
Dockerfile.bad:5 DL3009 info: Delete the apt lists (/var/lib/apt/lists) after installing something
Dockerfile.bad:6 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
Dockerfile.bad:6 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
Dockerfile.bad:6 DL3015 info: Avoid additional packages by specifying `--no-install-recommends`
Dockerfile.bad:7 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
Dockerfile.bad:7 DL3013 warning: Pin versions in pip. Instead of `pip install <package>` use `pip install <package>==<version>` or `pip install --requirement <requirements file>`
Dockerfile.bad:7 DL3042 warning: Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`
Dockerfile.bad:8 DL3002 warning: Last USER should not be root
Dockerfile.bad:8 DL3066 info: Non-numeric user-id may not be resolvable by host system
Dockerfile.bad:9 DL3025 warning: Use arguments JSON notation for CMD and ENTRYPOINT arguments
exit=1
--- good Dockerfile (no config)
exit=0
--- bad Dockerfile with repo config (DL3059 ignored, so fewer lines)
Dockerfile.bad:1 DL3007 warning: Using latest is prone to errors if the image will ever update. Pin the version explicitly to a release tag
Dockerfile.bad:2 DL3064 warning: Potentially sensitive data should not be used in the `ARG` or `ENV` commands
Dockerfile.bad:3 DL3020 error: Use COPY instead of ADD for files and folders
Dockerfile.bad:5 DL3009 info: Delete the apt lists (/var/lib/apt/lists) after installing something
Dockerfile.bad:6 DL3015 info: Avoid additional packages by specifying `--no-install-recommends`
Dockerfile.bad:6 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
Dockerfile.bad:7 DL3013 warning: Pin versions in pip. Instead of `pip install <package>` use `pip install <package>==<version>` or `pip install --requirement <requirements file>`
Dockerfile.bad:7 DL3042 warning: Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`
Dockerfile.bad:8 DL3002 warning: Last USER should not be root
Dockerfile.bad:8 DL3066 info: Non-numeric user-id may not be resolvable by host system
Dockerfile.bad:9 DL3025 warning: Use arguments JSON notation for CMD and ENTRYPOINT arguments
--- good Dockerfile with repo config
exit=0
--- yaml parse of pre-commit and CI fragments
.pre-commit-config.yaml parses, top keys: ['repos']
ci_fragment.yml parses, top keys: ['jobs']
cfg/hadolint.yaml parses, top keys: ['failure-threshold', 'ignored']
```

**Follow-ups:**
- *Hadolint or a scanner?* Both. Hadolint checks how you wrote the file. Trivy-style scanners check what is inside the built image.
- *Can you fail only on errors?* Yes: `failure-threshold: error`. I start at `warning` and keep info visible.
- *Is there a BuildKit built-in check?* Recent BuildKit has a build-check mode (`docker buildx build --check`, check current docs). It needs a builder, so it did not run here.

**Common mistakes:**
- Silencing a rule globally to get green CI, with no reason written down.
- Treating a clean lint as a security review.
- Putting the `ignore` comment in the wrong place, so it silently does nothing.
- Fixing `DL3064` by deleting the line but leaving the real token in git history.

### Q25 ⭐⭐ 🟡 Jupyter and dev containers on a shared GPU box. Data scientists want JupyterLab in Docker with GPU, their code mounted and files owned by them, not root. Explain bind-mounting the repo, UID and GID mismatch and the --user flag, exposing the port safely (token, localhost or SSH tunnel), persistent home directory, a base image with common libraries, and why a notebook container is not a production image. Show the run command and a compose service; not executed here.
**Asked at:** Bengaluru MLOps job postings that list Docker, Kubernetes and GPU/CUDA workloads (Infosys-linked, Quantiphi-linked, Skyworks, GrabJobs listings; snippets only) plus editorial Docker interview guides (snippets only); postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
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
```yaml
services:
  jupyter:
    image: ${JUPYTER_IMAGE:-jupyter-gpu:2026-10}   # built by the team from a pinned CUDA/PyTorch base
    user: "${HOST_UID:-1000}:${HOST_GID:-1000}"
    working_dir: /workspace
    environment:
      HOME: /home/ds
      JUPYTER_TOKEN: ${JUPYTER_TOKEN:?set a token}
    ports:
      - "127.0.0.1:8888:8888"          # localhost only; reach it with an SSH tunnel
    volumes:
      - ./:/workspace                  # code: bind mount, edits visible on the host
      - ds-home:/home/ds               # persistent home (kernels, config, caches)
      - /data/shared:/data:ro          # shared read-only datasets
    shm_size: "8gb"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1                 # one GPU, not all of them, on a shared box
              capabilities: [gpu]
    command: ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--ServerApp.root_dir=/workspace"]
volumes:
  ds-home:
```
```bash
# --- file: run.sh ---
# NOT EXECUTED (no daemon, no GPU here). Run on the GPU box.
docker run --rm -it --name lab-$USER \
  --user "$(id -u):$(id -g)" -e HOME=/home/ds \
  --gpus '"device=0"' --shm-size=8g \
  -p 127.0.0.1:8888:8888 \
  -e JUPYTER_TOKEN="$JUPYTER_TOKEN" \
  -v "$PWD":/workspace -v ds-home:/home/ds -v /data/shared:/data:ro \
  -w /workspace jupyter-gpu:2026-10 \
  jupyter lab --ip=0.0.0.0 --no-browser
# From the laptop:  ssh -L 8888:localhost:8888 user@gpu-box   then open http://localhost:8888

# --- file: run_all.sh ---
cd "$(dirname "$0")"
echo "--- docker compose config (needs env vars; no daemon needed)"
HOST_UID=1001 HOST_GID=1001 JUPYTER_TOKEN=demo-token docker compose -f compose.yml config 2>&1 | grep -E "user:|host_ip|published|source:|read_only|driver|count|shm_size"
echo "--- missing token must fail"
HOST_UID=1001 docker compose -f compose.yml config 2>&1 | head -3
echo "--- pyyaml check"
python3 -I validate.py compose.yml; echo "exit=$?"
echo "--- UID/GID of this sandbox user, to show what --user would get"
id -u; id -g
echo "--- bash -n syntax check of run.sh"
bash -n run.sh && echo "run.sh syntax OK"
```
```python
import sys, yaml
c = yaml.safe_load(open(sys.argv[1]))
s = c["services"]["jupyter"]
problems = []
if not str(s.get("user", "")).strip(): problems.append("no user: container runs as root, files on bind mount become root-owned")
for p in s.get("ports", []):
    if not str(p).startswith("127.0.0.1:"): problems.append(f"port {p} is published on all interfaces")
if "JUPYTER_TOKEN" not in s.get("environment", {}): problems.append("no token")
dev = s["deploy"]["resources"]["reservations"]["devices"][0]
if dev.get("driver") != "nvidia" or "gpu" not in dev.get("capabilities", []): problems.append("GPU reservation malformed")
if dev.get("count") == "all": problems.append("takes every GPU on a shared box")
named = [v for v in s["volumes"] if not v.startswith(("./", "/"))]
print("named volumes used:", [v.split(":")[0] for v in named])
print("problems:", problems or "none")
sys.exit(1 if problems else 0)
```

**Output (my run):** Docker Compose v5.6.1, PyYAML 6.0.3. Starting the container was not executed (no daemon, no GPU). What ran: `docker compose config` (grep'ed to the lines that matter, with `HOST_UID=1001`), the missing-token failure, a PyYAML policy check, and `bash -n` on the run script. The sandbox user is UID 0, so I set 1001 by hand to show the interpolation.
```text
--- docker compose config (needs env vars; no daemon needed)
              driver: nvidia
              count: 1
    shm_size: "8589934592"
    user: 1001:1001
        source: /home/user/case_studies/interviews/scratch/B4P02_Q24-34/code/q25
        source: ds-home
        source: /data/shared
        read_only: true
        host_ip: 127.0.0.1
        published: "8888"
--- missing token must fail
error while interpolating services.jupyter.environment.JUPYTER_TOKEN: required variable JUPYTER_TOKEN is missing a value: set a token
--- pyyaml check
```

**Follow-ups:**
- *Why not just `chmod 777`?* It hides the real problem and makes every file writable by everyone on a shared box. Matching UIDs is cleaner.
- *VS Code dev containers?* Same ideas (bind mount, matching UID, GPU flag). Check current docs for the exact `devcontainer.json` fields.
- *Where do big datasets go?* A read-only bind mount (`:ro`), not copied into the home volume.

**Common mistakes:**
- `-p 8888:8888` with `--NotebookApp.token=''` on a shared network.
- Running as root, then not being able to edit or delete the files from the host.
- Forgetting `HOME`, so Jupyter fails writing its runtime dir.
- Shipping the notebook image to production because "it already works".

### Q26 ⭐⭐ 🟡 Multi-architecture images and the Apple Silicon problem. A developer builds on an M-series Mac and the image fails on the amd64 GPU server with 'exec format error', or wheels are missing for arm64. Explain architectures (amd64, arm64), docker buildx build --platform, QEMU emulation speed, manifest lists, building in CI on native runners, and checking an image's architecture. Show buildx commands; run docker buildx version and docker buildx build --help here and say that real builds were not executed.
**Asked at:** Docker BuildKit references (BuildKit syntax.md, Docker Hub dockerfile frontend page, OneUptime and Opstree BuildKit articles, a 2026 CI cache-invalidation checklist; search snippets only, not opened); documentation and blogs, not interview reports; MLOps and platform engineer rounds
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
```bash
# --- file: commands.sh ---
# NOT EXECUTED (needs a daemon or a registry). Shown for the interview.
docker buildx create --use --name multi                       # a builder that can do multi-platform
docker buildx build --platform linux/amd64,linux/arm64 \
    -t registry.example.com/team/model-api:1.4.0 --push .      # pushes ONE tag that points to a manifest list
docker buildx imagetools inspect registry.example.com/team/model-api:1.4.0   # lists the platforms
docker image inspect --format '{{.Os}}/{{.Architecture}}' model-api:dev       # arch of a local image
docker run --rm --platform linux/amd64 model-api:dev          # on an M-series Mac: runs under QEMU emulation (slow)
# CI, native runners, one build per arch, then merge: see Q33 for caching

# --- file: run_all.sh ---
cd "$(dirname "$0")"
echo "--- docker buildx version"; docker buildx version 2>&1
echo "--- docker buildx build --help (platform and output lines)"
docker buildx build --help 2>&1 | grep -E "^\s+(--platform|--push|--load|-o, --output|--cache-from|--cache-to)\b"
echo "--- uname -m"; uname -m
echo "--- python3 -I arch_check.py"; python3 -I arch_check.py
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
echo "--- real build attempt:"; docker buildx build --platform linux/amd64,linux/arm64 . 2>&1 | head -3
```
```python
"""Two checks that explain 'exec format error'. Teaching tool, not a Docker API."""
import json, platform, struct, sys

E_MACHINE = {0x3E: "amd64 (x86-64)", 0xB7: "arm64 (aarch64)", 0x28: "arm (32-bit)"}

def elf_arch(path):
    with open(path, "rb") as f:
        head = f.read(20)
    if head[:4] != b"\x7fELF":
        return "not an ELF binary (script or other format)"
    (machine,) = struct.unpack_from("<H", head, 18)   # e_machine, little-endian files
    return E_MACHINE.get(machine, hex(machine))

def pick(manifest_list, os_, arch):
    for m in manifest_list["manifests"]:
        p = m["platform"]
        if p["os"] == os_ and p["architecture"] == arch:
            return m["digest"]
    return None

# Hand-written sample shaped like an OCI index (digests are fake).
SAMPLE = json.loads("""{
 "schemaVersion": 2,
 "mediaType": "application/vnd.oci.image.index.v1+json",
 "manifests": [
  {"digest": "sha256:aaaa", "platform": {"os": "linux", "architecture": "amd64"}},
  {"digest": "sha256:bbbb", "platform": {"os": "linux", "architecture": "arm64"}}
 ]}""")
ARM_ONLY = {"manifests": [SAMPLE["manifests"][1]]}

print("this machine, python platform.machine():", platform.machine())
print("ELF header of", sys.executable, "->", elf_arch(sys.executable))
print("ELF header of /bin/sh ->", elf_arch("/bin/sh"))
print("ELF header of this .py file ->", elf_arch(__file__))
for name, idx in [("multi-arch index", SAMPLE), ("arm64-only index (built on a Mac)", ARM_ONLY)]:
    print(f"{name}: amd64 pick = {pick(idx, 'linux', 'amd64')}, arm64 pick = {pick(idx, 'linux', 'arm64')}")
```

**Output (my run):** Docker CLI 29.9.2, buildx v0.38.1, Python 3.13.17, x86-64 Linux. Real multi-platform builds, QEMU, `imagetools` and registry pushes were not executed (no daemon, no registry). The last line is my attempt, which failed on the daemon connection. The manifest list is a hand-written sample with fake digests. The ELF check is a teaching tool I wrote, not a Docker feature.
```text
--- docker buildx version
github.com/docker/buildx v0.38.1 0dbe87f36ed472fe36b6796c3f70b4210a731fc5
--- docker buildx build --help (platform and output lines)
      --cache-from stringArray        External cache sources (e.g.,
      --cache-to stringArray          Cache export destinations (e.g.,
      --load                          Shorthand for "--output=type=docker"
  -o, --output stringArray            Output destination (format:
      --platform stringArray          Set target platform for build
      --push                          Shorthand for
--- uname -m
x86_64
--- python3 -I arch_check.py
this machine, python platform.machine(): x86_64
ELF header of /usr/bin/python3 -> amd64 (x86-64)
ELF header of /bin/sh -> amd64 (x86-64)
ELF header of this .py file -> not an ELF binary (script or other format)
multi-arch index: amd64 pick = sha256:aaaa, arm64 pick = sha256:bbbb
arm64-only index (built on a Mac): amd64 pick = None, arm64 pick = sha256:bbbb
--- bash -n commands.sh
OK
--- real build attempt:
ERROR: failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
```

**Follow-ups:**
- *Why is QEMU slow?* It translates every instruction in software. Compile steps suffer most.
- *Can I just pin `--platform linux/amd64` in `FROM`?* It works but hides the problem and forces emulation on Macs. Prefer `--platform` at build time.
- *Do I need arm64 at all?* Only if you run on arm machines (some cloud instances, Macs for dev). If the fleet is amd64 only, build amd64 and test on it.

**Common mistakes:**
- Pushing an arm64 build from a Mac to a tag the servers use.
- Believing `--platform` on `docker run` is free: it silently switches to slow emulation.
- Assuming a pip wheel exists for every architecture.
- Trying to test a CUDA image on a Mac.

### Q27 ⭐⭐ 🟡 A long training job in a container on spot or pre-emptible instances. Explain how to write checkpoints to a mounted volume or object store, resume logic in the entrypoint, handling SIGTERM to save a last checkpoint within the stop grace period (docker stop -t), idempotent output paths, logging to stdout, and why exit codes matter for orchestrators. Show a Python training-loop skeleton with a SIGTERM handler that you actually run and kill with a signal, and a docker run command (not executed).
**Asked at:** Bengaluru MLOps job postings that list Docker, Kubernetes and GPU/CUDA workloads (Infosys-linked, Quantiphi-linked, Skyworks, GrabJobs listings; snippets only) plus editorial Docker interview guides (snippets only); postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
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
```python
# --- file: train.py ---
"""Training skeleton for spot instances: atomic checkpoints, resume, SIGTERM -> save -> exit 143."""
import json, os, signal, sys, time

CKPT = os.environ.get("CKPT_PATH", "/ckpt/state.json")
TOTAL = int(os.environ.get("TOTAL_STEPS", "50"))
STEP_SECONDS = float(os.environ.get("STEP_SECONDS", "0.05"))
SAVE_EVERY = int(os.environ.get("SAVE_EVERY", "10"))
stop = False

def on_term(signum, frame):
    global stop
    stop = True                                    # only set a flag; do the save in the main loop
    print(f"got signal {signum}, will checkpoint and exit", flush=True)

def save(state):
    tmp = CKPT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, CKPT)                          # atomic: a reader sees the old or the new file, never half

def load():
    try:
        with open(CKPT) as f: return json.load(f)
    except FileNotFoundError:
        return {"step": 0, "loss": 1.0}

signal.signal(signal.SIGTERM, on_term)
state = load()
print(f"start at step {state['step']}", flush=True)
while state["step"] < TOTAL:
    time.sleep(STEP_SECONDS)                       # stands in for one training step
    state["step"] += 1
    state["loss"] = round(1.0 / (1 + state["step"]), 4)
    if state["step"] % SAVE_EVERY == 0: save(state)
    if stop:
        save(state)
        print(f"saved step {state['step']}, exiting 143", flush=True)
        sys.exit(143)                              # 128 + 15: 'stopped by SIGTERM', orchestrator can retry
save(state)
print(f"done at step {state['step']}, loss {state['loss']}", flush=True)

# --- file: drive.py ---
"""Run train.py, kill it with SIGTERM mid-run, run it again, check it resumed."""
import os, signal, subprocess, sys, tempfile, time, json

d = tempfile.mkdtemp()
env = dict(os.environ, CKPT_PATH=os.path.join(d, "state.json"), TOTAL_STEPS="50", STEP_SECONDS="0.05")
here = os.path.dirname(os.path.abspath(__file__))
cmd = [sys.executable, "-I", os.path.join(here, "train.py")]

p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, text=True)
time.sleep(1.0)                                    # let it get past step 10 or so
p.send_signal(signal.SIGTERM)
out, _ = p.communicate(timeout=10)
print("--- run 1 output\n" + out.strip())
print("run 1 exit code:", p.returncode)
saved = json.load(open(env["CKPT_PATH"]))
print("checkpoint on disk:", saved)

r = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
print("--- run 2 output\n" + r.stdout.strip())
print("run 2 exit code:", r.returncode)
assert saved["step"] > 0 and r.returncode == 0
print("resumed from", saved["step"], "and finished: OK")
```
```bash
# --- file: docker_run.sh ---
# NOT EXECUTED (no daemon). 'ckpt' is a named volume, so it survives the container being replaced.
docker run --name train-42 --init --gpus all --stop-timeout 60 \
  -v ckpt:/ckpt -e CKPT_PATH=/ckpt/state.json \
  --restart on-failure:5 \
  model-train:1.4.0 python train.py
# docker stop sends SIGTERM, waits 60 s, then SIGKILL. On a spot reclaim the node often gives
# only a short warning (check your cloud's docs), so keep SAVE_EVERY small too.

# --- file: run_all.sh ---
cd "$(dirname "$0")"
python3 -I drive.py
echo "--- bash -n docker_run.sh"; bash -n docker_run.sh && echo OK
```

**Output (my run):** Python 3.13.17. The signal test is real: a child process killed with SIGTERM, then restarted. The step number depends on timing, so a rerun may show another number (it was 20 here). The `docker run` command was not executed (no daemon, no GPU, no volume), only syntax-checked with `bash -n`.
```text
--- run 1 output
start at step 0
got signal 15, will checkpoint and exit
saved step 20, exiting 143
run 1 exit code: 143
checkpoint on disk: {'step': 20, 'loss': 0.0476}
--- run 2 output
start at step 20
done at step 50, loss 0.0196
run 2 exit code: 0
resumed from 20 and finished: OK
--- bash -n docker_run.sh
OK
```

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

### Q28 ⭐⭐ 🟡 Installing Python dependencies in an image: pip, uv, conda or micromamba. Compare speed, lockfiles, binary compatibility, and size; pip --no-cache-dir versus a BuildKit cache mount; installing torch from the CPU or CUDA wheel index with --index-url; the venv-in-image pattern for multi-stage copying; and why you should not run pip as root without a venv in some setups. Say when conda is justified in Docker (non-Python native stacks). Show two Dockerfile variants and compare the size by reasoning, not by claimed numbers.
**Asked at:** Docker BuildKit references (BuildKit syntax.md, Docker Hub dockerfile frontend page, OneUptime and Opstree BuildKit articles, a 2026 CI cache-invalidation checklist; search snippets only, not opened); documentation and blogs, not interview reports; MLOps and platform engineer rounds
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
```dockerfile
# --- file: Dockerfile.pip ---
# syntax=docker/dockerfile:1
FROM python:3.11.9-slim-bookworm AS builder
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
WORKDIR /build
COPY requirements.txt .
# torch from the CPU-only index (--index-url, not --extra-index-url, so PyPI cannot shadow it),
# then everything else from PyPI. requirements.txt pins torch too, so the second step keeps it.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu \
    && pip install -r requirements.txt

FROM python:3.11.9-slim-bookworm
COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
WORKDIR /app
COPY src/ ./src/
USER 10001
CMD ["python", "-m", "src.serve"]

# --- file: Dockerfile.uv ---
# syntax=docker/dockerfile:1
FROM python:3.11.9-slim-bookworm AS builder
# pin the uv image tag too (tag below is an example; check the registry for current tags)
COPY --from=ghcr.io/astral-sh/uv:0.11.0 /uv /usr/local/bin/uv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

FROM python:3.11.9-slim-bookworm
COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
WORKDIR /app
COPY src/ ./src/
USER 10001
CMD ["python", "-m", "src.serve"]
```
```bash
cd "$(dirname "$0")"
echo "--- hadolint on both variants"
hadolint --no-color Dockerfile.pip; echo "pip variant exit=$?"
hadolint --no-color Dockerfile.uv;  echo "uv variant exit=$?"
echo "--- uv version"; uv --version
echo "--- uv pip compile --generate-hashes (a real lockfile with hashes, tiny example)"
uv pip compile requirements.in --generate-hashes -q --no-header -o "${TMPDIR:-/tmp}/q28_req.txt" 2>&1 | tail -3
sed -E 's/(sha256:[0-9a-f]{12})[0-9a-f]+/\1.../' "${TMPDIR:-/tmp}/q28_req.txt"
echo "--- pip's own check that hashes are enforced: wrong hash must fail"
printf 'packaging==24.1 --hash=sha256:0000000000000000000000000000000000000000000000000000000000000000\n' > "${TMPDIR:-/tmp}/bad_req.txt"
python3 -m pip install --dry-run --no-deps --require-hashes -r "${TMPDIR:-/tmp}/bad_req.txt" 2>&1 | grep -iE "hash|error" | head -4
```

**Output (my run):** hadolint 2.15.1, uv 0.11.32, pip from Python 3.13.17. Image builds were not executed (no daemon), so neither Dockerfile was built and no sizes were measured. The `ghcr.io/astral-sh/uv:0.11.0` tag and `torch==2.5.1` in the files are examples I did not verify against the registries. Pin tags that exist when you build. The compile output hashes are shortened with `...` in the paste.
```text
--- hadolint on both variants
pip variant exit=0
uv variant exit=0
--- uv version
uv 0.11.32 (x86_64-unknown-linux-gnu)
--- uv pip compile --generate-hashes (a real lockfile with hashes, tiny example)
packaging==26.3 \
    --hash=sha256:94edc256424a... \
    --hash=sha256:d7193f7c8e4e...
    # via -r requirements.in
--- pip's own check that hashes are enforced: wrong hash must fail
ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.
```

**Follow-ups:**
- *uv or pip in production?* Either, with a lockfile and hashes. uv is faster in CI. Pick one and pin it.
- *Why conda at all?* A package that needs a native library the wheel does not bundle, or a stack that is not Python-first.
- *Does the cache mount change the image?* No. It is a build-time directory.

**Common mistakes:**
- `pip install` without a lockfile, so two builds differ.
- Forgetting `--no-cache-dir` and not using a cache mount either.
- The default torch wheel in a CPU-only service.
- Different Python versions in builder and runtime stage.

### Q29 ⭐⭐ 🟡 Debugging a container that will not start or keeps restarting. Walk through docker ps -a, docker logs, docker inspect (ExitCode, OOMKilled, State.Error), docker run --entrypoint sh -it to get a shell, docker exec, docker events, and causes such as 'exec format error', a script with CRLF line endings ('no such file or directory' on the shebang), a missing executable bit, wrong WORKDIR, a missing shared library, and a port conflict. Give a triage order and a table of symptom to cause. Commands not executed; parse a sample inspect JSON with python.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```bash
# --- file: commands.sh ---
# NOT EXECUTED (no daemon). Triage order for a container that will not stay up.
docker ps -a --filter name=api                       # 1. what state, what exit code, how long ago
docker logs --tail 100 api                           # 2. the app's own last words (stdout/stderr)
docker inspect api --format '{{json .State}}'        # 3. ExitCode, OOMKilled, Error (runtime errors live here, not in logs)
docker events --since 10m --filter container=api     # 4. die / oom / restart timeline
docker run --rm -it --entrypoint sh model-api:dev    # 5. get a shell INSIDE the image without the broken entrypoint
docker exec -it api sh                               # 6. only works while it is up

# --- file: crlf_demo.sh ---
# Runs on this machine, no Docker needed: the same failures a container shows.
d=$(mktemp -d); cd "$d"
printf '#!/bin/sh\r\necho hello\r\n' > crlf.sh;  chmod +x crlf.sh
printf '#!/bin/sh\necho hello\n'     > noexec.sh   # no chmod +x
printf '#!/bin/sh\necho hello\n'     > ok.sh;     chmod +x ok.sh
echo "--- CRLF script:";      ./crlf.sh;  echo "exit=$?"
echo "--- missing x bit:";    ./noexec.sh; echo "exit=$?"
echo "--- not in PATH:";      nosuchcmd;  echo "exit=$?"
echo "--- fixed CRLF (tr -d '\\r'):"; tr -d '\r' < crlf.sh > fixed.sh; chmod +x fixed.sh; ./fixed.sh; echo "exit=$?"
echo "--- what file/od shows for the CRLF script:"; od -c crlf.sh | head -2

# --- file: run_all.sh ---
cd "$(dirname "$0")"
python3 -I triage.py inspect_sample.json
echo; bash crlf_demo.sh 2>&1
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
```
```python
import json, sys

def diagnose(c):
    s = c["State"]; code = s["ExitCode"]; err = s.get("Error", "")
    if s.get("OOMKilled"):
        return "OOM kill: raise --memory, shrink batch/workers, check for a leak (docker logs will look like it just stopped)"
    if "exec format error" in err:
        return "wrong CPU architecture: image built for arm64 run on amd64 or the reverse (see Q26)"
    if "no such file or directory" in err:
        return "entrypoint path missing, OR script has CRLF line endings so the shebang interpreter is not found, OR wrong WORKDIR"
    if code == 127: return "command not found: binary or script not in PATH/image"
    if code == 126: return "found but not executable: missing chmod +x, or a directory, or noexec mount"
    if code == 139: return "segfault (SIGSEGV): bad native lib, CUDA/driver mismatch"
    if code == 143: return "stopped by SIGTERM (normal for docker stop); only a problem if nobody asked it to stop"
    if code == 137: return "SIGKILL without OOMKilled: docker kill, stop grace period expired, or host OOM killer (check dmesg)"
    if code == 1:   return "app error: read `docker logs` for the traceback (import error, bad config, missing file)"
    return "unknown: read docker logs and docker events"

data = json.load(open(sys.argv[1]))
print(f"{'container':10} {'status':11} {'exit':>4} {'restarts':>8}  diagnosis")
for c in data:
    print(f"{c['Name']:10} {c['State']['Status']:11} {c['State']['ExitCode']:>4} {c['RestartCount']:>8}  {diagnose(c)}")
```

**Output (my run):** Python 3.13.17, the sandbox shell. Docker commands were not executed (no daemon). The inspect JSON is a hand-written sample (seven made-up containers), parsed by a script I wrote, so the diagnosis text is my own mapping, not Docker output. The CRLF, missing-x-bit and not-found cases ran for real in a plain shell. A container shows "no such file or directory" for the CRLF case, my shell words it "required file not found".
```text
container  status      exit restarts  diagnosis
/api-1     restarting   137        6  OOM kill: raise --memory, shrink batch/workers, check for a leak (docker logs will look like it just stopped)
/api-2     exited       127        0  command not found: binary or script not in PATH/image
/api-3     created      128        0  entrypoint path missing, OR script has CRLF line endings so the shebang interpreter is not found, OR wrong WORKDIR
/api-4     exited       126        0  found but not executable: missing chmod +x, or a directory, or noexec mount
/api-5     exited       143        0  stopped by SIGTERM (normal for docker stop); only a problem if nobody asked it to stop
/api-6     exited         1        3  app error: read `docker logs` for the traceback (import error, bad config, missing file)
/api-7     created      128        0  wrong CPU architecture: image built for arm64 run on amd64 or the reverse (see Q26)

--- CRLF script:
crlf_demo.sh: line 6: ./crlf.sh: cannot execute: required file not found
exit=127
--- missing x bit:
crlf_demo.sh: line 7: ./noexec.sh: Permission denied
exit=126
--- not in PATH:
crlf_demo.sh: line 8: nosuchcmd: command not found
exit=127
--- fixed CRLF (tr -d '\r'):
hello
exit=0
--- what file/od shows for the CRLF script:
0000000   #   !   /   b   i   n   /   s   h  \r  \n   e   c   h   o    
0000020   h   e   l   l   o  \r  \n
--- bash -n commands.sh
OK
```

**Follow-ups:**
- *Logs are empty. Now what?* The process probably never started: read `State.Error`, then override the entrypoint.
- *Container is up but unhealthy?* Look at the health status and what the check runs (Q12).
- *How do I stop CRLF coming back?* `.gitattributes` with `eol=lf`, and lint shell scripts in CI.

**Common mistakes:**
- Reading only `docker logs` and missing `State.Error`.
- Running `docker exec` on a container that keeps dying.
- Treating 137 as "a bug in my code" before checking OOMKilled.
- Editing scripts on Windows without LF settings.

### Q30 ⭐⭐ 🟢 Logging and disk usage in Docker. Explain why apps log to stdout and stderr, the json-file driver and its default of unbounded log growth, log-opts max-size and max-file, other drivers at a glance, docker system df, prune commands and what each deletes (dangling images, build cache, stopped containers, volumes with the -a --volumes flags), and how a GPU server's disk fills up with old 8 GB images. Show a daemon.json snippet and validate it with python json; do not run prune against any real daemon.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  }
}
```
```bash
# --- file: commands.sh ---
# NOT EXECUTED against a daemon. Read-only first, destructive last.
docker system df                         # images, containers, volumes, build cache: size and RECLAIMABLE
docker system df -v                      # per-image / per-volume detail
docker image prune                       # dangling (untagged) images only
docker image prune -a --filter "until=720h"   # ALL images not used by a container, older than 30 days
docker container prune                   # stopped containers
docker builder prune                     # build cache
docker volume prune                      # unused anonymous volumes (add -a for named ones: data loss risk)
docker system prune                      # stopped containers, unused networks, dangling images, build cache
docker system prune -a --volumes         # the dangerous one: also unused images AND unused volumes
# per-container override of the default log settings:
docker run --log-driver json-file --log-opt max-size=50m --log-opt max-file=3 model-api:1.4.0

# --- file: run_all.sh ---
cd "$(dirname "$0")"
python3 -I check_daemon.py daemon.json bad_daemon.json; echo "exit=$?"
echo "--- rotation model"; python3 -I rotation_sim.py
echo "--- real flag names from the CLI help (no daemon needed)"
docker system prune --help 2>&1 | grep -E "^\s+(-a, --all|--volumes|--filter|-f, --force)"
docker volume prune --help 2>&1 | grep -E "^\s+(-a, --all|--filter)"
docker image prune --help 2>&1 | grep -E "^\s+(-a, --all|--filter)"
echo "--- docker system df (no daemon here)"; docker system df 2>&1 | head -2
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
```
```python
# --- file: check_daemon.py ---
import json, re, sys

def to_bytes(s):
    m = re.fullmatch(r"(\d+)([kmg]?)", s)
    return int(m.group(1)) * {"": 1, "k": 1024, "m": 1024**2, "g": 1024**3}[m.group(2)]

def check(path):
    try:
        cfg = json.load(open(path))
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"]
    probs = []
    opts = cfg.get("log-opts", {})
    if cfg.get("log-driver", "json-file") == "json-file":
        if "max-size" not in opts: probs.append("json-file without max-size: logs grow without limit")
        for k in ("max-size", "max-file"):
            if k in opts and not isinstance(opts[k], str): probs.append(f"{k} must be a string like '50m', got {type(opts[k]).__name__}")
    if not probs:
        worst = to_bytes(opts["max-size"]) * int(opts.get("max-file", "1"))
        print(f"{path}: OK. Upper bound per container = {opts['max-size']} x {opts.get('max-file','1')} = {worst/1024**2:.0f} MiB")
    return probs

rc = 0
for p in sys.argv[1:]:
    probs = check(p)
    for x in probs: print(f"{p}: PROBLEM: {x}")
    rc |= bool(probs)
sys.exit(rc)

# --- file: rotation_sim.py ---
"""Tiny model of the json-file driver rotation (max-size, max-file). Not Docker's code."""
import os, tempfile

d = tempfile.mkdtemp(); base = os.path.join(d, "c-json.log")
MAX_SIZE, MAX_FILE = 1000, 3                     # bytes, files
def write(line):
    if os.path.exists(base) and os.path.getsize(base) + len(line) > MAX_SIZE:
        for i in range(MAX_FILE - 1, 0, -1):     # .2 dropped, .1 -> .2, current -> .1
            src = base if i == 1 else f"{base}.{i-1}"
            if os.path.exists(src): os.replace(src, f"{base}.{i}")
    with open(base, "a") as f: f.write(line)
for n in range(200): write(f"step {n:04d} loss=0.123456 acc=0.9876\n")
total = sum(os.path.getsize(os.path.join(d, x)) for x in os.listdir(d))
print("files:", sorted(os.listdir(d)))
print("bytes written: ~", 200 * len("step 0000 loss=0.123456 acc=0.9876\n"), " bytes kept on disk:", total, " (cap = %d)" % (MAX_SIZE * MAX_FILE))
```

**Output (my run):** Docker CLI 29.9.2, Python 3.13.17. Nothing was pruned and `docker system df` could not connect (no daemon). The flag names come from the real `--help` output. The rotation script is my toy model of the idea (bytes kept stay under the cap), not Docker's code. `bad_daemon.json` has a trailing comma and numbers instead of strings; Python's parser stops at the comma first, so the string-type check did not get to run on that file.
```text
daemon.json: OK. Upper bound per container = 50m x 3 = 150 MiB
bad_daemon.json: PROBLEM: invalid JSON: Illegal trailing comma before end of object: line 3 column 46 (char 76)
exit=1
--- rotation model
files: ['c-json.log', 'c-json.log.1', 'c-json.log.2']
bytes written: ~ 7000  bytes kept on disk: 2100  (cap = 3000)
--- real flag names from the CLI help (no daemon needed)
  -a, --all             Remove all unused images not just dangling ones
      --filter filter   Provide filter values (e.g. "label=<key>=<value>")
  -f, --force           Do not prompt for confirmation
      --volumes         Prune anonymous volumes
  -a, --all             Remove all unused volumes, not just anonymous ones
      --filter filter   Provide filter values (e.g. "label=<label>")
  -a, --all             Remove all unused images, not just dangling ones
      --filter filter   Provide filter values (e.g. "until=<timestamp>")
--- docker system df (no daemon here)
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
--- bash -n commands.sh
OK
```

**Follow-ups:**
- *Can I set limits per container?* Yes: `--log-opt max-size=50m --log-opt max-file=3` on `docker run`.
- *Do logs survive `docker rm`?* No, with json-file they go with the container. Ship them to a log system if you need them.
- *Does `docker logs` work with every driver?* No, see the docs for your driver.

**Common mistakes:**
- Unbounded `json-file` on a long-running job.
- Numbers in `log-opts` instead of strings.
- Expecting a `daemon.json` change to apply to running containers.
- `docker system prune -a --volumes` on a shared box.

### Q31 ⭐⭐ 🟡 GPU in Docker Compose and compose structure for dev versus prod. Show how a service requests a GPU (deploy.resources.reservations.devices with driver nvidia, capabilities gpu), compose override files, profiles for optional services, environment-specific settings, restart policies, resource limits, and the difference between compose on one VM and an orchestrator. Validate with docker compose config and a pyyaml script; say that starting the stack was not executed.
**Asked at:** NVIDIA Container Toolkit user guide and runtime docs (docs.nvidia.com, several versions), E2E Networks GPU-in-Docker guide, HowToGeek and LinuxConfig tutorials (search snippets only, not opened); vendor docs and tutorials, not interview reports; GPU and deep-learning MLOps roles (Bengaluru postings mention GPU/CUDA workloads on Kubernetes)
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
```yaml
# --- file: compose.yml ---
services:
  api:
    image: registry.example.com/team/model-api:${TAG:-dev}
    restart: unless-stopped
    environment:
      MODEL_PATH: /models/current
    volumes:
      - models:/models:ro
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request as u; u.urlopen('http://localhost:8000/ready')"]
      interval: 15s
      start_period: 120s
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: 16g
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  prometheus:
    image: prom/prometheus:v2.53.0
    profiles: ["monitoring"]          # only starts with --profile monitoring
  notebook:
    image: jupyter-gpu:dev
    profiles: ["dev"]
volumes:
  models:

# --- file: compose.override.yml ---
# picked up automatically by `docker compose up` next to compose.yml: DEV settings
services:
  api:
    build: .
    restart: "no"
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src                # live code edits
    environment:
      LOG_LEVEL: debug

# --- file: compose.prod.yml ---
# used explicitly: docker compose -f compose.yml -f compose.prod.yml up -d   (override file is NOT read then)
services:
  api:
    restart: always
    ports:
      - "127.0.0.1:8000:8000"         # a reverse proxy on the same VM talks to it
    deploy:
      resources:
        limits:
          memory: 24g
```
```python
import subprocess, sys, yaml

def cfg(*files, profiles=()):
    cmd = ["docker", "compose"]
    for f in files: cmd += ["-f", f]
    for p in profiles: cmd += ["--profile", p]
    cmd += ["config"]
    return yaml.safe_load(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)

def gpu_ok(svc):
    devs = svc.get("deploy", {}).get("resources", {}).get("reservations", {}).get("devices", [])
    return any(d.get("driver") == "nvidia" and "gpu" in d.get("capabilities", []) for d in devs)

dev  = cfg("compose.yml", "compose.override.yml")
prod = cfg("compose.yml", "compose.prod.yml")
dev_all = cfg("compose.yml", "compose.override.yml", profiles=["dev", "monitoring"])
print("dev  services (no profile):      ", sorted(dev["services"]))
print("dev  services (+dev,monitoring): ", sorted(dev_all["services"]))
print("prod services:                   ", sorted(prod["services"]))
for name, c in [("dev", dev), ("prod", prod)]:
    a = c["services"]["api"]
    print(f"{name}: restart={a.get('restart')!r} gpu_reserved={gpu_ok(a)} ports={[ (p.get('host_ip','*'), p['published']) for p in a.get('ports', [])]} mem_limit={a['deploy']['resources']['limits']['memory']}")
assert gpu_ok(prod["services"]["api"]) and prod["services"]["api"]["restart"] == "always"
assert all(p.get("host_ip") == "127.0.0.1" for p in prod["services"]["api"]["ports"])
print("assertions OK: prod keeps GPU reservation, restarts always, publishes on localhost only")
```
```bash
cd "$(dirname "$0")"
echo "--- docker compose version"; docker compose version
echo "--- docker compose config (base only), GPU part"
docker compose -f compose.yml config | sed -n '/devices:/,/count/p'
echo "--- check.py"; python3 -I check.py
echo "--- up was not run:"; docker compose -f compose.yml up -d 2>&1 | head -2
```

**Output (my run):** Docker Compose v5.6.1, PyYAML 6.0.3, Python 3.13.17. `docker compose config` worked without a daemon and normalised the GPU block. Starting the stack (`up`) was not executed (no daemon, no GPU), so the host runtime and the actual GPU grant are unverified. The memory values print in bytes (16 GiB, 24 GiB).
```text
--- docker compose version
Docker Compose version v5.6.1
--- docker compose config (base only), GPU part
          devices:
            - capabilities:
                - gpu
              driver: nvidia
              count: 1
--- check.py
dev  services (no profile):       ['api']
dev  services (+dev,monitoring):  ['api', 'notebook', 'prometheus']
prod services:                    ['api']
dev: restart='no' gpu_reserved=True ports=[('*', '8000')] mem_limit=17179869184
prod: restart='always' gpu_reserved=True ports=[('127.0.0.1', '8000')] mem_limit=25769803776
assertions OK: prod keeps GPU reservation, restarts always, publishes on localhost only
--- up was not run:
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
```

**Follow-ups:**
- *Will `docker compose up` fail with no GPU?* Yes, at start. Config validation will not catch it.
- *`depends_on` and health?* See Q12 and Q14.
- *Can Compose scale across hosts?* Not by itself. That is where an orchestrator starts.

**Common mistakes:**
- Putting dev-only ports and bind mounts in the base file.
- `count: all` on a shared box.
- Trusting `compose config` as proof the GPU works.
- Forgetting that `-f` replaces the automatic override file.

### Q32 ⭐⭐ 🟡 Image scanning and supply-chain basics. Explain CVE scanning of base and Python layers (Trivy, Grype, Docker Scout; hedge tool availability and check current docs), what an SBOM is, why the base image drives most findings, how to triage (reachable, fixable, in the runtime stage or only builder), rebuilding on a schedule, signing images (cosign) at the concept level, and a CI gate with an agreed severity policy. Scanners were not run here unless they install; say so. Write a small policy checker over a sample JSON scan report.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```python
"""Gate: fail on CRITICAL, or HIGH that has a fix, unless waived with an unexpired waiver."""
import json, sys
from datetime import date

report, waivers_file, today = sys.argv[1], sys.argv[2], date.fromisoformat(sys.argv[3])
waivers = {w["id"]: w for w in json.load(open(waivers_file))}
blocking, notes = [], []
for res in json.load(open(report))["Results"]:
    for v in res.get("Vulnerabilities", []):
        sev, fixed, vid = v["Severity"], v.get("FixedVersion", ""), v["VulnerabilityID"]
        violates = sev == "CRITICAL" or (sev == "HIGH" and fixed)
        if not violates:
            notes.append(f"{vid} {sev} {v['PkgName']}: allowed ({'no fix yet' if sev=='HIGH' else 'below threshold'})")
            continue
        w = waivers.get(vid)
        if w and date.fromisoformat(w["expires"]) >= today:
            notes.append(f"{vid} {sev} {v['PkgName']}: WAIVED until {w['expires']} by {w['owner']} ({w['reason']})")
        else:
            why = "waiver EXPIRED" if w else "no waiver"
            blocking.append(f"{vid} {sev} {v['PkgName']} fix={fixed or '-'} [{why}]")
print("BLOCKING:"); [print("  " + b) for b in blocking]
print("OK / waived:"); [print("  " + n) for n in notes]
print("RESULT:", "FAIL" if blocking else "PASS")
sys.exit(1 if blocking else 0)
```
```bash
# --- file: commands.sh ---
# NOT EXECUTED: none of these tools are installed here and there is no image to scan.
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 registry.example.com/team/model-api:1.4.0
trivy image --format json -o scan.json registry.example.com/team/model-api:1.4.0     # feed policy_check.py
trivy image --format cyclonedx -o sbom.cdx.json registry.example.com/team/model-api:1.4.0   # an SBOM
grype registry.example.com/team/model-api:1.4.0 --fail-on high
docker scout cves registry.example.com/team/model-api:1.4.0                          # check current docs
cosign sign registry.example.com/team/model-api@sha256:"$DIGEST"                      # sign the DIGEST, not the tag
cosign verify registry.example.com/team/model-api@sha256:"$DIGEST" --certificate-identity="$IDENTITY" --certificate-oidc-issuer="$ISSUER"

# --- file: run_all.sh ---
cd "$(dirname "$0")"
echo "--- tools present?"; for t in trivy grype syft cosign; do command -v $t >/dev/null && echo "$t: found" || echo "$t: not installed"; done
docker scout version 2>&1 | head -1
echo "--- policy check, today = 2026-10-26"
python3 -I policy_check.py scan_sample.json waivers.json 2026-10-26; echo "exit=$?"
echo "--- same report with an empty waiver list"
W=$(mktemp); echo '[]' > "$W"; python3 -I policy_check.py scan_sample.json "$W" 2026-10-26 | sed -n '1,5p;$p'
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
```

**Output (my run):** Python 3.13.17. Trivy, Grype, Syft, Cosign are not installed here and `docker scout` is not a command in this CLI, so no scanner was run and nothing was signed. The scan report is a hand-written sample shaped like Trivy's JSON, with invented CVE IDs and package names (`CVE-0000-...`), so its findings are not real. The policy script is mine. The date is passed in so the run repeats.
```text
--- tools present?
trivy: not installed
grype: not installed
syft: not installed
cosign: not installed
docker: unknown command: docker scout
--- policy check, today = 2026-10-26
BLOCKING:
  CVE-0000-1001 CRITICAL libfoo fix=1.2.4 [no waiver]
  CVE-0000-2001 CRITICAL somewebpkg fix=9.1.0 [no waiver]
  CVE-0000-2002 HIGH otherpkg fix=0.9.2 [waiver EXPIRED]
OK / waived:
  CVE-0000-1002 HIGH libbar: allowed (no fix yet)
  CVE-0000-1003 HIGH libbaz: WAIVED until 2026-12-31 by platform-team (only reachable via a feature we do not enable)
  CVE-0000-1004 MEDIUM libqux: allowed (below threshold)
RESULT: FAIL
exit=1
--- same report with an empty waiver list
BLOCKING:
  CVE-0000-1001 CRITICAL libfoo fix=1.2.4 [no waiver]
  CVE-0000-1003 HIGH libbaz fix=3.0.1 [no waiver]
  CVE-0000-2001 CRITICAL somewebpkg fix=9.1.0 [no waiver]
  CVE-0000-2002 HIGH otherpkg fix=0.9.2 [no waiver]
RESULT: FAIL
--- bash -n commands.sh
OK
```

**Follow-ups:**
- *Why not fail on every HIGH?* If nothing can fix it, the team learns to bypass the gate. Fail on what is actionable.
- *Scan at build time only?* No: also on a schedule, since new CVEs appear after the build.
- *Does signing stop vulnerabilities?* No. It proves who built the image and that it was not changed.

**Common mistakes:**
- Scanning the builder stage or an old tag instead of the image that ships.
- Waivers with no owner or expiry.
- Treating a scanner result as a risk rating without checking reachability.
- Never rebuilding, so the base stays as old as the last release.

### Q33 ⭐⭐ 🟡 Build caching in CI. A Docker build takes 3 minutes on a laptop and 14 minutes in CI because every run starts with an empty cache. Explain cache-from and cache-to with the registry or inline types, the GitHub Actions cache backend, BuildKit cache mounts not surviving ephemeral runners without an explicit save step, how to order layers for hit rate, and why a pull of the previous image is not a cache by itself. Show a buildx command (not executed) and a workflow YAML fragment parsed with pyyaml. Full CI design is a later part.
**Asked at:** Docker BuildKit references (BuildKit syntax.md, Docker Hub dockerfile frontend page, OneUptime and Opstree BuildKit articles, a 2026 CI cache-invalidation checklist; search snippets only, not opened); documentation and blogs, not interview reports; MLOps and platform engineer rounds
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
```yaml
name: build-image
on:
  push:
    branches: [main]
  pull_request:
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3          # a BuildKit builder that supports cache export
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6            # check current docs for action versions
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ghcr.io/example-org/model-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```
```bash
# --- file: commands.sh ---
# NOT EXECUTED (needs a daemon or BuildKit builder and a registry).
# Registry cache: a separate tag holds cache metadata (and layers with mode=max)
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/example-org/model-api:buildcache \
  --cache-to   type=registry,ref=ghcr.io/example-org/model-api:buildcache,mode=max \
  -t ghcr.io/example-org/model-api:"$GIT_SHA" --push .
# Inline cache: cache metadata inside the image itself (only exports the final image's layers)
docker buildx build --cache-to type=inline --cache-from type=registry,ref=ghcr.io/example-org/model-api:latest -t ... --push .

# --- file: run_all.sh ---
cd "$(dirname "$0")"
echo "--- docker buildx build --help (cache flags)"
docker buildx build --help 2>&1 | grep -A3 -E "^\s+--cache-(from|to)"
echo "--- check_workflow.py"; python3 -I check_workflow.py build.yml
echo "--- cache_sim.py"; python3 -I cache_sim.py
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
```
```python
# --- file: check_workflow.py ---
import sys, yaml
wf = yaml.safe_load(open(sys.argv[1]))
# gotcha: YAML 1.1 reads the key `on` as boolean True
print("trigger key parsed as:", [k for k in wf if k in ("on", True)])
steps = wf["jobs"]["build"]["steps"]
uses = [s.get("uses", "").split("@")[0] for s in steps]
bp = next(s for s in steps if s.get("uses", "").startswith("docker/build-push-action"))
w = bp["with"]
print("steps:", uses)
print("setup-buildx before build-push:", uses.index("docker/setup-buildx-action") < uses.index("docker/build-push-action"))
print("cache-from:", w.get("cache-from"), "| cache-to:", w.get("cache-to"))
assert "cache-from" in w and "cache-to" in w
assert "mode=max" in w["cache-to"], "mode=min would skip intermediate (builder-stage) layers"
assert w["push"].startswith("${{") and "pull_request" in w["push"], "PRs must not push"
print("checks OK")

# --- file: cache_sim.py ---
"""Which layers rebuild when CI starts with an empty cache vs a restored one? (toy model of BuildKit keys)"""
import hashlib

def keys(parent_key, instrs):
    out = []
    for text, content in instrs:
        parent_key = hashlib.sha256((parent_key + text + content).encode()).hexdigest()[:8]
        out.append(parent_key)
    return out

def build(instrs, cache):
    k = keys("base", instrs); rebuilt = []
    for (text, _), key in zip(instrs, k):
        if key not in cache: rebuilt.append(text)
        cache.add(key)
    return rebuilt

run1 = [("COPY requirements.txt", "torch==2.x"), ("RUN pip install", ""), ("COPY src/", "v1")]
run2 = [("COPY requirements.txt", "torch==2.x"), ("RUN pip install", ""), ("COPY src/", "v2")]   # code-only change

shared = set()
build(run1, shared)                                   # a previous CI run saved its cache
print("empty runner cache, code-only change :", build(run2, set()))
print("restored cache, code-only change     :", build(run2, set(shared)))
```

**Output (my run):** buildx v0.38.1, Python 3.13.17, PyYAML 6.0.3. No build ran (no daemon or registry). What ran: `--help` for the cache flags, a PyYAML check of the workflow file, and my toy cache-key simulation. Action versions in the YAML (`@v3`, `@v4`, `@v6`) are what I remember, so check current docs. Pyyaml reads the key `on` as boolean `True`, which the first line of output shows. Use `wf[True]` or quote `"on"` when scripting against workflows.
```text
--- docker buildx build --help (cache flags)
      --cache-from stringArray        External cache sources (e.g.,
                                      "user/app:cache",
                                      "type=local,src=path/to/dir")
      --cache-to stringArray          Cache export destinations (e.g.,
                                      "user/app:cache",
                                      "type=local,dest=path/to/dir")
      --call string                   Set method for evaluating build
--- check_workflow.py
trigger key parsed as: [True]
steps: ['actions/checkout', 'docker/setup-buildx-action', 'docker/login-action', 'docker/build-push-action']
setup-buildx before build-push: True
cache-from: type=gha | cache-to: type=gha,mode=max
checks OK
--- cache_sim.py
empty runner cache, code-only change : ['COPY requirements.txt', 'RUN pip install', 'COPY src/']
restored cache, code-only change     : ['COPY src/']
--- bash -n commands.sh
OK
```

**Follow-ups:**
- *Registry or GHA cache?* GHA is easiest inside GitHub. Registry cache works anywhere and can be shared with laptops.
- *Why `mode=max`?* Multi-stage builds: the builder stage is not in the final image, so `min` would lose its layers.
- *Does a smaller image fix slow CI?* It helps pulls, but the cache is what saves build time.

**Common mistakes:**
- Setting `cache-to` and forgetting `cache-from`.
- Expecting `--mount=type=cache` to survive between runs.
- `COPY . .` before the install step.
- Pushing from pull requests by accident.

### Q34 ⭐⭐ 🟢 Docker in the Kubernetes era. 'Kubernetes removed Docker' (dockershim): explain what changed (kubelet talks to containerd or CRI-O), why images built with Docker still run (OCI image spec), what dockershim was, and what this means for ML teams that build with docker build or buildx and run in a cluster. Say which Docker features do not exist in a cluster (docker.sock in pods, docker compose) and what to use instead (Kaniko, BuildKit, Buildah, hedge names). Keep it to concepts; Kubernetes itself is a later part.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
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
```yaml
# --- file: pod_bad.yaml ---
apiVersion: v1
kind: Pod
metadata: {name: builder}
spec:
  containers:
    - name: build
      image: docker:27-cli
      command: ["docker", "build", "-t", "x", "."]
      volumeMounts:
        - {name: dockersock, mountPath: /var/run/docker.sock}
  volumes:
    - name: dockersock
      hostPath: {path: /var/run/docker.sock}

# --- file: pod_ok.yaml ---
apiVersion: v1
kind: Pod
metadata: {name: builder}
spec:
  containers:
    - name: build
      image: gcr.io/example/rootless-buildkit:placeholder   # a daemonless builder image (name is a placeholder)
      args: ["--context=git://example.com/repo.git", "--destination=registry.example.com/team/model-api:1.4.0"]
```
```python
# --- file: find_sock.py ---
import sys, yaml
for path in sys.argv[1:]:
    doc = yaml.safe_load(open(path))
    hits = [v["name"] for v in doc["spec"].get("volumes", [])
            if "docker.sock" in str(v.get("hostPath", {}).get("path", ""))]
    print(f"{path}: {'FOUND docker.sock hostPath in volume ' + str(hits) if hits else 'no docker.sock mount'}")

# --- file: oci_types.py ---
"""Docker-built images are OCI-compatible. Classify manifest media types from two samples."""
import json
SAMPLES = {
  "older docker v2 manifest": {"schemaVersion": 2, "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "config": {"mediaType": "application/vnd.docker.container.image.v1+json"},
      "layers": [{"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip"}]},
  "OCI manifest": {"schemaVersion": 2, "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "config": {"mediaType": "application/vnd.oci.image.config.v1+json"},
      "layers": [{"mediaType": "application/vnd.oci.image.layer.v1.tar+gzip"}]},
}
for name, m in SAMPLES.items():
    fam = "OCI" if "oci" in m["mediaType"] else "Docker schema 2"
    print(f"{name:26} -> {fam}; layers are tar+gzip: {all('gzip' in l['mediaType'] for l in m['layers'])}")
print("A CRI runtime (containerd, CRI-O) pulls and runs both; the 'Docker' in the image format is just a format.")
```
```bash
# --- file: commands.sh ---
# NOT EXECUTED: needs a cluster node or a daemon.
crictl ps                      # on a node: list containers through the CRI, no Docker involved
crictl images
ctr -n k8s.io images ls        # containerd's own CLI (namespace k8s.io holds Kubernetes images)
kubectl get nodes -o wide      # CONTAINER-RUNTIME column shows containerd://... or cri-o://...

# --- file: run_all.sh ---
cd "$(dirname "$0")"
echo "--- docker version (client part works; no server here)"; docker version 2>&1 | grep -E 'Client|^ Version|Server|failed'
echo "--- find_sock.py"; python3 -I find_sock.py pod_bad.yaml pod_ok.yaml
echo "--- oci_types.py"; python3 -I oci_types.py
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
```

**Output (my run):** Docker CLI 29.9.2 (client only, the daemon is not reachable), Python 3.13.17, PyYAML 6.0.3. No cluster, no `crictl`, no Kaniko or BuildKit pod was run. The pod files are small samples (the builder image name is a placeholder), and the scanner and classifier are my scripts. The `docker version` filter shows the client and the missing server.
```text
--- docker version (client part works; no server here)
Client: Docker Engine - Community
 Version:           29.9.2
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
--- find_sock.py
pod_bad.yaml: FOUND docker.sock hostPath in volume ['dockersock']
pod_ok.yaml: no docker.sock mount
--- oci_types.py
older docker v2 manifest   -> Docker schema 2; layers are tar+gzip: True
OCI manifest               -> OCI; layers are tar+gzip: True
A CRI runtime (containerd, CRI-O) pulls and runs both; the 'Docker' in the image format is just a format.
--- bash -n commands.sh
OK
```

**Follow-ups:**
- *Do I need to rebuild my images after the change?* No.
- *Is Docker dead?* No, Docker is still the common developer tool and builds OCI images. It is just not the cluster runtime by default.
- *Where do I read the runtime a node uses?* `kubectl get nodes -o wide` (CONTAINER-RUNTIME column).

**Common mistakes:**
- Saying "Kubernetes dropped Docker support" and meaning images stopped working.
- Mounting `docker.sock` into pods for builds.
- Using `docker` commands for node debugging on containerd nodes.
- Looking for a `--gpus` flag in Kubernetes.

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

