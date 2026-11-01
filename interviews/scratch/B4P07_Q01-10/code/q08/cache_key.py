import hashlib, pathlib, tempfile
def hash_files(paths):
    """hashFiles-style: sha256 of each file, then sha256 of the joined digests (sorted by path)."""
    outer = hashlib.sha256()
    for p in sorted(paths):
        outer.update(hashlib.sha256(pathlib.Path(p).read_bytes()).digest())
    return outer.hexdigest()
def key(os_name, paths):
    return f"pip-{os_name}-{hash_files(paths)[:12]}"

d = pathlib.Path(tempfile.mkdtemp(prefix="b7q08_", dir="/tmp/claude-0/b7_q01_10"))
req = d / "requirements.txt"
req.write_text("scikit-learn==1.5.2\nnumpy==2.0.2\npandas==2.2.3\n")
k1 = key("Linux", [req]); print("run 1      :", k1)
print("run 2 same :", key("Linux", [req]), "(hit)")
req.write_text("scikit-learn==1.5.2\nnumpy==2.0.2\npandas==2.2.3  \n")
print("whitespace :", key("Linux", [req]), "(miss: any byte change is a new key)")
req.write_text("scikit-learn==1.6.0\nnumpy==2.0.2\npandas==2.2.3\n")
k2 = key("Linux", [req]); print("pin bumped :", k2, "(miss -> fresh install)")
print("changed    :", k1 != k2)
print("stale key  : pip-Linux-v1 never changes -> old wheels forever")
print("noisy key  : pip-Linux-<run_id> changes every run -> never hits")
