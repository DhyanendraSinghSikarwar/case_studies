for f in ci train after_ci risky_target bad_triggers; do
  echo "== $f.yml"
  actionlint $f.yml; echo "actionlint exit=$?"
  check-jsonschema --builtin-schema vendor.github-workflows $f.yml; echo "schema exit=$?"
done
