V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")"); cd $D
echo '$ python3 -I ci_cost.py'; $V/python -I ci_cost.py
echo '$ actionlint ci_fast.yml'; $V/actionlint ci_fast.yml; echo "exit=$?"
echo '$ check-jsonschema --builtin-schema vendor.github-workflows ci_fast.yml'; $V/check-jsonschema --builtin-schema vendor.github-workflows ci_fast.yml
