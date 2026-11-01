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
