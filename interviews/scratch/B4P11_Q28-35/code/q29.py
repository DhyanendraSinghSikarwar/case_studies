# q29.py - ordered permission-failure checks for a job that cannot read its dataset (both clouds). Pure Python.
# The scenarios are made-up facts a human would collect from logs and the portal; nothing here was read from a real cloud.
ORDER = ["identity", "binding", "network", "region", "credential", "policy"]

def diagnose(s):
    """Return (check, advice) for the FIRST failing check, or ('none', ...)."""
    cloud = s["cloud"]
    # 1. Which identity does the job REALLY run as?
    if s["intended_identity"] != s["effective_identity"]:
        who = ("user-assigned vs system-assigned vs the submitting user's identity" if cloud == "azure"
               else "job service account vs the default compute service account")
        return "identity", f"job runs as {s['effective_identity']!r}, not {s['intended_identity']!r} ({who}); fix the job's identity setting"
    # 2. Role / IAM binding at the right scope (and the right data-plane role)
    need = s["needed_role"]
    if need not in s["roles_on_data_scope"]:
        return "binding", f"{s['effective_identity']!r} lacks {need!r} on {s['data_scope']!r}; a role on the workspace/project or on the control plane does not cover data access"
    # 3. Private networking between the compute and the storage
    if s["storage_public_access"] == "disabled" and not s["private_path_to_storage"]:
        return "network", "storage blocks public access and the job's compute has no private endpoint / PSC / managed-network rule to it"
    # 4. Region mismatch (latency, residency policy, or a service that must be in-region)
    if s["compute_region"] != s["data_region"] and s["same_region_required"]:
        return "region", f"compute in {s['compute_region']} but data in {s['data_region']}; policy or setup needs them together"
    # 5. Expired or missing credential (token, key, SAS, ADC)
    if s["credential_expired"]:
        return "credential", "token / SAS / key expired or was revoked; re-issue and prefer identity-based access to long-lived keys"
    # 6. Policy or perimeter denial that overrides an allow
    if s["policy_denial"]:
        return "policy", f"explicit deny from {s['policy_denial']}; read the denial text, an allow cannot beat it"
    return "none", "all six checks pass; look at the file path, object name, and the training code itself"

SCENARIOS = [
  dict(name="A azure wrong identity", cloud="azure", intended_identity="uami-train", effective_identity="user:dev@corp",
       needed_role="Storage Blob Data Reader", data_scope="storageacct/container", roles_on_data_scope=["Storage Blob Data Reader"],
       storage_public_access="enabled", private_path_to_storage=False, compute_region="centralindia", data_region="centralindia",
       same_region_required=False, credential_expired=False, policy_denial=None),
  dict(name="B azure role on wrong scope", cloud="azure", intended_identity="uami-train", effective_identity="uami-train",
       needed_role="Storage Blob Data Reader", data_scope="storageacct/container", roles_on_data_scope=["Contributor"],
       storage_public_access="enabled", private_path_to_storage=False, compute_region="centralindia", data_region="centralindia",
       same_region_required=False, credential_expired=False, policy_denial=None),
  dict(name="C vertex private storage", cloud="gcp", intended_identity="sa-train@proj", effective_identity="sa-train@proj",
       needed_role="roles/storage.objectViewer", data_scope="bucket", roles_on_data_scope=["roles/storage.objectViewer"],
       storage_public_access="disabled", private_path_to_storage=False, compute_region="asia-south1", data_region="asia-south1",
       same_region_required=False, credential_expired=False, policy_denial=None),
  dict(name="D vertex perimeter deny", cloud="gcp", intended_identity="sa-train@proj", effective_identity="sa-train@proj",
       needed_role="roles/storage.objectViewer", data_scope="bucket", roles_on_data_scope=["roles/storage.objectViewer"],
       storage_public_access="enabled", private_path_to_storage=True, compute_region="asia-south1", data_region="asia-south1",
       same_region_required=False, credential_expired=False, policy_denial="VPC Service Controls perimeter"),
]
if __name__ == "__main__":
    for s in SCENARIOS:
        c, adv = diagnose(s)
        print(f"{s['name']:30s} -> check={c:10s} {adv}")
    # ordering matters: a scenario with two faults reports the earlier one
    both = dict(SCENARIOS[1], credential_expired=True)
    print("two faults (binding + expired) ->", diagnose(both)[0])
    ok = dict(SCENARIOS[0], effective_identity="uami-train")
    print("healthy ->", diagnose(ok)[0])
