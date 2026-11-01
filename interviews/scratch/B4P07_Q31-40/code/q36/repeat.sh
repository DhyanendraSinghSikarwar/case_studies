#!/usr/bin/env bash
# usage: repeat.sh <test name> <runs>
fails=0
for i in $(seq 1 "$2"); do
  python -I -m pytest -q -p no:cacheprovider test_flaky.py -k "$1" >/dev/null 2>&1 || fails=$((fails+1))
done
echo "$1: $fails failures in $2 runs"
