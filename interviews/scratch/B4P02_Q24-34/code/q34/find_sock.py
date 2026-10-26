import sys, yaml
for path in sys.argv[1:]:
    doc = yaml.safe_load(open(path))
    hits = [v["name"] for v in doc["spec"].get("volumes", [])
            if "docker.sock" in str(v.get("hostPath", {}).get("path", ""))]
    print(f"{path}: {'FOUND docker.sock hostPath in volume ' + str(hits) if hits else 'no docker.sock mount'}")
