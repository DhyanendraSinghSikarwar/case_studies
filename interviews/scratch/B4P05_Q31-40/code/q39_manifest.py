import hashlib, json, os, subprocess, sys, tempfile

def git_sha(repo):
    return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()

def make_manifest(run_date, snapshot_id, params, repo, image):
    if snapshot_id == "latest" or "@sha256:" not in image:
        raise ValueError("pin the snapshot id and use an image digest, not 'latest' or a moving tag")
    m = {"run_date": run_date, "snapshot_id": snapshot_id, "git_sha": git_sha(repo),
         "params": params, "image": image}
    m["manifest_id"] = hashlib.sha256(json.dumps(m, sort_keys=True).encode()).hexdigest()[:12]
    return m

def pick_inputs(m):
    """Deterministic: files depend only on the snapshot and the run date, never on 'now'."""
    return [f"s3://lake/{m['snapshot_id']}/dt={m['run_date']}/part-{i:02d}.parquet" for i in range(3)]

if __name__ == "__main__":
    repo = tempfile.mkdtemp()
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(["git", "init", "-q", repo], check=True)
    subprocess.run(["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", "c1"], check=True, env=env)
    img = "registry.example.com/ml/train@sha256:" + "ab" * 32
    a = make_manifest("2026-10-01", "snap-0042", {"lr": 0.1}, repo, img)
    b = make_manifest("2026-10-01", "snap-0042", {"lr": 0.1}, repo, img)
    c = make_manifest("2026-10-01", "snap-0043", {"lr": 0.1}, repo, img)
    print(json.dumps(a, indent=1))
    print("same manifest, same inputs:", pick_inputs(a) == pick_inputs(b), "| same id:", a["manifest_id"] == b["manifest_id"])
    print("new snapshot, different inputs:", pick_inputs(a) != pick_inputs(c), "| ids:", a["manifest_id"], c["manifest_id"])
    try: make_manifest("2026-10-01", "latest", {}, repo, img)
    except ValueError as e: print("rejected:", e)
    try: make_manifest("2026-10-01", "snap-0042", {}, repo, "registry.example.com/ml/train:latest")
    except ValueError as e: print("rejected:", e)
