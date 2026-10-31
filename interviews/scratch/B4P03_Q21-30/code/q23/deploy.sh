#!/usr/bin/env bash
# CI-style release sequence. NOT executed in this sandbox (no helm, no cluster).
set -euo pipefail
ENV="${1:?usage: deploy.sh dev|prod}"
RELEASE=model-api
NS="ml-${ENV}"

helm lint ./chart -f "values-${ENV}.yaml"                         # chart + schema errors
helm template "$RELEASE" ./chart -f "values-${ENV}.yaml" > rendered.yaml
kubernetes-validate --strict rendered.yaml                           # offline schema check (pip install kubernetes-validate)
helm diff upgrade "$RELEASE" ./chart -n "$NS" -f "values-${ENV}.yaml"   # needs the helm-diff plugin
helm upgrade --install "$RELEASE" ./chart -n "$NS" --create-namespace \
  -f "values-${ENV}.yaml" --atomic --wait --timeout 10m           # --atomic rolls back on failure
helm history "$RELEASE" -n "$NS" --max 5
# Manual escape hatch if a bad release got through:
#   helm rollback "$RELEASE" <REVISION> -n "$NS" --wait
