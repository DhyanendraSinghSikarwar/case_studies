"""Gate: fail on CRITICAL, or HIGH that has a fix, unless waived with an unexpired waiver."""
import json, sys
from datetime import date

report, waivers_file, today = sys.argv[1], sys.argv[2], date.fromisoformat(sys.argv[3])
waivers = {w["id"]: w for w in json.load(open(waivers_file))}
blocking, notes = [], []
for res in json.load(open(report))["Results"]:
    for v in res.get("Vulnerabilities", []):
        sev, fixed, vid = v["Severity"], v.get("FixedVersion", ""), v["VulnerabilityID"]
        violates = sev == "CRITICAL" or (sev == "HIGH" and fixed)
        if not violates:
            notes.append(f"{vid} {sev} {v['PkgName']}: allowed ({'no fix yet' if sev=='HIGH' else 'below threshold'})")
            continue
        w = waivers.get(vid)
        if w and date.fromisoformat(w["expires"]) >= today:
            notes.append(f"{vid} {sev} {v['PkgName']}: WAIVED until {w['expires']} by {w['owner']} ({w['reason']})")
        else:
            why = "waiver EXPIRED" if w else "no waiver"
            blocking.append(f"{vid} {sev} {v['PkgName']} fix={fixed or '-'} [{why}]")
print("BLOCKING:"); [print("  " + b) for b in blocking]
print("OK / waived:"); [print("  " + n) for n in notes]
print("RESULT:", "FAIL" if blocking else "PASS")
sys.exit(1 if blocking else 0)
