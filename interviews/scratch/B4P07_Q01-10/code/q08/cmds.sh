actionlint cache.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows cache.yml
python -I cache_key.py
