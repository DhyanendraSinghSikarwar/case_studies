"""Q37: TEACHING MODEL of an OCI-style image layout. Not a real docker image.
Run: python3 -I oci_toy.py"""
import gzip, hashlib, io, json, os, tarfile, tempfile

def sha(b): return "sha256:" + hashlib.sha256(b).hexdigest()

def make_layer(files):
    """A layer = tar of files. Fixed mtime/owner so the same files give the same bytes."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as t:
        for name, data in sorted(files.items()):
            ti = tarfile.TarInfo(name); ti.size = len(data); ti.mtime = 0
            ti.uid = ti.gid = 0; ti.uname = ti.gname = ""
            t.addfile(ti, io.BytesIO(data))
    return buf.getvalue()

def gz(b):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", mtime=0) as g: g.write(b)
    return out.getvalue()

def write_blob(root, data):
    d = sha(data); path = os.path.join(root, "blobs", "sha256", d.split(":")[1])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(data); return d, len(data)

def build(root, layer_files_list, cmd):
    layers, diff_ids, history = [], [], []
    for files, created_by in layer_files_list:
        raw = make_layer(files); packed = gz(raw)
        d, n = write_blob(root, packed)
        layers.append({"mediaType": "application/vnd.oci.image.layer.v1.tar+gzip", "digest": d, "size": n})
        diff_ids.append(sha(raw))                      # diff_id = hash of UNcompressed tar
        history.append({"created_by": created_by})
    config = {"architecture": "amd64", "os": "linux", "config": {"Cmd": cmd},
              "rootfs": {"type": "layers", "diff_ids": diff_ids}, "history": history}
    cd, cn = write_blob(root, json.dumps(config, sort_keys=True).encode())
    manifest = {"schemaVersion": 2, "mediaType": "application/vnd.oci.image.manifest.v1+json",
                "config": {"mediaType": "application/vnd.oci.image.config.v1+json", "digest": cd, "size": cn},
                "layers": layers}
    md, mn = write_blob(root, json.dumps(manifest, sort_keys=True).encode())
    json.dump({"schemaVersion": 2, "manifests": [{"mediaType": manifest["mediaType"], "digest": md, "size": mn}]},
              open(os.path.join(root, "index.json"), "w"))
    json.dump({"imageLayoutVersion": "1.0.0"}, open(os.path.join(root, "oci-layout"), "w"))
    return md

def verify(root):
    ok = True
    for fn in os.listdir(os.path.join(root, "blobs", "sha256")):
        data = open(os.path.join(root, "blobs", "sha256", fn), "rb").read()
        good = hashlib.sha256(data).hexdigest() == fn
        ok &= good
    idx = json.load(open(os.path.join(root, "index.json")))
    mdig = idx["manifests"][0]["digest"].split(":")[1]
    man = json.load(open(os.path.join(root, "blobs", "sha256", mdig)))
    cfg = json.load(open(os.path.join(root, "blobs", "sha256", man["config"]["digest"].split(":")[1])))
    for layer, diff in zip(man["layers"], cfg["rootfs"]["diff_ids"]):
        try:
            raw = gzip.decompress(open(os.path.join(root, "blobs", "sha256", layer["digest"].split(":")[1]), "rb").read())
            ok &= sha(raw) == diff
        except (OSError, EOFError):                    # corrupt gzip counts as a failed check
            ok = False
    return ok, man, cfg

base = ({"etc/os-release": b"toy-linux 1\n", "usr/lib/libc.so": b"libc"}, "FROM toy-linux")
deps = ({"app/site-packages/numpy.py": b"# numpy"}, "RUN pip install numpy")
v1 = ({"app/main.py": b"print('v1')\n"}, "COPY main.py /app")
v2 = ({"app/main.py": b"print('v2')\n"}, "COPY main.py /app")

tmp = tempfile.mkdtemp()
a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
ma = build(a, [base, deps, v1], ["python", "/app/main.py"])
mb = build(b, [base, deps, v2], ["python", "/app/main.py"])
ok, man, cfg = verify(a)
print("image A verifies:", ok, "| image B verifies:", verify(b)[1] is not None and verify(b)[0])
print("manifest digests differ:", ma != mb)
la = [l["digest"][7:19] for l in man["layers"]]
lb = [l["digest"][7:19] for l in json.load(open(os.path.join(b, "blobs/sha256", mb[7:])))["layers"]]
print("layers A:", la); print("layers B:", lb)
print("shared layers:", [x for x in la if x in lb])
print("history from config:", [h["created_by"] for h in cfg["history"]])
# tamper test
blob = os.path.join(a, "blobs", "sha256", man["layers"][0]["digest"][7:])
open(blob, "ab").write(b"x")
print("after flipping one byte in a layer blob, verifies:", verify(a)[0])
