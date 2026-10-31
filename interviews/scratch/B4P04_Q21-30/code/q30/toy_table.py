# Q30: toy snapshot table (Delta/Iceberg idea in 60 lines): immutable data files + a manifest per version.
import json, os, tempfile, time
class ToyTable:
    def __init__(self, root): self.root = root; os.makedirs(root, exist_ok=True); self.log = []   # log[i] = manifest of version i
    def _write(self, name, rows):
        with open(os.path.join(self.root, name), "w") as f: json.dump(rows, f)
    def commit(self, add=(), remove=()):
        files = list(self.log[-1]["files"]) if self.log else []
        files = [f for f in files if f not in remove]
        for i, rows in enumerate(add):
            n = f"data-v{len(self.log)}-{i}.json"; self._write(n, rows); files.append(n)
        self.log.append({"version": len(self.log), "ts": time.time(), "files": files})   # files never edited in place
        return len(self.log) - 1
    def read(self, version=None, ts=None):
        if ts is not None: version = max(m["version"] for m in self.log if m["ts"] <= ts)
        m = self.log[-1 if version is None else version]
        rows = []
        for f in m["files"]:
            p = os.path.join(self.root, f)
            if not os.path.exists(p): raise FileNotFoundError(f"version {m['version']} needs {f}, which was vacuumed")
            rows += json.load(open(p))
        return rows
    def vacuum(self, keep_last_n):
        """Delete data files that no kept version references (like VACUUM / expire_snapshots)."""
        keep = {f for m in self.log[-keep_last_n:] for f in m["files"]}
        gone = [f for f in os.listdir(self.root) if f not in keep]
        for f in gone: os.remove(os.path.join(self.root, f))
        return sorted(gone)

t = ToyTable(tempfile.mkdtemp(prefix="toy_", dir="/tmp/claude-0"))
v0 = t.commit(add=[[{"id": 1, "amt": 10}, {"id": 2, "amt": 20}]]); time.sleep(0.05); mid = time.time(); time.sleep(0.05)
v1 = t.commit(add=[[{"id": 3, "amt": 30}]])
v2 = t.commit(add=[[{"id": 1, "amt": 10}, {"id": 2, "amt": 25}]], remove=["data-v0-0.json"])   # rewrite file: id 2 amt 20 -> 25
print("v0 rows:", len(t.read(0)), "| v1 rows:", len(t.read(1)), "| v2 rows:", len(t.read(2)))
print("as of timestamp 'mid' ->", [r["id"] for r in t.read(ts=mid)], "(version", max(m["version"] for m in t.log if m["ts"] <= mid), ")")
print("train snapshot = version 1 ids/amt:", [(r["id"], r["amt"]) for r in t.read(1)])
print("vacuum keeping only the latest version deletes:", t.vacuum(keep_last_n=1))
print("latest still fine:", [(r["id"], r["amt"]) for r in t.read()])
for v in (1, 0):
    try: t.read(v)
    except FileNotFoundError as e: print(f"time travel to v{v} ->", e)
