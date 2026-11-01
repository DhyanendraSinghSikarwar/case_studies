actionlint release.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows release.yml
python -I list_envs.py
actionlint bad_env.yml; echo "bad exit=$?"
