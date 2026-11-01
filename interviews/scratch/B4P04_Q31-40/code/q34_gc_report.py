"""List which DVC cache objects are referenced by given Git revisions, and which are not.
usage: python -I q34_gc_report.py REPO REV [REV ...]"""
import json, subprocess, sys, pathlib, yaml

repo = pathlib.Path(sys.argv[1]); revs = sys.argv[2:]
cache = repo / ".dvc" / "cache" / "files" / "md5"

def git(*a): return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout

def obj_path(h): return cache / h[:2] / h[2:]

def expand(h):                      # a '.dir' hash points to a manifest listing member hashes
    if not h.endswith(".dir"): return {h}
    out = {h}; p = obj_path(h)
    if p.exists():
        out |= {e["md5"] for e in json.loads(p.read_text())}
    return out

def hashes_at(rev):
    found = {}
    for f in git("ls-tree", "-r", "--name-only", rev).split():
        if f.endswith(".dvc") or f.endswith("dvc.lock"):
            doc = yaml.safe_load(git("show", f"{rev}:{f}")) or {}
            outs = doc.get("outs", []) if f.endswith(".dvc") else \
                   [o for s in doc.get("stages", {}).values() for o in s.get("outs", [])]
            for o in outs:
                for h in expand(o["md5"]): found[h] = f"{f}:{o['path']}"
    return found

ref = {}
for r in revs:
    for h, why in hashes_at(r).items(): ref.setdefault(h, []).append(f"{r}:{why}")
on_disk = {p.parent.name + p.name for p in cache.rglob("*") if p.is_file()}
print(f"revisions scanned : {revs}")
print(f"objects in cache  : {len(on_disk)}")
print(f"referenced        : {len(set(ref) & on_disk)}")
for h in sorted(set(ref) & on_disk): print(f"  KEEP   {h[:10]}  <- {ref[h][0]}")
unref = on_disk - set(ref)
print(f"unreferenced      : {len(unref)}  (a 'dvc gc' candidate, but ONLY for these revisions)")
for h in sorted(unref): print(f"  UNREF  {h[:10]}  {obj_path(h).stat().st_size} bytes")
missing = set(ref) - on_disk
print(f"referenced but not in cache: {len(missing)}")
