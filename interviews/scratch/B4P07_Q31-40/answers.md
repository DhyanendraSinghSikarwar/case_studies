# Book 4 Part 7, Q31-Q40 answers (Wave B)

### Q31 ⭐ 🔴 Supply-chain security for ML CI. Explain why tags are mutable (the March 2025 tj-actions/changed-files compromise rewrote tags, so pinning to a tag did not help while a full commit SHA did), pinning third-party actions to SHAs and updating them with Dependabot or Renovate, least-privilege permissions, pull_request_target, dependency pinning with hashes, and loading pickled models from untrusted places. Write a scanner script that flags uses: lines not pinned to a 40-character SHA and workflows without a permissions block, run it on a good and a bad sample tree and show the output.
**Asked at:** Actions supply-chain incident reports (orca.security, wiz.io, infoworld.com, phoenix.security, securityboulevard.com on the March 2025 tj-actions/changed-files compromise CVE-2025-30066; search snippets only, not opened; nothing found on SBOM or provenance attestations); security vendor posts, not interview reports; DevSecOps, platform and MLOps roles | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** A tag like `@v4` can be moved by whoever controls that repo, so I pin every third-party action to a full 40-character commit SHA, give each workflow the least permissions it needs, never run untrusted PR code with secrets, and never unpickle a model I did not produce.

**Then explain:**
- **Tags are mutable, SHAs are not.** In the March 2025 tj-actions/changed-files compromise (CVE-2025-30066, per incident write-ups; I read search snippets, not the advisory itself) the attacker repointed existing version tags to malicious code. Anyone on `@v45` pulled it on the next run. People pinned to a SHA were safe unless they updated to a bad SHA during the window.
- **Pinning needs upkeep.** A SHA never updates by itself. Let Dependabot or Renovate open PRs that bump the SHA (keep the version in a trailing comment so humans can read it). Review the diff of the action, not just the number.
- **Permissions and triggers.** Set `permissions: contents: read` at the top, and widen per job only where needed (`id-token: write`, `packages: write`). `pull_request_target` runs with the base repo's secrets and a writable token, so never check out the PR head code in it. If a job needs both, split it into two workflows.
- **Dependencies.** Pin Python deps in a lock file and install with `pip install --require-hashes`, so a swapped package fails the hash check. The same idea applies to base images (use a digest).
- **ML-specific: pickle.** Loading a pickle runs code. A model file from a bucket, a hub or a PR artifact can own the CI runner. Prefer formats that hold only tensors (safetensors, ONNX), verify a SHA-256 against the registry, and for torch check the current `weights_only` behaviour in the docs.
- **Failure modes.** The scanner below is a lint, not a guarantee. It cannot see a SHA that is itself malicious, a compromised dependency inside a pinned action, or a `run:` step that downloads and executes a script. actionlint does not flag any of these either (shown below).

**Example:** `uses: tj-actions/changed-files@v45` means "run whatever that tag points to today". `uses: actions/checkout@<40 hex chars> # v4.2.2` means "run exactly this commit". If the maintainer's account is hijacked tomorrow, the first changes under you and the second does not.

**Code:** scanner (flags non-SHA `uses:`, missing `permissions`, `pull_request_target`, unhashed `pip install`), sample workflows, and a harmless pickle demo. The SHAs in the good sample are examples I recalled from the checkout and setup-python releases, not verified here; always copy a SHA from the action's own releases page.
```python
# --- file: scan_workflows.py ---

"""Flag unpinned third-party actions, missing permissions, risky triggers, unhashed pip installs."""
import pathlib, re, sys
import yaml

SHA = re.compile(r"^[0-9a-f]{40}$")

def triggers(doc):
    on = doc.get("on", doc.get(True))      # YAML 1.1: the key `on` loads as True
    if isinstance(on, str):
        return [on]
    return list(on) if on else []

def scan_file(path):
    problems = []
    doc = yaml.safe_load(path.read_text())
    if "permissions" not in doc:
        jobs_without = [n for n, j in doc["jobs"].items() if "permissions" not in j]
        if jobs_without:
            problems.append(f"no permissions block (top level or job: {', '.join(jobs_without)})")
    if "pull_request_target" in triggers(doc):
        problems.append("trigger pull_request_target: never check out PR head code with it")
    for jname, job in doc["jobs"].items():
        for i, step in enumerate(job.get("steps", []), 1):
            uses = step.get("uses")
            if uses and not uses.startswith("./"):
                ref = uses.split("@", 1)[1] if "@" in uses else ""
                if not SHA.match(ref):
                    problems.append(f"{jname} step {i}: '{uses}' not pinned to a 40-char SHA")
            run = step.get("run", "")
            if "pip install" in run and "--require-hashes" not in run and " -e " not in run:
                problems.append(f"{jname} step {i}: pip install without --require-hashes")
    return problems

def main(root):
    bad = 0
    for f in sorted(pathlib.Path(root).glob(".github/workflows/*.y*ml")):
        problems = scan_file(f)
        print(f"{f.relative_to(root)}: {'OK' if not problems else str(len(problems)) + ' problem(s)'}")
        for p in problems:
            print("  -", p)
        bad += len(problems)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

# --- file: pickle_demo.py ---

"""Harmless demo: unpickling runs code. Never pickle.load a model you did not produce."""
import pickle

class Evil:
    def __reduce__(self):                 # a real attacker would return (os.system, ("...",))
        return (print, ("code ran during pickle.loads",))

blob = pickle.dumps(Evil())
pickle.loads(blob)
```
```yaml
# --- file: good/.github/workflows/ci.yml ---

name: ci
on:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5.3.0
        with:
          python-version: "3.12"
      - run: pip install --require-hashes -r requirements.lock
      - run: pytest -q

# --- file: bad/.github/workflows/ci.yml ---

name: ci
on:
  pull_request_target:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - uses: tj-actions/changed-files@v45
      - uses: some-org/ml-helper@main
      - uses: ./.github/actions/local-setup
      - run: pip install -r requirements.txt
      - run: pytest -q
```
```bash
python -I scan_workflows.py good
python -I scan_workflows.py bad
actionlint bad/.github/workflows/ci.yml
```

**Output (my run):** real run of `run_all.sh` (PyYAML 6.0.3, actionlint 1.7.12 via actionlint-py, Python 3.13). The scanner finds all six problems in the bad tree. actionlint says nothing about the bad file: it checks syntax and expression types, not supply-chain policy. Not executed: Dependabot, Renovate, a real hash-checked install, any action fetch.
```text
== scan good
.github/workflows/ci.yml: OK
exit=0
== scan bad
.github/workflows/ci.yml: 6 problem(s)
  - no permissions block (top level or job: test)
  - trigger pull_request_target: never check out PR head code with it
  - test step 1: 'actions/checkout@v4' not pinned to a 40-char SHA
  - test step 2: 'tj-actions/changed-files@v45' not pinned to a 40-char SHA
  - test step 3: 'some-org/ml-helper@main' not pinned to a 40-char SHA
  - test step 5: pip install without --require-hashes
exit=1
== pickle demo
code ran during pickle.loads
== actionlint on the bad file
exit=0
== actionlint on the good file
exit=0
```

**Follow-ups:**
- *Does SHA pinning solve it?* No. It stops silent tag moves. You still review what you pin, and a pinned action can pull unpinned dependencies.
- *Why Dependabot if you pin?* A pin that is never updated misses security fixes. Bots make the update a reviewed PR.
- *How do you make CI safer for fork PRs?* Plain `pull_request` (no secrets), read-only token, and a maintainer-approved second workflow for anything that needs secrets.

**Common mistakes:**
- Pinning to `@v4` or `@main` and calling it pinned.
- Using `pull_request_target` and checking out `github.event.pull_request.head.sha`.
- No `permissions` block, so the token gets the repository default.
- `pickle.load` or `joblib.load` on a file from an untrusted bucket or PR artifact.


### Q32 ⭐ 🔴 SBOM, signing and provenance for a model image at concept level. Explain what an SBOM is (SPDX or CycloneDX, a list of components), what a signature proves (who built it) versus what provenance proves (how and from which commit), keyless signing with cosign using the OIDC identity, build provenance attestations and SLSA levels (hedge, check current docs), verifying at deploy time with an admission policy, and what changes for models (signing weights, hash of the model file). Generate a minimal CycloneDX-style JSON from pip freeze with Python and compute a SHA-256 of a model file, run them and show the output. cosign, Syft, Trivy and an admission controller are not executed.
**Asked at:** Actions supply-chain incident reports (orca.security, wiz.io, infoworld.com, phoenix.security, securityboulevard.com on the March 2025 tj-actions/changed-files compromise CVE-2025-30066; search snippets only, not opened; nothing found on SBOM or provenance attestations); security vendor posts, not interview reports; DevSecOps, platform and MLOps roles | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** An SBOM lists what is inside the image, a signature proves who produced it, provenance proves how and from which commit it was built, and the cluster should verify all that at deploy time before it runs the image.

**Then explain:**
- **SBOM** (software bill of materials): a machine-readable component list, in SPDX or CycloneDX. It answers "are we affected by this new CVE?" without unpacking images. Tools like Syft generate it from an image (concept here, not run). A list made only from your lock file misses OS packages in the base image.
- **Signature vs provenance.** A signature says "this exact digest was signed by identity X". Provenance (an in-toto or SLSA-style attestation) says "built by workflow W from commit C with these inputs". A signature alone does not tell you the build was clean; provenance alone is useless if nobody checks it.
- **Keyless signing with cosign.** The job uses its GitHub OIDC token (`id-token: write`) to get a short-lived certificate tied to the workflow identity, so there is no long-lived signing key to leak. The signing event goes to a public transparency log. Check current Sigstore docs for details.
- **SLSA levels.** A graded scale for build integrity. Names and requirements change between versions, so I say "we aim for provenance from a hosted, isolated build" and check the current spec for the level.
- **Verify at deploy.** An admission policy (Kyverno, Sigstore policy-controller, Gatekeeper, at concept level) rejects images that lack a valid signature from the expected workflow identity. Verify by digest, never by tag.
- **For models.** Hash the weights file (SHA-256), store the hash in the registry and in the SBOM as a component (CycloneDX has a machine-learning-model component type; check the spec version), and sign the artifact or the image that bundles it. A changed hash means a changed model.
- **Failure modes.** A signature on a bad image still verifies. The identity regexp in the verify step must be tight (org, repo, workflow, tag), or any workflow in your org passes. Signing a mutable tag signs nothing useful.

**Example:** Pin a lock file of three packages and a 16-byte model file `model-weights-v1`. The SBOM has 4 components. `sha256sum model.bin` and the Python hash agree (6903dfbd...). Change one byte and the hash changes, so the deploy check would fail.

**Code:** Python builds the CycloneDX-style JSON from a pinned requirements file (the `pip freeze` format) and hashes the model; the workflow shows signing, attesting and verifying with cosign.
```python
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
```
```yaml
name: sign-model-image
on:
  push:
    tags: ["model-v*"]
permissions:
  contents: read
jobs:
  sign:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write        # keyless signing needs the OIDC token
      attestations: write    # build provenance attestation
    env:
      IMAGE: ghcr.io/example-org/churn-serving
      DIGEST: ${{ vars.IMAGE_DIGEST }}   # in a real job: output of the build job
    steps:
      - uses: sigstore/cosign-installer@v3        # pin to a SHA in real use
      - name: Sign image by digest (keyless)
        run: cosign sign --yes "$IMAGE@$DIGEST"
      - name: Attach SBOM as attestation
        run: cosign attest --yes --type cyclonedx --predicate sbom.json "$IMAGE@$DIGEST"
      - name: Verify as the deploy side would
        run: >
          cosign verify "$IMAGE@$DIGEST"
          --certificate-identity-regexp "^https://github.com/example-org/.+/.github/workflows/.+@refs/tags/model-v.+$"
          --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
```bash
printf 'model-weights-v1' > model.bin
python -I make_sbom.py requirements.lock model.bin
sha256sum model.bin
actionlint sign.yml
check-jsonschema --builtin-schema vendor.github-workflows sign.yml
```

**Output (my run):** the SBOM script, `sha256sum` cross-check, actionlint and the schema check ran. I used a small pinned file, not a live `pip freeze` of an environment, so the output stays hand-checkable. Not executed: cosign, Syft, Trivy (none installed, shown in the last lines), Rekor, SLSA verification, any admission controller, any registry push. The cosign flags are from memory of the docs; check current docs.
```text
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "components": [
    {
      "type": "library",
      "name": "numpy",
      "version": "2.5.4",
      "purl": "pkg:pypi/numpy@2.5.4"
    },
    {
      "type": "library",
      "name": "scikit-learn",
      "version": "1.9.1",
      "purl": "pkg:pypi/scikit-learn@1.9.1"
    },
    {
      "type": "library",
      "name": "fastapi",
      "version": "0.115.0",
      "purl": "pkg:pypi/fastapi@0.115.0"
    },
    {
      "type": "machine-learning-model",
      "name": "model.bin",
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "6903dfbdfe04273eedd148c9cfd6053c7960caa17d0166ac75fde62c8ea6292d"
        }
      ]
    }
  ]
}
component count: 4
hash changed after tamper: True
== sha256sum on the untouched file
6903dfbdfe04273eedd148c9cfd6053c7960caa17d0166ac75fde62c8ea6292d  model.bin
== actionlint sign.yml
exit=0
== check-jsonschema
ok -- validation done
cosign: not installed
syft: not installed
trivy: not installed
```

**Follow-ups:**
- *Is CycloneDX output from a requirements file a real SBOM?* It is a minimal one. Production SBOMs come from scanning the image, which also catches OS packages.
- *Why digest and not tag?* A tag can point to a different image tomorrow. A digest is the content.
- *Does signing stop a malicious insider?* Not alone. It narrows who can produce a deployable image; review and branch rules still matter.

**Common mistakes:**
- Saying "we scan, so we sign".
- Verifying that an image is signed but not by whom.
- Signing tags, not digests.
- Generating the SBOM once and never attaching it to the release.


### Q33 ⭐ 🔴 GitOps for model deployment with Argo CD or Flux at concept level. Explain the pull model (a controller in the cluster syncs the cluster to a Git repo) versus a CI job that runs kubectl apply, an Argo CD Application manifest (repoURL, path, destination, syncPolicy), automated sync, prune and self-heal, Flux's controllers and Kustomization, a separate config repo, a CI job that opens a PR bumping the image digest or model version in values.yaml, and rollback as git revert. Parse an Application manifest with pyyaml, then in a temp git repository bump a values file by script, show the git diff and revert it as a rollback. Argo CD and Flux were not executed. Part 3 owns Kubernetes and Helm.
**Asked at:** GitOps comparison posts (devtron.ai, codefresh.io, earthly.dev, harness.io, oneuptime.com 2026 Argo CD versus Flux; search snippets only, not opened); vendor and editorial blogs, nothing found on ML-specific GitOps or interview lists; platform and DevOps roles with ML workloads | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** In GitOps a controller inside the cluster keeps pulling a config repo and makes the cluster match it, so a deploy is a merged PR that bumps an image digest or model version, and a rollback is a `git revert`.

**Then explain:**
- **Pull vs push.** Push: a CI job holds cluster credentials and runs `kubectl apply`. Pull: the controller (Argo CD or Flux) lives in the cluster and reads Git, so CI never holds production cluster credentials, and the repo is the audit log.
- **Argo CD `Application`.** Fields to know: `source.repoURL`, `targetRevision`, `path`, `destination` (cluster and namespace), and `syncPolicy.automated` with `prune` (delete what is no longer in Git) and `selfHeal` (undo manual `kubectl edit` drift). Without `automated`, someone clicks Sync.
- **Flux.** Controllers (source, kustomize, helm, notification) and CRDs: a `GitRepository` source plus a `Kustomization` with `interval`, `path`, `prune`. Lighter, CLI-first, no built-in UI (per the comparison posts I saw; I did not open them, check current docs).
- **Separate config repo.** App code CI builds and pushes the image, then opens a PR to the config repo that edits `values.yaml` (digest, model version). Environments are folders or overlays. Approvals are normal PR reviews.
- **Rollback.** `git revert` the bump commit; the controller syncs the old digest and version. It only works if the old image and old model artifact still exist.
- **Failure modes.** Serving that loads `models:/name@champion` can change without a Git commit, which breaks "Git is the truth". For GitOps, pin a version number in Git. Also: self-heal fighting an autoscaler (ignore replica diffs), prune deleting something you meant to keep, a controller stuck on a bad manifest, and secrets in Git (use sealed or external secrets).

**Example:** values.yaml says digest `aaaa1111`, model 4. CI opens a PR changing it to `bbbb2222`, model 5. Merge, the controller rolls it out. Problem found: revert that one commit, and the file is back to model 4.

**Code:** the Argo CD `Application`, a Flux `Kustomization`, and the CI workflow that edits the config repo are shown as YAML. The Python parses both manifests, then in a temp git repo bumps a values file, prints the diff and reverts the commit.
```yaml
# --- file: application.yaml ---

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: churn-serving-prod
  namespace: argocd
spec:
  project: ml-serving
  source:
    repoURL: https://github.com/example-org/ml-deploy-config.git
    targetRevision: main
    path: apps/churn-serving/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: churn
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

# --- file: flux.yaml ---

apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: churn-serving-prod
  namespace: flux-system
spec:
  interval: 5m
  path: ./apps/churn-serving/overlays/prod
  prune: true
  sourceRef:
    kind: GitRepository
    name: ml-deploy-config

# --- file: bump-config.yml ---

name: bump-deploy-config
on:
  workflow_dispatch:
    inputs:
      digest:
        description: image digest, e.g. sha256:...
        required: true
      model_version:
        description: registry model version
        required: true
permissions:
  contents: read
jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          repository: example-org/ml-deploy-config
          token: ${{ secrets.CONFIG_REPO_TOKEN }}   # narrow token for the config repo only
      - name: Edit values and open a PR
        env:
          DIGEST: ${{ inputs.digest }}
          MODEL_VERSION: ${{ inputs.model_version }}
          GH_TOKEN: ${{ secrets.CONFIG_REPO_TOKEN }}
        run: |
          python scripts/bump_values.py values.yaml "$DIGEST" "$MODEL_VERSION"
          git switch -c "bump-model-$MODEL_VERSION"
          git commit -am "deploy: churn model $MODEL_VERSION"
          git push origin HEAD
          gh pr create --fill
```
```python
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
```
```bash
python -I gitops_demo.py application.yaml flux.yaml
actionlint bump-config.yml
```

**Output (my run):** manifests parse with PyYAML; the git diff and revert are real (git 2.43). The bump workflow passes actionlint. Argo CD and Flux were not executed (no cluster, no controllers) and I did not validate the manifests against the Argo CD or Flux CRD schemas, only that they parse as YAML. Commit hashes change on every run.
```text
Application: churn-serving-prod | path: apps/churn-serving/overlays/prod | prune: True | selfHeal: True
Flux Kustomization: churn-serving-prod | interval: 5m
--- git diff after the bump script ---
diff --git a/values.yaml b/values.yaml
index 3db1c26..76fa37e 100644
--- a/values.yaml
+++ b/values.yaml
@@ -1,6 +1,6 @@
 image:
   repository: ghcr.io/example-org/churn-serving
-  digest: sha256:aaaa1111
+  digest: sha256:bbbb2222
 model:
   name: churn
-  version: 4
+  version: 5

--- after git revert (the rollback) ---
image:
  repository: ghcr.io/example-org/churn-serving
  digest: sha256:aaaa1111
model:
  name: churn
  version: 4

73bdb75 Revert "deploy: churn model 5"
67c64e6 deploy: churn model 5
ba8a348 initial: model 4

== actionlint bump-config.yml
exit=0
```

**Follow-ups:**
- *Argo CD or Flux?* Argo CD if you want a UI, projects and SSO. Flux if you want a lighter, controller-and-CLI feel. Both work; pick what the platform team already runs.
- *Where does the model file go?* Not in Git. Git holds the version or digest; weights live in the registry or object store.
- *Canary?* Argo Rollouts or Flagger (concept; Part 6 and Part 3 own the mechanics).

**Common mistakes:**
- Keeping app code and cluster config in one repo, so every code commit triggers a deploy.
- Letting the serving layer resolve a mutable alias outside Git.
- `kubectl edit` in production with self-heal off, then wondering why Git and the cluster disagree.
- Rolling back Git but not checking that the old image is still in the registry.


### Q34 ⭐ 🔴 Design multi-environment promotion: dev, staging and production. Explain promoting the same immutable artifact (image digest and model version) through environments instead of rebuilding, per-environment config separate from the artifact, whether to keep one registry with aliases per environment (staging, champion) or a registry per environment with copy-on-promote, what evidence travels with the artifact (gate report, data version), data differences between environments, and drift between environments. Implement a promotion function with a ledger on a local sqlite MLflow registry that moves aliases staging then champion only in order, with pytest, and run it.
**Asked at:** Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** Build once, then move the same immutable artifact (image digest plus model version) through dev, staging and production in order, change only the per-environment config, and carry the evidence with it.

**Then explain:**
- **Same artifact, different config.** Rebuilding per environment means production runs something nobody tested. Config (endpoints, replicas, secrets, feature-store URL) lives outside the artifact, in per-environment files or overlays.
- **Registry layout, two options.** (1) One registry, aliases per environment (`staging`, `champion`): simple, one lineage, promotion is moving a pointer. (2) A registry per environment with copy-on-promote: stronger isolation and separate access rights (prod registry writable only by the release job), but copies must keep tags, hashes and lineage. MLflow has a copy call for this; check current docs. Regulated teams often choose (2) or (1) plus strict permissions.
- **Order is enforced in code.** `champion` is only reachable from a version that has been through `staging`. Skipping is refused. Re-running the same promotion is a no-op (idempotent), and every move is written to an append-only ledger.
- **Evidence travels.** Gate report URL, data version, git SHA, who approved. Without it, production has an artifact and no reason to trust it.
- **Failure modes.** Staging data is a sample, so staging proves the plumbing, not the quality. Drift between environments (different library version, different feature definition) makes a green staging meaningless. An alias moved by hand, outside the pipeline, breaks the ledger.

**Example:** versions 1 and 2 exist. Promoting 2 straight to `champion` is refused. Promote 1 to `staging`, then to `champion`; promote 2 to `staging` (champion stays 1); then 2 to `champion`. The ledger has four rows, with `previous` showing what each alias held before.

**Code:** `envpromo.py` is the function, then pytest cases, then a demo. (I hit a real bug while writing it: `get_model_version_by_alias(...).version` did not compare equal to my string version, so the "already there" check never fired and a re-run said `moved`. The `str()` in the code is the fix, and the idempotent test catches it.)
```python
# --- file: envpromo.py ---

"""Ordered promotion: a version must hold the staging alias before it can become champion."""
import json, pathlib, time
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

ORDER = ["staging", "champion"]

class PromotionError(Exception):
    pass

def _ledger(path, **row):
    row["ts"] = round(time.time(), 3)
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")

def promote(client, name, version, target, actor, ledger_path):
    version = str(version)
    if target not in ORDER:
        raise PromotionError(f"unknown environment {target!r}")
    try:
        mv = client.get_model_version(name, version)
    except MlflowException:
        raise PromotionError(f"version {version} of {name} does not exist")
    if target == "champion" and mv.tags.get("reached_staging") != "true":
        raise PromotionError(f"v{version} never reached staging; refusing to skip it")
    try:
        current = str(client.get_model_version_by_alias(name, target).version)
    except MlflowException:
        current = None
    if current == version:                      # idempotent re-run
        return "noop"
    client.set_registered_model_alias(name, target, version)
    if target == "staging":
        client.set_model_version_tag(name, version, "reached_staging", "true")
    client.set_model_version_tag(name, version, f"promoted_to_{target}_by", actor)
    _ledger(ledger_path, name=name, version=version, env=target, previous=current, actor=actor)
    return "moved"

# --- file: test_envpromo.py ---

import json, pytest
from mlflow import MlflowClient
from envpromo import promote, PromotionError

@pytest.fixture
def setup(tmp_path):
    uri = f"sqlite:///{tmp_path}/m.db"
    c = MlflowClient(tracking_uri=uri, registry_uri=uri)
    c.create_registered_model("churn")
    for _ in range(2):
        c.create_model_version("churn", source=str(tmp_path))
    return c, str(tmp_path / "ledger.jsonl")

def test_cannot_skip_staging(setup):
    c, led = setup
    with pytest.raises(PromotionError, match="never reached staging"):
        promote(c, "churn", 1, "champion", "ci", led)

def test_in_order_then_idempotent(setup):
    c, led = setup
    assert promote(c, "churn", 1, "staging", "ci", led) == "moved"
    assert promote(c, "churn", 1, "champion", "ci", led) == "moved"
    assert promote(c, "churn", 1, "champion", "ci", led) == "noop"
    rows = [json.loads(l) for l in open(led)]
    assert [(r["env"], r["version"]) for r in rows] == [("staging", "1"), ("champion", "1")]

def test_unknown_version_and_env(setup):
    c, led = setup
    with pytest.raises(PromotionError):
        promote(c, "churn", 9, "staging", "ci", led)
    with pytest.raises(PromotionError):
        promote(c, "churn", 1, "prod", "ci", led)

# --- file: demo.py ---

import os, sys, tempfile
sys.path.insert(0, os.getcwd())
from mlflow import MlflowClient
from envpromo import promote, PromotionError

d = tempfile.mkdtemp()
uri = f"sqlite:///{d}/m.db"; led = f"{d}/ledger.jsonl"
c = MlflowClient(tracking_uri=uri, registry_uri=uri)
c.create_registered_model("churn")
for _ in range(2):
    c.create_model_version("churn", source=d)
def alias(a):
    try: return c.get_model_version_by_alias("churn", a).version
    except Exception: return None
def show(tag): print(f"{tag:<28} staging={alias('staging')} champion={alias('champion')}")
show("start")
try: promote(c, "churn", 2, "champion", "dhyan", led)
except PromotionError as e: print("refused:", e)
print(promote(c, "churn", 1, "staging", "ci", led)); print(promote(c, "churn", 1, "champion", "ci", led)); show("v1 staging then champion")
print(promote(c, "churn", 2, "staging", "ci", led)); show("v2 in staging")
print(promote(c, "churn", 2, "champion", "ci", led)); show("v2 champion")
print(open(led).read().replace(d, "<tmp>"), end="")
```
```bash
export MLFLOW_DISABLE_TELEMETRY=true
python -I -m pytest -q -p no:cacheprovider test_envpromo.py
python -I demo.py
```

**Output (my run):** MLflow 3.17.2, local sqlite registry created in a temp directory, pytest 9.1.1. Timestamps replaced with `<t>`. Not executed: a remote tracking server, authentication, per-environment cloud accounts, a copy between two registries.
```text
== pytest
3 passed, 1 warning in 6.83s
== demo
start                        staging=None champion=None
refused: v2 never reached staging; refusing to skip it
moved
moved
v1 staging then champion     staging=1 champion=1
moved
v2 in staging                staging=2 champion=1
moved
v2 champion                  staging=2 champion=2
{"name": "churn", "version": "1", "env": "staging", "previous": null, "actor": "ci", "ts": <t>}
{"name": "churn", "version": "1", "env": "champion", "previous": null, "actor": "ci", "ts": <t>}
{"name": "churn", "version": "2", "env": "staging", "previous": "1", "actor": "ci", "ts": <t>}
{"name": "churn", "version": "2", "env": "champion", "previous": "1", "actor": "ci", "ts": <t>}
```

**Follow-ups:**
- *One registry or many?* One registry plus aliases is easier; many registries isolate access. Decide on who must be unable to write to production.
- *What about the data differences?* Staging gets a masked or sampled copy, so promote on the artifact's evidence plus a staging smoke test, and monitor in production.
- *Can staging skip for a hotfix?* Only through a documented break-glass path that still writes the ledger.

**Common mistakes:**
- Rebuilding the image in each environment.
- Baking environment config into the image or the model.
- Letting people move aliases by hand in the UI.
- No ledger, so nobody can say what production ran last Tuesday.


### Q35 ⭐ 🔴 Traceability from a GitHub Actions run to a production prediction. Explain recording GITHUB_SHA, GITHUB_RUN_ID, the workflow name, the data version and the image digest as tags on the registered model version, returning model_version in the API response, and answering 'which commit, which data, which run produced the model that scored this loan?' in one query. Write a script that simulates a CI run by setting those environment variables, logs the tags on a local sqlite MLflow registry, then looks the lineage up from a model version, and run it. Part 4 owns lineage mechanics; this is the CI wiring.
**Asked at:** Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** Stamp the git SHA, run id, workflow name, data version and image digest as tags on the registered model version at registration time, and make the API return `model_version`, so any prediction maps to its commit, data and run with one registry lookup.

**Then explain:**
- **The chain.** prediction log row -> `model_version` -> registry tags -> commit, workflow run URL (`github.com/<repo>/actions/runs/<run id>`), data version, image digest. The weakest link is a prediction store that did not save `model_version`.
- **What GitHub gives you.** The runner sets `GITHUB_SHA`, `GITHUB_RUN_ID`, `GITHUB_WORKFLOW` and `GITHUB_REPOSITORY` as environment variables. The data version and the image digest are not automatic; pass them in as env vars from earlier steps or repository variables.
- **Fail loudly.** If any lineage value is missing, the registration step exits non-zero. A version without lineage is not releasable.
- **MLflow also records source info** on runs it launches (for example a git commit tag when it can find a repo), but I do not rely on it in CI; explicit tags are clearer. Part 4 owns lineage mechanics; this is the wiring.
- **Failure modes.** Tags are mutable, so restrict who can edit them and keep the ledger too. Re-run attempts (`GITHUB_RUN_ATTEMPT`) share a run id, so add the attempt number if re-runs matter. Aliases pointing at the right version do not prove the tags are right.

**Example:** A loan is scored by `credit-risk` version 2. The response had `"model_version": "2"`. One lookup returns commit `ab12cd...`, run `9876543210`, data `data.20261001` and image `sha256:bbbb2222`. That answers the auditor in one query.

**Code:** the script simulates the CI run by setting environment variables, stamps tags on a sqlite registry, resolves lineage from the API response, and shows the refusal when a value is missing. The workflow shows where the values come from.
```python
"""Simulate a CI run stamping lineage on a model version, then answer 'who made the model that scored this loan?'."""
import os, tempfile
from mlflow import MlflowClient

LINEAGE_ENV = {"GITHUB_SHA": "git_sha", "GITHUB_RUN_ID": "gha_run_id", "GITHUB_WORKFLOW": "gha_workflow",
               "GITHUB_REPOSITORY": "gha_repo", "DATA_VERSION": "data_version", "IMAGE_DIGEST": "image_digest"}

def stamp(client, name, version):
    missing = [k for k in LINEAGE_ENV if not os.environ.get(k)]
    if missing:                                    # fail loudly: a version without lineage is not releasable
        raise SystemExit(f"missing lineage env vars: {missing}")
    for env_name, tag in LINEAGE_ENV.items():
        client.set_model_version_tag(name, version, tag, os.environ[env_name])

def lineage(client, name, version):
    return dict(client.get_model_version(name, str(version)).tags)

def predict(client, name, features):               # stand-in for the API: always return model_version
    v = client.get_model_version_by_alias(name, "champion").version
    return {"score": 0.37, "model_name": name, "model_version": str(v)}

d = tempfile.mkdtemp()
uri = f"sqlite:///{d}/m.db"
c = MlflowClient(tracking_uri=uri, registry_uri=uri)
c.create_registered_model("credit-risk")
c.create_model_version("credit-risk", source=d)
c.create_model_version("credit-risk", source=d)

# CI run for version 2 (values a workflow would get from the runner / earlier steps)
os.environ.update({"GITHUB_SHA": "ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12", "GITHUB_RUN_ID": "9876543210",
                   "GITHUB_WORKFLOW": "train-and-register", "GITHUB_REPOSITORY": "example-org/credit-risk",
                   "DATA_VERSION": "data.20261001", "IMAGE_DIGEST": "sha256:bbbb2222"})
stamp(c, "credit-risk", 2)
c.set_registered_model_alias("credit-risk", "champion", 2)

resp = predict(c, "credit-risk", {"income": 5})      # the loan scoring response stored with the decision
print("API response:", resp)
print("lineage of that version:")
for k, v in sorted(lineage(c, resp["model_name"], resp["model_version"]).items()):
    print(f"  {k:<14} {v}")

del os.environ["IMAGE_DIGEST"]
try:
    stamp(c, "credit-risk", 1)
except SystemExit as e:
    print("refused:", e)
```
```yaml
name: train-and-register
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      digest: ${{ steps.push.outputs.digest }}
    steps:
      - id: push
        run: echo "digest=sha256:placeholder" >> "$GITHUB_OUTPUT"   # real job: build-push-action output
  register:
    needs: build
    runs-on: ubuntu-latest
    env:
      MLFLOW_TRACKING_URI: ${{ vars.MLFLOW_TRACKING_URI }}
      DATA_VERSION: ${{ vars.DATA_VERSION }}
    steps:
      - uses: actions/checkout@v4
      - name: Train, register, stamp lineage
        env:
          IMAGE_DIGEST: ${{ needs.build.outputs.digest }}
        run: python scripts/register_and_stamp.py   # GITHUB_SHA, GITHUB_RUN_ID, GITHUB_WORKFLOW come from the runner
```
```bash
export MLFLOW_DISABLE_TELEMETRY=true
python -I trace_demo.py
actionlint trace.yml
```

**Output (my run):** real MLflow 3.17.2 on sqlite in a temp directory. The environment variables are set by my script, not by a GitHub runner, so nothing here proves what a real runner provides beyond the documented variable names. (actionlint also caught my first draft: it used `needs.build` without a `build` job.) Not executed: a real workflow run, a real build, a remote server.
```text
API response: {'score': 0.37, 'model_name': 'credit-risk', 'model_version': '2'}
lineage of that version:
  data_version   data.20261001
  gha_repo       example-org/credit-risk
  gha_run_id     9876543210
  gha_workflow   train-and-register
  git_sha        ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12
  image_digest   sha256:bbbb2222
refused: missing lineage env vars: ['IMAGE_DIGEST']
== actionlint trace.yml
exit=0
```

**Follow-ups:**
- *Where is the prediction-to-version link stored?* In the prediction log or response, next to the request id.
- *Can the tag say "approved by"?* Yes, that belongs to the approval-tags answer in this part; keep it in the same tag set.
- *What if the model is retrained with the same code?* Same SHA, different data version and run id, which is why you need all of them.

**Common mistakes:**
- Tagging the registry with only the git SHA, so data changes are invisible.
- Not logging `model_version` with the prediction.
- Relying on the alias name instead of the numeric version in logs (the alias moves).
- Letting registration succeed when lineage is incomplete.


### Q36 ⭐ 🔴 Flaky tests and non-determinism in ML CI. Explain sources (unseeded random state, thread or GPU non-determinism, floating-point order, time and network dependencies, test order), fixing with seeds and tolerances (pytest.approx, assertions on ranges and properties rather than exact values), statistical tests for stochastic behaviour, quarantining versus retrying, and measuring flakiness by repeated runs. Write one flaky test and its fixed version, run each 50 times in a loop and report the failure counts, and show a pytest marker for quarantine.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** A flaky ML test is almost always unseeded randomness or an exact-value assertion on a stochastic result, so I seed everything I can, assert ranges and properties with tolerances, test averages for truly random behaviour, and quarantine the rest while I fix it.

**Then explain:**
- **Sources.** Unseeded `random_state`, numpy or torch seeds, thread or GPU non-determinism (atomics, parallel reductions), floating-point summation order, tests that depend on the clock, the network, a shared file or test order, and tiny datasets where one sample moves the metric.
- **Fixes.** Seed at the entry point; use `pytest.approx` or `abs=` tolerances; assert properties ("loss falls", "output shape", "probabilities sum to 1", "score is between 0 and 1") instead of magic numbers; for randomness that is the point, average over N seeds and assert on the mean.
- **Quarantine, do not just retry.** A `quarantine` marker keeps the test out of the PR gate (`-m "not quarantine"`) but still runs it nightly, with an issue and an owner. Blind auto-retry hides real intermittent bugs.
- **Measure.** Run the test many times and count failures. A rate, not a feeling.
- **Failure modes.** A seed can hide a real bug that only shows on other data. Tolerances set so wide that nothing can fail are not tests. A quarantine list that only grows is a graveyard.

**Example:** The flaky test trains a logistic regression on freshly generated random data and asserts accuracy of at least 0.85. About a quarter of the time the random data is just harder and it fails. The fixed tests seed the data and assert a band, or average 20 seeds.

**Code:** `test_flaky.py` has the bad test, two fixed versions and a quarantined test; `conftest.py` registers the marker; `repeat.sh` runs one test N times in fresh processes and counts failures.
```python
# --- file: conftest.py ---

def pytest_configure(config):
    config.addinivalue_line("markers", "quarantine: known-flaky test, excluded from the PR gate (run nightly)")

# --- file: test_flaky.py ---

import numpy as np, pytest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def _accuracy(seed_data, seed_split):
    X, y = make_classification(n_samples=300, n_features=5, n_informative=3, class_sep=1.5,
                               random_state=seed_data)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed_split)
    return LogisticRegression().fit(Xtr, ytr).score(Xte, yte)

def test_flaky_exact_threshold():
    # BAD: nothing is seeded (None = fresh randomness each run) and the threshold is tight
    assert _accuracy(None, None) >= 0.85

def test_fixed_seeded_and_range():
    # GOOD 1: seeded, so the result is the same every run; assert a band, not a magic number
    acc = _accuracy(0, 0)
    assert 0.7 <= acc <= 1.0

def test_fixed_statistical():
    # GOOD 2: if randomness is the point, test the average over many seeds against a loose bound
    accs = [_accuracy(s, s) for s in range(20)]
    assert np.mean(accs) == pytest.approx(0.85, abs=0.1)

@pytest.mark.quarantine
def test_quarantined_example():
    assert _accuracy(None, None) >= 0.95   # known flaky, tracked in an issue, runs nightly only
```
```bash
python -I -m pytest -q -p no:cacheprovider test_flaky.py -m "not quarantine"   # the PR gate
python -I -m pytest -q -p no:cacheprovider test_flaky.py -m quarantine         # the nightly job
./repeat.sh test_flaky_exact_threshold 50
./repeat.sh test_fixed_seeded_and_range 50
./repeat.sh test_fixed_statistical 50
```

**Output (my run):** pytest 9.1.1, scikit-learn 1.9.1, each count is 50 fresh `pytest` processes. The 13 of 50 for the flaky test is one sample and will differ on yours (that is the point). The quarantined test failed in my one nightly-style run, which is why it is out of the PR gate. The loop took about five minutes, so I ran it once from a working copy with the same files, not inside `run_all.sh`.
```text
== PR gate: pytest -m "not quarantine"
3 passed, 1 deselected in 1.40s
== nightly: pytest -m quarantine (this run happened to fail; it is the known-flaky test)
FAILED test_flaky.py::test_quarantined_example - assert 0.9333333333333333 >=...
1 failed, 3 deselected in 1.17s
== repeat.sh, 50 fresh pytest processes each (took about 5 minutes)
test_flaky_exact_threshold: 13 failures in 50 runs
test_fixed_seeded_and_range: 0 failures in 50 runs
test_fixed_statistical: 0 failures in 50 runs
```

**Follow-ups:**
- *Why not just set `pytest-rerunfailures` to 3?* It makes the red go away, not the cause. Use it as a short-term bridge with a ticket.
- *GPU non-determinism?* Seed, enable deterministic algorithms where the framework supports it (check current docs), and compare with tolerances.
- *How do you decide a test is flaky and not a real regression?* It fails and passes on the same commit.

**Common mistakes:**
- `assert acc == 0.9137`.
- Seeding the split but not the model, or the reverse.
- Raising the tolerance until the test cannot fail.
- Quarantining with no owner and no deadline.


### Q37 ⭐ 🔴 CI for a monorepo with many models. Explain change detection with paths filters or a changed-files step, building a dynamic matrix from a job output with fromJSON so only changed models are tested, shared library changes that must test every model, and per-model versioning and tags (churn-v1.2.0). Write a script that maps changed file paths to a matrix JSON, show the workflow that consumes it, validate it with actionlint, and run the script on three sample change lists.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** One planning job turns the list of changed files into a matrix of affected models, the test job fans out over it with `fromJSON`, a change in shared code selects every model, and a single always-running summary job is the required check.

**Then explain:**
- **Change detection.** Either workflow `paths:` filters (cheap, but one workflow per model) or a step that runs `git diff --name-only origin/<base>...HEAD` and a script that maps paths to models. The script is testable; YAML filters are not.
- **Dynamic matrix.** The plan job writes `matrix=<json>` to `$GITHUB_OUTPUT`; the test job uses `strategy: matrix: ${{ fromJSON(needs.plan.outputs.matrix) }}`.
- **Shared code.** A change in `libs/`, `ci/`, `pyproject.toml` or a lock file triggers all models. If model B imports model A, the dependency map must say so.
- **Empty change.** A docs-only PR gives an empty `include`, and GitHub rejects an empty matrix (check current docs), so the plan job also outputs `any=true/false` and the test job is skipped when false. Then the required check must still go green: use an `all-green` job with `if: always()`.
- **Per-model versioning.** Tags like `churn-v1.2.0`; a release workflow on `tags: ["churn-v*"]` builds only that model. Needs `fetch-depth: 0` so the diff has history.
- **Failure modes.** Shallow clone makes `git diff` fail; renames show as delete plus add; matrix job names change per PR, so branch protection cannot require them directly (hence the summary job).

**Example:** Three changed-file lists in the run below. `models/churn/*` selects churn only. Mixed `fraud`, `ltv` and `docs/` selects those two. `libs/common/metrics.py` selects all three. `docs/index.md` alone selects none.

**Code:** mapper script (stdin to JSON) and the workflow that consumes it.
```python
"""Map changed file paths to a GitHub Actions matrix JSON for a monorepo of models."""
import json, sys

SHARED_PREFIXES = ("libs/", "ci/", "pyproject.toml", "requirements")   # a change here tests every model
ALL_MODELS = ["churn", "fraud", "ltv"]

def matrix(changed):
    hit = set()
    for p in changed:
        if p.startswith(SHARED_PREFIXES):
            return {"include": [{"model": m, "reason": "shared"} for m in ALL_MODELS]}
        parts = p.split("/")
        if parts[0] == "models" and len(parts) > 2 and parts[1] in ALL_MODELS:
            hit.add(parts[1])
    return {"include": [{"model": m, "reason": "changed"} for m in sorted(hit)]}

if __name__ == "__main__":
    changed = [l.strip() for l in sys.stdin if l.strip()]
    print(json.dumps(matrix(changed), separators=(",", ":")))
```
```yaml
name: monorepo-ci
on:
  pull_request:
permissions:
  contents: read
jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.m.outputs.matrix }}
      any: ${{ steps.m.outputs.any }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: m
        run: |
          git diff --name-only "origin/${{ github.base_ref }}...HEAD" > changed.txt
          MATRIX=$(python ci/changed_models.py < changed.txt)
          echo "matrix=$MATRIX" >> "$GITHUB_OUTPUT"
          echo "any=$(python -c 'import json,sys;print(str(bool(json.loads(sys.argv[1])["include"])).lower())' "$MATRIX")" >> "$GITHUB_OUTPUT"
  test:
    needs: plan
    if: needs.plan.outputs.any == 'true'
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix: ${{ fromJSON(needs.plan.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v4
      - run: pytest models/${{ matrix.model }} -q
  all-green:                      # one stable required check for branch protection
    needs: [plan, test]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: test "${{ needs.test.result }}" != "failure" && test "${{ needs.test.result }}" != "cancelled"
```
```bash
printf 'libs/common/metrics.py\nmodels/ltv/config.yaml\n' | python -I changed_models.py
actionlint monorepo.yml
check-jsonschema --builtin-schema vendor.github-workflows monorepo.yml
```

**Output (my run):** the mapper ran on four change lists with Python 3.13; actionlint and the schema check ran. Not executed: the workflow on GitHub (so `fromJSON`, the empty-matrix behaviour and the `all-green` logic are from docs and memory, not observed).
```text
--- changed files:
    models/churn/train.py
    models/churn/README.md
{"include":[{"model":"churn","reason":"changed"}]}
--- changed files:
    models/fraud/features.py
    models/ltv/config.yaml
    docs/index.md
{"include":[{"model":"fraud","reason":"changed"},{"model":"ltv","reason":"changed"}]}
--- changed files:
    libs/common/metrics.py
    models/ltv/config.yaml
{"include":[{"model":"churn","reason":"shared"},{"model":"fraud","reason":"shared"},{"model":"ltv","reason":"shared"}]}
--- changed files:
    docs/index.md
{"include":[]}
== actionlint monorepo.yml
exit=0
ok -- validation done
```

**Follow-ups:**
- *Why not one workflow per model?* Fine for 3 models; at 30 it is a maintenance burden and a branch-protection mess.
- *Test everything nightly?* Yes, a nightly full run catches missed dependencies in your map.
- *Tools?* Bazel, Nx or Pants do dependency-aware selection; I would mention them, not assume them.

**Common mistakes:**
- Forgetting shared code and shipping a broken model that was "not changed".
- Requiring matrix job names in branch protection.
- `fetch-depth: 1` with a diff-based planner.
- An empty matrix that fails the workflow on docs-only PRs.


### Q38 ⭐ 🔴 Design question: the CI/CD/CT system for a credit-risk model team in a regulated Indian bank or GCC, 30 data scientists, weekly retrains, audit requirements. Cover repositories, PR checks, data tests, scheduled training, registry and aliases, promotion gates with fairness and stability checks, environments with approvals, OIDC to the cloud, GitOps deploy, shadow then canary, rollback, audit trail, secrets, runner strategy and cost. Give a one-page whiteboard answer and a YAML skeleton of the main workflow, validate the YAML with actionlint, and state which parts are concept only. Part 12 owns system design in depth; check current RBI and other regulator guidance rather than quoting rules from memory.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** PRs run cheap checks on hosted runners, a Friday schedule retrains inside the bank's network, the model must pass a written gate (floor, champion, stability, fairness) before it gets a version alias, humans in the model-risk team approve production, the cloud is reached with OIDC, and the cluster deploys from Git, so every step leaves an audit record.

**Then explain (whiteboard, one page):**

| Area | Decision |
|---|---|
| Repos | One repo per model (code, gate policy YAML, workflows); one config repo for deploy manifests (GitOps); a shared reusable-workflow repo versioned by tag or SHA |
| PR checks | ruff, types, unit tests, data tests on a sample, 2-epoch smoke train, workflow lint, SHA-pinned actions, secret scan; required checks plus CODEOWNERS on gate thresholds and workflows |
| Scheduled training | Weekly cron (UTC) plus manual dispatch with a frozen data snapshot id; training on a runner inside the network, because data cannot leave |
| Registry | One registry, versions immutable, aliases `staging` and `champion`; tags hold git SHA, run id, data snapshot, gate report, approver |
| Gates | Absolute floor, no worse than champion, population-stability (PSI) on score and key features, fairness slices, latency and size budget, signature check; thresholds in Git, changed only by reviewed PR |
| Environments | `staging`, `shadow`, `production` GitHub environments; production needs reviewers from model risk who are not the author; branch restriction to main |
| Cloud access | OIDC with a trust policy pinned to repo and environment; no stored cloud keys |
| Deploy | CI opens a PR to the config repo bumping image digest and model version; Argo CD or Flux syncs (concept) |
| Rollout | Shadow (mirror, compare), canary at a small share, abort rules; labels arrive late so add a slower review after rollout |
| Rollback | Revert the config commit or move the alias back; previous image and artifact retained by policy |
| Audit | Immutable run logs, gate report artifacts, ledger of promotions, approvals from environment history; retention period by policy |
| Secrets | Environment-scoped, short-lived, none for forks; no data in logs |
| Runners | Hosted for PRs (no secrets); ephemeral self-hosted inside the network for training; never self-hosted on public repos |
| Cost | Path filters, smoke on PR and full on schedule, cancel-in-progress on PRs, idle runners scaled to zero |

- **Concept only here:** every cloud, cluster, approval and runner item. What ran is the lint of the skeleton below.
- **Regulation:** RBI and other regulator expectations on model risk, data localisation and audit are not quoted from memory; check current official guidance with the compliance team.
- **Failure modes:** a gate that cannot be edited without review but whose data can (check data tests too); one person holding both author and approver roles; a retrain that silently changes a feature definition.

**Example:** Friday 20:30 UTC the schedule fires. Data tests pass, the model trains, the gate compares it to the champion and checks fairness. It goes to `staging` (alias moves), then shadow and canary checks, then waits for two model-risk reviewers on `production`. After approval the alias moves and a PR to the config repo is opened; the controller deploys the pinned version.

**Code:** the skeleton of the main workflow. Python helper modules named in `run:` lines (`gates`, `promote`, `rollout_check`, `open_gitops_pr`) are placeholders, not written here.
```yaml
# --- file: weekly-retrain.yml ---

name: weekly-retrain-credit-risk
on:
  schedule:
    - cron: "30 20 * * 5"          # UTC; runs from the default branch only
  workflow_dispatch:
    inputs:
      data_version:
        description: frozen data snapshot id
        required: true
concurrency:
  group: credit-risk-release
  cancel-in-progress: false         # never cancel a half-finished promotion
permissions:
  contents: read
jobs:
  data-tests:
    runs-on: [self-hosted, linux, train]     # private runner inside the bank network (concept)
    steps:
      - uses: actions/checkout@v4
      - env:
          SNAPSHOT: ${{ inputs.data_version || vars.LATEST_SNAPSHOT }}
        run: python -m ci.data_tests --snapshot "$SNAPSHOT"
  train:
    needs: data-tests
    runs-on: [self-hosted, linux, train]
    outputs:
      version: ${{ steps.reg.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - env:
          SNAPSHOT: ${{ inputs.data_version || vars.LATEST_SNAPSHOT }}
        run: python -m train --snapshot "$SNAPSHOT"
      - id: reg
        run: python -m register --name credit-risk >> "$GITHUB_OUTPUT"
  gate:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Floor, champion regression, stability (PSI), fairness slices
        run: python -m gates --candidate "${{ needs.train.outputs.version }}" --policy policy/gates.yaml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: gate-report
          path: gate_report.json
  staging:
    needs: [train, gate]
    runs-on: ubuntu-latest
    environment: staging
    permissions:
      contents: read
      id-token: write                # OIDC to the cloud; no stored keys
    steps:
      - run: python -m promote --version "${{ needs.train.outputs.version }}" --alias staging
  shadow-canary:
    needs: [train, staging]
    runs-on: ubuntu-latest
    environment: shadow
    steps:
      - run: python -m rollout_check --version "${{ needs.train.outputs.version }}" --stages shadow,canary5
  production:
    needs: [train, shadow-canary]
    runs-on: ubuntu-latest
    environment: production           # required reviewers: model risk, not the author
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - run: python -m promote --version "${{ needs.train.outputs.version }}" --alias champion --require-approver
      - name: Open the GitOps PR (the cluster controller does the deploy)
        run: python -m open_gitops_pr --version "${{ needs.train.outputs.version }}"

# --- file: actionlint.yaml ---

self-hosted-runner:
  labels:
    - train
```
```bash
actionlint weekly-retrain.yml                              # fails: custom runner label 'train' unknown
actionlint -config-file actionlint.yaml weekly-retrain.yml # passes after declaring the label
check-jsonschema --builtin-schema vendor.github-workflows weekly-retrain.yml
```

**Output (my run):** actionlint 1.7.12 flags the self-hosted label until `actionlint.yaml` declares it (long label list trimmed in the paste); the vendored GitHub schema check passes. PyYAML shows the `on` key loaded as a boolean. Not executed: any job (no runner, no environment, no OIDC, no registry, no cluster).
```text
== actionlint, no config
weekly-retrain.yml:17:35: label "train" is unknown. available labels are "windows-latest", "windows-latest-8-c
   |
17 |     runs-on: [self-hosted, linux, train]     # private runner inside the bank network (concept)
   |                                   ^~~~~~
weekly-retrain.yml:25:35: label "train" is unknown. available labels are "windows-latest", "windows-latest-8-c
   |
25 |     runs-on: [self-hosted, linux, train]
   |                                   ^~~~~~
== actionlint with actionlint.yaml (label train declared)
exit=0
ok -- validation done
jobs: data-tests, train, gate, staging, shadow-canary, production
top-level key types: ['str', 'bool', 'str', 'str', 'str']
```

**Follow-ups:**
- *Why a separate config repo?* Deploy approvals and history stay apart from code churn, and the cluster controller watches only that repo.
- *Why weekly retrain and not drift-triggered?* A schedule is predictable for audit; drift alerts can open a manual dispatch.
- *Where is the human in the loop?* Environment approval on production, plus CODEOWNERS on the gate policy.

**Common mistakes:**
- Describing tools and no gates.
- Auto-deploying a retrain with no human on a credit model.
- Quoting regulator rules from memory.
- Forgetting the audit record (who approved, what evidence, which data).


### Q39 ⭐ 🔴 Scenario round: six CI/CD failures and the order you check them. (1) A scheduled retrain never fired. (2) The OIDC login says it cannot assume the role. (3) A PR from a fork fails because a secret is empty. (4) The required check stays pending after a docs-only change. (5) CI is green but the promoted model is worse in production. (6) Two promotions overlapped and the older model won. For each give the likely causes, the first command or setting to look at, and the fix. Implement the OIDC sub-claim mismatch diagnosis as a small Python function with tests and run it, and run actionlint on a workflow whose job is missing the permissions block that OIDC needs (show what actionlint does and does not catch).
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** For each failure I go from the cheapest, most mechanical check to the deepest: did the workflow even start, what does the log or the token actually say, then what does policy do on purpose, and only then the logic.

**Then explain (order of checks):**

| # | Symptom | Check first | Likely causes | Fix |
|---|---|---|---|---|
| 1 | Scheduled retrain never fired | Actions tab: is the workflow listed and enabled? Is the file on the default branch? | Cron is UTC; `schedule` only runs from the default branch; invalid YAML; Actions or the workflow disabled (a schedule can stop on inactive repos, check current docs); delays at busy times | Merge to default branch, re-enable, add `workflow_dispatch` as a manual fallback, alert on "no run in N days" |
| 2 | OIDC: cannot assume role | Workflow `permissions` for `id-token: write`, then the `sub` and `aud` in the token vs the trust policy | Missing `id-token: write`; job uses `environment:` so `sub` has the environment form; wrong repo or renamed repo; `aud` mismatch; wrong role ARN or region | Match the `sub` exactly (function below); fix permissions |
| 3 | Fork PR has an empty secret | Is the PR from a fork? | GitHub does not pass secrets to fork PRs (by design) | Run secret-free checks on forks; maintainers re-run trusted checks on a branch in the main repo; avoid `pull_request_target` with fork code |
| 4 | Required check pending after docs-only change | Does the workflow have a `paths` filter? | A path-filtered workflow never ran, so the required check never reports | Always-running summary job (see the branch-protection answer in this part) or no path filter on the required workflow |
| 5 | CI green, prod model worse | Gate report: which data, which slices; then training-serving skew | Gate set stale or leaked; offline metric is not the business metric; feature skew; no slice check; label delay | Fix the gate, compare shadow output, add monitoring (Part 8), roll back first |
| 6 | Overlapping promotions, older model won | Run timestamps and the promotion ledger | No `concurrency` group; promote step is not compare-and-set | `concurrency` with `cancel-in-progress: false`; refuse to move the alias to an older version |

- **Order inside a scenario:** reproduce or read first, change nothing; then the configuration that is cheapest to verify; then the code.
- **What actionlint does and does not catch:** it checks syntax, event names, `needs`, expression types and some injection patterns. It does **not** know that the OIDC login action needs `id-token: write`, so a deploy job with no `permissions` passes both actionlint and the schema (shown below). That mistake appears only at run time as the "cannot assume role" error.
- **Failure modes:** fixing the cloud trust to `*` to make it pass (an open door); retrying a schedule fix without a manual dispatch to prove it; blaming CI for a gate that was never testing the right thing.

**Example:** `repo:acme/churn:ref:refs/heads/main` against a trust that pins `repo:acme/churn:environment:production` is exactly the case where a job without `environment:` is rejected. The function below prints that reason in one line.

**Code:** `diagnose` compares `iss`, `aud` and `sub` to the trust and explains the likely shape of the mismatch; pytest covers match, ref token, environment form, pull-request token, wrong repo plus wrong audience; two workflows differ only in `permissions`.
```python
# --- file: oidc_diag.py ---

"""Explain why a cloud trust policy rejected a GitHub OIDC token, using sub/aud/iss only."""
from fnmatch import fnmatchcase

def sub_shape(sub):
    parts = sub.split(":")
    return parts[2] if len(parts) > 2 else "unknown"    # ref | environment | pull_request

def diagnose(claims, trust):
    """claims: decoded token claims. trust: {'sub': [patterns], 'aud': str, 'iss': str}. Returns list of findings."""
    findings = []
    if claims.get("iss") != trust["iss"]:
        findings.append(f"iss mismatch: token {claims.get('iss')!r} vs trust {trust['iss']!r}")
    if claims.get("aud") != trust["aud"]:
        findings.append(f"aud mismatch: token {claims.get('aud')!r} vs trust {trust['aud']!r} (check the audience input of the login action)")
    sub = claims["sub"]
    if not any(fnmatchcase(sub, p) for p in trust["sub"]):
        shape = sub_shape(sub)
        want_repo = trust["sub"][0].split(":")[1]
        got_repo = sub.split(":")[1]
        if got_repo != want_repo:
            findings.append(f"sub repo {got_repo!r} is not {want_repo!r} (renamed, moved or forked repo?)")
        elif shape == "environment":
            findings.append(f"sub {sub!r} uses the environment form; a job with `environment:` no longer sends ref:..., "
                            f"so a trust pinned to a branch will not match")
        elif shape == "pull_request":
            findings.append(f"sub {sub!r} is a pull_request token; trust only allows {trust['sub']} (usually correct: PRs should not assume deploy roles)")
        elif shape == "ref":
            findings.append(f"sub {sub!r} is a ref token for another branch or tag than the trust allows {trust['sub']}")
        else:
            findings.append(f"sub {sub!r} matches none of {trust['sub']}")
    return findings

# --- file: test_oidc_diag.py ---

from oidc_diag import diagnose

ISS = "https://token.actions.githubusercontent.com"
TRUST = {"sub": ["repo:acme/churn:environment:production"], "aud": "sts.amazonaws.com", "iss": ISS}

def claims(sub, aud="sts.amazonaws.com", iss=ISS):
    return {"sub": sub, "aud": aud, "iss": iss}

def test_match_gives_no_findings():
    assert diagnose(claims("repo:acme/churn:environment:production"), TRUST) == []

def test_branch_job_without_environment():
    f = diagnose(claims("repo:acme/churn:ref:refs/heads/main"), TRUST)
    assert len(f) == 1 and "ref token" in f[0]

def test_environment_mismatch_when_trust_pins_branch():
    trust = {**TRUST, "sub": ["repo:acme/churn:ref:refs/heads/main"]}
    f = diagnose(claims("repo:acme/churn:environment:production"), trust)
    assert "environment form" in f[0]

def test_pull_request_token():
    f = diagnose(claims("repo:acme/churn:pull_request"), TRUST)
    assert "pull_request token" in f[0]

def test_other_repo_and_wrong_audience():
    f = diagnose(claims("repo:acme/other:environment:production", aud="sts.example.com"), TRUST)
    assert any("aud mismatch" in x for x in f) and any("sub repo" in x for x in f)
```
```yaml
# --- file: no-permissions.yml ---

name: deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-deploy
          aws-region: ap-south-1
      - run: aws sts get-caller-identity

# --- file: with-permissions.yml ---

name: deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-deploy
          aws-region: ap-south-1
      - run: aws sts get-caller-identity
```
```bash
python -I -m pytest -q -p no:cacheprovider test_oidc_diag.py
actionlint no-permissions.yml; actionlint with-permissions.yml
check-jsonschema --builtin-schema vendor.github-workflows no-permissions.yml
```

**Output (my run):** the tests and both lint tools ran. Both workflows pass both tools, which is the point: the missing `id-token: write` is invisible to them. Not executed: a real OIDC token, a cloud trust policy, schedules, forks, branch protection, any real incident. The fork and schedule rows come from GitHub documentation as I know it; check current docs.
```text
== pytest
5 passed in 0.01s
== no-permissions.yml
actionlint exit=0
ok -- validation done
== with-permissions.yml
actionlint exit=0
ok -- validation done
== two live diagnoses
repo:acme/churn:ref:refs/heads/main
  -> sub 'repo:acme/churn:ref:refs/heads/main' is a ref token for another branch or tag than the trust allows ['repo:acme/churn:environment:production']
repo:acme/churn:pull_request
  -> sub 'repo:acme/churn:pull_request' is a pull_request token; trust only allows ['repo:acme/churn:environment:production'] (usually correct: PRs should not assume deploy roles)
```

**Follow-ups:**
- *OIDC works on main but not on a PR?* The PR token has a `pull_request` sub; that is usually correct, PRs should not assume deploy roles.
- *How do you see the real `sub`?* Decode the JWT in a debug step, or read the cloud's error and the token claims it echoes (never print the raw token in shared logs).
- *Scenario 5 first action?* Roll back, then investigate.

**Common mistakes:**
- Widening the trust policy to make it work.
- Debugging code before checking whether the workflow ran.
- Treating a green CI as proof of model quality.
- Believing actionlint verifies cloud permissions.


### Q40 ⭐ 🔴 CI/CD for an LLM application, kept to the CI side (Book 2 owns LLM internals and RAG). Explain versioning prompts and configs in Git, a golden evaluation set run on every PR, deterministic checks (format, schema, banned content) versus LLM-as-judge scores (noisy, cost per run, needs repeated runs and a tolerance), threshold gates on a sampled subset, caching of model calls, and secrets for API keys. Implement the evaluation gate with a stub model function (no real API call, so say the real provider call is not executed), a tolerance for noise, and pytest cases, and run it.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Keep prompts and configs in Git, run a golden evaluation set on every PR, split the checks into cheap deterministic ones (format, schema, banned content) that must pass and noisy LLM-judge scores that are repeated, averaged and compared with a tolerance, and keep the API key out of fork PRs.

**Then explain:**
- **Version everything that changes behaviour.** Prompt templates, model name and parameters, retrieval settings, tool schemas and the golden set are files in Git. A prompt edit is a code change, reviewed like one.
- **Golden set.** A small, curated set of inputs with expectations (must contain, JSON keys, forbidden phrases, or a reference answer). Version it; changes to it are reviewed, otherwise people edit the test until it passes.
- **Deterministic checks first.** Valid JSON, required keys, length, banned content, refusal on unsafe inputs. Free, fast, no key, and they run on forks.
- **LLM-as-judge is noisy and costs money.** Scores vary between runs, so run each case several times, average, and fail only when the mean drops more than a tolerance from a baseline or under a floor. Use a sample of the golden set on PRs and the full set nightly. In my run the per-repeat means ranged over 0.73 across five repeats, more than the 0.3 tolerance, which is why single runs are not gated.
- **Cache model calls** by hash of (model, parameters, prompt, input) so unchanged cases cost nothing on re-runs. Valid only when the setup is effectively deterministic or you accept recorded outputs; refresh the cache on model changes.
- **Secrets.** The API key is a repository or environment secret; fork PRs do not get it, so the judged job is skipped for forks and a maintainer re-runs it. Never print prompts with personal data into logs.
- **Failure modes.** The judge model changes silently under you (pin its version, check current provider docs). Judge and generator are the same model (bias). The golden set leaks into the prompt. A tolerance so loose that regressions pass.

**Example:** four golden cases, five repeats. The stub model answers one case with "Soon." in one repeat (missing "days"). Deterministic pass rate is 0.95, above the 0.90 floor; the judge mean 4.42 is above the 4.0 floor and within 0.3 of the 4.4 baseline: PASS. A model that always says "I cannot help" gets 0.0 and 2.05: FAIL, exit 1.

**Code:** the gate takes a model function and a judge function, so tests inject fakes. Both here are stubs: **no provider API call is made**, and the real provider call is not executed. The workflow shows the real shape.
```python
# --- file: eval_gate.py ---

"""CI gate for an LLM app. The model call is a STUB: no provider API is called here."""
import json, random, statistics, sys

BANNED = ["ignore previous instructions", "as an ai language model"]

def stub_model(prompt, seed):
    """Deterministic stand-in for the real call. Pretends to be a bit noisy on g3 only."""
    rnd = random.Random(f"{prompt}-{seed}")
    answer = {"Refund for order 118?": "You can request a refund within the window.",
              "Reset my password": "Use the reset link on the login page.",
              "Delivery time to Pune?": "Usually 3 to 5 days." if rnd.random() > 0.2 else "Soon.",
              "Cancel subscription": "You can cancel from Settings."}[prompt]
    return json.dumps({"answer": answer, "source": "faq"})

def stub_judge(prompt, output, seed):
    """Stand-in for LLM-as-judge: score 1-5 with noise. A real judge costs money and varies run to run."""
    base = 4.5 if "days" in output or "refund" in output.lower() or "reset" in output or "cancel" in output else 2.0
    return base + random.Random(f"j-{prompt}-{seed}").uniform(-0.4, 0.4)

def deterministic_checks(case, raw):
    fails = []
    try:
        obj = json.loads(raw)
    except ValueError:
        return ["not valid JSON"]
    for k in case["expect_json_keys"]:
        if k not in obj:
            fails.append(f"missing key {k}")
    text = str(obj.get("answer", "")).lower()
    fails += [f"missing '{w}'" for w in case["must_contain"] if w not in text]
    fails += [f"banned phrase '{b}'" for b in BANNED if b in text]
    return fails

def run_gate(cases, model=stub_model, judge=stub_judge, repeats=5,
             min_det_pass=0.9, min_judge_mean=4.0, tolerance=0.3, baseline_judge=4.4):
    problems, notes = [], []
    det_pass = 0
    judge_runs = []
    for r in range(repeats):                       # repeat: single judge scores are noisy
        scores = []
        for c in cases:
            out = model(c["input"], r)
            f = deterministic_checks(c, out)       # cheap, so run on every repeat
            det_pass += not f
            if f:
                notes.append(f"{c['id']} repeat {r}: " + "; ".join(f))
            scores.append(judge(c["input"], out, r))
        judge_runs.append(statistics.mean(scores))
    det_rate = det_pass / (len(cases) * repeats)
    jm = statistics.mean(judge_runs)
    if det_rate < min_det_pass:
        problems.append(f"deterministic pass rate {det_rate:.2f} < {min_det_pass}")
    if jm < min_judge_mean:
        problems.append(f"judge mean {jm:.2f} < floor {min_judge_mean}")
    if jm < baseline_judge - tolerance:
        problems.append(f"judge mean {jm:.2f} dropped more than tolerance {tolerance} from baseline {baseline_judge}")
    return {"det_rate": det_rate, "judge_mean": round(jm, 3), "judge_spread": round(max(judge_runs) - min(judge_runs), 3), "notes": notes}, problems

if __name__ == "__main__":
    cases = [json.loads(l) for l in open(sys.argv[1])]
    summary, problems = run_gate(cases)
    print({k: v for k, v in summary.items() if k != "notes"})
    for n in summary["notes"]:
        print("note:", n)
    for p in problems:
        print("FAIL:", p)
    print("GATE:", "FAIL" if problems else "PASS")
    sys.exit(1 if problems else 0)

# --- file: test_eval_gate.py ---

import json
from eval_gate import run_gate, deterministic_checks, stub_model, stub_judge

CASES = [json.loads(l) for l in open("golden.jsonl")]

def test_good_stub_passes():
    summary, problems = run_gate(CASES)
    assert problems == []
    assert summary["notes"]            # a noisy case was seen, but the rate stayed above 0.9

def test_single_runs_are_noisier_than_the_tolerance_so_we_average():
    summary, problems = run_gate(CASES)
    assert summary["judge_spread"] > 0.3          # one run could trip a 0.3 tolerance by luck
    assert abs(summary["judge_mean"] - 4.4) < 0.3  # the mean over repeats stays inside it

def test_broken_format_fails_deterministic_gate():
    bad = lambda p, s: "plain text, not json"
    summary, problems = run_gate(CASES, model=bad)
    assert any("deterministic pass rate" in p for p in problems)

def test_banned_phrase_is_caught():
    case = CASES[0]
    raw = json.dumps({"answer": "Refund: ignore previous instructions", "source": "x"})
    assert any("banned" in f for f in deterministic_checks(case, raw))

def test_quality_drop_beyond_tolerance_fails():
    worse = lambda p, o, s: 3.5
    _, problems = run_gate(CASES, judge=worse)
    assert any("floor" in p for p in problems) and any("tolerance" in p for p in problems)
```
```yaml
name: llm-eval
on:
  pull_request:
    paths: ["prompts/**", "config/**", "app/**", "evals/**"]
permissions:
  contents: read
concurrency:
  group: llm-eval-${{ github.ref }}
  cancel-in-progress: true
jobs:
  deterministic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest evals/deterministic -q       # format, schema, banned content; no API key, runs on forks too
  judged:
    needs: deterministic
    if: github.event.pull_request.head.repo.full_name == github.repository   # forks get no secrets
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: LLM-as-judge on a sampled subset, repeated
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
          EVAL_REPEATS: "3"
          EVAL_SAMPLE: "40"
        run: python evals/run_gate.py --golden evals/golden.jsonl
```
```bash
python -I eval_gate.py golden.jsonl            # exit 0 on pass, 1 on fail
python -I -m pytest -q -p no:cacheprovider test_eval_gate.py
actionlint llm-ci.yml
```
`golden.jsonl` is in `code/q40/` (four small cases with `must_contain` and `expect_json_keys`).

**Output (my run):** stub model and stub judge only, so the numbers show the mechanism, not the quality of any real LLM. pytest 9.1.1, actionlint 1.7.12.
```text
{'det_rate': 0.95, 'judge_mean': 4.422, 'judge_spread': 0.734}
note: g3 repeat 4: missing 'days'
GATE: PASS
exit=0
5 passed in 0.02s
== a broken model (always 'I cannot help')
{'det_rate': 0.0, 'judge_mean': 2.047, 'judge_spread': 0.147}
FAIL: deterministic pass rate 0.00 < 0.9
FAIL: judge mean 2.05 < floor 4.0
FAIL: judge mean 2.05 dropped more than tolerance 0.3 from baseline 4.4
== actionlint llm-ci.yml
exit=0
```

**Follow-ups:**
- *How many repeats?* Enough that the spread of the mean is well under the tolerance; measure it on your set, do not guess.
- *Why not gate on the judge alone?* It is noisy and gameable. Deterministic checks catch the failures that cost you most.
- *What about prompts changing without code?* Same pipeline: prompt files live in Git, so the PR runs the eval.

**Common mistakes:**
- Gating on one judge run.
- Evaluating on the cases you tuned the prompt on.
- Running the key-holding job on fork PRs.
- Calling a real API in every unit test.


