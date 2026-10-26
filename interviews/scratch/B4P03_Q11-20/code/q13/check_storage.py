"""Cross-check PVCs, StorageClasses and the pods that use them. Offline, pure Python."""
import sys, yaml

def load(path):
    return [d for d in yaml.safe_load_all(open(path)) if d]

def main(path):
    docs = load(path)
    classes = {d["metadata"]["name"] for d in docs if d["kind"] == "StorageClass"}
    pvcs = {d["metadata"]["name"]: d for d in docs if d["kind"] == "PersistentVolumeClaim"}
    findings = []
    for name, pvc in pvcs.items():
        sc = pvc["spec"].get("storageClassName")
        if sc is None:
            findings.append(f"PVC {name}: no storageClassName -> uses the cluster default class, if one exists")
        elif sc not in classes:
            findings.append(f"PVC {name}: class {sc!r} not defined here -> stays Pending unless the cluster has it")
    for d in docs:
        if d["kind"] != "Deployment":
            continue
        replicas = d["spec"].get("replicas", 1)
        pod = d["spec"]["template"]["spec"]
        for v in pod.get("volumes", []):
            if "persistentVolumeClaim" in v:
                claim = v["persistentVolumeClaim"]["claimName"]
                if claim not in pvcs:
                    findings.append(f"Deployment {d['metadata']['name']}: claim {claim!r} does not exist -> pod Pending")
                    continue
                modes = pvcs[claim]["spec"]["accessModes"]
                if replicas > 1 and modes == ["ReadWriteOnce"]:
                    findings.append(f"Deployment {d['metadata']['name']}: {replicas} replicas share RWO claim {claim!r} -> only pods on ONE node can mount it")
                if replicas > 1 and "ReadWriteOnce" not in modes and not v["persistentVolumeClaim"].get("readOnly") and "ReadWriteMany" not in modes:
                    findings.append(f"Deployment {d['metadata']['name']}: claim {claim!r} is {modes} but mounted writable")
            if "emptyDir" in v and "sizeLimit" not in v["emptyDir"]:
                findings.append(f"emptyDir {v['name']}: no sizeLimit -> can fill the node disk")
    for sc in (d for d in docs if d["kind"] == "StorageClass"):
        print(f"StorageClass {sc['metadata']['name']}: reclaimPolicy={sc.get('reclaimPolicy', 'Delete')}, binding={sc.get('volumeBindingMode', 'Immediate')}")
    print(f"{len(findings)} finding(s)")
    for f in findings:
        print(" -", f)

main(sys.argv[1])
