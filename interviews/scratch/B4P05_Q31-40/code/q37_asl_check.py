"""Offline structural check of an ASL file: every Next/Default/Catch target exists, no orphan states, a terminal state is reachable."""
import json, sys
sm = json.load(open(sys.argv[1])); S = sm["States"]; errs = []
def targets(name, s):
    t = []
    if "Next" in s: t.append(s["Next"])
    if "Default" in s: t.append(s["Default"])
    t += [c["Next"] for c in s.get("Choices", []) if "Next" in c]
    t += [c["Next"] for c in s.get("Catch", [])]
    return t
if sm["StartAt"] not in S: errs.append(f"StartAt {sm['StartAt']} missing")
for n, s in S.items():
    for t in targets(n, s):
        if t not in S: errs.append(f"{n} -> {t} does not exist")
    if s["Type"] in ("Task", "Pass", "Parallel", "Map", "Wait") and not ("Next" in s or s.get("End")):
        errs.append(f"{n} has neither Next nor End")
seen, stack = set(), [sm["StartAt"]]
while stack:
    n = stack.pop()
    if n in seen or n not in S: continue
    seen.add(n); stack += targets(n, S[n])
for n in S:
    if n not in seen: errs.append(f"{n} is unreachable")
terminal = [n for n in seen if S[n]["Type"] in ("Succeed", "Fail") or S[n].get("End")]
if not terminal: errs.append("no terminal state reachable")
print("states:", len(S), "| reachable:", len(seen), "| terminals:", sorted(terminal))
print("ERRORS:" if errs else "OK: all Next targets exist", *errs, sep="\n  " if errs else " ")
sys.exit(bool(errs))
