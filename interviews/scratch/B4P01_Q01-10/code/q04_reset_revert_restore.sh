#!/usr/bin/env bash
# Q4: undo a pushed bad commit with revert; reset modes; restore a single file
set -e
. "$(dirname "$0")/env.sh"
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
