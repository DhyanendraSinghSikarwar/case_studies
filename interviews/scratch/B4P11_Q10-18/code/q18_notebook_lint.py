"""Lint a notebook-instance config. The YAML shape is MY simplified schema, not an Azure or Google file format.
Azure side maps to ComputeInstance fields; Vertex side maps to Workbench instance settings (check current docs)."""
import sys, yaml
BROAD = {"Owner", "Contributor", "roles/owner", "roles/editor"}
GPU_HINT = ("nc", "nd", "nv", "a100", "t4", "v100", "h100", "l4", "a2-", "g2-", "a3-")

def lint(c):
    f = []
    idle = c.get("idle_shutdown_minutes")
    if not idle:
        f.append("no idle shutdown")
    elif idle > 120:
        f.append(f"idle shutdown {idle} min is long (policy max 120)")
    if c.get("public_ip", False):
        f.append("public IP enabled")
    if c.get("ssh_public_access", False):
        f.append("SSH open to internet")
    ident = c.get("identity", {})
    if not ident.get("principal"):
        f.append("no dedicated identity (falls back to default/user)")
    for r in ident.get("roles", []):
        if r in BROAD:
            f.append(f"broad role {r}")
    shape = str(c.get("machine", "")).lower()
    if any(h in shape for h in GPU_HINT) and c.get("gpu_count", 0) > 1 and c.get("schedule_stop") is None:
        f.append(f"{c['gpu_count']}-GPU machine with no scheduled stop")
    if not c.get("owner_label"):
        f.append("no owner label (cannot tell whose it is)")
    return f

try:   # optional: the real Azure entity carries the same knobs (offline object, nothing created)
    import warnings; warnings.filterwarnings("ignore")
    from azure.ai.ml.entities import ComputeInstance
    ci = ComputeInstance(name="ci-alice", size="Standard_DS3_v2", idle_time_before_shutdown_minutes=60,
                         enable_node_public_ip=False, ssh_public_access_enabled=False)
    print("ComputeInstance:", ci.name, ci.size, "idle_min:", ci.idle_time_before_shutdown_minutes,
          "node_public_ip:", ci.enable_node_public_ip, "ssh_public:", ci.ssh_public_access_enabled)
except ImportError:
    print("azure-ai-ml not installed here: ComputeInstance demo skipped")
bad_rc = 0
for doc in yaml.safe_load_all(open(sys.argv[1])):
    out = lint(doc)
    print(f"{doc['name']:22s} {doc['cloud']:7s}", "PASS" if not out else "FAIL: " + "; ".join(out))
    bad_rc |= bool(out)
sys.exit(bad_rc)
