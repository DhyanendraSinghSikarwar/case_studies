import yaml
am = yaml.safe_load(open("alertmanager.yml"))
cat = yaml.safe_load(open("catalogue.yaml"))["alerts"]
receivers = {r["name"] for r in am["receivers"]}
def walk(route):
    yield route
    for r in route.get("routes", []):
        yield from walk(r)
used = {r["receiver"] for r in walk(am["route"]) if "receiver" in r}
print("receivers defined but unused:", sorted(receivers - used) or "none")
print("routes pointing to unknown receiver:", sorted(used - receivers) or "none")
# which receiver would each catalogue entry reach? (simplified first-match on owner and severity)
def pick(a):
    for r in am["route"]["routes"]:
        want = dict(m.replace('"', '').split("=", 1) for m in r["matchers"])
        if all(a.get(k) == v for k, v in want.items()):
            return r["receiver"]
    return am["route"]["receiver"]
for a in cat:
    print(f"{a['name']:24s} -> {pick(a)}")
