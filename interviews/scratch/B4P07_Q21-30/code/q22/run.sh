V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
echo '$ python3 -I check_pipelines.py'; $V/python -I $D/check_pipelines.py $D/github-workflow.yml $D/.gitlab-ci.yml
echo '$ actionlint github-workflow.yml'; $V/actionlint $D/github-workflow.yml; echo "exit=$?"
echo '$ check-jsonschema --builtin-schema vendor.github-workflows github-workflow.yml'; $V/check-jsonschema --builtin-schema vendor.github-workflows $D/github-workflow.yml; echo "exit=$?"
