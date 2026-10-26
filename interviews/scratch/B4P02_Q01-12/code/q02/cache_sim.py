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
