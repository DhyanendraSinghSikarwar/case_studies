import pathlib, subprocess, sys, tempfile, yaml

def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout

# 1. parse the manifests
app = yaml.safe_load(open(sys.argv[1]))
auto = app["spec"]["syncPolicy"]["automated"]
print("Application:", app["metadata"]["name"], "| path:", app["spec"]["source"]["path"],
      "| prune:", auto["prune"], "| selfHeal:", auto["selfHeal"])
flux = yaml.safe_load(open(sys.argv[2]))
print("Flux Kustomization:", flux["metadata"]["name"], "| interval:", flux["spec"]["interval"])

# 2. the CI "bump PR" step on a temp config repo
def bump(values_path, digest, model_version):
    v = yaml.safe_load(values_path.read_text())
    v["image"]["digest"] = digest
    v["model"]["version"] = model_version
    values_path.write_text(yaml.safe_dump(v, sort_keys=False))

with tempfile.TemporaryDirectory() as d:
    repo = pathlib.Path(d)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "ci@example.com"); git(repo, "config", "user.name", "ci-bot")
    vp = repo / "values.yaml"
    vp.write_text(yaml.safe_dump({"image": {"repository": "ghcr.io/example-org/churn-serving", "digest": "sha256:aaaa1111"},
                                  "model": {"name": "churn", "version": 4}}, sort_keys=False))
    git(repo, "add", "."); git(repo, "commit", "-qm", "initial: model 4")
    bump(vp, "sha256:bbbb2222", 5)
    print("--- git diff after the bump script ---")
    print(git(repo, "diff"))
    git(repo, "commit", "-qam", "deploy: churn model 5")
    git(repo, "revert", "--no-edit", "HEAD")
    print("--- after git revert (the rollback) ---")
    print(vp.read_text())
    print(git(repo, "log", "--oneline"))
