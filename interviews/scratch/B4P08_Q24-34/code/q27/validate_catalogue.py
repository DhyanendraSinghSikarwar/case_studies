import sys, yaml, re
REQUIRED = ("name", "owner", "severity", "runbook", "action")
OWNERS = {"data-engineering", "data-science", "ml-platform"}
SEVERITIES = {"page", "ticket"}

def validate(doc):
    errors, seen = [], set()
    for i, a in enumerate(doc.get("alerts", [])):
        tag = a.get("name", f"#{i}")
        for k in REQUIRED:
            if not a.get(k):
                errors.append(f"{tag}: missing or empty '{k}'")
        if a.get("name") in seen:
            errors.append(f"{tag}: duplicate name")
        seen.add(a.get("name"))
        if a.get("owner") and a["owner"] not in OWNERS:
            errors.append(f"{tag}: owner '{a['owner']}' is not a known team")
        if a.get("severity") and a["severity"] not in SEVERITIES:
            errors.append(f"{tag}: severity must be one of {sorted(SEVERITIES)}")
        if a.get("runbook") and not re.match(r"https://", a["runbook"]):
            errors.append(f"{tag}: runbook must be an https link")
        if a.get("severity") == "page" and a.get("action") and len(a["action"].split()) < 5:
            errors.append(f"{tag}: a paging alert needs a real first action")
    return errors

for path in sys.argv[1:]:
    doc = yaml.safe_load(open(path))
    errs = validate(doc)
    print(f"{path}: {len(doc['alerts'])} alerts, {'OK' if not errs else str(len(errs)) + ' error(s)'}")
    for e in errs:
        print("  -", e)
