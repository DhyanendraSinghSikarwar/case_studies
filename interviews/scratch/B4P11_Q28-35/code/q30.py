# q30.py - Region x data-class policy checker. The policy is OUR org's choice, not law and not a list of what a cloud offers.
# Region names are labels used in the sample; whether a service exists in a Region: check current docs. Not legal advice.
import yaml
POLICY = yaml.safe_load("""
allowed_regions:
  public:        ["any"]
  personal:      ["centralindia", "southindia", "asia-south1", "asia-south2"]   # org choice: keep personal data in India
  regulated_fin: ["centralindia", "southindia", "asia-south1", "asia-south2"]   # sector rule (e.g. RBI-type) may be stricter than the Act; check current rules
  restricted_countries: []   # fill from any government notification; empty = none known to us
locations_that_count: [primary_data, training_compute, serving, artifacts, logs, backups, monitoring]
""")
CONFIGS = {
 "churn-azure": {"data_class": "personal", "primary_data": "centralindia", "training_compute": "centralindia",
                 "serving": "centralindia", "artifacts": "centralindia", "logs": "centralindia",
                 "backups": "southindia", "monitoring": "centralindia"},
 "fraud-gcp":   {"data_class": "regulated_fin", "primary_data": "asia-south1", "training_compute": "asia-south1",
                 "serving": "asia-south1", "artifacts": "asia-south1", "logs": "us-central1",
                 "backups": "asia-south2", "monitoring": "asia-south1"},
 "recsys-gcp":  {"data_class": "personal", "primary_data": "asia-south1", "training_compute": "us-central1",
                 "serving": "asia-south1", "artifacts": "multi-region-US", "logs": "asia-south1",
                 "backups": "asia-south1", "monitoring": "asia-south1"},
 "docs-public": {"data_class": "public", "primary_data": "westeurope", "training_compute": "westeurope",
                 "serving": "westeurope", "artifacts": "westeurope", "logs": "westeurope",
                 "backups": "westeurope", "monitoring": "westeurope"},
 "bad-config":  {"data_class": "personal", "primary_data": "centralindia", "serving": "centralindia"},
}
def check(name, cfg, pol=POLICY):
    issues = []
    cls = cfg.get("data_class")
    if cls not in pol["allowed_regions"]:
        return [f"unknown data_class {cls!r}"]
    ok = pol["allowed_regions"][cls]
    for loc in pol["locations_that_count"]:
        r = cfg.get(loc)
        if r is None:
            issues.append(f"{loc}: not declared (unknown is a finding, not a pass)")
        elif r in pol["allowed_regions"]["restricted_countries"]:
            issues.append(f"{loc}: {r} is on the restricted list")
        elif ok != ["any"] and r not in ok:
            issues.append(f"{loc}: {r} not in allowed list for {cls}")
    return issues
for n, c in CONFIGS.items():
    iss = check(n, c)
    print(f"{n:12s} [{c.get('data_class')}] ->", "PASS" if not iss else "FAIL")
    for i in iss: print("    -", i)
