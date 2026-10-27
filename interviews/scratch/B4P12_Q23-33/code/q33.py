# Q33: RACI as YAML, validated: known roles, exactly one A (a single role), at least one R, no role twice in one row, every role used.
import yaml, pathlib, copy
def validate(doc):
    errs = []; roles = set(doc["roles"]); used = set()
    for a in doc["activities"]:
        n = a["name"]
        if isinstance(a.get("A"), list): errs.append(f"{n}: A must be ONE role, got list {a['A']}")
        accountable = a.get("A")
        if not accountable: errs.append(f"{n}: no accountable owner")
        if not a.get("R"): errs.append(f"{n}: nobody is Responsible")
        for k in "RCI":
            for r in a.get(k, []):
                if r not in roles: errs.append(f"{n}: unknown role {r} in {k}")
                used.add(r)
        if isinstance(accountable, str):
            if accountable not in roles: errs.append(f"{n}: unknown role {accountable} in A")
            used.add(accountable)
        names = [x for k in "RCI" for x in a.get(k, [])]
        if len(names) != len(set(names)): errs.append(f"{n}: a role appears in more than one of R, C, I")
    for r in roles - used: errs.append(f"role {r} has no part in any activity")
    if len({a['name'] for a in doc['activities']}) != len(doc['activities']): errs.append("duplicate activity names")
    return errs
doc = yaml.safe_load(pathlib.Path("q33_raci.yaml").read_text())
print("good RACI:", validate(doc) or "no errors", "| activities:", len(doc["activities"]), "| metrics:", len(doc["metrics"]))
bad = copy.deepcopy(doc)
bad["activities"][0]["A"] = ["product_ds", "platform"]
bad["activities"][1]["R"] = []
bad["activities"][2]["C"] = ["data_wizard"]
bad["activities"][6]["A"] = None
bad["activities"][7]["I"] = ["security"]
for e in validate(bad): print("bad RACI:", e)
# queue arithmetic for the ticket-bottleneck failure mode (invented): 40 DS x 0.4 requests/week, platform does 2 people x 6 tickets/week
arr, cap = 40 * 0.4, 2 * 6
print(f"tickets/week in={arr:.1f} out={cap} -> utilisation {arr/cap:.2f}; with self-service handling 70% of requests: in={arr*0.3:.1f}, utilisation {arr*0.3/cap:.2f}")
