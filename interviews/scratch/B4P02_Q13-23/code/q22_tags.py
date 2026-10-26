# Q22: build a tag set for one image, validate tag syntax, print the (not executed) docker commands, and show why 'latest' breaks rollback.
import re, datetime as dt
TAG_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$")     # Docker tag grammar (check current docs)

def tags(app_ver, git_sha, model_name, model_ver, run_id, built, channel=None):
    t = [f"{app_ver}",                                   # human release, moves nothing once pushed
         f"{app_ver}-g{git_sha[:7]}",                    # exact code
         f"sha-{git_sha[:12]}",                          # CI convenience, unique per commit
         f"{app_ver}-{model_name}-m{model_ver}",         # which registry model version is inside / configured
         f"{built:%Y%m%d}-m{model_ver}"]                 # date for humans and retention rules
    if channel: t.append(channel)                        # moving pointer: staging / prod. NEVER the only tag
    return t

built = dt.date(2026, 10, 26)
ts = tags("1.14.0", "9f3c2a1b7d4e5f60", "churn", 23, "run-8841", built, channel="staging")
for t in ts: print(f"{t:32} valid={bool(TAG_RE.match(t))}")
bad = ["churn:v1", "my tag", "-lead", "x" * 129]
print("invalid examples:", [(b[:12], bool(TAG_RE.match(b))) for b in bad])

img, reg = "churn-api", "registry.example.com/ml"
print("\n# NOT EXECUTED (no registry, no daemon):")
print(f"docker build -t {reg}/{img}:{ts[1]} --label org.opencontainers.image.revision=9f3c2a1b7d4e5f60 --label ml.model.version=23 --label ml.run.id=run-8841 .")
for t in ts[:1] + ts[2:]: print(f"docker tag {reg}/{img}:{ts[1]} {reg}/{img}:{t}")
print(f"docker push --all-tags {reg}/{img}")

# latest vs immutable-by-convention: a registry as a dict tag -> digest
reg_state = {"latest": "sha256:aaa1", "1.13.0": "sha256:aaa1"}
reg_state["latest"] = "sha256:bbb2"; reg_state["1.14.0"] = "sha256:bbb2"       # a release moves latest
print("\nafter release 1.14.0, 'latest' ->", reg_state["latest"], "| what was running before? unknown unless you recorded the digest")
print("rollback by tag 1.13.0 ->", reg_state["1.13.0"], "(still there)")
