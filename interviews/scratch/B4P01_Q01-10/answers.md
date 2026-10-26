### Q1 ⭐⭐⭐ 🟢 What should and should not go into a Git repository for an ML project? A team has code, a 400 MB parquet training file, a 1.2 GB model.pkl, a .env file with a cloud key and a notebook with outputs. Say what you commit, what you ignore (give the .gitignore lines), where the big files live instead (Git LFS versus a data versioning tool, in one line each), and what you do if the key was already pushed.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Git holds code, small configs and the lockfile; data and models go to a data store, secrets never go in, and a pushed key is treated as leaked, so I rotate it first and clean history second.

**Then explain:**
- **Commit:** source, tests, `params.yaml`, `requirements.txt` or a lockfile, `.gitignore`, `.env.example` (names only, no values), pointer files from DVC or LFS, and notebooks with outputs stripped.
- **Ignore:** `.env`, the 400 MB parquet, the 1.2 GB `model.pkl`, `__pycache__`, `.ipynb_checkpoints`, virtualenvs.
- **Big files, one line each:** Git LFS keeps a tiny pointer in Git and the real file on an LFS server (simple, but it versions files, not pipelines). A data versioning tool such as DVC keeps a small `.dvc` file in Git and the bytes in object storage, and also links data to the pipeline and params.
- **Why not just commit them:** every version of a big binary stays in history forever, clones get slow, and binaries do not diff or merge.
- **Key already pushed:** (1) revoke and rotate it now, because anyone who cloned has it; (2) then remove it from history with `git filter-repo --invert-paths --path <file>` (needs a fresh clone, rewrites all hashes, so the team must re-clone); (3) check the provider's access logs; (4) add a secret scanner (pre-commit or CI). Failure mode: deleting the file in a new commit does nothing, the old commit still has it.

**Example:** The team has `src/`, `params.yaml`, `data/train.parquet`, `models/model.pkl`, `.env`, `notebooks/eda.ipynb`. After the `.gitignore` below, `git ls-files` shows only code, params, requirements, the notebook, `.gitignore` and `.env.example`. `git check-ignore -v` prints the exact rule that hides each big file.

**Code:** the script runs in a temp repo with small stand-in files (400 KB and 1.2 MB, same names). The LFS step only writes `.gitattributes`; there is no LFS server here, so nothing was uploaded.
```bash
#!/usr/bin/env bash
# Q1: what goes in Git, .gitignore, LFS, and removing a pushed secret
set -e
# --- env.sh (shared setup, shown inline) ---
# shared env for git demos: isolated config, fixed dates so output is repeatable
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=Demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=Demo GIT_COMMITTER_EMAIL=demo@example.com
_t=1760000000
tick() { _t=$((_t+60)); export GIT_AUTHOR_DATE="$_t +0000" GIT_COMMITTER_DATE="$_t +0000"; }
c() { tick; git commit -q "$@"; }   # fixed-date commit
# --- end env.sh ---
W=$(mktemp -d); cd "$W"; git init -q -b main proj; cd proj
mkdir -p src data models notebooks
echo 'def train(): pass' > src/train.py
echo 'numpy==2.5.3' > requirements.txt
echo 'seed: 42' > params.yaml
head -c 400000 /dev/urandom > data/train.parquet      # stand-in for the 400 MB file
head -c 1200000 /dev/urandom > models/model.pkl        # stand-in for the 1.2 GB file
echo 'AWS_SECRET_ACCESS_KEY=FAKEKEY123' > .env
echo '{"cells":[]}' > notebooks/eda.ipynb
mkdir -p __pycache__ .ipynb_checkpoints; echo x > __pycache__/a.pyc
cat > .gitignore <<'G'
# secrets
.env
.env.*
!.env.example
# data and models (tracked by DVC or LFS instead)
data/
models/
*.pkl
*.parquet
# python and notebook noise
__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
G
echo 'AWS_SECRET_ACCESS_KEY=' > .env.example
echo '--- git status --short (what Git sees)'; git status --short
echo '--- git check-ignore -v (which rule hides each file)'
git check-ignore -v .env data/train.parquet models/model.pkl __pycache__/a.pyc
echo '--- commit, then show tracked files'
git add -A; c -m "initial: code, params, gitignore"; git ls-files
echo '--- the Git LFS alternative: track patterns, writes .gitattributes'
git lfs install --local >/dev/null; git lfs track "*.parquet" "*.pkl"; cat .gitattributes
echo '--- secret already committed: simulate the mistake'
echo 'AWS_SECRET_ACCESS_KEY=FAKEKEY123' > config.env; git add -f config.env; c -m "oops add key"
git log --oneline --all -- config.env
echo '--- rewrite history with git filter-repo (on a fresh clone, as the tool requires)'
cd "$W"; git clone -q proj clean; cd clean
git filter-repo --invert-paths --path config.env --force 2>&1 | tail -2
echo 'file in history after rewrite:'; git log --oneline --all -- config.env | wc -l
echo '(rotate the key anyway: anyone who pulled earlier still has it)'
rm -rf "$W"
```

**Output (my run):** git 2.43.0, git-lfs 3.4.1, git-filter-repo 2.47.0. The key in the demo is a fake string.
```text
--- git status --short (what Git sees)
?? .env.example
?? .gitignore
?? notebooks/
?? params.yaml
?? requirements.txt
?? src/
--- git check-ignore -v (which rule hides each file)
.gitignore:2:.env	.env
.gitignore:6:data/	data/train.parquet
.gitignore:7:models/	models/model.pkl
.gitignore:11:__pycache__/	__pycache__/a.pyc
--- commit, then show tracked files
.env.example
.gitignore
notebooks/eda.ipynb
params.yaml
requirements.txt
src/train.py
--- the Git LFS alternative: track patterns, writes .gitattributes
Tracking "*.parquet"
Tracking "*.pkl"
*.parquet filter=lfs diff=lfs merge=lfs -text
*.pkl filter=lfs diff=lfs merge=lfs -text
--- secret already committed: simulate the mistake
710aba9 oops add key
--- rewrite history with git filter-repo (on a fresh clone, as the tool requires)
HEAD is now at db0bfee initial: code, params, gitignore
Completely finished after 0.07 seconds.
file in history after rewrite:
0
(rotate the key anyway: anyone who pulled earlier still has it)
```

**Follow-ups:**
- *Git LFS or DVC?* LFS if you only need big files to behave inside Git hosting; DVC if you want data tied to pipelines, remotes you choose, and params. Check your Git host's LFS storage limits (they change).
- *Can I just `git rm` the file?* No. It stays in earlier commits. Rotate, then rewrite history.
- *What stops this next time?* A pre-commit secret scan, a CI scan, and short-lived credentials (roles, not long-lived keys).

**Common mistakes:**
- Cleaning history but never rotating the key.
- Adding `.gitignore` after the file was already committed (ignore rules do not affect tracked files; run `git rm --cached`).
- Committing model files "just this once" and then needing `filter-repo` to shrink the repo.
- Putting the real key in `.env.example`.

### Q2 ⭐⭐⭐ 🟢 Git basics under pressure. Explain commit, branch, HEAD and the staging area, the difference between git fetch and git pull, what a detached HEAD is and how you get out of it without losing work, and what git status, git diff and git diff --staged each show. Walk through a throwaway repo where you end up on a detached HEAD after checking out an old tag, make a commit, and save it to a branch.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A commit is a snapshot, a branch is a movable name for a commit, HEAD is "where I am now", and the staging area is the draft of the next commit; on a detached HEAD I make a branch with `git switch -c name` before leaving.

**Then explain:**
- **Staging area (index):** what the next commit will contain. `git add` copies changes into it.
- **`git fetch` vs `git pull`:** fetch only downloads and moves `origin/main`; my `main` does not move. `pull` is fetch plus merge (or rebase with `--rebase`). I fetch first when I want to look before I merge.
- **Detached HEAD:** HEAD points at a commit, not a branch (for example after `git checkout v1.0`). New commits there belong to no branch, so switching away leaves them reachable only through the reflog. Fix: `git switch -c hotfix-1.0` while still on them.
- **Status and diffs:** `git status` lists the state of files; `git diff` = working tree vs staging; `git diff --staged` = staging vs last commit. A file edited after `git add` shows as `MM` and appears in both diffs.
- Failure mode: committing on a detached HEAD, switching away, and "losing" the work (recoverable with `git reflog`, but only until it expires).

**Example:** Tag `v1.0` is the first model version. I check out the tag, fix something, commit, then run `git switch -c hotfix-1.0`. The graph shows `hotfix-1.0` hanging off v1 and `main` unchanged.

**Code:** temp repo, a second clone as "origin" side, fixed commit dates.
```bash
#!/usr/bin/env bash
# Q2: detached HEAD from an old tag, commit, save to a branch; status/diff/diff --staged; fetch vs pull
set -e
# --- env.sh (shared setup, shown inline) ---
# shared env for git demos: isolated config, fixed dates so output is repeatable
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=Demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=Demo GIT_COMMITTER_EMAIL=demo@example.com
_t=1760000000
tick() { _t=$((_t+60)); export GIT_AUTHOR_DATE="$_t +0000" GIT_COMMITTER_DATE="$_t +0000"; }
c() { tick; git commit -q "$@"; }   # fixed-date commit
# --- end env.sh ---
W=$(mktemp -d); cd "$W"
git init -q -b main origin_repo; cd origin_repo
echo "v1" > model.txt; git add .; c -m "model v1"; git tag v1.0
echo "v2" > model.txt; git add .; c -m "model v2"
cd "$W"; git clone -q origin_repo work; cd work
echo '--- fetch vs pull: someone pushes to origin, then we fetch'
(cd ../origin_repo && echo "v3" > model.txt && git add . && c -m "model v3")
git fetch -q; echo "main (mine):   $(git rev-parse --short main)"; echo "origin/main:   $(git rev-parse --short origin/main)  <- fetch only updated this pointer"
git log --oneline main..origin/main
git pull -q; echo "after pull, main = $(git rev-parse --short main)  (pull = fetch + merge)"
echo '--- status / diff / diff --staged'
echo "edit1" >> model.txt; git diff --stat
git add model.txt; echo "edit2" >> model.txt
echo "[git status --short]"; git status --short
echo "[git diff = working tree vs index]"; git diff | grep '^[+-][^+-]'
echo "[git diff --staged = index vs HEAD]"; git diff --staged | grep '^[+-][^+-]'
git restore --staged model.txt; git checkout -q -- model.txt   # clean up
echo '--- detached HEAD'
git checkout -q v1.0 2>&1 || true
git status | head -1; echo "HEAD file says: $(cat model.txt)"
echo "hotfix" > model.txt; git add .; c -m "hotfix on old release"
echo "commit made on detached HEAD: $(git rev-parse --short HEAD)"
echo "[escape: branch it before leaving]"
git switch -q -c hotfix-1.0; git branch --show-current
git switch -q main; git branch -v
git log --oneline --graph --all
rm -rf "$W"
```

**Output (my run):** git 2.43.0.
```text
--- fetch vs pull: someone pushes to origin, then we fetch
main (mine):   0d8a57d
origin/main:   7bb1770  <- fetch only updated this pointer
7bb1770 model v3
after pull, main = 7bb1770  (pull = fetch + merge)
--- status / diff / diff --staged
 model.txt | 1 +
 1 file changed, 1 insertion(+)
[git status --short]
MM model.txt
[git diff = working tree vs index]
+edit2
[git diff --staged = index vs HEAD]
+edit1
--- detached HEAD
HEAD detached at v1.0
HEAD file says: v1
commit made on detached HEAD: ef587e9
[escape: branch it before leaving]
hotfix-1.0
  hotfix-1.0 ef587e9 hotfix on old release
* main       7bb1770 model v3
* ef587e9 hotfix on old release
| * 7bb1770 model v3
| * 0d8a57d model v2
|/  
* cb098c3 model v1
```

**Follow-ups:**
- *I already switched away from the detached commit. Now what?* `git reflog`, find the hash, `git branch rescue <hash>`.
- *Why fetch before pull?* To see incoming commits (`git log main..origin/main`) and avoid a surprise merge.
- *`switch` vs `checkout`?* `switch` moves between branches, `restore` fixes files; `checkout` did both, so it was split. Both still work.

**Common mistakes:**
- Ignoring the "detached HEAD" message and carrying on.
- Thinking `git diff` shows staged changes (it does not; use `--staged`).
- Running `git pull` on a dirty tree and getting a conflict mid-merge.

### Q3 ⭐⭐⭐ 🟢 Git merge versus rebase versus squash merge. Two data scientists branch from main to add features; one finishes first. Explain what each strategy does to history, which you would use for a private feature branch and which for a shared branch, and why you never rebase a branch others have pulled. Show a 3-commit example in a throwaway repo and the resulting git log --oneline --graph for each strategy.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Merge keeps history as it happened, rebase replays my commits on top of main for a straight line, squash merge collapses the branch into one commit; I rebase private branches, merge or squash shared ones, and I never rebase what others have pulled.

**Then explain:**
- **Merge (`--no-ff`):** adds a merge commit with two parents. Nothing is rewritten, so it is safe on shared branches. History has side branches.
- **Rebase:** copies my commits onto the new tip of main. Commits get new hashes; the old ones become unreachable. History is linear. Conflicts may appear commit by commit.
- **Squash merge:** all feature commits become one new commit on main. Clean main log, but the individual steps and their authors are not on main, and the feature branch is no longer "merged" in Git's eyes (do not reuse it).
- **Why not rebase shared branches:** rebase rewrites hashes. A teammate who pulled the old commits now has history that disagrees with yours. Pushing needs `--force`, they get duplicate commits or conflicts. If you must, use `--force-with-lease` and tell them.
- **Practical rule:** before opening a PR I rebase my private branch on the latest main; the team's PR button uses merge or squash (a team policy, check your repo settings).

**Example:** `A` is the base. Main gets `M1`. My branch has `F1 F2 F3`. Merge gives a diamond with a merge commit; rebase gives `A M1 F1' F2' F3'`; squash gives `A M1 S`, where `S` has all three changes.

**Code:** one setup function, run three times in a temp repo.
```bash
#!/usr/bin/env bash
# Q3: three strategies, same 3-commit situation. main has 1 commit after the branch point; feature has 3.
set -e
# --- env.sh (shared setup, shown inline) ---
# shared env for git demos: isolated config, fixed dates so output is repeatable
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=Demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=Demo GIT_COMMITTER_EMAIL=demo@example.com
_t=1760000000
tick() { _t=$((_t+60)); export GIT_AUTHOR_DATE="$_t +0000" GIT_COMMITTER_DATE="$_t +0000"; }
c() { tick; git commit -q "$@"; }   # fixed-date commit
# --- end env.sh ---
W=$(mktemp -d); cd "$W"
setup() {
  rm -rf r; git init -q -b main r; cd r
  echo base > base.txt; git add .; c -m "A base"
  git switch -q -c feature
  echo f1 > f1.txt; git add .; c -m "F1 add feature"
  echo f2 > f2.txt; git add .; c -m "F2 fix typo"
  echo f3 > f3.txt; git add .; c -m "F3 add tests"
  git switch -q main
  echo m1 > m1.txt; git add .; c -m "M1 teammate lands on main"
}
echo "=== 1. merge (merge commit, history kept as it happened)"
setup; c_=1; tick; git merge -q --no-ff feature -m "Merge feature"; git log --oneline --graph; cd ..
echo; echo "=== 2. rebase feature onto main, then fast-forward (linear, commits rewritten)"
setup; git switch -q feature; git rebase -q main; git switch -q main; git merge -q --ff-only feature
git log --oneline --graph; echo "(F1-F3 got new hashes; originals are no longer on any branch)"; cd ..
echo; echo "=== 3. squash merge (one new commit, feature commits not in main history)"
setup; git merge -q --squash feature; c -m "Add feature (squashed F1-F3)"; git log --oneline --graph
echo "feature branch still points at its own 3 commits: $(git log --oneline main..feature | wc -l) not in main"; cd ..
rm -rf "$W"
```

**Output (my run):** git 2.43.0, fixed dates so hashes repeat on a rerun with this git version.
```text
=== 1. merge (merge commit, history kept as it happened)
*   badcc03 Merge feature
|\  
| * 44f35b8 F3 add tests
| * ce2219f F2 fix typo
| * b8b618d F1 add feature
* | c6bd3a4 M1 teammate lands on main
|/  
* 6fe3137 A base

=== 2. rebase feature onto main, then fast-forward (linear, commits rewritten)
* 304dcb0 F3 add tests
* 7d39549 F2 fix typo
* 7399d91 F1 add feature
* fcaa03f M1 teammate lands on main
* e7b2410 A base
(F1-F3 got new hashes; originals are no longer on any branch)

=== 3. squash merge (one new commit, feature commits not in main history)
Automatic merge went well; stopped before committing as requested
Squash commit -- not updating HEAD
* 12c2b68 Add feature (squashed F1-F3)
* 731e5dc M1 teammate lands on main
* 8b5af45 A base
feature branch still points at its own 3 commits: 3 not in main
```

**Follow-ups:**
- *When do you prefer squash?* Noisy WIP commits ("fix typo", "oops"); one PR = one commit makes `git revert` of the whole feature a single command.
- *When do you avoid it?* When individual commits matter for `git bisect` or attribution.
- *What does `git pull --rebase` do?* Fetches, then rebases my local commits on top of the remote branch instead of making a merge commit.

**Common mistakes:**
- Rebasing a branch someone else branched from.
- Squashing and then continuing work on the same feature branch (it re-conflicts with itself).
- Resolving rebase conflicts with `--skip` and silently dropping a commit.

### Q4 ⭐⭐⭐ 🟢 git reset versus git revert versus git restore. A bad commit that changes the feature scaling was pushed to main and two teammates pulled it. Which command do you use to undo it and why? Also explain --soft, --mixed and --hard in one line each, and what git restore does to a single file. Demonstrate on a throwaway repo.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** The bad commit is already on main and two people pulled it, so I use `git revert`, which adds a new commit that undoes it and rewrites nothing; `reset` is for my own unpushed work and `restore` is for files.

**Then explain:**
- **`git revert <commit>`:** creates an inverse commit. History stays honest, teammates just pull. Reverting a merge commit needs `-m 1`. If later commits touched the same lines, expect a conflict.
- **`git reset`** moves the branch pointer. `--soft`: move the pointer only (changes stay staged). `--mixed` (default): move the pointer and unstage (changes stay in files). `--hard`: move the pointer and throw the changes away.
- **Why not reset here:** after `reset` plus a force push, the two teammates still hold the bad commit and will push it back.
- **`git restore <file>`:** puts one file back from the index (or `--source=<commit>` from any commit); it does not touch history. `--staged` unstages.
- Failure mode: `reset --hard` on uncommitted work cannot be undone (see reflog question for committed work).

**Example:** Three commits: good scaling, BAD scaling, later work. Revert of the BAD commit gives `scaler=standard` again while the later work (`train.py` v2) stays.

**Code:**
```bash
#!/usr/bin/env bash
# Q4: undo a pushed bad commit with revert; reset modes; restore a single file
set -e
# --- env.sh (shared setup, shown inline) ---
# shared env for git demos: isolated config, fixed dates so output is repeatable
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=Demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=Demo GIT_COMMITTER_EMAIL=demo@example.com
_t=1760000000
tick() { _t=$((_t+60)); export GIT_AUTHOR_DATE="$_t +0000" GIT_COMMITTER_DATE="$_t +0000"; }
c() { tick; git commit -q "$@"; }   # fixed-date commit
# --- end env.sh ---
W=$(mktemp -d); cd "$W"; git init -q -b main r; cd r
echo "scaler=standard" > cfg.txt; echo "v1" > train.py; git add .; c -m "good: standard scaling"
echo "scaler=NONE" > cfg.txt; git add .; c -m "BAD: change feature scaling"
echo "v2" > train.py; git add .; c -m "later work on top"
echo "--- pushed history"; git log --oneline
echo "--- revert the bad commit (safe on shared branch: adds a new commit)"
git revert --no-edit HEAD~1 >/dev/null; tick; git log --oneline; echo "cfg now: $(cat cfg.txt), train.py kept: $(cat train.py)"
echo; echo "--- reset modes on an UNPUSHED local commit"
git branch -f keep main
for mode in soft mixed hard; do
  git reset -q --hard keep
  echo "$mode-change" > x.txt; git add .; c -m "local commit"
  git reset --$mode HEAD~1 >/dev/null
  echo "reset --$mode HEAD~1 -> commit undone: yes | staged: '$(git diff --cached --name-only)' | file on disk: '$(cat x.txt 2>/dev/null || echo MISSING)'"
done
git reset -q --hard keep
echo; echo "--- restore a single file"
echo "scratch edit" > train.py; git status --short
git restore train.py; echo "after git restore train.py: $(cat train.py); status: '$(git status --short)'"
echo "restore from an older commit: git restore --source=HEAD~3 cfg.txt"
git restore --source=HEAD~3 cfg.txt; cat cfg.txt   # HEAD~3 here is the good commit
rm -rf "$W"
```

**Output (my run):** git 2.43.0.
```text
--- pushed history
c0fe011 later work on top
edd99e7 BAD: change feature scaling
e40b684 good: standard scaling
--- revert the bad commit (safe on shared branch: adds a new commit)
5bdad13 Revert "BAD: change feature scaling"
c0fe011 later work on top
edd99e7 BAD: change feature scaling
e40b684 good: standard scaling
cfg now: scaler=standard, train.py kept: v2

--- reset modes on an UNPUSHED local commit
reset --soft HEAD~1 -> commit undone: yes | staged: 'x.txt' | file on disk: 'soft-change'
reset --mixed HEAD~1 -> commit undone: yes | staged: '' | file on disk: 'mixed-change'
reset --hard HEAD~1 -> commit undone: yes | staged: '' | file on disk: 'MISSING'

--- restore a single file
 M train.py
after git restore train.py: v2; status: ''
restore from an older commit: git restore --source=HEAD~3 cfg.txt
scaler=standard
```

**Follow-ups:**
- *Can I get the feature back later?* Yes, revert the revert, or cherry-pick the original.
- *When is `reset` fine on shared history?* Almost never; only on a private branch nobody pulled.
- *How do I find which commit broke scaling?* `git bisect` with a test script.

**Common mistakes:**
- Force-pushing a reset to undo a pushed commit.
- Using `reset --hard` to "unstage".
- Forgetting that `revert` of a merge commit needs `-m`.

### Q5 ⭐⭐⭐ 🟡 How do you make a trained model reproducible six months later? List exactly what you record per training run (code commit, data version, dependency lockfile, config and hyperparameters, random seeds, hardware notes, metrics, artifact hash) and show a small Python function that writes this run manifest as JSON. Say which parts Git can hold and which need other tools, and what still breaks reproducibility (GPU nondeterminism, floating point, unpinned system libraries).
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** For every run I record the code commit (plus a dirty flag), a content hash of the data, the lockfile, config and seeds, hardware and library versions, metrics and a hash of the model file, so I can rebuild the same model or at least explain why I cannot.

**Then explain:**
- **What to record:** git commit and "dirty?", data version (content hash or DVC/lakeFS id), dependency lockfile hash, config and hyperparameters, seeds, Python/OS/GPU/driver/CUDA, metrics, model artifact hash, run date.
- **Git can hold:** code, config, lockfile, the small manifest itself. **Other tools:** data (DVC, object store with versioning), models (registry or artifact store), metrics and runs (experiment tracker), environment (Docker image digest).
- **What still breaks it:** GPU kernels that are nondeterministic (some CUDA ops add floats in varying order; frameworks have a deterministic mode that is slower or limited, check current docs), floating point differing across CPUs and thread counts, unpinned system libraries (CUDA, BLAS, libc), data edited in place, unseeded libraries (data loader workers), time-dependent features.
- **Honest target:** bit-exact is a bonus. Minimum: same data, code and env give metrics within a stated tolerance.
- Failure mode: a manifest written from a dirty working tree names a commit that does not match what ran. Store the dirty flag, or refuse to train when dirty.

**Example:** `run.json` says commit `760ecc4`, data hash `2a2b86...`, `numpy 2.5.3`, seed 42, `auc 0.91`, model hash. Six months later I check out that commit, fetch the data with that hash, install the pinned versions, rerun, and compare the model hash or metric.

**Code:** `python3 -I`; uses a temp git repo and a stand-in model file (random bytes from a seeded generator).
```python
# ===== q05_run_manifest.py =====
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
```

**Output (my run):** Python 3.13.17, numpy 2.5.3.
```text
{
  "config": {
    "lr": 0.1,
    "max_depth": 4
  },
  "data": {
    "train.csv": "2a2b86e74ffd5e6a9b75e52a105cf9d02920837179f8e8961aa15411d380f7a3"
  },
  "git": {
    "commit": "760ecc4f61526c1dcef5bb661299ca4c732265ae",
    "dirty": false
  },
  "hardware": {
    "gpu": "none (this demo)",
    "machine": "x86_64",
    "os": "<os string>",
    "python": "3.13.17"
  },
  "metrics": {
    "auc": 0.91
  },
  "model_sha256": "51f4c7fe675c87ed8c398050bf3d366eb64a2928b6cacd48eb72e92e62c0c6b3",
  "packages": {
    "numpy": "2.5.3"
  },
  "seed": 42
}
model bytes identical on rerun with same seed: True
```

**Follow-ups:**
- *Is a seed enough?* No. It controls randomness, not the data, code, library versions or GPU kernels.
- *Where is the manifest stored?* Next to the model artifact and in the tracker; also logged in the registry entry.
- *Docker?* It pins the environment (store the image digest), but not data or hardware.

**Common mistakes:**
- Recording a branch name instead of a commit hash.
- "Data v2" as a folder name, not a content hash.
- Pinning direct dependencies only (no lockfile for transitive ones).
- Promising bit-exact results on GPU.

### Q6 ⭐⭐⭐ 🟡 You ran git reset --hard HEAD~2 by mistake and lost two commits of a training script that were never pushed. Recover them using git reflog, in a reproducible demo on a throwaway repo. Also say how long reflog entries last by default (hedge: check current docs), what reflog cannot recover (uncommitted changes, never-staged files) and how git stash fits in.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Nothing is gone yet: `git reflog` lists where HEAD has been, so I find the commit I had before the reset and move the branch back to it (or hang a rescue branch on it).

**Then explain:**
- `reset --hard HEAD~2` moves the branch back two commits. The two commits still exist as objects; they are just unreachable from any branch.
- `git reflog` shows each HEAD move with `HEAD@{n}`. I pick the entry from before the reset (`HEAD@{1}` here) and run `git reset --hard <hash>` or, safer, `git branch rescue <hash>`.
- **How long:** reflog entries expire; commonly stated defaults are about 90 days for reachable entries and 30 days for unreachable ones (`gc.reflogExpire`, `gc.reflogExpireUnreachable`). I could not verify the numbers on this machine, so check the current git-config docs. `git gc` can then delete the objects.
- **What reflog cannot recover:** edits never committed (in my run the tracked unstaged edit was gone after `reset --hard`), files that were never staged or committed in the first place, and a different clone's reflog (reflog is local).
- **Stash:** `git stash` parks uncommitted work safely before risky commands; `git stash pop` brings it back.

**Example:** `c0 baseline`, `c1 add cross validation`, `c2 add early stopping`. After the mistaken reset only `c0` shows. The reflog still lists `c2` at `HEAD@{1}`; resetting to that hash brings back both commits and the file says `step2`.

**Code:**
```bash
#!/usr/bin/env bash
# Q6: lose two commits with reset --hard, recover with reflog
set -e
# --- env.sh (shared setup, shown inline) ---
# shared env for git demos: isolated config, fixed dates so output is repeatable
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=Demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=Demo GIT_COMMITTER_EMAIL=demo@example.com
_t=1760000000
tick() { _t=$((_t+60)); export GIT_AUTHOR_DATE="$_t +0000" GIT_COMMITTER_DATE="$_t +0000"; }
c() { tick; git commit -q "$@"; }   # fixed-date commit
# --- end env.sh ---
W=$(mktemp -d); cd "$W"; git init -q -b main r; cd r
echo "step0" > train.py; git add .; c -m "c0 baseline"
echo "step1: add cv" > train.py; git add .; c -m "c1 add cross validation"
echo "step2: add early stopping" > train.py; git add .; c -m "c2 add early stopping"
echo "--- before the mistake"; git log --oneline
git reset --hard HEAD~2
echo "--- after git reset --hard HEAD~2 (commits look gone)"; git log --oneline; cat train.py
echo "--- git reflog"; git reflog
LOST=$(git reflog | grep 'c2 add early stopping' | awk '{print $1}')
echo "lost tip is $LOST"
git reset --hard "$LOST" >/dev/null
echo "--- recovered"; git log --oneline; cat train.py
echo "--- safer: branch from the reflog entry instead of moving main"
git reset -q --hard HEAD~2; git branch rescue HEAD@{1}; git log --oneline rescue | head -1
echo "--- what reflog cannot save: uncommitted work"
git switch -q main; echo "never committed" > scratch.py; echo "edited, unstaged" >> train.py
git reset --hard HEAD >/dev/null
echo "scratch.py (untracked) survives reset --hard: $(ls scratch.py)"; echo "tracked unstaged edit is gone: train.py = $(cat train.py)"
echo "--- stash keeps uncommitted work"
echo "wip" >> train.py; git stash -q; echo "train.py after stash: $(cat train.py)"; git stash pop -q; echo "after pop: $(tail -1 train.py)"
rm -rf "$W"
```

**Output (my run):** git 2.43.0.
```text
--- before the mistake
80b92af c2 add early stopping
d542e02 c1 add cross validation
5530887 c0 baseline
HEAD is now at 5530887 c0 baseline
--- after git reset --hard HEAD~2 (commits look gone)
5530887 c0 baseline
step0
--- git reflog
5530887 HEAD@{0}: reset: moving to HEAD~2
80b92af HEAD@{1}: commit: c2 add early stopping
d542e02 HEAD@{2}: commit: c1 add cross validation
5530887 HEAD@{3}: commit (initial): c0 baseline
lost tip is 80b92af
--- recovered
80b92af c2 add early stopping
d542e02 c1 add cross validation
5530887 c0 baseline
step2: add early stopping
--- safer: branch from the reflog entry instead of moving main
80b92af c2 add early stopping
--- what reflog cannot save: uncommitted work
scratch.py (untracked) survives reset --hard: scratch.py
tracked unstaged edit is gone: train.py = step0
--- stash keeps uncommitted work
train.py after stash: step0
after pop: wip
```

**Follow-ups:**
- *Reflog in a fresh clone?* Empty; recovery only works where the work happened.
- *Dropped stash?* `git fsck --unreachable` can find it; not guaranteed.
- *How do you avoid this?* Make a safety branch (`git branch backup`) before any `reset --hard` or rebase.

**Common mistakes:**
- Running `git gc --prune=now` before checking the reflog.
- Believing untracked files can be recovered by git (never added means never stored).
- Resetting `main` to the rescued hash without first checking `git log` on it.

### Q7 ⭐⭐⭐ 🟡 Jupyter notebooks and Git. Two people edit the same notebook and every pull gives a conflict in the JSON, with outputs and execution counts changing. Explain how you keep notebooks reviewable: stripping outputs with nbstripout or a pre-commit hook, pairing with a .py file using jupytext, and when a notebook should not be in the repo at all. Show the commands and a before and after of the diff size on a small notebook.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** Notebooks are JSON with outputs and counters, so I strip outputs before commit (nbstripout), review a paired `.py` (jupytext), and keep real logic in modules, not in notebooks.

**Then explain:**
- **Why diffs explode:** execution counts, embedded images (base64) and outputs change on every re-run, even with no code change. Two people editing means conflicts in JSON that no human wants to resolve.
- **nbstripout:** removes outputs and counts. `nbstripout --install` sets a Git filter in this clone (the `.git/config` part is per clone, so also add it to onboarding or a pre-commit hook; the pre-commit hook needs hook repos from the network, so it was not run here).
- **jupytext:** pairs `eda.ipynb` with `eda.py` in percent format; reviewers read the `.py`, and a conflict in a `.py` file is a normal text conflict.
- **When a notebook should not be in the repo:** throwaway exploration, anything with PII or real customer rows in the outputs, and anything the pipeline depends on (move the code to a module with tests and call it from the notebook).
- Trade-off: stripped notebooks lose the plots. For a report that must show results, commit rendered HTML or outputs deliberately, or publish from CI.
- Failure mode: a hook that is not installed on a teammate's machine, so outputs sneak back in. Add a CI check that fails if a committed notebook has outputs.

**Example:** I committed a notebook with two cells and a fake 13 KB image. A teammate re-ran it with no code change. Plain Git: 40 diff lines, about 28 KB. After stripping both versions: the diff is empty, and the file shrinks from about 14.5 KB to 0.6 KB. The sizes come from this synthetic notebook, not a real project.

**Code:** the script builds a notebook with Python, diffs raw vs stripped, installs the filter, and pairs with jupytext.
```bash
#!/usr/bin/env bash
# Q7: notebook diffs: raw vs nbstripout vs jupytext
set -e
# --- env.sh (shared setup, shown inline) ---
# shared env for git demos: isolated config, fixed dates so output is repeatable
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=Demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=Demo GIT_COMMITTER_EMAIL=demo@example.com
_t=1760000000
tick() { _t=$((_t+60)); export GIT_AUTHOR_DATE="$_t +0000" GIT_COMMITTER_DATE="$_t +0000"; }
c() { tick; git commit -q "$@"; }   # fixed-date commit
# --- end env.sh ---
W=$(mktemp -d); cd "$W"; git init -q -b main r; cd r
python3 -I - <<'PY'
import json, base64
def nb(count, value):
    fake_png = base64.b64encode(bytes(range(256)) * 40).decode()      # ~13 KB fake plot
    cells = [
      {"cell_type":"code","id":"cell0001","execution_count":count,"metadata":{},"source":["import numpy as np\n","x = np.arange(5)\n","x.mean()"],
       "outputs":[{"output_type":"execute_result","execution_count":count,"data":{"text/plain":[str(value)]},"metadata":{}}]},
      {"cell_type":"code","id":"cell0002","execution_count":count+1,"metadata":{},"source":["plot()"],
       "outputs":[{"output_type":"display_data","data":{"image/png":fake_png,"text/plain":["<Figure>"]},"metadata":{}}]},
    ]
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
            "language_info":{"name":"python"}},"nbformat":4,"nbformat_minor":5}
json.dump(nb(1, 2.0), open("a.ipynb","w"), indent=1)
json.dump(nb(7, 2.0), open("b.ipynb","w"), indent=1)   # same code, re-run: only counts differ (+ image bytes re-rendered)
PY
cp a.ipynb eda.ipynb; git add eda.ipynb; c -m "notebook v1 (raw, with outputs)"
# teammate re-runs everything: new execution counts and a re-rendered image
python3 -I - <<'PY'
import json, base64
d = json.load(open("b.ipynb")); d["cells"][1]["outputs"][0]["data"]["image/png"] = base64.b64encode(bytes(range(255,-1,-1))*40).decode()
json.dump(d, open("eda.ipynb","w"), indent=1)
PY
echo "=== RAW notebook: diff after a plain re-run (no code change)"
git diff --stat; echo "diff lines: $(git diff | wc -l), diff bytes: $(git diff | wc -c)"
git add eda.ipynb; c -m "notebook v2 (raw re-run)"
echo; echo "=== STRIPPED: nbstripout on both versions"
git show HEAD~1:eda.ipynb | nbstripout > s1.ipynb
nbstripout < eda.ipynb > s2.ipynb
echo "size raw=$(wc -c < eda.ipynb) bytes, stripped=$(wc -c < s2.ipynb) bytes"
echo "diff lines between stripped v1 and stripped v2: $(diff s1.ipynb s2.ipynb | wc -l)  (re-run noise gone)"
echo; echo "=== install as a git filter so you cannot forget (writes .git/config + .git/info/attributes)"
nbstripout --install >/dev/null; grep -A3 'filter "nbstripout"' .git/config | head -4; cat .git/info/attributes   # per-clone; commit a .gitattributes line too so teammates get it
echo; echo "=== JUPYTEXT: pair with a .py file, review the .py"
jupytext --set-formats ipynb,py:percent eda.ipynb 2>&1 | tail -1   # pair them
jupytext --sync eda.ipynb 2>&1 | tail -1                           # keeps both files in step
git status --short
cat eda.py
echo "py size=$(wc -c < eda.py) bytes vs ipynb=$(wc -c < eda.ipynb) bytes"
rm -rf "$W"
```

**Output (my run):** nbstripout 0.9.1, jupytext 1.19.6, git 2.43.0. `git status` at the end is noisy because the demo keeps helper files in the repo.
```text
=== RAW notebook: diff after a plain re-run (no code change)
 eda.ipynb | 8 ++++----
 1 file changed, 4 insertions(+), 4 deletions(-)
diff lines: 40, diff bytes: 28133

=== STRIPPED: nbstripout on both versions
size raw=14562 bytes, stripped=566 bytes
diff lines between stripped v1 and stripped v2: 0  (re-run noise gone)

=== install as a git filter so you cannot forget (writes .git/config + .git/info/attributes)
[filter "nbstripout"]
	clean = \"/usr/bin/python3\" -m nbstripout
	smudge = cat
	required = true
*.ipynb filter=nbstripout
*.zpln filter=nbstripout
*.ipynb diff=ipynb

=== JUPYTEXT: pair with a .py file, review the .py
[jupytext] Updating eda.py
[jupytext] Unchanged eda.py
 M eda.ipynb
?? a.ipynb
?? b.ipynb
?? eda.py
?? s1.ipynb
?? s2.ipynb
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import numpy as np
x = np.arange(5)
x.mean()

# %%
plot()
py size=363 bytes vs ipynb=14617 bytes
```

**Follow-ups:**
- *Why not `.ipynb` diff tools only?* They help reading but do not fix merge conflicts or repo bloat.
- *Reproducibility without outputs?* Re-run in CI (for example with papermill or nbconvert) and publish artefacts.
- *Does jupytext lose outputs?* The `.py` has none; the `.ipynb` keeps them locally.

**Common mistakes:**
- Stripping outputs but still committing notebooks with secrets in code cells.
- Installing nbstripout only on one laptop.
- Keeping training code only in a notebook.

### Q8 ⭐⭐⭐ 🟡 Write pytest unit tests for a preprocessing function. Given def impute_and_scale(df, cols) that fills NaN with the column median and then standardises, write tests covering: normal data with known hand-computed output, a column that is all NaN, a constant column (zero variance), an empty DataFrame, an input DataFrame that must not be mutated, and a dtype check on the output. Use parametrize for the edge cases and say what the function should do in each (raise or return) and why.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** I test `impute_and_scale` with hand-computed numbers plus one test per edge case, and I decide up front what each edge case does: raise on all-NaN and constant columns, return an empty frame for no rows, never mutate the input.

**Then explain:**
- **Known values:** `[1, NaN, 3]`: median 2, so `[1, 2, 3]`, mean 2, population std `sqrt(2/3)`, result `[-1.2247, 0, 1.2247]`. Check by hand, not by copying the function's output.
- **All-NaN column:** no median exists. Raise `ValueError`; silently returning NaN hides a broken upstream feed.
- **Constant column:** std is 0, so dividing gives NaN or inf. Raise (a team could instead return zeros; the point is to choose and test it). Also a column that becomes constant after imputing.
- **Empty DataFrame:** nothing to learn from; return an empty float frame so pipelines do not crash on a quiet day. State it in the docstring.
- **No mutation and dtype:** `df.copy()` first; test with `assert_frame_equal` against a deep copy. Integers come back as `float64`.
- A test that fails on a sample-std bug proves the tests are doing work (see output).

**Example:** For `a = [1, NaN, 3]` the test expects `[-1/s, 0, 1/s]` with `s = sqrt(2/3)`. A version using sample std (`ddof=1`) gives about `±1.0` instead and fails.

**Code:** one file shown here for reading; in the repo it is `prep.py` and `test_prep.py`.
```python
# ===== q08/prep.py =====
import pandas as pd


def impute_and_scale(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Fill NaN with the column median, then standardise (mean 0, std 1, population std).

    Returns a NEW frame; the input is never changed.
    Raises ValueError for: missing columns, all-NaN column, zero-variance column.
    An empty frame (no rows) is returned as an empty float frame for those columns.
    """
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    out = df.copy()
    if len(out) == 0:
        out[cols] = out[cols].astype("float64")
        return out
    for c in cols:
        s = out[c].astype("float64")
        if s.isna().all():
            raise ValueError(f"column {c!r} is all NaN: no median to impute")
        s = s.fillna(s.median())
        std = s.std(ddof=0)
        if std == 0:
            raise ValueError(f"column {c!r} is constant: cannot standardise (std = 0)")
        out[c] = (s - s.mean()) / std
    return out

# ===== q08/test_prep.py =====
import numpy as np
import pandas as pd
import pytest

from prep import impute_and_scale


def test_known_values_by_hand():
    # a = [1, NaN, 3] -> median 2 -> [1,2,3] -> mean 2, pop std sqrt(2/3)
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    out = impute_and_scale(df, ["a"])
    s = np.sqrt(2 / 3)
    np.testing.assert_allclose(out["a"].to_numpy(), [-1 / s, 0.0, 1 / s])


def test_output_is_standardised():
    df = pd.DataFrame({"a": [1.0, 2.0, 4.0, 8.0, np.nan]})
    out = impute_and_scale(df, ["a"])
    assert out["a"].mean() == pytest.approx(0.0, abs=1e-12)
    assert out["a"].std(ddof=0) == pytest.approx(1.0)
    assert not out["a"].isna().any()


@pytest.mark.parametrize(
    "data, why",
    [
        ({"a": [np.nan, np.nan, np.nan]}, "all NaN"),
        ({"a": [5.0, 5.0, 5.0]}, "constant"),
        ({"a": [5.0, np.nan, 5.0]}, "constant after imputing"),
    ],
)
def test_bad_columns_raise(data, why):
    with pytest.raises(ValueError):
        impute_and_scale(pd.DataFrame(data), ["a"])


def test_missing_column_raises():
    with pytest.raises(ValueError, match="missing columns"):
        impute_and_scale(pd.DataFrame({"a": [1.0, 2.0]}), ["b"])


def test_empty_frame_returns_empty_floats():
    df = pd.DataFrame({"a": pd.Series([], dtype="int64")})
    out = impute_and_scale(df, ["a"])
    assert len(out) == 0 and out["a"].dtype == np.float64


def test_input_not_mutated():
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [1, 2, 3]})
    before = df.copy(deep=True)
    impute_and_scale(df, ["a"])
    pd.testing.assert_frame_equal(df, before)


def test_dtype_is_float_even_for_int_input_and_other_cols_untouched():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    out = impute_and_scale(df, ["a"])
    assert out["a"].dtype == np.float64
    assert out["b"].tolist() == ["x", "y", "z"]
```
```bash
#!/usr/bin/env bash
# Q8: run the tests, then prove they catch a bug (mutation: sample std instead of population std)
D=$(dirname "$(readlink -f "$0")")/q08; T=$(mktemp -d); cp "$D"/prep.py "$D"/test_prep.py "$T"; cd "$T"
echo "=== correct code"; python3 -I -m pytest -q -p no:cacheprovider 2>&1 | tail -3
sed -i 's/std = s.std(ddof=0)/std = s.std()/' prep.py
echo "=== injected bug (std with ddof=1)"; python3 -I -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-110
rm -rf "$T"
```

**Output (my run):** pytest 9.1.1, pandas 3.0.5, numpy 2.5.3, Python 3.13.17 (`python3 -I -m pytest`). Second run is the same code with the sample-std bug injected.
```text
=== correct code
.........                                                                [100%]
9 passed in 0.46s
=== injected bug (std with ddof=1)
E         comparison failed
FAILED test_prep.py::test_known_values_by_hand - AssertionError: 
FAILED test_prep.py::test_output_is_standardised - assert np.float64(0.894427...
2 failed, 7 passed in 0.42s
```

**Follow-ups:**
- *Why `approx` and `assert_allclose`?* Floats; exact equality breaks on rounding.
- *How would you add property tests?* Hypothesis: for any non-constant numeric column, output mean is about 0 and std about 1.
- *Why not raise on empty?* A design choice; either is fine if it is documented and tested.

**Common mistakes:**
- Expected values copied from the function's own output.
- Testing only the happy path.
- Forgetting that imputing can create a constant column.
- Mutating the caller's frame (the SettingWithCopy family of bugs).

### Q9 ⭐⭐⭐ 🟡 The testing pyramid for ML code. Describe unit tests, data tests, model tests and integration tests, give one concrete example of each for a churn model, and say which run on every pull request, which nightly and which only before release (with a rough time budget per stage). Explain why a normal software test suite is not enough for ML (nothing fails loudly when data silently changes).
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Four layers: unit tests for small functions, data tests for schema and ranges, model tests for behaviour after a fit, and integration tests for the whole path; fast layers on every PR, slower ones nightly or before release, because ML fails silently when data changes.

**Then explain:**
- **Unit (every PR):** one function, hand-checkable. Churn: a ratio feature does not divide by zero tenure.
- **Data (every PR on a small sample, and on every new data drop):** schema, nulls, ranges, label balance, units. Churn: `monthly_spend` stays in a plausible band.
- **Model (nightly, or on PR if cheap):** needs a fit. Churn: AUC beats a floor the team chose; more support calls never lowers the churn score; same seed gives the same predictions.
- **Integration (nightly / before release):** raw data to saved model to loaded model to prediction for new rows; later also the serving API and a canary comparison.
- **Rough budgets (team choices, not rules):** unit and data seconds to about a minute per PR; model tests a few minutes; integration up to tens of minutes. Keep PR checks short or people stop waiting for them.
- **Why normal tests are not enough:** a unit test of code passes while the data changes underneath. In my run, monthly spend scaled by 100 raised no exception; only the data tests failed.

**Example:** The unit test of the ratio function still passed after I multiplied spend by 100. The data layer caught the shift, and also showed the label becoming all ones (churn rate 1.0), a second signal that something was off.

**Code:** tests are tagged with markers. Files: `churn.py`, `conftest.py`, `test_pyramid.py`, `q09_run.sh` (shown joined).
```python
# ===== q09/churn.py =====
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

FEATURES = ["tenure_months", "monthly_spend", "support_calls"]


def make_data(n=600, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "tenure_months": rng.integers(1, 72, n),
        "monthly_spend": rng.normal(60, 15, n).round(2),
        "support_calls": rng.poisson(1.5, n),
    })
    z = -1.0 - 0.04 * df.tenure_months + 0.02 * df.monthly_spend + 0.5 * df.support_calls
    df["churned"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    return df


def add_ratio(df):                       # tiny feature function: UNIT test target
    out = df.copy()
    out["spend_per_month_tenure"] = out.monthly_spend / out.tenure_months.clip(lower=1)
    return out


def train(df, seed=0):
    model = LogisticRegression(max_iter=1000, random_state=seed)
    model.fit(df[FEATURES], df["churned"])
    return model

# ===== q09/conftest.py =====
import pytest
from churn import make_data

def pytest_configure(config):
    for m in ("unit", "data", "model", "integration"):
        config.addinivalue_line("markers", f"{m}: {m} tests")

@pytest.fixture(scope="session")
def df():
    return make_data()

# ===== q09/test_pyramid.py =====
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from churn import FEATURES, add_ratio, make_data, train


# 1. UNIT: one small function, hand-checkable, runs in milliseconds
@pytest.mark.unit
def test_add_ratio_zero_tenure_does_not_divide_by_zero():
    out = add_ratio(pd.DataFrame({"monthly_spend": [50.0], "tenure_months": [0]}))
    assert out.spend_per_month_tenure.iloc[0] == 50.0


# 2. DATA: schema, ranges, nulls, label balance (this is what catches silent data change)
@pytest.mark.data
def test_schema_ranges_and_nulls(df):
    assert list(df.columns) == FEATURES + ["churned"]
    assert df[FEATURES].notna().all().all()
    assert df.tenure_months.between(1, 72).all() and (df.support_calls >= 0).all()
    assert 0.05 < df.churned.mean() < 0.95          # not all one class


@pytest.mark.data
def test_spend_unit_did_not_change(df):
    # catches a silent unit change (e.g. rupees -> paise) that no Python error would ever flag
    assert 30 < df.monthly_spend.mean() < 90


# 3. MODEL: behaviour after training (needs a fit, so slower)
@pytest.mark.model
def test_beats_baseline_and_is_directional(df):
    tr, te = train_test_split(df, test_size=0.25, random_state=0, stratify=df.churned)
    model = train(tr)
    auc = roc_auc_score(te.churned, model.predict_proba(te[FEATURES])[:, 1])
    assert auc > 0.6                                  # floor chosen by the team, not a universal number
    low, high = te.iloc[[0]].copy(), te.iloc[[0]].copy()
    low["support_calls"], high["support_calls"] = 0, 8
    assert model.predict_proba(high[FEATURES])[0, 1] > model.predict_proba(low[FEATURES])[0, 1]


@pytest.mark.model
def test_same_seed_same_predictions(df):
    p1 = train(df, seed=1).predict_proba(df[FEATURES])
    p2 = train(df, seed=1).predict_proba(df[FEATURES])
    np.testing.assert_allclose(p1, p2)


# 4. INTEGRATION: the whole path, raw data to saved model to predictions for new rows
@pytest.mark.integration
def test_end_to_end_with_save_and_load(tmp_path):
    import joblib
    data = make_data(seed=3)
    joblib.dump(train(data), tmp_path / "m.joblib")
    loaded = joblib.load(tmp_path / "m.joblib")
    new_rows = pd.DataFrame({"tenure_months": [3], "monthly_spend": [80.0], "support_calls": [5]})
    p = loaded.predict_proba(new_rows[FEATURES])[0, 1]
    assert 0.0 <= p <= 1.0
```
```bash
#!/usr/bin/env bash
# Q9: pyramid layers as pytest markers; run each layer, show counts and timings
D=$(dirname "$(readlink -f "$0")")/q09; T=$(mktemp -d); cp "$D"/*.py "$T"; cd "$T"
for m in unit data model integration; do
  printf "%-12s" "-m $m:"; python3 -I -m pytest -q -p no:cacheprovider -m $m 2>&1 | tail -1
done
printf "%-12s" "all:"; python3 -I -m pytest -q -p no:cacheprovider 2>&1 | tail -1
echo "--- per-PR selection: -m 'unit or data'"; python3 -I -m pytest -q -p no:cacheprovider -m "unit or data" 2>&1 | tail -1
echo "--- silent data change: monthly_spend arrives in paise (x100); no exception anywhere in the code"
sed -i 's/rng.normal(60, 15, n).round(2)/(rng.normal(60, 15, n) * 100).round(2)/' churn.py
python3 -I -m pytest -q -p no:cacheprovider -m data 2>&1 | grep -E "^FAILED|passed|failed"
python3 -I -m pytest -q -p no:cacheprovider -m unit 2>&1 | tail -1 | sed "s/^/unit tests, same broken data: /"
rm -rf "$T"
```

**Output (my run):** pytest 9.1.1, scikit-learn 1.9.1, Python 3.13.17. Timings are from this sandbox, only to show the layers differ in cost.
```text
-m unit:    1 passed, 5 deselected in 0.11s
-m data:    2 passed, 4 deselected in 0.14s
-m model:   2 passed, 4 deselected in 0.21s
-m integration:1 passed, 5 deselected in 0.19s
all:        6 passed in 0.95s
--- per-PR selection: -m 'unit or data'
3 passed, 3 deselected in 0.11s
--- silent data change: monthly_spend arrives in paise (x100); no exception anywhere in the code
FAILED test_pyramid.py::test_schema_ranges_and_nulls - assert np.float64(1.0)...
FAILED test_pyramid.py::test_spend_unit_did_not_change - assert np.float64(59...
2 failed, 4 deselected in 0.25s
unit tests, same broken data: 1 passed, 5 deselected in 0.12s
```

**Follow-ups:**
- *What else belongs in a data test?* Freshness, row counts, category sets, null rate per column (tools like pandera or Great Expectations; not run here).
- *How do you stop flaky model tests?* Fixed seeds, fixed data slice, thresholds with margin.
- *Which tests gate release?* Model tests against a held-out set and against the current production model.

**Common mistakes:**
- One huge suite that runs 40 minutes on every PR.
- AUC threshold copied from one lucky run.
- No data tests, only code tests.
- Tests that need production data or the network.

### Q10 ⭐⭐⭐ 🟡 Python packaging for ML code. A team keeps helper code in a utils/ folder and imports it with sys.path hacks. Turn it into an installable package: show a minimal pyproject.toml, the src layout, how pip install -e . works for development, the difference between a wheel and an sdist, and how you build and test-install a wheel in a clean virtual environment. Build and install it for real in a temp folder.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** Put the code under `src/<name>/`, describe it in `pyproject.toml`, install it with `pip install -e .` while developing, and build a wheel (`python -m build`) that I install into a clean venv to prove it works without my source folder.

**Then explain:**
- **Why not `sys.path` hacks:** they depend on where you run from, break in CI and notebooks, and hide missing dependencies. A package works from anywhere once installed.
- **src layout:** code in `src/churnkit/`, tests in `tests/`. With `src/` you cannot import the package by accident from the current folder, so tests exercise the installed code (a common packaging recommendation).
- **Editable install (`pip install -e .`):** links the environment to the source folder, so edits show up with no reinstall. Changes to `pyproject.toml` itself (new dependencies, entry points) need a reinstall.
- **Wheel vs sdist:** the wheel (`.whl`) is a ready-to-unpack built package; the sdist (`.tar.gz`) is the source archive plus metadata that a tool must build. In my run the wheel held only `churnkit/` and metadata; the sdist also held `src/`, `tests/` and `pyproject.toml`.
- **Clean-venv test:** install only the wheel in a new venv and run from another folder; this finds missing files or undeclared dependencies.
- Failure mode: a dependency imported in code but missing from `dependencies` works on your laptop and fails in the clean venv.

**Example:** `utils/features.py` becomes `src/churnkit/features.py`. Everyone does `from churnkit import add_ratio`. After editing the clip value in the source, the editable venv reflected it at once.

**Code:** `pyproject.toml` (also written by the script), then the full demo.
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "churnkit"
version = "0.1.0"
description = "Shared feature helpers for the churn team"
requires-python = ">=3.10"
dependencies = ["pandas>=2.0"]

[project.optional-dependencies]
dev = ["pytest"]

[tool.hatch.build.targets.wheel]
packages = ["src/churnkit"]
```
```bash
#!/usr/bin/env bash
# Q10: sys.path hack -> installable src-layout package; build wheel + sdist; install in a clean venv
set -e
W=$(mktemp -d); cd "$W"; mkdir -p churnkit/src/churnkit churnkit/tests; cd churnkit
cat > pyproject.toml <<'T'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "churnkit"
version = "0.1.0"
description = "Shared feature helpers for the churn team"
requires-python = ">=3.10"
dependencies = ["pandas>=2.0"]

[project.optional-dependencies]
dev = ["pytest"]

[tool.hatch.build.targets.wheel]
packages = ["src/churnkit"]
T
cat > src/churnkit/__init__.py <<'T'
from churnkit.features import add_ratio

__version__ = "0.1.0"
__all__ = ["add_ratio"]
T
cat > src/churnkit/features.py <<'T'
import pandas as pd


def add_ratio(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ratio"] = out["spend"] / out["tenure"].clip(lower=1)
    return out
T
cat > tests/test_features.py <<'T'
import pandas as pd
from churnkit import add_ratio


def test_add_ratio():
    out = add_ratio(pd.DataFrame({"spend": [100.0], "tenure": [4]}))
    assert out["ratio"].iloc[0] == 25.0
T
echo "--- layout"; find . -type f | sort
echo "--- build wheel + sdist (isolated build env pulls hatchling from the index)"
python3 -m build 2>&1 | tail -2
ls dist
echo "--- wheel contents (src/ is NOT in the wheel; the package sits at the top level)"
python3 -c "import zipfile,sys; print('\n'.join(zipfile.ZipFile(sys.argv[1]).namelist()))" dist/*.whl
echo "--- sdist contents"
python3 -c "import tarfile,sys; print('\n'.join(tarfile.open(sys.argv[1]).getnames()))" dist/*.tar.gz
echo "--- fresh venv, install the WHEEL only, run from another folder (so the source tree cannot leak in)"
python3 -m venv "$W/v1" >/dev/null; mkdir "$W/elsewhere"; cd "$W/elsewhere"
"$W/v1/bin/pip" -q install "$W"/churnkit/dist/*.whl 2>&1 | tail -2
"$W/v1/bin/python" -I -c "import churnkit, pandas; print('imported from', churnkit.__file__.replace('$W','<tmp>')); print('version', churnkit.__version__)"
"$W/v1/bin/pip" list 2>/dev/null | grep -iE "churnkit|pandas"
echo "--- editable install in a second venv: edit the source, no reinstall needed"
python3 -m venv "$W/v2" >/dev/null
"$W/v2/bin/pip" -q install -e "$W/churnkit[dev]" 2>&1 | tail -2
cd "$W/churnkit"
sed -i 's/clip(lower=1)/clip(lower=2)/' src/churnkit/features.py
cd "$W/elsewhere"; "$W/v2/bin/python" -c "
import pandas as pd, churnkit
print('after editing source, ratio =', churnkit.add_ratio(pd.DataFrame({'spend':[100.0],'tenure':[1]})).ratio[0], '(clip(lower=2) is live)')"
sed -i 's/clip(lower=2)/clip(lower=1)/' "$W/churnkit/src/churnkit/features.py"
echo "--- run tests against the installed package"
cd "$W/churnkit"; "$W/v2/bin/python" -m pytest -q -p no:cacheprovider 2>&1 | tail -2
rm -rf "$W"
```

**Output (my run):** Python 3.13.17, build 1.6.1, hatchling pulled by the isolated build from the package index (the sandbox proxy allowed it); pandas 3.1.0 resolved from the index at run time. Nothing was uploaded; `twine` was not run.
```text
--- layout
./pyproject.toml
./src/churnkit/__init__.py
./src/churnkit/features.py
./tests/test_features.py
--- build wheel + sdist (isolated build env pulls hatchling from the index)
* Building wheel...
Successfully built churnkit-0.1.0.tar.gz and churnkit-0.1.0-py3-none-any.whl
churnkit-0.1.0-py3-none-any.whl
churnkit-0.1.0.tar.gz
--- wheel contents (src/ is NOT in the wheel; the package sits at the top level)
churnkit/__init__.py
churnkit/features.py
churnkit-0.1.0.dist-info/METADATA
churnkit-0.1.0.dist-info/WHEEL
churnkit-0.1.0.dist-info/RECORD
--- sdist contents
churnkit-0.1.0/src/churnkit/__init__.py
churnkit-0.1.0/src/churnkit/features.py
churnkit-0.1.0/tests/test_features.py
churnkit-0.1.0/pyproject.toml
churnkit-0.1.0/PKG-INFO
--- fresh venv, install the WHEEL only, run from another folder (so the source tree cannot leak in)
imported from <tmp>/v1/lib/python3.13/site-packages/churnkit/__init__.py
version 0.1.0
churnkit        0.1.0
pandas          3.1.0
--- editable install in a second venv: edit the source, no reinstall needed
after editing source, ratio = 50.0 (clip(lower=2) is live)
--- run tests against the installed package
.                                                                        [100%]
1 passed in 0.36s
```

**Follow-ups:**
- *Where does it get published?* A private index or an internal artifact repo, with CI building the wheel on a tag (hosted-index details vary; check your platform's docs).
- *setuptools or hatchling?* Either works with `pyproject.toml`; pick one and keep the config in that file.
- *How do you pin versions for reproducible training?* The package declares ranges; the application keeps a lockfile.

**Common mistakes:**
- Testing from the repo root, where the source folder hides a broken install.
- Forgetting `__init__.py` or listing the wrong package path (empty wheel).
- Pinning exact versions in a library (it makes installs conflict for users).
- Using `python setup.py install` in new code.
