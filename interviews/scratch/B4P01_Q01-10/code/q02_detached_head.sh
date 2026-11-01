#!/usr/bin/env bash
# Q2: detached HEAD from an old tag, commit, save to a branch; status/diff/diff --staged; fetch vs pull
set -e
. "$(dirname "$0")/env.sh"
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
