"""Q35: tiny Dockerfile stage parser. Fails if the final stage can see test dependencies.
Run: python3 -I check_stages.py Dockerfile"""
import re, sys

def stages(text):
    out, cur = {}, None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"FROM\s+(\S+)(?:\s+AS\s+(\S+))?$", line, re.I)
        if m:
            cur = m.group(2) or m.group(1)
            out[cur] = {"from": m.group(1), "lines": []}
        elif cur:
            out[cur]["lines"].append(line)
    return out

def lineage(st, name):
    chain = [name]
    while st[chain[-1]]["from"] in st:
        chain.append(st[chain[-1]]["from"])
    return chain

st = stages(open(sys.argv[1]).read())
print("stages:", list(st))
for name in st:
    print(f"  {name}: lineage {' -> '.join(lineage(st, name))}")
final = list(st)[-1]
chain = lineage(st, final)
bad = [l for n in chain for l in st[n]["lines"] if "requirements-test" in l or "tests/" in l or "pytest" in l]
print("final stage:", final, "| test-related lines in its lineage:", bad)
sys.exit(1 if bad else 0)
