"""Q37: each ServiceAccount carries the identity annotation its cloud expects; the manifests are placeholders (fake account ids)."""
import pathlib, yaml
EXPECT = {"trainer-eks": "eks.amazonaws.com/role-arn", "trainer-gke": "iam.gke.io/gcp-service-account", "trainer-aks": "azure.workload.identity/client-id"}
for d in yaml.safe_load_all((pathlib.Path(__file__).resolve().parent / "q37_sa.yaml").read_text()):
    name = d["metadata"]["name"]; key = EXPECT[name]
    print(f"{name:12} {key:34} {'present' if key in d['metadata'].get('annotations', {}) else 'MISSING'}")
