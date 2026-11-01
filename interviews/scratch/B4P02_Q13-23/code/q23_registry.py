# Q23: (1) parse image references the way the docker CLI normalises them, (2) simulate a retention policy and layer-shared storage.
import re

def parse(ref):
    digest = None
    if "@" in ref: ref, digest = ref.split("@", 1)
    first, _, rest = ref.partition("/")
    if rest and ("." in first or ":" in first or first == "localhost"): reg, path = first, rest
    else: reg, path = "docker.io", ref                      # default registry (Docker Hub)
    if reg == "docker.io" and "/" not in path: path = "library/" + path   # official images
    tag = None
    if ":" in path.rsplit("/", 1)[-1]: path, tag = path.rsplit(":", 1)
    if tag is None and digest is None: tag = "latest"
    return reg, path, tag, digest

for r in ["python:3.12-slim", "myorg/trainer:1.4.0", "ghcr.io/myorg/api:sha-9f3c2a1",
          "123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/api:1.0", "localhost:5000/ml/api",
          "python@sha256:" + "ab" * 32]:
    reg, path, tag, dg = parse(r); print(f"{r[:30]:30} -> registry={reg:34} repo={path:16} tag={tag} digest={'yes' if dg else '-'}")

# Retention: keep tags in use + newest N release tags; untagged manifests expire. Sizes are layer MB (toy numbers).
layers = {"base": 2000, "deps": 5000, "app1": 20, "app2": 20, "app3": 20, "app4": 20, "model_v1": 1500, "model_v2": 1500}
images = {  # tag -> layers, newest last
    "1.10.0": ["base", "deps", "app1"], "1.11.0": ["base", "deps", "app2"],
    "1.12.0": ["base", "deps", "app3", "model_v1"], "1.13.0": ["base", "deps", "app4", "model_v2"]}
def stored(tags): return sum(layers[l] for l in {l for t in tags for l in images[t]})
naive = sum(layers[l] for t in images for l in images[t])
print(f"\nsum of image sizes (no sharing): {naive} MB | stored with layer sharing: {stored(images)} MB")
in_use = {"1.12.0", "1.13.0"}; keep_new = 3
keep = in_use | set(list(images)[-keep_new:])
print("keep:", sorted(keep), "| delete:", sorted(set(images) - keep), "| stored after cleanup:", stored(keep), "MB")
print("lesson: a changed base or deps layer breaks sharing, so every rebuild then costs the full", layers["base"] + layers["deps"], "MB again")
