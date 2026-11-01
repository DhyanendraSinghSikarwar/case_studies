"""Q24: ordered checklist over a config dict. Pure Python, no Google call. Facts hedged: check current docs."""
import ipaddress

def checklist(c: dict) -> list[tuple[int, str, str]]:
    out = []
    def chk(name, ok, hint): out.append((len(out) + 1, name, "PASS" if ok else "FAIL: " + hint))
    chk("Vertex AI API and Storage API enabled in the project", c["apis_enabled"], "enable the APIs")
    chk("job service account has roles on bucket, image repo, project", c["sa_roles_ok"], "fix IAM first: perimeter is the second wall, not the first")
    chk("project perimeter membership matches the intent", c["project_in_perimeter"] == c["perimeter_expected"], "add project to perimeter (or confirm it is meant to be outside)")
    chk("restricted services include aiplatform and storage consistently", c["services_restricted"], "check the restricted-services list")
    chk("job has a network attachment (PSC interface) when data-plane egress is needed", c["network_attachment"], "create attachment, pass it in the job spec")
    ok_subnet = False
    if c["network_attachment"]:
        ok_subnet = ipaddress.ip_network(c["attachment_subnet"]).prefixlen <= 28   # docs recommend /28 or larger, check current docs
    chk("attachment subnet has room (docs recommend /28; check current docs)", ok_subnet or not c["network_attachment"], "subnet too small")
    chk("DNS resolves googleapis.com names to the restricted VIP", c["restricted_vip_dns"], "add private DNS zone for restricted.googleapis.com")
    chk("no step needs the public internet (pip install, git clone, external API)", not c["needs_internet"], "mirror packages in Artifact Registry or allow egress through a controlled proxy")
    chk("images and data live in-perimeter, or an ingress/egress rule names this identity", c["data_in_perimeter"] or c["egress_rule_for_sa"], "add an egress rule for the job service account and the bucket project")
    chk("denials checked in audit logs (dry-run mode first)", c["audit_logs_read"], "read the VPC-SC violation entries")
    return out

dev = dict(apis_enabled=True, sa_roles_ok=True, project_in_perimeter=False, services_restricted=False, network_attachment=False,
           attachment_subnet="10.0.0.0/24", restricted_vip_dns=False, needs_internet=True, data_in_perimeter=True,
           egress_rule_for_sa=False, audit_logs_read=False, perimeter_expected=False)
prod = dict(dev, perimeter_expected=True, project_in_perimeter=True, services_restricted=True, network_attachment=True, attachment_subnet="10.9.0.0/29",
            restricted_vip_dns=False, data_in_perimeter=False)

def run(cfg):
    rows = checklist(cfg)
    if not cfg["project_in_perimeter"]:       # outside a perimeter, checks 4-10 are not enforced
        rows = rows[:3]
    return rows

for name, cfg in (("dev project (outside perimeter)", dev), ("prod project (inside perimeter)", prod)):
    rows = run(cfg)
    print("==", name, "->", "first failure: #%d" % next((r[0] for r in rows if r[2] != "PASS"), 0) if any(r[2] != "PASS" for r in rows) else "all checks pass")
    for n, what, res in rows: print(f" {n:2d}. {what}: {res}")
