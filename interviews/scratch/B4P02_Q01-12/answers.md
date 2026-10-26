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
