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
