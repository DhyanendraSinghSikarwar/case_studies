from build_a import *

A[31] = f"""**Say this first (1 line):** For 8 teams I would pick a polyrepo with one shared, versioned package, owned through CODEOWNERS, and roll out breaking changes in two steps (add and deprecate, then remove); I would pick a monorepo only if we already have tooling that runs just the affected tests.

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
{block("bash", "q31/demo.sh")}

{block("python", "q31/ranges.py", "q31/shim.py")}

**Output (my run):** ({ENV}; the submodule demo uses local paths only, no GitHub)
{out("q31/out.txt")}
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
"""

A[32] = f"""**Say this first (1 line):** `git rm` only removes the file from the newest commit; the 2 GB blob stays in every old commit, so you rewrite history with `git filter-repo` in a fresh clone, force-push once, make everyone re-clone, and rotate any secret that was ever in it.

**Then explain:**
- Why `git rm` is not enough: history is a chain of snapshots. Old commits still point to the blob, so the repo stays huge and anyone can check out the old commit.
- filter-repo (fresh clone, `--invert-paths --path model.pkl`) rewrites every commit that touched the file. Every commit after it gets a new hash, so the whole branch changes. Commits that become empty are dropped. BFG Repo-Cleaner does a similar job (hedge: check which tool your team has approved; filter-repo is the one the Git docs point to).
- Everyone else: do not `git pull` the new history on top of old (it will merge both and bring the blob back). Re-clone, or reset hard to the new `origin/main` after saving unpushed work. Open pull requests and forks are based on old hashes, so rebase them onto the new history or recreate them. Forks and hosted pull-request refs may keep the old objects, so for a real incident ask the host (check current docs) to run garbage collection or purge cached views.
- Secrets: if the file held a key, assume it was copied. Rotate it first; rewriting is cleanup, not safety.
- Prevent it: `.gitignore`, a size-limit pre-commit hook, and an LFS or DVC rule for big files.

**Example:** The demo repo has 6 commits and a model file added in commit 2. After `git rm` the file is gone from the folder but 2 commits still touch it and the pack is about 19 MiB. After filter-repo the pack is about 2 KiB, history has 4 commits, and a teammate's old clone sees 6 commits only on their side and 4 only on the new side (diverged).

**Code:**
{block("bash", "q32/demo.sh")}

**Output (my run):** ({ENV}). The file is 20 MB of random bytes, not 2 GB, to keep the run fast; the mechanics are identical. Hashes differ on every run.
{out("q32/out.txt")}
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
"""

A[33] = f"""**Say this first (1 line):** Stash parks uncommitted changes (add `-u` to include untracked files), but with a long run reading your working directory the safer move is `git worktree add`, which gives the hotfix its own directory and branch while the run keeps its files untouched.

**Then explain:**
- `git stash` saves tracked changes and resets the working tree to HEAD. Plain `git stash` leaves untracked files behind; `-u` takes them; ignored files need `-a`. `git stash pop` brings them back, and can conflict if the base moved.
- The problem with stash here: it rewrites the files on disk. A 6-hour job that reads `train.py`, config or data from the folder would suddenly see different files. Switching branches in that folder has the same problem.
- `git worktree add ../proj-hotfix hotfix-null` creates a second working directory on a branch, sharing the same object store (no second clone, small cost). Commit and push the fix from there, then `git worktree remove`.
- Limits: one branch cannot be checked out in two worktrees at once; untracked or ignored data files (big datasets, `.env`) do not appear in the new worktree, so point it at the data by path or symlink.
- Stash is local and easy to forget: `git stash list` can hold old work for months. Name them with `git stash push -m "text"`.

**Example:** In the demo `train.py` has an experiment (`lr = 0.01`) and `notes.txt` is new. Plain stash leaves `notes.txt` in place; `stash -u` leaves a clean tree. Then the hotfix is committed in a sibling directory and the original `train.py` still says `lr = 0.01  # experiment`.

**Code:**
{block("bash", "q33/demo.sh")}

**Output (my run):** ({ENV})
{out("q33/out.txt")}

**Follow-ups:**
- *Could the run itself be made safe?* Yes: run training from a clean exported copy (a worktree or a tagged checkout) and log the commit hash, so working-directory edits never matter.
- *Where is a stash stored?* As commits under `refs/stash`, so it is not deleted by `git gc` quickly, but it is local and never pushed.
- *Stash versus a WIP commit?* A WIP commit on a branch is easier to share and find; squash it later.

**Common mistakes:**
- Forgetting `-u` and thinking everything was stashed.
- Switching branches under a running job.
- Leaving worktrees behind (use `git worktree remove` and `git worktree prune`).
- Assuming the new worktree has the ignored data files.
"""

A[34] = f"""**Say this first (1 line):** Branch protection plus required reviews, CODEOWNERS and required status checks stop an unreviewed or untested change reaching the deployable branch, and signed commits and tags make forged authorship detectable; each one closes a different hole.

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
{block("python", "q34/codeowners.py")}

**Output (my run):** ({ENV}). The GitHub or GitLab settings are not executed here (hosted services); the matcher is.
{out("q34/out.txt")}

**Follow-ups:**
- *How do you enforce it for admins too?* Turn on the "include administrators" style option or use organisation rulesets (check current docs).
- *Does CODEOWNERS replace reviews?* No, it only decides who must review.
- *Who owns the feature code if two teams share it?* List both owners on the line, as in the demo, so either-or review is not enough only if you require approval from each (check how your host counts).

**Common mistakes:**
- Creating a CODEOWNERS file but not switching on "require code owner review".
- Believing signed commits make code safe.
- Letting the default branch accept force-pushes.
- Putting the catch-all `*` line last, so it overrides every specific rule.
"""

A[35] = f"""**Say this first (1 line):** The test is flaky because an accuracy on 200 rows is a noisy number (standard error about 1.8 points here) and the split changes each run; seeding hides the noise, so the real fix is to set the threshold from the measured noise or test a property instead.

**Then explain:**
- Diagnose by repeating: run the same test 200 times and count failures. Here: unseeded split, 200 test rows, true accuracy near 0.93. The binomial standard error is sqrt(p(1-p)/n) = sqrt(0.928 x 0.072 / 200) = 0.018, so a 0.90 threshold is only 1.5 SE below the mean and fails about 5 percent of the time.
- Other causes: unseeded libraries, multi-threaded or GPU non-determinism, test data that drifts, tests that share state or depend on order.
- Fix 1, seed everything: makes it repeatable, but it only picks one draw. In the run, seed 42 gives 0.875 every time, so the test fails 100 percent of the time; the seed turned "sometimes red" into "always red". You must also re-calibrate the threshold.
- Fix 2, widen the tolerance with maths: threshold = expected accuracy minus 3 SE. Drawback: it now only catches big drops (here below 0.873).
- Fix 3, bigger fixed test set: 1000 rows cuts the SE to 0.7 points; the failures disappear at the same 0.90 threshold.
- Fix 4, test a property: "beats the majority-class baseline by 0.10" is stable and still catches a broken model. Pair it with a separate, non-blocking metric tracker for the exact number.

**Example:** n = 200, p = 0.93. SE = sqrt(0.93 x 0.07 / 200) = 0.0180. 0.90 is (0.93-0.90)/0.018 = 1.7 SE below: a one-sided tail near 5 percent. That matches the 5.5 percent measured.

**Code:**
{block("python", "q35/flaky.py")}

**Output (my run):** ({ENV}; seeds 0 to 199, so the numbers repeat)
{out("q35/out.txt")}

**Follow-ups:**
- *Should you retry flaky tests automatically?* Only as a stop-gap with a ticket; retries hide a real 5 percent failure rate.
- *Is a fixed seed ever the answer?* Yes for unit tests of logic (does the code run, shape, determinism), with the number-quality check kept separate.
- *What about GPU nondeterminism?* Use tolerances (`pytest.approx`) and, where the framework supports it, deterministic flags (check current docs); some ops stay non-deterministic.

**Common mistakes:**
- Fixing the symptom with a retry decorator.
- Picking a seed until the test goes green.
- Lowering the threshold with no reasoning (use SE).
- Comparing accuracy to a point value on a tiny test set.
"""
