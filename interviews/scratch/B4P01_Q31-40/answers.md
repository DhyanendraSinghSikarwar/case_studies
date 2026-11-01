<!-- Wave B answers, Book 4 Part 1, Q31-Q40 (no edits to the part file) -->

### Q31 ⭐⭐ 🔴 Monorepo versus polyrepo for ML platform code. A company has 8 model repos that each copy a feature library. Compare a monorepo, a polyrepo with a shared versioned package, and git submodules (cost, CI time, ownership with CODEOWNERS, breaking changes, release cadence). Recommend one for 8 teams and describe how a breaking change to the shared library is rolled out without breaking the other repos.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** For 8 teams I would pick a polyrepo with one shared, versioned package, owned through CODEOWNERS, and roll out breaking changes in two steps (add and deprecate, then remove); I would pick a monorepo only if we already have tooling that runs just the affected tests.

**Then explain:**
| Option | What you get | What it costs |
|---|---|---|
| Monorepo | one commit can change the library and all 8 callers; no version drift; easy search | CI must be smart (build only what changed) or it gets slow; one repo needs tooling and strong ownership rules; access control is coarse |
| Polyrepo + shared versioned package | teams ship on their own cadence; each repo pins a version; clear owner for the library | version drift (8 repos on 5 versions); a fix needs a release and 8 bumps; breaking changes need a plan |
| Git submodules | exact commit pinned, no package index needed | people forget `git submodule update`; detached HEAD confusion; CI must clone recursively; no semantic version, only a commit; I avoid them |
- Ownership: CODEOWNERS makes the platform team the required reviewer for the feature library path, so a model team cannot change shared code unreviewed.
- Breaking change rollout (expand then contract): release 1.5 with the new API and the old one kept as a warning shim, ping the 8 teams, let bots open bump PRs, run every consumer's tests against the release candidate in the library's CI, and remove the old API only in 2.0 after a stated window.
- Pin with a range like `>=1.4,<2` so a minor release flows in and a major one never lands by surprise. A too-tight pin (`==1.4.*`) blocks fixes, as the demo shows for the `forecast` repo.
- Failure modes: copy-paste of the library into each repo (what they have today, bugs fixed 8 times), a "shared" library with no owner, and a major bump nobody schedules so teams stay on 1.x forever.

**Example:** featlib 1.5.0 is published. With the 8 pin ranges below, 7 repos accept it and `forecast` (pinned `==1.4.*`) does not. featlib 2.0.0 is accepted by only `ranker` and `nlp`, and the other 6 stay safe on 1.x until they migrate. That is exactly what you want.

**Code:**
```bash
#!/bin/bash
# Q31: git submodule pins an exact commit; semver ranges decide which repos accept a new shared-lib release.
set -e
W=$(mktemp -d); cd $W
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@x GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@x
git init -q -b main featlib; cd featlib
echo "def scale(x): return x/100" > featlib.py; git add .; git commit -qm "featlib 1.4.0"; git tag v1.4.0
echo "def scale(x, *, unit): return x/unit" > featlib.py; git commit -qam "featlib 2.0.0 (breaking)"; git tag v2.0.0
cd ..
git init -q -b main model_repo; cd model_repo
git -c protocol.file.allow=always submodule add -q ../featlib vendor/featlib
git -C vendor/featlib checkout -q v1.4.0
git add .; git commit -qm "pin featlib at v1.4.0"
echo "--- git submodule status (the pinned commit; note the tag in brackets) ---"
git submodule status | sed 's/^\(.\)\([0-9a-f]\{7\}\)[0-9a-f]*/\1\2/'
echo "--- the parent repo stores only a commit pointer (mode 160000) ---"
git ls-tree HEAD vendor/ | awk '{print $1, $2}'
echo "--- upstream moved to v2.0.0, model_repo still sees v1.4.0 until someone bumps the pointer ---"
git -C vendor/featlib describe --tags
```

```python
# ---- q31/ranges.py ----
from packaging.specifiers import SpecifierSet
from packaging.version import Version
repos = {"churn": ">=1.4,<2", "fraud": ">=1.4,<2", "ltv": ">=1.2,<2", "ranker": ">=1.4,<3",
         "forecast": "==1.4.*", "nlp": ">=1.0", "pricing": ">=1.4,<2", "risk": ">=1.3,<2"}
for new in ["1.5.0", "2.0.0"]:
    ok = [r for r, s in repos.items() if Version(new) in SpecifierSet(s)]
    blocked = [r for r in repos if r not in ok]
    print(f"featlib {new}: accepted by {len(ok)} repos {ok}")
    print(f"             blocked in {len(blocked)} repos {blocked}")

# ---- q31/shim.py ----
"""Rollout step 1: ship 1.5 with the new API AND the old one, the old one warns."""
import warnings
def scale(x, *, unit=None):
    if unit is None:
        warnings.warn("scale(x) without unit is deprecated; pass unit= (removed in 2.0)", DeprecationWarning, stacklevel=2)
        unit = 100
    return x / unit
warnings.simplefilter("always")
print(scale(250, unit=100))      # new style, silent
print(scale(250))                # old style, still works, warns
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1; the submodule demo uses local paths only, no GitHub)
```text
--- git submodule status (the pinned commit; note the tag in brackets) ---
 4cb75e7 vendor/featlib (v1.4.0)
--- the parent repo stores only a commit pointer (mode 160000) ---
160000 commit
--- upstream moved to v2.0.0, model_repo still sees v1.4.0 until someone bumps the pointer ---
v1.4.0
featlib 1.5.0: accepted by 7 repos ['churn', 'fraud', 'ltv', 'ranker', 'nlp', 'pricing', 'risk']
             blocked in 1 repos ['forecast']
featlib 2.0.0: accepted by 2 repos ['ranker', 'nlp']
             blocked in 6 repos ['churn', 'fraud', 'ltv', 'forecast', 'pricing', 'risk']
<scratch>/code/q31/shim.py:10: DeprecationWarning: scale(x) without unit is deprecated; pass unit= (removed in 2.0)
  print(scale(250))                # old style, still works, warns
2.5
2.5
```
The CODEOWNERS and CI parts are described, not executed here (they are hosted-service features, check current docs).

**Follow-ups:**
- *When does the monorepo win?* When changes are often cross-cutting, you have a build tool that finds affected targets, and the company wants one lint and test standard. Then atomic changes beat version juggling.
- *How do you stop version drift in a polyrepo?* A dependency bot (Dependabot or Renovate style, check current docs), plus a dashboard of who is on which version and a rule that versions older than N months are unsupported.
- *What about the model artifacts?* They are versioned separately from the library; the model records which featlib version built its features.

**Common mistakes:**
- Choosing monorepo for fashion without affected-only CI, so every PR runs everything.
- Making a breaking change in a minor release.
- Deleting the old API the same day the new one ships.
- Using submodules as a package manager.

### Q32 ⭐ 🟡 Remove a 2 GB file that was committed by mistake and pushed three commits ago. Explain why git rm is not enough, show how git filter-repo (or BFG, hedge) rewrites history in a throwaway clone, why every collaborator must re-clone or reset, what to do with open pull requests and forks, and why a leaked secret must be rotated even after history is rewritten. Run filter-repo for real on a temp repo and show the size before and after.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** `git rm` only removes the file from the newest commit; the 2 GB blob stays in every old commit, so you rewrite history with `git filter-repo` in a fresh clone, force-push once, make everyone re-clone, and rotate any secret that was ever in it.

**Then explain:**
- Why `git rm` is not enough: history is a chain of snapshots. Old commits still point to the blob, so the repo stays huge and anyone can check out the old commit.
- filter-repo (fresh clone, `--invert-paths --path model.pkl`) rewrites every commit that touched the file. Every commit after it gets a new hash, so the whole branch changes. Commits that become empty are dropped. BFG Repo-Cleaner does a similar job (hedge: check which tool your team has approved; filter-repo is the one the Git docs point to).
- Everyone else: do not `git pull` the new history on top of old (it will merge both and bring the blob back). Re-clone, or reset hard to the new `origin/main` after saving unpushed work. Open pull requests and forks are based on old hashes, so rebase them onto the new history or recreate them. Forks and hosted pull-request refs may keep the old objects, so for a real incident ask the host (check current docs) to run garbage collection or purge cached views.
- Secrets: if the file held a key, assume it was copied. Rotate it first; rewriting is cleanup, not safety.
- Prevent it: `.gitignore`, a size-limit pre-commit hook, and an LFS or DVC rule for big files.

**Example:** The demo repo has 6 commits and a model file added in commit 2. After `git rm` the file is gone from the folder but 2 commits still touch it and the pack is about 19 MiB. After filter-repo the pack is about 2 KiB, history has 4 commits, and a teammate's old clone sees 6 commits only on their side and 4 only on the new side (diverged).

**Code:**
```bash
#!/bin/bash
# Q32: a big file committed 3 commits ago. Scaled down to 20 MB of random bytes (same mechanics as 2 GB).
set -e
W=$(mktemp -d); cd $W
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@x GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@x
git init -q -b main origin_bare --bare
git clone -q origin_bare work 2>/dev/null; cd work
echo "print('train')" > train.py; git add .; git commit -qm "c1 train script"
head -c 20000000 /dev/urandom > model.pkl; git add .; git commit -qm "c2 oops: add model.pkl"
echo "# v2" >> train.py; git commit -qam "c3 tweak"
echo "# v3" >> train.py; git commit -qam "c4 tweak"
echo "# v4" >> train.py; git commit -qam "c5 tweak"
git push -q origin main 2>/dev/null
echo "--- step 1: git rm is not enough ---"
git rm -q model.pkl; git commit -qm "c6 remove model.pkl"
echo "file in working tree: $(ls | tr '\n' ' ')"
echo "still in history: $(git log --oneline --all -- model.pkl | wc -l) commits touch model.pkl"
echo "size of .git: $(du -sh .git | cut -f1)"
git push -q origin main 2>/dev/null
cd ..
echo "--- step 2: rewrite in a throwaway clone ---"
git clone -q --no-local origin_bare clean; cd clean
git count-objects -vH | grep -E 'size-pack'
echo "before: $(git rev-list --count HEAD) commits, tip $(git rev-parse --short HEAD)"
git filter-repo --invert-paths --path model.pkl --force 2>&1 | tail -1
git gc -q --prune=now --aggressive
git count-objects -vH | grep -E 'size-pack'
echo "after:  $(git rev-list --count HEAD) commits (empty commits c2 and c6 dropped), tip $(git rev-parse --short HEAD)  (every hash changed)"
echo "model.pkl anywhere in history: $(git log --all --oneline -- model.pkl | wc -l)"
git log --oneline
echo "--- step 3: filter-repo drops the remote on purpose; re-add and force push is a deliberate act ---"
git remote -v | wc -l
echo "--- step 4: a teammate with the old history sees diverged branches ---"
cd ../work
git remote add rewritten ../clean; git fetch -q rewritten
git rev-list --left-right --count main...rewritten/main
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1). The file is 20 MB of random bytes, not 2 GB, to keep the run fast; the mechanics are identical. Hashes differ on every run.
```text
--- step 1: git rm is not enough ---
file in working tree: train.py 
still in history: 2 commits touch model.pkl
size of .git: 20M
--- step 2: rewrite in a throwaway clone ---
size-pack: 19.08 MiB
before: 6 commits, tip 0e87794
Completely finished after 0.09 seconds.
size-pack: 2.19 KiB
after:  4 commits (empty commits c2 and c6 dropped), tip e1f5c65  (every hash changed)
model.pkl anywhere in history: 0
e1f5c65 c5 tweak
169b08d c4 tweak
ad85148 c3 tweak
8790b4d c1 train script
--- step 3: filter-repo drops the remote on purpose; re-add and force push is a deliberate act ---
0
--- step 4: a teammate with the old history sees diverged branches ---
6	4
```
"0" under step 3 is the number of remotes left: filter-repo removes `origin` on purpose, so you add it back and force-push deliberately (use `--force-with-lease`). The force push itself was not run (no hosted remote).

**Follow-ups:**
- *Can you protect against this server-side?* Yes: hosted pre-receive size limits or push rules (check current docs).
- *How do you find the big blobs first?* `git rev-list --objects --all` piped to `git cat-file --batch-check`, sorted by size, or filter-repo's `--analyze`.
- *Why not just leave it and add the file to `.gitignore`?* `.gitignore` does not affect files already in history.

**Common mistakes:**
- Rewriting history in the only copy of the repo (no backup, no throwaway clone).
- Telling people to `git pull`, which merges old history back in.
- Not rotating a leaked secret because "we removed it".
- Forgetting open PRs and forks.

### Q33 ⭐ 🟡 git stash and git worktree for ML work. A training script is mid-edit with uncommitted changes while a production hotfix is needed on main, and a 6-hour run is reading files from the working directory. Explain stash (and its limits, untracked files with -u), and show how git worktree lets you check out the hotfix branch in a second directory without disturbing the run. Demonstrate in a throwaway repo.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Stash parks uncommitted changes (add `-u` to include untracked files), but with a long run reading your working directory the safer move is `git worktree add`, which gives the hotfix its own directory and branch while the run keeps its files untouched.

**Then explain:**
- `git stash` saves tracked changes and resets the working tree to HEAD. Plain `git stash` leaves untracked files behind; `-u` takes them; ignored files need `-a`. `git stash pop` brings them back, and can conflict if the base moved.
- The problem with stash here: it rewrites the files on disk. A 6-hour job that reads `train.py`, config or data from the folder would suddenly see different files. Switching branches in that folder has the same problem.
- `git worktree add ../proj-hotfix hotfix-null` creates a second working directory on a branch, sharing the same object store (no second clone, small cost). Commit and push the fix from there, then `git worktree remove`.
- Limits: one branch cannot be checked out in two worktrees at once; untracked or ignored data files (big datasets, `.env`) do not appear in the new worktree, so point it at the data by path or symlink.
- Stash is local and easy to forget: `git stash list` can hold old work for months. Name them with `git stash push -m "text"`.

**Example:** In the demo `train.py` has an experiment (`lr = 0.01`) and `notes.txt` is new. Plain stash leaves `notes.txt` in place; `stash -u` leaves a clean tree. Then the hotfix is committed in a sibling directory and the original `train.py` still says `lr = 0.01  # experiment`.

**Code:**
```bash
#!/bin/bash
set -e
W=$(mktemp -d); cd $W
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@x GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@x
git init -q -b main proj; cd proj
printf 'lr = 0.1\n' > train.py; printf 'id,x\n1,5\n' > data.csv
git add .; git commit -qm "base"
git branch hotfix-null
echo "--- mid-edit: tracked change + new untracked file ---"
printf 'lr = 0.01  # experiment\n' > train.py; echo "scratch notes" > notes.txt
git status --short
echo "--- stash without -u leaves the untracked file behind ---"
git stash -q; git status --short; git stash list
git stash pop -q
echo "--- stash -u takes it too ---"
git stash -u -q; git status --short | wc -l; git stash pop -q; git status --short
echo "--- worktree: second directory, run in the first is untouched ---"
git worktree add -q ../proj-hotfix hotfix-null
git worktree list | sed "s#$W#<tmp>#" || true
printf 'lr = 0.1\nfill = 0  # hotfix: null handling\n' > ../proj-hotfix/train.py
git -C ../proj-hotfix commit -qam "hotfix: fill nulls"
echo "main working dir still has the experiment:"; cat train.py
echo "hotfix branch log:"; git log --oneline hotfix-null
echo "--- cleanup ---"
git worktree remove ../proj-hotfix; git worktree list | wc -l
echo "--- same branch cannot be checked out twice ---"
git worktree add -q ../w2 hotfix-null; git worktree add ../w3 hotfix-null 2>&1 | grep fatal | sed "s#$W#<tmp>#" || true
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1)
```text
--- mid-edit: tracked change + new untracked file ---
 M train.py
?? notes.txt
--- stash without -u leaves the untracked file behind ---
?? notes.txt
stash@{0}: WIP on main: 9ec38ca base
--- stash -u takes it too ---
0
 M train.py
?? notes.txt
--- worktree: second directory, run in the first is untouched ---
<tmp>/proj         9ec38ca [main]
<tmp>/proj-hotfix  9ec38ca [hotfix-null]
main working dir still has the experiment:
lr = 0.01  # experiment
hotfix branch log:
524555b hotfix: fill nulls
9ec38ca base
--- cleanup ---
1
--- same branch cannot be checked out twice ---
fatal: 'hotfix-null' is already used by worktree at '<tmp>/w2'
```

**Follow-ups:**
- *Could the run itself be made safe?* Yes: run training from a clean exported copy (a worktree or a tagged checkout) and log the commit hash, so working-directory edits never matter.
- *Where is a stash stored?* As commits under `refs/stash`, so it is not deleted by `git gc` quickly, but it is local and never pushed.
- *Stash versus a WIP commit?* A WIP commit on a branch is easier to share and find; squash it later.

**Common mistakes:**
- Forgetting `-u` and thinking everything was stashed.
- Switching branches under a running job.
- Leaving worktrees behind (use `git worktree remove` and `git worktree prune`).
- Assuming the new worktree has the ignored data files.

### Q34 ⭐ 🟡 Repository governance for a model repo: branch protection, required reviews, CODEOWNERS, required status checks, signed commits and tags. Say what each protects against (an unreviewed change to the feature code reaching production, forged authorship), what the GitHub or GitLab settings are called (hedge: check current docs), and show a CODEOWNERS file that makes the data scientist team own models/ and the platform team own deploy/ and parse it for a given changed path in Python.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** Branch protection plus required reviews, CODEOWNERS and required status checks stop an unreviewed or untested change reaching the deployable branch, and signed commits and tags make forged authorship detectable; each one closes a different hole.

**Then explain:**
| Control | Protects against | Typical setting name (check current docs) |
|---|---|---|
| Branch protection | direct pushes and force-pushes to `main` | GitHub branch protection rules or rulesets; GitLab protected branches |
| Required reviews | one person merging their own change | "Require approvals" |
| CODEOWNERS | feature code or deploy config changed without the owning team seeing it | "Require review from Code Owners" (the file alone does nothing unless this is on) |
| Required status checks | merging when tests or the model gate failed | "Require status checks to pass" |
| Signed commits / tags | someone committing in another person's name; an unverified release tag | "Require signed commits"; signature verification on tags |
- Signing proves who holds the key, not that the change is good. Reviews and checks are still needed.
- Failure modes: admins who can bypass rules, owner teams too small so every PR waits, a CODEOWNERS entry naming a team without write access (the rule cannot be satisfied), and checks that are required but flaky so people bypass them.
- In CODEOWNERS the last matching line wins (GitHub documents this; check current docs for GitLab syntax differences). Put the broad default first and the specific paths after it.
- The Python below is a tiny matcher for the common patterns only, to show the logic; it is not the full gitignore-style syntax.

**Example:** `models/churn/model.py` goes to data-science; `deploy/k8s/serve.yaml` to ml-platform; `src/features/scale.py` needs both teams (a feature change can break the service); `deploy/secrets.example` is overridden by a later, more specific line to security.

**Code:**
```python
"""Tiny CODEOWNERS matcher. Rule: the LAST matching line wins. Supports the common patterns only:
'*', '/dir/' (anchored dir), 'dir/' (any depth), '*.ext', '/file'. Not full gitignore syntax."""
import fnmatch, sys

CODEOWNERS = """\
# default owner
*                       @acme/ml-platform
/models/                @acme/data-science
/src/features/          @acme/data-science @acme/ml-platform
/deploy/                @acme/ml-platform
*.ipynb                 @acme/data-science
/deploy/secrets.example @acme/security
"""

def parse(text):
    rules = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            pat, *owners = line.split()
            rules.append((pat, owners))
    return rules

def matches(pat, path):
    anchored = pat.startswith("/")
    p = pat.lstrip("/")
    if p.endswith("/"):                       # directory pattern
        return path.startswith(p) if anchored else (path.startswith(p) or ("/" + p) in ("/" + path))
    if anchored:
        return fnmatch.fnmatch(path, p)
    return fnmatch.fnmatch(path, p) or fnmatch.fnmatch(path.rsplit("/", 1)[-1], p)

def owners_of(path, rules):
    found = []
    for pat, owners in rules:                 # keep the last hit
        if matches(pat, path):
            found = owners
    return found

if __name__ == "__main__":
    rules = parse(CODEOWNERS)
    for path in ["models/churn/model.py", "deploy/k8s/serve.yaml", "deploy/secrets.example",
                 "src/features/scale.py", "notebooks/eda.ipynb", "README.md"]:
        print(f"{path:28} -> {' '.join(owners_of(path, rules))}")
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1). The GitHub or GitLab settings are not executed here (hosted services); the matcher is.
```text
models/churn/model.py        -> @acme/data-science
deploy/k8s/serve.yaml        -> @acme/ml-platform
deploy/secrets.example       -> @acme/security
src/features/scale.py        -> @acme/data-science @acme/ml-platform
notebooks/eda.ipynb          -> @acme/data-science
README.md                    -> @acme/ml-platform
```

**Follow-ups:**
- *How do you enforce it for admins too?* Turn on the "include administrators" style option or use organisation rulesets (check current docs).
- *Does CODEOWNERS replace reviews?* No, it only decides who must review.
- *Who owns code that two teams share?* List both owners on the line, as in the demo. Check how your host counts approvals: by default one owner may be enough, so ask for per-team approval if you need both.

**Common mistakes:**
- Creating a CODEOWNERS file but not switching on "require code owner review".
- Believing signed commits make code safe.
- Letting the default branch accept force-pushes.
- Putting the catch-all `*` line last, so it overrides every specific rule.

### Q35 ⭐ 🔴 Flaky tests in ML. A test asserts accuracy greater than 0.90 and fails about 1 run in 20. Diagnose the cause (unseeded split, small test set, nondeterministic library), compare fixes (seed everything, widen the tolerance using a binomial standard error on a 200-row test set, use a larger fixed fixture, test the property rather than the number) and show a run where you measure the failure rate before and after over 200 seeded repetitions with scikit-learn.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** The test is flaky because an accuracy on 200 rows is a noisy number (standard error about 1.8 points here) and the split changes each run; seeding hides the noise, so the real fix is to set the threshold from the measured noise or test a property instead.

**Then explain:**
- Diagnose by repeating: run the same test 200 times and count failures. Here: unseeded split, 200 test rows, true accuracy near 0.93. The binomial standard error is sqrt(p(1-p)/n) = sqrt(0.928 x 0.072 / 200) = 0.018, so a 0.90 threshold is only 1.5 SE below the mean and fails about 5 percent of the time.
- Other causes: unseeded libraries, multi-threaded or GPU non-determinism, test data that drifts, tests that share state or depend on order.
- Fix 1, seed everything: makes it repeatable, but it only picks one draw. In the run, seed 42 gives 0.875 every time, so the test fails 100 percent of the time; the seed turned "sometimes red" into "always red". You must also re-calibrate the threshold.
- Fix 2, widen the tolerance with maths: threshold = expected accuracy minus 3 SE. Drawback: it now only catches big drops (here below 0.873).
- Fix 3, bigger fixed test set: 1000 rows cuts the SE to 0.7 points; the failures disappear at the same 0.90 threshold.
- Fix 4, test a property: "beats the majority-class baseline by 0.10" is stable and still catches a broken model. Pair it with a separate, non-blocking metric tracker for the exact number.

**Example:** n = 200, p = 0.93. SE = sqrt(0.93 x 0.07 / 200) = 0.0180. 0.90 is (0.93-0.90)/0.018 = 1.7 SE below: a one-sided tail near 5 percent. That matches the 5.5 percent measured.

**Code:**
```python
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=3000, n_features=10, n_informative=5, flip_y=0, class_sep=1.7, random_state=7)
THRESH = 0.90

def acc(seed, n_test=200, fit_seed=0):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=n_test, random_state=seed)
    return LogisticRegression(max_iter=500, random_state=fit_seed).fit(Xtr, ytr).score(Xte, yte)

REPS = 200
a = np.array([acc(s) for s in range(REPS)])                       # "unseeded": a different split each run
print(f"typical accuracy (mean over {REPS} splits): {a.mean():.3f}   sd across splits: {a.std():.4f}")
print(f"binomial SE on 200 rows at p={a.mean():.3f}: {np.sqrt(a.mean()*(1-a.mean())/200):.4f}")
def rate(v, thr): return (v < thr).mean() * 100
print(f"\n{'variant':58} fail rate")
print(f"{'A. assert acc > 0.90, split differs each run (200 runs)':58} {rate(a,THRESH):5.1f}%")
fixed = np.array([acc(42) for _ in range(REPS)])
print(f"{'B. same seed 42 every run (200 runs)':58} {rate(fixed,THRESH):5.1f}%   (accuracy {fixed[0]:.3f} every time: all-or-nothing)")
p_hat = a.mean()
se = np.sqrt(p_hat*(1-p_hat)/200)
thr_w = p_hat - 3*se
print(f"{f'C. widen: assert acc > p_hat - 3*SE = {thr_w:.3f}, split differs':58} {rate(a,thr_w):5.1f}%")
big = np.array([acc(s, n_test=1000) for s in range(REPS)])
print(f"{'D. larger test set (1000 rows), same 0.90 threshold':58} {rate(big,THRESH):5.1f}%   sd {big.std():.4f}")
# E: property not number: model beats majority-class baseline by a margin
base = np.array([max(np.mean(y), 1-np.mean(y))]*REPS)
print(f"{'E. property: acc > majority baseline + 0.10':58} {rate(a, base[0]+0.10):5.1f}%   (baseline {base[0]:.3f})")
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1; seeds 0 to 199, so the numbers repeat)
```text
typical accuracy (mean over 200 splits): 0.928   sd across splits: 0.0185
binomial SE on 200 rows at p=0.928: 0.0183

variant                                                    fail rate
A. assert acc > 0.90, split differs each run (200 runs)      5.5%
B. same seed 42 every run (200 runs)                       100.0%   (accuracy 0.875 every time: all-or-nothing)
C. widen: assert acc > p_hat - 3*SE = 0.873, split differs   0.5%
D. larger test set (1000 rows), same 0.90 threshold          0.0%   sd 0.0071
E. property: acc > majority baseline + 0.10                  0.0%   (baseline 0.500)
```

**Follow-ups:**
- *Should you retry flaky tests automatically?* Only as a stop-gap with a ticket; retries hide a real 5 percent failure rate.
- *Is a fixed seed ever the answer?* Yes for unit tests of logic (does the code run, shape, determinism), with the number-quality check kept separate.
- *What about GPU nondeterminism?* Use tolerances (`pytest.approx`) and, where the framework supports it, deterministic flags (check current docs); some ops stay non-deterministic.

**Common mistakes:**
- Fixing the symptom with a retry decorator.
- Picking a seed until the test goes green.
- Lowering the threshold with no reasoning (use SE).
- Comparing accuracy to a point value on a tiny test set.

### Q36 ⭐ 🔴 Performance regression gate in CI. A new commit changes a feature and AUC on a fixed 5,000-row validation set falls from 0.874 to 0.869. Should the build fail? Design the gate: a stored baseline file, a threshold, a bootstrap confidence interval for the difference (paired on the same rows), slice checks, and an override process. Implement the bootstrap comparison on seeded synthetic scores with numpy and scikit-learn and report the decision for a small and a real degradation.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Do not fail on the raw number; fail when a paired bootstrap says the drop is plausibly bigger than the allowed margin, warn when it is inside noise, and keep a logged override for humans.

**Then explain:**
- A 0.005 AUC drop on 5,000 rows may be noise. Both models score the same rows, so compare them as a pair: resample rows with replacement, compute AUC of both models on the SAME resample, take the difference, repeat 2,000 times, read the 95 percent interval.
- Pairing matters: the two scores share row difficulty, so the difference has much less noise than two separate AUCs. How much it helps depends on how correlated the models are (here 0.86 for the small case, 0.97 for the big one).
- Decision rule I would write down: PASS if the interval lower end is above minus margin; FAIL if the whole interval is below zero and the lower end is past the margin; otherwise WARN (a human decides). The margin (here 0.01 AUC) is a business decision stored in the baseline file.
- Baseline file in git (`baseline.json`: metric, value, row count, margin, data version). It only changes through a reviewed PR, so a gate cannot be quietly loosened. Use a fixed validation set and fixed seed for the bootstrap.
- Slice checks: run the same comparison per important slice (new vs old customers, region). A flat overall AUC can hide a slice that got worse; use a looser or count-aware rule on small slices.
- Override: a label or a PR comment with a reason, a named approver, and a ticket, logged in CI. Never an edit of the threshold in the same PR.
- Failure modes: peeking at the same validation set so often that it is overfit; a baseline that is itself stale; many slices giving false alarms (multiple comparisons).

**Example:** In the run, the candidate AUC is 0.869 versus 0.874: delta minus 0.005, interval minus 0.0124 to plus 0.0026, which includes 0. We cannot call it a regression, but it might exceed 0.01, so WARN. A real degradation to 0.845 has an interval of minus 0.033 to minus 0.025, entirely below zero and past the margin: FAIL.

**Code:**
```python
import json, numpy as np
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(36)
N = 5000
y = (rng.random(N) < 0.3).astype(int)
shared = rng.normal(size=N)            # row difficulty both models see
own_new = rng.normal(size=N)           # what only the NEW model's changed feature adds

def make(strength, own_weight):
    return strength * y + shared + own_weight * own_new

def tune(target, own_weight):
    lo, hi = 0.05, 4.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if roc_auc_score(y, make(mid, own_weight)) < target: lo = mid
        else: hi = mid
    return mid

base  = make(tune(0.874, 0.0), 0.0)
small = make(tune(0.869, 0.8), 0.8)    # changed feature adds its own noise -> models only partly correlated
real  = make(tune(0.845, 0.3), 0.3)

baseline = {"metric": "roc_auc", "auc": round(float(roc_auc_score(y, base)), 3), "n_rows": N, "allowed_drop": 0.01}
json.dump(baseline, open("baseline.json", "w"))   # in CI: committed file, changed only through a reviewed PR
print("baseline.json:", baseline)

def gate(new, name, reps=2000, margin=baseline["allowed_drop"]):
    r = np.random.default_rng(1)
    diffs = np.empty(reps)
    for b in range(reps):
        i = r.integers(0, N, N)        # the SAME resampled rows for both models = paired bootstrap
        diffs[b] = roc_auc_score(y[i], new[i]) - roc_auc_score(y[i], base[i])
    d = roc_auc_score(y, new) - roc_auc_score(y, base)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    if lo > -margin and d > -margin:   verdict, why = "PASS", f"drop is not provably worse than {margin}"
    elif hi < 0 and lo < -margin:      verdict, why = "FAIL", f"drop plausibly bigger than {margin}"
    else:                              verdict, why = "WARN", "drop not shown to exceed margin; flag for review"
    zero = "includes 0" if lo <= 0 <= hi else "excludes 0"
    print(f"{name:11} AUC {roc_auc_score(y,new):.3f} vs {roc_auc_score(y,base):.3f} delta {d:+.4f}  95% CI [{lo:+.4f}, {hi:+.4f}] ({zero})  -> {verdict}: {why}")
gate(small, "small drop")
gate(real,  "real drop")
print("Pearson corr of scores, base vs small:", round(float(np.corrcoef(base, small)[0,1]), 3), " base vs real:", round(float(np.corrcoef(base, real)[0,1]), 3))
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1; seed 36, 2000 resamples). The data is synthetic.
```text
baseline.json: {'metric': 'roc_auc', 'auc': 0.874, 'n_rows': 5000, 'allowed_drop': 0.01}
small drop  AUC 0.869 vs 0.874 delta -0.0050  95% CI [-0.0124, +0.0026] (includes 0)  -> WARN: drop not shown to exceed margin; flag for review
real drop   AUC 0.845 vs 0.874 delta -0.0290  95% CI [-0.0329, -0.0254] (excludes 0)  -> FAIL: drop plausibly bigger than 0.01
Pearson corr of scores, base vs small: 0.859  base vs real: 0.97
```

**Follow-ups:**
- *Why not a DeLong test?* It is a valid analytic alternative for paired AUCs; the bootstrap also works for any metric and is easy to explain.
- *What if the metric is not AUC?* The same loop works for F1 or log loss; for rare positives use stratified resampling.
- *Is 0.005 ever worth blocking?* If the model's profit or risk is very sensitive to it, set a tighter margin and a bigger validation set; the margin comes from the business cost, not from the stats.

**Common mistakes:**
- Failing the build on any drop (noise causes constant red) or passing anything within a loose fixed margin (a slow decline gets through).
- Bootstrapping the two models on different resamples (loses the pairing).
- Letting the threshold be edited in the same PR as the model change.
- Ignoring slices.

### Q37 ⭐ 🔴 Wheels, platform tags and optional extras. A package has a pure-Python core and an optional GPU module. Explain pure-Python wheels versus platform wheels (manylinux tags in one line), how extras (pip install pkg[gpu]) separate heavy dependencies, why you do not put torch or CUDA in install_requires of a small utility library, and how you check what a built wheel contains. Build a wheel with an extra for real in a temp folder and inspect its METADATA.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** A pure-Python wheel (`py3-none-any`) works anywhere; a platform wheel contains compiled code and is tagged for an OS and CPU; heavy or optional dependencies go in extras (`pkg[gpu]`) so a small utility does not drag in torch.

**Then explain:**
- Wheel tag format: name-version-python tag-ABI tag-platform tag. `py3-none-any` means no compiled code, any OS. A compiled wheel looks like `cp313-cp313-manylinux_x_y_x86_64`: the `manylinux` tag says it was built to run on most Linux distributions with a baseline glibc (check the current manylinux policy for the exact versions).
- A source distribution (sdist) is the source; installing it runs the build on the user's machine, so it needs a compiler for C extensions. Wheels install with no build.
- Extras: `[project.optional-dependencies] gpu = ["torch>=2.1"]`. `pip install mlutil` stays light; `pip install "mlutil[gpu]"` adds torch. Import the heavy module lazily and raise a clear error that names the extra.
- Why not put torch or CUDA in the core `dependencies`: it forces a huge download and a specific build on everyone (CPU-only users, edge devices), and the right torch build depends on the CUDA and index setup, which a utility library should not decide. Also it makes version conflicts with the user's own torch likely.
- Inspect a built wheel: it is a zip. List the files, read `METADATA` for `Requires-Dist` (with `extra == 'gpu'` markers) and `Provides-Extra`, read `WHEEL` for the tag.
- Failure modes: forgetting that extras are not installed in CI (the GPU path is untested), extras names with typos silently ignored by pip (it warns), and tests that import the optional module at top level.

**Example:** `mlutil` 0.3.0 has `numpy>=1.24` as core and `torch>=2.1` under `gpu`. The built wheel is `mlutil-0.3.0-py3-none-any.whl`; installing it in a clean venv and calling `mlutil.gpu` without torch gives the friendly error that tells you to install `mlutil[gpu]`.

**Code:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mlutil"
version = "0.3.0"
description = "Small ML utilities; core is pure Python, GPU module is optional"
requires-python = ">=3.9"
dependencies = ["numpy>=1.24"]          # light, only what the core needs

[project.optional-dependencies]
gpu = ["torch>=2.1"]                     # heavy, only on request: pip install mlutil[gpu]
dev = ["pytest"]

[tool.hatch.build.targets.wheel]
packages = ["src/mlutil"]
```

```python
# ---- q37/pkg/src/mlutil/__init__.py ----
def scale(xs):
    lo, hi = min(xs), max(xs)
    return [(x - lo) / (hi - lo) for x in xs]

# ---- q37/pkg/src/mlutil/gpu.py ----
def to_device(x):
    try:
        import torch          # imported lazily: the core never needs torch
    except ImportError as e:
        raise ImportError("mlutil.gpu needs the extra: pip install 'mlutil[gpu]'") from e
    return torch.as_tensor(x)
```

```bash
set -e
W=$(mktemp -d); cp -r "<scratch>/code/q37/pkg" $W/pkg; cd $W/pkg
python3 -m build --wheel --no-isolation -o ../dist . 2>&1 | tail -1
cd ..; ls dist
echo "--- name-version-python-abi-platform: py3-none-any = pure Python, any OS ---"
echo "--- contents ---"; python3 -m zipfile -l dist/*.whl | awk '{print $1}' | tail -n +2
echo "--- METADATA (header part) ---"; python3 -m zipfile -e dist/*.whl x >/dev/null; cat x/mlutil-0.3.0.dist-info/METADATA | sed -n 1,14p
echo "--- WHEEL file ---"; cat x/mlutil-0.3.0.dist-info/WHEEL
echo "--- clean venv: install base vs extra (offline for the base; torch not downloaded) ---"
python3 -m venv v; ./v/bin/pip -q install --no-index --no-deps dist/*.whl
./v/bin/python -c "import mlutil; print(mlutil.scale([2,4,6]))"
./v/bin/python -c "import mlutil.gpu as g; g.to_device([1])" 2>&1 | tail -1
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1). Built with `--no-isolation` using the already installed hatchling. The `[gpu]` install itself was not run (it would download torch); only the metadata and the error message were checked.
```text
Successfully built mlutil-0.3.0-py3-none-any.whl
mlutil-0.3.0-py3-none-any.whl
--- name-version-python-abi-platform: py3-none-any = pure Python, any OS ---
--- contents ---
mlutil/__init__.py
mlutil/gpu.py
mlutil-0.3.0.dist-info/METADATA
mlutil-0.3.0.dist-info/WHEEL
mlutil-0.3.0.dist-info/RECORD
--- METADATA (header part) ---
Metadata-Version: 2.5
Name: mlutil
Version: 0.3.0
Summary: Small ML utilities; core is pure Python, GPU module is optional
Requires-Python: >=3.9
Requires-Dist: numpy>=1.24
Provides-Extra: dev
Requires-Dist: pytest; extra == 'dev'
Provides-Extra: gpu
Requires-Dist: torch>=2.1; extra == 'gpu'
--- WHEEL file ---
Wheel-Version: 1.0
Generator: hatchling 1.32.4
Root-Is-Purelib: true
Tag: py3-none-any
--- clean venv: install base vs extra (offline for the base; torch not downloaded) ---
[0.0, 0.5, 1.0]
ImportError: mlutil.gpu needs the extra: pip install 'mlutil[gpu]'
```

**Follow-ups:**
- *How do you ship a platform wheel for several OSes?* Build in CI per platform (a tool such as cibuildwheel, check current docs) and upload all wheels plus the sdist.
- *Extras versus a separate package?* If the optional part is big or has its own release cycle, a separate package (`mlutil-gpu`) is cleaner.
- *Should `torch` be a dev dependency?* Put it in the `dev` or `test` extra for CI jobs that need it.

**Common mistakes:**
- Listing torch in core dependencies of a small library.
- Importing the optional module at the top of `__init__.py`.
- Not testing the install without the extra.
- Calling a wheel with C code "pure" and uploading only one platform.

### Q38 ⭐ 🔴 Distribute an internal ML library to 30 data scientists. Compare a private package index (Artifact Registry, CodeArtifact, Nexus or Artifactory, hedge names and check current docs), installing from a git URL with a tag, and a shared mounted directory. Cover authentication, versioning, yanking a bad release, deprecation warnings via the warnings module and a compatibility policy. Show the pip install forms and a deprecation shim that is tested with pytest.warns.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** For 30 people use a private package index with versioned releases (it gives auth, yanking and a normal `pip install`); a git URL with a tag is a good small-team shortcut; a shared mounted directory is the weakest option.

**Then explain:**
| Option | Auth | Versioning | Good for | Weak point |
|---|---|---|---|---|
| Private index (Artifact Registry, CodeArtifact, Nexus, Artifactory; check current docs) | tokens or cloud identity | real releases, ranges like `>=1.2,<2` | 30 users and many projects | someone must run it and manage tokens |
| `pip install "lib @ git+https://host/org/lib.git@v1.2.0"` | the git host's SSH key or token | a tag or commit | tiny teams, quick start | builds from source each time; needs git and build tools; no yank |
| Shared directory of wheels with `--no-index --find-links` | file permissions | file names | air-gapped or very small | no history, no access control per project, stale copies |
- Authentication: never put tokens in `requirements.txt`; use keyring helpers or environment variables injected by CI, and read-only tokens for installs (check the docs of the chosen registry).
- Versioning: semantic versions, release only from tags, one changelog. Pin consumers with ranges.
- Yanking a bad release: a yanked release stays installable only if someone pins it exactly, so new resolutions skip it. Index support varies, so check your registry's docs; on a private index you can often delete it. Then ship a fixed patch version.
- Deprecation: warn first with `warnings.warn(..., DeprecationWarning, stacklevel=2)`, keep the old name for at least one minor series, then remove in the next major. Write the policy down (for example: warn for 2 minor releases or 3 months).
- Test the shim with `pytest.warns`, and check that the new API is silent.

**Example:** `build_features()` is renamed `make_features()` in 1.2.0. The old name still works but warns, with a message pointing to the new one and the version where it disappears. Users see the warning at their own call site because of `stacklevel=2`.

**Code:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
[project]
name = "teamlib"
version = "1.2.0"
dependencies = []
[tool.hatch.build.targets.wheel]
packages = ["src/teamlib"]
```

```python
# ---- q38/pkg/src/teamlib/__init__.py ----
import warnings

def make_features(df_rows, *, fill=0):
    """New API (1.2+)."""
    return [fill if v is None else v for v in df_rows]

def build_features(df_rows):
    """Old name, kept as a shim for one minor series, removed in 2.0."""
    warnings.warn(
        "build_features() is deprecated since 1.2 and will be removed in 2.0; use make_features()",
        DeprecationWarning,
        stacklevel=2,          # point at the CALLER's line, not this file
    )
    return make_features(df_rows)

# ---- q38/tests/test_shim.py ----
import pytest, teamlib

def test_old_name_warns_and_still_works():
    with pytest.warns(DeprecationWarning, match="use make_features"):
        out = teamlib.build_features([1, None, 3])
    assert out == [1, 0, 3]

def test_new_name_is_silent(recwarn):
    teamlib.make_features([1, None])
    assert len(recwarn) == 0
```

```bash
set -e -o pipefail
Q=<scratch>/code/q38
W=$(mktemp -d); cp -r $Q/pkg $W/src; cp -r $Q/tests $W/tests; cd $W
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@x GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@x
cd src; git init -q -b main; git add .; git commit -qm "teamlib 1.2.0"; git tag v1.2.0; cd ..
python3 -m build --wheel --no-isolation -o shared_dir src >/dev/null 2>&1
python3 -m venv v; PIP="./v/bin/pip -q install --disable-pip-version-check"
echo "--- form 1: git URL pinned to a tag (local path used here instead of a hosted remote) ---"
$PIP "teamlib @ git+file://$W/src@v1.2.0" 2>&1 | tail -2
./v/bin/pip list --disable-pip-version-check 2>/dev/null | grep -i teamlib
./v/bin/pip uninstall -y -q teamlib
echo "--- form 3: shared directory of wheels, no network, no index ---"
$PIP --no-index --find-links shared_dir teamlib==1.2.0
./v/bin/pip list --disable-pip-version-check 2>/dev/null | grep -i teamlib
echo "--- tests (pytest.warns) ---"
$PIP pytest 2>&1 | tail -1
./v/bin/python -m pytest -q tests 2>&1 | tail -3
echo "--- how the old call looks to a user ---"
./v/bin/python -W default -c "import teamlib; teamlib.build_features([1,None])" 2>&1 | cut -c1-200 | sed "s#$W#<tmp>#"
```

Pip forms against a hosted index, shown but NOT executed here (replace names and URLs; check your registry's docs):
```text
pip install teamlib==1.2.0 --index-url https://<private-index>/simple/ --extra-index-url https://pypi.org/simple/
pip install "teamlib @ git+https://<host>/<org>/teamlib.git@v1.2.0"
pip install --no-index --find-links /mnt/shared/wheels teamlib==1.2.0
```
Note: `--extra-index-url` mixes indexes, which allows dependency confusion if an attacker publishes the same name publicly; prefer one index that mirrors public packages.

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1). Forms 1 (local git repo, tag v1.2.0) and 3 (directory of wheels) were really run; hosted index forms were not.
```text
--- form 1: git URL pinned to a tag (local path used here instead of a hosted remote) ---
teamlib 1.2.0
--- form 3: shared directory of wheels, no network, no index ---
teamlib 1.2.0
--- tests (pytest.warns) ---
..                                                                       [100%]
2 passed in 0.01s
--- how the old call looks to a user ---
<string>:1: DeprecationWarning: build_features() is deprecated since 1.2 and will be removed in 2.0; use make_features()
```

**Follow-ups:**
- *What is dependency confusion?* Pip picks the highest version across all indexes, so an attacker can publish your internal package name publicly with a higher number. Use a single index, or pin hashes.
- *How long do you keep deprecated names?* Write a policy; my default is at least one minor release and a few weeks, longer when many teams use it.
- *Who tests that consumers still work?* The library's CI runs a few consumer test suites against each release candidate.

**Common mistakes:**
- Tokens in committed requirements files.
- Installing from `main` instead of a tag.
- Deprecating with a `print` or a silent change instead of a warning.
- Forgetting `stacklevel=2`, so the warning points inside the library.

### Q39 ⭐ 🔴 Hidden technical debt in ML systems (Sculley et al.). Name and explain four forms (glue code, pipeline jungles, dead experimental code paths, undeclared consumers or configuration debt), give a code smell for each in a repository of 20 modules, and describe a 3-sprint plan to pay one down with tests first. Say which refactors you would refuse to do without tests.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** The paper's point is that the model code is a small part of an ML system and the real debt lives around it: glue code, pipeline jungles, dead experimental paths and configuration, plus undeclared consumers; I pay it down by writing characterisation tests first and then refactoring in small steps.

**Then explain:**
| Debt (Sculley et al., from memory, check the paper for wording) | Code smell in a 20-module repo | What it costs |
|---|---|---|
| Glue code | a module whose only job is converting between two libraries' data types (numpy to pandas to a tool format and back) | every library change touches glue; hard to swap tools |
| Pipeline jungle | `step2_clean_v2.py`, `step3_clean_final.py`, `step4_clean_final2.py`: scripts chained by file names and order, nobody knows which are live | one change breaks a step three files later; no one dares to touch it |
| Dead experimental code paths | a constant flag like `USE_OLD_FEATURES = False` guarding a branch nobody has run for a year | every new change must work around code that never runs |
| Configuration debt | keys in `config.json` that no code reads, and keys read but never documented | wrong runs, hidden defaults, fear of deleting anything |
| Undeclared consumers (related) | other jobs reading your output table or model file with no contract | a harmless change breaks someone you did not know about |
- Detecting is mostly mechanical: the demo below finds all four planted smells with about 40 lines of `ast` and regular expressions. Counting them each sprint gives a trend.
- Plan, 3 sprints, to pay one down (the pipeline jungle): Sprint 1, characterisation tests: run the current pipeline on a frozen sample and store the output as golden files; add a smoke test that runs end to end. Sprint 2, turn the step scripts into named functions with one entry point and a config object, keep outputs identical to the golden files. Sprint 3, delete the dead scripts and flags, write down inputs and outputs per step, add a data contract check on the final table.
- I would refuse to refactor without tests: feature engineering code, anything that writes the table or model other systems read, scaling and encoding, and any rewrite of the training-serving shared code. If the behaviour is not pinned, "cleaner" can silently change predictions.
- Failure modes: a big-bang rewrite, refactoring and changing behaviour in one PR, and golden files that nobody reviews.

**Example:** The detector prints four lines for the toy repo: glue in `glue.py`, 4 jungle-named step files, the dead flag in `features.py`, and 3 unread config keys (`dropout`, `legacy_mode`, `tmp_fix_2022`). Then a characterisation test pins the output of a tangled function (`[3.0, 5.0, 0, -2]`) before anyone edits it.

**Code:**
```python
# ---- q39/smells.py ----
"""Q39: build a tiny 'repo' with four planted debts and find them with ~40 lines of ast/regex.
Not a real tool: it shows that each smell is mechanically visible, so you can count it and track it."""
import ast, re, tempfile, textwrap
from pathlib import Path

FILES = {
 "features.py": '''
    USE_OLD_FEATURES = False          # flag nobody has flipped since 2023
    def build(df):
        if USE_OLD_FEATURES:
            return old_build(df)      # dead experimental path
        return new_build(df)
    def old_build(df): return df
    def new_build(df): return df
 ''',
 "glue.py": '''
    import numpy as np, pandas as pd
    def to_api(df):                   # glue: only converts shapes between two packages
        arr = np.asarray(df); df2 = pd.DataFrame(arr); return df2.to_numpy().tolist()
 ''',
 "train.py": '''
    import json
    cfg = json.load(open("config.json"))
    def run():
        return cfg["lr"], cfg["depth"]         # reads only lr and depth
 ''',
 "config.json": '{"lr": 0.1, "depth": 4, "dropout": 0.3, "legacy_mode": true, "tmp_fix_2022": 1}',
 "job_a.py": "from features import build\nbuild(None)\n",
 "step1_clean.py": "pass\n", "step2_clean_v2.py": "pass\n", "step3_clean_final.py": "pass\n",
 "step4_clean_final2.py": "pass\n", "step5_join_tmp.py": "pass\n",
}
root = Path(tempfile.mkdtemp())
for n, t in FILES.items(): (root / n).write_text(textwrap.dedent(t).lstrip())
py = {p.name: ast.parse(p.read_text()) for p in root.glob("*.py")}
text = {p.name: p.read_text() for p in root.glob("*.py")}

# 1 glue code: modules that import both numpy and pandas and define no logic beyond conversions
for n, t in py.items():
    src = text[n]
    if "asarray" in src and "to_numpy" in src and "DataFrame(" in src:
        print(f"glue code            : {n} converts np<->pandas back and forth with no real logic")
# 2 pipeline jungle: many step files with version-ish names
jungle = sorted(n for n in py if re.match(r"step\d+_.*(v\d|final|tmp)", n))
print(f"pipeline jungle      : {len(jungle)} step files with v2/final/tmp style names -> {jungle[:3]} ...")
# 3 dead experimental path: module-level flag that is constant False/True and guards a branch
for n, t in py.items():
    for node in t.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, bool) \
           and node.targets[0].id.isupper():
            print(f"dead experimental    : {n}: constant flag {node.targets[0].id} = {node.value.value} guards a branch")
# 4 config debt: keys in config.json never read via cfg["key"] in code
import json
keys = json.loads((root / "config.json").read_text())
used = set(re.findall(r'cfg\["(\w+)"\]', "".join(text.values())))
print(f"configuration debt   : {sorted(set(keys) - used)} are in config.json but never read")

# ---- q39/characterize.py ----
"""Tests first: pin down what the code does TODAY (golden output) before touching it."""
def legacy_score(rows):                       # pretend this is the tangled function we want to refactor
    out = []
    for r in rows:
        v = r.get("a", 0) * 2 + (1 if r.get("flag") else 0)
        out.append(round(v, 2))
    return out

# GOLDEN was produced by running the CURRENT code once and checking it by eye; it lives in git next to the test.
GOLDEN = [3.0, 5.0, 0, -2]
ROWS = [{"a": 1.0, "flag": True}, {"a": 2.5}, {}, {"a": -1, "flag": False}]

def test_characterization():
    assert legacy_score(ROWS) == GOLDEN

test_characterization()
print("characterization test passed: refactor may start; it must keep this green")
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1). The toy repo is generated by the script in a temp folder.
```text
glue code            : glue.py converts np<->pandas back and forth with no real logic
pipeline jungle      : 4 step files with v2/final/tmp style names -> ['step2_clean_v2.py', 'step3_clean_final.py', 'step4_clean_final2.py'] ...
dead experimental    : features.py: constant flag USE_OLD_FEATURES = False guards a branch
configuration debt   : ['dropout', 'legacy_mode', 'tmp_fix_2022'] are in config.json but never read
characterization test passed: refactor may start; it must keep this green
```

**Follow-ups:**
- *Which debt hurts most first?* The one that blocks releases or hides wrong results: undeclared consumers and untested feature code.
- *How do you find undeclared consumers?* Access logs on the table or file, a registry of consumers, and breaking changes announced with a deprecation window.
- *Is deleting dead code safe?* With tests green and version control behind you, yes; delete in its own commit so it can be reverted.

**Common mistakes:**
- Refactoring without a safety net.
- Treating technical debt as a one-off clean-up week instead of a tracked backlog.
- Quoting the paper from memory as if word for word; paraphrase and name the paper.
- Deleting a config key without checking who reads it.

### Q40 ⭐ 🔴 Reviewing AI-generated ML code (AI-era twist). A teammate pastes an LLM-written training function that runs and reports 0.97 accuracy. List the checks you do before merging: leakage, seed handling, metric on the correct split, silent exception swallowing, an invented API or parameter, and unpinned imports. Show a 30-line example with three planted problems, the tests that expose each, and run it with scikit-learn. Serving and prompting of LLMs are out of scope here (Book 2).
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** I treat LLM-written code as an untrusted PR from a stranger: I do not accept the metric, I check where the data is split, where fitting happens, what the seed is, whether errors can be swallowed, and whether every imported API and argument really exists in the version we pin.

**Then explain:**
- Leakage: anything fitted (scaler, imputer, feature selector, encoder) must be fitted on training rows only, inside a Pipeline, after the split. Quick test: shuffle the labels or use pure noise; an honest pipeline scores about 0.5.
- Seeds: `train_test_split` without `random_state` gives a different split every run, so results cannot be reproduced or compared. Two runs of the same code must give the same number.
- Metric on the right split: check which array goes to `.score()` or the metric function (train versus test), and which metric is right for the problem (accuracy on imbalanced data is a trap).
- Silent failure: a bare `except Exception: pass` means a failed save or a failed feature step looks like success. Catch specific exceptions or let it raise.
- Invented APIs: LLMs sometimes make up parameters or functions (for example a plural `class_weights`). Check with `inspect.signature` or the docs of the pinned version; in many cases the call just raises `TypeError`, but some wrappers swallow unknown keywords.
- Unpinned imports: confirm every import is in the lockfile with a version, and that there is no import of an unfamiliar package with a similar name to a real one (typosquatting risk).
- Also: the code runs and prints a pleasing number is the weakest evidence there is. Ask for tests, not a screenshot.

**Example:** The 30-line function below looks fine and reports an accuracy of 0.93 on data where the labels are coin flips (the real score is about 0.5). Three planted problems: feature selection fitted on all rows (leakage), no seed in the split, and a swallowed `joblib.dump` error. Three tests catch them (all fail on the pasted code, all pass on the fixed one). A fourth test shows the invented-parameter check: it reads the real signature of the installed library and passes on both versions, because this code has no invented argument.

**Code:**
```python
# ---- q40/llm_train.py ----
"""LLM-written training function (as pasted). It runs and prints a great number."""
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

def train(X, y, out_path):
    # keep the 20 most predictive features
    X = SelectKBest(f_classif, k=20).fit_transform(X, y)            # PROBLEM 1: selector sees ALL rows, incl. future test rows
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3)  # PROBLEM 2: no random_state, different split every run
    model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    try:
        joblib.dump(model, out_path)
    except Exception:                                               # PROBLEM 3: swallowed error, caller thinks it saved
        pass
    return model, model.score(X_te, y_te)

def make_data(seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(100, 2000))      # 100 rows, 2000 features, ALL pure noise
    y = rng.integers(0, 2, size=100)      # labels are coin flips: honest accuracy is about 0.5
    return X, y

if __name__ == "__main__":
    X, y = make_data()
    _, acc = train(X, y, "/no/such/dir/model.joblib")
    print(f"accuracy {acc:.2f}  <- reported (the labels are coin flips)")

# ---- q40/test_review.py ----
import inspect, numpy as np, pytest
from sklearn.linear_model import LogisticRegression
from llm_train import make_data, train

def test_no_leakage_on_pure_noise():
    # labels are coin flips, so any honest pipeline scores ~0.5. Averaging over 10 datasets removes luck.
    accs = [train(*make_data(s), "/tmp/_m.joblib")[1] for s in range(10)]
    assert np.mean(accs) < 0.65, f"mean accuracy {np.mean(accs):.2f} on noise labels = leakage"

def test_same_input_same_result():
    X, y = make_data()
    a = train(X, y, "/tmp/_m.joblib")[1]
    b = train(X, y, "/tmp/_m.joblib")[1]
    assert a == b, f"two runs differ ({a:.3f} vs {b:.3f}): no seed"

def test_model_file_really_written(tmp_path):
    X, y = make_data()
    target = tmp_path / "missing_dir" / "m.joblib"              # directory does not exist
    try:
        train(X, y, str(target))
    except OSError:
        return                                                   # failing LOUDLY is acceptable
    assert target.exists(), "save failed silently"

def test_invented_parameters_do_not_exist():
    # check the claim against the installed library, never against the LLM's confidence
    params = inspect.signature(LogisticRegression).parameters
    assert "class_weight" in params and "class_weights" not in params

# ---- q40/fixed/llm_train.py ----
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import joblib

def train(X, y, out_path, seed=0):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=seed)   # split FIRST, seeded
    model = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))  # selector fitted on train only
    model.fit(X_tr, y_tr)
    joblib.dump(model, out_path)         # let a failed save raise
    return model, model.score(X_te, y_te)

def make_data(seed=0):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(100, 2000)), rng.integers(0, 2, size=100)
```

**Output (my run):** (Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1). The pasted function was run directly, then `pytest` against it, then against the fixed version in `q40/fixed/` (selector inside a Pipeline after a seeded split, no try/except). The reported accuracy changes on every run of the buggy version because it is unseeded (0.70 and 0.73 in two earlier runs, 0.93 in the pasted one).
```text
accuracy 0.93  <- reported (the labels are coin flips)
E       AssertionError: mean accuracy 0.81 on noise labels = leakage
E       AssertionError: two runs differ (0.767 vs 0.867): no seed
>       assert target.exists(), "save failed silently"
E       AssertionError: save failed silently
FAILED test_review.py::test_no_leakage_on_pure_noise - AssertionError: mean a...
FAILED test_review.py::test_same_input_same_result - AssertionError: two runs...
FAILED test_review.py::test_model_file_really_written - AssertionError: save ...
3 failed, 1 passed in 1.52s
--- fixed version ---
4 passed in 1.47s
```

**Follow-ups:**
- *Would you ban AI-generated code?* No. I would require the same bar as any code: tests, review, pinned deps, and the author must be able to explain every line.
- *How do you catch invented packages?* Install from the lockfile in CI only, and have a review rule that new dependencies need a justification and a check on the package index page.
- *Is the leakage here that bad with real data?* It depends; with many features and few rows (as here) it is severe, and with large data it is smaller but still wrong.

**Common mistakes:**
- Trusting the printed metric.
- Reviewing only style, not data flow.
- Asking the LLM to confirm its own code is correct.
- Running the code once and calling it verified.
