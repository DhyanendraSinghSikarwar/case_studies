V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")"); cd $D
for f in broken/bad_event.yml broken/missing_needs.yml broken/unknown_label.yml good_dispatch.yml; do
  echo "=== $f"
  echo "\$ actionlint $f"; $V/actionlint $f; echo "exit=$?"
  echo "\$ check-jsonschema --builtin-schema vendor.github-workflows $f"; $V/check-jsonschema --builtin-schema vendor.github-workflows $f; echo "exit=$?"
done
