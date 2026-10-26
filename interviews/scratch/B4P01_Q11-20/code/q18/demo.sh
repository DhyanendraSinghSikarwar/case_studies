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
