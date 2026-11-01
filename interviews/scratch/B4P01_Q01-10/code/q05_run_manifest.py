"""Q5: write a run manifest as JSON. Run: python3 -I q05_run_manifest.py"""
import hashlib, json, os, platform, random, subprocess, sys, tempfile
from importlib import metadata

def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()

def git_state(repo="."):
    def run(*a):
        return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout.strip()
    commit = run("rev-parse", "HEAD")
    dirty = bool(run("status", "--porcelain"))      # uncommitted changes make the commit hash a lie
    return {"commit": commit or None, "dirty": dirty}

def write_manifest(path, *, repo, config, seed, data_files, model_file, metrics, packages):
    manifest = {
        "git": git_state(repo),
        "config": config,                                   # hyperparameters
        "seed": seed,
        "data": {os.path.basename(p): sha256_file(p) for p in data_files},   # data version = content hash
        "packages": {p: metadata.version(p) for p in packages},             # lockfile hash also worth storing
        "hardware": {"python": sys.version.split()[0], "os": platform.platform(),
                     "machine": platform.machine(), "gpu": "none (this demo)"},
        "metrics": metrics,
        "model_sha256": sha256_file(model_file),
    }
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    return manifest

if __name__ == "__main__":
    import numpy as np
    tmp = tempfile.mkdtemp()
    repo = os.path.join(tmp, "repo"); os.makedirs(repo)
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_AUTHOR_NAME="d", GIT_AUTHOR_EMAIL="d@e.x",
               GIT_COMMITTER_NAME="d", GIT_COMMITTER_EMAIL="d@e.x", GIT_AUTHOR_DATE="1760000000 +0000", GIT_COMMITTER_DATE="1760000000 +0000")
    for cmd in (["init", "-q", "-b", "main"], ["commit", "-q", "--allow-empty", "-m", "init"]):
        subprocess.run(["git", "-C", repo, *cmd], check=True, env=env)
    seed = 42
    random.seed(seed); rng = np.random.default_rng(seed)
    data = os.path.join(tmp, "train.csv"); model = os.path.join(tmp, "model.bin")
    open(data, "w").write("x,y\n1,2\n3,4\n")
    open(model, "wb").write(rng.random(4).tobytes())     # stand-in for a trained model
    m = write_manifest(os.path.join(tmp, "run.json"), repo=repo, config={"lr": 0.1, "max_depth": 4}, seed=seed,
                       data_files=[data], model_file=model, metrics={"auc": 0.91}, packages=["numpy"])
    m["hardware"]["os"] = "<os string>"                  # keep the printed output short and portable
    print(json.dumps(m, indent=2, sort_keys=True))
    # same seed -> same bytes -> same hash: a hand-checkable reproducibility test
    again = np.random.default_rng(seed).random(4).tobytes()
    print("model bytes identical on rerun with same seed:", hashlib.sha256(again).hexdigest() == m["model_sha256"])
