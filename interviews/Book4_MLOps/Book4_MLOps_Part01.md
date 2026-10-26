# Book 4 — Part 1: Git, code quality, packaging and testing ML code

**Topic:** the software-engineering base of MLOps: Git workflows and recovery, reproducible repos, notebook hygiene, code quality gates, Python packaging and dependencies, and testing ML code (unit, data, model and integration tests)
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 15, ⭐⭐ 16, ⭐ 9)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Book 1 owns ML theory (leakage, metrics and validation are only used here as things to test); Book 2 owns LLM serving and RAG (only the code-review angle of AI-generated code appears here); Book 3 owns SQL; Book 6 owns product and business. Later Book 4 parts own Docker (Part 2), Kubernetes (Part 3), DVC, MLflow and W&B (Part 4), orchestration (Part 5), serving (Part 6), CI/CD pipelines and model registry (Part 7) and monitoring (Part 8). This part stays on the repository, the code and the tests; where a question touches those later tools it names them in one line and defers. Every prompt is self-contained and can be answered with Python 3.13, git, pytest and scikit-learn; items that depend on a hosted service (private package index, GitHub branch protection) are concept-and-hedge only.

Evidence limits: the free pages found could not be opened (WebFetch failed with getaddrinfo ENOTFOUND), so every source is a search snippet only (see research_notes/Book4_Part01_sources.md). No page was found that reports exact interview questions asked by a named company for these topics; the Bangalore results were job postings, not interview reports. 'Asked at' tags therefore name source types (editorial guides, testing write-ups, job postings), not companies that asked these exact questions, and many questions are expert extensions in the style of those guides. No salary figures.

---

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

### Q11 ⭐⭐⭐ 🟡 Dependency management in an ML repo. Compare a loose requirements.txt, a pinned requirements file produced by pip-compile or uv, and a full lockfile; say what you pin directly versus transitively, how you handle separate dev, test and GPU dependencies, and why a model pickled with one scikit-learn version can fail or silently misbehave under another. Demonstrate the pickle version warning or a safer export idea, and show the commands to produce a lock.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** Loose files say what I want, a compiled pin file says exactly what I got, and a lockfile says it for every platform with hashes; I write only direct dependencies by hand, compile the rest, and never trust a pickle across scikit-learn versions.

**Then explain:**
- Three levels. Loose `requirements.txt` (`pandas>=2`): easy to write, but two installs a month apart give two different environments. Pinned file from `pip-compile` or `uv pip compile`: every package, direct and transitive, at an exact version. Lockfile (`uv.lock`, poetry.lock): the same idea, resolved for all platforms and Python versions at once, usually with hashes.
- What I pin by hand: only direct dependencies, as ranges in `pyproject.toml` or a small `requirements.in` (pin exactly only when a bug forces it). Transitive ones (numpy, scipy, joblib) are the tool's job. I commit the compiled output and update it on purpose, in a PR, with tests.
- Dev, test and GPU: keep them out of the runtime list. Use extras or dependency groups (`dev`, `test`) and a separate compiled file per environment (`requirements.txt` for serving, `requirements-dev.txt` for CI). For GPU, the torch wheel comes from a different index and CUDA version, so I keep a separate GPU requirements file or group and build a separate image. Check current docs for how your tool handles extra indexes.
- Pickle problem: a pickle stores the object's internal attributes, not a stable format. A different scikit-learn version can have renamed or added attributes, so loading may raise, or load fine and give different numbers because a default changed. Newer versions emit `InconsistentVersionWarning`; many people never read it. Pickle also runs code on load, so never load one you do not trust.
- Safer ideas: serve in the same locked image the model was trained in; store a sidecar file with library versions and fail closed on a mismatch; or export to a portable format (ONNX for supported models, or `skops` for scikit-learn, check current docs; not run here); or keep the training code and data version so you can retrain.
- Edge cases: the minor-version jump is the dangerous one (1.6 to 1.9 below); an unpinned `latest` in a Docker build makes the same Dockerfile produce different images; a lockfile made on Linux can miss a Windows-only wheel unless it is multi-platform.

**Example:** `requirements.in` has two lines (scikit-learn pinned, pandas as a range). `uv pip compile` turned them into 11 exact pins. Count them by hand in the output below: pandas pulls numpy, python-dateutil, six, tzdata; scikit-learn pulls numpy, scipy, joblib, threadpoolctl (plus narwhals and cloudpickle in these versions). Then I trained a LogisticRegression under scikit-learn 1.6.1, pickled it, and loaded it under 1.9.1: it loaded, and only a warning told me the versions differ.

**Code:** the commands first, then `pyproject.toml`, then the two Python scripts (the first run in an old venv, the second in the current environment).
```sh
# 1. loose: hand-written, direct dependencies only
cat requirements.in            # scikit-learn==1.9.1 / pandas>=2.0
# 2. pinned file (pick one tool; pip-tools line not run here)
pip-compile requirements.in -o requirements.txt          # pip-tools
uv pip compile requirements.in -o requirements.txt       # ran; uv 0.11.32
uv pip sync requirements.txt                             # install exactly the pinned set
# 3. lockfile from pyproject.toml (ran)
uv lock
uv sync --frozen                                         # CI/Docker: fail if the lock is out of date
# old environment for the pickle demo (ran)
uv venv old && uv pip install --python old/bin/python scikit-learn==1.6.1
old/bin/python -I make_pickle.py && python3 -I load_pickle.py
```
```toml
# pyproject.toml
[project]
name = "demo"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["scikit-learn>=1.5", "pandas>=2.0"]

[dependency-groups]
dev = ["pytest>=8", "ruff"]
```
```python
# ===== make_pickle.py =====
# run under the OLD environment (scikit-learn 1.6.1)
import json, pickle, sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=100, random_state=0)
m = LogisticRegression().fit(X, y)
with open("model_old.pkl", "wb") as f:
    pickle.dump(m, f)
with open("model_old.meta.json", "w") as f:        # sidecar: what built this artifact
    json.dump({"sklearn": sklearn.__version__, "python": "3.13"}, f)
print("wrote model_old.pkl with scikit-learn", sklearn.__version__)

# ===== load_pickle.py =====
# run under the NEW environment (system python, scikit-learn 1.9.1)
import json, pickle, warnings, sklearn
from sklearn.exceptions import InconsistentVersionWarning
print("loading with scikit-learn", sklearn.__version__)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always", InconsistentVersionWarning)
    with open("model_old.pkl", "rb") as f:
        m = pickle.load(f)
for x in w:
    print("warning:", x.category.__name__, "|", str(x.message).split(" This")[0])
print("loaded:", type(m).__name__, "| version warnings:", len(w))

# safer: fail closed using the sidecar, instead of trusting a warning
meta = json.load(open("model_old.meta.json"))
if meta["sklearn"] != sklearn.__version__:
    print(f"GUARD: artifact built with {meta['sklearn']}, runtime has {sklearn.__version__} -> refuse to serve, retrain or re-export")
```

**Output (my run):** uv 0.11.32, Python 3.13.17; the `.in` was pinned to scikit-learn 1.9.1, the old venv had 1.6.1. `pip-compile` itself was not run (pip-tools not installed); `uv pip compile` gives the same kind of file. The versions below will differ when you run it later.
```text
$ cat requirements.in
scikit-learn==1.9.1
pandas>=2.0

$ uv pip compile requirements.in -o requirements.txt --no-header   # then:
direct lines in .in: 2, pinned lines in requirements.txt: 11
$ cat requirements.txt (first 12 lines)
cloudpickle==3.1.2
    # via joblib
joblib==1.6.0
    # via scikit-learn
narwhals==2.27.1
    # via scikit-learn
numpy==2.5.4
    # via
    #   pandas
    #   scikit-learn
    #   scipy
pandas==3.1.0
$ uv lock  ->  packages in uv.lock (all platforms, incl. dev group): 29
```
```text
loading with scikit-learn 1.9.1
warning: InconsistentVersionWarning | Trying to unpickle estimator LogisticRegression from version 1.6.1 when using version 1.9.1.
loaded: LogisticRegression | version warnings: 1
GUARD: artifact built with 1.6.1, runtime has 1.9.1 -> refuse to serve, retrain or re-export
```
`uv lock` printed `Resolved 29 packages`; the lockfile covers all platforms and the dev group, so it is bigger than the single-platform pin file.

**Follow-ups:**
- *Why not just `pip freeze`?* It mixes direct and transitive packages with no record of which you asked for, so you cannot tell what is safe to remove or upgrade. Compile from a small input instead.
- *Does the pin protect me from a changed wheel?* Only with hashes (`--require-hashes`, or the lockfile's hashes). Without them a re-uploaded file would go unnoticed. Check current docs for the flag in your tool.
- *Library or application?* An application locks everything. A library declares ranges only, because pinning exactly in a library breaks its users.

**Common mistakes:**
- Committing `pip freeze` output from a dirty laptop environment (extra packages, wrong OS).
- Pinning in `requirements.in` everything by hand, then never updating, so security fixes never arrive.
- One requirements file for training, serving, tests and notebooks; the serving image gets Jupyter.
- Ignoring `InconsistentVersionWarning` in logs, or filtering warnings to silence it.
- Loading a pickle from an untrusted place; it can run arbitrary code.

---

### Q12 ⭐⭐⭐ 🟡 Code quality gates for an ML repository. Set up ruff (lint and format), mypy and pytest in a .pre-commit-config.yaml and the same checks in a CI job, and say what you would enforce hard (failing the build) versus softly. Explain why pre-commit alone is not enough (--no-verify, new contributors) and how you keep checks fast enough that people do not skip them. Show the config and run it against a small bad file.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I run ruff, mypy and fast tests in pre-commit for quick feedback, then run the same commands in CI as the real gate, because a local hook can be skipped with `--no-verify`.

**Then explain:**
- Hard gates (fail the build): ruff lint, ruff format check, mypy on the `src` package, fast unit tests, a coverage floor that is modest and never lowered silently. Soft (warn, do not block): stricter mypy on old modules, complexity, docstring rules, slow tests, notebook lint. I tighten a soft check to hard only after the existing violations are fixed.
- Why pre-commit alone is not enough: `git commit --no-verify` skips it, a new contributor may not have run `pre-commit install`, and local tool versions drift. CI runs the same commands from the same pinned dev requirements, and branch protection makes that job required (a hosted setting; check your platform's docs).
- Speed rules so people do not skip: pre-commit only checks changed files; ruff is fast; mypy runs only on `src`; the slow tests are marked and run in CI or on pre-push, not on every commit. If a commit hook takes more than a few seconds, people find the bypass.
- Failure modes: pinned hook versions differ from CI versions (so "passes locally, fails in CI"); `types: [python]` hooks miss notebooks (use `nbstripout` or jupytext, not covered here); auto-fixing hooks edit files and the commit fails once, which confuses newcomers (tell them to re-add and commit again).
- I used `repo: local` hooks because this sandbox cannot clone hook repositories. On a real team I would pin the official hook repos with a `rev`, and let `pre-commit autoupdate` raise PRs (check current docs for the repos and revisions).

**Example:** The bad file `src/train.py` has an unused import and a multi-import line, a mutable default argument `mean=[]`, an unused variable, a function with no type hints and a function that returns a `str` when annotated `int`. By hand: ruff should flag the imports, `B006` (mutable default) and `F841` (unused variable); `ruff format` flags `x/ 2`; mypy flags the missing annotation and the bad return. That is exactly what the run printed. Normal commit blocked (exit 1); with `--no-verify` the same file went into history, and only the CI-style run caught it.

**Code:** `.pre-commit-config.yaml` plus the CI job (both parse as YAML, validated below), tool settings, the bad file and the demo script that runs in a throwaway repo.
```yaml
# ===== .pre-commit-config.yaml =====
# Local hooks use tools already in the env (no network clone). For a real team you can
# pin remote repos instead, e.g. repo: https://github.com/astral-sh/ruff-pre-commit (check current docs for rev).
repos:
  - repo: local
    hooks:
      - id: ruff-lint
        name: ruff lint
        entry: ruff check --output-format=concise
        language: system
        types: [python]
      - id: ruff-format
        name: ruff format --check
        entry: ruff format --check --quiet
        language: system
        types: [python]
      - id: mypy
        name: mypy
        entry: mypy --ignore-missing-imports
        language: system
        types: [python]
        exclude: ^tests/
      - id: pytest-fast
        name: pytest (fast only)
        entry: pytest -q -m "not slow"
        language: system
        pass_filenames: false
        stages: [pre-push]   # heavier check runs on push, not on every commit

# ===== .github-ci.yml =====
# GitHub Actions job (not executed here; check current docs for action versions). File would live at .github/workflows/ci.yml
name: ci
on: [pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pip install -r requirements-dev.txt
      - run: ruff check . && ruff format --check .
      - run: mypy src
      - run: pytest -q -m "not slow" --cov=src --cov-fail-under=70
```
```toml
# pyproject.toml
[tool.ruff]
line-length = 88
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
[tool.mypy]
disallow_untyped_defs = true
[tool.pytest.ini_options]
markers = ["slow: slow tests, skipped in the fast gate"]
```
```python
# src/train.py
import os,sys
import numpy as np

def fit_scale(x, mean=[]):
    mean.append(1)
    unused = 5
    return x/ 2

def load(path: str) -> int:
    return "oops"
```
```sh
# run_demo.sh
#!/bin/sh
# copies this folder to a temp git repo and runs pre-commit there (nothing touches the main repo)
T=$(mktemp -d); cp -r "$(dirname "$0")"/. "$T"/; cd "$T"
git init -q; git config user.email a@b.c; git config user.name demo; git add -A
pre-commit install
echo "== 1. normal commit"; out=$(git commit -q -m "bad file" 2>&1); rc=$?; echo "$out" | grep -E "Failed|Passed|train.py:[0-9]+:[0-9]+: (B006|F841)|error:"; echo "git commit exit code: $rc (blocked)"
echo "== 2. same commit with --no-verify"; git commit -q --no-verify -m "bad file"; echo "git commit exit code: $?  (hooks skipped, bad file is now in history)"
echo "== 3. CI-style run of the same checks"; ruff check -q --output-format=concise . ; echo "ruff exit: $?"
```

**Output (my run):** pre-commit 4.7.0, ruff 0.16.9, mypy 2.3.1, git 2.43.0, in a temp repo. The CI workflow was not executed (needs the hosted platform; the action versions in it should be checked against current docs). I did validate that both YAML files parse with pyyaml: `.pre-commit-config.yaml parses ['repos']`, and the CI file parses with keys `name`, `on` and `jobs` (YAML reads the bare word `on` as `True`, which is a known gotcha; GitHub reads it as `on`).
```text
pre-commit installed at .git/hooks/pre-commit
== 1. normal commit
ruff lint................................................................Failed
src/train.py:4:23: B006 Do not use mutable data structures for argument defaults
src/train.py:6:5: F841 Local variable `unused` is assigned to but never used
ruff format --check......................................................Failed
mypy.....................................................................Failed
src/train.py:4: error: Function is missing a type annotation  [no-untyped-def]
src/train.py:10: error: Incompatible return value type (got "str", expected "int")  [return-value]
git commit exit code: 1 (blocked)
== 2. same commit with --no-verify
git commit exit code: 0  (hooks skipped, bad file is now in history)
== 3. CI-style run of the same checks
src/train.py:1:1: E401 [*] Multiple imports on one line
src/train.py:1:1: I001 [*] Import block is un-sorted or un-formatted
src/train.py:1:8: F401 [*] `os` imported but unused
src/train.py:1:11: F401 [*] `sys` imported but unused
src/train.py:2:17: F401 [*] `numpy` imported but unused
src/train.py:4:23: B006 Do not use mutable data structures for argument defaults
src/train.py:6:5: F841 Local variable `unused` is assigned to but never used
ruff exit: 1
```
The pytest hook is on `pre-push`, so it did not run on commit; the demo repo has a passing test anyway.

**Follow-ups:**
- *Should CI also auto-fix?* No. CI checks and fails; fixing is local (`ruff check --fix`, `ruff format`).
- *Where does the type-check strictness go for a messy legacy repo?* Start with `mypy src/new_package` only, grow the list, and do not turn on `disallow_untyped_defs` globally on day one.
- *How do you stop pre-commit versions drifting from CI?* CI runs `pre-commit run --all-files` itself, or both read the same pinned dev requirements.

**Common mistakes:**
- Treating pre-commit as the only gate.
- Making the hook slow (full test suite on every commit) so everyone uses `--no-verify`.
- Different ruff versions in hooks and CI.
- A gate that nobody can pass on the existing code, so it is switched off for everything.
- Running mypy on tests and notebooks first and drowning in noise.

---

### Q13 ⭐⭐⭐ 🔴 Training-serving skew from the code side. A model scores well offline but badly online because the training notebook computes features with pandas while the service re-implements them. Explain how repository structure prevents this: one shared feature module imported by both paths, a golden-file parity test comparing the two paths on 20 sample rows, and a schema contract. Build the shared module and the parity test with a seeded example in which a deliberate bug (different rounding or a different fill value) is caught by the test.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Put every feature calculation in one module that both training and the service import, add a golden-file parity test that runs both paths on the same 20 rows, and validate inputs with a schema, so a re-implementation cannot drift without a red test.

**Then explain:**
- Why it happens: notebook pandas code is copied into the API as hand-written Python. Small differences (fill value, rounding, category order, timezone) give different numbers, and the model sees inputs it was never trained on. Offline metrics stay good; online quality drops with no error.
- Repo fix: `features.py` is the only place with feature logic. Training calls `build_features(df)`. The service calls the same function (a thin wrapper, no maths). Constants such as the fill value live there too, or in a config both read.
- Golden-file parity test: save 20 raw rows and the features training produced (`golden_features.csv`). The test pushes the raw rows through the real serving function and compares with a tolerance. Include rows with missing values on purpose, since edge cases are where paths differ.
- Schema contract: a pydantic model (or pandera for frames) at the service boundary rejects wrong types early and documents what the model expects.
- Limits: the parity test only covers the sample rows, so choose them to include nulls, zeros and extremes. If a feature uses a fitted statistic (a median), store it as an artefact with the model, not as a number typed in two places. Features computed in a warehouse or feature store are a different setup; this covers the in-repo case.

**Example:** The seeded golden set has 20 rows, rows 3, 11 and 17 with missing income. Training fills missing income with 50,000. The buggy service fills 0 and rounds `income_per_head` to 1 decimal instead of 2. Hand check: row 3's income column should be 50000.0 and the buggy service gives 0.0. The 3 missing-income rows (3, 11, 17) differ on several columns. Three more rows (6, 13, 14, all household size 3) differ only because of rounding: row 6 is 92000/3 = 30666.67 in training and 30666.7 in the buggy service. The test reports 6 of 20 rows differ and names the first one.

**Code:** run with `python3 -I`. `SERVICE=buggy` points the same test at the re-implementation; `SERVICE=shared` points it at the fixed service.
```python
# ===== features.py =====
"""Single source of truth for features. Training and serving both import this."""
import numpy as np
import pandas as pd
from pydantic import BaseModel

INCOME_FILL = 50_000.0   # constant learned at training time, stored in code/config, not retyped elsewhere
COLUMNS = ["age", "income", "household", "income_per_head", "log_income", "is_senior"]


class RawRow(BaseModel):          # schema contract at the service boundary
    age: int
    income: float | None = None
    household: int


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["age"] = df["age"]
    out["income"] = df["income"].fillna(INCOME_FILL)
    out["household"] = df["household"]
    out["income_per_head"] = (out["income"] / out["household"]).round(2)
    out["log_income"] = np.log1p(out["income"]).round(4)
    out["is_senior"] = (out["age"] >= 60).astype(int)
    return out[COLUMNS]

# ===== service_buggy.py =====
"""A re-implementation written by someone else for the API. Looks fine, is not."""
import math
from features import COLUMNS


def predict_features(rows: list[dict]) -> list[list[float]]:
    out = []
    for r in rows:
        income = r["income"] if r["income"] is not None and r["income"] == r["income"] else 0.0  # BUG 1: fills 0
        ph = round(income / r["household"], 1)                                                    # BUG 2: 1 decimal
        out.append([r["age"], income, r["household"], ph, round(math.log1p(income), 4), int(r["age"] >= 60)])
    return out

# ===== service_shared.py =====
"""Service path after the fix: no feature logic here, only a call into the shared module."""
import pandas as pd
from features import RawRow, build_features


def predict_features(rows: list[dict]) -> list[list[float]]:
    rows = [RawRow(**{**r, "income": None if r["income"] != r["income"] else r["income"]}).model_dump() for r in rows]  # schema check
    return build_features(pd.DataFrame(rows)).values.tolist()

# ===== make_golden.py =====
"""Run once at training time: 20 seeded sample rows + the features the training path produced."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
from features import build_features

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "age": rng.integers(18, 80, 20),
    "income": rng.integers(20, 200, 20) * 1000.0,
    "household": rng.integers(1, 6, 20),
})
df.loc[[3, 11, 17], "income"] = np.nan          # missing incomes on purpose
df.to_csv("golden_raw.csv", index=False)
build_features(df).to_csv("golden_features.csv", index=False)
print("golden rows:", len(df), "| NaN incomes:", int(df.income.isna().sum()))

# ===== tests/test_parity.py =====
import importlib, os
import numpy as np, pandas as pd, pytest

IMPL = os.environ.get("SERVICE", "shared")


def test_serving_matches_golden_training_features():
    raw = pd.read_csv("golden_raw.csv")
    want = pd.read_csv("golden_features.csv").values
    rows = [{k: (None if v != v else v) for k, v in r.items()} for r in raw.to_dict("records")]
    got = np.array(importlib.import_module(f"service_{IMPL}").predict_features(rows), dtype=float)
    assert got.shape == want.shape
    bad = np.where(~np.isclose(got, want, rtol=0, atol=1e-6))
    assert bad[0].size == 0, f"{len(set(bad[0]))} of {len(want)} rows differ; first: row {bad[0][0]} col {bad[1][0]} got {got[bad[0][0], bad[1][0]]} want {want[bad[0][0], bad[1][0]]}"


def test_schema_contract_rejects_bad_payload():
    from features import RawRow
    with pytest.raises(Exception):
        RawRow(age="old", household=2)
```
```ini
# pytest.ini
[pytest]
pythonpath = .
```
```sh
# run.sh
python3 -I make_golden.py                                   # once, at training time
SERVICE=buggy  python3 -I -m pytest -q -p no:cacheprovider tests   # parity test fails
SERVICE=shared python3 -I -m pytest -q -p no:cacheprovider tests   # passes
```

**Output (my run):** Python 3.13.17, pandas 3.0.5, numpy 2.5.3, pytest 9.1.1, pydantic 2.13.5.
```text
golden rows: 20 | NaN incomes: 3
=== SERVICE=buggy
E       AssertionError: 6 of 20 rows differ; first: row 3 col 1 got 0.0 want 50000.0
E       assert 12 == 0
E        +  where 12 = array([ 3,  3,  3,  6, 11, 11, 11, 13, 14, 17, 17, 17]).size
1 failed, 1 passed in 0.64s
=== SERVICE=shared
..                                                                       [100%]
2 passed in 0.56s
```
The buggy run: 1 failed (parity), 1 passed (schema test). The shared run: both pass.

**Follow-ups:**
- *Why a tolerance and not equality?* Float maths can differ in the last digits across machines. Use `atol=1e-6` for features and say why; exact equality for integers and categories.
- *What if the service must be fast and cannot use pandas?* Then write a pure-Python version and keep the parity test, which is the contract. Better, vectorise the shared function so it handles one row and many rows.
- *How do you catch skew that is not code, such as different data distributions?* That is drift monitoring, not this test.

**Common mistakes:**
- Copy-pasting notebook code into the API "for now".
- Testing the service against hand-written expected values instead of the training path's output.
- Golden rows that are all clean; the bug hides in nulls.
- Typing the fill median in two places.
- Letting a pydantic model coerce silently (`"12"` to 12) when you wanted a rejection; check strict mode.

---

### Q14 ⭐⭐⭐ 🔴 How do you test an ML model itself (not just the code)? Explain pre-train tests (output shape and range, probabilities sum to 1, loss goes down on one batch, the model can overfit a 10-row dataset) and post-train tests (minimum accuracy on a slice, invariance to irrelevant changes, directional expectation, no leakage). Implement five of these as pytest tests for a scikit-learn LogisticRegression on seeded synthetic data and show the passing run and one deliberately failing case.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** I test a model in two groups: pre-train checks that the machinery is sane (shapes, probabilities, can overfit a tiny set), and post-train checks of behaviour (minimum score on a slice, invariance, directional expectation, no leakage), all as ordinary pytest tests on seeded data.

**Then explain:**
- Pre-train tests need no quality bar: output shape, probabilities in [0, 1] and summing to 1, loss goes down on a batch, and the model can memorise 10 rows. If it cannot overfit 10 rows, something in the pipeline is broken.
- Post-train tests check behaviour: a minimum accuracy on an important slice (not only overall), invariance (changing an irrelevant feature should not flip predictions), directional expectation (more of a positively-linked feature should not lower the probability), and no train/test overlap or leaky feature.
- Thresholds: set them from observed spread with a margin, not from one lucky run; otherwise the test is flaky. Record seeds.
- These tests catch pipeline bugs and regressions, not "is the model good enough for the business"; that is evaluation and monitoring.
- Failure modes: a test that passes on a tiny sample for the wrong reason, a threshold too tight, and tests that retrain a big model on every run (use a small fixture trained once per module).

**Example:** Data: 600 rows, x0 pushes class 1 up, x1 pushes it down, a third column is pure noise, split 70/30 stratified, seed 0. Hand expectation: shifting the noise column by 0.5 should flip almost no predictions (limit 2%). Then I inject a bug: the noise column secretly equals the label plus small noise (a leak). The model now leans on it, and shifting it flips 5.6% of predictions, so the invariance test fails and names the number.

**Code:** `test_model.py`, six tests. Set `LEAK=1` to inject the leaky column.
```python
# test_model.py
import os
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

LEAK = os.environ.get("LEAK") == "1"   # flip to 1 to inject a leaky feature and watch tests fail


def make_data(n=600, seed=0):
    rng = np.random.default_rng(seed)
    x0 = rng.normal(size=n)                      # informative, positive effect
    x1 = rng.normal(size=n)                      # informative, negative effect
    noise = rng.normal(size=n)                   # should be irrelevant
    y = (1.5 * x0 - 1.0 * x1 + rng.normal(scale=0.7, size=n) > 0).astype(int)
    if LEAK:
        noise = y + rng.normal(scale=0.1, size=n)  # the "irrelevant" column secretly encodes the label
    return np.c_[x0, x1, noise], y


@pytest.fixture(scope="module")
def split():
    X, y = make_data()
    idx = np.arange(len(y))
    tr, te = train_test_split(idx, test_size=0.3, random_state=0, stratify=y)
    return X[tr], X[te], y[tr], y[te], tr, te


@pytest.fixture(scope="module")
def model(split):
    Xtr, _, ytr, *_ = split
    return LogisticRegression().fit(Xtr, ytr)


# ---- pre-train style: no quality bar, just "is the machinery sane"
def test_output_shape_range_sum(model, split):
    p = model.predict_proba(split[1])
    assert p.shape == (len(split[1]), 2)
    assert ((p >= 0) & (p <= 1)).all()
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-9)


def test_can_overfit_ten_rows():
    X, y = make_data(n=10, seed=1)
    m = LogisticRegression(C=1e6, max_iter=1000).fit(X, y)
    assert (m.predict(X) == y).mean() == 1.0     # if it cannot memorise 10 rows, the pipeline is broken


# ---- post-train behaviour
def test_min_accuracy_on_slice(model, split):
    _, Xte, _, yte, *_ = split
    mask = Xte[:, 0] > 0                         # slice: x0 positive
    acc = (model.predict(Xte[mask]) == yte[mask]).mean()
    assert acc >= 0.80, f"slice accuracy {acc:.3f}"


def test_invariance_to_irrelevant_feature(model, split):
    Xte = split[1]
    shifted = Xte.copy(); shifted[:, 2] += 0.5   # nudge the column that should not matter
    flips = (model.predict(Xte) != model.predict(shifted)).mean()
    assert flips <= 0.02, f"{flips:.1%} predictions flipped"


def test_directional_expectation(model, split):
    Xte = split[1]
    up = Xte.copy(); up[:, 0] += 1.0             # more x0 -> probability of class 1 must not drop
    assert (model.predict_proba(up)[:, 1] >= model.predict_proba(Xte)[:, 1] - 1e-12).all()


def test_no_train_test_overlap(split):
    *_, tr, te = split
    assert set(tr).isdisjoint(te)
```
```sh
# run.sh
python3 -I -m pytest -q -p no:cacheprovider            # all pass
LEAK=1 python3 -I -m pytest -q -p no:cacheprovider     # injected leak: invariance test fails
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, pytest 9.1.1.
```text
$ pytest -q
......                                                                   [100%]
6 passed in 1.65s
$ LEAK=1 pytest -q   # the "irrelevant" column secretly encodes the label
E       AssertionError: 5.6% predictions flipped
E       assert np.float64(0.05555555555555555) <= 0.02
FAILED test_model.py::test_invariance_to_irrelevant_feature - AssertionError:...
1 failed, 5 passed in 1.45s
```

**Follow-ups:**
- *Where does a leakage test come from in real life?* Compare IDs or timestamps across splits, and check that no feature is suspiciously close to the target (very high single-feature score).
- *How do you test fairness or slices?* Same pattern: a parametrized test per slice with a minimum metric, and a clear owner for changing the thresholds.
- *Would you use a metamorphic test for a text model?* Yes: change casing or add a harmless word, expect the same class. Not run here.

**Common mistakes:**
- One accuracy threshold on the whole test set only.
- Thresholds copied from a single run.
- Tests that need the full production data.
- No seed, so the failing case cannot be reproduced.
- Forgetting that these tests do not replace online monitoring.

---

### Q15 ⭐⭐⭐ 🔴 Refactor a messy notebook into production code. The notebook loads data from a hard-coded path, fits a scaler on all rows, trains a model, prints the metric and saves model.pkl, all in global cells. Describe your step-by-step plan (functions, a config object, a train/predict split, tests, a CLI entry point, a pinned environment) and show the refactored layout and key functions, including the bug the refactor exposes (scaler fitted before the split). Run the refactored pipeline on seeded data.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I move the notebook into a package in small steps (functions, a config object, a pipeline with the scaler inside it, tests, a CLI, a pinned environment), and doing it shows the bug: the scaler was fitted on all rows before the split.

**Then explain:**
- Plan in order: (1) freeze the current output (metric and a few predictions) so I can tell if the refactor changes behaviour; (2) split cells into functions: `load_data`, `split`, `build_model`, `train`, `predict`; (3) replace hard-coded values with a config object (paths, feature list, seed, test size); (4) put the scaler and model into one `Pipeline` so `fit` only sees training rows; (5) save one artefact (the pipeline plus feature names), not just the model; (6) add a CLI entry point and a few tests; (7) pin the environment with a lockfile.
- The bug the refactor exposes: the notebook did `StandardScaler().fit_transform(X)` on all rows, then split. The test rows influenced the mean and standard deviation. It is mild leakage with a scaler, severe with target encoding or feature selection. It also meant the saved `model.pkl` could not reproduce the inputs at serving time, because the scaler was never saved.
- Also fixed: no seed on the split (different metric every run), metric only printed (now returned as a dict), absolute path on one laptop.
- Edge cases: the metric will change after the fix, and that is correct; say so in the PR. Keep notebooks for exploration, importing the package.

**Example:** Layout after refactor:
```text
churn/
  pyproject.toml          # package, console script "churn", pinned deps via lock
  src/churn/
    config.py             # TrainConfig dataclass: paths, features, seed, test_size
    pipeline.py           # load_data, split, build_model (Pipeline), train, predict
    cli.py                # `churn train --data ... --out ...`
  tests/test_pipeline.py
  notebooks/explore.ipynb # thin, imports churn
```
Hand check of the leak: on 400 rows, the notebook's scaler mean for `tenure` is computed over all 400, the fixed one over the 320 training rows. The two differ (37.415 vs 38.219 in the run below), so the scaled test values changed.

**Code:** the original notebook as a flat script (for reference, not run), then the refactor.
```python
# ===== notebook_before.py =====
# What the notebook looked like, flattened into one script (cells in order). DO NOT ship this.
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("C:/Users/me/Downloads/churn_final_v3.csv")     # hard-coded path
X = df[["tenure", "monthly_spend", "support_calls"]]
y = df["churned"]
X = StandardScaler().fit_transform(X)                            # fitted on ALL rows: test statistics leak in
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2)       # no seed
m = LogisticRegression().fit(Xtr, ytr)
print("accuracy", m.score(Xte, yte))                             # metric only printed
pickle.dump(m, open("model.pkl", "wb"))                          # scaler not saved: serving cannot reproduce inputs

# ===== src/churn/config.py =====
from dataclasses import dataclass


@dataclass(frozen=True)
class TrainConfig:
    data_path: str
    out_path: str = "model.joblib"
    features: tuple[str, ...] = ("tenure", "monthly_spend", "support_calls")
    target: str = "churned"
    test_size: float = 0.2
    seed: int = 42

# ===== src/churn/pipeline.py =====
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from churn.config import TrainConfig


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def split(df: pd.DataFrame, cfg: TrainConfig):
    X, y = df[list(cfg.features)], df[cfg.target]
    return train_test_split(X, y, test_size=cfg.test_size, random_state=cfg.seed, stratify=y)


def build_model(seed: int) -> Pipeline:
    # scaler lives INSIDE the pipeline, so fit() only ever sees training rows
    return Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(random_state=seed))])


def train(cfg: TrainConfig) -> dict:
    df = load_data(cfg.data_path)
    Xtr, Xte, ytr, yte = split(df, cfg)
    model = build_model(cfg.seed).fit(Xtr, ytr)
    metrics = {"accuracy": round(float(model.score(Xte, yte)), 4), "n_train": len(Xtr), "n_test": len(Xte)}
    joblib.dump({"model": model, "features": list(cfg.features)}, cfg.out_path)
    return metrics


def predict(model_path: str, rows: pd.DataFrame):
    art = joblib.load(model_path)
    return art["model"].predict(rows[art["features"]])

# ===== src/churn/cli.py =====
import argparse
import json

from churn.config import TrainConfig
from churn.pipeline import predict, train


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="churn")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("--data", required=True)
    t.add_argument("--out", default="model.joblib")
    t.add_argument("--seed", type=int, default=42)
    args = p.parse_args(argv)
    if args.cmd == "train":
        print(json.dumps(train(TrainConfig(data_path=args.data, out_path=args.out, seed=args.seed))))


if __name__ == "__main__":
    main()

# ===== make_data.py =====
import sys, numpy as np, pandas as pd
rng = np.random.default_rng(7)
n = 400
df = pd.DataFrame({"tenure": rng.integers(1, 72, n), "monthly_spend": rng.normal(60, 20, n).round(2), "support_calls": rng.poisson(2, n)})
z = -0.04 * df.tenure + 0.02 * df.monthly_spend + 0.4 * df.support_calls - 0.3 + rng.normal(0, 0.8, n)
df["churned"] = (z > 0).astype(int)
df.to_csv(sys.argv[1], index=False)
print("rows", n, "churn rate", round(df.churned.mean(), 3))

# ===== bug_demo.py =====
# shows what the refactor exposes: the notebook's scaler statistics include the test rows
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv("data.csv")
X, y = df[["tenure", "monthly_spend", "support_calls"]], df["churned"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("mean (all 400 rows, notebook):", X.mean().round(3).tolist())
print("mean (320 train rows, fixed) :", Xtr.mean().round(3).tolist())
print("max abs gap in std units:", float(((X.mean() - Xtr.mean()).abs() / Xtr.std()).max().round(4)))

# ===== tests/test_pipeline.py =====
import numpy as np, pandas as pd
from churn.config import TrainConfig
from churn.pipeline import build_model, split, train, predict


def _df(n=200):
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"tenure": rng.integers(1, 72, n), "monthly_spend": rng.normal(60, 20, n), "support_calls": rng.poisson(2, n)})
    df["churned"] = (df.support_calls + rng.normal(0, 1, n) > 2).astype(int)
    return df


def test_scaler_sees_train_rows_only(tmp_path):
    df = _df(); cfg = TrainConfig(data_path="unused")
    Xtr, Xte, ytr, yte = split(df, cfg)
    m = build_model(cfg.seed).fit(Xtr, ytr)
    np.testing.assert_allclose(m["scale"].mean_, Xtr.mean().values)      # train mean
    assert not np.allclose(m["scale"].mean_, df[list(cfg.features)].mean().values)  # NOT the all-rows mean


def test_train_is_deterministic_and_roundtrips(tmp_path):
    p = tmp_path / "d.csv"; _df().to_csv(p, index=False)
    a = train(TrainConfig(data_path=str(p), out_path=str(tmp_path / "a.joblib")))
    b = train(TrainConfig(data_path=str(p), out_path=str(tmp_path / "b.joblib")))
    assert a == b
    assert len(predict(str(tmp_path / "a.joblib"), _df().head(5))) == 5
```
```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "churn"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["pandas>=2", "scikit-learn>=1.5", "joblib"]

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
churn = "churn.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/churn"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```
```sh
# run_demo.sh
#!/bin/sh
# builds a throwaway venv in a temp dir, installs the package, runs tests and the CLI
set -e
SRC=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d); cd "$T"
cp -r "$SRC"/src "$SRC"/tests "$SRC"/pyproject.toml "$SRC"/make_data.py .
uv venv -q venv; uv pip install -q --python venv/bin/python -e ".[dev]"
venv/bin/python -I make_data.py data.csv
venv/bin/churn train --data data.csv --out model.joblib
venv/bin/churn train --data data.csv --out model2.joblib
venv/bin/python -I -m pytest -q -p no:cacheprovider
cp "$SRC"/bug_demo.py .; venv/bin/python -I bug_demo.py
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, pandas 3.0.5, pytest 9.1.1, uv 0.11.32; a throwaway venv with an editable install. Data is synthetic and seeded (`default_rng(7)`). `notebook_before.py` was not run (it points to a path that does not exist, which is the point). The numbers below were produced by the run.
```text
rows 400 churn rate 0.538
{"accuracy": 0.8375, "n_train": 320, "n_test": 80}
{"accuracy": 0.8375, "n_train": 320, "n_test": 80}
..                                                                       [100%]
2 passed in 1.06s
mean (all 400 rows, notebook): [37.415, 57.454, 1.988]
mean (320 train rows, fixed) : [38.219, 57.492, 2.059]
max abs gap in std units: 0.054
```
The CLI ran twice with the same data and seed and printed the identical metric, and the two pytest tests pass: one checks that the scaler's mean equals the training-rows mean and not the all-rows mean, one checks determinism and a save/load round trip.

**Follow-ups:**
- *Why a Pipeline instead of scaling first and splitting?* A pipeline refits the scaler inside each fit and cross-validation fold automatically, which removes the leak by construction.
- *How do you check you did not break anything?* Compare the metric and predictions on a fixed sample before and after; expect a small honest change from the leak fix only.
- *Where do the pinned deps go?* `pyproject.toml` ranges plus a lockfile, as in a dependency answer.

**Common mistakes:**
- Rewriting everything at once with no behaviour baseline.
- Moving globals into a class but keeping the fit-on-all-rows bug.
- Saving only the model, not the preprocessing.
- Config values as global constants imported everywhere instead of an object passed in.
- Leaving the notebook as the only entry point.

---

### Q16 ⭐⭐ 🟢 Trunk-based development versus Gitflow for an ML team that runs many experiments. Explain short-lived branches, feature flags, long-lived experiment branches and their cost, how releases and hotfixes work in each model, and which you would pick for a team of 6 shipping a model every two weeks. Say how experiment code that never merges is kept (tags or an archive branch) without cluttering main.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** For six people shipping every two weeks I would pick trunk-based development: short-lived branches into main, unfinished work behind flags, releases as tags, and experiments archived as tags instead of long-lived branches.

**Then explain:**
- Trunk-based: branches live a day or two and merge to main often. Main is always releasable. Releases are tags; hotfixes are a fix on main (or a short release branch only if main has moved too far). Less merge pain, easier CI.
- Gitflow: long-lived `develop` and `release/*` branches, feature branches, hotfix branches. It suits versioned products with many supported releases. For a team of six on a two-week cadence it adds merge overhead and drift between branches.
- ML twist: experiments are cheap to start and rarely merge. Long-lived experiment branches rot: they fall behind main, conflict with everything, and nobody can reproduce them. Cost is real: weeks of divergence turn one merge into a mini-project.
- Keep the experiment without cluttering main: tag the last commit (`exp/2026-10-wide-features`), write the result in the tag message or a short doc, then delete the branch. The commit stays reachable through the tag. A shared `archive/` branch namespace is the other common option.
- Unfinished model code merges behind a flag (config value, off by default) so main always builds; turn it on when metrics and tests are ready.
- Failure modes: flags that never get removed (set a cleanup date); a flag changes behaviour in tests only when on (test both); hotfix on main that cannot ship because main holds half-done work (the flag is why this does not happen).

**Example:** Team of six, release every second Friday. Monday: `feat/new-ranker` branch, merged to main behind `USE_NEW_RANKER=false` on Tuesday. A wide-features experiment fails: tag it and delete the branch. Release Friday: tag `release-1.1`. A bug appears Monday: fix on main, tag `release-1.1.1`. In the demo below the history is one straight line plus one merge bubble, and `git branch` lists only `main`.

**Code:** a throwaway-repo walk-through (git 2.43.0).
```sh
# demo.sh
#!/bin/sh
# Trunk-based flow in a throwaway repo: short branch, flag-off merge, archive an experiment as a tag, tagged release, hotfix.
set -e
T=$(mktemp -d); cd "$T"; git init -q -b main; git config user.email a@b.c; git config user.name demo
echo 'MODEL=v1' > config.txt; git add .; git commit -qm "model v1"; git tag release-1.0

# 1. short-lived branch; new model code merged but flagged OFF
git switch -qc feat/new-ranker
echo 'USE_NEW_RANKER=false' >> config.txt; echo 'def new_ranker(): ...' > ranker.py
git add .; git commit -qm "add new ranker behind flag (off)"
git switch -q main; git merge -q --no-ff feat/new-ranker -m "merge: ranker behind flag"; git branch -d feat/new-ranker -q

# 2. an experiment that will never merge: keep it as a tag, then delete the branch
git switch -qc exp/wide-features
echo 'WIDE=1' >> config.txt; git commit -qam "experiment: 400 wide features, metric not better"
git tag -a exp/2026-10-wide-features -m "tried; no gain; see notebook link in wiki"
git switch -q main; git branch -D exp/wide-features -q

# 3. release = a tag on main; hotfix = fix on main, tag again (no long-lived release branch)
echo 'USE_NEW_RANKER=true' > flag.txt; git add .; git commit -qm "turn the flag on"
git tag release-1.1
echo 'fix: null guard' > fix.txt; git add .; git commit -qm "hotfix: null guard"; git tag release-1.1.1

echo "--- branches:"; git branch
echo "--- tags:"; git tag -l
echo "--- history:"; git log --oneline --graph --decorate
echo "--- experiment still reachable:"; git show -s --format='%h %s' exp/2026-10-wide-features^{commit}
```

**Output (my run):** commit hashes differ on every run because timestamps differ.
```text
--- branches:
* main
--- tags:
exp/2026-10-wide-features
release-1.0
release-1.1
release-1.1.1
--- history:
* 5e01680 (HEAD -> main, tag: release-1.1.1) hotfix: null guard
* 5cf9ead (tag: release-1.1) turn the flag on
*   08755dc merge: ranker behind flag
|\  
| * 4ea5443 add new ranker behind flag (off)
|/  
* 250572a (tag: release-1.0) model v1
--- experiment still reachable:
0ce7287 experiment: 400 wide features, metric not better
```

**Follow-ups:**
- *When would Gitflow be right?* Several versions supported in the field at once (an on-prem product), or a heavy manual release gate.
- *Experiment tracking?* Tags keep the code; a tracking tool keeps parameters and metrics (a different topic).
- *Squash or merge commits on main?* Team choice; whichever, keep main linear enough to bisect.

**Common mistakes:**
- Calling any branching "trunk-based" while branches live for weeks.
- Merging half-finished model code to main with the flag on.
- Deleting an experiment branch with no tag, losing the commit after garbage collection.
- A `develop` branch with no clear owner that is always broken.
- Hotfixing release without bringing the fix back to main.

---

### Q17 ⭐⭐ 🟢 What goes into a pull request review checklist for ML code? List at least eight items specific to ML (data leakage, fixed seeds, hard-coded paths, metric on the right split, untracked data version, large diffs from notebooks, missing tests, silent shape or dtype changes), say which a linter could catch, and review a 25-line training function with three planted bugs, naming each bug.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** My ML review checklist starts with data and evaluation, not style: could the test set influence training, is the metric on the right split, is it reproducible, and what changed in the data version and shapes.

**Then explain:** Checklist (the ones a linter can help with are marked):
- Data leakage: any fit (scaler, encoder, feature selection, imputer) before the split. Not catchable by a linter.
- Metric computed on the right split (test or validation, not train). A linter only hints (unused variables, see below).
- Fixed seeds and `random_state` on splits and models. Partly lintable with a custom rule.
- Hard-coded paths and secrets. Lintable (grep rule or a plugin).
- Data version recorded (hash, tag, table snapshot) with the run. Not lintable.
- Large diffs from notebooks (outputs checked in): strip outputs with `nbstripout`; a pre-commit hook catches it.
- Tests for new logic; a new feature has a unit test and the parity or golden test still passes. CI catches missing tests only with a coverage rule.
- Silent shape, dtype or column-order changes (a float turned into an object, a column renamed). Types and schema checks help; mypy catches only some.
- Mutable defaults, unused imports and variables: ruff does these.
- Class imbalance, stratified split, group split for repeated users, time split for time series.
- Does the PR change the model's inputs without changing the serving code?
- The review target below: a short training function (15 lines here, shorter than the 25 in the question; the review method is the same) with three planted bugs.

**Example:** Bug 1: `SelectKBest.fit_transform(X, y)` runs on the whole frame before `train_test_split`, so the test labels choose the features. Bug 2: `train_test_split` has no `random_state`, so the result changes every run. Bug 3: the printed accuracy is `model.score(Xtr, ytr)`, the training split. Plus a smell: hard-coded `/home/me/data.csv`. On pure random labels the honest accuracy should be near 0.5, which gives a hand-check: the leaky pipeline's accuracy is clearly above 0.5, the training score is very high, and a fixed pipeline lands near 0.5.

**Code:** the target function, the fixed version and a harness on seeded noise data (120 rows, 400 random features, random labels).
```python
# ===== review_target.py =====
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def train_and_report(path="/home/me/data.csv"):              # smell: hard-coded path
    df = pd.read_csv(path)
    y = df["y"]
    X = df.drop(columns="y")
    X = SelectKBest(f_classif, k=20).fit_transform(X, y)      # BUG 1: selection sees the test rows
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3)  # BUG 2: no random_state
    model = LogisticRegression(max_iter=200).fit(Xtr, ytr)
    print("accuracy", round(model.score(Xtr, ytr), 3))       # BUG 3: metric on the TRAIN split
    return model

# ===== fixed.py =====
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


def train_and_report(path, seed=0):
    df = pd.read_csv(path)
    X, y = df.drop(columns="y"), df["y"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
    model = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=200)).fit(Xtr, ytr)  # selection inside the pipeline
    print("test accuracy", round(model.score(Xte, yte), 3))
    return model

# ===== harness.py =====
import sys, pathlib, tempfile, numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import review_target, fixed

rng = np.random.default_rng(0)                       # PURE NOISE: 120 rows, 400 features, random labels -> honest accuracy is about 0.5
df = pd.DataFrame(rng.normal(size=(120, 400)), columns=[f"f{i}" for i in range(400)])
df["y"] = rng.integers(0, 2, 120)
p = pathlib.Path(tempfile.mkdtemp()) / "data.csv"; df.to_csv(p, index=False)

print("== buggy, run 3 times (note: prints TRAIN accuracy, and it changes each run)")
for _ in range(3):
    review_target.train_and_report(str(p))
print("== buggy but score on its own test split (what bug 3 hides)")
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X = SelectKBest(f_classif, k=20).fit_transform(df.drop(columns="y"), df["y"])
Xtr, Xte, ytr, yte = train_test_split(X, df["y"], test_size=0.3, random_state=0)
print("leaky test accuracy:", round(LogisticRegression(max_iter=200).fit(Xtr, ytr).score(Xte, yte), 3), "(labels are random, so this should be about 0.5)")
print("== fixed")
fixed.train_and_report(str(p)); fixed.train_and_report(str(p))
```
```sh
# run.sh
python3 -I harness.py
ruff check --output-format=concise review_target.py
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, ruff 0.16.9.
```text
== buggy, run 3 times (note: prints TRAIN accuracy, and it changes each run)
accuracy 0.905
accuracy 0.857
accuracy 0.821
== buggy but score on its own test split (what bug 3 hides)
leaky test accuracy: 0.667 (labels are random, so this should be about 0.5)
== fixed
test accuracy 0.611
test accuracy 0.611
```
ruff on the target (this ruff default set; rule set may differ by version):
```text
q17/review_target.py:12:10: RUF059 Unpacked variable `Xte` is never used
q17/review_target.py:12:20: RUF059 Unpacked variable `yte` is never used
Found 2 errors.
No fixes available (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
```
So the linter flagged the unused test variables, a clue for bug 3, but did not name any of the three bugs. The fixed run reports 0.611 test accuracy on 36 rows, which is within noise of 0.5 for random labels; I do not read it as skill.

**Follow-ups:**
- *Which check is highest value?* Leakage and metric split; they make a good-looking number meaningless.
- *Can a bot do this review?* It can flag patterns, but a human must confirm leakage and data questions.
- *What do you require in the PR description?* Data version, seed, metric on the right split, and what changed in inputs.

**Common mistakes:**
- Reviewing only formatting.
- Approving a metric jump without asking about the split.
- Accepting notebook diffs with outputs.
- Treating a lint pass as a pass on correctness.

---

### Q18 ⭐⭐ 🟡 Cherry-pick and hotfix backports. Version 2.3 of a scoring service is in production, main has moved on to 2.4 work, and a one-line fix to a null-handling bug landed on main. Show how you backport just that commit to a release/2.3 branch with git cherry-pick, what happens when the commit conflicts, why cherry-picking creates a duplicate commit with a new hash, and how to keep track of which fixes went where. Demonstrate in a throwaway repo.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** To backport a fix I switch to `release/2.3`, run `git cherry-pick -x <hash>`, resolve any conflict by hand and continue; it makes a new commit with a new hash that has the same change.

**Then explain:**
- Why a new hash: a commit's hash includes its parent. The same change on a different parent is a different commit, so the copy on the release branch has a new hash. `-x` appends "(cherry picked from commit ...)" so you can trace it.
- Conflict: the release branch has older or different code around the line. Git stops with `UU` status and conflict markers. Edit the file, `git add` it, then `git cherry-pick --continue` (or `--abort` to back out). Always re-run tests on the release branch afterwards, because a clean pick can still be wrong in older code.
- Tracking: `git cherry -v release/2.3 main` marks `-` for commits whose patch is already on release and `+` for those that are not. Also keep a backport label or a changelog line; tools that tag the PR are a team choice.
- Alternatives: fix on the release branch first and merge forward to main, so there is only one change and history stays connected. Cherry-pick is for when the fix was already made on main.
- Failure modes: forgetting to backport to a second supported release; picking a commit that depends on earlier unpicked commits (code compiles, behaves differently); cherry-picking a merge commit (needs `-m`).

**Example:** In the run: `release/2.3` and a 2.4 feature-set commit on main. The null fix on main is `17a9415`; backporting it creates `e6a0f4c` on release. Searching both branches by message shows two commits with different hashes. `git cherry` shows `-` against the null fix (already applied) and `+` against the 2.4 feature-set commit (not on release, correctly). Part B: a second fix ("score never negative") conflicts with a local release tweak ("round score"), so git stops; the resolved line keeps both ideas.

**Code:** run in a throwaway repo (git 2.43.0).
```sh
# demo.sh
#!/bin/sh
T=$(mktemp -d); cd "$T"; git init -q -b main; git config user.email a@b.c; git config user.name demo
cat > score.py <<'PY'
def score(row):
    return row["amount"] * 0.1
PY
git add .; git commit -qm "2.3 scoring service"; git branch release/2.3; git tag v2.3.0
# main moves on to 2.4 work (touches the same area later)
cat > other.py <<'PY'
FEATURE_SET = "v24"
PY
git add .; git commit -qm "2.4: new feature set"
# the one-line null fix lands on main
cat > score.py <<'PY'
def score(row):
    return (row["amount"] or 0) * 0.1
PY
git commit -qam "fix: null amount no longer crashes score()"
FIX=$(git rev-parse --short HEAD)
echo "--- A) clean backport"
git switch -q release/2.3
git cherry-pick -x "$FIX" | head -1
git log --oneline --format='%h %s' -2
echo "--- same change, different hash on each branch:"; git log --oneline --all --grep='null amount'
echo "--- -x records where it came from:"; git log -1 --format=%b
echo "--- git cherry: '-' = an equivalent patch is already on release, '+' = not yet:"; git cherry -v release/2.3 main
echo "--- B) conflicting backport: a second fix on main touches the same line that release changed differently"
git switch -q main
printf 'def score(row):\n    return max((row["amount"] or 0) * 0.1, 0.0)\n' > score.py; git commit -qam "fix: score never negative"
FIX2=$(git rev-parse --short HEAD)
git switch -q release/2.3
printf 'def score(row):\n    return round((row["amount"] or 0) * 0.1, 2)\n' > score.py; git commit -qam "2.3.1: round score"
git cherry-pick -x "$FIX2" 2>&1 | grep -E "CONFLICT|error: could not"
git status --short
echo "--- conflict markers in the file:"; cat score.py
echo "--- resolve by hand (keep both ideas), then continue"
printf 'def score(row):\n    return max(round((row["amount"] or 0) * 0.1, 2), 0.0)\n' > score.py; git add score.py
GIT_EDITOR=true git cherry-pick --continue >/dev/null 2>&1
git log --oneline -4
```

**Output (my run):** hashes differ each run.
```text
--- A) clean backport
[release/2.3 e6a0f4c] fix: null amount no longer crashes score()
e6a0f4c fix: null amount no longer crashes score()
d9019fa 2.3 scoring service
--- same change, different hash on each branch:
17a9415 fix: null amount no longer crashes score()
e6a0f4c fix: null amount no longer crashes score()
--- -x records where it came from:
(cherry picked from commit 17a9415780dc094663046937b4612ff5b3347e29)

--- git cherry: '-' = an equivalent patch is already on release, '+' = not yet:
+ e74237da1751b966478b19db4c6dc4dcf4518323 2.4: new feature set
- 17a9415780dc094663046937b4612ff5b3347e29 fix: null amount no longer crashes score()
--- B) conflicting backport: a second fix on main touches the same line that release changed differently
CONFLICT (content): Merge conflict in score.py
error: could not apply 4cb52c9... fix: score never negative
UU score.py
--- conflict markers in the file:
def score(row):
<<<<<<< HEAD
    return round((row["amount"] or 0) * 0.1, 2)
=======
    return max((row["amount"] or 0) * 0.1, 0.0)
>>>>>>> 4cb52c9 (fix: score never negative)
--- resolve by hand (keep both ideas), then continue
accbc72 fix: score never negative
13c6680 2.3.1: round score
e6a0f4c fix: null amount no longer crashes score()
d9019fa 2.3 scoring service
```

**Follow-ups:**
- *What if the commit touches many files?* Cherry-pick a range (`A..B`), or merge a fix branch that was cut from an old enough base.
- *Rebase instead?* No; rebasing release onto main would pull in 2.4 work.
- *How do you avoid doing the fix twice?* Branch the fix from the oldest supported release and merge it into the newer ones.

**Common mistakes:**
- Forgetting `-x`, so the origin is lost.
- Assuming a clean pick is a correct pick, with no tests on the release branch.
- Cherry-picking one commit of a dependent series.
- Backporting to release but never recording it, then shipping 2.3.2 without it.

---

### Q19 ⭐⭐ 🟡 Make randomness testable. A function train_test_split_and_fit(df, seed) gives slightly different metrics on every run. Explain seeding Python, NumPy (np.random.default_rng) and sklearn random_state, the limits of seeding (multi-threaded libraries, GPU kernels), and how to assert on floats with pytest.approx or np.testing.assert_allclose with a justified tolerance. Show a flaky test and the fixed version, both run.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Pass a seed through the function, use a local `np.random.default_rng(seed)` and `random_state`, and assert floats with a tolerance I can justify; seeding is for reproducibility, tolerances are for the leftovers.

**Then explain:**
- Where randomness lives: the train/test split, model initialisation, data generation, shuffling, sampling and dropout. Seed all that you use: `random.seed`, `np.random.seed` (legacy global), a local `np.random.default_rng(seed)` (preferred, no hidden state), and `random_state=seed` in scikit-learn.
- Limits: multi-threaded libraries can sum in a different order, so floats differ in the last digits; GPU kernels and some ops are non-deterministic unless a deterministic mode is on (check the framework's docs); different BLAS builds or CPUs give tiny differences; a different library version can change the algorithm.
- So: same machine, same code, same seed should be exactly equal (assert `==`). Across machines use `pytest.approx(abs=...)` or `np.testing.assert_allclose(rtol=..., atol=...)`. Choose the tolerance from the noise you saw (here a metric is deterministic at 1e-6) and write the reason in a comment.
- For the model quality itself, do not assert one lucky number; assert a floor below the spread seen over many seeds.
- Failure modes: a tolerance so wide it hides bugs (`atol=0.1` on a metric); relying on `np.random.seed` while a library uses its own generator; a seed set once at import so test order changes results.

**Example:** `0.1 + 0.2 == 0.3` is `False` in Python, so exact float equality is the wrong tool for computed values. In the data below, 20 seeds gave a metric spread (min 0.678, max 0.822), so a test that demands `> 0.77` on an unseeded split passes only part of the time. In my run of that flaky test, 6 of 8 runs passed and 2 failed with identical code.

**Code:** `fitmod.py` (with `seed=None` reproducing the original bug), the flaky test and the fixed tests. Run with `python3 -I -m pytest`.
```python
# ===== fitmod.py =====
import random
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def make_df(n=300, seed=0):
    rng = np.random.default_rng(seed)               # local generator: no hidden global state
    x = rng.normal(size=(n, 3))
    y = (x[:, 0] + 0.5 * x[:, 1] + rng.normal(scale=1.0, size=n) > 0).astype(int)
    return pd.DataFrame(x, columns=["a", "b", "c"]).assign(y=y)


def train_test_split_and_fit(df, seed=None):
    """seed=None reproduces the original problem: the split changes every call."""
    if seed is not None:
        random.seed(seed); np.random.seed(seed)      # only matters for third-party code using the globals
    Xtr, Xte, ytr, yte = train_test_split(df[["a", "b", "c"]], df["y"], test_size=0.3, random_state=seed)
    m = LogisticRegression(random_state=seed).fit(Xtr, ytr)
    return float(m.score(Xte, yte))

# ===== test_flaky.py =====
from fitmod import make_df, train_test_split_and_fit
def test_flaky():
    # unseeded split: the metric moves around, and the threshold sits right in the middle of that spread
    assert train_test_split_and_fit(make_df()) > 0.77

# ===== test_fixed.py =====
import numpy as np, pytest
from fitmod import make_df, train_test_split_and_fit

GOLDEN = 0.7666666666666667      # recorded once with seed=1 (python3 -I run, scikit-learn 1.9.1)


def test_same_seed_same_metric():
    df = make_df()
    assert train_test_split_and_fit(df, seed=1) == train_test_split_and_fit(df, seed=1)   # exact: same machine, same code


def test_golden_metric_with_tolerance():
    # 1e-6 absolute: allows tiny BLAS/platform differences, still catches a changed split or model
    assert train_test_split_and_fit(make_df(), seed=1) == pytest.approx(GOLDEN, abs=1e-6)


def test_metric_is_good_across_seeds():
    # property test: do not depend on one lucky split; assert a floor below the observed spread (min 0.678 over 20 seeds)
    accs = [train_test_split_and_fit(make_df(), seed=s) for s in range(20)]
    assert min(accs) > 0.60


def test_arrays_close():
    np.testing.assert_allclose(np.array([0.1 + 0.2]), [0.3], rtol=1e-9)   # 0.1+0.2 != 0.3 exactly
```
```ini
# pytest.ini
[pytest]
pythonpath = .
```
```sh
# run.sh
for i in 1 2 3 4 5 6 7 8; do python3 -I -m pytest -q -p no:cacheprovider test_flaky.py | tail -1; done   # flaky, then count
python3 -I -m pytest -q -p no:cacheprovider test_fixed.py
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1. Spread printed by a one-off script: seed 1 gives 0.7667; across 20 seeds min 0.678, mean 0.772, max 0.822, std 0.034.
The flaky test, 8 runs (count of results), then the fixed file:
```text
      2 1 failed
      6 1 passed
4 passed in 1.50s
```

**Follow-ups:**
- *Why `default_rng` and not `np.random.seed`?* The global seed is shared state: another test or library can change it. A local generator passed into the function is explicit.
- *Can I make a GPU run bit-exact?* Often with deterministic flags and fixed library versions, at some speed cost; do not promise it across hardware. Check the framework docs.
- *What tolerance for an ML metric?* Based on repeat runs: a few standard deviations of the seed spread for quality floors; much tighter (1e-6) for the same-seed regression value.

**Common mistakes:**
- Hard-coding a number copied from one run with no seed.
- Seeding only NumPy while scikit-learn uses its own `random_state`.
- `assert a == b` on floats from different code paths.
- Tolerances picked to make the test pass, without a reason.
- Re-seeding inside the function and surprising callers.

---

### Q20 ⭐⭐ 🟡 pytest features used in ML test suites: fixtures (including scope), parametrize, tmp_path, monkeypatch and markers. Write a conftest.py fixture that builds a small seeded DataFrame once per session, a test that uses tmp_path to check a save and load round trip of a model artifact, and a test that monkeypatches a slow model-download function. Say how you mark and skip slow tests (--runslow style) and show the run.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Fixtures build shared inputs (scope controls how often), `parametrize` repeats a test over cases, `tmp_path` gives a clean folder, `monkeypatch` swaps slow or networked code for a stub, and a `slow` marker plus a `--runslow` option keeps heavy tests out of the default run.

**Then explain:**
- Fixture scope: `function` (default, rebuilt per test), `module`, `session` (once for the whole run). A seeded small DataFrame is cheap and read-only, so session scope is fine; a trained model used by many tests is a good `module` fixture. Danger: a session fixture that tests mutate leaks state between tests, so return copies or treat it as read-only.
- `parametrize` turns one test into many named cases (`test_fit_on_subsets[10]`); good for sizes, edge values, and dtype cases.
- `tmp_path`: a unique temp directory per test, cleaned up later by pytest. Use it for save and load round trips instead of writing into the repo.
- `monkeypatch`: replace `download_pretrained` for the test only; it is undone afterwards. Patch the name where it is looked up (the module that calls it).
- Markers: register `slow` in `pytest.ini` (otherwise a warning, and an error with `--strict-markers`). A `conftest.py` hook adds a skip to marked tests unless `--runslow` is passed. Also use `pytest -m "not slow"` for the fast gate in CI.
- Failure modes: autouse fixtures that hide a dependency; an order-dependent test that only passes after another one; patching the wrong import path so the real function runs (here it would sleep and raise).

**Example:** Six tests were collected: a round trip (fit, `joblib.dump` to `tmp_path`, reload, same predictions), one monkeypatched test, three parametrized sizes (10, 25 and 50 rows) and one slow test. Hand count: 1 + 1 + 3 + 1 = 6. Default run: 5 pass and 1 skipped. With `--runslow`, the slow test runs and fails on purpose here because there is no network (and the real function sleeps 5 seconds, which is why the run took about 6 seconds).

**Code:** `pytest.ini`, `conftest.py` (fixtures and the `--runslow` hook), the code under test and the tests.
```ini
# pytest.ini
[pytest]
pythonpath = .
markers =
    slow: slow tests, skipped unless --runslow is given
```
```python
# ===== modelio.py =====
import time
import joblib
from sklearn.linear_model import LogisticRegression


def download_pretrained(name: str):
    time.sleep(5)                                   # pretend this is a big network download
    raise RuntimeError("no network in tests")


def fit_and_save(df, path):
    m = LogisticRegression().fit(df[["a", "b"]], df["y"])
    joblib.dump(m, path)
    return m


def load_embeddings(name: str):
    weights = download_pretrained(name)
    return weights

# ===== tests/conftest.py =====
import numpy as np
import pandas as pd
import pytest


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="run tests marked slow")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip = pytest.mark.skip(reason="slow: use --runslow to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip)


BUILDS = []                                          # counts how often the fixture body really ran


@pytest.fixture(scope="session")
def small_df():
    BUILDS.append(1)                                 # built once per session, shared by every test
    rng = np.random.default_rng(0)
    x = rng.normal(size=(50, 2))
    return pd.DataFrame({"a": x[:, 0], "b": x[:, 1], "y": (x[:, 0] > 0).astype(int)})


@pytest.fixture(scope="session", autouse=True)
def report_builds():
    yield
    print(f"\n[session fixture small_df built {len(BUILDS)} time(s)]")

# ===== tests/test_modelio.py =====
import joblib
import numpy as np
import pytest
import modelio


def test_save_load_roundtrip(small_df, tmp_path):
    path = tmp_path / "m.joblib"                       # fresh temp dir, auto-cleaned later
    m = modelio.fit_and_save(small_df, path)
    loaded = joblib.load(path)
    np.testing.assert_array_equal(m.predict(small_df[["a", "b"]]), loaded.predict(small_df[["a", "b"]]))


def test_load_embeddings_without_network(monkeypatch):
    monkeypatch.setattr(modelio, "download_pretrained", lambda name: {"fake": name})   # replace the slow call
    assert modelio.load_embeddings("tiny") == {"fake": "tiny"}


@pytest.mark.parametrize("n_rows", [10, 25, 50])
def test_fit_on_subsets(small_df, tmp_path, n_rows):
    modelio.fit_and_save(small_df.head(n_rows), tmp_path / "x.joblib")
    assert (tmp_path / "x.joblib").exists()


@pytest.mark.slow
def test_real_download():
    modelio.load_embeddings("big")                      # would hit the network
```
```sh
# run.sh
python3 -I -m pytest -v -s -p no:cacheprovider               # default: slow test skipped
python3 -I -m pytest -q -p no:cacheprovider --runslow        # includes the slow test (fails here: no network)
```

**Output (my run):** Python 3.13.17, pytest 9.1.1, scikit-learn 1.9.1, joblib 1.6.0.
```text
tests/test_modelio.py::test_save_load_roundtrip PASSED
tests/test_modelio.py::test_load_embeddings_without_network PASSED
tests/test_modelio.py::test_fit_on_subsets[10] PASSED
tests/test_modelio.py::test_fit_on_subsets[25] PASSED
tests/test_modelio.py::test_fit_on_subsets[50] PASSED
tests/test_modelio.py::test_real_download SKIPPED (slow: use --runsl...)
[session fixture small_df built 1 time(s)]
========================= 5 passed, 1 skipped in 1.02s =========================
=========================== short test summary info ============================
FAILED tests/test_modelio.py::test_real_download - RuntimeError: no network i...
1 failed, 5 passed in 6.18s
```
The fixture counter shows the session-scoped DataFrame was built once for the four tests that used it.

**Follow-ups:**
- *Fixture or helper function?* Fixture when pytest should manage setup, teardown and sharing; helper when it is a plain pure function.
- *How do I run only a few?* `-k name`, `-m marker`, or `path::test_name`.
- *Can I share conftest across packages?* Yes: a `conftest.py` applies to its folder and below.

**Common mistakes:**
- Session fixtures that tests modify.
- Unregistered markers.
- Patching `modelio.download_pretrained` after `from modelio import download_pretrained` already copied the name elsewhere.
- Writing test artefacts into the repo instead of `tmp_path`.
- Skipping slow tests forever so they rot; run them nightly in CI.

---

### Q21 ⭐⭐ 🟡 Data validation tests as code. Write a validate(df) function (using pydantic, plain pandas or pandera, your choice, say why) that checks columns and dtypes, non-null keys, a value range, allowed category values and uniqueness of an id, and reports all violations at once instead of stopping at the first. Test it on a good frame and a frame with four planted problems, and say where in the pipeline it runs (ingest, before training, before serving) and what happens on failure.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** I write one `validate(df)` function in plain pandas that checks every rule, collects the problems in a list and returns them all, so the team fixes the data once instead of five times.

**Then explain:**
- Why plain pandas: no extra dependency, I control the messages, and it is easy to explain. pandera is the better pick when many people share schemas (declare once, `lazy=True` collects all failures, I cross-check it below). pydantic validates row by row, which is slow and clumsy for a big frame, so I keep it for configs and API payloads.
- Rules, in order: columns exist, dtype family is right, key not null, key unique, value in range, category in the allowed set. If a column is missing, I report it and skip the other checks on that column.
- Where it runs: at ingest (reject or quarantine the file), before training (hard stop, do not train on bad data), before serving (cheap schema check on each batch or request). Same function, different strictness.
- On failure: the job exits non-zero, an alert goes out with the violation list, and the pipeline keeps using the last good dataset or model. I never silently fill or drop rows in the validator.
- Two traps from my own run: one null turns an integer id column into float, so I use nullable `Int64` and check dtype families; and pandas 3 shows text as `str`, not `object`, so exact string dtype checks break across versions.

**Example:** The bad frame has 4 rows. `loan_id = [1, 1, NA, 4]` gives a null key and a duplicate id 1. `age = [25, 17, 130, 40]` puts rows 1 and 2 out of range. `segment` has `vip`, which is not allowed. That is four planted problems and the function reports exactly four lines. The good frame returns an empty list.

**Code:** `python3 -I q21.py`
```python
# Q21: validate(df) that reports ALL violations at once (plain pandas), plus a pandera lazy cross-check.
import pandas as pd
import pandera.pandas as pa

from pandas.api import types as T
# dtype FAMILIES, not exact strings: pandas 3 uses "str" for text, older pandas used "object"
EXPECTED = {"loan_id": ("integer", T.is_integer_dtype), "age": ("integer", T.is_integer_dtype),
            "income": ("float", T.is_float_dtype), "segment": ("string", T.is_string_dtype)}
SEGMENTS = {"retail", "sme", "corporate"}

def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of human-readable violations. Empty list = valid."""
    errs = []
    # 1) columns and dtypes: if a column is missing we cannot check it further
    missing = [c for c in EXPECTED if c not in df.columns]
    errs += [f"missing column: {c}" for c in missing]
    for c, (family, is_ok) in EXPECTED.items():
        if c in df.columns and not is_ok(df[c].dtype):
            errs.append(f"dtype of {c}: expected {family}, got {df[c].dtype}")
    # 2) non-null key
    if "loan_id" in df.columns:
        n = int(df["loan_id"].isna().sum())
        if n:
            errs.append(f"loan_id has {n} null(s)")
        # 3) uniqueness of the id (ignore nulls, already reported)
        dup = df["loan_id"].dropna()
        dup = dup[dup.duplicated(keep=False)].unique().tolist()
        if dup:
            errs.append(f"loan_id not unique: {sorted(dup)}")
    # 4) value range
    if "age" in df.columns:
        bad = df.index[(df["age"] < 18) | (df["age"] > 100)].tolist()
        if bad:
            errs.append(f"age outside [18, 100] at rows {bad}")
    # 5) allowed categories
    if "segment" in df.columns:
        bad = sorted(set(df["segment"].dropna()) - SEGMENTS)
        if bad:
            errs.append(f"segment has unknown values: {bad}")
    return errs

good = pd.DataFrame({"loan_id": [1, 2, 3], "age": [25, 40, 61],
                     "income": [5.0, 7.5, 6.1], "segment": ["retail", "sme", "corporate"]})
# four planted problems: null key, duplicate id, age 17 / 130, unknown segment 'vip'
bad = pd.DataFrame({"loan_id": pd.array([1, 1, None, 4], dtype="Int64"), "age": [25, 17, 130, 40],
                    "income": [5.0, 7.5, 6.1, 4.0], "segment": ["retail", "vip", "sme", "sme"]})
print("good frame ->", validate(good))
errs = validate(bad)
print("bad frame  ->", len(errs), "violations")
for e in errs:
    print("  -", e)

# same idea with pandera, lazy=True collects every failure (version printed below)
schema = pa.DataFrameSchema({
    "loan_id": pa.Column("Int64", nullable=False, unique=True),
    "age": pa.Column(int, pa.Check.in_range(18, 100)),
    "income": pa.Column(float),
    "segment": pa.Column(str, pa.Check.isin(sorted(SEGMENTS))),
})
try:
    schema.validate(bad, lazy=True)
except pa.errors.SchemaErrors as e:
    print("pandera lazy failure cases:", len(e.failure_cases))
    print(e.failure_cases[["column", "check", "failure_case"]].to_string(index=False))
import importlib.metadata as md
print("pandera", md.version("pandera"), "pandas", pd.__version__)
assert validate(good) == [] and len(errs) == 4
```

**Output (my run):** pandas 3.0.5, pandera 0.35.0 (pandera also reports 6 failure cases because it lists duplicates and each bad age separately).
```text
good frame -> []
bad frame  -> 4 violations
  - loan_id has 1 null(s)
  - loan_id not unique: [1]
  - age outside [18, 100] at rows [1, 2]
  - segment has unknown values: ['vip']
pandera lazy failure cases: 6
 column                                check failure_case
loan_id                         not_nullable         <NA>
loan_id                     field_uniqueness            1
loan_id                     field_uniqueness            1
    age                    in_range(18, 100)           17
    age                    in_range(18, 100)          130
segment isin(['corporate', 'retail', 'sme'])          vip
pandera 0.35.0 pandas 3.0.5
```

**Follow-ups:**
- *Hard rule or warning?* Keys, schema and categories are hard rules. Distribution checks (mean shifted) are warnings with thresholds, and they belong to monitoring, not to this function.
- *Why not Great Expectations?* It is fine for big teams, but it is heavier. For a small pipeline a 30-line function plus tests is easier to own (check current docs if the team already uses it).
- *How do you test the validator?* With the good frame and one frame per rule, each asserting the exact message. A validator without tests is itself untested code.

**Common mistakes:**
- Raising on the first problem, so the data team fixes one issue per run.
- Checking `dtype == "object"` or `"int64"` as strings and breaking after a pandas upgrade or after one null appears.
- Validating after `fillna`, which hides the nulls.
- Forgetting uniqueness of the id, then joining and silently duplicating rows.

### Q22 ⭐⭐ 🟡 Write tests that catch data leakage. Using seeded data, show a leaky pipeline (scaler fitted on all rows, or duplicate rows across train and test, or a target-derived feature) and the tests that expose each: no id overlap between train and test, scaler statistics equal to train-only statistics, and an unrealistically high score alarm. Run the leaky and fixed versions with scikit-learn and report both scores.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Leakage tests check the split and the preprocessing, not just the score: no shared ids between train and test, scaler statistics equal to train-only statistics, and an alarm when the score is too good.

**Then explain:**
- Three classic leaks: fit a scaler or imputer on all rows before splitting; the same entity in both train and test (duplicates, or several rows per customer); a feature built from the target or from the future.
- Test 1, id overlap: `set(train.id) & set(test.id)` must be empty. If rows from one customer can appear twice, split by customer group, not by row.
- Test 2, scaler stats: after fitting, `scaler.mean_` must equal the train mean. Scale-before-split leaks only a little, so the score barely moves (my run shows 0.708 vs 0.708). The stats test still catches it. A score alarm would not.
- Test 3, score alarm: if AUC is far above what this problem allows, stop and look for leakage. The ceiling is a judgement per problem; mine is 0.90 for a weak-signal task.
- Best fix is structural: put the scaler inside a `Pipeline` and use `GroupKFold` or a split by id, so the leak cannot be written by accident.

**Example:** Seed 0, 400 rows, `x1` weakly predicts `y`. I duplicate 100 rows before the split, so 41 ids land in both train and test; a RandomForest memorises them and reports AUC 0.841 against an honest 0.576. A feature `leak = 5*y + noise` gives AUC 1.000 against an honest 0.708. All of this is in the output below.

**Code:** `python3 -I q22.py`
```python
# Q22: leaky vs fixed pipelines, plus tests that expose each leak. Seeded, scikit-learn.
import numpy as np, pandas as pd, sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

SEED = 0
rng = np.random.default_rng(SEED)
n = 400
df = pd.DataFrame({"id": np.arange(n), "x1": rng.normal(size=n), "x2": rng.normal(10, 5, size=n)})
df["y"] = (0.3 * df.x1 + rng.normal(size=n) > 0).astype(int)   # weak signal on purpose
FEATS = ["x1", "x2"]

def auc(tr, te, feats):
    m = LogisticRegression().fit(tr[feats], tr["y"])
    return roc_auc_score(te["y"], m.predict_proba(te[feats])[:, 1])

# ---- tests (plain functions that return None or raise AssertionError) ----
def test_no_id_overlap(tr, te):
    both = set(tr["id"]) & set(te["id"])
    assert not both, f"{len(both)} ids in both train and test"

def test_scaler_uses_train_only(scaler, tr):
    assert np.allclose(scaler.mean_, tr[FEATS].mean().to_numpy()), "scaler mean != train mean"

def test_score_not_suspicious(score, ceiling=0.90):
    assert score < ceiling, f"AUC {score:.3f} >= {ceiling}: too good for this problem, look for leakage"

def run(name, checks):
    bad = []
    for label, fn in checks:
        try: fn()
        except AssertionError as e: bad.append(f"{label}: {e}")
    print(f"  {name}: " + ("all tests pass" if not bad else f"{len(bad)} test(s) FAIL"))
    for b in bad: print("     -", b)

# ---- leak 1: scaler fitted on ALL rows before the split ----
tr, te = train_test_split(df, test_size=0.25, random_state=SEED)
leaky_sc = StandardScaler().fit(df[FEATS])                      # sees test rows
good_sc = StandardScaler().fit(tr[FEATS])
print("1) scaler fitted before the split")
run("leaky", [("scaler stats", lambda: test_scaler_uses_train_only(leaky_sc, tr))])
run("fixed", [("scaler stats", lambda: test_scaler_uses_train_only(good_sc, tr))])

# ---- leak 2: duplicate rows across train and test (same id appears twice before split) ----
dup = pd.concat([df, df.sample(100, random_state=SEED)], ignore_index=True)   # 100 rows duplicated
tr_d, te_d = train_test_split(dup, test_size=0.25, random_state=SEED)
tr_f, te_f = train_test_split(df, test_size=0.25, random_state=SEED)           # dedupe first = split by id
# a flexible model memorises duplicates, so use a tree to show the effect
from sklearn.ensemble import RandomForestClassifier
def auc_rf(tr_, te_, feats):
    m = RandomForestClassifier(n_estimators=100, random_state=SEED).fit(tr_[feats], tr_["y"])
    return roc_auc_score(te_["y"], m.predict_proba(te_[feats])[:, 1])
s_leak, s_fix = auc_rf(tr_d, te_d, FEATS), auc_rf(tr_f, te_f, FEATS)
print("2) duplicate rows across train/test")
run("leaky", [("id overlap", lambda: test_no_id_overlap(tr_d, te_d))])
run("fixed", [("id overlap", lambda: test_no_id_overlap(tr_f, te_f))])
print(f"   RandomForest AUC leaky={s_leak:.3f} fixed={s_fix:.3f}")

# ---- leak 3: a target-derived feature (e.g. 'refund_amount' only exists when y = 1) ----
df3 = df.assign(leak=df["y"] * 5 + rng.normal(0, 0.1, size=n))
tr3, te3 = train_test_split(df3, test_size=0.25, random_state=SEED)
s3_leak = auc(tr3, te3, FEATS + ["leak"]); s3_fix = auc(tr3, te3, FEATS)
print("3) target-derived feature")
run("leaky", [("score alarm", lambda: test_score_not_suspicious(s3_leak))])
run("fixed", [("score alarm", lambda: test_score_not_suspicious(s3_fix))])
print(f"   LogisticRegression AUC leaky={s3_leak:.3f} fixed={s3_fix:.3f}")

# ---- leak 1 score effect (small, honest): scaling leak rarely changes AUC much ----
def auc_scaled(sc):
    Xtr, Xte = sc.transform(tr[FEATS]), sc.transform(te[FEATS])
    m = LogisticRegression().fit(Xtr, tr["y"]); return roc_auc_score(te["y"], m.predict_proba(Xte)[:, 1])
print(f"1b) scaler-leak AUC leaky={auc_scaled(leaky_sc):.3f} fixed={auc_scaled(good_sc):.3f}  (the stats test catches it even when the score barely moves)")
print("seed", SEED, "numpy", np.__version__, "pandas", pd.__version__, "sklearn", sklearn.__version__)
```

**Output (my run):** Python 3.13, scikit-learn 1.9.1, numpy 2.5.3, pandas 3.0.5, seed 0.
```text
1) scaler fitted before the split
  leaky: 1 test(s) FAIL
     - scaler stats: scaler mean != train mean
  fixed: all tests pass
2) duplicate rows across train/test
  leaky: 1 test(s) FAIL
     - id overlap: 41 ids in both train and test
  fixed: all tests pass
   RandomForest AUC leaky=0.841 fixed=0.576
3) target-derived feature
  leaky: 1 test(s) FAIL
     - score alarm: AUC 1.000 >= 0.9: too good for this problem, look for leakage
  fixed: all tests pass
   LogisticRegression AUC leaky=1.000 fixed=0.708
1b) scaler-leak AUC leaky=0.708 fixed=0.708  (the stats test catches it even when the score barely moves)
seed 0 numpy 2.5.3 pandas 3.0.5 sklearn 1.9.1
```

**Follow-ups:**
- *Time series?* Split by time (train on past, test on future) and add a test that `max(train.date) < min(test.date)`.
- *Cross-validation?* Put preprocessing inside the `Pipeline` passed to `cross_val_score`, so each fold refits it on its own training part.
- *Is a high score always a leak?* No. It is a reason to investigate. Some tasks are easy. The alarm triggers a human, not an automatic failure of the model.

**Common mistakes:**
- Fitting `StandardScaler`, `SimpleImputer` or target encoding on the whole dataset first.
- Random row split when the same customer has many rows.
- Tuning hyperparameters on the test set and then calling it unbiased.
- Trusting a good score without a baseline to compare against.

### Q23 ⭐⭐ 🟡 Property-based testing with Hypothesis for ML utilities. Write properties for a min-max scaler and a train/test splitter (output in [0,1] when the input is non-constant, order of rows preserved or not, sizes add up, no row lost or duplicated) and let Hypothesis find a failing edge case in a deliberately naive implementation (constant column, a single row, NaN or inf). Run it and show the shrunk counterexample. Say when this is worth the effort versus example tests.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Property-based testing states a rule that must hold for all inputs (output in [0, 1], sizes add up, no row lost), and Hypothesis generates many inputs, finds one that breaks the rule and shrinks it to the smallest example.

**Then explain:**
- Properties for a min-max scaler: same length out, every value in [0, 1] for finite input, bigger input never gives smaller output, and a defined behaviour for constant columns and NaN or inf (raise or return zeros, but never silent NaN).
- Properties for a splitter: train plus test sizes equal n, every index appears exactly once (no loss, no duplicate), both sides non-empty when n >= 2, same seed gives the same split.
- In my run the naive scaler failed on `[0.0]` (a single row is also a constant column: 0/0 gives NaN) and on `[nan]`. The naive splitter sampled with replacement and truncated with `int()`, so it failed on `n=15` (9 + 7 rows is not 15, and index 4 is duplicated) and on `n=2` (empty test set).
- The monotone property passed for both, which is a useful result too: it tells me that part is safe.
- Worth it for pure functions with clear rules: scalers, splitters, encoders, metric code, parsers. Not worth it for plumbing, IO, or model training. Example tests stay for known regression cases.

**Example:** Hand-check the shrunk case: `minmax([0.0])` computes `(0 - 0) / (0 - 0) = 0/0 = nan`, and `nan >= 0` is False, so the property fails. For the splitter, `n=2, frac=0.25`: `int(2 * 0.25) = 0`, so the test set is empty.

**Code:** `IMPL=impl_naive` or `IMPL=impl_fixed` picks which implementation the same tests run against. `derandomize=True` makes the run repeatable.
```python
# ===== file: impl_naive.py =====
import numpy as np

def minmax(x):
    x = np.asarray(x, dtype=float)
    return (x - x.min()) / (x.max() - x.min())          # constant column -> 0/0

def split_idx(n, test_frac, seed):
    rng = np.random.default_rng(seed)
    n_test = int(n * test_frac)                          # truncates: n=2, 0.2 -> 0 test rows
    test = rng.integers(0, n, size=n_test)               # sampling WITH replacement -> duplicates
    train = np.setdiff1d(np.arange(n), test)
    return train, test

# ===== file: impl_fixed.py =====
import numpy as np

def minmax(x):
    x = np.asarray(x, dtype=float)
    if x.size == 0 or not np.isfinite(x).all():
        raise ValueError("minmax needs a non-empty array of finite numbers")
    lo, hi = x.min(), x.max()
    if hi == lo:
        return np.zeros_like(x)                          # documented choice: constant column -> all 0.0
    return (x - lo) / (hi - lo)

def split_idx(n, test_frac, seed):
    if n < 2:
        raise ValueError("need at least 2 rows to split")
    n_test = min(max(round(n * test_frac), 1), n - 1)    # both sides non-empty
    perm = np.random.default_rng(seed).permutation(n)    # without replacement
    return np.sort(perm[n_test:]), np.sort(perm[:n_test])

# ===== file: test_props.py =====
import importlib, os
import numpy as np
from hypothesis import assume, given, settings, strategies as st

impl = importlib.import_module(os.environ["IMPL"])
S = settings(derandomize=True, database=None, max_examples=200)   # same run every time
finite = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)
arrays = st.lists(finite, min_size=1, max_size=20)

@S
@given(arrays)
def test_minmax_in_unit_interval(xs):
    out = impl.minmax(xs)
    assert out.shape == (len(xs),)
    assert np.all((out >= 0) & (out <= 1)), out          # also fails on NaN

@S
@given(arrays)
def test_minmax_is_monotone(xs):
    assume(len(set(xs)) > 1)                              # constant columns are a separate rule
    x, out = np.asarray(xs), impl.minmax(xs)
    order = np.argsort(x, kind="stable")
    assert (np.diff(out[order]) >= 0).all()               # bigger input never gives smaller output

@S
@given(st.lists(st.sampled_from([float("nan"), float("inf"), -float("inf"), 1.0, 2.0]), min_size=1, max_size=5))
def test_minmax_rejects_non_finite_or_returns_finite(xs):
    try:
        out = impl.minmax(xs)
    except ValueError:
        return
    assert np.isfinite(out).all(), out                  # never hand NaN downstream silently

split_args = dict(n=st.integers(2, 50), frac=st.floats(0.05, 0.95), seed=st.integers(0, 2**32 - 1))

@S
@given(**split_args)
def test_split_sizes_add_up_no_loss_no_dup(n, frac, seed):
    tr, te = impl.split_idx(n, frac, seed)
    assert len(tr) + len(te) == n, (len(tr), len(te))
    assert sorted(np.concatenate([tr, te]).tolist()) == list(range(n))   # every row exactly once

@S
@given(**split_args)
def test_split_both_sides_non_empty(n, frac, seed):
    tr, te = impl.split_idx(n, frac, seed)
    assert len(tr) > 0 and len(te) > 0

@S
@given(**split_args)
def test_split_is_deterministic(n, frac, seed):
    a, b = impl.split_idx(n, frac, seed), impl.split_idx(n, frac, seed)
    assert all(np.array_equal(p, q) for p, q in zip(a, b))
```
```bash
IMPL=impl_naive python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
IMPL=impl_fixed python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
```

**Output (my run):** naive output is trimmed (warnings and long assertion helpers removed); hypothesis 6.170.11, pytest 9.1.1, numpy 2.5.3. The `n=15` split case did not shrink further because that failure depends on the random draw.
```text
$ IMPL=impl_naive python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
F.FFF.                                                                   [100%]
=================================== FAILURES ===================================
_________________________ test_minmax_in_unit_interval _________________________
test_props.py:11: in test_minmax_in_unit_interval
test_props.py:15: in test_minmax_in_unit_interval
    assert np.all((out >= 0) & (out <= 1)), out          # also fails on NaN
E   AssertionError: array([nan])
E   assert np.False_
E   Failing test case: test_minmax_in_unit_interval(
E       xs=[0.0],
E   )
_______________ test_minmax_rejects_non_finite_or_returns_finite _______________
test_props.py:26: in test_minmax_rejects_non_finite_or_returns_finite
test_props.py:32: in test_minmax_rejects_non_finite_or_returns_finite
    assert np.isfinite(out).all(), out                  # never hand NaN downstream silently
E   AssertionError: array([nan])
E   assert np.False_
E   Failing test case: test_minmax_rejects_non_finite_or_returns_finite(
E       xs=[nan],
E   )
____________________ test_split_sizes_add_up_no_loss_no_dup ____________________
test_props.py:37: in test_split_sizes_add_up_no_loss_no_dup
test_props.py:40: in test_split_sizes_add_up_no_loss_no_dup
    assert len(tr) + len(te) == n, (len(tr), len(te))
E   AssertionError: (9, 7)
E   assert (9 + 7) == 15
E   Failing test case: test_split_sizes_add_up_no_loss_no_dup(
E       n=15,
E       frac=0.5,
E       seed=0,
E   )
_______________________ test_split_both_sides_non_empty ________________________
test_props.py:44: in test_split_both_sides_non_empty
test_props.py:47: in test_split_both_sides_non_empty
    assert len(tr) > 0 and len(te) > 0
E   assert (2 > 0 and 0 > 0)
E   Failing test case: test_split_both_sides_non_empty(
E       n=2,
E       frac=0.25,
E       seed=0,  # or any other generated value
E   )
=========================== short test summary info ============================
FAILED test_props.py::test_minmax_in_unit_interval - AssertionError: array([n...
FAILED test_props.py::test_minmax_rejects_non_finite_or_returns_finite - Asse...
FAILED test_props.py::test_split_sizes_add_up_no_loss_no_dup - AssertionError...
FAILED test_props.py::test_split_both_sides_non_empty - assert (2 > 0 and 0 > 0)
4 failed, 2 passed, 38 warnings in 2.60s
hypothesis 6.170.11 pytest 9.1.1 numpy 2.5.3

$ IMPL=impl_fixed python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
......                                                                   [100%]
6 passed in 1.78s
hypothesis 6.170.11 pytest 9.1.1 numpy 2.5.3
```

**Follow-ups:**
- *Why does Hypothesis try NaN and inf?* Because real data has them. That is the point: it explores the places I forgot.
- *How do I replay a failure?* Hypothesis keeps a database of failing examples locally and prints a reproduce hint. I also turn a found case into a normal example test so the regression stays pinned.
- *Float roundoff?* Compare with `pytest.approx` or `np.isclose`. Also note that tiny differences can collapse into the same scaled value, so I test "non-decreasing", not "strictly increasing".

**Common mistakes:**
- Writing a property that just re-implements the function, so it can never fail.
- Unbounded floats, which find overflow in every function and bury the real rules (I bounded floats to +/- 1e6 on purpose).
- Leaving the test random in CI with no seed policy, then being unable to reproduce.
- Using Hypothesis everywhere. It costs run time and thinking time.

### Q24 ⭐⭐ 🟡 Test coverage in ML repos. A repo reports 92 percent line coverage but a bad scaling bug shipped. Explain line versus branch coverage, why coverage does not measure assertions or data coverage, what a sensible target and a diff-coverage rule look like, and how to run coverage with pytest-cov and fail under a threshold. Show a tiny function where 100 percent line coverage still misses a bug, with the run.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Coverage only tells me which lines ran during tests, not whether the tests checked anything or used the right data, so 92 percent coverage can still ship a scaling bug.

**Then explain:**
- Line coverage: was this line executed. Branch coverage: was each side of every `if` taken. Branch is stricter and I turn it on (`--cov-branch`).
- What it cannot see: missing assertions, wrong expected values, and data coverage. A scaler tested only with `lo = 0` runs every line and never notices a wrong formula.
- Sensible target: a floor around the team's current level (often 70-85 percent; no magic number), a fail-under so it never drops, and a diff-coverage rule: new or changed lines in a PR must be covered (for example 80 percent or more). Diff coverage punishes new untested code and does not force teams to chase old code.
- Honest use: coverage finds untested code. It does not prove tested code is right. Pair it with property tests, regression tests on real examples, and review.
- In ML repos watch for the big blind spots: data issues, training loops marked `# pragma: no cover`, and notebooks that are not measured at all.

**Example:** `scale(x, lo, hi)` returns `(x - lo) / hi`; it should divide by `hi - lo`. One test, `scale(5, 0, 10, clip=True) == 0.5`, passes because `lo = 0` hides the bug. Line coverage is 100 percent, branch coverage is 86 percent (the `clip=False` path was never taken), and the bug is still there. A second test with `lo = 10` fails: expected 0.5, got 0.25. The bug was found by a better test, not by any coverage number.

**Code:** the function and tests, the commands, and the diff-coverage demo (temp git repo).
```python
# ===== file: scaling.py =====
def scale(x, lo, hi, clip=False):
    out = (x - lo) / hi              # BUG: should divide by (hi - lo)
    if clip:
        out = min(max(out, 0.0), 1.0)
    return out

# ===== file: test_scaling.py =====
from scaling import scale

def test_scale_clip():
    assert scale(5, 0, 10, clip=True) == 0.5     # lo = 0 hides the bug

# ===== file: test_scaling_more.py =====
from scaling import scale

def test_scale_nonzero_lo():
    assert scale(15, 10, 20) == 0.5              # (15-10)/(20-10); the buggy code gives 0.25
```
```bash
# line coverage, then branch coverage, both failing under 100
python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-report=term-missing --cov-fail-under=100 test_scaling.py
python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-branch --cov-report=term-missing --cov-fail-under=100 test_scaling.py
# diff coverage in a throwaway git repo (needs: pip install diff-cover)
python3 -I -m pytest -q --cov=lib --cov-report=xml test_lib.py
diff-cover coverage.xml --compare-branch=main~1 --fail-under=80
```

**Output (my run):** coverage 7.17.0, pytest-cov 7.1.0, diff-cover 10.6.0. First the three runs, then the diff-coverage run: the PR added a 4-line function with no test, so 1 of 4 new lines is covered (25 percent) and the gate fails.
```text
$ python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-report=term-missing --cov-fail-under=100 test_scaling.py   # line coverage only
.                                                                        [100%]
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.13.17-final-0 _______________

Name         Stmts   Miss  Cover   Missing
------------------------------------------
scaling.py       5      0   100%
------------------------------------------
TOTAL            5      0   100%
Required test coverage of 100% reached. Total coverage: 100.00%
1 passed in 0.16s
exit=0

$ ... --cov-branch   # same tests, branch coverage on
.
ERROR: Coverage failure: total of 86 is less than fail-under=100
                                                                         [100%]
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.13.17-final-0 _______________

Name         Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------
scaling.py       5      0      2      1    86%   3->5
--------------------------------------------------------
TOTAL            5      0      2      1    86%
FAIL Required test coverage of 100% not reached. Total coverage: 85.71%
1 passed in 0.13s
exit=1

$ add a test with lo != 0 -> the bug shows up (coverage was never the thing that could catch it)
.F                                                                       [100%]
=================================== FAILURES ===================================
E   assert 0.25 == 0.5
     +  where 0.25 = scale(15, 10, 20)
/home/user/case_studies/interviews/scratch/B4P01_Q21-30/code/q24/test_scaling_more.py:4: assert 0.25 == 0.5
=========================== short test summary info ============================
FAILED test_scaling_more.py::test_scale_nonzero_lo - assert 0.25 == 0.5
1 failed, 1 passed in 0.13s
exit=1
coverage 7.17.0 pytest-cov 7.1.0


Coverage XML written to file coverage.xml
1 passed in 0.14s
$ diff-cover coverage.xml --compare-branch=main~1 --fail-under=80
-------------
Diff Coverage
Diff: main~1...HEAD, staged and unstaged changes
-------------
lib.py (25.0%): Missing lines 5-7
-------------
Total:   4 lines
Missing: 3 lines
Coverage: 25%
-------------

Failure. Coverage is below 80%.
exit=1
```

**Follow-ups:**
- *Is 100 percent a good target?* No. It pushes people to write assertion-free tests. A fail-under floor plus a diff rule works better.
- *How do you measure test quality instead?* Mutation testing (tools like mutmut; concept, not run here) changes the code and checks that a test fails. That catches the `/ hi` bug.
- *Where does the threshold live?* In `pyproject.toml` or CI config, so it is the same on every laptop and in CI.

**Common mistakes:**
- Treating the coverage percent as a quality score.
- Counting tests that call the function but assert nothing.
- Only using the easy input (`lo = 0`, no NaN, balanced classes).
- Excluding hard code with `# pragma: no cover` until the number looks good.

### Q25 ⭐⭐ 🟡 Use git bisect to find the commit that broke the model. Accuracy dropped between a good tag v1.0 and the current HEAD across 12 commits. Show a throwaway repo with a deterministic test script, then run git bisect start/good/bad and git bisect run to locate the first bad commit and count the steps. Say how you handle commits that cannot build (git bisect skip) and why a flaky test breaks bisect.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** I give Git one good commit and one bad commit plus a script that exits 0 for good and 1 for bad, and `git bisect run` finds the first bad commit by binary search in about log2 of N steps.

**Then explain:**
- Setup: `git bisect start HEAD v1.0`. The first commit is bad, the second is good. Git checks out the middle commit, runs my script, reads the exit code, and halves the range.
- Exit codes: 0 means good, 1 to 127 (except 125) means bad, 125 means "cannot test this commit, skip it". A commit that does not compile or install is a skip, not a bad.
- Steps: 12 commits after the tag means about 4 tests instead of 12. My run tested 5 commits because one of them was a skip.
- The script must be deterministic: seeded data, fixed threshold on the metric, no network. A threshold like "accuracy >= 0.85" is better than "accuracy equals 0.885".
- A flaky test breaks bisect, because one wrong answer sends Git into the wrong half and it names a confident, wrong commit. My demo makes the check lie once and Git blames c8 instead of c9. Fix: make it deterministic, or run it several times in the script and only exit 1 when it fails every time.

**Example:** A tag `v1.0` has accuracy 0.885. Twelve commits later HEAD has 0.615. Commit c6 does not compile (syntax error), c7 fixes it, and c9 changes `scale` from 1.0 to 0.6 in `cfg.json`. Bisect skips c6 and returns `c9` as the first bad commit. Hand-check: with scale 0.6 a class-1 point needs x >= 0.833 to pass the 0.5 threshold, so most class-1 rows are wrong and accuracy falls from 0.885 to 0.615 (the HEAD line in the output).

**Code:** the whole demo, run in a temp repo with fixed commit dates, so the hashes and the bisect path are the same every run.
```bash
set -e
D=$(mktemp -d); cd "$D"
export GIT_AUTHOR_DATE="2026-01-01T00:00:00+0000" GIT_COMMITTER_DATE="2026-01-01T00:00:00+0000"   # fixed dates: same hashes every run
git init -q -b main; git config user.email a@b.c; git config user.name demo
# the "model": threshold classifier on 200 seeded points; accuracy must stay >= 0.85
cat > train.py <<'PY'
import random, json
random.seed(0)
cfg = json.load(open("cfg.json"))
pts = [(random.random() * 0.55, 0) for _ in range(100)] + [(0.45 + random.random() * 0.55, 1) for _ in range(100)]
# class 0 lives in [0,0.55), class 1 in [0.45,1): a little overlap, so ~0.9 accuracy at threshold 0.5
hits = sum((x * cfg["scale"] >= cfg["threshold"]) == bool(y) for x, y in pts)
print(f"accuracy={hits/len(pts):.3f}")
PY
cat > check.sh <<'SH'
#!/bin/sh
# exit 0 = good, 1 = bad, 125 = cannot test this commit (skip)
python3 -I -m py_compile train.py 2>/dev/null || exit 125
acc=$(python3 -I train.py | sed 's/accuracy=//')
python3 -I -c "import sys; sys.exit(0 if float('$acc') >= 0.85 else 1)"
SH
chmod +x check.sh
echo '{"threshold": 0.5, "scale": 1.0}' > cfg.json
git add .; git commit -qm "v1.0 baseline"; git tag v1.0
echo "baseline: $(python3 -I train.py)"
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  case $i in
    6) echo 'def broken(:' >> train.py ;;                                   # c6: does not even compile
    7) sed -i '$d' train.py ;;                                              # c7: fixes the syntax error
    9) echo '{"threshold": 0.5, "scale": 0.6}' > cfg.json ;;               # c9: the real culprit (bad scale)
    *) echo "# note $i" >> README.md ;;
  esac
  git add -A; git commit -qm "c$i"
done
echo "HEAD:     $(python3 -I train.py)"
echo; echo '$ git bisect start HEAD v1.0 && git bisect run ./check.sh'
git bisect start HEAD v1.0 >/dev/null
git bisect run ./check.sh > run.log 2>&1 || true
grep -E "^(Bisecting|running)|is the first bad commit|^    c[0-9]+$" run.log | sed -E 's#^running .*check.sh.*#running ./check.sh#; s/^[0-9a-f]{40} is/<sha> is/'
echo "commits tested by the script (one of them skipped): $(git bisect log | grep -c "^git bisect \(good\|bad\|skip\)")"
git bisect log | grep -E "^(# (good|bad|skip)|git bisect (good|bad|skip))" | sed -E 's/\[[0-9a-f]{40}\]//; s/git bisect (good|bad|skip) [0-9a-f]{40}/git bisect \1 <sha>/' | grep '^#' 
git bisect reset >/dev/null 2>&1
echo; echo '--- a flaky check blames the wrong commit (deterministic demo: it lies once, on its 3rd call) ---'
cat > flaky.sh <<'SH'
#!/bin/sh
n=$(cat /tmp/_flaky_count 2>/dev/null || echo 0); n=$((n+1)); echo $n > /tmp/_flaky_count
[ "$n" -eq 3 ] && exit 1          # lies once: reports 'bad' for a good commit
exec ./check.sh
SH
chmod +x flaky.sh; rm -f /tmp/_flaky_count
git bisect start HEAD v1.0 >/dev/null
git bisect run ./flaky.sh > flaky.log 2>&1 || true
grep -E "first bad|could be any|^[0-9a-f]{40} |^    c[0-9]+$" flaky.log | sed -E "s/^[0-9a-f]{40} /<sha> /"
git bisect reset >/dev/null 2>&1; rm -f /tmp/_flaky_count
git --version
```

**Output (my run):** git 2.43.0. Five commits tested (c6 skipped, c3 good, c8 good, c10 bad, c9 bad), culprit c9. Short hashes are replaced with `<sha>`.
```text
baseline: accuracy=0.885
HEAD:     accuracy=0.615

$ git bisect start HEAD v1.0 && git bisect run ./check.sh
running ./check.sh
Bisecting: 5 revisions left to test after this (roughly 3 steps)
running ./check.sh
Bisecting: 3 revisions left to test after this (roughly 2 steps)
running ./check.sh
Bisecting: 1 revision left to test after this (roughly 1 step)
running ./check.sh
Bisecting: 0 revisions left to test after this (roughly 0 steps)
running ./check.sh
<sha> is the first bad commit
    c9
commits tested by the script (one of them skipped): 5
# bad:  c12
# good:  v1.0 baseline
# skip:  c6
# good:  c3
# good:  c8
# bad:  c10
# bad:  c9

--- a flaky check blames the wrong commit (deterministic demo: it lies once, on its 3rd call) ---
<sha> is the first bad commit
    c8
bisect found first bad commit
git version 2.43.0
```

**Follow-ups:**
- *What if the tag is not good?* Bisect only works if the good commit is really good. Check it first by running the script on it.
- *Can I bisect a metric, not a pass/fail?* Yes: the script computes the metric and exits 1 below a threshold. Pick the threshold with margin so noise cannot flip it.
- *How do I finish?* `git bisect reset` returns to where I started. Then I write a regression test so the fix stays.

**Common mistakes:**
- Using an unseeded training run as the check, so results flip between runs.
- Marking a broken build as bad instead of skipping it, so Git blames the build break.
- Forgetting `git bisect reset` and committing on a detached HEAD.
- Not saving the real culprit: after bisect, add a regression test, or the bug can return.

### Q26 ⭐⭐ 🟡 Git hooks and the pre-commit framework for data science teams. Configure hooks that strip notebook outputs, block files larger than 5 MB, detect obvious secrets in staged changes (a regex-based hook, hedge on tools) and run ruff. Show the .pre-commit-config.yaml, a commit that gets blocked and one that passes, and explain how the same checks must also run in CI because local hooks can be bypassed.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I put the checks in `.pre-commit-config.yaml` so they run on every `git commit` (strip notebook outputs, block big files, block obvious secrets, lint with ruff), and I run the same config in CI because anyone can skip local hooks.

**Then explain:**
- pre-commit runs each hook on the staged files only, so it is fast. If a hook modifies files (nbstripout, ruff `--fix`) the commit fails once, and I `git add` and commit again.
- My four hooks: `nbstripout` cleans notebooks (small diffs, no leaked data in outputs); a 5 MB size check points to DVC or Git LFS; a regex secrets check; `ruff check`.
- The regex secrets hook is a tripwire, not a scanner. It misses many leaks and gives false alarms. Real teams use a maintained secret scanner (for example detect-secrets or gitleaks; check current docs) and also rotate any key that ever reached a commit.
- Hooks can be bypassed (`git commit --no-verify`) or never installed. So CI runs `pre-commit run --all-files`, and branch protection (hosted-service setting, check current docs) makes that check required.
- For a demo that runs offline I used `repo: local` hooks. In a real repo most teams pin published hook repos with `rev:` and keep the versions updated.

**Example:** My first commit adds a notebook with an output, a 6 MB file, `API_KEY = "sk_live_abcdef123456"` and a script with an unused import. All four hooks fail: nbstripout rewrites the notebook, the size check names `big.bin` (6.0 MB), the secrets check flags `config.py:1`, and ruff reports F401 for `train.py`. After removing the big file, reading the key from the environment, deleting the import and re-adding the cleaned notebook, the second commit passes all four.

**Code:** config, the two hook scripts, and the demo run in a temp git repo.
```yaml
# .pre-commit-config.yaml  (all hooks are "local" so this demo runs offline)
# In a real repo you would normally pin published hook repos with rev: (check current docs).
repos:
  - repo: local
    hooks:
      - id: nbstripout
        name: strip notebook outputs
        entry: nbstripout
        language: system
        files: \.ipynb$
      - id: no-big-files
        name: block files larger than 5 MB
        entry: python3 -I tools/check_big_files.py
        language: system
        pass_filenames: true
      - id: no-secrets
        name: block obvious secrets (regex, not a real scanner)
        entry: python3 -I tools/check_secrets.py
        language: system
        pass_filenames: true
      - id: ruff
        name: ruff lint
        entry: ruff check --isolated --select E,F
        language: system
        types: [python]
        exclude: ^tools/
```
```python
# ===== file: check_big_files.py =====
import os, sys
LIMIT = 5 * 1024 * 1024
bad = [f for f in sys.argv[1:] if os.path.getsize(f) > LIMIT]
for f in bad:
    print(f"{f}: {os.path.getsize(f)/1024/1024:.1f} MB > 5 MB (use DVC or Git LFS instead)")
sys.exit(1 if bad else 0)

# ===== file: check_secrets.py =====
import re, sys
# deliberately small; real teams use a maintained scanner (detect-secrets, gitleaks, ...). Check current docs.
PATTERNS = [r"AKIA[0-9A-Z]{16}", r"(?i)(api[_-]?key|secret|password|token)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
            r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"]
bad = 0
for f in sys.argv[1:]:
    try: text = open(f, errors="ignore").read()
    except OSError: continue
    for i, line in enumerate(text.splitlines(), 1):
        if any(re.search(p, line) for p in PATTERNS):
            print(f"{f}:{i}: looks like a secret"); bad = 1
sys.exit(bad)
```
```bash
set -e
D=$(mktemp -d); cd "$D"
git init -q -b main; git config user.email a@b.c; git config user.name demo
cp "$1/pre-commit-config.yaml" .pre-commit-config.yaml; cp -r "$1/tools" tools
git add -A; git commit -qm "add hooks" --no-verify
pre-commit install | sed "s#$D#<repo>#"
# a notebook with an output, a 6 MB file, a fake key, and a lint error
python3 -I - <<'PY'
import json
nb = {"cells":[{"cell_type":"code","execution_count":1,"metadata":{},"source":["print(1)"],
       "outputs":[{"output_type":"stream","name":"stdout","text":["1\n"]}]}],
      "metadata":{},"nbformat":4,"nbformat_minor":5}
json.dump(nb, open("eda.ipynb","w"))
open("big.bin","wb").write(b"0"*(6*1024*1024))
open("config.py","w").write('API_KEY = "sk_live_abcdef123456"\n')
open("train.py","w").write("import os\nprint('hi')\n")      # unused import -> ruff F401
PY
git add -A
echo '$ git commit -m "add eda"      # should be BLOCKED'
git commit -m "add eda" 2>&1 | sed -E 's/^(.{0,100}).*/\1/' | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
echo; echo "--- fix each problem ---"
git rm -q --cached big.bin; rm big.bin
printf 'import os\nAPI_KEY = os.environ["API_KEY"]\n' > config.py
printf 'print("hi")\n' > train.py
git add -A            # nbstripout already cleaned eda.ipynb in the working tree during the failed run
echo '$ git commit -m "add eda"      # second try'
git commit -m "add eda" 2>&1 | sed -E 's/^(.{0,100}).*/\1/' | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
echo; echo '--- bypass is possible: git commit --no-verify. So CI runs the same hooks: ---'
echo '$ pre-commit run --all-files   # same config, run in CI'
pre-commit run --all-files 2>&1 | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
git log --oneline | cat
git show --stat --format=%s HEAD | head -5
python3 -I -c "import json,subprocess; nb=json.loads(subprocess.check_output(['git','show','HEAD:eda.ipynb'])); print('outputs in the committed notebook:', nb['cells'][0]['outputs'])"
```

**Output (my run):** pre-commit 4.7.0, ruff 0.16.9, nbstripout 0.9.1. The config also parses with pyyaml (4 hooks). Warnings from nbstripout about missing cell ids are filtered out. The commit hash is from this run.
```text
pre-commit installed at .git/hooks/pre-commit
$ git commit -m "add eda"      # should be BLOCKED
strip notebook outputs...................................................Failed
- hook id: nbstripout
- files were modified by this hook
block files larger than 5 MB.............................................Failed
- hook id: no-big-files
- exit code: 1
big.bin: 6.0 MB > 5 MB (use DVC or Git LFS instead)
block obvious secrets (regex, not a real scanner)........................Failed
- hook id: no-secrets
- exit code: 1
config.py:1: looks like a secret
ruff lint................................................................Failed
- hook id: ruff
- exit code: 1
F401 [*] `os` imported but unused
 --> train.py:1:8
  |
1 | import os
  |        ^^
2 | print('hi')
  |
help: Remove unused import: `os`
  |
  - import os
1 | print('hi')
  |
Found 1 error.
[*] 1 fixable with the `--fix` option.

--- fix each problem ---
$ git commit -m "add eda"      # second try
strip notebook outputs...................................................Passed
block files larger than 5 MB.............................................Passed
block obvious secrets (regex, not a real scanner)........................Passed
ruff lint................................................................Passed
[main 6772647] add eda
 3 files changed, 20 insertions(+)
 create mode 100644 config.py
 create mode 100644 eda.ipynb
 create mode 100644 train.py

--- bypass is possible: git commit --no-verify. So CI runs the same hooks: ---
$ pre-commit run --all-files   # same config, run in CI
strip notebook outputs...................................................Passed
block files larger than 5 MB.............................................Passed
block obvious secrets (regex, not a real scanner)........................Passed
ruff lint................................................................Passed
6772647 add eda
3f5b50f add hooks
add eda

 config.py |  2 ++
 eda.ipynb | 17 +++++++++++++++++
 train.py  |  1 +
outputs in the committed notebook: []
```

**Follow-ups:**
- *Hook too slow?* Run only fast checks locally (format, lint, size, secrets) and move tests to CI.
- *What about a key already committed?* Rotate it first. Removing it from history (git filter-repo) comes second, because clones and forks may still have it.
- *Big files that are really needed?* Version them with DVC or Git LFS (Part 4 covers DVC), not plain Git.

**Common mistakes:**
- Relying on local hooks only, with no CI check.
- Believing a regex hook catches all secrets.
- Committing notebooks with outputs, so a customer table sits in Git history.
- Not telling new team members to run `pre-commit install`.

### Q27 ⭐⭐ 🟡 Versioning and tagging a model package. Explain semantic versioning for a library that wraps a model (what is a major, minor and patch change when the feature set or the output scale changes), how you tag a release in Git, how the model artifact version is linked to the code tag and the data version, and how you roll back. Show git tag -a, a version string read at runtime from package metadata (importlib.metadata) and a changelog entry, run in a temp repo.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** I use semantic versioning MAJOR.MINOR.PATCH for the package, tag each release with `git tag -a vX.Y.Z`, read the version at runtime from package metadata, and store the code tag and data version next to the model artifact so I can roll back by installing the previous tag.

**Then explain:**
- PATCH: bug fix, same contract (clamp negative income). MINOR: new feature that old callers can ignore (an optional `tenure_years` argument). MAJOR: anything that can break a caller, and a change of output scale is exactly that (0-1 to 0-100 breaks every threshold downstream).
- A retrained model with the same features and scale is usually a patch or minor, but I also record a separate model version in the registry. Code version and model version are different things, and both must be traceable.
- Link them: the model card or registry entry stores code tag, data version (a DVC revision, snapshot id or hash) and metrics. From any prediction I can get to code, data and model.
- Single source of truth: the version lives in `pyproject.toml`, and the code reads it with `importlib.metadata.version`, so no second copy can drift.
- Rollback: the previous tag is still installable. Check it out or reinstall that version, and the model card shows the old version and old output scale. The old model artifact stays in the registry, so I do not retrain in an emergency.

**Example:** Releases: 1.0.0 (first), 1.1.0 (optional argument, backward compatible), 1.1.1 (clamp negatives), 2.0.0 (output 0-100, BREAKING). Hand-check the scale: `score(40)` gives 0.4 on 1.1.1 and 40 on 2.0.0, and the output below shows exactly that after the rollback.

**Code:** run in a temp repo with fixed commit dates; installed into a venv with the hatchling build backend (installed locally, no network needed).
```bash
set -e
export GIT_AUTHOR_DATE="2026-01-01T00:00:00+0000" GIT_COMMITTER_DATE="2026-01-01T00:00:00+0000"
D=$(mktemp -d); cd "$D"
git init -q -b main; git config user.email a@b.c; git config user.name demo
mkdir -p src/credit_model
pyproject() { cat > pyproject.toml <<T
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "credit-model"
version = "$1"
dependencies = []

[tool.hatch.build.targets.wheel]
packages = ["src/credit_model"]
T
}
code() { cat > src/credit_model/__init__.py <<P
from importlib.metadata import version

__version__ = version("credit-model")   # single source of truth: the installed package metadata

def score(income$1):
    """Risk score in $2."""
    return $3

def model_card():
    return {"code_version": __version__, "data_version": "loans-2026-01", "output_scale": "$4"}
P
}
release() { git add -A; git commit -qm "release $1"; git tag -a "v$1" -m "credit-model $1 $2"; }

pyproject 1.0.0; code "" "[0, 1]" "min(income / 100.0, 1.0)" "0-1"
printf '# Changelog\n\n## 1.0.0\n- First release. score() returns a value in [0, 1].\n' > CHANGELOG.md
release 1.0.0 "(data loans-2026-01)"

pyproject 1.1.0; code ", tenure_years=0" "[0, 1]" "min(income / 100.0, 1.0)" "0-1"          # new optional arg: MINOR
printf '# Changelog\n\n## 1.1.0\n- Added optional tenure_years argument (backward compatible).\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 1.1.0 ""

pyproject 1.1.1; code ", tenure_years=0" "[0, 1]" "max(min(income / 100.0, 1.0), 0.0)" "0-1"   # clamp negatives: PATCH
printf '# Changelog\n\n## 1.1.1\n- Fix: negative income no longer gives a negative score.\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 1.1.1 ""

pyproject 2.0.0; code ", tenure_years=0" "[0, 100]" "max(min(income, 100.0), 0.0)" "0-100"        # scale change: MAJOR
printf '# Changelog\n\n## 2.0.0 (BREAKING)\n- score() now returns 0-100 instead of 0-1. Update your thresholds.\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 2.0.0 "(output scale 0-100)"

echo '$ git tag -n1'; git tag -n1
echo; echo '$ head -9 CHANGELOG.md'; head -9 CHANGELOG.md

python3 -m venv --system-site-packages "$D/.venv" >/dev/null
PIP="$D/.venv/bin/pip install -q --no-build-isolation --no-deps --disable-pip-version-check"
echo; echo "--- install the latest tag, read version at runtime ---"
git checkout -q v2.0.0; $PIP .
"$D/.venv/bin/python" -I -c "import credit_model as m; print(m.__version__, m.score(40), m.model_card())"
echo "--- rollback: check out the previous good tag and reinstall ---"
git checkout -q v1.1.1; $PIP --force-reinstall .
"$D/.venv/bin/python" -I -c "import credit_model as m; print(m.__version__, m.score(40), m.model_card())"
echo; echo '$ git describe --tags   # one commit after v2.0.0'
git checkout -q main; echo "" >> CHANGELOG.md; git commit -qam "docs"; git describe --tags | sed -E 's/g[0-9a-f]+$/g<sha>/'
```

**Output (my run):** git 2.43.0, Python 3.13, hatchling 1.32.4. `git describe` hash replaced with `<sha>`.
```text
$ git tag -n1
v1.0.0          credit-model 1.0.0 (data loans-2026-01)
v1.1.0          credit-model 1.1.0
v1.1.1          credit-model 1.1.1
v2.0.0          credit-model 2.0.0 (output scale 0-100)

$ head -9 CHANGELOG.md
# Changelog

## 2.0.0 (BREAKING)
- score() now returns 0-100 instead of 0-1. Update your thresholds.
## 1.1.1
- Fix: negative income no longer gives a negative score.
## 1.1.0
- Added optional tenure_years argument (backward compatible).
## 1.0.0

--- install the latest tag, read version at runtime ---
2.0.0 40 {'code_version': '2.0.0', 'data_version': 'loans-2026-01', 'output_scale': '0-100'}
--- rollback: check out the previous good tag and reinstall ---
1.1.1 0.4 {'code_version': '1.1.1', 'data_version': 'loans-2026-01', 'output_scale': '0-1'}

$ git describe --tags   # one commit after v2.0.0
v2.0.0-1-g<sha>
```

**Follow-ups:**
- *Annotated or lightweight tags?* Annotated (`-a`): they carry author, date and message, and show in `git describe`. I use them for releases.
- *Do I need to bump for a retrain?* My rule: new model artifact always gets a registry version. The package version moves only if the code or contract changed.
- *Calendar versioning?* Some teams use dates for data-heavy projects. Pick one scheme, write it down, and automate the bump.

**Common mistakes:**
- Version number hard-coded in two places (`pyproject.toml` and `__init__.py`).
- Changing the output scale in a patch release.
- Shipping a model file with no record of the code and data that made it.
- Moving or re-using a tag after release instead of making a new one.

### Q28 ⭐⭐ 🟡 Configuration management for ML code. A training script has learning rate, paths and feature lists hard-coded. Move them to a YAML file validated by a pydantic model, with environment overrides and a CLI flag, and fail fast on unknown keys or wrong types. Show the code with a good and a bad config run, say how you log the resolved config with each run, and when a config framework such as Hydra is worth it (hedge, concept only).
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I move every knob into one YAML file, load it into a pydantic model that forbids unknown keys and checks types and ranges, apply overrides in a fixed order (file, then environment, then CLI), and log the resolved config with the run.

**Then explain:**
- Precedence is easy to explain: defaults, then YAML, then `TRAIN_*` environment variables, then CLI flags. The last one wins. The run output below shows each layer winning.
- Fail fast: `extra="forbid"` turns a typo like `epoch` into an error instead of a silent default, and `Field(gt=0, le=1)` stops `learning_rate: fast` or `epochs: 0` before any compute starts.
- All problems are reported together (pydantic collects them), so one run shows both mistakes.
- Log the resolved config (after all overrides) as JSON plus a short hash with each run, in MLflow params or a file next to the model. The YAML file alone is not enough, because the env and CLI values may differ.
- Secrets do not go in YAML. Read them from the environment or a secret manager.
- Hydra (hedge, not run here) is worth it when I need config composition, sweeps over many parameters, or many experiment variants. For one script with ten keys, YAML plus pydantic is enough.

**Example:** `config.yaml` says `epochs: 5`. With `TRAIN_EPOCHS=20` it becomes 20. With `TRAIN_EPOCHS=20 --epochs 3` it becomes 3. The bad file has `learning_rate: fast` and the typo `epoch: 5`; both are reported and the exit code is 2.

**Code:** `python3 -I train.py --config config.yaml`
```yaml
# ===== file: config.yaml =====
learning_rate: 0.01
epochs: 5
data_path: data/train.csv
features: [age, income, tenure]
seed: 42

# ===== file: bad_config.yaml =====
learning_rate: fast        # wrong type
epoch: 5                   # typo: unknown key (and 'epochs' is missing -> default used, which is the danger)
data_path: data/train.csv
features: [age, income]
```
```python
"""Config: defaults < YAML file < env vars (TRAIN_*) < CLI flags. Unknown keys and wrong types fail fast."""
import argparse, hashlib, json, os, sys
import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")            # a typo like 'epoch' is an error, not silently ignored
    learning_rate: float = Field(0.1, gt=0, le=1)
    epochs: int = Field(10, ge=1)
    data_path: str = "data/train.csv"
    features: list[str] = Field(min_length=1)
    seed: int = 0

def load(path, cli_overrides):
    raw = yaml.safe_load(open(path)) or {}
    for key in Config.model_fields:                      # env: TRAIN_LEARNING_RATE=0.05 etc.
        env = os.environ.get("TRAIN_" + key.upper())
        if env is not None:
            raw[key] = yaml.safe_load(env)               # parse "0.05" -> float, "[a,b]" -> list
    raw.update({k: v for k, v in cli_overrides.items() if v is not None})
    return Config(**raw)                                 # validation happens here

def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--learning-rate", type=float)
    p.add_argument("--epochs", type=int)
    a = p.parse_args(argv)
    try:
        cfg = load(a.config, {"learning_rate": a.learning_rate, "epochs": a.epochs})
    except ValidationError as e:
        print(f"CONFIG ERROR ({e.error_count()} problem(s)):")
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']} (got {err.get('input')!r})")
        return 2
    resolved = cfg.model_dump()
    blob = json.dumps(resolved, sort_keys=True)
    print("resolved config:", blob)
    print("config hash:", hashlib.sha256(blob.encode()).hexdigest()[:12], "(log this with the run, e.g. as an MLflow param or a JSON file)")
    # ... training would start here, using only cfg.*
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

**Output (my run):** pydantic 2.13.5, pyyaml 6.0.1.
```text
$ python3 -I train.py --config config.yaml
resolved config: {"data_path": "data/train.csv", "epochs": 5, "features": ["age", "income", "tenure"], "learning_rate": 0.01, "seed": 42}
config hash: ac04e83152fd (log this with the run, e.g. as an MLflow param or a JSON file)
exit=0

$ TRAIN_EPOCHS=20 python3 -I train.py --config config.yaml   # env overrides file
resolved config: {"data_path": "data/train.csv", "epochs": 20, "features": ["age", "income", "tenure"], "learning_rate": 0.01, "seed": 42}
config hash: 92680eff27c1 (log this with the run, e.g. as an MLflow param or a JSON file)
exit=0

$ TRAIN_EPOCHS=20 python3 -I train.py --config config.yaml --epochs 3 --learning-rate 0.5   # CLI wins
resolved config: {"data_path": "data/train.csv", "epochs": 3, "features": ["age", "income", "tenure"], "learning_rate": 0.5, "seed": 42}
config hash: 37d87f7fbb73 (log this with the run, e.g. as an MLflow param or a JSON file)
exit=0

$ python3 -I train.py --config bad_config.yaml
CONFIG ERROR (2 problem(s)):
  - learning_rate: Input should be a valid number, unable to parse string as a number (got 'fast')
  - epoch: Extra inputs are not permitted (got 5)
exit=2

$ TRAIN_EPOCHS=0 python3 -I train.py --config config.yaml
CONFIG ERROR (1 problem(s)):
  - epochs: Input should be greater than or equal to 1 (got 0)
exit=2
pydantic 2.13.5 pyyaml 6.0.1
```

**Follow-ups:**
- *Why not argparse only?* Twenty flags are hard to review and repeat. A file can be committed, diffed and reused.
- *Different environments (dev, prod)?* One base file plus a small override file per environment, or env vars for the few values that change (paths, endpoints).
- *Typed config at runtime?* Pass the `Config` object around, not a dict, so a misspelled attribute fails in the IDE and in mypy.

**Common mistakes:**
- Silently ignoring unknown keys.
- Parsing env vars as strings, so `"False"` is truthy.
- Logging only the YAML, not the final values.
- Putting passwords or API keys in the committed config.

### Q29 ⭐⭐ 🟡 Logging and error handling in ML pipelines. Replace print debugging in a batch scoring function with the logging module: levels, a structured JSON log line with run id and row counts, raising specific exceptions on bad input versus logging and continuing, and never swallowing exceptions in a bare except. Show the code, its output on a good and a bad batch, and what you would alert on.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I replace `print` with the `logging` module, log JSON lines that carry a run id and row counts, raise a specific exception when the whole batch is unusable, log a warning and continue when only a few rows are bad, and never use a bare `except`.

**Then explain:**
- Levels: DEBUG for detail, INFO for normal milestones (batch received, batch scored), WARNING for something odd but handled (dropped rows), ERROR for a failed batch. Production runs at INFO.
- Structured logs (one JSON object per line) can be searched and counted: filter by `run_id`, plot `rows_bad`. Free text cannot.
- Decision rule: a bad row is a data problem, so warn, drop, count it, and continue until a limit (my rule is 20 percent). A missing column or an empty batch is a pipeline problem, so raise `BadInputError`, which the caller catches by type.
- Never `except: pass` or `except Exception: pass`. It hides real bugs and the job "succeeds" with no output. Catch the specific error, log with `exc_info`, then re-raise or return a non-zero exit code so the scheduler marks the run failed.
- Do not log secrets or raw personal data. Log ids and counts. In real code the run id is generated per run (for example `uuid.uuid4().hex[:8]`); I fixed it here so the output is repeatable.

**Example:** Four batches. Good (5 rows): two INFO lines. Ragged (10 rows, 1 bad, 10 percent): a WARNING with `bad_ids: [2]`, then scored 9 rows. Bad (5 rows, 3 bad, 60 percent): a WARNING, then an ERROR and `BadInputError`. No `income` column: ERROR immediately. Process exit code is 1 because at least one batch was rejected.

**Code:** `python3 -I score_batch.py`
```python
import json, logging, sys
import pandas as pd

class JsonFormatter(logging.Formatter):
    def format(self, record):
        d = {"level": record.levelname, "logger": record.name, "msg": record.getMessage(), "run_id": RUN_ID}
        d.update(getattr(record, "ctx", {}))              # structured extras: row counts etc.
        if record.exc_info:
            d["exc"] = repr(record.exc_info[1])
        return json.dumps(d, sort_keys=True)

RUN_ID = "run-0001"     # fixed here so the output is reproducible; use uuid.uuid4().hex[:8] in real code
log = logging.getLogger("scoring")
h = logging.StreamHandler(sys.stdout); h.setFormatter(JsonFormatter())
log.addHandler(h); log.setLevel(logging.INFO); log.propagate = False

class BadInputError(ValueError):
    """The batch itself is unusable (missing column, empty). Stop the job."""

def score_batch(df: pd.DataFrame, max_bad_frac: float = 0.2) -> pd.DataFrame:
    log.info("batch received", extra={"ctx": {"rows_in": len(df)}})
    if "income" not in df.columns:
        raise BadInputError("missing column: income")        # specific exception, caller can alert on it
    if df.empty:
        raise BadInputError("empty batch")
    ok = df["income"].notna() & (df["income"] >= 0)
    n_bad = int((~ok).sum())
    if n_bad:
        log.warning("dropping bad rows", extra={"ctx": {"rows_bad": n_bad, "bad_ids": df.loc[~ok, "id"].tolist()}})
    if n_bad / len(df) > max_bad_frac:                        # a few bad rows: continue. Too many: stop.
        raise BadInputError(f"{n_bad}/{len(df)} bad rows exceeds limit {max_bad_frac:.0%}")
    out = df[ok].assign(score=lambda d: (d["income"] / 100).clip(upper=1.0))
    log.info("batch scored", extra={"ctx": {"rows_in": len(df), "rows_out": len(out), "rows_bad": n_bad}})
    return out

def main():
    batches = {
      "good":   pd.DataFrame({"id": range(1, 6), "income": [10., 50., 80., 120., 30.]}),
      "ragged": pd.DataFrame({"id": range(1, 11), "income": [10., None, 80., 120., 30., 5., 6., 7., 8., 9.]}),   # 1 bad of 10
      "bad":    pd.DataFrame({"id": range(1, 6), "income": [None, -5., None, 120., 30.]}),                        # 3 bad of 5
      "nocol":  pd.DataFrame({"id": [1, 2], "salary": [1., 2.]}),
    }
    code = 0
    for name, df in batches.items():
        print(f"--- batch: {name}")
        try:
            score_batch(df)
        except BadInputError as e:
            log.error("batch rejected", extra={"ctx": {"reason": str(e)}}, exc_info=True)
            code = 1                       # non-zero exit lets the scheduler mark the job failed
        # NOT: except Exception: pass   (hides real bugs, the job 'succeeds' with no output)
    return code

if __name__ == "__main__":
    sys.exit(main())
```

**Output (my run):** pandas 3.0.5.
```text
--- batch: good
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 5, "run_id": "run-0001"}
{"level": "INFO", "logger": "scoring", "msg": "batch scored", "rows_bad": 0, "rows_in": 5, "rows_out": 5, "run_id": "run-0001"}
--- batch: ragged
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 10, "run_id": "run-0001"}
{"bad_ids": [2], "level": "WARNING", "logger": "scoring", "msg": "dropping bad rows", "rows_bad": 1, "run_id": "run-0001"}
{"level": "INFO", "logger": "scoring", "msg": "batch scored", "rows_bad": 1, "rows_in": 10, "rows_out": 9, "run_id": "run-0001"}
--- batch: bad
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 5, "run_id": "run-0001"}
{"bad_ids": [1, 2, 3], "level": "WARNING", "logger": "scoring", "msg": "dropping bad rows", "rows_bad": 3, "run_id": "run-0001"}
{"exc": "BadInputError('3/5 bad rows exceeds limit 20%')", "level": "ERROR", "logger": "scoring", "msg": "batch rejected", "reason": "3/5 bad rows exceeds limit 20%", "run_id": "run-0001"}
--- batch: nocol
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 2, "run_id": "run-0001"}
{"exc": "BadInputError('missing column: income')", "level": "ERROR", "logger": "scoring", "msg": "batch rejected", "reason": "missing column: income", "run_id": "run-0001"}
exit=1
pandas 3.0.5
```

**Follow-ups:**
- *What do you alert on?* Job failed (exit code or ERROR count above 0), rows_bad fraction above the normal level, rows_out much lower than rows_in, and no `batch scored` line at all in the expected time window (silence is a failure too).
- *print vs logging in containers?* Log to stdout in JSON; the platform collects it. Logging handlers and formats stay in one place.
- *How do you trace one request?* The run id (batch) or request id (online) is on every line.

**Common mistakes:**
- `except Exception: pass` or `except: print("error")`.
- Logging inside a tight loop for each row, which floods the log and slows the job.
- Using ERROR for expected conditions, so the alert is always on and everyone ignores it.
- Logging free text with no ids, so you cannot link a message to a run.

### Q30 ⭐⭐ 🟡 Type hints and mypy for data and ML code. Explain what type hints buy you in a pandas and NumPy codebase (documentation, catching wrong arguments, IDE help) and what they cannot check (DataFrame columns, array shapes). Annotate a small feature function with typing and numpy.typing, run mypy on a version with a planted type error, and mention gradual adoption (strict only for new modules) and runtime checking with pydantic at the boundaries.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** Type hints document what a function takes and returns and let mypy catch wrong calls before runtime, but they cannot check DataFrame column names or array shapes, so I add runtime validation (pydantic or schema checks) at the boundaries.

**Then explain:**
- What they buy: a self-checking signature, IDE autocomplete and rename help, and mypy errors for calls like passing a list where an array is needed or a string where a float is needed.
- What they cannot check: which columns a `DataFrame` has, the shape or length of an array, value ranges, or NaN. `NDArray[np.float64]` checks dtype only. My run shows both `add_features(df_without_income)` and a 2-D array going through type checking and failing or misbehaving at runtime.
- Practical setup: install `pandas-stubs` (without it mypy complains about missing stubs for pandas, which my first run showed), and use `numpy.typing.NDArray`.
- Gradual adoption: start with loose settings on the old code (no failures from missing annotations), and use `--strict` or per-module strict overrides only for new modules. Fix errors as files are touched. Do not try to annotate everything in one week.
- Boundaries: validate config, API payloads and incoming data with pydantic or the validation function, then pass trusted typed objects inside the code.

**Example:** `features_bad.py` has four planted errors. mypy reports all four with exit code 1: `floor="1"` to `add_features`, a Python list to `log_income`, `floor="1"` to `log_income`, and assigning an array to an `int` variable. The good file passes, also under `--strict`.

**Code:** the typed module, the module with planted errors, and a script for what the type checker cannot see.
```python
# ===== file: features.py =====
import numpy as np
import numpy.typing as npt
import pandas as pd

FloatArray = npt.NDArray[np.float64]

def log_income(income: FloatArray, floor: float = 1.0) -> FloatArray:
    """log of income with a floor, so zeros do not give -inf."""
    return np.log(np.maximum(income, floor))

def add_features(df: pd.DataFrame, floor: float = 1.0) -> pd.DataFrame:
    out = df.copy()
    out["log_income"] = log_income(out["income"].to_numpy(dtype=np.float64), floor)
    return out

def mean_log_income(df: pd.DataFrame) -> float:
    return float(add_features(df)["log_income"].mean())

# ===== file: features_bad.py =====
import numpy as np
import numpy.typing as npt
import pandas as pd
from features import add_features

FloatArray = npt.NDArray[np.float64]

def log_income(income: FloatArray, floor: float = 1.0) -> FloatArray:
    return np.log(np.maximum(income, floor))

def run(df: pd.DataFrame) -> None:
    add_features(df, floor="1")             # ERROR: str where float expected
    log_income([1.0, 2.0])                  # ERROR: list is not an ndarray
    log_income(np.array([1.0]), floor="1")  # ERROR: str where float expected
    x: int = log_income(np.array([1.0]))    # ERROR: array assigned to int

# ===== file: runtime_traps.py =====
# things the type checker cannot see: both lines type-check, both fail or mislead at runtime
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I removes the script dir from sys.path
import numpy as np
import pandas as pd
from features import add_features, log_income

df = pd.DataFrame({"salary": [10.0, 20.0]})        # wrong column name: mypy is happy
try:
    add_features(df)
except KeyError as e:
    print("KeyError at runtime (mypy cannot see DataFrame columns):", e)
a = np.ones((3, 2))                               # wrong shape / dtype is also invisible to NDArray[float64]
print("2-D array accepted by a function meant for 1-D income:", log_income(a).shape)
```
```bash
python3 -I -m mypy features.py
python3 -I -m mypy features_bad.py
python3 -I -m mypy --strict features.py
python3 -I runtime_traps.py
```

**Output (my run):** mypy 2.4.0, numpy 2.5.3, pandas 3.0.5, pandas-stubs 3.0.5.260914. Error message wording and stub coverage change between versions (check current docs).
```text
$ mypy features.py
Success: no issues found in 1 source file
exit=0

$ mypy features_bad.py
features_bad.py:12: error: Argument "floor" to "add_features" has incompatible type "str"; expected "float"  [arg-type]
features_bad.py:13: error: Argument 1 to "log_income" has incompatible type "list[float]"; expected "ndarray[tuple[Any, ...], dtype[float64]]"  [arg-type]
features_bad.py:14: error: Argument "floor" to "log_income" has incompatible type "str"; expected "float"  [arg-type]
features_bad.py:15: error: Incompatible types in assignment (expression has type "ndarray[tuple[Any, ...], dtype[float64]]", variable has type "int")  [assignment]
Found 4 errors in 1 file (checked 1 source file)
exit=1

$ mypy --strict features.py   # what "strict for new modules" means
Success: no issues found in 1 source file
exit=0

$ python3 -I runtime_traps.py
KeyError at runtime (mypy cannot see DataFrame columns): 'income'
2-D array accepted by a function meant for 1-D income: (3, 2)
mypy 2.4.0 numpy 2.5.3 pandas 3.0.5
pandas-stubs              3.0.5.260914
```

**Follow-ups:**
- *Do hints slow code down?* No. Python ignores them at runtime. mypy is a separate step in CI or in pre-commit.
- *How do you type DataFrame columns?* mypy cannot. Options are a pandera schema or a pydantic or dataclass row type at the boundary. Treat them as runtime checks.
- *What about `Any`?* It switches checking off. Use it sparingly and mark it with a comment. A pile of `Any` gives false comfort.

**Common mistakes:**
- Adding hints and not running mypy in CI, so they rot.
- Believing `NDArray[np.float64]` checks shape.
- Forgetting pandas-stubs and ignoring all pandas errors with `ignore_missing_imports`.
- Turning on strict for the whole old codebase at once, then switching mypy off in frustration.

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

