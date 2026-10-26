"""Parse a multi-stage Dockerfile: stages, COPY --from targets, apt packages per stage."""
import re, sys
text = open(sys.argv[1]).read().replace("\\\n", " ")
stages, cur = {}, None
for line in text.splitlines():
    line = line.strip()
    m = re.match(r"FROM\s+(\S+)(?:\s+AS\s+(\S+))?", line, re.I)
    if m:
        cur = m.group(2) or str(len(stages)); stages[cur] = {"base": m.group(1), "apt": [], "from": []}
        continue
    if cur is None: continue
    m = re.search(r"COPY\s+--from=(\S+)", line)
    if m: stages[cur]["from"].append(m.group(1))
    m = re.search(r"apt-get install\s+(.*?)(?:&&|$)", line)
    if m: stages[cur]["apt"] += [w for w in m.group(1).split() if not w.startswith("-")]
for name, s in stages.items():
    print(f"stage {name:8} base={s['base']:26} apt={s['apt']} copy_from={s['from']}")
ok = True
for name, s in stages.items():
    for src in s["from"]:
        if src not in stages: print("ERROR: unknown stage", src); ok = False
final = list(stages)[-1]
left = set(stages["builder"]["apt"]) - set(stages[final]["apt"])
print("final stage:", final)
print("left behind (apt in builder, not in final):", sorted(left))
print("runtime libs kept:", sorted(set(stages["builder"]["apt"]) & set(stages[final]["apt"])))
print("COPY --from references valid:", ok)
