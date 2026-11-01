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
