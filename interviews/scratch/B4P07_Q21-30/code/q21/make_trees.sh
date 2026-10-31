set -e
T=$1; rm -rf "$T"; mkdir -p "$T/good/.github/workflows" "$T/good/configs" "$T/good/serving" "$T/bad/.github/workflows"
cd "$T/good"
cat > .github/workflows/ci.yml <<'Y'
name: ci
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python gate.py --config configs/gates.yaml
        env:
          REGISTRY_TOKEN: ${{ secrets.REGISTRY_TOKEN }}
Y
printf 'min_auc: 0.80\nmax_auc_drop: 0.005\nmax_p95_ms: 120\n' > configs/gates.yaml
printf 'FROM python:3.12-slim\n' > Dockerfile
printf 'apiVersion: apps/v1\nkind: Deployment\n' > serving/deployment.yaml
printf '/configs/ @ml-leads\n/models/ @ml-leads\n' > CODEOWNERS
cd "$T/bad"
cat > .github/workflows/ci.yml <<'Y'
name: ci
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python gate.py --threshold 0.80
        env:
          API_KEY: abcd1234efgh5678ijkl
          AWS_ID: AKIAABCDEFGHIJKLMNOP
Y
printf 'FROM python:3.12-slim\n' > Dockerfile
