import re, yaml
DUR = re.compile(r"^(\d+(ms|s|m|h|d|w|y))+$")
rules = yaml.safe_load(open("ml_rules.yml"))
errs, names = [], []
for g in rules["groups"]:
    for r in g["rules"]:
        n = r.get("alert", "?"); names.append(n)
        for k in ("alert", "expr", "for"):
            if k not in r: errs.append(f"{n}: no '{k}'")
        if "for" in r and not DUR.match(str(r["for"])): errs.append(f"{n}: bad duration {r['for']!r}")
        if r.get("expr", "").count("(") != r.get("expr", "").count(")"): errs.append(f"{n}: unbalanced brackets in expr")
        for k in ("severity", "owner"):
            if k not in r.get("labels", {}): errs.append(f"{n}: label '{k}' missing")
        if "runbook_url" not in r.get("annotations", {}): errs.append(f"{n}: no runbook_url")
am = yaml.safe_load(open("alertmanager.yml"))
recv = {x["name"] for x in am["receivers"]}
def walk(r):
    yield r
    for c in r.get("routes", []): yield from walk(c)
for r in walk(am["route"]):
    if r["receiver"] not in recv: errs.append(f"route to unknown receiver {r['receiver']}")
for i in am["inhibit_rules"]:
    for k in ("source_matchers", "target_matchers", "equal"):
        if k not in i: errs.append(f"inhibit rule missing {k}")
    src = re.findall(r'alertname="(\w+)"', " ".join(i["source_matchers"]))
    for s in src:
        if s not in names: errs.append(f"inhibit source {s} is not a defined alert")
print("alerts:", names)
print("route keys ok:", all(k in am["route"] for k in ("receiver", "group_by", "group_wait", "group_interval", "repeat_interval")))
print("errors:", errs or "none")
print("structural check only: promtool and Alertmanager were NOT run")
