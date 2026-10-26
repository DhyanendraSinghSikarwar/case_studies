"""Q25: offline lint with pyyaml. No deploy, no network. (actionlint is not installed here.)"""
import sys, re, yaml
SECRET_PAT = re.compile(r"(client[-_]secret|credentials_json|AZURE_CREDENTIALS|private_key|\.json)", re.I)

def lint(path):
    doc = yaml.safe_load(open(path))
    trig = doc.get("on", doc.get(True))             # pyyaml (YAML 1.1) reads the key `on` as boolean True
    errs = []
    perms = doc.get("permissions", {})
    if perms.get("id-token") != "write": errs.append("workflow lacks permissions.id-token: write (OIDC login would fail)")
    text = open(path).read()
    for line in text.splitlines():
        code = line.split("#")[0]
        if SECRET_PAT.search(code): errs.append(f"long-lived credential pattern: {code.strip()}")
    for name, job in doc["jobs"].items():
        steps = job["steps"]
        login = [s for s in steps if str(s.get("uses", "")).startswith(("azure/login", "google-github-actions/auth"))]
        if not login: errs.append(f"job {name}: no federated login step")
        for s in steps:
            if "uses" in s and "@" not in s["uses"]: errs.append(f"job {name}: unpinned action {s['uses']}")
        if "deploy" in name and "environment" not in job: errs.append(f"job {name}: deploy job without an environment (no approval gate)")
    return trig, errs

for p in sys.argv[1:]:
    trig, errs = lint(p)
    print(p.split("/")[-1], "| trigger:", trig)
    for e in errs: print("   -", e)
    if not errs: print("   lint: OK")

# negative test: a bad workflow must be caught
bad = """
name: bad
on: push
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
"""
open("bad.yml", "w").write(bad)
trig, errs = lint("bad.yml"); print("bad.yml |", len(errs), "findings"); [print("   -", e) for e in errs]
import os; os.remove("bad.yml")
