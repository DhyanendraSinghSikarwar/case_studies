import sys, yaml
wf = yaml.safe_load(open(sys.argv[1]))
# gotcha: YAML 1.1 reads the key `on` as boolean True
print("trigger key parsed as:", [k for k in wf if k in ("on", True)])
steps = wf["jobs"]["build"]["steps"]
uses = [s.get("uses", "").split("@")[0] for s in steps]
bp = next(s for s in steps if s.get("uses", "").startswith("docker/build-push-action"))
w = bp["with"]
print("steps:", uses)
print("setup-buildx before build-push:", uses.index("docker/setup-buildx-action") < uses.index("docker/build-push-action"))
print("cache-from:", w.get("cache-from"), "| cache-to:", w.get("cache-to"))
assert "cache-from" in w and "cache-to" in w
assert "mode=max" in w["cache-to"], "mode=min would skip intermediate (builder-stage) layers"
assert w["push"].startswith("${{") and "pull_request" in w["push"], "PRs must not push"
print("checks OK")
