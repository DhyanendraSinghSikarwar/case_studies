#!/usr/bin/env bash
# Q9: pyramid layers as pytest markers; run each layer, show counts and timings
D=$(dirname "$(readlink -f "$0")")/q09; T=$(mktemp -d); cp "$D"/*.py "$T"; cd "$T"
for m in unit data model integration; do
  printf "%-12s" "-m $m:"; python3 -I -m pytest -q -p no:cacheprovider -m $m 2>&1 | tail -1
done
printf "%-12s" "all:"; python3 -I -m pytest -q -p no:cacheprovider 2>&1 | tail -1
echo "--- per-PR selection: -m 'unit or data'"; python3 -I -m pytest -q -p no:cacheprovider -m "unit or data" 2>&1 | tail -1
echo "--- silent data change: monthly_spend arrives in paise (x100); no exception anywhere in the code"
sed -i 's/rng.normal(60, 15, n).round(2)/(rng.normal(60, 15, n) * 100).round(2)/' churn.py
python3 -I -m pytest -q -p no:cacheprovider -m data 2>&1 | grep -E "^FAILED|passed|failed"
python3 -I -m pytest -q -p no:cacheprovider -m unit 2>&1 | tail -1 | sed "s/^/unit tests, same broken data: /"
rm -rf "$T"
