#!/usr/bin/env bash
# Runs every qNN/cmds.sh in a fresh temp copy; writes ../out/qNN.txt (real output pasted into answers.md)
export PATH=/tmp/claude-0/b7p07/v/bin:$PATH MLFLOW_DISABLE_TELEMETRY=true PYTHONDONTWRITEBYTECODE=1
HERE=$(cd "$(dirname "$0")" && pwd); W=/tmp/claude-0/b7_q01_10/work; OUT=$HERE/../out
rm -rf "$W"; mkdir -p "$W" "$OUT"
for d in "$HERE"/q[0-9][0-9]; do
  n=$(basename "$d"); cp -r "$d" "$W/$n"; (cd "$W/$n" && PS4='$ ' bash -x ./cmds.sh 2>&1 | grep -v -e '^+ echo ' -e '^+ for ' | sed 's/^+ /$ /' > "$OUT/$n.txt")
done
