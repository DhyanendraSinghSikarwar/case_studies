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
