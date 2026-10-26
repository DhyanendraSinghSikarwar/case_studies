actionlint deploy.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows deploy.yml
python -I -c "import json; json.load(open('trust_policy.json')); print('trust policy: valid JSON')"
python -I sub_matcher.py
