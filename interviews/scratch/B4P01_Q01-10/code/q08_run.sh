#!/usr/bin/env bash
# Q8: run the tests, then prove they catch a bug (mutation: sample std instead of population std)
D=$(dirname "$(readlink -f "$0")")/q08; T=$(mktemp -d); cp "$D"/prep.py "$D"/test_prep.py "$T"; cd "$T"
echo "=== correct code"; python3 -I -m pytest -q -p no:cacheprovider 2>&1 | tail -3
sed -i 's/std = s.std(ddof=0)/std = s.std()/' prep.py
echo "=== injected bug (std with ddof=1)"; python3 -I -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-110
rm -rf "$T"
