import json
d = json.load(open("states.json")); S = d["States"]
targets = {d["StartAt"]}
for n, s in S.items():
    if "Next" in s: targets.add(s["Next"])
    for c in s.get("Choices", []): targets.add(c["Next"])
    if "Default" in s: targets.add(s["Default"])
    assert s["Type"] in ("Succeed", "Fail", "Choice") or "Next" in s or s.get("End"), f"{n} has no exit"
missing = targets - set(S)
reachable = targets & set(S)
print("states:", list(S), "| missing targets:", sorted(missing) or "none", "| unreachable:", sorted(set(S) - reachable) or "none")
