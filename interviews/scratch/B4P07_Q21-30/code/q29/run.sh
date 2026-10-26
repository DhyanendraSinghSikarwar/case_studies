V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")"); cd $D
echo '$ actionlint ci.yml'; $V/actionlint ci.yml; echo "exit=$?"
echo '$ check-jsonschema --builtin-schema vendor.github-workflows ci.yml'; $V/check-jsonschema --builtin-schema vendor.github-workflows ci.yml; echo "exit=$?"
echo "\$ python3 -I summary_rule.py"; $V/python -I summary_rule.py
