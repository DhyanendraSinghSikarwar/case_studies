pytest -m "not slow" -q -p no:cacheprovider
pytest -m slow -q -p no:cacheprovider
actionlint ci.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows ci.yml
