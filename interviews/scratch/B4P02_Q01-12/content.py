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
