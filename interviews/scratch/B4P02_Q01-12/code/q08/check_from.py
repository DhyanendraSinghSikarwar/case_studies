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
