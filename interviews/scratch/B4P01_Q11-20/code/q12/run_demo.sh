#!/bin/sh
# copies this folder to a temp git repo and runs pre-commit there (nothing touches the main repo)
T=$(mktemp -d); cp -r "$(dirname "$0")"/. "$T"/; cd "$T"
git init -q; git config user.email a@b.c; git config user.name demo; git add -A
pre-commit install
echo "== 1. normal commit"; out=$(git commit -q -m "bad file" 2>&1); rc=$?; echo "$out" | grep -E "Failed|Passed|train.py:[0-9]+:[0-9]+: (B006|F841)|error:"; echo "git commit exit code: $rc (blocked)"
echo "== 2. same commit with --no-verify"; git commit -q --no-verify -m "bad file"; echo "git commit exit code: $?  (hooks skipped, bad file is now in history)"
echo "== 3. CI-style run of the same checks"; ruff check -q --output-format=concise . ; echo "ruff exit: $?"
