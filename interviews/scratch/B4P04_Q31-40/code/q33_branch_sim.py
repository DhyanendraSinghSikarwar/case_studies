"""Toy lakeFS-style branching: objects are immutable blobs; a commit is a path->blob-id map.
Branching copies only the map (zero-copy); merge is a 3-way merge on paths."""
import hashlib

class Repo:
    def __init__(self):
        self.blobs = {}            # blob_id -> bytes  (the "object store")
        self.commits = {}          # commit_id -> (parent, {path: blob_id}, msg)
        self.branches = {}         # name -> commit_id
        self.hooks = []            # pre-merge hooks: fn(files: dict[path, bytes]) -> None or raises
        c = self._commit(None, {}, "init"); self.branches["main"] = c
        self.staged = {}           # branch -> {path: blob_id or None}

    def _commit(self, parent, tree, msg):
        cid = hashlib.sha1(f"{parent}{sorted(tree.items())}{msg}".encode()).hexdigest()[:8]
        self.commits[cid] = (parent, dict(tree), msg); return cid
    def branch(self, name, source="main"):
        self.branches[name] = self.branches[source]            # copies a pointer, no data
    def put(self, branch, path, data: bytes):
        bid = hashlib.sha1(data).hexdigest()[:8]; self.blobs.setdefault(bid, data)
        self.staged.setdefault(branch, {})[path] = bid
    def delete(self, branch, path): self.staged.setdefault(branch, {})[path] = None
    def tree(self, cid): return self.commits[cid][1]
    def commit(self, branch, msg):
        tree = dict(self.tree(self.branches[branch]))
        for p, b in self.staged.pop(branch, {}).items():
            tree.pop(p, None) if b is None else tree.__setitem__(p, b)
        self.branches[branch] = self._commit(self.branches[branch], tree, msg)
    def files(self, branch): return {p: self.blobs[b] for p, b in self.tree(self.branches[branch]).items()}
    def base(self, a, b):
        anc = set(); c = a
        while c: anc.add(c); c = self.commits[c][0]
        c = b
        while c not in anc: c = self.commits[c][0]
        return c
    def merge(self, src, dst):
        for h in self.hooks: h(self.files(src))               # pre-merge quality gate
        ca, cb = self.branches[src], self.branches[dst]; base = self.tree(self.base(ca, cb))
        s, d = self.tree(ca), self.tree(cb); out = dict(d)
        for p in set(s) | set(d) | set(base):
            if s.get(p) == d.get(p): continue
            if s.get(p) == base.get(p): continue                   # only dst changed
            if d.get(p) == base.get(p):                            # only src changed
                out.pop(p, None) if p not in s else out.__setitem__(p, s[p]); continue
            raise RuntimeError(f"conflict on {p}")
        self.branches[dst] = self._commit(cb, out, f"merge {src}")

def no_null_ids(files):
    for p, data in files.items():
        if p.endswith(".csv") and any(l.startswith(b",") for l in data.splitlines()): raise ValueError(f"quality gate failed: empty id in {p}")

r = Repo(); r.hooks.append(no_null_ids)
r.put("main", "users/part-0.csv", b"1,a\n2,b\n"); r.commit("main", "load v1")
print("main files:", sorted(r.files("main")))

r.branch("ingest-2026-10-26")
print("blobs before branch write:", len(r.blobs))
r.put("ingest-2026-10-26", "users/part-1.csv", b"3,c\n,d\n")      # bad row: empty id
r.commit("ingest-2026-10-26", "new batch")
print("blobs after one new file :", len(r.blobs), "(old file not copied)")
try: r.merge("ingest-2026-10-26", "main")
except ValueError as e: print("merge blocked:", e)
print("main still:", sorted(r.files("main")))

r.put("ingest-2026-10-26", "users/part-1.csv", b"3,c\n4,d\n"); r.commit("ingest-2026-10-26", "fix batch")
r.merge("ingest-2026-10-26", "main")
print("merged main:", sorted(r.files("main")))

# conflict: two branches edit the same path
r.branch("a"); r.branch("b")
r.put("a", "users/part-0.csv", b"1,A\n"); r.commit("a", "edit a")
r.put("b", "users/part-0.csv", b"1,B\n"); r.commit("b", "edit b")
r.merge("a", "main")
try: r.merge("b", "main")
except RuntimeError as e: print("second merge:", e)
