import sys
import yaml

gh = yaml.safe_load(open(sys.argv[1]))
print("github keys:", list(gh))
print("github 'on' key present as string:", "on" in gh, "| as boolean True:", True in gh)
print("github jobs:", {k: v.get("needs") for k, v in gh["jobs"].items()})

gl = yaml.safe_load(open(sys.argv[2]))
jobs = {k: v for k, v in gl.items() if isinstance(v, dict) and "stage" in v}
print("gitlab stages:", gl["stages"])
for name, j in jobs.items():
    assert j["stage"] in gl["stages"], name
    for dep in j.get("needs", []):
        assert dep in jobs, (name, dep)
    print(f"gitlab job {name}: stage={j['stage']} needs={j.get('needs', [])}")
print("gitlab references all valid")
