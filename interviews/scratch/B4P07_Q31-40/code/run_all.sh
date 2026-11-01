#!/usr/bin/env bash
# Re-runs every demo; writes qNN/output.txt. Venv: /tmp/claude-0/b7p07/v. q36 repeat loop is run separately (slow).
export PATH=/tmp/claude-0/b7p07/v/bin:$PATH MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1
export TMPDIR=/tmp/claude-0/b7_q31_40/tmp; mkdir -p "$TMPDIR"
cd "$(dirname "$0")"
filt() { grep -v -i "warning\|^20[0-9][0-9]/\|^$" ; }

( cd q31
  for t in good bad; do echo "== scan $t"; python -I scan_workflows.py $t; echo "exit=$?"; done
  echo "== pickle demo"; python -I pickle_demo.py
  echo "== actionlint on the bad file"; actionlint bad/.github/workflows/ci.yml; echo "exit=$?"
  echo "== actionlint on the good file"; actionlint good/.github/workflows/ci.yml; echo "exit=$?"
) > q31/output.txt 2>&1

( cd q32
  printf 'model-weights-v1' > model.bin
  python -I make_sbom.py requirements.lock model.bin
  printf 'model-weights-v1' > model.bin
  echo "== sha256sum on the untouched file"; sha256sum model.bin
  echo "== actionlint sign.yml"; actionlint sign.yml; echo "exit=$?"
  echo "== check-jsonschema"; check-jsonschema --builtin-schema vendor.github-workflows sign.yml
  for t in cosign syft trivy; do command -v $t >/dev/null && echo "$t found" || echo "$t: not installed"; done
) > q32/output.txt 2>&1

( cd q33
  python -I gitops_demo.py application.yaml flux.yaml
  echo "== actionlint bump-config.yml"; actionlint bump-config.yml; echo "exit=$?"
) > q33/output.txt 2>&1

( cd q34
  echo "== pytest"; python -I -m pytest -q -p no:cacheprovider test_envpromo.py 2>&1 | tail -1
  echo "== demo"; python -I demo.py 2>&1 | filt | sed -E 's/"ts": [0-9.]+/"ts": <t>/'
) > q34/output.txt 2>&1

( cd q35
  python -I trace_demo.py 2>&1 | filt
  echo "== actionlint trace.yml"; actionlint trace.yml; echo "exit=$?"
) > q35/output.txt 2>&1

( cd q37
  for c in "models/churn/train.py
models/churn/README.md" "models/fraud/features.py
models/ltv/config.yaml
docs/index.md" "libs/common/metrics.py
models/ltv/config.yaml" "docs/index.md"; do echo "--- changed files:"; echo "$c" | sed 's/^/    /'; echo "$c" | python -I changed_models.py; done
  echo "== actionlint monorepo.yml"; actionlint monorepo.yml; echo "exit=$?"
  check-jsonschema --builtin-schema vendor.github-workflows monorepo.yml
) > q37/output.txt 2>&1

( cd q38
  echo "== actionlint, no config"; actionlint weekly-retrain.yml 2>&1 | cut -c1-110; 
  echo "== actionlint with actionlint.yaml (label train declared)"; actionlint -config-file actionlint.yaml weekly-retrain.yml; echo "exit=$?"
  check-jsonschema --builtin-schema vendor.github-workflows weekly-retrain.yml
  python -I -c "
import yaml
d = yaml.safe_load(open('weekly-retrain.yml'))
print('jobs:', ', '.join(d['jobs']))
print('top-level key types:', [type(k).__name__ for k in d])"
) > q38/output.txt 2>&1

( cd q39
  echo "== pytest"; python -I -m pytest -q -p no:cacheprovider test_oidc_diag.py 2>&1 | tail -1
  for f in no-permissions with-permissions; do echo "== $f.yml"; actionlint $f.yml; echo "actionlint exit=$?"; check-jsonschema --builtin-schema vendor.github-workflows $f.yml; done
  echo "== two live diagnoses"
  python -I -c "
import sys; sys.path.insert(0, '.')
from oidc_diag import diagnose
T = {'sub': ['repo:acme/churn:environment:production'], 'aud': 'sts.amazonaws.com', 'iss': 'https://token.actions.githubusercontent.com'}
for s in ['repo:acme/churn:ref:refs/heads/main', 'repo:acme/churn:pull_request']:
    print(s); [print('  ->', f) for f in diagnose({'sub': s, 'aud': T['aud'], 'iss': T['iss']}, T)]"
) > q39/output.txt 2>&1

( cd q40
  python -I eval_gate.py golden.jsonl; echo "exit=$?"
  python -I -m pytest -q -p no:cacheprovider test_eval_gate.py 2>&1 | tail -1
  echo "== a broken model (always 'I cannot help')"
  python -I -c "
import sys, json; sys.path.insert(0, '.')
import eval_gate as g
cases = [json.loads(l) for l in open('golden.jsonl')]
s, p = g.run_gate(cases, model=lambda q, seed: json.dumps({'answer': 'I cannot help', 'source': 'faq'}))
print({k: v for k, v in s.items() if k != 'notes'}); [print('FAIL:', x) for x in p]"
  echo "== actionlint llm-ci.yml"; actionlint llm-ci.yml; echo "exit=$?"
) > q40/output.txt 2>&1
find . -name __pycache__ -prune -exec rm -rf {} +; rm -rf q32/model.bin
echo done
