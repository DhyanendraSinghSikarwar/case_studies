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
