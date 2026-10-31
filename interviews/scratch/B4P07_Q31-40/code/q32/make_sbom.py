"""Minimal CycloneDX-style SBOM from pinned requirements + SHA-256 of a model file."""
import hashlib, json, pathlib, sys

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def sbom(req_file, model_file):
    comps = []
    for line in pathlib.Path(req_file).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, version = line.split("==")
        comps.append({"type": "library", "name": name, "version": version,
                      "purl": f"pkg:pypi/{name}@{version}"})
    comps.append({"type": "machine-learning-model", "name": pathlib.Path(model_file).name,
                  "hashes": [{"alg": "SHA-256", "content": sha256(model_file)}]})
    return {"bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1, "components": comps}

if __name__ == "__main__":
    doc = sbom(sys.argv[1], sys.argv[2])
    print(json.dumps(doc, indent=2))
    print("component count:", len(doc["components"]))
    before = sha256(sys.argv[2])
    pathlib.Path(sys.argv[2]).write_bytes(b"model-weights-v1 TAMPERED")
    after = sha256(sys.argv[2])
    print("hash changed after tamper:", before != after)
