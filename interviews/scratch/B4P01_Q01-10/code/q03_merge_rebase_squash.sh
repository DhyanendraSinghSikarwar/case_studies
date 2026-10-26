#!/usr/bin/env bash
# Q3: three strategies, same 3-commit situation. main has 1 commit after the branch point; feature has 3.
set -e
. "$(dirname "$0")/env.sh"
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
