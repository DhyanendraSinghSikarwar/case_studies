#!/usr/bin/env bash
# Q6: lose two commits with reset --hard, recover with reflog
set -e
. "$(dirname "$0")/env.sh"
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
