set -e
D=$(mktemp -d); cd "$D"
git init -q -b main; git config user.email a@b.c; git config user.name demo
printf 'def old(x):\n    return x + 1\n' > lib.py
printf 'from lib import old\n\ndef test_old():\n    assert old(1) == 2\n' > test_lib.py
git add .; git commit -qm base
# the PR adds an untested function and a tested one
printf '\ndef new_untested(x):\n    if x > 0:\n        return x * 2\n    return 0\n' >> lib.py
git commit -qam "add new_untested"
python3 -I -m pytest -q -p no:cacheprovider --cov=lib --cov-report=xml test_lib.py | tail -3
echo '$ diff-cover coverage.xml --compare-branch=main~1 --fail-under=80'
diff-cover coverage.xml --compare-branch=main~1 --fail-under=80 || echo "exit=$?"
