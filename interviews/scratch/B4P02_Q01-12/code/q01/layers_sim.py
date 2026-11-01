"""Toy model of image layers + container writable layer (union view)."""
import hashlib, json

def digest(files):
    return "sha256:" + hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()[:12]

# image = ordered, read-only layers; each layer is {path: content or None (None = whiteout/delete)}
image = [
    {"/app/model.pkl": "v1", "/app/serve.py": "code-v1"},   # layer 1
    {"/app/config.yaml": "threshold=0.5"},                  # layer 2
]
image_ids = [digest(l) for l in image]

def view(layers):
    fs = {}
    for layer in layers:                 # upper layers win
        for p, c in layer.items():
            if c is None: fs.pop(p, None)
            else: fs[p] = c
    return fs

class Container:
    def __init__(self, image):
        self.image = image               # shared, never modified
        self.upper = {}                  # private writable layer
    def write(self, path, content): self.upper[path] = content
    def delete(self, path): self.upper[path] = None
    def fs(self): return view(self.image + [self.upper])
    def diff(self):                      # what `docker diff` reports: A / C / D
        base = view(self.image); out = []
        for p, c in sorted(self.upper.items()):
            if c is None: out.append(f"D {p}")
            elif p in base: out.append(f"C {p}")
            else: out.append(f"A {p}")
        return out

c1, c2 = Container(image), Container(image)
c1.write("/app/model.pkl", "v2-retrained")      # change model inside container 1
c1.write("/tmp/pred.log", "42 rows")
c1.delete("/app/config.yaml")
print("c1 sees model:", c1.fs()["/app/model.pkl"])
print("c2 sees model:", c2.fs()["/app/model.pkl"], "(same image, own writable layer)")
print("docker diff c1:", c1.diff())
print("image layer ids unchanged:", image_ids == [digest(l) for l in image])

# docker rm c1 -> writable layer is thrown away; docker run again -> fresh container
c1 = Container(image)
print("after rm + run again, model:", c1.fs()["/app/model.pkl"])

# docker commit: freezes the upper layer into a NEW layer (new image); no recipe, not reviewable
c3 = Container(image); c3.write("/app/model.pkl", "v2-retrained")
new_image = image + [c3.upper]
print("commit -> layers:", len(image), "->", len(new_image), "| new top layer:", c3.upper)
