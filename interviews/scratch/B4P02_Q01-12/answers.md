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
