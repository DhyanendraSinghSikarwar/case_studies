# Q29: pickle opcode scanner + pinned-hash requirements check + mutable action tag check. Nothing is ever unpickled.
import pickle, pickletools, hashlib, re
DENY_MODULES = {"os", "posix", "nt", "subprocess", "sys", "socket", "shutil", "builtins", "importlib", "ctypes", "pty", "runpy"}
DENY_BUILTINS = {"eval", "exec", "open", "__import__", "compile", "getattr"}
ALLOW = {("collections", "OrderedDict"), ("numpy", "dtype"), ("numpy.core.multiarray", "_reconstruct"), ("numpy", "ndarray")}
def globals_in(data):
    out, strs = [], []
    for op, arg, pos in pickletools.genops(data):
        if op.name in ("SHORT_BINUNICODE", "BINUNICODE", "UNICODE", "SHORT_BINSTRING", "BINSTRING"): strs.append(arg)
        elif op.name == "GLOBAL": m, n = arg.split(" ", 1); out.append((m, n, pos))
        elif op.name == "STACK_GLOBAL" and len(strs) >= 2: out.append((strs[-2], strs[-1], pos))
    return out
def scan(data):
    findings = []
    for m, n, pos in globals_in(data):
        root = m.split(".")[0]
        bad = root in DENY_MODULES or (m == "builtins" and n in DENY_BUILTINS)
        findings.append((pos, f"{m}.{n}", "DENY" if bad else "ok" if (m, n) in ALLOW else "REVIEW"))
    return findings
class Harmless:                       # when LOADED it would call os.getcwd(): harmless, but it shows the mechanism
    def __reduce__(self):
        import os; return (os.getcwd, ())
good = pickle.dumps({"weights": [0.1, 0.2], "name": "m1"}, protocol=2)
bad2 = pickle.dumps(Harmless(), protocol=2)
bad4 = pickle.dumps(Harmless(), protocol=4)
for label, d in (("plain dict, protocol 2", good), ("reduce->os.getcwd, protocol 2", bad2), ("reduce->os.getcwd, protocol 4", bad4)):
    print(label, "->", scan(d) or "no globals")
# pinned-hash requirements check
REQ = """numpy==1.26.4 --hash=sha256:aaaa
requests>=2.0
torch
internal-lib==1.0 --hash=sha256:bbbb
git+https://example.invalid/x.git
reqests==2.31.0 --hash=sha256:cccc"""
KNOWN = {"numpy", "requests", "torch", "internal-lib"}
for line in REQ.splitlines():
    name = re.split(r"[=<>@ ]", line)[0]; issues = []
    if line.startswith(("git+", "http")): issues.append("URL install, no hash")
    elif "==" not in line: issues.append("not pinned with ==")
    if "--hash=sha256:" not in line and not issues: issues.append("no hash")
    if "==" in line and name not in KNOWN: issues.append("name not in approved index list (typosquat?)")
    print(f"{line[:38]:<40}", "OK" if not issues else "; ".join(issues))
# artefact hash check
blob = b"pretend-weights"; want = hashlib.sha256(blob).hexdigest()
print("hash match:", hashlib.sha256(blob).hexdigest() == want, "| tampered:", hashlib.sha256(blob + b"x").hexdigest() == want)
# mutable CI action tags
WF = ["uses: actions/checkout@v4", "uses: actions/setup-python@" + "a" * 40, "uses: some-org/deploy@main"]
for l in WF: print(l[:50], "->", "pinned SHA" if re.search(r"@[0-9a-f]{40}$", l) else "MUTABLE tag/branch")
