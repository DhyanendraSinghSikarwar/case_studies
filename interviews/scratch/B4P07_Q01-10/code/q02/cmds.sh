actionlint q02_good.yml; echo "exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows q02_good.yml; echo "exit=$?"
actionlint q02_bad.yml; echo "exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows q02_bad.yml; echo "exit=$?"
python -I q02_on_trap.py
