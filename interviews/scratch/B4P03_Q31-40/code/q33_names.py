"""Q33: list the pod names, PVC names and DNS names a StatefulSet will create. Reads the manifest, no cluster."""
import pathlib, sys, yaml

def plan(sts, ns="default"):
    name = sts["metadata"]["name"]; n = sts["spec"]["replicas"]; svc = sts["spec"]["serviceName"]
    vcts = [v["metadata"]["name"] for v in sts["spec"].get("volumeClaimTemplates", [])]
    rows = []
    for i in range(n):
        pod = f"{name}-{i}"
        rows.append((pod, [f"{v}-{pod}" for v in vcts], f"{pod}.{svc}.{ns}.svc.cluster.local"))
    return rows

path = pathlib.Path(__file__).resolve().parent / "q33_statefulset.yaml"
sts = next(d for d in yaml.safe_load_all(path.read_text()) if d["kind"] == "StatefulSet")
for replicas in (sts["spec"]["replicas"], 5):
    sts["spec"]["replicas"] = replicas
    print(f"replicas={replicas}")
    for pod, pvcs, dns in plan(sts):
        print(f"  {pod:8} pvc={','.join(pvcs):14} dns={dns}")
print("start order: 0 -> 1 -> 2 (OrderedReady); stop order: reverse. PVCs are NOT deleted on scale-down by default.")
