"""Q23: Workspace with managed network + checker, offline. Nothing is created."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import Workspace, ManagedNetwork, IsolationMode, FqdnDestination, PrivateEndpointDestination
print("azure-ai-ml", md.version("azure-ai-ml"))
mn = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND, outbound_rules=[
    FqdnDestination(name="pypi", destination="pypi.org"),
    PrivateEndpointDestination(name="pe-storage", service_resource_id="/subscriptions/0000/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/stdemo", subresource_target="blob", spark_enabled=False)])
ws = Workspace(name="ws-secure", location="centralindia", public_network_access="Disabled", managed_network=mn)
print(type(ws).__name__, ws.location, "public:", ws.public_network_access, "| mode:", ws.managed_network.isolation_mode,
      "| rules:", [(r.name, type(r).__name__) for r in ws.managed_network.outbound_rules])

def check_network(cfg: dict) -> list[str]:
    f = []
    if cfg.get("public_network_access") != "Disabled": f.append("workspace public_network_access is not Disabled")
    if not cfg.get("private_endpoint_inbound"): f.append("no private endpoint for inbound access to the workspace")
    mode = cfg.get("isolation_mode")
    if mode == "disabled": f.append("managed network off: outbound is uncontrolled")
    if mode == "allow_internet_outbound": f.append("internet outbound allowed: exfiltration path open (ok only with a written reason)")
    for dep in ("storage", "key_vault", "container_registry"):
        if dep not in cfg.get("private_endpoint_outbound", []): f.append(f"no outbound private endpoint rule for {dep}")
    for ep in cfg.get("online_endpoints", []):
        if ep.get("public_network_access") != "disabled": f.append(f"endpoint {ep['name']} is public")
    if not cfg.get("deployer_can_create_private_endpoints"): f.append("deployer lacks RBAC to create private endpoints (managed network creation fails)")
    return f

good = {"public_network_access": "Disabled", "private_endpoint_inbound": True, "isolation_mode": "allow_only_approved_outbound",
        "private_endpoint_outbound": ["storage", "key_vault", "container_registry"],
        "online_endpoints": [{"name": "fraud-ep", "public_network_access": "disabled"}], "deployer_can_create_private_endpoints": True}
bad = {"public_network_access": "Enabled", "isolation_mode": "allow_internet_outbound", "private_endpoint_outbound": ["storage"],
       "online_endpoints": [{"name": "fraud-ep", "public_network_access": "enabled"}]}
for n, c in (("good", good), ("bad", bad)):
    r = check_network(c); print(n, "->", "OK" if not r else ""); [print("   -", x) for x in r]
