import yaml, sys
p = yaml.safe_load(open(sys.argv[1]))
need = ["model", "validation", "monitoring", "challenger", "audit", "explainability", "change_control"]
missing = [k for k in need if k not in p]
assert not missing, missing
levels = {"warn", "breach"}
for c in p["monitoring"]["checks"]:
    assert c["level"] in levels and isinstance(c["threshold"], float) and c["action"], c
# every check name with a breach level must have an action that is not just a notification
breach_actions = {c["action"] for c in p["monitoring"]["checks"] if c["level"] == "breach"}
assert breach_actions <= {"open_review", "block_scoring_and_page"}, breach_actions
# a warn threshold must be below its breach threshold when both exist
by = {}
for c in p["monitoring"]["checks"]: by.setdefault(c["name"], {})[c["level"]] = c["threshold"]
for n, d in by.items():
    if len(d) == 2: assert d["warn"] < d["breach"], n
assert p["challenger"]["mode"] == "shadow" and "retain_years" in p["audit"]
print("policy OK: sections", sorted(p), "| checks", len(p["monitoring"]["checks"]), "| names with both levels:", [n for n, d in by.items() if len(d) == 2])
