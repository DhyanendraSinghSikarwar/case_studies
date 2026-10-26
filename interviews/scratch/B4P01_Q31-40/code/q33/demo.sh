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
